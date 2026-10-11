#!/usr/bin/env python3
"""A3b Stage I sample list (contract v0.2 §1): every sample that enters identity calling.

- normal-primary: naive adjacent-normal + naive primary-tumour samples (>=30 Atlas epithelial cells) of every
  patient with both sides at >=30, in studies with >=5 such patients; plus every other naive adjacent-normal
  sample (>=30) of those studies, which enters only the Evidence N reference pool (role = reference_only).
- pre/post: every tumour and normal sample in a3b_clinical_manifest.tsv with >=30 epithelial cells
  (Chen P02 excluded: not neoadjuvant).
Immune-enriched samples are dropped first. Output: tables/metadata_gate/a3b_samples.tsv
"""
import argparse

import pandas as pd

THR = 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--crosswalk", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    s = pd.read_csv(a.meta, sep="\t")
    cw = pd.read_csv(a.crosswalk, sep="\t")
    s = s[~s.enrichment_cell_types.astype(str).isin(set(cw.loc[cw.cls == "immune_enriched", "enrichment_cell_types"]))]
    s = s[s.epi_total >= THR]
    naive = s[s.treatment_status_before_resection == "naive"]
    nor = naive[naive.sample_type == "adjacent normal"]
    tum = naive[naive.sample_type == "primary tumor"]
    both = set(nor.patient_id) & set(tum.patient_id)
    per = pd.Series([p.split(".")[0] for p in both]).value_counts()
    ok_pat = {p for p in both if s.loc[s.patient_id == p, "study_id"].iloc[0] in
              set(s[s.patient_id.isin(both)].groupby("study_id").patient_id.nunique().loc[lambda x: x >= 5].index)}
    studies = set(s.loc[s.patient_id.isin(ok_pat), "study_id"])
    rows = []
    for _, r in pd.concat([nor, tum]).iterrows():
        if r.study_id not in studies:
            continue
        if r.patient_id in ok_pat:
            role = "pair"
        elif r.sample_type == "adjacent normal":
            role = "reference_only"
        else:
            continue
        rows.append(dict(branch="normal_primary", study_id=r.study_id, patient_id=r.patient_id, sample_id=r.sample_id,
                         side="normal" if r.sample_type == "adjacent normal" else "tumour", stage="naive", role=role,
                         epi_total=r.epi_total))
    m = pd.read_csv(a.manifest, sep="\t")
    m = m[(m.epi_total >= THR) & (m.patient_id != "Chen_2024_Cancer_Cell.P02")]
    for _, r in m.iterrows():
        rows.append(dict(branch="pre_post", study_id=r.study_id, patient_id=r.patient_id, sample_id=r.sample_id,
                         side="normal" if r.sample_type == "adjacent normal" else "tumour", stage=r.stage,
                         role="pair", epi_total=r.epi_total))
    out = pd.DataFrame(rows).drop_duplicates(["branch", "sample_id"])
    out.to_csv(a.out, sep="\t", index=False)
    print(out.groupby(["branch", "study_id", "side", "role"]).agg(samples=("sample_id", "size"),
                                                                patients=("patient_id", "nunique")).to_string())
    print("unique samples:", out.sample_id.nunique(), "patients:", out.patient_id.nunique())


if __name__ == "__main__":
    main()
