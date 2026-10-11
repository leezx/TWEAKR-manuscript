#!/usr/bin/env python3
"""Fig. 1c Stage 3 (contract "Stage 3 analysis specification lock"; GPT M1-M5): CT2 joined to frozen v0.3a labels.

phase 'sample' (SGE task = study index): per sample, M5 join checks; contrast estimates for CT2 final, raw,
ds1-5 (unadjusted) and adjusted OLS (full / reduced); M3 OOD-pass-only estimates; M2 continuous partial
Spearman of CT2 with pro/rev. Private sample-level output only.
phase 'pool': M1 eligibility manifest (Stage 1 counts), M5 summary (stop on failure), patient -> study ->
REML+HK pooling, Holm / BH, public aggregate tables (no patient rows).
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, "/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/code")
from fig1b_stats import reml_hk, holm  # noqa: E402

REF = "Absorptive differentiated-like"
CYC = "Cycling Stem/TA"
CLASSES = [CYC, "Secretory differentiated-like", "Transitional stem/secretory",
           "Transitional secretory/absorptive", "Rare lineages"]
UNAUDITED = {"Transitional stem/secretory", "Transitional secretory/absorptive", "Rare lineages"}
COV = ["log_umi", "log_genes", "mito_frac", "S_score", "G2M_score"]
RED = ["log_umi", "log_genes"]
PRIMARY = ["pro_vs_ref", "rev_vs_ref", "pro_vs_rev"]
MIN_PAT, MIN_STUDY = 5, 3


def tagof(s):
    return "".join(c if (c.isalnum() or c in "_.-") else "_" for c in s)


def masks(d):
    st, lin = d.stratum75.values, d.lineage.values
    m = {"pro": st == "pro_dominant", "rev": st == "rev_dominant", "ref": st == "reference"}
    m["pro_cyc"], m["rev_cyc"] = m["pro"] & (lin == CYC), m["rev"] & (lin == CYC)
    for c in CLASSES:
        m[f"cls:{c}"] = lin == c
    return m


def contrasts():
    c = {"pro_vs_ref": ("pro", "ref"), "rev_vs_ref": ("rev", "ref"), "pro_vs_rev": ("pro", "rev"),
         "cycling_pro_vs_rev": ("pro_cyc", "rev_cyc")}
    c.update({f"{k}_vs_ref": (f"cls:{k}", "ref") for k in CLASSES})
    return c


def eligible(nA, nB, b):
    return bool(nA >= 30 and nB >= (50 if b == "ref" else 30))


def mdiff(y, a, b):
    ya, yb = y[a & np.isfinite(y)], y[b & np.isfinite(y)]
    return float(np.median(ya) - np.median(yb)) if len(ya) and len(yb) else np.nan


def ols_coef(y, ind, C):
    ok = np.isfinite(y) & np.all(np.isfinite(C), axis=1)
    y, ind, C = y[ok], ind[ok], C[ok]
    if len(y) < 70 or ind.all() or not ind.any():
        return np.nan, len(y)
    keep = [j for j in range(C.shape[1]) if np.ptp(C[:, j]) > 0]
    X = np.column_stack([np.ones(len(y)), ind.astype(float)] + [C[:, j] for j in keep])
    if np.linalg.matrix_rank(X) < X.shape[1]:
        return np.nan, len(y)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(beta[1]), len(y)


def partial(x, y, Ccont, D):
    """Rank-residual partial Spearman; D = 0/1 dummy matrix. Returns (r, status)."""
    rx, ry = stats.rankdata(x), stats.rankdata(y)
    cols = [stats.rankdata(Ccont[:, j]) for j in range(Ccont.shape[1]) if np.ptp(Ccont[:, j]) > 0]
    cols += [D[:, j] for j in range(D.shape[1]) if np.ptp(D[:, j]) > 0]
    X = np.column_stack([np.ones(len(x))] + cols)
    if np.linalg.matrix_rank(X) < X.shape[1]:
        return np.nan, "ineligible_rank_deficient"
    ex = rx - X @ np.linalg.lstsq(X, rx, rcond=None)[0]
    ey = ry - X @ np.linalg.lstsq(X, ry, rcond=None)[0]
    if ex.std() == 0 or ey.std() == 0:
        return np.nan, "ineligible_constant"
    return float(np.corrcoef(ex, ey)[0, 1]), "ok"


def sample_phase(a):
    files = sorted(Path(a.labels_dir).glob("*.cell_labels.tsv.gz"))
    if a.task > len(files):
        return
    lf = files[a.task - 1]
    study = lf.name[:-len(".cell_labels.tsv.gz")]
    lab = pd.read_csv(lf, sep="\t")
    cov = pd.read_csv(Path(a.cells_dir) / f"{study}.cells.tsv.gz", sep="\t",
                      usecols=["cell_id", "variant", "umi", "genes", "mito_frac", "S_score", "G2M_score"])
    cov = cov[cov.variant == "main"].drop(columns="variant")
    cov["log_umi"], cov["log_genes"] = np.log10(cov.umi.clip(lower=1)), np.log10(cov.genes.clip(lower=1))
    F = Path(a.fig1b_root)
    rows, integ, m2 = [], [], []
    for sample, d in lab.groupby("sample_id"):
        tag = tagof(sample)
        ct = pd.read_csv(F / "full/scores" / f"{tag}.model.scores.tsv.gz", sep="\t",
                         usecols=["cell_id", "whole_score", "intrinsic_score"])
        n_lab = len(d)
        d = d.merge(cov[["cell_id"] + COV], on="cell_id", how="left").merge(ct, on="cell_id", how="left")
        mk = masks(d)
        meta = {"study_id": study, "patient_id": d.patient_id.iloc[0], "sample_id": sample}
        integ.append({**meta, "n_labels": n_lab, "dup_label_ids": int(lab[lab.sample_id == sample].cell_id.duplicated().sum()),
                      "dup_ct2_ids": int(ct.cell_id.duplicated().sum()), "n_merged": len(d),
                      "n_missing_ct2_final": int(d.whole_score.isna().sum()),
                      "n_missing_ct2_raw": int(d.intrinsic_score.isna().sum()),
                      "n_missing_cov": int(d[COV].isna().any(axis=1).sum()),
                      "ref_overlap_prorev": int((mk["ref"] & (mk["pro"] | mk["rev"])).sum()),
                      "n_discordant_in_ref": int((mk["ref"] & d.discordant75.astype(bool).values).sum())})
        yf, yr = d.whole_score.values.astype(float), d.intrinsic_score.values.astype(float)
        C, Cr = d[COV].values.astype(float), d[RED].values.astype(float)
        oodp = d.ood_pass.astype(bool).values
        ds = {}
        for r in range(1, 6):
            p = F / "full/scores_ds" / f"{tag}.ds{r}.scores.tsv.gz"
            if p.exists():
                x = pd.read_csv(p, sep="\t", usecols=["cell_id", "whole_score"]).drop_duplicates("cell_id")
                ds[r] = d[["cell_id"]].merge(x, on="cell_id", how="left").whole_score.values.astype(float)
        for cn, (ga, gb) in contrasts().items():
            A, B = mk[ga], mk[gb]
            nA, nB = int(A.sum()), int(B.sum())
            row = {**meta, "n_cells": n_lab, "contrast": cn, "nA": nA, "nB": nB, "eligible": eligible(nA, nB, gb)}
            Ao, Bo = A & oodp, B & oodp
            row.update(nA_ood=int(Ao.sum()), nB_ood=int(Bo.sum()), eligible_ood=eligible(Ao.sum(), Bo.sum(), gb))
            if row["eligible"]:
                sel = A | B
                row.update(final=mdiff(yf, A, B), raw=mdiff(yr, A, B),
                           medA_final=float(np.nanmedian(yf[A])), medB_final=float(np.nanmedian(yf[B])))
                row["adj_full"], row["n_adj"] = ols_coef(yf[sel], A[sel], C[sel])
                row["adj_reduced"], _ = ols_coef(yf[sel], A[sel], Cr[sel])
                for r, y in ds.items():
                    row[f"ds{r}"] = mdiff(y, A, B)
                    row[f"ds{r}_missA"] = float(np.isnan(y[A]).mean())
                    row[f"ds{r}_missB"] = float(np.isnan(y[B]).mean())
                row["n_ds"] = len(ds)
            if row["eligible_ood"]:
                row["final_ood"] = mdiff(yf, Ao, Bo)
            rows.append(row)
        if n_lab >= 100:
            ok = np.isfinite(yf) & np.all(np.isfinite(C), axis=1)
            x = d[ok]
            levels = x.lineage.value_counts()
            D = np.column_stack([(x.lineage.values == lv).astype(float) for lv in levels.index[1:]]) \
                if len(levels) > 1 else np.empty((len(x), 0))
            for prog, other in [("proCSC", "revCSC"), ("revCSC", "proCSC")]:
                Cc = np.column_stack([x[other].values] + [x[c].values for c in COV])
                r_l, s_l = partial(x[prog].values, x.whole_score.values, Cc, D)
                r_n, s_n = partial(x[prog].values, x.whole_score.values, Cc, np.empty((len(x), 0)))
                r_u = stats.spearmanr(x[prog], x.whole_score).correlation
                m2.append({**meta, "n_cells": int(ok.sum()), "programme": prog, "unadjusted": r_u,
                           "partial_lineage": r_l, "status_lineage": s_l, "partial_nolineage": r_n,
                           "status_nolineage": s_n, "n_lineage_levels": len(levels)})
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / f"{study}.s3_contrasts.private.tsv.gz", sep="\t", index=False)
    pd.DataFrame(integ).to_csv(out / f"{study}.s3_integrity.private.tsv", sep="\t", index=False)
    pd.DataFrame(m2).to_csv(out / f"{study}.s3_m2.private.tsv", sep="\t", index=False)
    print(study, len(integ), flush=True)


# ---------------------------------------------------------------- pooling
def study_table(pv, label):
    st = []
    for s, x in pv.groupby("study_id").v:
        if len(x) >= MIN_PAT:
            st.append({**label, "study_id": s, "n_patients": len(x), "mean": x.mean(),
                       "se": x.std(ddof=1) / np.sqrt(len(x))})
    return pd.DataFrame(st)


def pool_values(pv, label, back=None):
    """pv: study_id, patient_id, v. Returns (study table, pooled row). back: inverse transform (tanh)."""
    f = back or (lambda v: v)
    st = study_table(pv, label)
    base = {**label, "n_patients_eligible": int(len(pv)), "n_studies_any": int(pv.study_id.nunique())}
    if len(st) < MIN_STUDY:
        return st, {**base, "status": "descriptive_fewer_than_3_studies", "k": len(st),
                    "n_patients": int(st.n_patients.sum()) if len(st) else 0}
    r = reml_hk(st["mean"], st.se)
    loso = [f(reml_hk(st["mean"][st.study_id != s], st.se[st.study_id != s])["estimate"]) for s in st.study_id] \
        if len(st) > MIN_STUDY else [np.nan]
    sgn = np.sign(r["estimate"])
    return st, {**base, "status": "pooled", "k": r["k"], "n_patients": int(st.n_patients.sum()),
                "estimate": f(r["estimate"]), "ci_low": f(r["ci_low"]), "ci_high": f(r["ci_high"]),
                "pi_low": f(r["pi_low"]), "pi_high": f(r["pi_high"]), "p": r["p"], "tau2": r["tau2"],
                "I2": r["I2"], "studies_same_sign": int((np.sign(st["mean"]) == sgn).sum()),
                "loso_min": float(np.nanmin(loso)), "loso_max": float(np.nanmax(loso))}


def patient_median(df, col):
    x = df[np.isfinite(df[col])]
    return x.groupby(["study_id", "patient_id"], as_index=False)[col].median().rename(columns={col: "v"})


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pool_phase(a):
    S, P = Path(a.out_dir), Path(a.public_out)
    P.mkdir(parents=True, exist_ok=True)
    integ = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(S.glob("*.s3_integrity.private.tsv"))])
    con = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(S.glob("*.s3_contrasts.private.tsv.gz"))])
    m2 = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(S.glob("*.s3_m2.private.tsv")) if f.stat().st_size > 1])
    summ = {}
    # ---------------- M5 integrity (stop on failure)
    lab_files = sorted(Path(a.labels_dir).glob("*.cell_labels.tsv.gz"))
    hashes = {f.name: sha(f) for f in lab_files}
    g10 = json.load(open(a.stage1_summary)).get("G10", {})
    stage1_hashes = g10.get("cell_labels_sha256", {})
    m5 = {"samples": int(len(integ)), "cells_labelled": int(integ.n_labels.sum()),
          "dup_label_ids": int(integ.dup_label_ids.sum()), "dup_ct2_ids": int(integ.dup_ct2_ids.sum()),
          "merged_equals_labels": bool((integ.n_merged == integ.n_labels).all()),
          "missing_ct2_final": int(integ.n_missing_ct2_final.sum()), "missing_ct2_raw": int(integ.n_missing_ct2_raw.sum()),
          "missing_covariates": int(integ.n_missing_cov.sum()), "ref_overlap_prorev": int(integ.ref_overlap_prorev.sum()),
          "discordant_in_ref": int(integ.n_discordant_in_ref.sum()),
          "label_hash_matches_stage1": (all(stage1_hashes.get(k) == v for k, v in hashes.items())
                                        if stage1_hashes else "stage1_hash_not_recorded"),
          "label_sha256": hashes}
    m5["pass"] = bool(m5["dup_label_ids"] == 0 and m5["dup_ct2_ids"] == 0 and m5["merged_equals_labels"]
                      and m5["ref_overlap_prorev"] == 0 and m5["label_hash_matches_stage1"] is not False)
    json.dump(m5, open(P / "S3_M5_integrity.json", "w"), indent=1)
    if not m5["pass"]:
        print("M5 FAILED", json.dumps({k: v for k, v in m5.items() if k != "label_sha256"}))
        sys.exit(2)
    summ["M5"] = {k: v for k, v in m5.items() if k != "label_sha256"}
    # ---------------- M1 eligibility funnel (Stage 1 counts; identical to G5 definitions)
    funnel = []
    for cn in list(contrasts()):
        x = con[con.contrast == cn]
        b = contrasts()[cn][1]
        lvl1 = x[x.nB >= (50 if b == "ref" else 30)] if b == "ref" else x[x.nA >= 30]
        el = x[x.eligible]
        ep = el.groupby("study_id").patient_id.nunique()
        q = ep[ep >= MIN_PAT]
        funnel.append({"contrast": cn, "patients_total": x.patient_id.nunique(),
                       "L1_patients_with_reference_or_A": lvl1.patient_id.nunique(),
                       "L2_patients_with_eligible_sample": el.patient_id.nunique(),
                       "L2_eligible_samples": int(len(el)),
                       "L3_patients_in_qualifying_studies": int(q.sum()), "L3_studies": int(len(q)),
                       "max_study_share": round(float(q.max() / q.sum()), 4) if len(q) else np.nan})
    funnel = pd.DataFrame(funnel)
    funnel.to_csv(P / "S3_M1_eligibility_funnel.tsv", sep="\t", index=False)
    # ---------------- contrasts
    pooled, studies = [], []

    def run(pv, label):
        st, r = pool_values(pv, label)
        studies.append(st)
        pooled.append(r)

    for cn in contrasts():
        e = con[(con.contrast == cn) & con.eligible].copy()
        fam = "primary_holm" if cn in PRIMARY else ("sensitivity_planned" if cn.startswith("cycling") else "secondary_bh")
        for est in ["final", "raw", "adj_full", "adj_reduced"]:
            run(patient_median(e, est), dict(contrast=cn, estimand=est, family=fam if est == "final" else "robustness"))
        # depth-matched: per replicate patient median, then patient mean over replicates
        per_r = []
        for r in range(1, 6):
            if f"ds{r}" in e:
                pr = patient_median(e, f"ds{r}")
                per_r.append(pr.assign(rep=r))
                st, rr = pool_values(pr, dict(contrast=cn, estimand=f"ds{r}", family="ds_replicate"))
                pooled.append(rr)
        if per_r:
            allr = pd.concat(per_r)
            pm = allr.groupby(["study_id", "patient_id"], as_index=False).v.mean()
            run(pm, dict(contrast=cn, estimand="ds_mean", family="robustness_mandatory"))
            miss = {"contrast": cn, "eligible_samples": int(len(e)),
                    "samples_without_any_ds": int((e.n_ds.fillna(0) == 0).sum()),
                    "patients_ds_mean": int(len(pm))}
            for r in range(1, 6):
                if f"ds{r}" in e:
                    miss[f"ds{r}_samples_missing"] = int(e[f"ds{r}"].isna().sum())
                    miss[f"ds{r}_median_missA"] = float(e[f"ds{r}_missA"].median())
                    miss[f"ds{r}_median_missB"] = float(e[f"ds{r}_missB"].median())
            studies.append(pd.DataFrame([{**miss, "table": "ds_missingness"}]))
        # M3 OOD-pass-only
        eo = con[(con.contrast == cn) & con.eligible_ood]
        run(patient_median(eo, "final_ood"), dict(contrast=cn, estimand="final_ood_pass_only", family="M3_sensitivity"))
    pooled = pd.DataFrame(pooled)
    pooled["p_adj"] = np.nan
    for fam, fn in [("primary_holm", holm), ("secondary_bh", None)]:
        m = (pooled.family == fam) & (pooled.status == "pooled")
        if m.any():
            p = pooled.loc[m, "p"].values
            if fn is holm:
                pooled.loc[m, "p_adj"] = holm(p)
            else:
                o = np.argsort(p); n = len(p); adj = np.empty(n); run_ = 1.0
                for k in range(n - 1, -1, -1):
                    i = o[k]; run_ = min(run_, p[i] * n / (k + 1)); adj[i] = run_
                pooled.loc[m, "p_adj"] = adj
    pooled["unaudited_class"] = pooled.contrast.str.replace("_vs_ref", "").isin(UNAUDITED)
    pooled.to_csv(P / "S3_contrasts_pooled.tsv", sep="\t", index=False)
    st_all = pd.concat([s for s in studies if len(s)], ignore_index=True)
    st_all[st_all.get("table") != "ds_missingness"].drop(columns=[c for c in ["table"] if c in st_all]) \
        .dropna(axis=1, how="all").to_csv(P / "S3_contrasts_by_study.tsv", sep="\t", index=False)
    st_all[st_all.get("table") == "ds_missingness"].dropna(axis=1, how="all") \
        .to_csv(P / "S3_ds_missingness.tsv", sep="\t", index=False)
    # ds replicate variability (not biological uncertainty)
    dsr = pooled[pooled.family == "ds_replicate"]
    dsv = dsr.groupby("contrast").estimate.agg(["mean", "std", "min", "max", "count"]).reset_index()
    dsv.to_csv(P / "S3_ds_replicate_variability.tsv", sep="\t", index=False)
    # descriptive group CT2 (patient median of sample group medians)
    desc = []
    for cn in contrasts():
        e = con[(con.contrast == cn) & con.eligible]
        for g in ["medA_final", "medB_final"]:
            pv = e.groupby("patient_id")[g].median()
            desc.append({"contrast": cn, "group": "A" if g == "medA_final" else "B", "n_patients": len(pv),
                         "median": pv.median(), "q25": pv.quantile(.25), "q75": pv.quantile(.75)})
    pd.DataFrame(desc).to_csv(P / "S3_group_ct2_descriptive.tsv", sep="\t", index=False)
    # ---------------- M2 continuous model (Fisher z; patient = mean z)
    m2p, m2s = [], []
    for prog in ["proCSC", "revCSC"]:
        for est, stc in [("unadjusted", None), ("partial_lineage", "status_lineage"),
                         ("partial_nolineage", "status_nolineage")]:
            x = m2[m2.programme == prog]
            if stc:
                x = x[x[stc] == "ok"]
            x = x[np.isfinite(x[est])]
            pz = x.assign(z=np.arctanh(np.clip(x[est], -0.999999, 0.999999))) \
                .groupby(["study_id", "patient_id"], as_index=False).z.mean().rename(columns={"z": "v"})
            st, r = pool_values(pz, dict(programme=prog, estimand=est), back=np.tanh)
            r["n_samples"] = int(len(x))
            if stc:
                r["n_samples_ineligible"] = int((m2[(m2.programme == prog)][stc] != "ok").sum())
            m2p.append(r)
            m2s.append(st)
    m2p = pd.DataFrame(m2p)
    m2p.to_csv(P / "S3_M2_continuous_pooled.tsv", sep="\t", index=False)
    pd.concat(m2s).to_csv(P / "S3_M2_continuous_by_study.tsv", sep="\t", index=False)
    # ---------------- summary
    keep = ["contrast", "estimand", "family", "status", "k", "n_patients", "estimate", "ci_low", "ci_high",
            "p", "p_adj", "I2", "studies_same_sign", "loso_min", "loso_max"]
    summ["M1"] = funnel.to_dict(orient="records")
    summ["contrasts"] = pooled[[c for c in keep if c in pooled]].round(5).to_dict(orient="records")
    summ["M2"] = m2p.round(5).to_dict(orient="records")
    summ["ds_replicate_variability"] = dsv.round(5).to_dict(orient="records")
    json.dump(summ, open(P / "stage3_summary.json", "w"), indent=1, default=str)
    show = pooled[pooled.family.isin(["primary_holm", "robustness", "robustness_mandatory", "sensitivity_planned",
                                      "secondary_bh", "M3_sensitivity"])]
    print(show[[c for c in keep if c in show]].round(4).to_string())
    print(m2p[["programme", "estimand", "status", "k", "n_patients", "estimate", "ci_low", "ci_high", "p"]].round(4).to_string())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["sample", "pool"])
    ap.add_argument("--task", type=int, default=0)
    ap.add_argument("--labels_dir", required=True)
    ap.add_argument("--cells_dir")
    ap.add_argument("--fig1b_root")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--public_out")
    ap.add_argument("--stage1_summary")
    a = ap.parse_args()
    sample_phase(a) if a.phase == "sample" else pool_phase(a)


if __name__ == "__main__":
    main()
