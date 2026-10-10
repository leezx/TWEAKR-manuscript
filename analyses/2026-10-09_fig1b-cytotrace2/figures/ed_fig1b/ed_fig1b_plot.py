#!/usr/bin/env python3
"""Extended Data for Fig. 1b (nature-figure, Python): heterogeneity, robustness and L2 landscape.

Claim: the Fig. 1b ordering holds in every cohort and every completed sensitivity analysis, its
magnitude depends on sequencing depth, and the stromal signal is concentrated in fibroblasts.
Panels
  a  13-cohort forest plots for the three primary contrasts: study mean with 95% t-CI (points),
     pooled estimate with 95% CI (diamond) and 95% prediction interval (thin grey bar).
  b  pooled estimates (95% CI) across completed sensitivity analyses.
  c  L2 landscape: patient medians per eligible L2 type (secondary, descriptive), n patients / cohorts.
  d  cohort x L2 type median of patient medians (descriptive heatmap).
Size: 183 x 190 mm; text 5-6 pt; panel labels 8 pt.
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon

HERE = Path(__file__).resolve().parent
T = HERE.parents[1] / "tables" / "full"
MM = 1 / 25.4
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none", "pdf.fonttype": 42, "font.size": 5.5,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2, "ytick.major.size": 2, "axes.labelsize": 5.5,
    "xtick.labelsize": 5, "ytick.labelsize": 5,
    "axes.spines.right": False, "axes.spines.top": False, "legend.frameon": False,
})
BLUE, GREY, DARK = "#0F4D92", "#767676", "#272727"
PAIRS = ["Epithelial-Immune", "Epithelial-Stromal", "Stromal-Immune"]
PL = {"Epithelial-Immune": "Epithelial − Immune", "Epithelial-Stromal": "Epithelial − Stromal",
      "Stromal-Immune": "Stromal − Immune"}
SHORT = {"Chen_2024_Cancer_Cell": "Chen 2024", "Guo_2022_JCI_Insight": "Guo 2022",
         "Joanito_2022_Nat_Genet": "Joanito 2022", "Khaliq_2022_Genome_Biol": "Khaliq 2022",
         "Lee_2020_Nat_Genet": "Lee 2020", "Li_2023_Cancer_Cell": "Li 2023", "Liu_2024_Cancer_Res": "Liu 2024",
         "MUI_Innsbruck": "MUI Innsbruck", "Pelka_2021_Cell": "Pelka 2021", "Qi_2022_Nat_Commun": "Qi 2022",
         "Qian_2020_Cell_Res": "Qian 2020", "Qin_2023_Cell_Rep_Med": "Qin 2023",
         "Uhlitz_2021_EMBO_Mol_Med": "Uhlitz 2021"}
SENS = [("primary", "Primary"), ("raw_model_score", "Raw model score"), ("stringent_50_10", "Stringent (50 cells)"),
        ("unsorted_only", "Unsorted samples only"), ("F1_clean_L1", "F1-clean cells"),
        ("cycling_negative", "Cycling-negative cells"), ("low_gene_excluded_500", "Low-gene cells excluded"),
        ("detection_adjusted", "Detection-adjusted"), ("depth_matched", "Depth-matched (5 seeds)"),
        ("depth_matched_raw", "Depth-matched raw score")]
L2_ORDER = [("Stromal", ["Fibroblast", "Smooth muscle", "Pericyte", "Endothelial"]),
            ("Epithelial", ["Malignant epithelial"]),
            ("Immune", ["Plasma", "Monocyte", "Mast", "Macrophage", "Dendritic cell", "B", "Neutrophil", "NK",
                        "CD4 T", "CD8 T"])]
LCOL = {"Stromal": "#42949E", "Epithelial": BLUE, "Immune": GREY}


def forest(ax, st, pr, contrast, show_labels):
    s = st[(st.analysis == "primary") & (st.contrast == contrast)].sort_values("study_id", ascending=False)
    y = np.arange(len(s)) + 2
    ax.errorbar(s.mean_delta, y, xerr=[s.mean_delta - s.ci_low, s.ci_high - s.mean_delta], fmt="s", ms=2,
                color=DARK, elinewidth=0.6, capsize=0)
    r = pr[(pr.analysis == "primary") & (pr.contrast == contrast)].iloc[0]
    ax.plot([r.pi_low, r.pi_high], [0.45, 0.45], color="#CFCECE", lw=2.2, solid_capstyle="butt")
    ax.add_patch(Polygon([[r.ci_low, 1], [r.estimate, 1.32], [r.ci_high, 1], [r.estimate, 0.68]],
                         closed=True, color=BLUE, lw=0))
    ax.axvline(0, color=GREY, lw=0.5, ls=(0, (2, 2)), zorder=0)
    ax.axvline(r.estimate, color=BLUE, lw=0.4, ls=(0, (1, 1.5)), zorder=0)
    labels = [f"{SHORT[x]} ({n})" for x, n in zip(s.study_id, s.n_patients)] + ["Pooled (95% CI)", "95% PI"]
    ax.set_yticks(list(y) + [1, 0.45], labels if show_labels else [""] * len(labels))
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_ylim(0, len(s) + 2.6)
    ax.set_title(PL[contrast], fontsize=5.5, pad=2)
    ax.set_xlabel("Within-patient difference")


def sensitivity(ax, pr):
    rows = []
    for key, lab in SENS:
        for c in PAIRS:
            if key.startswith("depth_matched"):
                x = pr[pr.analysis.str.fullmatch(key + r"_ds\d") & (pr.contrast == c)]
                rows.append((lab, c, x.estimate.mean(), x.ci_low.mean(), x.ci_high.mean(), int(x.n_patients.iloc[0])))
            else:
                x = pr[(pr.analysis == key) & (pr.contrast == c)].iloc[0]
                rows.append((lab, c, x.estimate, x.ci_low, x.ci_high, int(x.n_patients)))
    d = pd.DataFrame(rows, columns=["analysis", "contrast", "estimate", "ci_low", "ci_high", "n"])
    labs = [l for _, l in SENS]
    off = {"Epithelial-Immune": 0.25, "Epithelial-Stromal": 0, "Stromal-Immune": -0.25}
    mk = {"Epithelial-Immune": "o", "Epithelial-Stromal": "s", "Stromal-Immune": "^"}
    for c in PAIRS:
        x = d[d.contrast == c]
        yy = np.array([len(labs) - 1 - labs.index(a) for a in x.analysis]) + off[c]
        ax.errorbar(x.estimate, yy, xerr=[x.estimate - x.ci_low, x.ci_high - x.estimate], fmt=mk[c], ms=2.4,
                    color=BLUE if c != "Stromal-Immune" else "#42949E", mfc="white" if c == "Epithelial-Stromal" else None,
                    elinewidth=0.6, capsize=0, label=PL[c])
    ax.axvline(0, color=GREY, lw=0.5, ls=(0, (2, 2)), zorder=0)
    ax.set_yticks(range(len(labs))[::-1], [f"{l} ({d[d.analysis == l].n.iloc[0]})" for l in labs])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Pooled within-patient difference (95% CI)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=5, handletextpad=0.2,
              columnspacing=0.8, borderaxespad=0.2)
    return d


def l2_landscape(ax, l2):
    rng = np.random.default_rng(2)
    xi, ticks, labs = 0, [], []
    for lin, types in L2_ORDER:
        for t in types:
            v = l2.loc[l2.group == t, "v"].to_numpy()
            ax.scatter(xi + rng.uniform(-0.22, 0.22, len(v)), v, s=1.2, color=LCOL[lin], alpha=0.45, linewidths=0)
            ax.boxplot(v, positions=[xi], widths=0.55, showfliers=False, patch_artist=True,
                       boxprops=dict(facecolor="none", edgecolor=DARK, linewidth=0.6),
                       medianprops=dict(color=DARK, linewidth=0.9), whiskerprops=dict(color=DARK, linewidth=0.6),
                       capprops=dict(linewidth=0))
            sub = l2[l2.group == t]
            ax.text(xi, 0.815, f"{sub.patient_id.nunique()}\n{sub.study_id.nunique()}", ha="center", va="bottom",
                    fontsize=4.5, linespacing=1.0, clip_on=False)
            ticks.append(xi); labs.append(t.replace("Malignant epithelial", "Malignant epi.*"))
            xi += 1
        xi += 0.5
    ax.text(-1.0, 0.815, "patients\ncohorts", ha="right", va="bottom", fontsize=4.5, linespacing=1.0,
            clip_on=False)
    ax.set_xticks(ticks, labs, rotation=45, ha="right")
    ax.set_xlim(-0.7, xi - 0.8)
    ax.set_ylim(0, 0.8)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.set_ylabel("CytoTRACE2 score (patient median)")


def heatmap(ax, hm, cax):
    types = [t for _, ts in L2_ORDER for t in ts]
    m = hm.pivot(index="study_id", columns="group", values="median_of_patient_medians").reindex(columns=types)
    m = m.sort_index()
    im = ax.imshow(m.to_numpy(), aspect="auto", cmap="cividis", vmin=0, vmax=0.6, interpolation="nearest")
    for (i, j), v in np.ndenumerate(m.to_numpy()):
        if np.isnan(v):
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor="white", edgecolor="#CFCECE", lw=0.3,
                                       hatch="//////"))
    ax.set_xticks(range(len(types)), [t.replace("Malignant epithelial", "Malignant epi.*") for t in types],
                  rotation=45, ha="right")
    ax.set_yticks(range(len(m)), [SHORT[s] for s in m.index])
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    cb = plt.colorbar(im, cax=cax)
    cb.set_label("Median CytoTRACE2 score", fontsize=5)
    cb.ax.tick_params(labelsize=5, width=0.5, length=1.5)
    cb.outline.set_linewidth(0.5)
    return m


def main():
    st = pd.read_csv(T / "study_contrasts.csv")
    pr = pd.read_csv(T / "pooled_contrasts.csv")
    l2 = pd.read_csv(T / "patient_medians_L2.csv")
    hm = pd.read_csv(T / "L2_study_heatmap.csv")
    fig = plt.figure(figsize=(183 * MM, 190 * MM))
    # a: three forest plots
    xs = [0.15, 0.43, 0.71]
    for k, c in enumerate(PAIRS):
        ax = fig.add_axes([xs[k], 0.70, 0.25, 0.27])
        forest(ax, st, pr, c, show_labels=(k == 0))
    # b: sensitivity
    axb = fig.add_axes([0.20, 0.40, 0.29, 0.22])
    sens = sensitivity(axb, pr)
    # c: L2 landscape
    axc = fig.add_axes([0.62, 0.40, 0.36, 0.20])
    l2_landscape(axc, l2)
    # d: heatmap
    axd = fig.add_axes([0.15, 0.06, 0.62, 0.24])
    cax = fig.add_axes([0.79, 0.12, 0.012, 0.14])
    m = heatmap(axd, hm, cax)
    for lab, (x, y) in zip("abcd", [(0.01, 0.995), (0.01, 0.655), (0.53, 0.655), (0.01, 0.335)]):
        fig.text(x, y, lab, fontsize=8, fontweight="bold", va="top")
    for ext in ["svg", "pdf"]:
        fig.savefig(HERE / f"ed_fig1b.{ext}")
    fig.savefig(HERE / "ed_fig1b.tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(HERE / "ed_fig1b_preview.png", dpi=300)
    st[st.analysis == "primary"].to_csv(HERE / "ed_fig1b_source_a.csv", index=False)
    sens.to_csv(HERE / "ed_fig1b_source_b.csv", index=False)
    l2.to_csv(HERE / "ed_fig1b_source_c.csv", index=False)
    m.to_csv(HERE / "ed_fig1b_source_d.csv")
    print("done")


if __name__ == "__main__":
    main()
