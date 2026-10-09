#!/usr/bin/env python3
"""Fig. 1B dataset screen (v2): compartment completeness of CRC Atlas studies.

Reads obs metadata only (no expression). v2 adds, after review on 2026-10-09:
  - study inclusion flow covering every study in the H5AD and the manuscript scope table;
  - identifier checks (cell, patient -> study, sample -> patient);
  - treatment coded as naive / treated / unknown (unknown is never merged into either);
  - per-sample enrichment class (unsorted / immune-enriched / non-immune-enriched / mixed / unknown);
  - completeness at patient level (primary tumour samples pooled) and at sample level
    (one primary tumour sample complete on its own), plus an unsorted-only variant;
  - threshold sets permissive 20/5, primary 30/5, stringent 50/10;
  - 7-lineage counts and a fibroblast-specific completeness table (not an inclusion criterion).

Compartments from harmonized `atlas_cell_type_middle` (fixed before counting):
  Epithelial = Epithelial progenitor, Epithelial cell, Goblet, Tuft, Enteroendocrine, Cancer cell, CRLM
  Myeloid    = Monocyte, Macrophage, Dendritic cell, Neutrophil, Eosinophil, Mast cell
  T/NK       = T cell CD4, T cell regulatory, T cell CD8, NK cell, ILC, T cell γδ, NKT
  B/Plasma   = B cell, Plasma cell
  Fibroblast, Endothelial (Endothelial cell), Pericyte
  Immune = Myeloid + T/NK + B/Plasma;  Stromal = Fibroblast + Endothelial + Pericyte
  Other (not counted) = Platelet, Cancer cell circulating, Hepatocyte, Schwann cell, unlabelled
"""
import argparse
import json
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

BROAD = ["Epithelial", "Immune", "Stromal"]
LINEAGES = ["Epithelial", "T/NK", "B/Plasma", "Myeloid", "Fibroblast", "Endothelial", "Pericyte"]
COUNT_COLS = LINEAGES + ["Immune", "Stromal"]  # Epithelial is both a lineage and a broad compartment
BROAD_OF = {"Epithelial": "Epithelial", "T/NK": "Immune", "B/Plasma": "Immune", "Myeloid": "Immune",
            "Fibroblast": "Stromal", "Endothelial": "Stromal", "Pericyte": "Stromal"}
MIDDLE_TO_LINEAGE = {
    **{k: "Epithelial" for k in ["Epithelial progenitor", "Epithelial cell", "Goblet", "Tuft",
                                 "Enteroendocrine", "Cancer cell", "CRLM"]},
    **{k: "Myeloid" for k in ["Monocyte", "Macrophage", "Dendritic cell", "Neutrophil", "Eosinophil",
                              "Mast cell"]},
    **{k: "T/NK" for k in ["T cell CD4", "T cell regulatory", "T cell CD8", "NK cell", "ILC",
                           "T cell γδ", "NKT"]},
    **{k: "B/Plasma" for k in ["B cell", "Plasma cell"]},
    "Fibroblast": "Fibroblast", "Endothelial cell": "Endothelial", "Pericyte": "Pericyte",
}
MALIGNANT = {"Cancer cell", "CRLM"}
THRESHOLDS = {"permissive_20_5": (20, 5), "primary_30_5": (30, 5), "stringent_50_10": (50, 10)}
ENRICHMENT_CLASS = {
    "naive": "unsorted",
    "mixCD45+CD45-": "mixed", "CD45+/CD45-": "mixed",
    "CD45-": "non_immune_enriched", "EPCAM+": "non_immune_enriched", "EPCAM-/CD45-/CD31-": "non_immune_enriched",
    "epithelial": "non_immune_enriched", "AnnexinV-": "unsorted",
}  # every other recorded value is an immune marker sort (CD45+, CD3+, CD14+, CD56+, ...) -> immune_enriched
OBS_FIELDS = ["study_id", "patient_id", "sample_id", "sample_type", "treatment_status_before_resection",
              "enrichment_cell_types", "platform", "atlas_cell_type_middle"]


def read_cat(obs, key):
    g = obs[key]
    if not isinstance(g, h5py.Group):
        return np.array([x.decode() if isinstance(x, bytes) else str(x) for x in g[:]], dtype=object)
    cats = np.array([c.decode() if isinstance(c, bytes) else str(c) for c in g["categories"][:]], dtype=object)
    codes = g["codes"][:]
    out = np.full(codes.shape, "NA", dtype=object)
    ok = codes >= 0
    out[ok] = cats[codes[ok]]
    return out


