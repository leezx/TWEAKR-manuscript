#!/usr/bin/env python3
"""Freeze the Fig. 1B primary cohort (approved 2026-10-09) as explicit patient and cell ID lists.

Cohort = patients complete at 30 cells per broad compartment in the 13 studies that pass 30/5,
using treatment-naive primary tumour samples only (screen v2, `screen_compartments.py`).
Cells kept = every cell of those patients' naive primary tumour samples, including lineage
"Other", so that CytoTRACE2 can later be run per sample on the full sample.

Also flags each patient for the pre-specified sensitivity sets:
  stringent_50_10   - complete at 50 cells and study passes 50/10
  unsorted_30_5     - complete at 30 cells using unsorted samples only, study passes 30/5 that way
  fibroblast_30     - Epithelial, Immune and Fibroblast each >= 30 cells (descriptive)
  permissive_20_5   - complete at 20 cells and study passes 20/5
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

from screen_compartments import (BROAD_OF, COUNT_COLS, LINEAGES, OBS_FIELDS, enrichment_class,
                                 read_cat, treatment_class, MIDDLE_TO_LINEAGE)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def complete_patients(cells, n_cells, n_patients, cols=("Epithelial", "Immune", "Stromal")):
    t = cells.groupby(["study_id", "patient_id"])[list(cols)].sum()
    ok = (t >= n_cells).all(axis=1)
    per_study = ok.groupby(level=0).sum()
    passing = set(per_study[per_study >= n_patients].index)
    return {(s, p) for (s, p), v in ok.items() if v and s in passing}  # (study, patient): IDs can recur across studies


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--scope-tsv", required=True)
    ap.add_argument("--out-dir", required=True, help="heavy outputs (cell list), Argos")
    ap.add_argument("--light-dir", required=True, help="light outputs (patient list, manifest)")
    ap.add_argument("--screen-commit", required=True)
    a = ap.parse_args()
    out, light = Path(a.out_dir), Path(a.light_dir)
    out.mkdir(parents=True, exist_ok=True)
    light.mkdir(parents=True, exist_ok=True)

    scope = pd.read_csv(a.scope_tsv, sep="\t")
    backbone = set(scope.loc[scope.source_role.str.startswith("integrated_backbone"), "patient_id"])
    with h5py.File(a.h5ad, "r") as f:
        obs = f["obs"]
        cell_id = read_cat(obs, obs.attrs["_index"])
        df = pd.DataFrame({k: read_cat(obs, k) for k in OBS_FIELDS})
    df.insert(0, "cell_id", cell_id)
    df = df[df.patient_id.isin(backbone) & (df.sample_type == "primary tumor")]
    df = df[df.treatment_status_before_resection.map(treatment_class) == "naive"].copy()
    df["lineage"] = df.atlas_cell_type_middle.map(MIDDLE_TO_LINEAGE).fillna("Other")
    df["broad"] = df.lineage.map(BROAD_OF).fillna("Other")
    df["enrichment_class"] = df.enrichment_cell_types.map(enrichment_class)
    for c in COUNT_COLS:
        df[c] = (df.lineage == c) if c in LINEAGES else (df.broad == c)

    primary = complete_patients(df, 30, 5)
    sets = {
        "permissive_20_5": complete_patients(df, 20, 5),
        "stringent_50_10": complete_patients(df, 50, 10),
        "unsorted_30_5": complete_patients(df[df.enrichment_class == "unsorted"], 30, 5),
        "fibroblast_30": complete_patients(df, 30, 1, ("Epithelial", "Immune", "Fibroblast")) & primary,
    }
    df["key"] = list(zip(df.study_id, df.patient_id))
    cells = df[df.key.isin(primary)]
    keep = ["cell_id", "study_id", "patient_id", "sample_id", "enrichment_class", "platform",
            "atlas_cell_type_middle", "lineage", "broad"]
    cell_file = out / "fig1b_cohort_cells_v1.tsv.gz"
    with gzip.open(cell_file, "wt") as h:
        cells[keep].sort_values(["study_id", "patient_id", "sample_id", "cell_id"]).to_csv(h, sep="\t", index=False)

    pat = (cells.groupby(["study_id", "patient_id"])
           .agg(samples=("sample_id", "nunique"), cells=("cell_id", "size"),
                **{f"{c}_cells": (c, "sum") for c in COUNT_COLS})
           .reset_index())
    for k, v in sets.items():
        pat[f"in_{k}"] = pd.Series(list(zip(pat.study_id, pat.patient_id))).isin(v).values
    pat_file = light / "fig1b_cohort_patients_v1.csv"
    pat.to_csv(pat_file, index=False)

    manifest = {
        "cohort_version": "v1", "approved": "2026-10-09 (user review of screen v2)",
        "screen_commit": a.screen_commit, "h5ad": a.h5ad, "scope_tsv": a.scope_tsv,
        "rule": "treatment-naive primary tumour samples; >=30 cells in each of Epithelial/Immune/Stromal per patient; study >=5 such patients",
        "studies": int(pat.study_id.nunique()), "patients": len(pat), "cells": len(cells),
        "samples": int(cells.groupby(["patient_id", "sample_id"]).ngroups),
        "cells_by_broad": cells.broad.value_counts().to_dict(),
        "patients_by_study": pat.groupby("study_id").size().to_dict(),
        "sensitivity_patients": {k: int(pat[f"in_{k}"].sum()) for k in sets},
        "permissive_vs_primary": {
            "in_permissive_not_primary": sorted("|".join(k) for k in sets["permissive_20_5"] - primary),
            "in_primary_not_permissive": sorted("|".join(k) for k in primary - sets["permissive_20_5"])},
        "files": {cell_file.name: sha256(cell_file), pat_file.name: sha256(pat_file)},
    }
    (light / "fig1b_cohort_manifest_v1.json").write_text(json.dumps(manifest, indent=1))
    print(json.dumps({k: v for k, v in manifest.items() if k != "permissive_vs_primary"}, indent=1))
    print("permissive extra patients:", len(manifest["permissive_vs_primary"]["in_permissive_not_primary"]))


if __name__ == "__main__":
    main()
