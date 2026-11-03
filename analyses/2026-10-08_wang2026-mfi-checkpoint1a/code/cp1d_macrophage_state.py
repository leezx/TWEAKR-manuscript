#!/usr/bin/env python3
"""Checkpoint 1D: TWEAK-associated macrophage state in Wang et al. Nature 2026 snRNA-seq (DS-013).

Level 1: immune landscape from author labels. Level 2: score candidate AOM/DSS-derived
Tnfsf12+ TAM modules in decidual macrophages and test association with independently
measured TNFSF12 detection. TNFSF12 is never part of any module. See docs/Checkpoint_1D_contract.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
from scipy import sparse
from scipy.stats import binomtest, spearmanr, wilcoxon
import statsmodels.api as sm
from statsmodels.stats.contingency_tables import StratifiedTable

SEED = 0
TARGET = "TNFSF12"
IMMUNE = ["CD14_M", "CD16_M", "HB", "dNK", "T", "B", "cDC"]
POPULATIONS = {
    "maternal_macrophage (CD14_M+CD16_M)": ["CD14_M", "CD16_M"],
    "sensitivity: CD14_M only": ["CD14_M"],
    "fetal_macrophage (HB)": ["HB"],
}
MODULES = {
    "CORE": ["GPNMB", "SPP1", "TREM2", "APOE", "FABP5", "PLD3"],
    "EXTENDED": ["GPNMB", "SPP1", "TREM2", "APOE", "FABP5", "PLD3", "CTSD", "CTSB", "CTSS", "ACP5",
                 "C1QA", "C1QB", "C1QC", "LGMN", "LIPA"],
    "LYSO_CONTROL": ["CTSD", "CTSB", "CTSS", "ACP5", "LGMN", "LIPA"],
    "COMPLEMENT_CONTROL": ["C1QA", "C1QB", "C1QC"],
    "MAC_IDENTITY": ["CD68", "CD163", "CSF1R", "CD14", "MRC1"],
    "MONO_LIKE": ["FCN1", "S100A8", "S100A9", "LYZ", "VCAN"],
}
TEST_MODULES = ("CORE", "EXTENDED")
MARKERS = {
    "Macrophage": ["CD68", "CD163", "C1QA", "C1QB", "CSF1R"],
    "Monocyte": ["FCN1", "S100A8", "S100A9", "LYZ"],
    "T cell": ["CD3D", "CD3E", "TRAC"],
    "NK cell": ["NKG7", "GNLY", "KLRD1"],
    "B cell": ["MS4A1", "CD79A"],
    "Dendritic cell": ["FCER1A", "CD1C", "CLEC9A"],
    "Mast cell": ["TPSAB1", "KIT"],
}
N_BINS, CTRL_SIZE, N_NULL, MIN_DONOR_CELLS = 25, 50, 500, 40


def load_immune(path: Path):
    a = ad.read_h5ad(path, backed="r")
    keep = a.obs.celltype_shortname.astype(str).isin(IMMUNE).to_numpy()
    sub = a[keep].to_memory()
    X = sub.X.tocsr().astype(np.float64)
    counts = X.copy()
    counts.data = np.rint(np.expm1(counts.data))
    lib = np.asarray(counts.sum(1)).ravel()
    norm = sparse.diags(1e4 / lib) @ counts
    norm.data = np.log1p(norm.data)
    sub.X = norm.tocsr().astype(np.float32)
    sub.obs["library_size"] = lib
    sub.obs["celltype"] = sub.obs.celltype_shortname.astype(str)
    gidx = int(np.where(sub.var_names == TARGET)[0][0])
    sub.obs["tnfsf12_umi"] = counts[:, gidx].toarray().ravel()
    return sub


class Scorer:
    """Re-implementation of scanpy score_genes (binned control genes) for fast repeated scoring."""

    def __init__(self, X_csc, var_names, rng):
        self.X = X_csc
        self.var = np.asarray(var_names)
        self.pos = {g: i for i, g in enumerate(self.var)}
        self.means = np.asarray(X_csc.mean(0)).ravel()
        ranks = pd.Series(self.means).rank(method="min")
        self.bins = np.asarray(pd.cut(ranks, N_BINS, labels=False))
        self.rng = rng

    def colmean(self, idx):
        return np.asarray(self.X[:, idx].mean(1)).ravel()

    def score(self, genes):
        gi = np.array([self.pos[g] for g in genes])
        ctrl = set()
        for b in np.unique(self.bins[gi]):
            pool = np.setdiff1d(np.where(self.bins == b)[0], gi)
            ctrl.update(self.rng.choice(pool, min(CTRL_SIZE, len(pool)), replace=False).tolist())
        return self.colmean(gi) - self.colmean(np.array(sorted(ctrl)))

    def matched_random(self, genes, exclude):
        excl = {self.pos[g] for g in exclude}
        out = []
        for g in genes:
            pool = [i for i in np.where(self.bins == self.bins[self.pos[g]])[0] if i not in excl]
            out.append(self.var[self.rng.choice(pool)])
        return out


def _fe_logit(y, covariates, groups):
    """Logistic regression with donor fixed effects on donors with >=1 TNFSF12+ cell
    (donors without positives are uninformative for within-donor association)."""
    informative = pd.Series(y).groupby(groups).transform("sum").to_numpy() > 0
    dummies = pd.get_dummies(groups[informative], drop_first=False).to_numpy(float)
    exog = np.column_stack([c[informative] for c in covariates] + [dummies])
    fit = sm.GLM(y[informative], exog, family=sm.families.Binomial()).fit()
    return fit, int(dummies.shape[1])


def clogit(y, score, loglib, groups):
    z = (score - score.mean()) / score.std()
    fit, ninf = _fe_logit(y, [z, loglib], groups)
    lo, hi = fit.conf_int()[0]
    return float(np.exp(fit.params[0])), float(np.exp(lo)), float(np.exp(hi)), float(fit.pvalues[0]), ninf


def clogit_joint(y, s1, s2, loglib, groups):
    zs = [(s - s.mean()) / s.std() for s in (s1, s2)]
    fit, _ = _fe_logit(y, zs + [loglib], groups)
    ci = fit.conf_int()
    return [(float(np.exp(fit.params[k])), float(np.exp(ci[k][0])), float(np.exp(ci[k][1])),
             float(fit.pvalues[k])) for k in (0, 1)]


def donor_split(df, score_col):
    rows, tables = [], []
    for donor, d in df.groupby("sample_id", observed=True):
        if len(d) < MIN_DONOR_CELLS:
            continue
        hi = d[score_col] > d[score_col].median()
        h, l = d[hi], d[~hi]
        rows.append({"donor": donor, "trimester": d.trimester.iloc[0], "n_high": len(h), "n_low": len(l),
                     "pos_high": int(h.pos.sum()), "pos_low": int(l.pos.sum()),
                     "pct_high": 100 * h.pos.mean(), "pct_low": 100 * l.pos.mean(),
                     "median_lib_high": h.library_size.median(), "median_lib_low": l.library_size.median()})
        tables.append(np.array([[h.pos.sum(), (~h.pos).sum()], [l.pos.sum(), (~l.pos).sum()]], float))
    r = pd.DataFrame(rows)
    informative = [t for t in tables if t[:, 0].sum() > 0]
    st = StratifiedTable([t + 0.0 for t in informative])
    mh, (mlo, mhi) = st.oddsratio_pooled, st.oddsratio_pooled_confint()
    inf = r[(r.pos_high + r.pos_low) > 0]
    d = inf.pct_high - inf.pct_low
    n_up, n_nz = int((d > 0).sum()), int((d != 0).sum())
    return r, {
        "n_donors": len(r), "n_donors_informative": len(inf), "n_donors_high_gt_low": n_up,
        "n_donors_low_gt_high": int((d < 0).sum()),
        "sign_test_p": binomtest(n_up, n_nz).pvalue if n_nz else np.nan,
        "wilcoxon_p": wilcoxon(inf.pct_high, inf.pct_low).pvalue if n_nz >= 6 else np.nan,
        "mh_or": mh, "mh_or_lo": mlo, "mh_or_hi": mhi, "mh_test_p": st.test_null_odds().pvalue,
        "median_lib_ratio_high_over_low": float((r.median_lib_high / r.median_lib_low).median()),
        "pct_high_pooled": 100 * sum(t[0, 0] for t in tables) / sum(t[0].sum() for t in tables),
        "pct_low_pooled": 100 * sum(t[1, 0] for t in tables) / sum(t[1].sum() for t in tables),
    }


def trimester(gw):
    w = int(str(gw).upper().replace("GW", ""))
    return "T1" if w <= 13 else ("T2" if w <= 27 else "T3")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--h5ad", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path, help="lightweight aggregate tables (repo)")
    p.add_argument("--cell-dir", required=True, type=Path, help="cell-level outputs (heavy workspace)")
    a = p.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    a.cell_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)

    imm = load_immune(a.h5ad)
    imm.obs["trimester"] = imm.obs.gestational_week.map(trimester)
    for genes in list(MODULES.values()) + list(MARKERS.values()):
        missing = [g for g in genes if g not in imm.var_names]
        if missing:
            raise KeyError(f"Genes absent: {missing}")

    # Level 1
    mk = [g for gs in MARKERS.values() for g in gs]
    Xm = imm[:, mk].X.toarray()
    rows = []
    for ct in IMMUNE:
        m = (imm.obs.celltype == ct).to_numpy()
        for j, g in enumerate(mk):
            v = Xm[m, j]
            rows.append({"celltype": ct, "marker_group": next(k for k, gs in MARKERS.items() if g in gs),
                         "gene": g, "n_cells": int(m.sum()), "pct_expr": 100 * float((v > 0).mean()),
                         "mean_log1p_cp10k": float(v.mean())})
    pd.DataFrame(rows).to_csv(a.out_dir / "cp1d_L1_immune_marker_dotplot.csv", index=False)
    comp = imm.obs.groupby(["sample_id", "gestational_week", "trimester", "celltype"], observed=True).size() \
        .rename("n_cells").reset_index()
    comp.to_csv(a.out_dir / "cp1d_L1_immune_composition_by_donor.csv", index=False)
    umap = pd.DataFrame(imm.obsm["X_umap"], columns=["umap1", "umap2"], index=imm.obs_names)
    umap.assign(celltype=imm.obs.celltype.values, sample_id=imm.obs.sample_id.values) \
        .to_csv(a.cell_dir / "cp1d_L1_immune_umap_cells.csv.gz")

    # Level 2
    summary, donor_tabs, null_rows, joint_rows, overlap_rows, scores_out = [], [], [], [], [], []
    scanpy_check = {}
    for pop, labels in POPULATIONS.items():
        sub = imm[imm.obs.celltype.isin(labels).to_numpy()].copy()
        scorer = Scorer(sub.X.tocsc(), sub.var_names, np.random.default_rng(SEED))
        df = sub.obs[["sample_id", "trimester", "celltype", "library_size"]].copy()
        df["pos"] = sub.obs.tnfsf12_umi.to_numpy() > 0
        for m, genes in MODULES.items():
            df[m] = scorer.score(genes)
        if pop.startswith("maternal"):
            sc.tl.score_genes(sub, MODULES["CORE"], ctrl_size=CTRL_SIZE, n_bins=N_BINS, random_state=SEED,
                              score_name="scanpy_core")
            scanpy_check = {"spearman_core_vs_scanpy": float(spearmanr(df.CORE, sub.obs.scanpy_core)[0])}
            scores_out.append(df.assign(umap1=sub.obsm["X_umap"][:, 0], umap2=sub.obsm["X_umap"][:, 1]))

        y = df.pos.to_numpy().astype(int)
        groups = df.sample_id.astype(str).to_numpy()
        loglib = np.log10(df.library_size.to_numpy())
        for m in MODULES:
            r, s = donor_split(df, m)
            or_, lo, hi, pv, ninf = clogit(y, df[m].to_numpy(), loglib, groups)
            summary.append({"population": pop, "module": m, "n_cells": len(df), "n_tnfsf12_pos": int(y.sum()),
                            "pct_tnfsf12": 100 * y.mean(), **s, "clogit_or_per_sd": or_, "clogit_lo": lo,
                            "clogit_hi": hi, "clogit_p": pv, "clogit_n_informative_donors": ninf})
            r.insert(0, "module", m)
            r.insert(0, "population", pop)
            donor_tabs.append(r)
        for m, adj in [(m, c) for m in TEST_MODULES for c in ("LYSO_CONTROL", "COMPLEMENT_CONTROL")]:
            (c_or, c_lo, c_hi, c_p), (l_or, l_lo, l_hi, l_p) = clogit_joint(
                y, df[m].to_numpy(), df[adj].to_numpy(), loglib, groups)
            joint_rows.append({"population": pop, "module": m, "adjusted_for": adj,
                               "analysis": "pre-specified" if adj == "LYSO_CONTROL" else "post hoc",
                               "module_or_per_sd": c_or, "module_lo": c_lo, "module_hi": c_hi, "module_p": c_p,
                               "adj_or_per_sd": l_or, "adj_lo": l_lo, "adj_hi": l_hi, "adj_p": l_p})
        cors = df[list(MODULES)].corr(method="spearman")
        for i, m1 in enumerate(MODULES):
            for m2 in list(MODULES)[i + 1:]:
                q1 = df.groupby("sample_id", observed=True)[m1].transform(lambda s: s >= s.quantile(0.75))
                q2 = df.groupby("sample_id", observed=True)[m2].transform(lambda s: s >= s.quantile(0.75))
                overlap_rows.append({"population": pop, "module_a": m1, "module_b": m2,
                                     "spearman_rho": float(cors.loc[m1, m2]),
                                     "jaccard_top_quartile_within_donor": float((q1 & q2).sum() / (q1 | q2).sum())})
        if not pop.startswith("fetal"):
            for m in TEST_MODULES:
                obs_or = next(x["clogit_or_per_sd"] for x in summary if x["population"] == pop and x["module"] == m)
                nulls = []
                excl = set(MODULES[m]) | {TARGET}
                for _ in range(N_NULL):
                    genes = scorer.matched_random(MODULES[m], excl)
                    nulls.append(clogit(y, scorer.score(genes), loglib, groups)[0])
                nulls = np.array(nulls)
                null_rows.append({"population": pop, "module": m, "observed_or_per_sd": obs_or,
                                  "null_n": N_NULL, "null_median_or": float(np.median(nulls)),
                                  "null_q95_or": float(np.quantile(nulls, 0.95)),
                                  "empirical_p_one_sided": float((1 + (nulls >= obs_or).sum()) / (N_NULL + 1))})
                pd.DataFrame({"null_or_per_sd": nulls}).to_csv(
                    a.out_dir / f"cp1d_L2_null_{m}_{'cd14' if 'CD14_M only' in pop else 'mac'}.csv", index=False)

    pd.DataFrame(summary).to_csv(a.out_dir / "cp1d_L2_tnfsf12_association.csv", index=False)
    pd.concat(donor_tabs).to_csv(a.out_dir / "cp1d_L2_donor_split.csv", index=False)
    pd.DataFrame(null_rows).to_csv(a.out_dir / "cp1d_L2_matched_random_null.csv", index=False)
    pd.DataFrame(joint_rows).to_csv(a.out_dir / "cp1d_L2_adjusted_models.csv", index=False)
    pd.DataFrame(overlap_rows).to_csv(a.out_dir / "cp1d_L2_module_overlap.csv", index=False)
    scores_out[0].to_csv(a.cell_dir / "cp1d_L2_macrophage_scores_cells.csv.gz")
    (a.out_dir / "cp1d_run_summary.json").write_text(json.dumps({
        "input": a.h5ad.name, "seed": SEED, "immune_labels": IMMUNE, "populations": POPULATIONS,
        "modules": MODULES, "n_bins": N_BINS, "ctrl_size": CTRL_SIZE, "n_null": N_NULL,
        "min_donor_cells": MIN_DONOR_CELLS, "scanpy_equivalence": scanpy_check,
        "n_immune_cells": int(imm.n_obs),
        "umap": "author integrated X_umap (subset); not recomputed",
        "cell_level_outputs": str(a.cell_dir),
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