def enrichment_class(v):
    if v in ("NA", "nan", ""):
        return "unknown"
    return ENRICHMENT_CLASS.get(v, "immune_enriched")


def treatment_class(v):
    return {"naive": "naive", "treated": "treated"}.get(v, "unknown")


def load(h5ad):
    with h5py.File(h5ad, "r") as f:
        obs = f["obs"]
        idx = read_cat(obs, obs.attrs["_index"])
        df = pd.DataFrame({k: read_cat(obs, k) for k in OBS_FIELDS})
    checks = {"cells": len(df), "cell_index_unique": bool(pd.Index(idx).is_unique),
              "patients_in_multiple_studies": int((df.groupby("patient_id").study_id.nunique() > 1).sum()),
              "samples_in_multiple_patients": int((df.groupby("sample_id").patient_id.nunique() > 1).sum()),
              "samples_with_multiple_sample_types": int((df.groupby("sample_id").sample_type.nunique() > 1).sum()),
              "patients_with_multiple_treatment_values": int(
                  (df.groupby("patient_id").treatment_status_before_resection.nunique() > 1).sum())}
    df["lineage"] = df.atlas_cell_type_middle.map(MIDDLE_TO_LINEAGE).fillna("Other")
    df["malignant"] = df.atlas_cell_type_middle.isin(MALIGNANT)
    df["treatment"] = df.treatment_status_before_resection.map(treatment_class)
    df["enrichment_class"] = df.enrichment_cell_types.map(enrichment_class)
    return df, checks


def sample_table(df):
    """One row per study x patient x sample with lineage counts and design labels."""
    keys = ["study_id", "patient_id", "sample_id", "sample_type", "treatment", "enrichment_class", "platform"]
    t = df.groupby(keys + ["lineage"], observed=True).size().unstack(fill_value=0)
    t = t.reindex(columns=LINEAGES + ["Other"], fill_value=0)
    for b in BROAD:
        t[b] = t[[l for l in LINEAGES if BROAD_OF[l] == b]].sum(axis=1)
    return t.reset_index()


def complete(t, cols, n):
    return (t[cols] >= n).all(axis=1)


def screen(st, scope_name, treatments):
    """Per study: complete patients under each threshold, for several completeness definitions."""
    s = st[(st.sample_type == "primary tumor") & st.treatment.isin(treatments)]
    pat = s.groupby(["study_id", "patient_id"])[COUNT_COLS].sum()
    pat_unsorted = (s[s.enrichment_class == "unsorted"]
                    .groupby(["study_id", "patient_id"])[COUNT_COLS].sum())
    rows = []
    for study in sorted(st.study_id.unique()):
        p = pat.loc[study] if study in pat.index.get_level_values(0) else pat.iloc[0:0]
        pu = pat_unsorted.loc[study] if study in pat_unsorted.index.get_level_values(0) else pat_unsorted.iloc[0:0]
        smp = s[s.study_id == study]
        r = {"scope": scope_name, "study": study, "patients": len(p), "samples": len(smp),
             "cells": int(p[BROAD].sum().sum())}
        for b in BROAD:
            r[f"{b}_pct"] = round(100 * p[b].sum() / max(r["cells"], 1), 2)
        for name, (n_cells, n_pat) in THRESHOLDS.items():
            r[f"{name}_patients"] = int(complete(p, BROAD, n_cells).sum())
            r[f"{name}_pass"] = r[f"{name}_patients"] >= n_pat
            r[f"{name}_sample_level_patients"] = int(
                smp[complete(smp, BROAD, n_cells)].patient_id.nunique())
            r[f"{name}_unsorted_only_patients"] = int(complete(pu, BROAD, n_cells).sum())
            r[f"{name}_fibroblast_patients"] = int(
                complete(p, ["Epithelial", "Immune", "Fibroblast"], n_cells).sum())
        rows.append(r)
    return pd.DataFrame(rows), pat.reset_index()


def lineage_table(pat, n_cells=30):
    """Per study: patients with >= n_cells in each of the 7 lineages (descriptive, not a criterion)."""
    rows = []
    for study, g in pat.groupby("study_id"):
        r = {"study": study, "patients": len(g)}
        for l in LINEAGES:
            r[f"{l}_cells"] = int(g[l].sum())
            r[f"{l}_patients_ge{n_cells}"] = int((g[l] >= n_cells).sum())
        r["Stromal_fibroblast_share_pct"] = round(100 * g.Fibroblast.sum() / max(g.Stromal.sum(), 1), 1)
        rows.append(r)
    return pd.DataFrame(rows)


