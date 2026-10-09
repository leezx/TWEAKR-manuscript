#!/usr/bin/env python3
"""Are HTAPP_HTAN cells/patients duplicates of Pelka_2021_Cell? (obs metadata only)

Identifier systems differ (HTA1_xxx vs Cxxx), so identifier overlap alone cannot rule out duplication.
Tests:
  1. shared patient / sample / accession identifiers;
  2. cell fingerprint: exact (total_counts, n_genes_by_counts) pairs. If an HTAPP sample is a re-release
     of a Pelka sample, nearly all its fingerprints match one Pelka sample. The background rate is
     estimated with a control study on a similar platform;
  3. patient demographics from the scope table (age, sex, stage, MSI), shown side by side.
"""
import argparse
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

FIELDS = ["study_id", "patient_id", "sample_id", "total_counts", "n_genes_by_counts"]


def read(obs, k):
    g = obs[k]
    if isinstance(g, h5py.Group):
        c = np.array([x.decode() if isinstance(x, bytes) else str(x) for x in g["categories"][:]], dtype=object)
        codes = g["codes"][:]
        o = np.full(codes.shape, "NA", dtype=object)
        o[codes >= 0] = c[codes[codes >= 0]]
        return o
    return g[:]


def fingerprint_match(query, ref):
    """Per query sample: fraction of cells whose fingerprint occurs in ref, and the best-matching ref sample."""
    ref_fp = ref.groupby("fp").sample_id.agg(lambda s: s.mode().iat[0])
    rows = []
    for sample, g in query.groupby("sample_id"):
        hit = g.fp.map(ref_fp)
        best = hit.value_counts()
        rows.append({"query_sample": sample, "patient": g.patient_id.iat[0], "cells": len(g),
                     "fraction_matched": round(hit.notna().mean(), 4),
                     "best_ref_sample": best.index[0] if len(best) else "",
                     "fraction_matched_to_best": round(best.iat[0] / len(g), 4) if len(best) else 0.0})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--scope-tsv", required=True)
    ap.add_argument("--control-study", default="Lee_2020_Nat_Genet")
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    out = Path(a.out_dir)
    with h5py.File(a.h5ad, "r") as f:
        df = pd.DataFrame({k: read(f["obs"], k) for k in FIELDS})
    df = df[df.study_id.isin(["HTAPP_HTAN", "Pelka_2021_Cell", a.control_study])].copy()
    df["fp"] = df.total_counts.round().astype(int).astype(str) + "_" + df.n_genes_by_counts.astype(int).astype(str)
    h, p, c = (df[df.study_id == s] for s in ["HTAPP_HTAN", "Pelka_2021_Cell", a.control_study])

    ids = {k: len(set(h[k]) & set(p[k])) for k in ["patient_id", "sample_id"]}
    vs_pelka = fingerprint_match(h, p).assign(reference="Pelka_2021_Cell")
    vs_ctrl = fingerprint_match(h, c).assign(reference=a.control_study)
    res = pd.concat([vs_pelka, vs_ctrl])
    res.to_csv(out / "htapp_vs_pelka_fingerprint.csv", index=False)

    scope = pd.read_csv(a.scope_tsv, sep="\t")
    demo = scope[scope.study.isin(["HTAPP_HTAN", "Pelka_2021_Cell"])][
        ["study", "patient_id", "age", "sex", "tumor_stage", "msi_status", "treatment_context"]]
    demo.to_csv(out / "htapp_pelka_patient_demographics.csv", index=False)

    print("shared identifiers:", ids)
    for ref, g in res.groupby("reference"):
        print(ref, "median fraction matched", g.fraction_matched.median(),
              "median matched-to-best", g.fraction_matched_to_best.median())
    print(demo.groupby("study")[["sex", "tumor_stage", "msi_status", "treatment_context"]]
          .agg(lambda s: dict(s.value_counts())).to_string())


if __name__ == "__main__":
    main()
