#!/usr/bin/env python3
"""A3a step 1 (one SGE task per study): all-gene epithelial counts, covariates, P2/P3 inputs.

Per cohort-v1 sample (frozen contract A3a v0.2):
  - main: raw counts of L1 Epithelial cells over all Atlas genes (GENCODE v44 space) -> <sample>.main.h5
  - ds1..ds5: the Fig. 1b depth-matched counts, regenerated over ALL genes with the identical procedure
    as export_sample_counts.py (same cells, same row order, same seed, multivariate hypergeometric to
    T_s on all genes). The restriction to CT2 model genes is checked to equal the exported Fig. 1b
    ds file exactly (verify_ds column); a mismatch stops the task.
  - per-cell covariates (main and ds): total UMI, detected genes, mito fraction (MT- genes) from the
    counts used; S/G2M score and phase from the Atlas obs.
  - P2: TNFRSF12A counts per epithelial cell.
  - P3: per-sample macrophage (L2 Macrophage) TNFSF12 pseudobulk and detection.
No CytoTRACE2 is run and no CT2 score is read here.
"""
import argparse
import re
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix, csr_matrix, vstack

BLOCK = 20000
SEEDS = [1, 2, 3, 4, 5]


def dec(x):
    return x.decode() if isinstance(x, bytes) else str(x)


