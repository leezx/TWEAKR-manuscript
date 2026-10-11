#!/usr/bin/env python3
"""A3b Stage I step 2b: Evidence T calls and gates (contract A3b v0.3 §5). No CT2, no programme score.

Per patient (joint inferCNV): reference P99/P95 of score and correlation from that patient's reference cells
(Fig. 1b rule) -> CNV-high / CNV-low / intermediate for every epithelial observation cell.
Clear-CNV: >= 20% of pre/primary tumour-side epithelium CNV-high.
Gates:
  concordance - cohort-v1 tumour cells in both runs: Cohen's kappa over {high, intermediate, low} vs Fig. 1b
                annotation_v1 cnv_state; kappa < 0.40 or a clear-CNV flip -> Evidence T not evaluable (patient).
  normal-side - per patient share of normal-side epithelium CNV-high (patients with >= 30 normal-side cells and
                CNV assessable); >= 3 such patients per study, else 'uncalibrated'; study median > 2% -> T void.
Outputs: <out>/identity_T.private.tsv.gz (per cell), <public>/a3b_T_patients.tsv, a3b_T_studies.tsv.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

HIGH_Q, LOW_Q, CLEAR, KAPPA_MIN, NORM_MAX, NORM_MIN_CELLS, NORM_MIN_PAT = 0.99, 0.95, 0.20, 0.40, 0.02, 30, 3


def kappa(a, b):
    cats = sorted(set(a) | set(b))
    t = pd.crosstab(pd.Categorical(a, cats), pd.Categorical(b, cats), dropna=False).to_numpy(float)
    n = t.sum()
    if n == 0:
        return np.nan
    po = np.trace(t) / n
    pe = (t.sum(0) * t.sum(1)).sum() / n ** 2
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="A3b run root (export/, cnv_out/)")
    ap.add_argument("--annotation", required=True, help="Fig. 1b annotation_v1.tsv.gz")
    ap.add_argument("--fig1b-patients", required=True, help="Fig. 1b malignancy_by_patient.csv")
    ap.add_argument("--public", required=True)
    a = ap.parse_args()
    R, PUB = Path(a.root), Path(a.public)
    PUB.mkdir(parents=True, exist_ok=True)
    cells = pd.concat([pd.read_csv(p, sep="\t") for p in sorted((R / "export/cells").glob("*.epi_cells.tsv.gz"))])
    pats = pd.concat([pd.read_csv(p, sep="\t") for p in sorted((R / "export/cnv_inputs").glob("*.patients.tsv"))])
    res = []
    for _, p in pats[pats.assessable].iterrows():
        f = R / "cnv_out" / p["dir"] / "cnv_metrics.tsv.gz"
        if not f.exists():
            raise FileNotFoundError(f)
        t = pd.read_csv(f, sep="\t")
        ref = t[t.group.str.startswith("ref_")]
        ob = t[t.group.str.startswith("obs__")].copy()
        if ob.cnv_cor.isna().all():
            ob["cnv_state"] = "no_profile"
        else:
            s_hi, r_hi = ref.cnv_score.quantile(HIGH_Q), ref.cnv_cor.quantile(HIGH_Q)
            s_lo, r_lo = ref.cnv_score.quantile(LOW_Q), ref.cnv_cor.quantile(LOW_Q)
            ob["cnv_state"] = np.where((ob.cnv_score > s_hi) & (ob.cnv_cor > r_hi), "CNV-high",
                              np.where((ob.cnv_score <= s_lo) & (ob.cnv_cor <= r_lo), "CNV-low", "intermediate"))
        ob["patient_id"] = p.patient_id
        res.append(ob[["cell_id", "patient_id", "cnv_score", "cnv_cor", "cnv_state"]])
    res = pd.concat(res)
    e = cells.merge(res.drop(columns="patient_id"), on="cell_id", how="left")
    e["cnv_state"] = e.cnv_state.fillna("not_assessable")

    pt = e.groupby("patient_id").apply(lambda g: pd.Series({
        "study_id": g.study_id.iat[0],
        "n_epi": len(g),
        "n_primary_side": int((g.side.eq("tumour") & g.stage.isin(["naive", "Pre"])).sum()),
        "frac_primary_cnv_high": ((g.cnv_state == "CNV-high") & g.side.eq("tumour") & g.stage.isin(["naive", "Pre"])).sum()
        / max(1, (g.side.eq("tumour") & g.stage.isin(["naive", "Pre"])).sum()),
        "n_normal_side": int(g.side.eq("normal").sum()),
        "normal_cnv_high_rate": ((g.cnv_state == "CNV-high") & g.side.eq("normal")).sum() / max(1, g.side.eq("normal").sum()),
        "assessable": bool((g.cnv_state.isin(["CNV-high", "CNV-low", "intermediate"])).any()),
    })).reset_index()
    pt["clear_cnv"] = pt.assessable & (pt.n_primary_side > 0) & (pt.frac_primary_cnv_high >= CLEAR)

    # concordance with Fig. 1b annotation_v1 (cohort-v1 tumour cells)
    ann = pd.read_csv(a.annotation, sep="\t", usecols=["cell_id", "cnv_state"]).rename(columns={"cnv_state": "cnv_v1"})
    old = pd.read_csv(a.fig1b_patients)[["patient_id", "clear_cnv"]].rename(columns={"clear_cnv": "clear_cnv_v1"})
    cc = e.merge(ann, on="cell_id")
    cc = cc[cc.cnv_state.isin(["CNV-high", "CNV-low", "intermediate"]) & cc.cnv_v1.isin(["CNV-high", "CNV-low", "intermediate"])]
    kp = cc.groupby("patient_id").apply(lambda g: pd.Series({
        "n_overlap": len(g), "kappa_v1": kappa(g.cnv_state.tolist(), g.cnv_v1.tolist()),
        "high_agree_v1": ((g.cnv_state == "CNV-high") == (g.cnv_v1 == "CNV-high")).mean()})).reset_index()
    pt = pt.merge(kp, on="patient_id", how="left").merge(old, on="patient_id", how="left")
    has_v1 = pt.clear_cnv_v1.notna()
    pt["clear_flip"] = has_v1 & ((pt.clear_cnv_v1.astype(str) == "True") != pt.clear_cnv)
    pt["concordance_fail"] = (pt.kappa_v1 < KAPPA_MIN).fillna(False) | pt.clear_flip
    pt["T_evaluable"] = pt.assessable & ~pt.concordance_fail & (pt.n_primary_side > 0)

    # normal-side calibration gate (study)
    ev = pt[pt.assessable & (pt.n_normal_side >= NORM_MIN_CELLS)]
    st = ev.groupby("study_id").agg(n_patients_calib=("patient_id", "size"),
                                    median_normal_cnv_high=("normal_cnv_high_rate", "median"),
                                    max_normal_cnv_high=("normal_cnv_high_rate", "max")).reset_index()
    st = pt.groupby("study_id").agg(n_patients=("patient_id", "size"), n_assessable=("assessable", "sum"),
                                    n_clear=("clear_cnv", "sum"), n_concordance_fail=("concordance_fail", "sum"),
                                    median_kappa_v1=("kappa_v1", "median")).reset_index().merge(st, on="study_id", how="left")
    st["T_status"] = np.where(st.n_patients_calib.fillna(0) < NORM_MIN_PAT, "uncalibrated",
                     np.where(st.median_normal_cnv_high > NORM_MAX, "void", "calibrated"))
    pt = pt.merge(st[["study_id", "T_status"]], on="study_id")
    e = e.merge(pt[["patient_id", "clear_cnv", "T_evaluable", "T_status"]], on="patient_id", how="left")
    e["T_positive"] = (e.cnv_state == "CNV-high") & e.clear_cnv.fillna(False) & e.T_evaluable.fillna(False) \
        & (e.T_status == "calibrated")
    e[["cell_id", "study_id", "patient_id", "sample_id", "side", "stage", "cnv_score", "cnv_cor", "cnv_state",
       "clear_cnv", "T_evaluable", "T_status", "T_positive"]].to_csv(R / "identity_T.private.tsv.gz", sep="\t", index=False)
    pt.to_csv(PUB / "a3b_T_patients.tsv", sep="\t", index=False)
    st.to_csv(PUB / "a3b_T_studies.tsv", sep="\t", index=False)
    print(st.to_string())


if __name__ == "__main__":
    main()
