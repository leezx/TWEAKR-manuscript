#!/usr/bin/env python3
"""Fig. 1B — CytoTRACE2-predicted developmental potential across CRC compartments (nature-figure, Python).

Figure contract
- Claim: across 222 patients from 13 cohorts, predicted developmental potential is ordered
  Stromal > Epithelial > Immune; the ordering survives depth matching, but the effects shrink by ~43-55%.
- Archetype: quantitative grid, hero panel (left) + robustness panel (right).
- Left: patient-level medians (n = 222 per compartment), box = median/IQR, small black
  markers = per-study median of patient medians (13 per compartment).
- Right: pooled within-patient contrasts (REML + Hartung-Knapp, 95% CI), original counts vs
  depth-matched counts (mean of 5 seeds; CI = mean of seed CIs; seed range in source data).
- Size: 120 x 52 mm (sub-panel of Figure 1, two-column page); text 5-7 pt; label 8 pt.
Inputs: ../../tables/full/{patient_medians_L1_primary.csv, pooled_contrasts.csv}
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
T = HERE.parents[1] / "tables" / "full"
MM = 1 / 25.4

mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none", "pdf.fonttype": 42, "font.size": 6,
    "axes.linewidth": 0.7, "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "axes.labelsize": 6,
    "xtick.labelsize": 6, "ytick.labelsize": 6,
    "axes.spines.right": False, "axes.spines.top": False, "legend.frameon": False,
})

COMP = ["Stromal", "Epithelial", "Immune"]
COL = {"Stromal": "#42949E", "Epithelial": "#0F4D92", "Immune": "#767676"}
PAIRS = ["Stromal-Immune", "Epithelial-Immune", "Epithelial-Stromal"]
PAIR_LABEL = {"Stromal-Immune": "Stromal − Immune", "Epithelial-Immune": "Epithelial − Immune",
              "Epithelial-Stromal": "Epithelial − Stromal"}


def load():
    pm = pd.read_csv(T / "patient_medians_L1_primary.csv")
    pc = pd.read_csv(T / "pooled_contrasts.csv")
    prim = pc[pc.analysis == "primary"].set_index("contrast")
    ds = pc[pc.analysis.str.fullmatch(r"depth_matched_ds\d")]
    dsm = ds.groupby("contrast").agg(estimate=("estimate", "mean"), ci_low=("ci_low", "mean"),
                                     ci_high=("ci_high", "mean"), est_min=("estimate", "min"),
                                     est_max=("estimate", "max"), n_patients=("n_patients", "first"),
                                     k=("k", "first"))
    return pm, prim, dsm


def panel_scores(ax, pm):
    rng = np.random.default_rng(1)
    for i, c in enumerate(COMP):
        v = pm.loc[pm.group == c, "v"].to_numpy()
        ax.scatter(i - 0.08 + rng.uniform(-0.17, 0.17, len(v)), v, s=2.2, color=COL[c], alpha=0.45,
                   linewidths=0, zorder=2, rasterized=False)
        ax.boxplot(v, positions=[i - 0.08], widths=0.42, showfliers=False, patch_artist=True, zorder=3,
                   boxprops=dict(facecolor="none", edgecolor="#272727", linewidth=0.7),
                   medianprops=dict(color="#272727", linewidth=1.1),
                   whiskerprops=dict(color="#272727", linewidth=0.7), capprops=dict(linewidth=0))
        sm = pm[pm.group == c].groupby("study_id").v.median().to_numpy()
        ax.scatter(np.full(len(sm), i + 0.27), sm, s=5, marker="D", facecolor="white",
                   edgecolor="#272727", linewidths=0.5, zorder=4)
    ax.set_xticks(range(len(COMP)), COMP)
    ax.set_xlim(-0.6, 2.55)
    ax.set_ylim(0, 0.62)
    ax.set_yticks([0, 0.2, 0.4, 0.6])
    ax.set_ylabel("CytoTRACE2 score (patient median)")
    ax.text(0.98, 0.98, "222 patients · 13 cohorts", transform=ax.transAxes, ha="right", va="top", fontsize=5.5)
    # in-panel key for the two marker types
    ax.scatter([1.62], [0.535], s=2.2, color="#767676", linewidths=0)
    ax.text(1.70, 0.535, "patient", va="center", fontsize=5)
    ax.scatter([1.62], [0.495], s=5, marker="D", facecolor="white", edgecolor="#272727", linewidths=0.5)
    ax.text(1.70, 0.495, "cohort median", va="center", fontsize=5)


def panel_contrasts(ax, prim, dsm):
    y = np.arange(len(PAIRS))[::-1].astype(float)
    off = 0.16
    for yi, p in zip(y, PAIRS):
        r = prim.loc[p]
        ax.errorbar(r.estimate, yi + off, xerr=[[r.estimate - r.ci_low], [r.ci_high - r.estimate]], fmt="o",
                    ms=3.2, color="#0F4D92", mec="#0F4D92", elinewidth=0.8, capsize=0)
        d = dsm.loc[p]
        ax.errorbar(d.estimate, yi - off, xerr=[[d.estimate - d.ci_low], [d.ci_high - d.estimate]], fmt="o",
                    ms=3.2, color="#0F4D92", mfc="white", mec="#0F4D92", mew=0.8, elinewidth=0.8, capsize=0)
    ax.axvline(0, color="#767676", lw=0.6, ls=(0, (2, 2)), zorder=0)
    ax.set_yticks(y, [PAIR_LABEL[p] for p in PAIRS])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(-0.25, 0.32)
    ax.set_xticks([-0.2, -0.1, 0, 0.1, 0.2, 0.3])
    ax.set_ylim(-0.6, len(PAIRS) - 0.4)
    ax.set_xlabel("Pooled within-patient difference\n(CytoTRACE2 score, 95% CI)")
    ax.errorbar([], [], fmt="o", ms=3.2, color="#0F4D92", label="Original counts (n = 222)")
    ax.errorbar([], [], fmt="o", ms=3.2, color="#0F4D92", mfc="white", mew=0.8,
                label=f"Depth-matched (n = {int(dsm.n_patients.iloc[0])}; 5 seeds)")
    ax.legend(loc="lower left", bbox_to_anchor=(-0.02, 1.0), fontsize=5, handletextpad=0.3,
              borderaxespad=0, ncol=1)


def main():
    pm, prim, dsm = load()
    fig = plt.figure(figsize=(120 * MM, 52 * MM))
    a1 = fig.add_axes([0.085, 0.16, 0.38, 0.76])
    a2 = fig.add_axes([0.665, 0.22, 0.32, 0.58])
    panel_scores(a1, pm)
    panel_contrasts(a2, prim, dsm)
    fig.text(0.005, 0.985, "b", fontsize=8, fontweight="bold", va="top")
    for ext in ["svg", "pdf"]:
        fig.savefig(HERE / f"fig1b.{ext}")
    fig.savefig(HERE / "fig1b.tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(HERE / "fig1b_preview.png", dpi=300)

    # source data (one tidy file per panel element)
    s1 = pm.rename(columns={"group": "compartment", "v": "patient_median_score"})
    s1.insert(0, "panel", "left_patient_medians")
    rows = []
    for p in PAIRS:
        r = prim.loc[p]
        rows.append({"panel": "right_contrasts", "contrast": p, "analysis": "original", "estimate": r.estimate,
                     "ci_low": r.ci_low, "ci_high": r.ci_high, "pi_low": r.pi_low, "pi_high": r.pi_high,
                     "n_patients": r.n_patients, "k_studies": r.k, "p_holm": r.p_holm})
        d = dsm.loc[p]
        rows.append({"panel": "right_contrasts", "contrast": p, "analysis": "depth_matched_mean_5_seeds",
                     "estimate": d.estimate, "ci_low": d.ci_low, "ci_high": d.ci_high, "seed_min": d.est_min,
                     "seed_max": d.est_max, "n_patients": d.n_patients, "k_studies": d.k})
    s1.to_csv(HERE / "fig1b_source_left.csv", index=False)
    pd.DataFrame(rows).to_csv(HERE / "fig1b_source_right.csv", index=False)
    print("done")


if __name__ == "__main__":
    main()