def safe(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", s)


def read_obs_col(obs, key):
    g = obs[key]
    if isinstance(g, h5py.Group):
        cats = np.array([dec(c) for c in g["categories"][:]], dtype=object)
        codes = g["codes"][:]
        out = np.full(codes.shape, "NA", dtype=object)
        out[codes >= 0] = cats[codes[codes >= 0]]
        return out
    return g[:]


def rows_matrix(mat, indptr, rows, n_genes):
    parts = []
    for b in np.unique(rows // BLOCK):
        r = rows[rows // BLOCK == b]
        start, end = int(r.min()), int(r.max()) + 1
        lo, hi = int(indptr[start]), int(indptr[end])
        x = csr_matrix((mat["data"][lo:hi], mat["indices"][lo:hi], indptr[start:end + 1] - lo),
                       shape=(end - start, n_genes))
        parts.append(x[r - start])
    return vstack(parts).tocsr()


def write_h5(path, x_cells_by_genes, genes, cells):
    y = x_cells_by_genes.T.tocsc()
    with h5py.File(path, "w") as h:
        h["data"] = y.data.astype(np.int32)
        h["indices"] = y.indices.astype(np.int32)
        h["indptr"] = y.indptr.astype(np.int64)
        h["shape"] = np.array(y.shape, dtype=np.int64)
        h["genes"] = np.array(genes, dtype="S")
        h["cells"] = np.array(cells, dtype="S")


def covariates(x, mt_cols, tn_col):
    umi = np.asarray(x.sum(axis=1)).ravel()
    genes = np.diff(x.indptr)
    mt = np.asarray(x[:, mt_cols].sum(axis=1)).ravel()
    tn = np.asarray(x[:, tn_col].todense()).ravel()
    return umi, genes, np.divide(mt, umi, out=np.zeros_like(mt, dtype=float), where=umi > 0), tn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--cohort-cells", required=True)
    ap.add_argument("--annotation", required=True)
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--depth-targets", required=True)
    ap.add_argument("--fig1b-ds-dir", required=True)
    ap.add_argument("--study", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    out = Path(a.out_dir)
    (out / "counts").mkdir(parents=True, exist_ok=True)
    (out / "cells").mkdir(parents=True, exist_ok=True)

    cohort = pd.read_csv(a.cohort_cells, sep="\t")
    cohort = cohort[cohort.study_id == a.study]
    ann = pd.read_csv(a.annotation, sep="\t", usecols=["cell_id", "celltype_L1", "celltype_L2", "F1"])
    ann = ann[ann.cell_id.isin(cohort.cell_id)].set_index("cell_id")
    mapping = pd.read_csv(a.mapping, sep="\t")
    model_cols = np.flatnonzero(mapping.model_feature.to_numpy())
    t = pd.read_csv(a.depth_targets)
    ts = int(t[(t.target == "T_s") & (t.study == a.study)].umi.iloc[0])

    rows_out, macro_out, verify = [], [], []
    with h5py.File(a.h5ad, "r") as f:
        obs = f["obs"]
        idx = pd.Index([dec(x) for x in obs[obs.attrs["_index"]][:]])
        genes = np.array([dec(x) for x in f["var"]["var_names"][:]], dtype=object)
        s_score = read_obs_col(obs, "S_score")
        g2m = read_obs_col(obs, "G2M_score")
        phase = read_obs_col(obs, "phase")
        mt_cols = np.flatnonzero(pd.Series(genes).str.startswith("MT-").to_numpy())
        tn_col = int(np.flatnonzero(genes == "TNFRSF12A")[0])
        tw_col = int(np.flatnonzero(genes == "TNFSF12")[0])
        cohort = cohort.assign(row=idx.get_indexer(cohort.cell_id))
        if (cohort.row < 0).any():
            raise ValueError("cohort cells missing from H5AD")
        mat = f["layers/counts"]
        indptr = mat["indptr"][:]
        n_genes = int(mat.attrs["shape"][1])
        for (study, patient, sample), g in cohort.groupby(["study_id", "patient_id", "sample_id"]):
            rows = np.sort(g.row.to_numpy())
            x = rows_matrix(mat, indptr, rows, n_genes)
            cells = idx[rows].to_numpy()
            l1 = ann.reindex(cells).celltype_L1.to_numpy()
            l2 = ann.reindex(cells).celltype_L2.to_numpy()
            f1 = ann.reindex(cells).F1.to_numpy()
            epi = l1 == "Epithelial"
            # P3 inputs: macrophage pseudobulk
            mac = l2 == "Macrophage"
            xm = x[mac]
            macro_out.append({"study_id": study, "patient_id": patient, "sample_id": sample,
                              "cells_total": len(cells), "macrophage_cells": int(mac.sum()),
                              "macrophage_umi": int(xm.sum()), "macrophage_TNFSF12_umi": int(xm[:, tw_col].sum()),
                              "macrophage_TNFSF12_detected": int((xm[:, tw_col] > 0).sum())})
            if epi.sum() == 0:
                continue
            tag = safe(sample)
            # main
            xe = x[epi]
            write_h5(out / "counts" / f"{tag}.main.h5", xe, genes, cells[epi])
            umi, ng, mtf, tn = covariates(xe, mt_cols, tn_col)
            r = rows[epi]
            rows_out.append(pd.DataFrame({
                "cell_id": cells[epi], "study_id": study, "patient_id": patient, "sample_id": sample,
                "variant": "main", "F1": f1[epi], "celltype_L2": l2[epi], "umi": umi, "genes": ng,
                "mito_frac": mtf, "TNFRSF12A_umi": tn, "S_score": s_score[r], "G2M_score": g2m[r],
                "phase": phase[r]}))
            # ds: regenerate exactly as export_sample_counts.py (all cohort cells of the sample, sorted rows)
            lib = np.asarray(x.sum(axis=1)).ravel()
            keep = np.flatnonzero(lib >= ts)
            for seed in SEEDS:
                rng = np.random.default_rng(seed)
                xs = x[keep].tocsr().astype(np.int64)
                for i in range(xs.shape[0]):
                    lo, hi = xs.indptr[i], xs.indptr[i + 1]
                    xs.data[lo:hi] = rng.multivariate_hypergeometric(xs.data[lo:hi], ts)
                xs.eliminate_zeros()
                # verify against the Fig. 1b exported ds file (model genes)
                fpath = Path(a.fig1b_ds_dir) / f"{tag}.ds{seed}.h5"
                with h5py.File(fpath, "r") as h:
                    ref = csc_matrix((h["data"][:], h["indices"][:], h["indptr"][:]), shape=tuple(h["shape"][:]))
                    ref_cells = np.array([dec(c) for c in h["cells"][:]])
                mine = xs[:, model_cols].T.tocsc()
                ok = (np.array_equal(ref_cells, cells[keep]) and ref.shape == mine.shape
                      and (ref != mine).nnz == 0)
                verify.append({"sample_id": sample, "seed": seed, "cells": len(keep), "identical": bool(ok)})
                if not ok:
                    raise ValueError(f"ds regeneration mismatch: {sample} seed {seed}")
                ek = epi[keep]
                if ek.sum() == 0:
                    continue
                xse = xs[ek].tocsr()
                write_h5(out / "counts" / f"{tag}.ds{seed}.h5", xse, genes, cells[keep][ek])
                umi, ng, mtf, tn = covariates(xse, mt_cols, tn_col)
                r = rows[keep][ek]
                rows_out.append(pd.DataFrame({
                    "cell_id": cells[keep][ek], "study_id": study, "patient_id": patient, "sample_id": sample,
                    "variant": f"ds{seed}", "F1": f1[keep][ek], "celltype_L2": l2[keep][ek], "umi": umi,
                    "genes": ng, "mito_frac": mtf, "TNFRSF12A_umi": tn, "S_score": s_score[r],
                    "G2M_score": g2m[r], "phase": phase[r]}))
            print(study, sample, int(epi.sum()), len(keep), flush=True)
    st = safe(a.study)
    pd.concat(rows_out).to_csv(out / "cells" / f"{st}.cells.tsv.gz", sep="\t", index=False)
    pd.DataFrame(macro_out).to_csv(out / "cells" / f"{st}.macrophage.tsv", sep="\t", index=False)
    pd.DataFrame(verify).to_csv(out / "cells" / f"{st}.ds_verify.tsv", sep="\t", index=False)
    (out / "cells" / f"{st}.DONE").write_text("ok\n")


if __name__ == "__main__":
    main()