def study_design(st, df):
    rows = []
    for study, g in st.groupby("study_id"):
        cls = sorted(g.enrichment_class.unique())
        d = df[df.study_id == study]
        rows.append({
            "study": study, "platform": ";".join(sorted(g.platform.unique())),
            "enrichment_values": ";".join(f"{k}:{v}" for k, v in d.enrichment_cell_types.value_counts().items()),
            "enrichment_classes": ";".join(cls),
            "study_sorting": cls[0] if len(cls) == 1 else "mixed_by_sample",
            "sample_types": ";".join(f"{k}:{v}" for k, v in d.sample_type.value_counts().items()),
            "treatment_cells": ";".join(f"{k}:{v}" for k, v in d.treatment.value_counts().items()),
            "malignant_epithelial_cells": int(d.malignant.sum()),
            "normal_epithelial_cells": int(((d.lineage == "Epithelial") & ~d.malignant).sum()),
        })
    return pd.DataFrame(rows)


def inclusion_flow(df_all, scope, lineage_dir, primary):
    """Every study in the H5AD or in the manuscript scope table, with its fate."""
    h5 = df_all.groupby("study_id").agg(h5ad_patients=("patient_id", "nunique"), h5ad_cells=("patient_id", "size"))
    sc = scope.groupby("study").agg(scope_patients=("patient_id", "nunique"), source_role=("source_role", "first"))
    flow = h5.join(sc, how="outer")
    flow.index.name = "study"
    flow = flow.reset_index()
    p = primary.set_index("study")
    out = []
    for _, r in flow.iterrows():
        role = r.source_role if isinstance(r.source_role, str) else "not in manuscript scope"
        if role == "not in manuscript scope":
            fate = "excluded before screening: not in the 42-study manuscript scope (reference/non-CRC)"
        elif role == "supplemental_primary_object":
            done = (Path(lineage_dir) / f"{r.study}_COMPLETE.txt").exists()
            fate = ("not screened: no harmonized cell types; heuristic lineage at study level only"
                    if done else "not screened: no harmonized cell types; heuristic lineage not complete")
        elif r.study in p.index and bool(p.loc[r.study, "primary_30_5_pass"]):
            fate = "PASS (primary 30/5, primary tumour, treatment-naive)"
        else:
            n = int(p.loc[r.study, "primary_30_5_patients"]) if r.study in p.index else 0
            fate = f"FAIL: {n} complete patients (need 5)"
        out.append({**r.to_dict(), "source_role": role, "fate": fate})
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--scope-tsv", required=True)
    ap.add_argument("--lineage-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    scope = pd.read_csv(a.scope_tsv, sep="\t")
    df_all, checks = load(a.h5ad)
    backbone = set(scope.loc[scope.source_role.str.startswith("integrated_backbone"), "patient_id"])
    checks["scope_backbone_patients"] = len(backbone)
    checks["scope_backbone_patients_missing_from_h5ad"] = len(backbone - set(df_all.patient_id))
    df = df_all[df_all.patient_id.isin(backbone)]
    checks["cells_in_scope"] = len(df)
    checks["studies_in_scope"] = int(df.study_id.nunique())
    checks["unknown_enrichment_values"] = sorted(
        v for v in df.enrichment_cell_types.unique()
        if v not in ENRICHMENT_CLASS and v not in ("NA", "nan"))  # all classified as immune_enriched

    st = sample_table(df)
    st.to_csv(out / "sample_lineage_counts.csv.gz", index=False)
    study_design(st, df).to_csv(out / "study_design_flags.csv", index=False)

    primary, pat = screen(st, "primary_tumor_naive", ["naive"])
    sens, _ = screen(st, "primary_tumor_naive_or_unknown", ["naive", "unknown"])
    anyt, _ = screen(st, "primary_tumor_any_treatment", ["naive", "unknown", "treated"])
    pd.concat([primary, sens, anyt]).to_csv(out / "study_screen_summary.csv", index=False)
    pat.to_csv(out / "patient_lineage_counts_primary_tumor_naive.csv.gz", index=False)
    lineage_table(pat).to_csv(out / "lineage_coverage_primary_tumor_naive.csv", index=False)
    inclusion_flow(df_all, scope, a.lineage_dir, primary).to_csv(out / "study_inclusion_flow.csv", index=False)

    checks["n_pass"] = {name: int(primary[f"{name}_pass"].sum()) for name in THRESHOLDS}
    checks["complete_patients_primary_30_5"] = int(primary.loc[primary.primary_30_5_pass, "primary_30_5_patients"].sum())
    (out / "run_summary.json").write_text(json.dumps(checks, indent=1))
    print(json.dumps(checks, indent=1))


if __name__ == "__main__":
    main()
