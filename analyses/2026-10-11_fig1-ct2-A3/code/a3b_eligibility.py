#!/usr/bin/env python3
"""A3b Stage C: sample-level eligibility funnel (metadata only; identity-dependent E3 counts come after Stage I).

Rules (contract v0.2 §4):
- A sample contributes to E1 if it has >=100 Atlas epithelial cells, and to composition (E2) if >=30.
- A side is eligible if >=1 sample on it qualifies; qualifying samples on a side are aggregated later
  (per-sample median, then unweighted median across samples).
- A study enters a pooled normal-primary estimate with >=5 eligible patients; pre/post is per cohort.
Normal-primary: naive adjacent-normal vs naive primary tumour, immune-enriched samples dropped (as in pair_gate.py).
Pre/post: from a3b_clinical_manifest.tsv (verified stages).
"""
import argparse

import pandas as pd

E1, E2 = 100, 30


def side_ok(df, thr):
    return df[df.epi_total >= thr].groupby("patient_id").sample_id.nunique()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--crosswalk", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    s = pd.read_csv(a.meta, sep="\t")
    cw = pd.read_csv(a.crosswalk, sep="\t")
    immune = set(cw.loc[cw.cls == "immune_enriched", "enrichment_cell_types"].astype(str))
    s = s[~s.enrichment_cell_types.astype(str).isin(immune)]
    naive = s[s.treatment_status_before_resection == "naive"]
    rows = []
    for thr, lab in [(E1, "E1_ge100"), (E2, "E2_ge30")]:
        n = side_ok(naive[naive.sample_type == "adjacent normal"], thr)
        t = side_ok(naive[naive.sample_type == "primary tumor"], thr)
        both = n.index.intersection(t.index)
        st = naive[naive.patient_id.isin(both)].groupby("study_id").patient_id.nunique()
        q = st[st >= 5]
        rows.append(dict(design="normal_primary_naive", contrast="N vs T", rule=lab, patients=len(both),
                         qualifying_studies=len(q), patients_in_qualifying=int(q.sum()),
                         by_study="; ".join(f"{k}:{v}" for k, v in st.sort_values(ascending=False).items())))
    m = pd.read_csv(a.manifest, sep="\t")
    m = m[m.sample_type == "primary tumor"]
    contrasts = [("Qin_2023_Cell_Rep_Med", "Pre", "Post", None),
                 ("Qin_2023_Cell_Rep_Med", "Pre", "Post", "surgical resection"),
                 ("Chen_2024_Cancer_Cell", "Pre", "Post", None),
                 ("Chen_2024_Cancer_Cell", "Pre", "Post", "surgical specimen"),
                 ("Chen_2024_Cancer_Cell", "Pre", "On", None),
                 ("Li_2023_Cancer_Cell", "Pre", "Post", None)]
    for study, x, y, spec in contrasts:
        d = m[m.study_id == study]
        if study == "Chen_2024_Cancer_Cell":
            d = d[d.patient_id != "Chen_2024_Cancer_Cell.P02"]  # not neoadjuvant
        dy = d[d.stage == y]
        if spec:
            dy = dy[dy.specimen.str.startswith(spec)]
        for thr, lab in [(E1, "E1_ge100"), (E2, "E2_ge30")]:
            px, py = side_ok(d[d.stage == x], thr), side_ok(dy, thr)
            both = px.index.intersection(py.index)
            resp = d[d.patient_id.isin(both)].groupby("patient_id").response.first().value_counts()
            msi = d[d.patient_id.isin(both)].groupby("patient_id").msi.first().fillna("NA").value_counts()
            rows.append(dict(design=f"pre_post|{study}", contrast=f"{x} vs {y}" + (f" [{spec}]" if spec else ""),
                             rule=lab, patients=len(both), qualifying_studies=None, patients_in_qualifying=None,
                             by_study="response " + ", ".join(f"{k}:{v}" for k, v in resp.items())
                             + " | MSI " + ", ".join(f"{k}:{v}" for k, v in msi.items())))
    out = pd.DataFrame(rows)
    out.to_csv(a.out, sep="\t", index=False)
    print(out.to_string())


if __name__ == "__main__":
    main()
