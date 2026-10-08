#!/usr/bin/env python3
"""CP1D figures (Python / matplotlib only). Reads tables/cp1d aggregates and cell-level
UMAP/score files from the heavy workspace."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 6, "svg.fonttype": "none", "pdf.fonttype": 42,
    "axes.spines.right": False, "axes.spines.top": False, "axes.linewidth": 0.7,
    "xtick.major.width": 0.7, "ytick.major.width": 0.7, "xtick.major.size": 2, "ytick.major.size": 2,
    "legend.frameon": False,
})
MM = 1 / 25.4
IMMUNE = ["CD14_M", "CD16_M", "HB", "dNK", "T", "B", "cDC"]
COLORS = {"CD14_M": "#0F4D92", "CD16_M": "#3775BA", "HB": "#42949E", "dNK": "#9A4D8E",
          "T": "#767676", "B": "#B64342", "cDC": "#272727"}
BLUE = LinearSegmentedColormap.from_list("b", ["#F4F4F4", "#9DBBDD", "#3775BA", "#0F4D92", "#0A2F5C"])
MOD_LABEL = {"CORE": "Core", "EXTENDED": "Extended", "LYSO_CONTROL": "Lysosomal ctrl",
             "COMPLEMENT_CONTROL": "Complement ctrl", "MAC_IDENTITY": "Macrophage identity",
             "MONO_LIKE": "Monocyte-like"}
MAIN = "maternal_macrophage (CD14_M+CD16_M)"
SENS = "sensitivity: CD14_M only"


def label(ax, s, x=-0.18):
    ax.text(x, 1.06, s, transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom")


def save(fig, stem: Path):
    stem.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "pdf"):
        fig.savefig(stem.with_suffix(f".{ext}"), dpi=600)
    fig.savefig(stem.with_suffix(".tiff"), dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(stem.parent / f"{stem.name}_preview.png", dpi=300)
    plt.close(fig)


def fig_l1(t: Path, cells: Path, out: Path):
    u = pd.read_csv(cells / "cp1d_L1_immune_umap_cells.csv.gz", index_col=0)
    mk = pd.read_csv(t / "cp1d_L1_immune_marker_dotplot.csv")
    comp = pd.read_csv(t / "cp1d_L1_immune_composition_by_donor.csv")
    fig = plt.figure(figsize=(183 * MM, 72 * MM))
    ax = fig.add_axes([0.035, 0.12, 0.19, 0.76])
    for ct in IMMUNE:
        d = u[u.celltype == ct]
        ax.scatter(d.umap1, d.umap2, s=0.5, c=COLORS[ct], lw=0, rasterized=True)
    x0, x1 = u.umap1.quantile([0.005, 0.995]); y0, y1 = u.umap2.quantile([0.005, 0.995])
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("UMAP1 (author integrated)"); ax.set_ylabel("UMAP2")
    lg = fig.add_axes([0.23, 0.40, 0.05, 0.48]); lg.axis("off")
    for i, ct in enumerate(IMMUNE):
        lg.scatter([0.05], [1 - i * 0.14], s=8, c=COLORS[ct], lw=0)
        lg.text(0.25, 1 - i * 0.14, f"{ct.replace('_', ' ')} ({int((u.celltype == ct).sum()):,})", va="center",
                fontsize=5.5)
    lg.set_xlim(0, 1); lg.set_ylim(0, 1.05)
    label(ax, "a", x=-0.08)

    ax = fig.add_axes([0.40, 0.30, 0.285, 0.58])
    genes = list(dict.fromkeys(mk.gene))
    xm = {g: i for i, g in enumerate(genes)}
    ym = {c: i for i, c in enumerate(IMMUNE)}
    vmax = mk.mean_log1p_cp10k.quantile(0.98)
    sc = ax.scatter(mk.gene.map(xm), mk.celltype.map(ym), s=0.3 * mk.pct_expr.clip(upper=100) ** 1.0 + 0.0,
                    c=mk.mean_log1p_cp10k.clip(upper=vmax), cmap=BLUE, vmin=0, vmax=vmax,
                    edgecolors="#272727", linewidths=0.2)
    ax.set_xticks(range(len(genes)), genes, rotation=90)
    ax.set_yticks(range(len(IMMUNE)), [c.replace("_", " ") for c in IMMUNE])
    ax.set_ylim(len(IMMUNE) - 0.5, -0.5); ax.set_xlim(-0.6, len(genes) - 0.4)
    groups = mk.drop_duplicates("gene")[["gene", "marker_group"]]
    for grp, gg in groups.groupby("marker_group", sort=False):
        xs = [xm[g] for g in gg.gene]
        ax.plot([min(xs) - 0.3, max(xs) + 0.3], [-0.9, -0.9], color="#272727", lw=0.6, clip_on=False)
        ax.text(np.mean(xs), -1.1, grp.replace(" cell", "").replace("Dendritic", "DC"), ha="center", va="bottom", fontsize=5.5)
    cax = fig.add_axes([0.695, 0.62, 0.008, 0.22])
    cb = fig.colorbar(sc, cax=cax); cb.outline.set_linewidth(0.5); cb.ax.tick_params(labelsize=5.5, length=2)
    cb.set_label("Mean log1p(CP10k)", fontsize=5.5)
    sl = fig.add_axes([0.69, 0.28, 0.05, 0.26]); sl.axis("off")
    sl.text(0, 1.0, "Expressing (%)", fontsize=5.5, va="top")
    for i, pct in enumerate([10, 50, 100]):
        sl.scatter([0.15], [0.72 - i * 0.28], s=0.3 * pct, facecolor="#CFCECE", edgecolor="#272727", lw=0.2)
        sl.text(0.45, 0.72 - i * 0.28, f"{pct}", va="center", fontsize=5.5)
    sl.set_xlim(0, 1); sl.set_ylim(0, 1)
    label(ax, "b", x=-0.12)

    ax = fig.add_axes([0.84, 0.30, 0.145, 0.58])
    piv = comp.pivot_table(index=["sample_id", "gestational_week"], columns="celltype", values="n_cells",
                           fill_value=0).reset_index()
    piv["gw"] = piv.gestational_week.str.replace("GW", "").astype(int)
    piv = piv.sort_values("gw")
    frac = piv[IMMUNE].div(piv[IMMUNE].sum(1), axis=0)
    left = np.zeros(len(piv))
    for ct in IMMUNE:
        ax.barh(range(len(piv)), frac[ct], left=left, color=COLORS[ct], height=0.85, lw=0)
        left += frac[ct].to_numpy()
    ax.set_yticks(range(len(piv)), [f"{s} ({g})" for s, g in zip(piv.sample_id, piv.gestational_week)],
                  fontsize=5)
    ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xlabel("Fraction of immune nuclei")
    label(ax, "c", x=-0.55)
    save(fig, out / "CP1D_L1_immune_landscape" / "CP1D_L1_immune_landscape")


def fig_l2(t: Path, cells: Path, out: Path):
    s = pd.read_csv(cells / "cp1d_L2_macrophage_scores_cells.csv.gz", index_col=0)
    assoc = pd.read_csv(t / "cp1d_L2_tnfsf12_association.csv")
    ds = pd.read_csv(t / "cp1d_L2_donor_split.csv")
    null = pd.read_csv(t / "cp1d_L2_null_CORE_mac.csv")
    fig = plt.figure(figsize=(183 * MM, 62 * MM))

    ax = fig.add_axes([0.035, 0.14, 0.19, 0.74])
    o = s.sort_values("CORE")
    lim = np.quantile(o.CORE, [0.02, 0.98])
    scat = ax.scatter(o.umap1, o.umap2, c=o.CORE.clip(*lim), cmap=BLUE, s=1.0, lw=0, rasterized=True)
    pos = s[s.pos]
    ax.scatter(pos.umap1, pos.umap2, s=1.5, facecolor="none", edgecolor="#B64342", lw=0.3)
    x0, x1 = s.umap1.quantile([0.02, 0.98]); y0, y1 = s.umap2.quantile([0.02, 0.98])
    px, py = 0.15 * (x1 - x0), 0.15 * (y1 - y0)
    ax.set_xlim(x0 - px, x1 + px); ax.set_ylim(y0 - py, y1 + py)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel("UMAP1 (author integrated, zoomed)"); ax.set_ylabel("UMAP2")
    cax = fig.add_axes([0.232, 0.50, 0.007, 0.25])
    cb = fig.colorbar(scat, cax=cax); cb.outline.set_linewidth(0.5); cb.ax.tick_params(labelsize=5.5, length=2)
    cb.set_label("Core score", fontsize=5.5)
    ax.set_title("Maternal macrophages; open red, TNFSF12 UMI > 0", fontsize=5.5, loc="left")
    label(ax, "a", x=-0.08)

    ax = fig.add_axes([0.35, 0.18, 0.14, 0.66])
    d = ds[(ds.population == MAIN) & (ds.module == "CORE")]
    for _, r in d.iterrows():
        ax.plot([0, 1], [r.pct_low, r.pct_high], color="#767676", lw=0.5, zorder=1)
    ax.scatter(np.zeros(len(d)), d.pct_low, s=6, c="#CFCECE", edgecolor="#272727", lw=0.3, zorder=2)
    ax.scatter(np.ones(len(d)), d.pct_high, s=6, c="#0F4D92", edgecolor="#272727", lw=0.3, zorder=2)
    ax.set_xticks([0, 1], ["Core low", "Core high"]); ax.set_xlim(-0.4, 1.4)
    ax.set_ylabel("TNFSF12-detected macrophages (%)")
    a = assoc[(assoc.population == MAIN) & (assoc.module == "CORE")].iloc[0]
    ax.set_title(f"{a.n_donors_high_gt_low}/{a.n_donors_informative} donors high > low\n"
                 f"MH OR {a.mh_or:.2f} ({a.mh_or_lo:.2f}–{a.mh_or_hi:.2f})", fontsize=5.5, loc="left")
    label(ax, "b")

    ax = fig.add_axes([0.62, 0.18, 0.17, 0.66])
    mods = list(MOD_LABEL)
    for k, (pop, col, off) in enumerate([(MAIN, "#0F4D92", -0.15), (SENS, "#42949E", 0.15)]):
        q = assoc[assoc.population == pop].set_index("module").loc[mods]
        y = np.arange(len(mods)) + off
        ax.errorbar(q.clogit_or_per_sd, y, xerr=[q.clogit_or_per_sd - q.clogit_lo, q.clogit_hi - q.clogit_or_per_sd],
                    fmt="o", ms=2.5, color=col, ecolor=col, elinewidth=0.7, capsize=0,
                    label="CD14_M + CD16_M" if k == 0 else "CD14_M only")
    ax.axvline(1, color="#767676", lw=0.5, ls=(0, (2, 2)))
    ax.set_yticks(range(len(mods)), [MOD_LABEL[m] for m in mods]); ax.invert_yaxis()
    ax.set_xlim(0.7, 1.8); ax.set_xticks([0.8, 1.0, 1.2, 1.4, 1.6])
    ax.set_xlabel("OR per SD of score\n(logit, donor fixed effects + library size)")
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), fontsize=5.5, handletextpad=0.2, ncol=1,
              borderaxespad=0.2)
    label(ax, "c", x=-0.62)

    ax = fig.add_axes([0.87, 0.18, 0.115, 0.66])
    ax.hist(null.null_or_per_sd, bins=30, color="#CFCECE", edgecolor="#767676", lw=0.3)
    obs = a.clogit_or_per_sd
    ax.axvline(obs, color="#0F4D92", lw=1.0)
    nm = pd.read_csv(t / "cp1d_L2_matched_random_null.csv")
    pe = nm[(nm.population == MAIN) & (nm.module == "CORE")].empirical_p_one_sided.iloc[0]
    ax.set_xlabel("OR per SD, matched\nrandom 6-gene modules"); ax.set_ylabel("Count")
    ax.set_title(f"Core observed (line)\nempirical P = {pe:.3f}", fontsize=5.5, loc="left")
    label(ax, "d")
    save(fig, out / "CP1D_L2_tweak_associated_state" / "CP1D_L2_tweak_associated_state")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tables", required=True, type=Path)
    p.add_argument("--cell-dir", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    a = p.parse_args()
    fig_l1(a.tables, a.cell_dir, a.out_dir)
    fig_l2(a.tables, a.cell_dir, a.out_dir)


if __name__ == "__main__":
    main()
