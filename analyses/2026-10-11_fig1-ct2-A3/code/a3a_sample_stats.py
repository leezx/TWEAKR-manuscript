#!/usr/bin/env python3
"""A3a step 3: per-sample correlations (frozen contract A3a v0.2 §1, §3, §4, §6).

For every cohort-v1 sample with >=50 L1 epithelial cells (eligibility for 100 is flagged), per cell set
(primary / F1clean / malignant / noncycling) and programme (8 UCell sets, plus TNFRSF12A log1p CPM for P2):
  proxies     ct2_final (whole_score), ct2_raw (intrinsic_score),
              ds_both (ds UCell vs ds whole_score; mean Fisher z over seeds 1-5),
              ds_ct2_fixed_programme (ds whole_score vs main UCell on the retained cells)
  estimands   unadjusted Spearman; partial Spearman = Pearson of OLS residuals of ranks on covariate ranks
              (log UMI, log detected genes, mito fraction, S score, G2M score; constant covariates dropped)
A sample x programme x proxy whose programme or proxy IQR is 0 is non-estimable (NaN).
Also writes P2 descriptive correlations (TNFRSF12A vs each programme), TNFRSF12A detection,
the proCSC-revCSC co-activation readout and P3 sample-level inputs.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SETS = ["proCSC", "revCSC", "Lgr5CSC", "ExtCIOC", "YAPcore", "ECOS38", "YAPfetal", "Placenta"]
COV = ["log_umi", "log_genes", "mito_frac", "S_score", "G2M_score"]


def iqr0(v):
    q = np.nanpercentile(v, [25, 75])
    return q[1] - q[0] <= 0


def resid(r, C):
    if C.shape[1] == 0:
        return r - r.mean()
    X = np.column_stack([np.ones(len(r)), C])
    beta, *_ = np.linalg.lstsq(X, r, rcond=None)
    return r - X @ beta


def corr_pair(x, y, cov):
    """Return (unadjusted Spearman, partial Spearman) or NaN when non-estimable."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(cov), axis=1)
    x, y, cov = x[ok], y[ok], cov[ok]
    if len(x) < 10 or iqr0(x) or iqr0(y):
        return np.nan, np.nan
    rx, ry = stats.rankdata(x), stats.rankdata(y)
    un = np.corrcoef(rx, ry)[0, 1]
    keep = [j for j in range(cov.shape[1]) if np.ptp(cov[:, j]) > 0]
    C = np.column_stack([stats.rankdata(cov[:, j]) for j in keep]) if keep else np.empty((len(x), 0))
    ex, ey = resid(rx, C), resid(ry, C)
    pa = np.corrcoef(ex, ey)[0, 1] if ex.std() > 0 and ey.std() > 0 else np.nan
    return un, pa


def prep(d):
    d = d.copy()
    d["log_umi"] = np.log10(d.umi.clip(lower=1))
    d["log_genes"] = np.log10(d.genes.clip(lower=1))
    d["TNFRSF12A_cpm"] = np.log1p(d.TNFRSF12A_umi / d.umi.clip(lower=1) * 1e6)
    return d


