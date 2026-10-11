#!/usr/bin/env python3
"""A3a step 4: patient -> study -> REML+HK pooling (frozen contract A3a v0.2 §4-§6).

Inputs (private, Argos): sample_correlations, coactivation, TNFRSF12A detection, P3 sample table,
patient metadata (MSI). Outputs: public study-level and pooled tables only (no patient rows).
Rules: sample eligible with >=100 cells (>=50 = coverage sensitivity); patient = mean Fisher z over its
eligible samples; study pooled with >=5 patients; pooled estimate needs >=3 studies; BH within the
primary family (5 P1 core sets x ct2_final x unadjusted) and the CCAT family (not run here).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, "/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/code")
from fig1b_stats import reml_hk  # validated against metafor (Fig. 1b)

P1 = ["proCSC", "revCSC", "Lgr5CSC", "ExtCIOC", "YAPcore"]
ALL = P1 + ["ECOS38", "YAPfetal", "Placenta"]
MIN_PAT, MIN_STUDY = 5, 3


def bh(p):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); adj = np.empty(m); run = 1.0
    for r in range(m - 1, -1, -1):
        i = o[r]; run = min(run, p[i] * m / (r + 1)); adj[i] = run
    return adj


def z(r):
    return np.arctanh(np.clip(r, -0.999999, 0.999999))


def patient_z(d, col):
    d = d[np.isfinite(d[col])]
    return d.assign(z=z(d[col])).groupby(["study_id", "patient_id"], as_index=False).z.mean()


def pool(pz, label):
    st = []
    for s, x in pz.groupby("study_id").z:
        n = len(x)
        if n < MIN_PAT:
            continue
        m, sd = x.mean(), x.std(ddof=1); se = sd / np.sqrt(n); h = stats.t.ppf(0.975, n - 1) * se
        st.append({**label, "study_id": s, "n_patients": n, "z_mean": m, "se": se,
                   "rho": np.tanh(m), "rho_ci_low": np.tanh(m - h), "rho_ci_high": np.tanh(m + h)})
    st = pd.DataFrame(st)
    if len(st) < MIN_STUDY:
        return st, {**label, "k": len(st), "status": "fewer_than_3_studies"}
    r = reml_hk(st.z_mean, st.se)
    loso = [np.tanh(reml_hk(st.z_mean[st.study_id != s], st.se[st.study_id != s])["estimate"]) for s in st.study_id] \
        if len(st) > MIN_STUDY else [np.nan]
    sign = np.sign(r["estimate"])
    out = {**label, "status": "pooled", "k": r["k"], "n_patients": int(st.n_patients.sum()),
           "rho": np.tanh(r["estimate"]), "ci_low": np.tanh(r["ci_low"]), "ci_high": np.tanh(r["ci_high"]),
           "pi_low": np.tanh(r["pi_low"]), "pi_high": np.tanh(r["pi_high"]), "p": r["p"], "tau2": r["tau2"],
           "I2": r["I2"], "studies_same_sign": int((np.sign(st.z_mean) == sign).sum()),
           "loso_min": float(np.nanmin(loso)), "loso_max": float(np.nanmax(loso))}
    return st, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats-dir", required=True)
    ap.add_argument("--patient-meta", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    S, O = Path(a.stats_dir), Path(a.out)
    O.mkdir(parents=True, exist_ok=True)
    sc = pd.read_csv(S / "sample_correlations.private.tsv.gz", sep="\t")
    meta = pd.read_csv(a.patient_meta, sep="\t", usecols=["patient_id", "msi_status"])
    sc = sc.merge(meta, on="patient_id", how="left")
    sc["msi_group"] = sc.msi_status.fillna("unknown").replace({"Unknown": "unknown"})

    pooled, studies = [], []

    def run(d, label, col):
        st, r = pool(patient_z(d, col), label)
        studies.append(st); pooled.append(r)

    base = sc[sc.cellset == "primary"]
    for thr, tname in [(100, "ge100"), (50, "ge50")]:
        for proxy in ["ct2_final", "ct2_raw", "ds_both", "ds_ct2_fixed_programme"]:
            for est in ["unadjusted", "adjusted"]:
                for p in ALL:
                    d = base[(base.n_cells >= thr) & (base.proxy == proxy) & (base.programme == p)]
                    run(d, dict(analysis=f"{proxy}|{est}|{tname}", cellset="primary", programme=p, proxy=proxy,
                                estimand=est, threshold=thr), est)
    for cs in ["F1clean", "malignant", "noncycling"]:
        for est in ["unadjusted", "adjusted"]:
            for p in ALL:
                d = sc[(sc.cellset == cs) & (sc.n_cells >= 100) & (sc.proxy == "ct2_final") & (sc.programme == p)]
                run(d, dict(analysis=f"ct2_final|{est}|ge100|{cs}", cellset=cs, programme=p, proxy="ct2_final",
                            estimand=est, threshold=100), est)
    for p in ["ExtCIOC", "ECOS38"]:  # Khaliq-excluded (Extended CIOC selected partly on Khaliq)
        for est in ["unadjusted", "adjusted"]:
            d = base[(base.n_cells >= 100) & (base.proxy == "ct2_final") & (base.programme == p)
                     & (base.study_id != "Khaliq_2022_Genome_Biol")]
            run(d, dict(analysis=f"ct2_final|{est}|ge100|noKhaliq", cellset="primary", programme=p,
                        proxy="ct2_final", estimand=est, threshold=100), est)
    for g in ["MSS", "MSI-H", "unknown"]:  # effect modifier, descriptive
        for p in P1:
            d = base[(base.n_cells >= 100) & (base.proxy == "ct2_final") & (base.programme == p) & (base.msi_group == g)]
            run(d, dict(analysis=f"ct2_final|unadjusted|ge100|MSI={g}", cellset="primary", programme=p,
                        proxy="ct2_final", estimand="unadjusted", threshold=100), "unadjusted")
    # P2: TNFRSF12A vs CT2 final (primary for P2) + vs programmes (descriptive)
    for est in ["unadjusted", "adjusted"]:
        d = base[(base.n_cells >= 100) & (base.proxy == "ct2_final") & (base.programme == "TNFRSF12A_cpm")]
        run(d, dict(analysis=f"P2|{est}", cellset="primary", programme="TNFRSF12A_cpm", proxy="ct2_final",
                    estimand=est, threshold=100), est)
        for p in ALL:
            d = base[(base.n_cells >= 100) & (base.proxy == f"prog:{p}")]
            run(d, dict(analysis=f"P2desc|{est}", cellset="primary", programme="TNFRSF12A_cpm", proxy=f"prog:{p}",
                        estimand=est, threshold=100), est)
    # programme contrasts (descriptive): per patient z(prog) - z(proCSC)
    for est in ["unadjusted", "adjusted"]:
        d = base[(base.n_cells >= 100) & (base.proxy == "ct2_final")]
        pz = {p: patient_z(d[d.programme == p], est).set_index(["study_id", "patient_id"]).z for p in P1}
        for p in ["revCSC", "ExtCIOC", "YAPcore"]:
            diff = (pz[p] - pz["proCSC"]).dropna().rename("z").reset_index()
            st = []
            for s, x in diff.groupby("study_id").z:
                n = len(x)
                if n >= MIN_PAT:
                    st.append({"study_id": s, "n_patients": n, "z_mean": x.mean(), "se": x.std(ddof=1) / np.sqrt(n)})
            st = pd.DataFrame(st)
            lab = dict(analysis=f"contrast|{est}", cellset="primary", programme=f"{p}-proCSC", proxy="ct2_final",
                       estimand=est, threshold=100)
            if len(st) >= MIN_STUDY:
                r = reml_hk(st.z_mean, st.se)
                pooled.append({**lab, "status": "pooled_descriptive_z_scale", "k": r["k"],
                               "n_patients": int(st.n_patients.sum()), "rho": r["estimate"], "ci_low": r["ci_low"],
                               "ci_high": r["ci_high"], "pi_low": r["pi_low"], "pi_high": r["pi_high"],
                               "I2": r["I2"], "tau2": r["tau2"]})
            studies.append(st.assign(**lab))
    pooled = pd.DataFrame(pooled)
    for c in ["p", "rho", "ci_low", "ci_high", "k", "n_patients"]:
        if c not in pooled:
            pooled[c] = np.nan
    prim = (pooled.analysis == "ct2_final|unadjusted|ge100") & pooled.programme.isin(P1) & (pooled.status == "pooled")
    pooled["family"] = np.where(prim, "primary", "descriptive")
    pooled["p_bh"] = np.nan
    if prim.any():
        pooled.loc[prim, "p_bh"] = bh(pooled.loc[prim, "p"])
    pooled.to_csv(O / "A3a_pooled.tsv", sep="\t", index=False)
    pd.concat([s for s in studies if len(s)], ignore_index=True).to_csv(O / "A3a_study.tsv", sep="\t", index=False)

    # gates and descriptive readouts (study level only)
    det = pd.read_csv(S / "TNFRSF12A_detection_samples.private.tsv", sep="\t")
    p2g = det.groupby("study_id").apply(lambda x: np.average(x.TNFRSF12A_detected_frac, weights=x.epi_cells)).rename(
        "TNFRSF12A_detected_frac").reset_index()
    p2g.to_csv(O / "P2_gate_study.tsv", sep="\t", index=False)
    co = pd.read_csv(S / "coactivation_samples.private.tsv", sep="\t")
    co = co[co.n_cells >= 100]
    cs = co.groupby("study_id").agg(samples=("sample_id", "size"), share_co_high_median=("share_co_high", "median"),
                                    **{f"ct2_median_{k}": (f"ct2_median_{k}", "median")
                                       for k in ["co_high", "pro_only", "rev_only", "neither"]}).reset_index()
    cs.to_csv(O / "coactivation_study.tsv", sep="\t", index=False)
    p3 = pd.read_csv(S / "P3_samples.private.tsv", sep="\t")
    p3 = p3[p3.macrophage_cells >= 30].copy()
    g3 = p3.groupby("study_id").apply(lambda x: x.macrophage_TNFSF12_detected.sum() / x.macrophage_cells.sum()).rename(
        "TNFSF12_detected_frac").reset_index()
    g3.to_csv(O / "P3_gate_study.tsv", sep="\t", index=False)
    p3["TNFSF12_log1p_cpm"] = np.log1p(p3.macrophage_TNFSF12_umi / p3.macrophage_umi * 1e6)
    st3 = []
    for s, x in p3.dropna(subset=["ExtCIOC_median"]).groupby("study_id"):
        if len(x) >= 5:
            rho = stats.spearmanr(x.TNFSF12_log1p_cpm, x.ExtCIOC_median).statistic
            st3.append({"study_id": s, "n_samples": len(x), "rho": rho, "z_mean": z(rho), "se": 1 / np.sqrt(len(x) - 3)})
    st3 = pd.DataFrame(st3)
    st3.to_csv(O / "P3_study.tsv", sep="\t", index=False)
    if len(st3) >= MIN_STUDY:
        r = reml_hk(st3.z_mean, st3.se)
        pd.DataFrame([{"k": r["k"], "rho": np.tanh(r["estimate"]), "ci_low": np.tanh(r["ci_low"]),
                       "ci_high": np.tanh(r["ci_high"]), "p": r["p"], "I2": r["I2"]}]).to_csv(
            O / "P3_pooled.tsv", sep="\t", index=False)
    print(pooled[pooled.family == "primary"][["programme", "k", "n_patients", "rho", "ci_low", "ci_high", "p_bh"]])


if __name__ == "__main__":
    main()
