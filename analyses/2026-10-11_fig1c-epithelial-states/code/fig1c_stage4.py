#!/usr/bin/env python3
"""Fig. 1c Stage 4 sensitivities (contract "Stage 4 specification"; GPT Stage 3 review).

phase 'sample' (SGE task = study index): per sample, group-median CT2 differences for each variant
(p70/p80, mechanism-blinded strata, reference strict/broad, CNV+ (malignant) subset, CCAT, ds-intersection
A/B/C), depth-dropout audit D1, mb membership transitions, CCAT M2. Private output.
phase 'pool': pooling of every variant, MSI/MSS, LOSO, common-subset comparisons, D1-D3 summaries,
sample-universe reconciliation. Public aggregate tables only.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent))
from fig1c_stage3 import (CYC, COV, REF, eligible, mdiff, partial, patient_median,  # noqa: E402
                          pool_values, reml_hk, tagof)

SEC = "Secretory differentiated-like"
CONTRASTS = {"pro_vs_ref": ("pro", "ref"), "rev_vs_ref": ("rev", "ref"), "pro_vs_rev": ("pro", "rev"),
             "cycling_pro_vs_rev": ("pro_cyc", "rev_cyc")}
PRIMARY = ["pro_vs_ref", "rev_vs_ref", "pro_vs_rev"]


def groups_from(stratum, lin):
    g = {"pro": stratum == "pro_dominant", "rev": stratum == "rev_dominant", "ref": stratum == "reference"}
    g["pro_cyc"], g["rev_cyc"] = g["pro"] & (lin == CYC), g["rev"] & (lin == CYC)
    return g


def strata_like_stage1(pro, rev, is_ref, pct=75):
    ph, rh = pro >= np.percentile(pro, pct), rev >= np.percentile(rev, pct)
    s = np.select([ph & ~rh, rh & ~ph, ph & rh], ["pro_dominant", "rev_dominant", "hybrid_high"], "neither_high")
    return np.where(is_ref, "reference", s)


def contrast_rows(meta, variant, g, y, sel=None):
    out = []
    for cn, (a, b) in CONTRASTS.items():
        A, B = g[a], g[b]
        if sel is not None:
            A, B = A & sel, B & sel
        nA, nB = int(A.sum()), int(B.sum())
        el = eligible(nA, nB, b)
        out.append({**meta, "variant": variant, "contrast": cn, "nA": nA, "nB": nB, "eligible": el,
                    "est": mdiff(y, A, B) if el else np.nan})
    return out


def sample_phase(a):
    files = sorted(Path(a.labels_dir).glob("*.cell_labels.tsv.gz"))
    if a.task > len(files):
        return
    lf = files[a.task - 1]
    study = lf.name[:-len(".cell_labels.tsv.gz")]
    lab = pd.read_csv(lf, sep="\t")
    cov = pd.read_csv(Path(a.cells_dir) / f"{study}.cells.tsv.gz", sep="\t",
                      usecols=["cell_id", "variant", "celltype_L2", "umi", "genes", "mito_frac", "S_score", "G2M_score"])
    cov = cov[cov.variant == "main"].drop(columns="variant")
    cov["log_umi"], cov["log_genes"] = np.log10(cov.umi.clip(lower=1)), np.log10(cov.genes.clip(lower=1))
    F, CC = Path(a.fig1b_root), Path(a.ccat_dir)
    rows, d1, trans, m2c = [], [], [], []
    for sample, d in lab.groupby("sample_id"):
        tag = tagof(sample)
        ct = pd.read_csv(F / "full/scores" / f"{tag}.model.scores.tsv.gz", sep="\t", usecols=["cell_id", "whole_score"])
        d = d.merge(cov, on="cell_id", how="left").merge(ct, on="cell_id", how="left")
        cp = CC / f"{tag}.ccat.tsv.gz"
        d = d.merge(pd.read_csv(cp, sep="\t"), on="cell_id", how="left") if cp.exists() else d.assign(CCAT=np.nan)
        meta = {"study_id": study, "patient_id": d.patient_id.iloc[0], "sample_id": sample}
        lin = d.lineage.values
        y = d.whole_score.values.astype(float)
        g75 = groups_from(d.stratum75.values, lin)
        rows += contrast_rows(meta, "base", g75, y)
        for p in [70, 80]:
            rows += contrast_rows(meta, f"p{p}", groups_from(d[f"stratum{p}"].values, lin), y)
        # mechanism-blinded strata
        smb = strata_like_stage1(d.proCSC_mb.values, d.revCSC_mb.values, lin == REF)
        rows += contrast_rows(meta, "mechanism_blinded", groups_from(smb, lin), y)
        ct_ = pd.crosstab(d.stratum75, pd.Series(smb, index=d.index, name="mb")).stack()
        trans += [{**meta, "full": k[0], "mb": k[1], "n": int(v)} for k, v in ct_.items()]
        # reference sensitivities
        gs = dict(g75)
        gs["ref"] = g75["ref"] & ~(d.pro_high75.astype(bool).values | d.rev_high75.astype(bool).values)
        rows += contrast_rows(meta, "ref_strict", gs, y)
        gb = {k: v & (lin != SEC) for k, v in g75.items()}
        gb["ref"] = g75["ref"] | (lin == SEC)
        rows += contrast_rows(meta, "ref_broad", gb, y)
        # CNV+ (Atlas malignant call) subset
        rows += contrast_rows(meta, "cnv_malignant", g75, y, sel=(d.celltype_L2 == "Malignant epithelial").values)
        # CCAT
        rows += contrast_rows(meta, "ccat", g75, d.CCAT.values.astype(float))
        # depth: presence per replicate, intersection
        pres, dsv = [], []
        for r in range(1, 6):
            p = F / "full/scores_ds" / f"{tag}.ds{r}.scores.tsv.gz"
            if p.exists():
                x = pd.read_csv(p, sep="\t", usecols=["cell_id", "whole_score"]).drop_duplicates("cell_id")
                v = d[["cell_id"]].merge(x, on="cell_id", how="left").whole_score.values.astype(float)
                pres.append(np.isfinite(v))
                dsv.append(v)
        if pres:
            inter = np.logical_and.reduce(pres)
            rows += contrast_rows(meta, "dsint_B_final", g75, y, sel=inter)
            for cn, (ga, gb_) in CONTRASTS.items():
                A, B = g75[ga] & inter, g75[gb_] & inter
                el = eligible(A.sum(), B.sum(), gb_)
                est = float(np.mean([mdiff(v, A, B) for v in dsv])) if el else np.nan
                rows.append({**meta, "variant": "dsint_C_ds", "contrast": cn, "nA": int(A.sum()), "nB": int(B.sum()),
                             "eligible": el, "est": est})
            # D1: dropped (absent from ds1) vs retained, per group
            drop = ~pres[0]
            for grp in ["pro", "rev", "ref"]:
                m = g75[grp]
                nd, nr = int((m & drop).sum()), int((m & ~drop).sum())
                r_ = {**meta, "group": grp, "n_group": int(m.sum()), "n_dropped": nd, "frac_dropped": nd / max(m.sum(), 1),
                      "frac_dropped_any_rep": float((m & ~inter).sum() / max(m.sum(), 1))}
                if nd >= 10 and nr >= 10:
                    for v in ["log_umi", "log_genes", "mito_frac", "whole_score", "proCSC", "revCSC"]:
                        x = d[v].values.astype(float)
                        r_[f"diff_{v}"] = float(np.nanmedian(x[m & drop]) - np.nanmedian(x[m & ~drop]))
                d1.append(r_)
        # CCAT M2 (lineage-adjusted partial), samples >= 100 cells
        if len(d) >= 100 and np.isfinite(d.CCAT).sum() >= 100:
            x = d[np.isfinite(d.CCAT) & d[COV].notna().all(axis=1)]
            lv = x.lineage.value_counts()
            D = np.column_stack([(x.lineage.values == l).astype(float) for l in lv.index[1:]]) if len(lv) > 1 \
                else np.empty((len(x), 0))
            for prog, other in [("proCSC", "revCSC"), ("revCSC", "proCSC")]:
                Cc = np.column_stack([x[other].values] + [x[c].values for c in COV])
                r_l, s_l = partial(x[prog].values, x.CCAT.values, Cc, D)
                m2c.append({**meta, "programme": prog, "partial_lineage": r_l, "status": s_l,
                            "unadjusted": stats.spearmanr(x[prog], x.CCAT).correlation})
        rows.append({**meta, "variant": "_sample_info", "contrast": "", "nA": len(d), "nB": 0, "eligible": False,
                     "est": float(np.median(d.revCSC))})
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / f"{study}.s4_contrasts.private.tsv.gz", sep="\t", index=False)
    pd.DataFrame(d1).to_csv(out / f"{study}.s4_d1.private.tsv", sep="\t", index=False)
    pd.DataFrame(trans).to_csv(out / f"{study}.s4_mbtrans.private.tsv", sep="\t", index=False)
    pd.DataFrame(m2c).to_csv(out / f"{study}.s4_m2ccat.private.tsv", sep="\t", index=False)
    print(study, flush=True)


# ---------------------------------------------------------------- pooling
def pooled_contrasts(df, col, label_extra, pooled, studies):
    for cn in CONTRASTS:
        e = df[(df.contrast == cn) & df.eligible]
        st, r = pool_values(patient_median(e, col), {**label_extra, "contrast": cn})
        pooled.append(r)
        if len(st):
            studies.append(st)


def loso_rows(pv, label):
    """pv: study_id, patient_id, v -> per-left-out-study pooled estimate with CI."""
    st = []
    for s, x in pv.groupby("study_id").v:
        if len(x) >= 5:
            st.append({"study_id": s, "mean": x.mean(), "se": x.std(ddof=1) / np.sqrt(len(x)), "n": len(x)})
    st = pd.DataFrame(st)
    out = []
    for s in st.study_id if len(st) > 3 else []:
        k = st[st.study_id != s]
        r = reml_hk(k["mean"], k.se)
        out.append({**label, "left_out": s, "k": r["k"], "n_patients": int(k.n.sum()), "estimate": r["estimate"],
                    "ci_low": r["ci_low"], "ci_high": r["ci_high"], "p": r["p"], "I2": r["I2"]})
    return out


def pool_phase(a):
    S, P = Path(a.out_dir), Path(a.public_out)
    P.mkdir(parents=True, exist_ok=True)
    s4 = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(S.glob("*.s4_contrasts.private.tsv.gz"))])
    info = s4[s4.variant == "_sample_info"]
    s4 = s4[s4.variant != "_sample_info"]
    s3 = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(Path(a.s3_dir).glob("*.s3_contrasts.private.tsv.gz"))])
    meta = pd.read_csv(a.patient_meta, sep="\t", usecols=["patient_id", "msi_status"])
    summ, pooled, studies = {}, [], []
    # ---- variants
    for v in ["base", "p70", "p80", "mechanism_blinded", "ref_strict", "ref_broad", "cnv_malignant", "ccat",
              "dsint_B_final", "dsint_C_ds"]:
        pooled_contrasts(s4[s4.variant == v], "est", {"analysis": v}, pooled, studies)
    # feasibility for every variant (eligible patients/studies)
    feas = []
    for (v, cn), x in s4.groupby(["variant", "contrast"]):
        e = x[x.eligible]
        ep = e.groupby("study_id").patient_id.nunique()
        feas.append({"variant": v, "contrast": cn, "eligible_samples": int(len(e)), "eligible_patients": e.patient_id.nunique(),
                     "patients_in_qualifying_studies": int(ep[ep >= 5].sum()), "qualifying_studies": int((ep >= 5).sum())})
    pd.DataFrame(feas).to_csv(P / "S4_feasibility.tsv", sep="\t", index=False)
    # ---- MSI/MSS (Stage 3 final, unadjusted)
    s3m = s3.merge(meta, on="patient_id", how="left")
    s3m["msi"] = s3m.msi_status.fillna("unknown").replace({"Unknown": "unknown"})
    for g in ["MSI-H", "MSS"]:
        pooled_contrasts(s3m[s3m.msi == g], "final", {"analysis": f"MSI={g}"}, pooled, studies)
    msi_overlap = []
    for cn in CONTRASTS:
        e = s3m[(s3m.contrast == cn) & s3m.eligible]
        t = e.groupby(["study_id", "msi"]).patient_id.nunique().unstack(fill_value=0)
        both = int(((t.get("MSI-H", 0) >= 5) & (t.get("MSS", 0) >= 5)).sum()) if len(t) else 0
        msi_overlap.append({"contrast": cn, "studies_with_ge5_in_both": both,
                            "interaction_tested": both >= 3})
    pd.DataFrame(msi_overlap).to_csv(P / "S4_msi_overlap.tsv", sep="\t", index=False)
    # ---- LOSO (Stage 3 final) incl. Pelka excluded
    loso = []
    for cn in CONTRASTS:
        e = s3[(s3.contrast == cn) & s3.eligible]
        loso += loso_rows(patient_median(e, "final"), {"contrast": cn})
    loso = pd.DataFrame(loso)
    loso.to_csv(P / "S4_loso.tsv", sep="\t", index=False)
    # ---- common-subset comparisons
    common = []
    for cn in CONTRASTS:
        e = s3[(s3.contrast == cn) & s3.eligible]
        c1 = e[np.isfinite(e.final) & np.isfinite(e.adj_full)]
        c2 = e[np.isfinite(e.adj_full) & np.isfinite(e.adj_reduced)]
        for lab, df, col in [("unadj_on_adjfull_set", c1, "final"), ("adjfull_on_adjfull_set", c1, "adj_full"),
                             ("adjfull_on_common_full_reduced", c2, "adj_full"),
                             ("adjreduced_on_common_full_reduced", c2, "adj_reduced")]:
            st, r = pool_values(patient_median(df, col), {"analysis": f"common:{lab}", "contrast": cn})
            pooled.append(r)
    for cn in ["pro_vs_ref", "rev_vs_ref"]:
        el = {v: set(s4[(s4.variant == v) & (s4.contrast == cn) & s4.eligible].patient_id)
              for v in ["base", "ref_strict", "ref_broad"]}
        cp = el["base"] & el["ref_strict"] & el["ref_broad"]
        common.append({"contrast": cn, **{f"n_{k}": len(v) for k, v in el.items()}, "n_common": len(cp)})
        for v in ["base", "ref_strict", "ref_broad"]:
            x = s4[(s4.variant == v) & (s4.contrast == cn) & s4.eligible & s4.patient_id.isin(cp)]
            st, r = pool_values(patient_median(x, "est"), {"analysis": f"refcommon:{v}", "contrast": cn})
            pooled.append(r)
    pd.DataFrame(common).to_csv(P / "S4_reference_common_subset.tsv", sep="\t", index=False)
    # ---- D2 A' : Stage 3 final on the D2 (intersection-eligible) patient population
    for cn in CONTRASTS:
        pop = set(s4[(s4.variant == "dsint_B_final") & (s4.contrast == cn) & s4.eligible].sample_id)
        e = s3[(s3.contrast == cn) & s3.eligible & s3.sample_id.isin(pop)]
        st, r = pool_values(patient_median(e, "final"), {"analysis": "dsint_Aprime_final_same_samples", "contrast": cn})
        pooled.append(r)
    pooled = pd.DataFrame(pooled)
    pooled.to_csv(P / "S4_pooled.tsv", sep="\t", index=False)
    pd.concat(studies, ignore_index=True).to_csv(P / "S4_by_study.tsv", sep="\t", index=False)
    # ---- D1 / D3
    d1 = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(S.glob("*.s4_d1.private.tsv")) if f.stat().st_size > 1])
    d1s = []
    for grp, x in d1.groupby("group"):
        r = {"group": grp, "samples": len(x), "median_frac_dropped": x.frac_dropped.median(),
             "median_frac_dropped_any_rep": x.frac_dropped_any_rep.median()}
        for v in ["log_umi", "log_genes", "mito_frac", "whole_score", "proCSC", "revCSC"]:
            c = f"diff_{v}"
            if c not in x:
                continue
            pv =x[np.isfinite(x[c])].groupby(["study_id", "patient_id"], as_index=False)[c].median().rename(columns={c: "v"})
            st, rr = pool_values(pv, {})
            r[f"{v}_dropped_minus_retained"] = rr.get("estimate", np.nan)
            r[f"{v}_ci"] = f"[{rr.get('ci_low', np.nan):.4f}, {rr.get('ci_high', np.nan):.4f}]"
            r[f"{v}_k"] = rr.get("k", 0)
        d1s.append(r)
    pd.DataFrame(d1s).to_csv(P / "S4_D1_dropout_audit.tsv", sep="\t", index=False)
    # D3 eligibility retention and loss by patient revCSC tertile
    prev = info.groupby("patient_id").est.median()
    terc = pd.qcut(prev, 3, labels=["low", "mid", "high"])
    d3 = []
    for cn in CONTRASTS:
        b = set(s4[(s4.variant == "base") & (s4.contrast == cn) & s4.eligible].patient_id)
        i = set(s4[(s4.variant == "dsint_B_final") & (s4.contrast == cn) & s4.eligible].patient_id)
        lost = b - i
        r = {"contrast": cn, "eligible_base": len(b), "eligible_intersection": len(i), "lost": len(lost)}
        for t in ["low", "mid", "high"]:
            bt = [p for p in b if terc.get(p) == t]
            r[f"lost_frac_rev_{t}"] = round(sum(p in lost for p in bt) / max(len(bt), 1), 3)
        d3.append(r)
    pd.DataFrame(d3).to_csv(P / "S4_D3_eligibility_retention.tsv", sep="\t", index=False)
    # ---- mb transitions
    tr = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(S.glob("*.s4_mbtrans.private.tsv")) if f.stat().st_size > 1])
    tm = tr.groupby(["full", "mb"]).n.sum().unstack(fill_value=0)
    tm.to_csv(P / "S4_mb_transition_matrix.tsv", sep="\t")
    jac = {}
    for s in ["pro_dominant", "rev_dominant", "hybrid_high", "neither_high", "reference"]:
        inter = tm.loc[s, s] if s in tm.index and s in tm.columns else 0
        jac[s] = float(inter / (tm.loc[s].sum() + tm[s].sum() - inter)) if s in tm.index else np.nan
    # ---- CCAT M2
    m2c = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(S.glob("*.s4_m2ccat.private.tsv")) if f.stat().st_size > 1])
    m2r = []
    for prog in ["proCSC", "revCSC"]:
        for est in ["unadjusted", "partial_lineage"]:
            x = m2c[(m2c.programme == prog) & np.isfinite(m2c[est])]
            if est == "partial_lineage":
                x = x[x.status == "ok"]
            pz = x.assign(v=np.arctanh(np.clip(x[est], -0.999999, 0.999999))) \
                .groupby(["study_id", "patient_id"], as_index=False).v.mean()
            st, r = pool_values(pz, {"programme": prog, "estimand": est, "proxy": "CCAT"}, back=np.tanh)
            m2r.append(r)
    pd.DataFrame(m2r).to_csv(P / "S4_M2_ccat.tsv", sep="\t", index=False)
    # ---- sample universe reconciliation
    ss = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(Path(a.stage1_dir).glob("*.sample_stats.tsv"))])
    miss = ss[~ss.sample_id.isin(set(s3.sample_id))][["study_id", "sample_id", "status", "n_cells"]]
    lab_samples = set(info.sample_id)
    miss = miss.assign(in_labels=miss.sample_id.isin(lab_samples))
    summ["sample_universe"] = {"stage1_samples": int(ss.sample_id.nunique()), "stage3_samples": int(s3.sample_id.nunique()),
                               "absent": int(len(miss)), "absent_status": miss.status.value_counts().to_dict(),
                               "absent_n_cells_max": float(miss.n_cells.max()) if len(miss) else 0,
                               "absent_n_cells_sum": float(miss.n_cells.fillna(0).sum())}
    miss.drop(columns=["sample_id"]).groupby(["study_id", "status"]).agg(
        n_samples=("in_labels", "size"), cells=("n_cells", "sum"), max_cells=("n_cells", "max")).reset_index() \
        .to_csv(P / "S4_sample_universe_absent_by_study.tsv", sep="\t", index=False)
    summ["mb_jaccard"] = jac
    keep = ["analysis", "contrast", "status", "k", "n_patients", "estimate", "ci_low", "ci_high", "pi_low", "pi_high",
            "p", "I2", "tau2", "studies_same_sign"]
    summ["pooled"] = pooled[[c for c in keep if c in pooled]].round(5).to_dict(orient="records")
    json.dump(summ, open(P / "stage4_summary.json", "w"), indent=1, default=str)
    pd.set_option("display.width", 250)
    print(pooled[[c for c in keep if c in pooled]].round(4).to_string())
    print(json.dumps({k: v for k, v in summ.items() if k != "pooled"}, indent=1, default=str))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["sample", "pool"])
    ap.add_argument("--task", type=int, default=0)
    ap.add_argument("--labels_dir", required=True)
    ap.add_argument("--cells_dir")
    ap.add_argument("--fig1b_root")
    ap.add_argument("--ccat_dir")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--public_out")
    ap.add_argument("--s3_dir")
    ap.add_argument("--stage1_dir")
    ap.add_argument("--patient_meta")
    a = ap.parse_args()
    sample_phase(a) if a.phase == "sample" else pool_phase(a)


if __name__ == "__main__":
    main()