def cellsets(d):
    return {"primary": np.ones(len(d), bool), "F1clean": ~d.F1.astype(str).eq("True").to_numpy(),
            "malignant": d.celltype_L2.eq("Malignant epithelial").to_numpy(),
            "noncycling": d.phase.eq("G1").to_numpy()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a3-root", required=True)
    ap.add_argument("--fig1b-root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    A, F, O = Path(a.a3_root), Path(a.fig1b_root), Path(a.out)
    O.mkdir(parents=True, exist_ok=True)
    cells = pd.concat([pd.read_csv(p, sep="\t") for p in sorted((A / "export/cells").glob("*.cells.tsv.gz"))])
    rows, coact, detect = [], [], []
    for sample, g in cells.groupby("sample_id"):
        tag = "".join(c if (c.isalnum() or c in "_.-") else "_" for c in sample)
        uc = pd.read_csv(A / "ucell" / f"{tag}.ucell.tsv.gz", sep="\t")
        uc.columns = [c.rstrip("_") if c.endswith("_") else c for c in uc.columns]
        main = prep(g[g.variant == "main"]).merge(uc[uc.variant == "main"].drop(columns="variant"), on="cell_id")
        ct = pd.read_csv(F / "full/scores" / f"{tag}.model.scores.tsv.gz", sep="\t")
        main = main.merge(ct[["cell_id", "whole_score", "intrinsic_score"]], on="cell_id", how="inner")
        n_all = len(main)
        if n_all < 50:
            continue
        meta = dict(study_id=main.study_id.iloc[0], patient_id=main.patient_id.iloc[0], sample_id=sample)
        detect.append({**meta, "epi_cells": n_all, "TNFRSF12A_detected_frac": float((main.TNFRSF12A_umi > 0).mean())})
        progs = SETS + ["TNFRSF12A_cpm"]
        for cs, m in cellsets(main).items():
            d = main[m]
            if len(d) < 50:
                continue
            cov = d[COV].to_numpy(float)
            for p in progs:
                for proxy, col in [("ct2_final", "whole_score"), ("ct2_raw", "intrinsic_score")]:
                    un, pa = corr_pair(d[p], d[col], cov)
                    rows.append({**meta, "cellset": cs, "n_cells": len(d), "programme": p, "proxy": proxy,
                                 "unadjusted": un, "adjusted": pa})
            if cs == "primary":
                for p in SETS:  # P2 descriptive: TNFRSF12A vs each programme
                    un, pa = corr_pair(d["TNFRSF12A_cpm"], d[p], cov)
                    rows.append({**meta, "cellset": cs, "n_cells": len(d), "programme": "TNFRSF12A_cpm",
                                 "proxy": f"prog:{p}", "unadjusted": un, "adjusted": pa})
                # co-activation (descriptive, ED)
                tp, tr = np.percentile(d.proCSC, 75), np.percentile(d.revCSC, 75)
                hp, hr = d.proCSC >= tp, d.revCSC >= tr
                grp = np.select([hp & hr, hp & ~hr, ~hp & hr], ["co_high", "pro_only", "rev_only"], "neither")
                r = {**meta, "n_cells": len(d), "share_co_high": float((hp & hr).mean()),
                     "share_pro_high": float(hp.mean()), "share_rev_high": float(hr.mean())}
                for k in ["co_high", "pro_only", "rev_only", "neither"]:
                    r[f"n_{k}"] = int((grp == k).sum())
                    r[f"ct2_median_{k}"] = float(d.whole_score[grp == k].median()) if (grp == k).any() else np.nan
                coact.append(r)
        # depth perturbation (primary cell set only)
        zs = {}
        for seed in range(1, 6):
            ds = g[g.variant == f"ds{seed}"]
            if ds.empty:
                continue
            ds = prep(ds).merge(uc[uc.variant == f"ds{seed}"].drop(columns="variant"), on="cell_id")
            cds = pd.read_csv(F / "full/scores_ds" / f"{tag}.ds{seed}.scores.tsv.gz", sep="\t")
            ds = ds.merge(cds[["cell_id", "whole_score"]], on="cell_id", how="inner")
            fixed = ds[["cell_id", "whole_score"] + COV].merge(main[["cell_id"] + SETS], on="cell_id")
            if len(ds) < 50:
                continue
            for p in SETS:
                un, pa = corr_pair(ds[p], ds.whole_score, ds[COV].to_numpy(float))
                zs.setdefault(("ds_both", p), []).append((un, pa, len(ds)))
                un, pa = corr_pair(fixed[p], fixed.whole_score, fixed[COV].to_numpy(float))
                zs.setdefault(("ds_ct2_fixed_programme", p), []).append((un, pa, len(fixed)))
        for (proxy, p), v in zs.items():
            v = np.array(v, float)
            zun = np.nanmean(np.arctanh(np.clip(v[:, 0], -0.999999, 0.999999))) if np.isfinite(v[:, 0]).any() else np.nan
            zpa = np.nanmean(np.arctanh(np.clip(v[:, 1], -0.999999, 0.999999))) if np.isfinite(v[:, 1]).any() else np.nan
            rows.append({**meta, "cellset": "primary", "n_cells": int(np.median(v[:, 2])), "programme": p,
                         "proxy": proxy, "unadjusted": float(np.tanh(zun)), "adjusted": float(np.tanh(zpa)),
                         "n_seeds": len(v)})
        print(sample, n_all, flush=True)
    pd.DataFrame(rows).to_csv(O / "sample_correlations.private.tsv.gz", sep="\t", index=False)
    pd.DataFrame(coact).to_csv(O / "coactivation_samples.private.tsv", sep="\t", index=False)
    pd.DataFrame(detect).to_csv(O / "TNFRSF12A_detection_samples.private.tsv", sep="\t", index=False)
    # P3 inputs: macrophage pseudobulk + epithelial ExtCIOC sample median (primary set, main)
    mac = pd.concat([pd.read_csv(p, sep="\t") for p in sorted((A / "export/cells").glob("*.macrophage.tsv"))])
    med = []
    for sample, g in cells[cells.variant == "main"].groupby("sample_id"):
        tag = "".join(c if (c.isalnum() or c in "_.-") else "_" for c in sample)
        uc = pd.read_csv(A / "ucell" / f"{tag}.ucell.tsv.gz", sep="\t")
        uc.columns = [c.rstrip("_") if c.endswith("_") else c for c in uc.columns]
        uc = uc[uc.variant == "main"]
        ct = pd.read_csv(F / "full/scores" / f"{tag}.model.scores.tsv.gz", sep="\t")
        x = uc.merge(ct[["cell_id", "whole_score"]], on="cell_id")
        med.append({"sample_id": sample, "epi_cells": len(x), "ExtCIOC_median": x.ExtCIOC.median(),
                    "ct2_median": x.whole_score.median(), "proCSC_median": x.proCSC.median(),
                    "revCSC_median": x.revCSC.median(), "epi_median_log_umi": np.log10(g.umi.clip(lower=1)).median()})
    mac.merge(pd.DataFrame(med), on="sample_id", how="left").to_csv(O / "P3_samples.private.tsv", sep="\t", index=False)
    (O / "SAMPLE_STATS_DONE").write_text("ok\n")


if __name__ == "__main__":
    main()
