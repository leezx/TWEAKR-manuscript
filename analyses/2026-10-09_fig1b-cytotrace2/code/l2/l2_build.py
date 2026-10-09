#!/usr/bin/env python3
"""Step 1 (r4p3): lineage objects, F1 marker-contradiction flags, L1 cross-check.

Reads cohort v1 cells from the Atlas counts layer (CSR) and writes one H5AD per lineage
(raw counts, all genes). Cells with cohort `broad == Other` are counted, never annotated.
"""
import argparse
import json

import anndata as ad
import h5py
import numpy as np
import pandas as pd
from scipy import sparse

from l2_common import LINEAGES, MARKER_LINEAGE_TO_L1, dec, load_cfg, read_h5_col, run_paths

OBS_COLS = ["atlas_cell_type_fine", "atlas_cell_type_middle", "cell_type_study", "SOLO_doublet_prob",
            "S_score", "G2M_score", "microsatellite_status"]
MAX_SLAB = 100_000_000  # non-zeros read per H5 slab


def smoke_subset(cohort, n_studies, n_patients):
    sizes = cohort.groupby("study_id").size().sort_values()
    keep = []
    for s in sizes.index[:n_studies]:
        pats = sorted(cohort.loc[cohort.study_id == s, "patient_id"].unique())[:n_patients]
        keep += pats
    return cohort[cohort.patient_id.isin(keep)].copy()


