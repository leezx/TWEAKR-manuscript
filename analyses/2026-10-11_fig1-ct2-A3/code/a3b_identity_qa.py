#!/usr/bin/env python3
"""A3b Stage I QA package (contract A3b v0.3 §8 step 5 deliverables). Aggregates only; no CT2, no programme.

Public tables (tables/a3b_identity/):
  qa_summary.json              cell totals, gate outcomes, identity_v1 SHA256, code commit
  composition_by_study.tsv     study x branch x side x stage x MSI: cells, samples, median sample fractions
  eligibility_patients.tsv     per patient: E1 (pre-/post-matching), E2, E3, E4 flags and reasons
  eligibility_studies.tsv      per contrast x study: eligible patients; qualifying (>=5)
  T_studies.tsv / T_patients.tsv  (copied from step 2b) ; N_calibration.tsv (all studies)
  N_space_cnv_high.tsv         share of CNV-high cells (clear-CNV patients) beyond tau_p, per study
  axisL_coverage.tsv           Axis-L v0.3a class shares per study x side x stage
T_s (depth target, contract §4): per branch x study, min over sides of the 25th-percentile epithelial UMI.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

E1, E2, E34 = 100, 30, 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--samples", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--public", required=True)
    a = ap.parse_args()
    R, P = Path(a.root), Path(a.public)
    P.mkdir(parents=True, exist_ok=True)
    idt = pd.read_csv(R / "identity_v1.private.tsv.gz", sep="\t")
    sl = pd.read_csv(a.samples, sep="\t")
    man = pd.read_csv(a.manifest, sep="\t")
    meta = pd.read_csv(a.meta, sep="\t")
    msi = meta.groupby("patient_id").microsatellite_status.first().fillna("NA")
    resp = man.groupby("patient_id").response.first()
    spec = man.set_index("sample_id").specimen

    # one row per (branch, cell): samples can belong to both branches (Chen naive samples)
    x = sl[["branch", "sample_id", "side", "stage", "role"]].merge(
        idt.drop(columns=["side", "stage"]), on="sample_id")
    x["msi"] = x.patient_id.map(msi)
    for c in ["normal_like", "tumour_evidence", "ambiguous"]:
        x[c] = x.identity.eq(c)

    # depth targets
    def side_key(r):
        return r.side if r.branch == "normal_primary" else f"{r.side}:{r.stage}"
    x["side_key"] = [side_key(r) for r in x[["branch", "side", "stage"]].itertuples()]
    ts = {}
    for (b, s), g in x.groupby(["branch", "study_id"]):
        sides = ["normal", "tumour"] if b == "normal_primary" else ["tumour:Pre", "tumour:Post"]
        q = [g.loc[g.side_key == k, "umi"].quantile(0.25) for k in sides if (g.side_key == k).any()]
        ts[(b, s)] = float(min(q)) if q else np.nan
    x["T_s"] = [ts[(b, s)] for b, s in zip(x.branch, x.study_id)]
    x["kept_after_match"] = x.umi >= x.T_s

    # composition
    smp = x.groupby(["branch", "study_id", "patient_id", "sample_id", "side", "stage", "msi"]).agg(
        cells=("cell_id", "size"), normal_like=("normal_like", "mean"), tumour_evidence=("tumour_evidence", "mean"),
        ambiguous=("ambiguous", "mean")).reset_index()
    comp = smp.groupby(["branch", "study_id", "side", "stage", "msi"]).agg(
        samples=("sample_id", "size"), patients=("patient_id", "nunique"), cells=("cells", "sum"),
        median_normal_like=("normal_like", "median"), median_tumour_evidence=("tumour_evidence", "median"),
        median_ambiguous=("ambiguous", "median")).reset_index()
    comp.to_csv(P / "composition_by_study.tsv", sep="\t", index=False)

    # eligibility (per branch x patient x contrast)
    s2 = x.groupby(["branch", "study_id", "patient_id", "sample_id", "side_key"]).agg(
        n=("cell_id", "size"), n_matched=("kept_after_match", "sum"), n_normal_like=("normal_like", "sum"),
        n_tumour_ev=("tumour_evidence", "sum")).reset_index()
    contrasts = {"normal_primary": [("E", "normal", "tumour")],
                 "pre_post": [("E", "tumour:Pre", "tumour:Post")]}
    rows = []
    for (b, st, pid), g in s2.groupby(["branch", "study_id", "patient_id"]):
        for _, a1, a2 in contrasts[b]:
            g1, g2 = g[g.side_key == a1], g[g.side_key == a2]
            if b == "pre_post" and st == "Qin_2023_Cell_Rep_Med":
                g2 = g2[g2.sample_id.map(spec).eq("surgical resection")]
            r = dict(branch=b, study_id=st, patient_id=pid, contrast=f"{a1} vs {a2}", msi=msi.get(pid, "NA"),
                     response=resp.get(pid, ""),
                     E1_prematch=bool((g1.n >= E1).any() and (g2.n >= E1).any()),
                     E1=bool((g1.n_matched >= E1).any() and (g2.n_matched >= E1).any()),
                     E2=bool((g1.n >= E2).any() and (g2.n >= E2).any()),
                     E4=bool((g1.n_normal_like >= E34).any() and (g2.n_normal_like >= E34).any()))
            if b == "normal_primary":
                r["E3"] = bool((g1.n_normal_like >= E34).any() and (g2.n_tumour_ev >= E34).any())
            else:
                r["E3"] = bool((g1.n_tumour_ev >= E34).any() and (g2.n_tumour_ev >= E34).any()) \
                    and st != "Li_2023_Cancer_Cell"
            rows.append(r)
    el = pd.DataFrame(rows)
    if len(el):
        q = el.response.astype(str)
        trg0 = el.study_id.eq("Qin_2023_Cell_Rep_Med") & q.eq("TRG0")
        el.loc[trg0, ["E1", "E3"]] = False  # TRG0: composition only (contract §3)
        li = el.study_id.eq("Li_2023_Cancer_Cell")
        el.loc[li, ["E1", "E3"]] = False  # Li: composition / descriptive only
    el.to_csv(P / "eligibility_patients.tsv", sep="\t", index=False)
    es = []
    for (b, st, c), g in el.groupby(["branch", "study_id", "contrast"]):
        for e in ["E1_prematch", "E1", "E2", "E3", "E4"]:
            es.append(dict(branch=b, study_id=st, contrast=c, estimand=e, patients=int(g[e].sum()),
                           study_qualifies=bool(g[e].sum() >= 5)))
    es = pd.DataFrame(es)
    es.to_csv(P / "eligibility_studies.tsv", sep="\t", index=False)

    # N-space distribution of CNV-high cells (clear-CNV patients)
    ch = idt[(idt.cnv_state == "CNV-high") & idt.clear_cnv.fillna(False).astype(bool) & idt.N_status.eq("assessable")]
    ns = ch.groupby("study_id").apply(lambda g: pd.Series({"cnv_high_cells": len(g),
                                                          "share_beyond_tau": float((g.N_dist > g.N_tau).mean())})).reset_index()
    ns.to_csv(P / "N_space_cnv_high.tsv", sep="\t", index=False)
    cal = pd.concat([pd.read_csv(f, sep="\t") for f in sorted((R / "evidenceN").glob("*.N_calibration.tsv"))])
    cal.to_csv(P / "N_calibration.tsv", sep="\t", index=False)
    ax = idt.assign(stage=idt.stage.fillna("")).groupby(["study_id", "side", "stage"]).axisL_v03a.value_counts(
        normalize=True).rename("share").reset_index()
    ax.to_csv(P / "axisL_coverage.tsv", sep="\t", index=False)
    sha = (R / "identity_v1.private.tsv.gz.sha256").read_text().split()[0]
    summ = dict(identity_v1=str(R / "identity_v1.private.tsv.gz"), sha256=sha, commit=a.commit,
                cells=int(len(idt)), samples=int(idt.sample_id.nunique()), patients=int(idt.patient_id.nunique()),
                identity_counts=idt.identity.value_counts().to_dict(),
                N_status_by_study=cal.groupby("study_id").N_status.first().to_dict(),
                T_s={f"{b}|{s}": v for (b, s), v in ts.items()},
                eligibility=es.pivot_table(index=["branch", "study_id", "contrast"], columns="estimand",
                                           values="patients").reset_index().to_dict("records"))
    (P / "qa_summary.json").write_text(json.dumps(summ, indent=1, default=str))
    print(json.dumps({k: summ[k] for k in ["cells", "samples", "patients", "identity_counts", "N_status_by_study"]},
                     indent=1))
    print(es.pivot_table(index=["branch", "study_id"], columns="estimand", values="patients").to_string())


if __name__ == "__main__":
    main()
