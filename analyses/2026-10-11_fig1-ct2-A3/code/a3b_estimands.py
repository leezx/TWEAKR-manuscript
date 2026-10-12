#!/usr/bin/env python3
"""A3b Stage S estimands (contract A3b v0.3 §4, §6, §7; identity_v1 QA limited GO).

Cells: identity_v1 L1 epithelium. Within a branch, a sample's side value is the median over its cells; a side
with several qualifying samples takes the unweighted median of sample medians. Patient delta = tumour - normal
(normal-primary) or Post - Pre (pre/post). Eligibility is read from the frozen QA table
(eligibility_patients.tsv): E1 (post-matching >= 100 cells/sample), E1_prematch (sensitivity i, programmes).
  E1      depth-matched CT2 final (whole_score; per-cell mean over seeds 1-5; cells present in ds = umi >= T_s)
  E1-s(i)   original-depth CT2 final            E1-s(ii) depth-matched raw model score (intrinsic_score)
  E1-s(iii) complexity-adjusted: per patient, OLS of depth-matched CT2 final (0-1) on side + log UMI + log genes
            + mito fraction + S + G2M (original-depth cell covariates); side coefficient
  E1-L    E1 within Axis-L v0.3a class (Absorptive differentiated-like; Cycling Stem/TA): >= 30 matched class cells
          per qualifying sample; Pelka excluded; class pooled only with >= 20 patients and >= 3 studies
  R       sample-median UCell (original-depth epithelium) delta for proCSC, revCSC, ExtCIOC, YAPcore; BH over 4
  E1-pp   Qin (surgical Post; TRG0 excluded) and Chen (GEO-annotated Post): per-cohort mean delta, t-CI, Wilcoxon
  E3      descriptive: tumour-evidence (tumour side) vs normal-like (normal side), Pelka and Lee only
Pooling (normal-primary): patient -> study mean, t-CI (studies with >= 5 patients) -> REML + Hartung-Knapp (>= 3
studies), PI (k-2 df), I2, LOSO. Outputs: public tables in --public.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

MIN_PAT, MIN_STUDY, CLASS_MIN_CELLS, CLASS_MIN_PAT = 5, 3, 30, 20
CLASSES = ["Absorptive differentiated-like", "Cycling Stem/TA"]
PROGS = ["proCSC", "revCSC", "ExtCIOC", "YAPcore"]
# Clinical-eligibility amendment 2026-10-12 (Stage S review, docs/A3b_stageS_review_20261012.md): Chen P02 is a
# second-line metastatic patient (Chen 2024 STAR Methods), so its Atlas "naive" (pre-anti-PD-1) samples follow prior
# systemic therapy and fail the normal-primary treatment-naive criterion. Excluded from all normal-primary estimands;
# the frozen Atlas-label E1 (P02 included) is kept as a traceable sensitivity.
AMEND_EXCLUDE_NP = {("Chen_2024_Cancer_Cell", "Chen_2024_Cancer_Cell.P02")}


def read_scores(d):
    fs = sorted(Path(d).glob("*.scores.tsv.gz"))
    return pd.concat([pd.read_csv(f, sep="\t", usecols=["cell_id", "whole_score", "intrinsic_score"])
                      .assign(file=f.name) for f in fs], ignore_index=True)


def ds_mean(d):
    s = read_scores(d)
    return s.groupby("cell_id")[["whole_score", "intrinsic_score"]].mean().reset_index()


def side_values(cells, col, min_cells, side_col="side_key"):
    sm = cells.groupby(["study_id", "patient_id", "sample_id", side_col]).agg(v=(col, "median"), n=(col, "size"))
    sm = sm[sm.n >= min_cells].reset_index()
    return sm.groupby(["study_id", "patient_id", side_col]).v.median().unstack(side_col)


def bh(p):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); adj = np.empty(m); run = 1.0
    for r, i in list(enumerate(o))[::-1]:
        run = min(run, p[i] * m / (r + 1)); adj[i] = run
    return adj


def pool(delta, label, reml_hk):
    st = []
    for s, x in delta.groupby(level="study_id"):
        x = x.dropna(); n = len(x)
        if n < MIN_PAT:
            continue
        m, se = x.mean(), x.std(ddof=1) / np.sqrt(n); h = stats.t.ppf(0.975, n - 1) * se
        st.append({**label, "study_id": s, "n_patients": n, "mean_delta": m, "se": se, "ci_low": m - h, "ci_high": m + h})
    st = pd.DataFrame(st)
    if len(st) < MIN_STUDY:
        return st, {**label, "status": "not_estimable_fewer_than_3_studies", "k": len(st),
                    "n_patients": int(st.n_patients.sum()) if len(st) else 0}
    r = reml_hk(st.mean_delta, st.se)
    loso = [reml_hk(st.mean_delta[st.study_id != s], st.se[st.study_id != s])["estimate"] for s in st.study_id] \
        if len(st) > MIN_STUDY else [np.nan]
    sign = np.sign(r["estimate"])
    return st, {**label, "status": "pooled", "k": r["k"], "n_patients": int(st.n_patients.sum()),
                "estimate": r["estimate"], "ci_low": r["ci_low"], "ci_high": r["ci_high"], "p": r["p"],
                "pi_low": r["pi_low"], "pi_high": r["pi_high"], "tau2": r["tau2"], "I2": r["I2"],
                "studies_same_sign": int((np.sign(st.mean_delta) == sign).sum()),
                "loso_min": float(np.nanmin(loso)), "loso_max": float(np.nanmax(loso))}


def cohort(delta, label):
    x = delta.dropna(); n = len(x)
    if n < 2:
        return {**label, "n_patients": n, "status": "too_few"}
    m, se = x.mean(), x.std(ddof=1) / np.sqrt(n); h = stats.t.ppf(0.975, n - 1) * se
    w = stats.wilcoxon(x) if n >= 5 else None
    return {**label, "n_patients": n, "status": "exploratory" if n >= MIN_PAT else "descriptive_lt5",
            "mean_delta": m, "ci_low": m - h, "ci_high": m + h, "median_delta": float(x.median()),
            "n_positive": int((x > 0).sum()), "wilcoxon_p": float(w.pvalue) if w else np.nan}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--fig1b-code", required=True)
    ap.add_argument("--public", required=True)
    a = ap.parse_args()
    sys.path.insert(0, a.fig1b_code)
    from fig1b_stats import reml_hk  # noqa: E402
    R, P = Path(a.root), Path(a.public)
    P.mkdir(parents=True, exist_ok=True)
    idt = pd.read_csv(R / "identity_v1.private.tsv.gz", sep="\t", low_memory=False)
    sl = pd.read_csv(R / "inputs/a3b_samples.tsv", sep="\t")
    el = pd.read_csv(R / "public/eligibility_patients.tsv", sep="\t")
    man = pd.read_csv(R / "inputs/a3b_clinical_manifest.tsv", sep="\t").set_index("sample_id")
    main_s = read_scores(R / "ct2/scores_main")[["cell_id", "whole_score", "intrinsic_score"]] \
        .rename(columns={"whole_score": "ct2_orig", "intrinsic_score": "raw_orig"})
    uc = pd.concat([pd.read_csv(f, sep="\t") for f in sorted((R / "ucell").glob("*.ucell.tsv.gz"))])
    uc = uc[uc.variant == "epi"].drop(columns="variant")
    pooled, studies, pp_rows, qc = [], [], [], []

    for br, tag in [("normal_primary", "np"), ("pre_post", "pp")]:
        ds = ds_mean(R / f"ct2/scores_{tag}").rename(columns={"whole_score": "ct2_ds", "intrinsic_score": "raw_ds"})
        smp = sl[sl.branch == br][["sample_id", "side", "stage"]].drop_duplicates("sample_id")
        c = idt.drop(columns=["side", "stage"]).merge(smp, on="sample_id")
        if br == "normal_primary":
            c["side_key"] = c.side
            A, B = "normal", "tumour"
        else:
            c = c[c.side == "tumour"].copy()
            c["side_key"] = c.stage
            A, B = "Pre", "Post"
        c = c.merge(main_s, on="cell_id", how="left").merge(ds, on="cell_id", how="left").merge(uc, on="cell_id", how="left")
        qc.append(dict(branch=br, cells=len(c), with_ct2_orig=int(c.ct2_orig.notna().sum()),
                       with_ct2_ds=int(c.ct2_ds.notna().sum()), with_ucell=int(c.proCSC.notna().sum()),
                       duplicated_cells=int(c.cell_id.duplicated().sum())))
        if c.cell_id.duplicated().any():
            raise ValueError("duplicate cells within branch")
        e = el[el.branch == br].set_index(["study_id", "patient_id"]).copy()
        # contract §3: Qin TRG0 -> composition only; E1_prematch did not apply this, so enforce it for every readout
        trg0 = e.response.eq("TRG0")
        for col in ["E1_prematch", "E1", "E3"]:
            e[col] = e[col] & ~trg0
        e_frozen = e.copy()
        if br == "normal_primary":
            amend = e.index.isin(list(AMEND_EXCLUDE_NP))
            for col in ["E1_prematch", "E1", "E3"]:
                e[col] = e[col] & ~amend
        if br == "pre_post":  # Qin: surgical Post only (contract §3)
            spec = c.sample_id.map(man.specimen)
            c = c[~(c.study_id.eq("Qin_2023_Cell_Rep_Med") & c.side_key.eq("Post") & ~spec.eq("surgical resection"))]
        cm = c[c.ct2_ds.notna()]
        runs = {
            "E1": (cm, "ct2_ds", 100, "E1"),
            "E1s_i_original_depth": (c, "ct2_orig", 100, "E1_prematch"),
            "E1s_ii_raw_depth_matched": (cm, "raw_ds", 100, "E1"),
        }
        if br == "normal_primary":
            runs["E1_frozen_atlas_label_incl_P02"] = (cm, "ct2_ds", 100, "E1_frozen")
        else:  # descriptive: original depth in exactly the E1 (depth-matched) patients
            runs["E1pp_desc_original_depth_same_patients"] = (c, "ct2_orig", 100, "E1")
        for name, (cc, col, mn, elig) in runs.items():
            sv = side_values(cc, col, mn)
            d = (sv[B] - sv[A]).dropna()
            ok = e_frozen[e_frozen.E1].index if elig == "E1_frozen" else e[e[elig]].index
            d = d[d.index.isin(ok)]
            label = dict(branch=br, estimand=name, value=col)
            if br == "normal_primary":
                st, r = pool(d, label, reml_hk); studies.append(st); pooled.append(r)
            else:
                for s, x in d.groupby(level="study_id"):
                    if s in ("Qin_2023_Cell_Rep_Med", "Chen_2024_Cancer_Cell"):
                        pp_rows.append(cohort(x, {**label, "study_id": s}))
        # (iii) complexity-adjusted
        adj = {}
        for (s, p), g in cm.groupby(["study_id", "patient_id"]):
            if (s, p) not in e.index or not e.loc[(s, p), "E1"]:
                continue
            g = g.dropna(subset=["ct2_ds", "umi", "genes", "mito_frac", "S_score", "G2M_score"])
            if g.side_key.nunique() < 2:
                continue
            X = np.column_stack([np.ones(len(g)), g.side_key.eq(B).astype(float), np.log1p(g.umi), np.log1p(g.genes),
                                 g.mito_frac, g.S_score, g.G2M_score])
            beta = np.linalg.lstsq(X, g.ct2_ds.to_numpy(), rcond=None)[0]
            adj[(s, p)] = beta[1]
        d = pd.Series(adj, dtype=float)
        if len(d):
            d.index = pd.MultiIndex.from_tuples(d.index, names=["study_id", "patient_id"])
        label = dict(branch=br, estimand="E1s_iii_adjusted", value="ct2_ds")
        if br == "normal_primary":
            st, r = pool(d, label, reml_hk); studies.append(st); pooled.append(r)
        else:
            for s, x in d.groupby(level="study_id"):
                if s in ("Qin_2023_Cell_Rep_Med", "Chen_2024_Cancer_Cell"):
                    pp_rows.append(cohort(x, {**label, "study_id": s}))
        # programmes (original-depth UCell, E1_prematch eligibility)
        prog = []
        for pr in PROGS:
            sv = side_values(c, pr, 100)
            d = (sv[B] - sv[A]).dropna()
            d = d[d.index.isin(e[e.E1_prematch].index)]
            label = dict(branch=br, estimand=f"R_{pr}", value=pr)
            if br == "normal_primary":
                st, r = pool(d, label, reml_hk); studies.append(st); prog.append(r)
            else:
                for s, x in d.groupby(level="study_id"):
                    if s in ("Qin_2023_Cell_Rep_Med", "Chen_2024_Cancer_Cell"):
                        pp_rows.append(cohort(x, {**label, "study_id": s}))
        if br == "normal_primary":
            ps = [r.get("p", np.nan) for r in prog]
            ok = [i for i, p in enumerate(ps) if np.isfinite(p)]
            if ok:
                adjp = bh([ps[i] for i in ok])
                for j, i in enumerate(ok):
                    prog[i]["p_bh"] = adjp[j]
            pooled += prog
            # E1-L (Pelka excluded)
            for cl in CLASSES:
                cc = cm[cm.axisL_v03a.eq(cl) & ~cm.study_id.eq("Pelka_2021_Cell")]
                sv = side_values(cc, "ct2_ds", CLASS_MIN_CELLS)
                if A not in sv or B not in sv:
                    pooled.append(dict(branch=br, estimand=f"E1L_{cl}", status="no_pairs")); continue
                d = (sv[B] - sv[A]).dropna()
                d = d[d.index.isin(e[e.E1].index)]
                label = dict(branch=br, estimand=f"E1L_{cl}", value="ct2_ds")
                st, r = pool(d, label, reml_hk)
                if r.get("status") == "pooled" and r["n_patients"] < CLASS_MIN_PAT:
                    r["status"] = "descriptive_lt20_patients"
                studies.append(st); pooled.append(r)
            # E3 descriptive (Pelka, Lee): tumour-evidence (tumour side) vs normal-like (normal side), depth-matched
            t3 = cm[(cm.side_key.eq(B) & cm.identity.eq("tumour_evidence")) | (cm.side_key.eq(A) & cm.identity.eq("normal_like"))]
            sv = side_values(t3, "ct2_ds", 30)
            if A in sv and B in sv:
                d = (sv[B] - sv[A]).dropna()
                d = d[d.index.isin(e[e.E3].index)]
                for s, x in d.groupby(level="study_id"):
                    if s in ("Pelka_2021_Cell", "Lee_2020_Nat_Genet"):
                        pp_rows.append(cohort(x, dict(branch=br, estimand="E3_descriptive", value="ct2_ds", study_id=s)))
            # patient-level deltas for figures (E1)
            sv = side_values(cm, "ct2_ds", 100)
            dd = (sv[B] - sv[A]).dropna().rename("delta_E1").reset_index()
            dd = dd[dd.set_index(["study_id", "patient_id"]).index.isin(e[e.E1].index)]
            dd.to_csv(P / "E1_patient_deltas.tsv", sep="\t", index=False)
        else:
            sv = side_values(cm, "ct2_ds", 100)
            dd = (sv[B] - sv[A]).dropna().rename("delta_E1pp").reset_index()
            dd = dd[dd.set_index(["study_id", "patient_id"]).index.isin(e[e.E1].index)]
            dd.to_csv(P / "E1pp_patient_deltas.tsv", sep="\t", index=False)

    pd.DataFrame(pooled).to_csv(P / "A3b_pooled.tsv", sep="\t", index=False)
    pd.concat([s for s in studies if len(s)]).to_csv(P / "A3b_study.tsv", sep="\t", index=False)
    pd.DataFrame(pp_rows).to_csv(P / "A3b_cohort_estimates.tsv", sep="\t", index=False)
    pd.DataFrame(qc).to_csv(P / "A3b_stageS_join_qc.tsv", sep="\t", index=False)
    print(pd.DataFrame(qc).to_string())
    print(pd.DataFrame(pooled)[["estimand", "status", "k", "n_patients", "estimate", "ci_low", "ci_high", "pi_low",
                                "pi_high", "I2"]].to_string())
    print(pd.DataFrame(pp_rows)[["estimand", "study_id", "n_patients", "mean_delta", "ci_low", "ci_high",
                                 "wilcoxon_p"]].to_string())


if __name__ == "__main__":
    main()
