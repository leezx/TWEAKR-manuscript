#!/usr/bin/env python3
"""A3a POST-HOC checks requested by the 2026-10-11 results review (not part of the frozen contract;
reported separately and labelled post hoc; frozen sets and estimands are unchanged).

1. Self-inclusion: TNFRSF12A is one of the 32 revCSC genes. Rescore revCSC without TNFRSF12A
   (revCSC_noTN, UCell, main counts) and re-estimate (a) TNFRSF12A vs revCSC_noTN and (b) revCSC_noTN vs
   CT2 final, unadjusted and adjusted, with the frozen aggregation.
2. P3: (a) enforce the epithelial >=100-cell rule; (b) patient-level version (mean over a patient's
   eligible samples, then within-study Spearman across patients).
3. Co-activation: observed co-high share vs the per-sample expected share P(pro-high) x P(rev-high).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a3a_sample_stats import COV, corr_pair, prep  # noqa: E402
from a3a_pool import patient_z, pool, reml_hk, z  # noqa: E402


def safe(s):
    return "".join(c if (c.isalnum() or c in "_.-") else "_" for c in s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a3-root", required=True)
    ap.add_argument("--fig1b-root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    A, F, O = Path(a.a3_root), Path(a.fig1b_root), Path(a.out)
    O.mkdir(parents=True, exist_ok=True)
    cells = pd.concat([pd.read_csv(p, sep="\t") for p in sorted((A / "export/cells").glob("*.cells.tsv.gz"))])
    cells = cells[cells.variant == "main"]
    rows = []
    for sample, g in cells.groupby("sample_id"):
        tag = safe(sample)
        uc = pd.read_csv(A / "posthoc/ucell" / f"{tag}.ucell.tsv.gz", sep="\t")
        if uc.empty:
            continue
        uc = uc[uc.variant == "main"].drop(columns="variant")
        ct = pd.read_csv(F / "full/scores" / f"{tag}.model.scores.tsv.gz", sep="\t")
        d = prep(g).merge(uc, on="cell_id").merge(ct[["cell_id", "whole_score"]], on="cell_id")
        if len(d) < 100:
            continue
        cov = d[COV].to_numpy(float)
        meta = dict(study_id=d.study_id.iloc[0], patient_id=d.patient_id.iloc[0], sample_id=sample, n_cells=len(d))
        un, pa = corr_pair(d.TNFRSF12A_cpm, d.revCSC_noTN, cov)
        rows.append({**meta, "test": "TNFRSF12A_vs_revCSC_noTN", "unadjusted": un, "adjusted": pa})
        un, pa = corr_pair(d.revCSC_noTN, d.whole_score, cov)
        rows.append({**meta, "test": "revCSC_noTN_vs_CT2final", "unadjusted": un, "adjusted": pa})
    sc = pd.DataFrame(rows)
    pooled, studies = [], []
    for test in sc.test.unique():
        for est in ["unadjusted", "adjusted"]:
            st, r = pool(patient_z(sc[sc.test == test], est), dict(analysis="posthoc_self_inclusion", test=test, estimand=est))
            pooled.append(r); studies.append(st)
    # P3 QC
    p3 = pd.read_csv(A / "stats/P3_samples.private.tsv", sep="\t")
    p3 = p3[p3.macrophage_cells >= 30].copy()
    p3["TNFSF12_log1p_cpm"] = np.log1p(p3.macrophage_TNFSF12_umi / p3.macrophage_umi * 1e6)
    for label, d in [("P3_epi_ge100_samples", p3[p3.epi_cells >= 100]),
                     ("P3_epi_ge100_patients", p3[p3.epi_cells >= 100].groupby(["study_id", "patient_id"], as_index=False)
                      [["TNFSF12_log1p_cpm", "ExtCIOC_median"]].mean())]:
        st = []
        for s, x in d.dropna(subset=["ExtCIOC_median"]).groupby("study_id"):
            if len(x) >= 5:
                rho = stats.spearmanr(x.TNFSF12_log1p_cpm, x.ExtCIOC_median).statistic
                st.append({"analysis": label, "study_id": s, "n_units": len(x), "rho": rho, "z_mean": z(rho),
                           "se": 1 / np.sqrt(len(x) - 3)})
        st = pd.DataFrame(st); studies.append(st)
        if len(st) >= 3:
            r = reml_hk(st.z_mean, st.se)
            pooled.append({"analysis": label, "status": "pooled", "k": r["k"], "n_units": int(st.n_units.sum()),
                           "rho": np.tanh(r["estimate"]), "ci_low": np.tanh(r["ci_low"]),
                           "ci_high": np.tanh(r["ci_high"]), "p": r["p"], "I2": r["I2"]})
    # co-activation expected share
    co = pd.read_csv(A / "stats/coactivation_samples.private.tsv", sep="\t")
    co = co[co.n_cells >= 100].copy()
    co["expected_co_high"] = co.share_pro_high * co.share_rev_high
    co["obs_over_exp"] = co.share_co_high / co.expected_co_high
    cs = co.groupby("study_id").agg(samples=("sample_id", "size"), share_pro_high_median=("share_pro_high", "median"),
                                    share_rev_high_median=("share_rev_high", "median"),
                                    observed_co_high_median=("share_co_high", "median"),
                                    expected_co_high_median=("expected_co_high", "median"),
                                    obs_over_exp_median=("obs_over_exp", "median")).reset_index()
    pd.DataFrame(pooled).to_csv(O / "A3a_posthoc_pooled.tsv", sep="\t", index=False)
    pd.concat([s for s in studies if len(s)], ignore_index=True).to_csv(O / "A3a_posthoc_study.tsv", sep="\t", index=False)
    cs.to_csv(O / "coactivation_expected_study.tsv", sep="\t", index=False)
    print(pd.DataFrame(pooled).to_string())
    print(cs.to_string())


if __name__ == "__main__":
    main()
