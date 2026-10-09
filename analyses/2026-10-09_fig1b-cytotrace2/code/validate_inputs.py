#!/usr/bin/env python3
"""CytoTRACE2 input validation for the frozen Fig. 1B cohort (v1; no CytoTRACE2 run).

For every cohort cell, reads its row of the Atlas `layers/counts` (CSR) and checks:
  - counts are finite, non-negative integers (CytoTRACE2 expects raw counts);
  - per-cell library size (UMI total) and number of detected genes;
and per study, the number of cells in which each gene is detected (count > 0). Genes never
detected in a study are candidates for "not measured" by that study's reference/gene annotation,
which CytoTRACE2 cannot distinguish from "not expressed" (it fills missing model genes with 0).

Outputs (heavy, Argos): per-cell QC table; per-study gene detection table.
"""
import argparse
import gzip
import json
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

BLOCK = 20000


def dec(x):
    return x.decode() if isinstance(x, bytes) else str(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--cohort-cells", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    cohort = pd.read_csv(a.cohort_cells, sep="\t")
    with h5py.File(a.h5ad, "r") as f:
        obs = f["obs"]
        idx = pd.Index([dec(x) for x in obs[obs.attrs["_index"]][:]])
        var = f["var"]
        genes = np.array([dec(x) for x in var["var_names"][:]], dtype=object)
        ensembl = np.array([dec(x) for x in var[var.attrs["_index"]][:]], dtype=object)
        row = idx.get_indexer(cohort.cell_id)
        if (row < 0).any():
            raise ValueError(f"{(row < 0).sum()} cohort cells not found in the H5AD")
        cohort["row"] = row
        cohort = cohort.sort_values("row").reset_index(drop=True)

        mat = f["layers/counts"]
        if dec(mat.attrs["encoding-type"]) != "csr_matrix":
            raise ValueError("counts layer is not CSR")
        n_genes = int(mat.attrs["shape"][1])
        indptr = mat["indptr"][:]
        studies = sorted(cohort.study_id.unique())
        s_index = {s: i for i, s in enumerate(studies)}
        detect = np.zeros((len(studies), n_genes), dtype=np.int64)
        lib = np.zeros(len(cohort))
        ngene = np.zeros(len(cohort), dtype=np.int64)
        bad_values = 0

        rows = cohort.row.to_numpy()
        study_code = cohort.study_id.map(s_index).to_numpy()
        blocks = rows // BLOCK
        for b in np.unique(blocks):
            sel = np.flatnonzero(blocks == b)
            start, end = int(b * BLOCK), int(min((b + 1) * BLOCK, len(indptr) - 1))
            lo, hi = int(indptr[start]), int(indptr[end])
            x = csr_matrix((mat["data"][lo:hi], mat["indices"][lo:hi], indptr[start:end + 1] - lo),
                           shape=(end - start, n_genes))[rows[sel] - start]
            d = x.data
            bad_values += int(np.sum(~np.isfinite(d) | (d < 0) | (np.abs(d - np.rint(d)) > 1e-6)))
            lib[sel] = np.asarray(x.sum(axis=1)).ravel()
            ngene[sel] = np.diff(x.indptr)
            for code in np.unique(study_code[sel]):
                m = study_code[sel] == code
                xs = x[np.flatnonzero(m)]
                detect[code] += np.bincount(xs.indices, minlength=n_genes)
            print("block", b, "cells", len(sel), flush=True)

    cohort["library_size"] = lib
    cohort["n_genes_detected"] = ngene
    with gzip.open(out / "cohort_cell_qc.tsv.gz", "wt") as h:
        cohort.drop(columns="row").to_csv(h, sep="\t", index=False)
    det = pd.DataFrame(detect.T, columns=studies)
    det.insert(0, "gene", genes)
    det.insert(1, "ensembl", ensembl)
    with gzip.open(out / "study_gene_detection.tsv.gz", "wt") as h:
        det.to_csv(h, sep="\t", index=False)

    summary = {
        "cohort_cells": len(cohort), "non_integer_or_negative_values": bad_values,
        "zero_library_cells": int((lib == 0).sum()), "atlas_genes": n_genes,
        "genes_detected_per_study": {s: int((detect[i] > 0).sum()) for s, i in s_index.items()},
    }
    (out / "validate_inputs_summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
