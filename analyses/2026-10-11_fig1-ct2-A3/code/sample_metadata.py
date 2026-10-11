#!/usr/bin/env python3
"""A3b metadata gate, step 1: one row per Atlas sample with design labels and epithelial cell counts.

Reads obs metadata only (no expression, no CytoTRACE2). Same Atlas H5AD and manuscript patient scope
(integrated backbone) as the Fig. 1B dataset screen. For each sample it records every design field
needed to judge normal-tumour and pre/post-treatment pairs, the number of distinct values per field
(a value of >1 flags a mixed sample), and epithelial counts by harmonized `atlas_cell_type_middle`.
"""
import argparse
import json

import h5py
import numpy as np
import pandas as pd

KEYS = ["study_id", "patient_id", "sample_id"]
DESIGN = ["sample_type", "tissue", "tissue_type", "sample_tissue", "tumor_source", "anatomic_location",
          "anatomic_region", "treatment_status_before_resection", "treatment_drug", "treatment_response",
          "RECIST", "medical_condition", "microsatellite_status", "mismatch_repair_deficiency_status",
          "tumor_stage_TNM", "platform", "platform_fine", "enrichment_cell_types", "replicate"]
EPI = ["Epithelial progenitor", "Epithelial cell", "Goblet", "Tuft", "Enteroendocrine", "Cancer cell", "CRLM"]


def read_col(obs, key):
    g = obs[key]
    if not isinstance(g, h5py.Group):
        v = g[:]
        return np.array([x.decode() if isinstance(x, bytes) else str(x) for x in v], dtype=object)
    cats = np.array([c.decode() if isinstance(c, bytes) else str(c) for c in g["categories"][:]], dtype=object)
    codes = g["codes"][:]
    out = np.full(codes.shape, "NA", dtype=object)
    out[codes >= 0] = cats[codes[codes >= 0]]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--scope-tsv", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with h5py.File(a.h5ad, "r") as f:
        obs = f["obs"]
        df = pd.DataFrame({k: read_col(obs, k) for k in KEYS + DESIGN + ["atlas_cell_type_middle"]})
        df["n_counts"] = obs["n_counts"][:] if not isinstance(obs["n_counts"], h5py.Group) else np.nan
    scope = pd.read_csv(a.scope_tsv, sep="\t")
    backbone = set(scope.loc[scope.source_role.str.startswith("integrated_backbone"), "patient_id"])
    df = df[df.patient_id.isin(backbone)]
    df["is_epi"] = df.atlas_cell_type_middle.isin(EPI)
    g = df.groupby(KEYS, sort=True)
    out = g.size().rename("cells").to_frame()
    for k in DESIGN:
        out[k] = g[k].agg(lambda s: "|".join(sorted(set(s))))
        out[f"{k}_n"] = g[k].nunique()
    for m in EPI:
        out[f"epi_{m.replace(' ', '_')}"] = g.atlas_cell_type_middle.agg(lambda s, m=m: int((s == m).sum()))
    out["epi_total"] = g.is_epi.sum()
    out["epi_median_umi"] = df[df.is_epi].groupby(KEYS).n_counts.median()
    out = out.reset_index()
    out.to_csv(a.out, sep="\t", index=False)
    mixed = {k: int((out[f"{k}_n"] > 1).sum()) for k in DESIGN}
    print(json.dumps({"samples": len(out), "patients": int(out.patient_id.nunique()),
                      "studies": int(out.study_id.nunique()), "cells": int(out.cells.sum()),
                      "samples_with_mixed_values": mixed}, indent=1))


if __name__ == "__main__":
    main()
