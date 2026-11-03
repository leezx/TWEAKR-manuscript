#!/usr/bin/env python3
"""Checkpoint 1A: TNFSF12 / TNFRSF12A expression feasibility in the Wang et al.
Nature 2026 maternal-fetal interface snRNA-seq atlas (DS-013).

Origin is author_cell_type_origin (Supplementary Table 13), not genotype.
Descriptive expression screen only: no DEG, pathway or spatial analysis.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy.stats import binomtest, wilcoxon

GENES = ("TNFSF12", "TNFRSF12A")
REQUIRED_OBS = ("sample_id", "gestational_week", "major_class", "minor_class", "celltype_shortname")
MIN_CELLS_DONOR = 20
TARGET_SUM = 1e4
CHUNK_ROWS = 20_000
CHUNK_NNZ = 50_000_000

CONTRAST_GROUPS = {
    "TNFSF12": {
        "maternal_macrophage (CD14_M+CD16_M)": ("celltype_shortname", ["CD14_M", "CD16_M"]),
        "fetal_macrophage (HB)": ("celltype_shortname", ["HB"]),
        "maternal_stroma (DSC+eS)": ("major_class", ["DSC"]),
        "dNK": ("celltype_shortname", ["dNK"]),
    },
    "TNFRSF12A": {
        "EVT (EVT+eEVT+iEVT+pEVT)": ("minor_class", ["EVT"]),
        "VCT (all VCT subtypes)": ("minor_class", ["VCT"]),
        "SCT (SCT+SCT_a+SCT_b)": ("minor_class", ["SCT"]),
        "maternal_stroma (DSC+eS)": ("major_class", ["DSC"]),
        "Epi": ("celltype_shortname", ["Epi"]),
    },
}


def trimester(gw: str) -> str:
    w = int(str(gw).upper().replace("GW", ""))
    return "T1 (GW5-13)" if w <= 13 else ("T2 (GW14-27)" if w <= 27 else "T3 (GW28-40)")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def read_obs(f: h5py.File) -> pd.DataFrame:
    g = f["obs"]
    index = g[g.attrs["_index"]][:].astype(str)
    cols = {}
    for c in REQUIRED_OBS:
        if c not in g:
            raise KeyError(f"Required obs field absent: {c}")
        node = g[c]
        if isinstance(node, h5py.Group):
            cats = node["categories"][:].astype(str)
            codes = node["codes"][:]
            if (codes < 0).any():
                raise ValueError(f"Missing values in obs/{c}")
            cols[c] = cats[codes]
        else:
            cols[c] = node[:].astype(str)
    obs = pd.DataFrame(cols, index=index)
    if not obs.index.is_unique:
        raise ValueError("Duplicate cell IDs in obs")
    return obs


def matrix_pass(f: h5py.File, gene_idx: dict[str, int]):
    """One pass over CSR X: library size per cell, target-gene counts, integrity checks."""
    X = f["X"]
    if X.attrs.get("encoding-type") != "csr_matrix":
        raise ValueError(f"Unexpected X encoding: {X.attrs.get('encoding-type')}")
    indptr = X["indptr"][:]
    n = len(indptr) - 1
    lib = np.zeros(n, dtype=np.float64)
    gcount = {g: np.zeros(n, dtype=np.float64) for g in gene_idx}
    max_dev, min_val, neg = 0.0, np.inf, 0
    for r0 in range(0, n, CHUNK_ROWS):
        r1 = min(r0 + CHUNK_ROWS, n)
        a, b = indptr[r0], indptr[r1]
        data = X["data"][a:b].astype(np.float64)
        idx = X["indices"][a:b]
        counts = np.expm1(data)
        max_dev = max(max_dev, float(np.abs(counts - np.rint(counts)).max()) if counts.size else 0.0)
        min_val = min(min_val, float(data.min()) if data.size else np.inf)
        neg += int((data < 0).sum())
        counts = np.rint(counts)
        rows = np.repeat(np.arange(r0, r1), np.diff(indptr[r0:r1 + 1]))
        lib[r0:r1] = np.bincount(rows - r0, weights=counts, minlength=r1 - r0)
        for g, j in gene_idx.items():
            m = idx == j
            gcount[g][rows[m]] = counts[m]
    qc = {
        "x_encoding": "csr_matrix", "n_cells": int(n), "nnz": int(indptr[-1]),
        "min_nonzero_value": min_val, "n_negative_values": neg,
        "max_abs_deviation_expm1_from_integer": max_dev,
        "interpretation": "X = log1p(raw integer UMI counts) without library-size normalisation"
        if (neg == 0 and max_dev < 1e-3 and abs(min_val - np.log(2)) < 1e-5) else "UNEXPECTED - inspect",
        "library_size_quantiles_0_1_50_99_100": np.percentile(lib, [0, 1, 50, 99, 100]).tolist(),
    }
    if qc["interpretation"].startswith("UNEXPECTED"):
        raise ValueError(f"Matrix QC failed: {qc}")
    return lib, gcount, qc


def summarise(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    if df[keys].isna().any().any():
        raise ValueError(f"Missing values in grouping keys {keys}")
    g = df.groupby(keys, observed=True, sort=False)
    out = g.agg(n_cells=("norm", "size"), n_donors=("sample_id", "nunique"), n_expr=("pos", "sum"),
                mean_log1p_cp10k=("norm", "mean"), mean_cp10k_per_nucleus=("cp10k", "mean"),
                sum_counts=("counts", "sum"), sum_library=("lib", "sum"),
                mean_counts=("counts", "mean")).reset_index()
    posmean = df[df.pos].groupby(keys, observed=True)["norm"].mean().rename("mean_log1p_cp10k_positive")
    out = out.merge(posmean.reset_index(), on=keys, how="left")
    out["mean_log1p_cp10k_positive"] = out["mean_log1p_cp10k_positive"].fillna(0.0)
    out["pct_expr"] = 100.0 * out.n_expr / out.n_cells
    out["pseudobulk_cp10k"] = TARGET_SUM * out.sum_counts / out.sum_library
    out = out.drop(columns="sum_library")
    return out


def donor_stats(donor_tab: pd.DataFrame, key: str) -> pd.DataFrame:
    ev = donor_tab[donor_tab.n_cells >= MIN_CELLS_DONOR]
    g = ev.groupby(key, observed=True)
    out = pd.DataFrame({
        "n_donors_evaluable": g.size(),
        "n_donors_detected": g.apply(lambda x: int((x.n_expr > 0).sum()), include_groups=False),
        "donor_median_pct_expr": g.pct_expr.median(),
        "donor_q25_pct_expr": g.pct_expr.quantile(0.25),
        "donor_q75_pct_expr": g.pct_expr.quantile(0.75),
        "donor_median_mean_log1p_cp10k": g.mean_log1p_cp10k.median(),
    }).reset_index()
    out["donor_detection_rate"] = out.n_donors_detected / out.n_donors_evaluable
    return out


def paired_contrasts(cells: pd.DataFrame, gene: str) -> list[dict]:
    rows = []
    for label, (field, members) in CONTRAST_GROUPS[gene].items():
        inside = cells[field].isin(members)
        recs = []
        for donor, d in cells.groupby("sample_id", observed=True):
            ins, out = d[inside.loc[d.index]], d[~inside.loc[d.index]]
            if len(ins) < MIN_CELLS_DONOR or len(out) < MIN_CELLS_DONOR:
                continue
            recs.append((donor, d.trimester.iloc[0], len(ins), ins.pos.mean() * 100, out.pos.mean() * 100,
                         ins.norm.mean(), out.norm.mean()))
        if not recs:
            continue
        r = pd.DataFrame(recs, columns=["donor", "trimester", "n_group", "pct_in", "pct_rest", "mean_in", "mean_rest"])
        dp, dm = r.pct_in - r.pct_rest, r.mean_in - r.mean_rest
        p_pct = wilcoxon(r.pct_in, r.pct_rest).pvalue if len(r) >= 6 and dp.abs().sum() > 0 else np.nan
        p_mean = wilcoxon(r.mean_in, r.mean_rest).pvalue if len(r) >= 6 and dm.abs().sum() > 0 else np.nan
        n_up, n_nonzero = int((dp > 0).sum()), int((dp != 0).sum())
        by_t = {tr: f"{int((dp[r.trimester == tr] > 0).sum())}/{int((r.trimester == tr).sum())}"
                for tr in sorted(r.trimester.unique())}
        rows.append({
            "gene": gene, "group": label,
            "comparison": "group vs all other nuclei of the same donor; donor = unit; trimester not adjusted",
            "n_donors": len(r), "min_group_nuclei_per_donor": int(r.n_group.min()),
            "n_donors_group_zero_detection": int((r.pct_in == 0).sum()),
            "n_donors_group_higher_pct": n_up,
            "group_higher_pct_by_trimester": "; ".join(f"{k}: {v}" for k, v in by_t.items()),
            "sign_test_p_pct_two_sided": binomtest(n_up, n_nonzero).pvalue if n_nonzero else np.nan,
            "median_pct_in": r.pct_in.median(), "median_pct_rest": r.pct_rest.median(),
            "median_delta_pct": dp.median(),
            "median_mean_log1p_cp10k_in": r.mean_in.median(), "median_mean_log1p_cp10k_rest": r.mean_rest.median(),
            "median_delta_mean_log1p_cp10k": dm.median(),
            "wilcoxon_p_pct_two_sided": p_pct, "wilcoxon_p_mean_two_sided": p_mean,
        })
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--h5ad", required=True, type=Path)
    p.add_argument("--origin-map", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    p.add_argument("--expected-sha256")
    a = p.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)

    digest = sha256(a.h5ad)
    if a.expected_sha256 and digest != a.expected_sha256:
        raise ValueError(f"SHA256 mismatch: {digest}")

    omap = pd.read_csv(a.origin_map, sep="\t", keep_default_na=False)
    with h5py.File(a.h5ad, "r") as f:
        obs = read_obs(f)
        var = f["var"][f["var"].attrs["_index"]][:].astype(str)
        gene_idx = {}
        for g in GENES:
            hits = np.where(var == g)[0]
            if len(hits) != 1:
                raise KeyError(f"{g}: {len(hits)} matches in var")
            gene_idx[g] = int(hits[0])
        lib, gcount, qc = matrix_pass(f, gene_idx)

    missing = set(obs.celltype_shortname) - set(omap.celltype_shortname)
    if missing:
        raise KeyError(f"Cell types absent from origin map: {sorted(missing)}")
    if (lib <= 0).any():
        raise ValueError("Cells with zero library size")
    ann = omap.set_index("celltype_shortname")[["author_cell_type_origin", "analysis_role", "mapping_basis"]]
    base = obs.join(ann, on="celltype_shortname")
    base["trimester"] = base.gestational_week.map(trimester)

    lib_lo, lib_hi = np.percentile(lib, [25, 75])
    in_window = (lib >= lib_lo) & (lib <= lib_hi)
    summaries, donor_rows, trim_rows, contrasts, overall, depth_rows = [], [], [], [], [], []
    for gene in GENES:
        c = gcount[gene]
        cells = base.copy()
        cells["counts"] = c
        cells["cp10k"] = c / lib * TARGET_SUM
        cells["norm"] = np.log1p(cells.cp10k)
        cells["pos"] = c > 0
        cells["lib"] = lib
        total = c.sum()
        overall.append({"gene": gene, "n_cells": len(c), "n_expr": int((c > 0).sum()),
                        "pct_expr": 100 * float((c > 0).mean()), "total_umis": float(total),
                        "mean_log1p_cp10k": float(cells.norm.mean()),
                        "pseudobulk_cp10k": float(TARGET_SUM * total / lib.sum())})

        keys = ["author_cell_type_origin", "major_class", "minor_class", "celltype_shortname", "analysis_role",
                "mapping_basis"]
        s = summarise(cells, keys)
        if len(s) != cells.celltype_shortname.nunique() or s.n_cells.sum() != len(cells):
            raise AssertionError("Cell-type summary does not cover every cell")
        s["share_of_gene_umis_pct"] = 100 * s.sum_counts / total
        rest = []
        for ct in s.celltype_shortname:
            o = cells[cells.celltype_shortname != ct]
            rest.append((100 * o.pos.mean(), o.cp10k.mean()))
        s["pct_expr_rest"] = [r[0] for r in rest]
        s["cp10k_fold_vs_rest"] = s.mean_cp10k_per_nucleus / np.array([r[1] for r in rest])
        dt = summarise(cells, ["sample_id", "gestational_week", "trimester", "author_cell_type_origin",
                               "major_class", "minor_class", "celltype_shortname"])
        dt["evaluable_min_cells"] = dt.n_cells >= MIN_CELLS_DONOR
        s = s.merge(donor_stats(dt, "celltype_shortname"), on="celltype_shortname", how="left")
        s["pct_expr_rank"] = s.pct_expr.rank(ascending=False, method="min").astype(int)
        s["mean_log1p_cp10k_rank"] = s.mean_log1p_cp10k.rank(ascending=False, method="min").astype(int)
        s.insert(0, "gene", gene)
        summaries.append(s)
        dt.insert(0, "gene", gene)
        donor_rows.append(dt)

        all_t = summarise(cells.assign(trimester="All"), ["trimester", "author_cell_type_origin", "celltype_shortname"])
        by_t = summarise(cells, ["trimester", "author_cell_type_origin", "celltype_shortname"])
        t = pd.concat([all_t, by_t], ignore_index=True)
        t.insert(0, "gene", gene)
        trim_rows.append(t)
        contrasts += paired_contrasts(cells, gene)

        dm = summarise(cells[in_window], ["author_cell_type_origin", "celltype_shortname"])
        dm = dm[["author_cell_type_origin", "celltype_shortname", "n_cells", "n_expr", "pct_expr",
                 "mean_log1p_cp10k"]].rename(columns=lambda x: x if x in ("author_cell_type_origin",
                                                                           "celltype_shortname") else f"{x}_depth_matched")
        dm = dm.merge(s[["celltype_shortname", "pct_expr", "pct_expr_rank"]], on="celltype_shortname")
        dm["pct_expr_rank_depth_matched"] = dm.pct_expr_depth_matched.rank(ascending=False, method="min").astype(int)
        dm.insert(0, "gene", gene)
        dm.insert(1, "library_size_window", f"{lib_lo:.0f}-{lib_hi:.0f} (atlas IQR)")
        depth_rows.append(dm)

    cols_drop = ["sum_counts"]
    pd.concat(summaries).drop(columns=cols_drop).to_csv(a.out_dir / "expression_summary_by_celltype.csv", index=False)
    pd.concat(donor_rows).drop(columns=cols_drop).to_csv(a.out_dir / "expression_by_donor_celltype.csv", index=False)
    pd.concat(trim_rows).drop(columns=cols_drop).to_csv(a.out_dir / "expression_by_trimester_celltype.csv", index=False)
    pd.concat(depth_rows).to_csv(a.out_dir / "qc_depth_matched_detection.csv", index=False)
    con = pd.DataFrame(contrasts)
    for col in ("wilcoxon_p_pct_two_sided", "wilcoxon_p_mean_two_sided"):
        pv = con[col].to_numpy()
        ok = ~np.isnan(pv)
        adj = np.full_like(pv, np.nan)
        order = np.argsort(pv[ok])
        ranked = pv[ok][order] * ok.sum() / (np.arange(ok.sum()) + 1)
        ranked = np.minimum.accumulate(ranked[::-1])[::-1].clip(max=1)
        tmp = np.empty_like(ranked); tmp[order] = ranked
        adj[ok] = tmp
        con[col.replace("wilcoxon_p", "bh_q")] = adj
    con.to_csv(a.out_dir / "donor_paired_contrasts.csv", index=False)

    libdf = base.assign(library_size=lib)
    lq = []
    for level in ("celltype_shortname", "sample_id", "trimester"):
        g = libdf.groupby(level, observed=True).library_size
        q = g.describe(percentiles=[0.25, 0.5, 0.75]).reset_index().rename(columns={level: "group"})
        q.insert(0, "level", level)
        lq.append(q)
    pd.concat(lq, ignore_index=True).to_csv(a.out_dir / "qc_library_size.csv", index=False)

    donors = base.groupby("trimester").sample_id.nunique().to_dict()
    (a.out_dir / "run_summary.json").write_text(json.dumps({
        "input": a.h5ad.name, "input_sha256": digest, "shape": [int(len(obs)), int(len(var))],
        "obs_fields_used": list(REQUIRED_OBS), "donor_field": "sample_id (one sample per donor; Supp Table 1c)",
        "target_gene_var_index": gene_idx, "matrix_qc": qc,
        "expression_definition": {
            "detection": "raw UMI count > 0 (pct_expr)",
            "mean_log1p_cp10k": "per-nucleus log1p(UMI / library size * 1e4), then arithmetic mean over nuclei",
            "mean_log1p_cp10k_positive": "same, restricted to nuclei with UMI > 0",
            "mean_cp10k_per_nucleus": "arithmetic mean of per-nucleus CP10k (linear scale)",
            "pseudobulk_cp10k": "sum of gene UMIs / sum of library sizes * 1e4 within the group",
            "library_size": "per-nucleus total UMI reconstructed as sum(round(expm1(X)))",
        },
        "contrast_definition": "within-donor group vs all other nuclei; donors need >=20 nuclei on each side; "
                               "two-sided Wilcoxon signed-rank on donor-level pct_expr and mean_log1p_cp10k; "
                               "BH across all contrasts of one metric (9); exact two-sided sign test on "
                               "direction; trimester not adjusted",
        "origin_definition": "author_cell_type_origin from Supplementary Table 13a/b; NOT per-cell genotype",
        "min_cells_per_donor_celltype": MIN_CELLS_DONOR, "donors_per_trimester": donors,
        "overall": overall,
        "scope_exclusions": ["DEG", "pathway", "spatial", "Stereo-seq", "genotype origin inference"],
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
