#!/usr/bin/env python3
"""A3a CCAT secondary family (frozen contract v0.2 §3-§4): programme x CCAT, same estimands and aggregation
as the CT2 family. Family: 5 P1 sets x CCAT x unadjusted, BH. Adjusted and secondary sets are descriptive.
Also reports CT2-vs-CCAT agreement per programme for the §5 discordance rule.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a3a_sample_stats import COV, SETS, cellsets, corr_pair, prep  # noqa: E402
from a3a_pool import ALL, P1, bh, patient_z, pool  # noqa: E402


def safe(s):
    return "".join(c if (c.isalnum() or c in "_.-") else "_" for c in s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a3-root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    A, O = Path(a.a3_root), Path(a.out)
    O.mkdir(parents=True, exist_ok=True)
    cells = pd.concat([pd.read_csv(p, sep="\t") for p in sorted((A / "export/cells").glob("*.cells.tsv.gz"))])
    cells = cells[cells.variant == "main"]
    rows = []
    for sample, g in cells.groupby("sample_id"):
        tag = safe(sample)
        cc = pd.read_csv(A / "ccat" / f"{tag}.ccat.tsv.gz", sep="\t")
        if cc.empty:
            continue
        uc = pd.read_csv(A / "ucell" / f"{tag}.ucell.tsv.gz", sep="\t")
        uc = uc[uc.variant == "main"].drop(columns="variant")
        d = prep(g).merge(uc, on="cell_id").merge(cc, on="cell_id")
        if len(d) < 50:
            continue
        meta = dict(study_id=d.study_id.iloc[0], patient_id=d.patient_id.iloc[0], sample_id=sample)
        for cs, m in cellsets(d).items():
            x = d[m]
            if len(x) < 50:
                continue
            cov = x[COV].to_numpy(float)
            for p in SETS + ["TNFRSF12A_cpm"]:
                un, pa = corr_pair(x[p], x.CCAT, cov)
                rows.append({**meta, "cellset": cs, "n_cells": len(x), "programme": p, "proxy": "ccat",
                             "unadjusted": un, "adjusted": pa})
    sc = pd.DataFrame(rows)
    sc.to_csv(A / "stats" / "sample_correlations_ccat.private.tsv.gz", sep="\t", index=False)
    pooled, studies = [], []
    for cs in ["primary", "F1clean", "malignant", "noncycling"]:
        for est in ["unadjusted", "adjusted"]:
            for p in ALL + ["TNFRSF12A_cpm"]:
                d = sc[(sc.cellset == cs) & (sc.n_cells >= 100) & (sc.programme == p)]
                st, r = pool(patient_z(d, est), dict(analysis=f"ccat|{est}|ge100|{cs}", cellset=cs, programme=p,
                                                     proxy="ccat", estimand=est, threshold=100))
                pooled.append(r); studies.append(st)
    pooled = pd.DataFrame(pooled)
    for c in ["p", "rho"]:
        if c not in pooled:
            pooled[c] = np.nan
    fam = (pooled.analysis == "ccat|unadjusted|ge100|primary") & pooled.programme.isin(P1) & (pooled.status == "pooled")
    pooled["family"] = np.where(fam, "secondary_ccat", "descriptive")
    pooled["p_bh"] = np.nan
    if fam.any():
        pooled.loc[fam, "p_bh"] = bh(pooled.loc[fam, "p"])
    pooled.to_csv(O / "A3a_ccat_pooled.tsv", sep="\t", index=False)
    pd.concat([s for s in studies if len(s)], ignore_index=True).to_csv(O / "A3a_ccat_study.tsv", sep="\t", index=False)
    print(pooled[pooled.analysis.str.contains("primary")][["analysis", "programme", "k", "n_patients", "rho",
                                                            "ci_low", "ci_high", "p_bh"]].to_string())


if __name__ == "__main__":
    main()