def read_rows(mat, rows):
    """CSR rows (sorted ascending) of an H5AD sparse group -> scipy CSR."""
    indptr = mat["indptr"][:]
    n_genes = int(mat.attrs["shape"][1])
    data_parts, ind_parts, lens = [], [], []
    i = 0
    while i < len(rows):
        j = i
        while j + 1 < len(rows) and indptr[rows[j + 1] + 1] - indptr[rows[i]] <= MAX_SLAB:
            j += 1
        lo, hi = indptr[rows[i]], indptr[rows[j] + 1]
        d = mat["data"][lo:hi]
        x = mat["indices"][lo:hi]
        for r in rows[i:j + 1]:
            a, b = indptr[r] - lo, indptr[r + 1] - lo
            data_parts.append(d[a:b])
            ind_parts.append(x[a:b])
            lens.append(b - a)
        i = j + 1
    ptr = np.concatenate([[0], np.cumsum(lens)])
    return sparse.csr_matrix((np.concatenate(data_parts).astype(np.float32),
                              np.concatenate(ind_parts), ptr), shape=(len(rows), n_genes))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    P = run_paths(a.run_root)

    cohort = pd.read_csv(cfg["paths"]["cohort_cells"], sep="\t")
    if a.smoke:
        st = cfg["smoke_test"]
        cohort = smoke_subset(cohort, st["n_studies"], st["n_patients_per_study"])
    print("cells", len(cohort), flush=True)

    with h5py.File(cfg["paths"]["h5ad"], "r") as f:
        obs = f["obs"]
        idx = pd.Index([dec(x) for x in obs[obs.attrs["_index"]][:]])
        row = idx.get_indexer(cohort.cell_id)
        if (row < 0).any():
            raise ValueError(f"{(row < 0).sum()} cohort cells missing from H5AD")
        cohort["row"] = row
        cohort = cohort.sort_values("row").reset_index(drop=True)
        for c in OBS_COLS:
            cohort[c] = read_h5_col(obs, c, cohort.row.to_numpy())
        var = f["var"]
        genes = pd.DataFrame({
            "symbol": read_h5_col(var, "var_names"),
            "Chromosome": read_h5_col(var, "Chromosome"),
            "Start": read_h5_col(var, "Start"),
            "End": read_h5_col(var, "End"),
        })
        if dec(f["layers/counts"].attrs["encoding-type"]) != "csr_matrix":
            raise ValueError("counts layer is not CSR")
        X = read_rows(f["layers/counts"], cohort.row.to_numpy())
    genes.index = pd.Index(genes.symbol.astype(str))
    if genes.index.duplicated().any():
        genes.index = ad.utils.make_index_unique(genes.index)
    gpos = {g: i for i, g in enumerate(genes.index)}

    # independent marker lineage (cross-check and F2 input)
    ml = []
    for s in sorted(cohort.study_id.unique()):
        fn = f"{cfg['paths']['marker_lineage_dir']}/{s}_lineage.tsv.gz"
        try:
            t = pd.read_csv(fn, sep="\t", usecols=["cell", "Lineage_cell", "Lineage_margin"])
        except FileNotFoundError:
            print("WARNING no marker lineage for", s, flush=True)
            continue
        ml.append(t[t.cell.isin(cohort.cell_id)])
    ml = pd.concat(ml).drop_duplicates("cell").set_index("cell")
    cohort["marker_lineage"] = ml.Lineage_cell.reindex(cohort.cell_id).to_numpy()
    cohort["marker_lineage_L1"] = cohort.marker_lineage.map(MARKER_LINEAGE_TO_L1)

    # F1: >= f1_min_genes genes of a foreign panel, each >= f1_min_umi UMI
    fl = cfg["l1_flags"]
    cohort["F1"] = False
    cohort["F1_panels"] = ""
    for name, spec in fl["panels"].items():
        cols = [gpos[g] for g in spec["genes"] if g in gpos]
        hit = np.asarray((X[:, cols] >= fl["f1_min_umi"]).sum(axis=1)).ravel() >= fl["f1_min_genes"]
        foreign = cohort.broad.isin(LINEAGES) & (cohort.broad != spec["lineage"])
        h = hit & foreign.to_numpy()
        cohort.loc[h, "F1"] = True
        cohort.loc[h, "F1_panels"] = cohort.loc[h, "F1_panels"] + name + ";"

    # lineage objects (all genes, raw counts)
    var = genes.drop(columns="symbol")
    for lin in LINEAGES:
        m = (cohort.broad == lin).to_numpy()
        o = cohort.loc[m, ["cell_id", "study_id", "patient_id", "sample_id", "platform", "broad",
                           "atlas_cell_type_fine", "cell_type_study", "F1"]].copy()
        o.index = pd.Index(o.cell_id.astype(str))
        for c in o.columns:
            if o[c].dtype == object:
                o[c] = o[c].astype(str)
        obj = ad.AnnData(X=X[m], obs=o, var=var.astype(str))
        obj.write_h5ad(P["objects"] / f"{lin}.h5ad")
        print(lin, obj.shape, flush=True)

    cols = ["cell_id", "study_id", "patient_id", "sample_id", "platform", "broad", "F1", "F1_panels",
            "marker_lineage", "marker_lineage_L1"] + OBS_COLS
    cohort[cols].to_csv(P["cells"] / "l1_cells.tsv.gz", sep="\t", index=False)

    f1 = cohort[cohort.broad.isin(LINEAGES)].groupby(["study_id", "broad"]).agg(
        n_cells=("F1", "size"), n_F1=("F1", "sum")).reset_index()
    f1["frac_F1"] = f1.n_F1 / f1.n_cells
    f1.to_csv(P["light"] / "l1_F1_by_study_lineage.csv", index=False)
    xc = pd.crosstab([cohort.study_id, cohort.broad], cohort.marker_lineage.fillna("NA")).reset_index()
    xc.to_csv(P["light"] / "l1_crosscheck_atlas_vs_marker_lineage.csv", index=False)
    other = cohort[cohort.broad == "Other"].groupby(["study_id", "atlas_cell_type_fine"]).size()
    other.rename("n_cells").reset_index().to_csv(P["light"] / "l1_other_not_annotated.csv", index=False)
    json.dump({"n_cells": int(len(cohort)), "smoke": a.smoke,
               "n_F1": int(cohort.F1.sum())}, open(P["light"] / "l1_summary.json", "w"), indent=1)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
