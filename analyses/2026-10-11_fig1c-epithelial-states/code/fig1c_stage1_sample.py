#!/usr/bin/env python3
"""Fig. 1c Stage 1 phase 1 (one SGE task per study; contract v0.3 §3.2-§4): per-sample programme and
group statistics plus frozen cell-level labels. CT2-blinded: reads only A3a cell covariates, Fig. 1c UCell
scores and Axis L predictions.

Within each sample: Spearman of full vs split / leave-one-gene-out scores (G2), external concordance (G3),
pro-rev correlation and rank-residual partial correlations (G4; A3a corr_pair), technical dependence (G7),
operational strata at the 70/75/80th percentile and group sizes (G5/G6).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, "/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011/code")
from a3a_sample_stats import corr_pair  # noqa: E402

REF = "Absorptive differentiated-like"
STEM = ["Stem/TA-like", "Cycling Stem/TA"]
PCTS = [70, 75, 80]


def spear(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 10 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return np.nan
    return stats.spearmanr(x, y).correlation


def strata(pro, rev, pct):
    ph = pro >= np.percentile(pro, pct)
    rh = rev >= np.percentile(rev, pct)
    s = np.select([ph & ~rh, rh & ~ph, ph & rh], ["pro_dominant", "rev_dominant", "hybrid_high"], "neither_high")
    return ph, rh, s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", type=int, required=True)
    ap.add_argument("--cells_dir", required=True)
    ap.add_argument("--ucell_dir", required=True)
    ap.add_argument("--axisl_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--rule", default="v03", choices=["v03", "v03a"],
                    help="v03: frozen rule (max-p, margin, OOD); v03a: amendment B (max-p, margin only)")
    ap.add_argument("--verdict", default=None, help="v0.3a lineage audit verdict table (study_id, class, verdict)")
    a = ap.parse_args()
    files = sorted(Path(a.cells_dir).glob("*.cells.tsv.gz"))
    if a.task > len(files):
        return
    cf = files[a.task - 1]
    study = cf.name[:-len(".cells.tsv.gz")]
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cells = pd.read_csv(cf, sep="\t")
    cells = cells[cells.variant == "main"]
    unver = set()
    if a.verdict:
        vt = pd.read_csv(a.verdict, sep="\t")
        unver = {c for st_, c, v in vt[["study_id", "class", "verdict"]].itertuples(index=False)
                 if st_ == study and v == "lineage_transfer_unverified"}
    srows, lrows, labs = [], [], []
    for tag, cd in cells.groupby("sample_id"):
        uf = Path(a.ucell_dir) / f"{tag}.ucell.tsv.gz"
        lf = Path(a.axisl_dir) / f"{tag}.axisL.tsv.gz"
        if not uf.exists() or not lf.exists():
            srows.append({"study_id": study, "sample_id": tag, "status": "missing_input"})
            continue
        u = pd.read_csv(uf, sep="\t")
        u = u[u.variant == "main"].drop(columns="variant")
        lp = pd.read_csv(lf, sep="\t", usecols=["cell_id", "lineage", "pred_agg", "ood_pct", "assigned",
                                                "maxp_agg", "margin_agg"])
        lp["ood_pass"] = lp.ood_pct <= 99.0
        if a.rule == "v03a":  # amendment B: OOD no longer a rejection criterion; thresholds unchanged
            ok_ = (lp.maxp_agg >= 0.70) & (lp.margin_agg >= 0.20)
            lp["lineage"] = np.where(ok_, lp.pred_agg, "lineage-unresolved")
            # audit: a study x class without marker support leaves all lineage-specific groups
            lp["lineage"] = np.where(lp.lineage.isin(unver), "lineage-transfer-unverified", lp.lineage)
        d = cd.merge(u, on="cell_id", how="inner").merge(lp, on="cell_id", how="inner")
        n = len(d)
        row = {"study_id": study, "patient_id": d.patient_id.iloc[0] if n else None, "sample_id": tag,
               "status": "ok", "n_cells": n, "n_ucell_sets": u.shape[1] - 1,
               "median_umi": float(d.umi.median()) if n else np.nan}
        if n == 0:
            srows.append(row)
            continue
        d["log_umi"] = np.log10(d.umi.clip(lower=1))
        d["log_genes"] = np.log10(d.genes.clip(lower=1))
        pro, rev = d.proCSC.values, d.revCSC.values
        for c, v in d.lineage.value_counts().items():
            row[f"lin_n|{c}"] = int(v)
        # G2: full vs split (median over 200 splits) and leave-one-gene-out
        for s in ["proCSC", "revCSC"]:
            sp = [c for c in d.columns if c.startswith(f"{s}_split")]
            row[f"G2_split_rho|{s}"] = float(np.nanmedian([spear(d[s], d[c]) for c in sp])) if n >= 10 else np.nan
            row[f"G2_n_splits|{s}"] = len(sp)
            for c in [c for c in d.columns if c.startswith(f"{s}_minus_")]:
                lrows.append({"study_id": study, "patient_id": row["patient_id"], "sample_id": tag, "set": s,
                              "gene": c[len(f"{s}_minus_"):], "rho": spear(d[s], d[c]), "n_cells": n})
        # G3 and other set agreements
        for k, (x, y) in {"rev_hOnF_no": ("revCSC", "hOnF_no"), "rev_hOnF": ("revCSC", "hOnF"),
                          "pro_hStem_no": ("proCSC", "hStem_no"), "pro_hStem": ("proCSC", "hStem"),
                          "pro_mb": ("proCSC", "proCSC_mb"), "rev_mb": ("revCSC", "revCSC_mb"),
                          "pro_noCC": ("proCSC", "proCSC_noCC"), "pro_rev": ("proCSC", "revCSC"),
                          "pro_noCC_rev": ("proCSC_noCC", "revCSC")}.items():
            row[f"rho|{k}"] = spear(d[x], d[y])
        cc = d[["S_score", "G2M_score"]].values
        row["G4_partial|rev_hOnF_no"] = corr_pair(d.revCSC, d.hOnF_no, np.column_stack([pro, cc]))[1]
        row["G4_partial|pro_hStem_no"] = corr_pair(d.proCSC, d.hStem_no, np.column_stack([rev, cc]))[1]
        # strata and groups
        for pct in PCTS:
            ph, rh, s = strata(pro, rev, pct)
            is_ref = d.lineage.values == REF
            st = np.where(is_ref, "reference", s)
            row[f"high_frac_pro|p{pct}"], row[f"high_frac_rev|p{pct}"] = ph.mean(), rh.mean()
            row[f"hybrid_obs|p{pct}"], row[f"hybrid_exp|p{pct}"] = (ph & rh).mean(), ph.mean() * rh.mean()
            row[f"n_ref|p{pct}"] = int(is_ref.sum())
            row[f"n_ref_neither|p{pct}"] = int((is_ref & (s == "neither_high")).sum())
            row[f"n_discordant|p{pct}"] = int((is_ref & (ph | rh)).sum())
            row[f"n_ref_plus_secretory|p{pct}"] = int(np.isin(d.lineage, [REF, "Secretory differentiated-like"]).sum())
            for g in ["pro_dominant", "rev_dominant", "hybrid_high", "neither_high"]:
                m = st == g
                row[f"n_{g}|p{pct}"] = int(m.sum())
                row[f"n_{g}_stemlineage|p{pct}"] = int((m & np.isin(d.lineage, STEM)).sum())
                if pct == 75:
                    for c, v in d.lineage[m].value_counts().items():
                        row[f"stratum_lin|{g}|{c}"] = int(v)
            if pct == 75:
                d["stratum75"], d["pro_high75"], d["rev_high75"] = st, ph, rh
                d["discordant75"] = is_ref & (ph | rh)
            d[f"stratum{pct}"] = st
        # G7 technical dependence
        for v in ["proCSC", "revCSC"]:
            for t in ["log_umi", "log_genes", "mito_frac", "S_score", "G2M_score"]:
                row[f"G7|{v}|{t}"] = spear(d[v], d[t])
        for g in ["pro_dominant", "rev_dominant"]:
            ind = (d.stratum75 == g).astype(float)
            for t in ["log_umi", "log_genes", "mito_frac", "S_score", "G2M_score"]:
                row[f"G7|{g}|{t}"] = spear(ind, d[t])
        srows.append(row)
        labs.append(d[["cell_id", "study_id", "patient_id", "sample_id", "lineage", "pred_agg", "ood_pct", "ood_pass",
                       "proCSC", "revCSC", "proCSC_mb", "revCSC_mb", "proCSC_noCC", "hOnF_no", "hStem_no",
                       "pro_high75", "rev_high75", "stratum70", "stratum75", "stratum80", "discordant75"]])
    pd.DataFrame(srows).to_csv(out / f"{study}.sample_stats.tsv", sep="\t", index=False)
    pd.DataFrame(lrows).to_csv(out / f"{study}.logo.tsv.gz", sep="\t", index=False)
    if labs:
        pd.concat(labs).to_csv(out / f"{study}.cell_labels.tsv.gz", sep="\t", index=False)
    print(study, len(srows), sum(r.get("status") == "ok" for r in srows))


if __name__ == "__main__":
    main()
