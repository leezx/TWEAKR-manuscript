#!/usr/bin/env python3
"""Export raw counts per sample (cohort v1) for CytoTRACE2 runs.

One HDF5 file per (study, patient, sample) with a CSC genes x cells matrix restricted to Atlas genes
that map to a CytoTRACE2 1.1.0 model feature. CytoTRACE2 drops every other gene in preprocessing, so
the restriction does not change its input (checked on one sample in the pilot with all genes).

Depth-matched variant (contract A2): with --depth-targets, cells whose library size (all genes) is
below the study target T_s are dropped, and every other cell is downsampled to exactly T_s UMI
without replacement (multivariate hypergeometric over its genes), once per seed, before the
restriction to model genes.

A2.1 diagnostic variants:
  --selection-only : with --depth-targets, keep cells >= T_s with their ORIGINAL counts ("sel"), to
                     separate the selection effect (dropping shallow cells) from the depth effect.
  --pool-by-patient: one file per patient with >= 2 samples, all samples concatenated ("patientpool").

Usage: python export_sample_counts.py --h5ad ... --cohort-cells ... --mapping ... --studies A,B --out-dir ...
       [--depth-targets depth_targets.csv --seeds 1,2,3,4,5]
"""
import argparse
import re
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

BLOCK = 20000


def dec(x):
    return x.decode() if isinstance(x, bytes) else str(x)


def safe(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--cohort-cells", required=True)
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--studies", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--all-genes-sample", default="", help="one sample_id also exported with all genes")
    ap.add_argument("--depth-targets", default="", help="depth_targets.csv; exports downsampled variants only")
    ap.add_argument("--seeds", default="1,2,3,4,5")
    ap.add_argument("--selection-only", action="store_true")
    ap.add_argument("--pool-by-patient", action="store_true")
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    cohort = pd.read_csv(a.cohort_cells, sep="\t")
    cohort = cohort[cohort.study_id.isin(a.studies.split(","))]
    mapping = pd.read_csv(a.mapping, sep="\t")
    targets = {}
    if a.depth_targets:
        t = pd.read_csv(a.depth_targets)
        targets = t[t.target == "T_s"].set_index("study").umi.to_dict()
    with h5py.File(a.h5ad, "r") as f:
        obs = f["obs"]
        idx = pd.Index([dec(x) for x in obs[obs.attrs["_index"]][:]])
        genes = np.array([dec(x) for x in f["var"]["var_names"][:]], dtype=object)
        if len(mapping) != len(genes) or not (mapping.original_gene.str.replace("-", ".") ==
                                                pd.Series(genes).str.replace("-", ".")).all():
            raise ValueError("mapping table is not aligned with Atlas var_names")
        keep_genes = np.flatnonzero(mapping.model_feature.to_numpy())
        cohort = cohort.assign(row=idx.get_indexer(cohort.cell_id))
        if (cohort.row < 0).any():
            raise ValueError("cohort cells missing from H5AD")
        mat = f["layers/counts"]
        indptr = mat["indptr"][:]
        n_genes = int(mat.attrs["shape"][1])
        manifest = []
        if a.pool_by_patient:
            multi = cohort.groupby("patient_id").sample_id.nunique()
            cohort = cohort[cohort.patient_id.isin(multi[multi >= 2].index)].copy()
            cohort["sample_id"] = cohort.patient_id + ".POOLED"
        for (study, patient, sample), g in cohort.groupby(["study_id", "patient_id", "sample_id"]):
            rows = np.sort(g.row.to_numpy())
            parts = []
            for b in np.unique(rows // BLOCK):
                r = rows[rows // BLOCK == b]
                start, end = int(r.min()), int(r.max()) + 1
                lo, hi = int(indptr[start]), int(indptr[end])
                x = csr_matrix((mat["data"][lo:hi], mat["indices"][lo:hi], indptr[start:end + 1] - lo),
                               shape=(end - start, n_genes))
                parts.append(x[r - start])
            from scipy.sparse import vstack
            x = vstack(parts).tocsr()
            cells = idx[rows].to_numpy()
            if targets and a.selection_only:
                lib = np.asarray(x.sum(axis=1)).ravel()
                keep = np.flatnonzero(lib >= targets[study])
                variants = [("sel", keep_genes, x[keep].tocsr(), cells[keep])]
            elif a.pool_by_patient:
                variants = [("patientpool", keep_genes, x, cells)]
            elif targets:
                lib = np.asarray(x.sum(axis=1)).ravel()
                keep = np.flatnonzero(lib >= targets[study])
                variants = []
                for seed in [int(v) for v in a.seeds.split(",")]:
                    rng = np.random.default_rng(seed)
                    xs = x[keep].tocsr().astype(np.int64)
                    for i in range(xs.shape[0]):
                        lo, hi = xs.indptr[i], xs.indptr[i + 1]
                        xs.data[lo:hi] = rng.multivariate_hypergeometric(xs.data[lo:hi], targets[study])
                    xs.eliminate_zeros()
                    variants.append((f"ds{seed}", keep_genes, xs, cells[keep]))
            else:
                variants = [("model", keep_genes, x, cells)]
                if sample == a.all_genes_sample:
                    variants.append(("allgenes", np.arange(n_genes), x, cells))
            for tag, cols, xv, cv in variants:
                y = xv[:, cols].T.tocsc()  # genes x cells
                name = f"{safe(sample)}.{tag}.h5"
                with h5py.File(out / name, "w") as h:
                    h["data"] = y.data.astype(np.int32)
                    h["indices"] = y.indices.astype(np.int32)
                    h["indptr"] = y.indptr.astype(np.int64)
                    h["shape"] = np.array(y.shape, dtype=np.int64)
                    h["genes"] = np.array(genes[cols], dtype="S")
                    h["cells"] = np.array(cv, dtype="S")
                manifest.append({"study_id": study, "patient_id": patient, "sample_id": sample,
                                 "variant": tag, "file": name, "cells": len(cv), "genes": len(cols)})
            print(study, sample, len(cells), flush=True)
    pd.DataFrame(manifest).to_csv(out / "export_manifest.tsv", sep="\t", index=False)
    lineage = cohort[["cell_id", "study_id", "patient_id", "sample_id", "lineage", "broad"]]
    lineage.to_csv(out / "cell_labels.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
