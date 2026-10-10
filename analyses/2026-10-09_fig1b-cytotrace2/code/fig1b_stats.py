#!/usr/bin/env python3
"""Fig. 1B statistics (contract A2.1) on the full 13-study CytoTRACE2 run and frozen annotation_v1.

Aggregation (contract "Outputs and metrics"): median per sample x compartment -> per patient the
unweighted median across samples; a patient x compartment needs >= min_cells cells (30; 50 for the
stringent set). Contrasts are within-patient differences on the same complete-patient set.
Pooling (contract "Statistics"): per-study mean delta with t-interval -> random-effects REML with
Hartung-Knapp; tau2, I2, 95% prediction interval, leave-one-study-out; Holm over the 3 contrasts.
Studies need >= 5 complete patients (cohort rule) to enter a pooled estimate.

Primary: whole-sample CytoTRACE2_Score, L1 compartments (Atlas), frozen 222 patients.
Review 2026-10-10: F1-clean L1 is a QC sensitivity; the malignant L2 subset never replaces L1.
No parameter here is chosen from results; every set below is pre-specified in the contract.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import optimize, stats

COMP = ["Epithelial", "Immune", "Stromal"]
PAIRS = [("Epithelial", "Immune"), ("Epithelial", "Stromal"), ("Stromal", "Immune")]
MIN_STUDY_PATIENTS = 5


def read_scores(d, manifest):
    m = pd.read_csv(Path(d) / "export_manifest.tsv", sep="\t")
    out = []
    for f, v in zip(m.file, m.variant):
        s = pd.read_csv(Path(d).parent / Path(d).name.replace("counts", "scores") / f.replace(".h5", ".scores.tsv.gz"),
                        sep="\t", usecols=["cell_id", "n_model_genes_detected", "whole_score", "whole_potency",
                                           "intrinsic_score", "intrinsic_potency"])
        s["variant"] = v
        out.append(s)
    return pd.concat(out, ignore_index=True)


def patient_medians(cells, value, group, min_cells):
    sm = cells.groupby(["study_id", "patient_id", "sample_id", group], observed=True)[value].median().rename("v")
    pm = sm.groupby(["study_id", "patient_id", group], observed=True).median()
    n = cells.groupby(["study_id", "patient_id", group], observed=True).size().rename("n_cells")
    pm = pd.concat([pm, n], axis=1).reset_index().rename(columns={group: "group"})
    return pm[pm.n_cells >= min_cells]


def deltas(pm, groups, pairs, patients=None):
    w = pm.pivot_table(index=["study_id", "patient_id"], columns="group", values="v")
    w = w.reindex(columns=groups).dropna()
    if patients is not None:
        w = w[w.index.get_level_values(1).isin(patients)]
    keep = w.groupby(level=0).size()
    w = w[w.index.get_level_values(0).isin(keep[keep >= MIN_STUDY_PATIENTS].index)]
    out = pd.DataFrame({f"{a}-{b}": w[a] - w[b] for a, b in pairs})
    return out.reset_index(), w.reset_index()


def study_table(d, col):
    rows = []
    for s, x in d.groupby("study_id")[col]:
        n = len(x); m = x.mean(); sd = x.std(ddof=1); se = sd / np.sqrt(n)
        h = stats.t.ppf(0.975, n - 1) * se
        rows.append({"study_id": s, "n_patients": n, "mean_delta": m, "sd": sd, "se": se,
                     "ci_low": m - h, "ci_high": m + h, "frac_positive": float((x > 0).mean())})
    return pd.DataFrame(rows)


def reml_hk(y, se):
    y, v = np.asarray(y, float), np.asarray(se, float) ** 2
    k = len(y)

    def nll(t2):
        w = 1 / (v + t2); mu = (w * y).sum() / w.sum()
        return 0.5 * (np.log(v + t2).sum() + np.log(w.sum()) + (w * (y - mu) ** 2).sum())

    t2 = optimize.minimize_scalar(nll, bounds=(0, max(10 * np.var(y), 1e-8)), method="bounded").x
    t2 = 0.0 if nll(0.0) <= nll(t2) else t2
    w = 1 / (v + t2); mu = (w * y).sum() / w.sum()
    q_hk = (w * (y - mu) ** 2).sum() / (k - 1)
    se_hk = np.sqrt(q_hk / w.sum())
    tq = stats.t.ppf(0.975, k - 1)
    wf = 1 / v; muf = (wf * y).sum() / wf.sum(); Q = (wf * (y - muf) ** 2).sum()
    i2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0  # Higgins-Thompson I2 from the fixed-effect Q
    # prediction interval with k-2 df (Higgins, Thompson & Spiegelhalter 2009); metafor uses k-1
    pi = stats.t.ppf(0.975, k - 2) * np.sqrt(t2 + se_hk ** 2) if k > 2 else np.nan
    return {"k": k, "estimate": mu, "se_hk": se_hk, "ci_low": mu - tq * se_hk, "ci_high": mu + tq * se_hk,
            "p": float(2 * stats.t.sf(abs(mu / se_hk), k - 1)), "tau2": t2, "I2": i2, "Q": Q,
            "pi_low": mu - pi, "pi_high": mu + pi}


def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); m = len(p); adj = np.empty(m); run = 0.0
    for r, i in enumerate(o):
        run = max(run, (m - r) * p[i]); adj[i] = min(1.0, run)
    return adj


def analyse(name, pm, groups, pairs, patients, out, loso=False):
    d, w = deltas(pm, groups, pairs, patients)
    pooled, studies = [], []
    for a, b in pairs:
        c = f"{a}-{b}"
        st = study_table(d, c); st.insert(0, "contrast", c); st.insert(0, "analysis", name)
        studies.append(st)
        r = reml_hk(st.mean_delta, st.se); r.update(analysis=name, contrast=c, n_patients=int(len(d)),
                                                     median_patient_delta=float(d[c].median()))
        if loso:
            ests = [reml_hk(st.mean_delta[st.study_id != s], st.se[st.study_id != s])["estimate"]
                    for s in st.study_id]
            lo = pd.DataFrame({"analysis": name, "contrast": c, "left_out": st.study_id, "estimate": ests})
            out.setdefault("loso", []).append(lo)
            r.update(loso_min=float(min(ests)), loso_max=float(max(ests)))
        pooled.append(r)
    pooled = pd.DataFrame(pooled); pooled["p_holm"] = holm(pooled.p)
    out.setdefault("pooled", []).append(pooled)
    out.setdefault("study", []).extend(studies)
    return d, w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="fig1b_cytotrace2_20261009 run root")
    ap.add_argument("--cohort-cells", required=True)
    ap.add_argument("--cohort-patients", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    R = Path(a.root); O = Path(a.out); O.mkdir(parents=True, exist_ok=True)

    ann = pd.read_csv(R / "l2_annotation/final/annotation_v1.tsv.gz", sep="\t",
                      usecols=["cell_id", "study_id", "patient_id", "sample_id", "celltype_L1", "celltype_L2",
                               "cellstate_L3", "F1"])
    coh = pd.read_csv(a.cohort_cells, sep="\t", usecols=["cell_id", "enrichment_class"])
    pts = pd.read_csv(a.cohort_patients)
    ann = ann.merge(coh, on="cell_id", how="left")
    ann["F1"] = ann.F1.astype(str) == "True"
    sc = read_scores(R / "full/counts", None)
    cells = ann.merge(sc, on="cell_id", how="inner")
    assert len(cells) == len(ann), (len(cells), len(ann))
    cells = cells[cells.celltype_L1.isin(COMP)].copy()
    cells["log_genes"] = np.log10(cells.n_model_genes_detected.clip(lower=1))
    allp = set(pts.patient_id)
    out, notes = {}, {}

    # primary + raw model score + pre-specified sensitivities (same aggregation, own patient sets)
    pm = patient_medians(cells, "whole_score", "celltype_L1", 30)
    d_primary, w_primary = analyse("primary", pm, COMP, PAIRS, allp, out, loso=True)
    pm.to_csv(O / "patient_medians_L1_primary.csv", index=False)
    analyse("raw_model_score", patient_medians(cells, "intrinsic_score", "celltype_L1", 30), COMP, PAIRS, allp, out)
    analyse("stringent_50_10", patient_medians(cells, "whole_score", "celltype_L1", 50), COMP, PAIRS,
            set(pts.patient_id[pts.in_stringent_50_10]), out)
    uns = cells[cells.enrichment_class == "unsorted"]
    analyse("unsorted_only", patient_medians(uns, "whole_score", "celltype_L1", 30), COMP, PAIRS,
            set(pts.patient_id[pts.in_unsorted_30_5]), out)
    fib = cells[(cells.celltype_L1 != "Stromal") | (cells.celltype_L2 == "Fibroblast")].copy()
    fib["grp"] = np.where(fib.celltype_L1 == "Stromal", "Fibroblast", fib.celltype_L1)
    fpairs = [("Epithelial", "Immune"), ("Epithelial", "Fibroblast"), ("Fibroblast", "Immune")]
    analyse("fibroblast_L2", patient_medians(fib, "whole_score", "grp", 30), ["Epithelial", "Immune", "Fibroblast"],
            fpairs, set(pts.patient_id[pts.in_fibroblast_30]), out)
    analyse("F1_clean_L1", patient_medians(cells[~cells.F1], "whole_score", "celltype_L1", 30), COMP, PAIRS, allp, out)
    analyse("cycling_negative", patient_medians(cells[cells.cellstate_L3 != "Cycling"], "whole_score",
                                                "celltype_L1", 30), COMP, PAIRS, allp, out)
    analyse("low_gene_excluded_500", patient_medians(cells[cells.n_model_genes_detected >= 500], "whole_score",
                                                     "celltype_L1", 30), COMP, PAIRS, allp, out)

    # detection-adjusted (secondary): per study, OLS of patient delta on delta median log10 detected
    # model genes; the intercept is the adjusted contrast; then REML-HK.
    gm = patient_medians(cells, "log_genes", "celltype_L1", 30)
    gd, _ = deltas(gm, COMP, PAIRS, allp)
    rows, srows = [], []
    for a_, b_ in PAIRS:
        c = f"{a_}-{b_}"
        m = d_primary[["study_id", "patient_id", c]].merge(gd[["patient_id", c]].rename(columns={c: "dg"}),
                                                          on="patient_id")
        for s, x in m.groupby("study_id"):
            f = smf.ols(f"Q('{c}') ~ dg", data=x).fit()
            srows.append({"analysis": "detection_adjusted", "contrast": c, "study_id": s, "n_patients": len(x),
                          "mean_delta": f.params["Intercept"], "se": f.bse["Intercept"],
                          "slope_per_log10_gene": f.params["dg"]})
        st = pd.DataFrame([r for r in srows if r["contrast"] == c])
        r = reml_hk(st.mean_delta, st.se); r.update(analysis="detection_adjusted", contrast=c,
                                                     n_patients=int(len(m)))
        rows.append(r)
    pr = pd.DataFrame(rows); pr["p_holm"] = holm(pr.p)
    out["pooled"].append(pr); out["study"].append(pd.DataFrame(srows))
    gm.to_csv(O / "patient_median_log10_genes_L1.csv", index=False)

    # depth-matched (A1/A2): per seed, T_s-dropped and downsampled cells; eligibility re-applied
    ds = read_scores(R / "full/counts_ds", None)
    ds = ds.merge(ann[["cell_id", "study_id", "patient_id", "sample_id", "celltype_L1"]], on="cell_id")
    ds = ds[ds.celltype_L1.isin(COMP)]
    for v, x in ds.groupby("variant"):
        analyse(f"depth_matched_{v}", patient_medians(x, "whole_score", "celltype_L1", 30), COMP, PAIRS, allp, out)
        analyse(f"depth_matched_raw_{v}", patient_medians(x, "intrinsic_score", "celltype_L1", 30), COMP, PAIRS,
                allp, out)
    del ds

    # supporting mixed model on patient medians (primary)
    lm = w_primary.melt(id_vars=["study_id", "patient_id"], value_vars=COMP, var_name="compartment", value_name="v")
    mm = smf.mixedlm("v ~ C(compartment, Treatment('Immune'))", lm, groups="study_id",
                     vc_formula={"patient": "0 + C(patient_id)"}).fit(reml=True)
    mmt = pd.DataFrame({"coef": mm.params, "se": mm.bse, "ci_low": mm.conf_int()[0], "ci_high": mm.conf_int()[1],
                        "p": mm.pvalues})
    mmt.to_csv(O / "mixed_model_primary.csv")

    # descriptive: cycling shares, potency shares, L2 patient medians (secondary, eligibility rules)
    cells.groupby(["study_id", "celltype_L1"]).cellstate_L3.apply(lambda s: (s == "Cycling").mean()) \
        .rename("frac_cycling").reset_index().to_csv(O / "cycling_share_by_study_L1.csv", index=False)
    cells.groupby(["study_id", "celltype_L1"]).whole_potency.value_counts(normalize=True).rename("share") \
        .reset_index().to_csv(O / "potency_share_by_study_L1.csv", index=False)
    elig = pd.read_csv(R / "l2_annotation/light/l2_eligibility.csv")
    l2types = list(elig.celltype_L2[elig.main_panel])
    l2 = patient_medians(cells[cells.celltype_L2.isin(l2types)], "whole_score", "celltype_L2", 30)
    l2 = l2[l2.patient_id.isin(allp)]
    l2.to_csv(O / "patient_medians_L2.csv", index=False)
    l2.groupby("group").agg(n_patients=("patient_id", "nunique"), n_studies=("study_id", "nunique"),
                            median=("v", "median"), q1=("v", lambda x: x.quantile(.25)),
                            q3=("v", lambda x: x.quantile(.75))).reset_index() \
        .to_csv(O / "L2_patient_median_summary.csv", index=False)
    l2.groupby(["study_id", "group"]).v.median().rename("median_of_patient_medians").reset_index() \
        .to_csv(O / "L2_study_heatmap.csv", index=False)

    pd.concat(out["pooled"]).to_csv(O / "pooled_contrasts.csv", index=False)
    pd.concat(out["study"]).to_csv(O / "study_contrasts.csv", index=False)
    pd.concat(out["loso"]).to_csv(O / "loso_primary.csv", index=False)
    notes = {"n_cells_scored": int(len(cells)), "n_patients_primary": int(len(w_primary)),
             "not_run": {"permissive_20_5": "11 extra patients are outside cohort v1 and were not exported",
                         "HTAPP_HTAN": "not part of cohort v1 exports"},
             "min_study_patients": MIN_STUDY_PATIENTS}
    json.dump(notes, open(O / "stats_notes.json", "w"), indent=1)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
