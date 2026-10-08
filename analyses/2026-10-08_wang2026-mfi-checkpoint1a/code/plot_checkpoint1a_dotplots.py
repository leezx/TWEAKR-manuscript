#!/usr/bin/env python3
"""Checkpoint 1A DotPlots (Python / matplotlib, Nature-style export).

Reads only the lightweight summary table produced by checkpoint1a_expression.py.
"""

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
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "font.size": 6,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "xtick.major.size": 2,
    "ytick.major.size": 2,
    "legend.frameon": False,
    "text.color": "#000000",
})

MM = 1 / 25.4
MIN_CELLS = 20
COLUMNS = ["All", "T1 (GW5-13)", "T2 (GW14-27)", "T3 (GW28-40)"]
COL_LABELS = ["All", "T1", "T2", "T3"]
ORIGINS = ["maternal", "fetal", "mixed", "ambiguous"]
ORIGIN_LABELS = {"maternal": "Maternal", "fetal": "Fetal", "mixed": "Mixed", "ambiguous": "Ambiguous"}
CMAP = LinearSegmentedColormap.from_list("tweakr_blue", ["#F4F4F4", "#9DBBDD", "#3775BA", "#0F4D92", "#0A2F5C"])
PCT_REF = 20.0
SIZE_MAX = 30.0


def dot_size(pct):
    return SIZE_MAX * np.clip(np.asarray(pct, dtype=float) / PCT_REF, 0, 1.3)


def row_order(omap: pd.DataFrame) -> list[tuple[str, str]]:
    major_order = ["M", "dNK", "T", "B", "cDC", "DSC", "EC", "Epi", "EVT", "VCT", "SCT", "HB", "FB", "PV", "Ery"]
    rows = []
    for o in ORIGINS:
        sub = omap[omap.author_cell_type_origin == o].copy()
        sub["mo"] = sub.major_class.map({m: i for i, m in enumerate(major_order)}).fillna(99)
        sub = sub.sort_values(["mo", "minor_class", "celltype_shortname"])
        rows += [(o, c) for c in sub.celltype_shortname]
    return rows


def plot_gene(gene: str, tab: pd.DataFrame, omap: pd.DataFrame, stem: Path):
    t = tab[tab.gene == gene]
    rows = row_order(omap)
    ypos = {}
    headers = {}
    y, prev = 0.0, None
    for o, c in rows:
        if o != prev:
            y += 0.4 if prev is not None else 0.0
            headers[o] = y
            y += 1.0
        ypos[c] = y
        y += 1.0
        prev = o
    ymax = y

    keep = t[(t.n_cells >= MIN_CELLS) & t.trimester.isin(COLUMNS)].copy()
    keep["x"] = keep.trimester.map({c: i for i, c in enumerate(COLUMNS)})
    keep["y"] = keep.celltype_shortname.map(ypos)
    vmax = float(np.ceil(keep.mean_log1p_cp10k.max() * 20) / 20)

    fig = plt.figure(figsize=(89 * MM, 118 * MM))
    ax = fig.add_axes([0.30, 0.06, 0.40, 0.86])
    det, zero = keep[keep.n_expr > 0], keep[keep.n_expr == 0]
    sc = ax.scatter(det.x, det.y, s=dot_size(det.pct_expr), c=det.mean_log1p_cp10k, cmap=CMAP,
                    vmin=0, vmax=vmax, edgecolors="#272727", linewidths=0.25, zorder=3)
    ax.scatter(zero.x, zero.y, s=1.2, facecolor="none", edgecolor="#767676", linewidths=0.4, zorder=3)
    ax.set_xlim(-0.6, len(COLUMNS) - 0.4)
    ax.set_ylim(ymax - 0.2, -0.6)
    ax.set_xticks(range(len(COLUMNS)), COL_LABELS)
    ax.xaxis.tick_top()
    ax.spines["top"].set_visible(True)
    ax.spines["bottom"].set_visible(False)
    ax.set_yticks([ypos[c] for _, c in rows], [c.replace("_", " ") for _, c in rows])
    ax.axvline(0.5, color="#767676", lw=0.4, ls=(0, (2, 2)), zorder=1)

    for o, yh in headers.items():
        ax.text(-0.04, yh, ORIGIN_LABELS[o], transform=ax.get_yaxis_transform(), ha="right", va="center",
                fontsize=6, fontweight="bold")

    lax = fig.add_axes([0.76, 0.62, 0.20, 0.26])
    lax.axis("off")
    lax.text(0, 1.0, "Expressing nuclei (%)", fontsize=6, va="top")
    for i, p in enumerate([0, 1, 5, 10, 20]):
        yy = 0.84 - i * 0.15
        if p == 0:
            lax.scatter([0.12], [yy], s=1.2, facecolor="none", edgecolor="#767676", linewidth=0.4)
            lax.text(0.32, yy, "0 (open)", va="center", fontsize=6)
            continue
        lax.scatter([0.12], [yy], s=dot_size(p), facecolor="#CFCECE", edgecolor="#272727", linewidth=0.25)
        lax.text(0.32, yy, f"{p}", va="center", fontsize=6)
    lax.set_xlim(0, 1)
    lax.set_ylim(0, 1)

    cax = fig.add_axes([0.77, 0.36, 0.035, 0.18])
    cb = fig.colorbar(sc, cax=cax)
    cb.outline.set_linewidth(0.5)
    cb.ax.tick_params(width=0.6, length=2, labelsize=6)
    cb.set_label("Mean per-nucleus log1p(CP10k)", fontsize=6)

    fig.text(0.02, 0.975, gene, fontsize=7, fontweight="bold", va="top")
    fig.text(0.76, 0.30, "T1, GW5–13\nT2, GW14–27\nT3, GW28–40\n\n"
             f"Blank: <{MIN_CELLS} nuclei\nin that stratum", fontsize=6, va="top")
    for ext in ("svg", "pdf"):
        fig.savefig(stem.with_suffix(f".{ext}"))
    fig.savefig(stem.with_suffix(".tiff"), dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(stem.parent / f"{stem.name}_preview.png", dpi=300)
    plt.close(fig)

    src = t[t.trimester.isin(COLUMNS)].copy()
    src["plotted"] = src.n_cells >= MIN_CELLS
    src.to_csv(stem.parent / f"{stem.name}_source.csv", index=False)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tables", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    a = p.parse_args()
    tab = pd.read_csv(a.tables / "expression_by_trimester_celltype.csv")
    omap = pd.read_csv(a.tables / "author_celltype_origin_map.tsv", sep="\t", keep_default_na=False)
    for gene in ("TNFSF12", "TNFRSF12A"):
        d = a.out_dir / f"CP1A_{gene}_dotplot"
        d.mkdir(parents=True, exist_ok=True)
        plot_gene(gene, tab, omap, d / f"CP1A_{gene}_dotplot")


if __name__ == "__main__":
    main()
