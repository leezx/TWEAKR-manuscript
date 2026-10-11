#!/usr/bin/env python3
"""Fig. 1c Stage 1 phase 2 (contract v0.3 §4-§5): evaluate gates G1-G10 and apply the decision matrix.

Aggregation for G2-G4/G7: sample = evaluable with >=100 cells; patient value = median over its samples;
pooled = Fisher z of patient values -> study (>=5 patients) -> REML+HK (A3a pool / Fig. 1b reml_hk).
G5/G6/G9 use contrast-specific sample eligibility at the 75th percentile (70/80 reported).
Private outputs: frozen cell labels + hashes. Public outputs (tables/stage1): study-level and pooled only.
CT2-blinded.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_recall_fscore_support

sys.path.insert(0, "/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011/code")
from a3a_pool import pool  # noqa: E402

REF = "Absorptive differentiated-like"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ece(conf, correct, bins=15):
    e, edges = 0.0, np.linspace(0, 1, bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            e += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return float(e)


def patient_median(s, col):
    d = s[(s.n_cells >= 100) & np.isfinite(s[col])]
    return d.groupby(["study_id", "patient_id"], as_index=False)[col].median()


def pooled(s, col, label):
    pm = patient_median(s, col)
    pz = pm.assign(z=np.arctanh(np.clip(pm[col], -0.999999, 0.999999)))[["study_id", "patient_id", "z"]]
    st, out = pool(pz, {"metric": label})
    out["n_patients_evaluable"] = len(pm)
    out["patient_median"] = float(pm[col].median()) if len(pm) else np.nan
    out["frac_patients_pos"] = float((pm[col] > 0).mean()) if len(pm) else np.nan
    return st, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--patient_meta", required=True)
    ap.add_argument("--public_out", required=True)
    ap.add_argument("--phase1", default="stage1/phase1", help="phase-1 directory relative to root")
    ap.add_argument("--summary_name", default="stage1/stage1_gate_summary.json")
    a = ap.parse_args()
    R = Path(a.root)
    pub = Path(a.public_out)
    pub.mkdir(parents=True, exist_ok=True)
    res = {}

    # ---------- G1 / G8: Axis L on held-out Pelka ----------
    oof = pd.concat([pd.read_csv(f, sep="\t") for f in sorted((R / "axisL/models").glob("oof_fold*.tsv.gz"))])
    classes = sorted(oof.true_agg.unique())
    g1 = {"macroF1_agg_all": f1_score(oof.true_agg, oof.pred_agg, average="macro"),
          "macroF1_11_all": f1_score(oof.true11, oof.pred11, average="macro"),
          "macroF1_agg_tumour": f1_score(oof[oof.tissue == "T"].true_agg, oof[oof.tissue == "T"].pred_agg, average="macro"),
          "macroF1_agg_normal": f1_score(oof[oof.tissue == "N"].true_agg, oof[oof.tissue == "N"].pred_agg, average="macro"),
          "ECE_agg": ece(oof.maxp_agg.values, (oof.pred_agg == oof.true_agg).values),
          "assigned_frac": float(oof.assigned.mean()),
          "accuracy_among_assigned": float((oof[oof.assigned].pred_agg == oof[oof.assigned].true_agg).mean()),
          "n_cells": len(oof), "n_patients": int(oof.PID.nunique())}
    okB = (oof.maxp_agg >= 0.70) & (oof.margin_agg >= 0.20)
    g1["v03a_assigned_frac"] = float(okB.mean())
    g1["v03a_accuracy_among_assigned"] = float((oof[okB].pred_agg == oof[okB].true_agg).mean())
    g1["v03a_macroF1_agg_assigned"] = f1_score(oof[okB].true_agg, oof[okB].pred_agg, average="macro")
    to = pd.concat([pd.read_csv(f, sep="\t") for f in sorted((R / "axisL/models").glob("tumouronly_fold*.tsv.gz"))])
    g1["macroF1_agg_tumour_only_training"] = f1_score(to.true_agg, to.pred_agg, average="macro")
    pr, rc, f1, n = precision_recall_fscore_support(oof.true_agg, oof.pred_agg, labels=classes, zero_division=0)
    per = pd.DataFrame({"class": classes, "precision": pr, "recall": rc, "f1": f1, "n": n})
    for t in ["T", "N"]:
        o = oof[oof.tissue == t]
        _, rct, _, nt = precision_recall_fscore_support(o.true_agg, o.pred_agg, labels=classes, zero_division=0)
        per[f"recall_{t}"], per[f"n_{t}"] = rct, nt
    per["rare_uncertain"] = per.recall < 0.50
    per.to_csv(pub / "G1_axisL_per_class.tsv", sep="\t", index=False)
    pd.crosstab([oof.tissue, oof.true_agg], oof.pred_agg, normalize="index").round(4) \
        .to_csv(pub / "G1_axisL_confusion_by_tissue.tsv", sep="\t")
    loco = pd.concat([pd.read_csv(f, sep="\t") for f in sorted((R / "axisL/models").glob("loco_fold*.tsv"))])
    loco.groupby("held_out_class")[["auroc_1_minus_maxp", "auroc_ood_pct", "unknown_rejected_frac",
                                    "known_rejected_frac"]].mean().round(4).to_csv(pub / "G8_loco_unknown_rejection.tsv", sep="\t")
    fold_info = [json.loads((R / f"axisL/models/axisL_fold{k}.json").read_text()) for k in range(6)]
    pd.DataFrame(fold_info).to_csv(pub / "G1_axisL_fold_info.tsv", sep="\t", index=False)
    res["G1"] = {**{k: (round(v, 4) if isinstance(v, float) else v) for k, v in g1.items()},
                 "pass": bool(g1["macroF1_agg_all"] >= 0.70),
                 "rare_uncertain_classes": per[per.rare_uncertain]["class"].tolist()}

    # ---------- load phase-1 outputs ----------
    s = pd.concat([pd.read_csv(f, sep="\t") for f in sorted((R / a.phase1).glob("*.sample_stats.tsv"))])
    meta = pd.read_csv(a.patient_meta, sep="\t", usecols=["patient_id", "msi_status"])
    s = s.merge(meta, on="patient_id", how="left")
    s["msi_group"] = s.msi_status.fillna("unknown").replace({"Unknown": "unknown"})
    ok = s[s.status == "ok"]
    res["inputs"] = {"samples": int(len(s)), "samples_ok": int(len(ok)),
                     "samples_missing": s[s.status != "ok"].sample_id.tolist(),
                     "ucell_set_counts": sorted(ok.n_ucell_sets.unique().tolist()),
                     "cells": int(ok.n_cells.sum()), "patients": int(ok.patient_id.nunique())}

    # G8 cohort: unresolved fraction per study
    lin = ok.filter(like="lin_n|").fillna(0)
    lin.columns = [c.split("|", 1)[1] for c in lin.columns]
    lin_st = lin.groupby(ok.study_id).sum()
    lin_frac = lin_st.div(lin_st.sum(axis=1), axis=0).round(4)
    lin_frac.to_csv(pub / "G8_lineage_composition_by_study.tsv", sep="\t")

    # ---------- G2 ----------
    man = json.loads((R / "stage0/stage0_manifest.json").read_text())
    logo = pd.concat([pd.read_csv(f, sep="\t") for f in sorted((R / a.phase1).glob("*.logo.tsv.gz"))])
    logo = logo[logo.n_cells >= 100]
    g2 = {}
    for st_ in ["proCSC", "revCSC"]:
        pm = patient_median(ok, f"G2_split_rho|{st_}")
        lg = logo[logo.set == st_].groupby(["gene", "study_id", "patient_id"]).rho.median().groupby("gene").median()
        g2[st_] = {"coverage": man["sets"][st_]["atlas_coverage"],
                   "split_overall_median": float(pm[f"G2_split_rho|{st_}"].median()),
                   "logo_min_overall_rho": float(lg.min()), "logo_worst_gene_rank": lg.idxmin(),
                   "n_patients": len(pm)}
        g2[st_]["pass"] = bool(g2[st_]["coverage"] >= 0.80 and g2[st_]["split_overall_median"] >= 0.80
                               and (1 - g2[st_]["logo_min_overall_rho"]) <= 0.10)
        lg.rename("overall_median_rho").to_csv(pub / f"G2_logo_{st_}.tsv", sep="\t")
    res["G2"] = {**g2, "pass": bool(g2["proCSC"]["pass"] and g2["revCSC"]["pass"])}

    # ---------- G3 / G4 / agreements / G7 (pooled) ----------
    rows, studies = [], []
    metrics = ["rho|rev_hOnF_no", "rho|rev_hOnF", "rho|pro_hStem_no", "rho|pro_hStem", "rho|pro_rev",
               "rho|pro_noCC_rev", "rho|pro_mb", "rho|rev_mb", "rho|pro_noCC",
               "G4_partial|rev_hOnF_no", "G4_partial|pro_hStem_no"] + [c for c in ok.columns if c.startswith("G7|")]
    for mcol in metrics:
        st, out = pooled(ok, mcol, mcol)
        rows.append(out)
        if len(st):
            studies.append(st)
    pt = pd.DataFrame(rows)
    pt.to_csv(pub / "G3_G4_G7_pooled.tsv", sep="\t", index=False)
    pd.concat(studies).to_csv(pub / "G3_G4_G7_study.tsv", sep="\t", index=False)
    P = pt.set_index("metric")

    def ci_pos(m):
        return bool(P.loc[m, "status"] == "pooled" and P.loc[m, "ci_low"] > 0)
    g3_assessable = man["hOnF_no_present_in_atlas"] >= 10
    res["G3"] = {"assessable": bool(g3_assessable),
                 "rev_frac_patients_pos": round(float(P.loc["rho|rev_hOnF_no", "frac_patients_pos"]), 4),
                 "rev_pooled_rho": round(float(P.loc["rho|rev_hOnF_no", "rho"]), 4),
                 "rev_pass": bool(g3_assessable and P.loc["rho|rev_hOnF_no", "frac_patients_pos"] >= 2 / 3
                                  and ci_pos("rho|rev_hOnF_no")),
                 "pro_frac_patients_pos": round(float(P.loc["rho|pro_hStem_no", "frac_patients_pos"]), 4),
                 "pro_pooled_rho": round(float(P.loc["rho|pro_hStem_no", "rho"]), 4),
                 "pro_pass": bool(P.loc["rho|pro_hStem_no", "frac_patients_pos"] >= 2 / 3 and ci_pos("rho|pro_hStem_no"))}
    a_ = float(P.loc["rho|pro_rev", "patient_median"])
    res["G4"] = {"a_median_patient_rho_pro_rev": round(a_, 4), "a_pass": bool(a_ < 0.90),
                 "b_partial_rev_hOnF_no": round(float(P.loc["G4_partial|rev_hOnF_no", "rho"]), 4),
                 "b_pass": ci_pos("G4_partial|rev_hOnF_no"),
                 "c_partial_pro_hStem_no": round(float(P.loc["G4_partial|pro_hStem_no", "rho"]), 4),
                 "c_pass": ci_pos("G4_partial|pro_hStem_no")}
    hyb = {p: {"obs": float(ok[ok.n_cells >= 100][f"hybrid_obs|p{p}"].median()),
               "exp": float(ok[ok.n_cells >= 100][f"hybrid_exp|p{p}"].median())} for p in [70, 75, 80]}
    res["G4"]["d_hybrid_sample_median"] = hyb
    res["G4"]["pass"] = bool(res["G4"]["a_pass"] and res["G4"]["b_pass"] and res["G4"]["c_pass"])

    # ---------- G5 / G6 / G9: contrast-specific eligibility ----------
    elig_rows, g5 = [], {}
    for pct in [70, 75, 80]:
        defs = {"pro_vs_ref": (ok[f"n_pro_dominant|p{pct}"] >= 30) & (ok[f"n_ref|p{pct}"] >= 50),
                "rev_vs_ref": (ok[f"n_rev_dominant|p{pct}"] >= 30) & (ok[f"n_ref|p{pct}"] >= 50),
                "pro_vs_rev": (ok[f"n_pro_dominant|p{pct}"] >= 30) & (ok[f"n_rev_dominant|p{pct}"] >= 30),
                "pro_vs_rev_within_stem": (ok[f"n_pro_dominant_stemlineage|p{pct}"] >= 30)
                & (ok[f"n_rev_dominant_stemlineage|p{pct}"] >= 30)}
        for cname, e in defs.items():
            ep = ok[e].groupby("study_id").patient_id.nunique()
            qual = ep[ep >= 5]
            r = {"pct": pct, "contrast": cname, "eligible_samples": int(e.sum()),
                 "eligible_patients_all": int(ep.sum()), "studies_qualifying": int(len(qual)),
                 "patients_in_qualifying_studies": int(qual.sum()),
                 "max_study_share": round(float(qual.max() / qual.sum()), 4) if len(qual) else np.nan}
            r["pass"] = bool(r["patients_in_qualifying_studies"] >= 20 and r["studies_qualifying"] >= 3)
            r["G9_warning"] = bool(r["max_study_share"] > 0.40) if len(qual) else False
            elig_rows.append(r)
            if pct == 75:
                g5[cname] = r
                # eligibility audit: included vs excluded patients (aggregated)
                pat = ok.groupby(["study_id", "patient_id"]).agg(
                    msi=("msi_group", "first"), median_umi=("median_umi", "median"),
                    n_cells=("n_cells", "sum"), n_ref=(f"n_ref|p{pct}", "sum")).reset_index()
                inc = set(ok[e].patient_id)
                pat["included"] = pat.patient_id.isin(inc)
                pat["ref_frac"] = pat.n_ref / pat.n_cells
                aud = pat.groupby("included").agg(n=("patient_id", "size"), median_umi=("median_umi", "median"),
                                                  median_ref_frac=("ref_frac", "median"),
                                                  msi_h=("msi", lambda v: int((v == "MSI-H").sum())),
                                                  mss=("msi", lambda v: int((v == "MSS").sum())),
                                                  msi_unknown=("msi", lambda v: int((v == "unknown").sum())))
                aud.to_csv(pub / f"G5_audit_{cname}.tsv", sep="\t")
                pd.crosstab(pat.study_id, pat.included).to_csv(pub / f"G5_audit_{cname}_by_study.tsv", sep="\t")
    pd.DataFrame(elig_rows).to_csv(pub / "G5_G6_G9_eligibility.tsv", sep="\t", index=False)
    # top rev tertile lacking a reference
    pr_ = ok.groupby("patient_id").agg(ref=("n_ref|p75", "max"))
    revmed = pd.concat([pd.read_csv(f, sep="\t", usecols=["patient_id", "revCSC"])
                        for f in sorted((R / a.phase1).glob("*.cell_labels.tsv.gz"))]) \
        .groupby("patient_id").revCSC.median()
    top = revmed[revmed >= revmed.quantile(2 / 3)].index
    lack = float((pr_.reindex(top).ref < 50).mean())
    res["G5"] = {**{k: {"patients": v["patients_in_qualifying_studies"], "studies": v["studies_qualifying"],
                        "pass": v["pass"]} for k, v in g5.items()},
                 "top_rev_tertile_lacking_reference_frac": round(lack, 4),
                 "secondary_continuous_model_triggered": bool(lack > 0.25)}
    res["G6"] = {"patients": g5["pro_vs_rev"]["patients_in_qualifying_studies"],
                 "studies": g5["pro_vs_rev"]["studies_qualifying"], "pass": g5["pro_vs_rev"]["pass"]}
    res["G9"] = {k: {"max_study_share": v["max_study_share"], "warning": v["G9_warning"]} for k, v in g5.items()}

    # stratum lineage composition (aggregate, 75th pct)
    sl = ok.filter(like="stratum_lin|").sum()
    sl.index = pd.MultiIndex.from_tuples([tuple(i.split("|")[1:]) for i in sl.index], names=["stratum", "lineage"])
    sl.unstack(fill_value=0).to_csv(pub / "strata75_lineage_composition.tsv", sep="\t")
    res["strata75_cells"] = {g: int(ok[f"n_{g}|p75"].sum()) for g in
                             ["pro_dominant", "rev_dominant", "hybrid_high", "neither_high"]}
    res["strata75_cells"]["reference"] = int(ok["n_ref|p75"].sum())
    res["strata75_cells"]["discordant_in_reference"] = int(ok["n_discordant|p75"].sum())

    # old (v0.3, OOD veto) -> new (current phase-1 labels) transition, cell counts
    lab = pd.concat([pd.read_csv(f, sep="\t", usecols=["study_id", "lineage", "pred_agg", "ood_pass"])
                     for f in sorted((R / a.phase1).glob("*.cell_labels.tsv.gz"))], ignore_index=True)
    old = np.where(lab.ood_pass & ~lab.lineage.isin(["lineage-unresolved"]), lab.pred_agg, "lineage-unresolved")
    pd.crosstab(pd.Series(old, name="v03_lineage"), lab.lineage.rename("current_lineage")) \
        .to_csv(pub / "label_transition_v03_to_current.tsv", sep="\t")
    pd.crosstab(lab.study_id, lab.lineage, normalize="index").round(4) \
        .to_csv(pub / "G8_lineage_composition_by_study_current.tsv", sep="\t")

    # ---------- G10 + decision ----------
    labels = sorted((R / a.phase1).glob("*.cell_labels.tsv.gz"))
    res["G10"] = {"stage0_manifest_sha256": sha(R / "stage0/stage0_manifest.json"),
                  "genesets_sha256": sha(R / "private/genesets_fig1c.private.tsv"),
                  "holdout_sha256": sha(R / "private/holdout_H.private.txt"),
                  "pelka_folds_sha256": sha(R / "axisL/ref/pelka_outer_folds.tsv"),
                  "code_sha256": {f.name: sha(f) for f in sorted((R / "code").glob("fig1c_*.py"))},
                  "cell_labels_sha256": {f.name: sha(f) for f in labels}}
    res["G10"]["pass"] = bool(res["inputs"]["samples_missing"] == [] and len(res["inputs"]["ucell_set_counts"]) == 1)
    G1, G2, G10 = res["G1"]["pass"], res["G2"]["pass"], res["G10"]["pass"]
    if not G2:
        branch = "G2 fail: stop two-configuration claim"
    elif not G1:
        branch = "G1 fail: lineage-independent programme description only"
    elif not res["G4"]["a_pass"]:
        branch = "shared stem-associated programme architecture (contrasts descriptive)"
    elif res["G3"]["rev_pass"] and not res["G4"]["c_pass"]:
        branch = "proliferation- vs oncofetal-associated programmes (weaker pro wording)"
    elif res["G3"]["rev_pass"] and res["G4"]["pass"]:
        branch = "distinct transcriptional configurations, possibly hybrid continuum"
    else:
        branch = "gates G1/G2 pass; G3/G4 do not support distinct-configuration wording (descriptive)"
    res["decision"] = {"branch": branch, "formal_contrasts_allowed": {
        k: bool(G1 and G2 and G10 and v["pass"]) for k, v in g5.items()}}
    (pub / "stage1_gate_summary.json").write_text(json.dumps(res, indent=1, default=str))
    (R / a.summary_name).write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({k: res[k] for k in ["inputs", "G1", "G2", "G3", "G4", "G5", "G6", "decision"]}, indent=1, default=str))


if __name__ == "__main__":
    main()
