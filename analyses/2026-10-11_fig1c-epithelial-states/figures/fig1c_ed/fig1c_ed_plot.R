#!/usr/bin/env Rscript
# Extended Data for Fig. 1c (nature-figure, R). Panel map frozen in docs/Fig1c_stage4_final_review_20261011.md.
#
# Figure contract
# - Claim supported: the pro-rev separation in predicted developmental potency (Fig. 1c) is robust to annotation,
#   definition, depth, reference, subset and proxy choices; rev-ref is small and reference/proxy-dependent.
# - Role: robustness / reviewability. Archetype: quantitative grid.
# - a (ED-A) lineage transfer audit: per-study module-audit verdicts, annotation composition, OOD failure.
# - b (ED-B) raw UCell score architecture coloured by frozen sample-specific strata; full vs mechanism-blinded
#   p75 membership; stratum sizes at p70/p75/p80.
# - c (ED-C) study-level forests for the three primary contrasts with pooled estimate, 95% CI, 95% PI, I2, tau2
#   and leave-one-study-out (LOSO) range.
# - d (ED-D) depth and complexity: raw/final/adjusted/depth-matched estimands and the D2 intersection audit.
# - e (ED-E) definition robustness: p70/p80, mechanism-blinded scores, alternative references (+ common
#   subset), OOD-pass only.
# - f (ED-F) subsets: MSS, MSI-H, CNV-positive cells, Pelka excluded; MSI interaction.
# - g (ED-G) CytoTRACE2 vs SCENT-CCAT for the categorical contrasts and the continuous model.
# - h (ED-H) eligibility funnel, reference missingness after depth matching (D1) and eligibility loss (D3).
# - Size: 183 mm x 240 mm (full page); text 5-6 pt; panel letters 8 pt bold lower case.
# - Statistics: each estimate is a REML random-effects pooled study mean with Hartung-Knapp 95% CI; study-level
#   intervals in c are mean +/- 1.96 SE. Rows with < 3 studies are shown as "descriptive" without an estimate.
# Inputs: ../../tables/{stage1_v03a,stage3,stage4,figure/ed}/*.tsv (aggregate tables only).
suppressPackageStartupMessages({ library(ggplot2); library(data.table); library(patchwork) })

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)])))
tab <- file.path(here, "..", "..", "tables")
rd <- function(...) fread(file.path(tab, ...))

INK <- "#272727"; MID <- "#767676"; LIGHT <- "#CFCECE"; SIGNAL <- "#0F4D92"; REV <- "#9A4D8E"; TEAL <- "#42949E"
theme_nat <- theme_classic(base_size = 5.5, base_family = "Arial") +
  theme(axis.line = element_line(linewidth = 0.3, colour = INK),
        axis.ticks = element_line(linewidth = 0.3, colour = INK),
        axis.ticks.length = unit(0.7, "mm"),
        axis.text = element_text(size = 5, colour = "black"),
        axis.title = element_text(size = 5.5, colour = "black"),
        plot.title = element_text(size = 6, colour = "black", face = "plain", margin = margin(b = 1.5)),
        strip.text = element_text(size = 5.5, colour = "black"), strip.background = element_blank(),
        legend.title = element_text(size = 5), legend.text = element_text(size = 5),
        legend.key.size = unit(2, "mm"), legend.margin = margin(0, 0, 0, 0),
        plot.margin = margin(2, 3, 2, 2), panel.grid = element_blank())

short_study <- function(s) sub("^([A-Za-z]+)_(\\d{4}).*$", "\\1 \\2", sub("^MUI_Innsbruck$", "MUI Innsbruck", s))
CONTRASTS <- c(pro_vs_ref = "pro − ref", rev_vs_ref = "rev − ref", pro_vs_rev = "pro − rev",
               cycling_pro_vs_rev = "pro − rev\n(Cycling)")
CCOL <- c("pro − ref" = INK, "rev − ref" = INK, "pro − rev" = SIGNAL, "pro − rev\n(Cycling)" = MID)
# Per-contrast display limits; intervals beyond them are truncated and marked with an arrow.
XLIM <- list("pro − ref" = c(-0.10, 0.35), "rev − ref" = c(-0.06, 0.12), "pro − rev" = c(-0.06, 0.22),
             "pro − rev\n(Cycling)" = c(-0.02, 0.24))
fmt3 <- function(x) sprintf("%.3f", x)

# Shared robustness forest: rows = analysis variants, columns = contrasts.
rob_forest <- function(d, levels_variant, title, base_variant = NULL) {
  d <- copy(d)
  d[, contrast := factor(CONTRASTS[contrast], levels = CONTRASTS)]
  d[, variant := factor(variant, levels = rev(levels_variant))]
  d[, pooled := status == "pooled"]
  d[, xmid := sapply(as.character(contrast), function(k) mean(XLIM[[k]]))]
  lim <- rbindlist(lapply(names(XLIM), function(k) data.table(contrast = k, x = XLIM[[k]])))
  lim[, contrast := factor(contrast, levels = CONTRASTS)]
  d[pooled == TRUE, `:=`(lo = pmax(ci_low, XLIM[[as.character(contrast)]][1]),
                         hi = pmin(ci_high, XLIM[[as.character(contrast)]][2])), by = contrast]
  d[pooled == TRUE, `:=`(cut_lo = ci_low < lo, cut_hi = ci_high > hi)]
  base <- if (is.null(base_variant)) d[0] else d[variant == base_variant & pooled]
  p <- ggplot(d, aes(y = variant)) +
    geom_blank(data = lim, aes(x = x), inherit.aes = FALSE) +
    geom_vline(xintercept = 0, linewidth = 0.25, linetype = "22", colour = MID)
  if (!is.null(base_variant))
    p <- p + geom_vline(data = base, aes(xintercept = estimate), linewidth = 0.25, colour = LIGHT)
  p + geom_segment(data = d[pooled == TRUE], aes(x = lo, xend = hi, yend = variant, colour = contrast),
                   linewidth = 0.4) +
    geom_segment(data = d[pooled == TRUE & cut_hi], aes(x = hi - 1e-3, xend = hi, yend = variant, colour = contrast),
                 linewidth = 0.4, arrow = arrow(length = unit(0.8, "mm"), type = "closed")) +
    geom_segment(data = d[pooled == TRUE & cut_lo], aes(x = lo + 1e-3, xend = lo, yend = variant, colour = contrast),
                 linewidth = 0.4, arrow = arrow(length = unit(0.8, "mm"), type = "closed")) +
    geom_point(data = d[pooled == TRUE], aes(x = estimate, colour = contrast), size = 0.9) +
    geom_text(data = d[pooled == FALSE], aes(x = xmid, label = note), size = 5 / .pt, colour = MID,
              hjust = 0.5, family = "Arial") +
    scale_colour_manual(values = CCOL, guide = "none") +
    scale_x_continuous(breaks = function(l) if (diff(l) < 0.2) c(0, 0.1) else c(0, 0.2),
                       labels = function(b) sub("-", "−", ifelse(b == 0, "0", format(b, trim = TRUE, drop0trailing = TRUE))),
                       expand = expansion(mult = 0.02)) +
    facet_grid(. ~ contrast, scales = "free_x") +
    labs(x = "Δ predicted potency (CytoTRACE2)", y = NULL, title = title) +
    theme_nat +
    theme(axis.ticks.y = element_blank(), axis.line.y = element_blank(), panel.spacing.x = unit(1.6, "mm"),
          strip.text = element_text(size = 5, lineheight = 0.9))
}

s4 <- rd("stage4", "S4_pooled.tsv")
s3 <- rd("stage3", "S3_contrasts_pooled.tsv")[contrast %in% names(CONTRASTS)]
desc_note <- function(status, k, n) ifelse(status == "pooled", NA_character_,
                                           sprintf("k = %d, desc.", k))

# ================================================================ a  lineage audit (ED-A)
ver <- rd("stage1_v03a", "A_lineage_audit_verdict.tsv")
ver[, study := short_study(study_id)]
ver[, class := factor(sub(" differentiated-like", "", class),
                      levels = c("Absorptive", "Cycling Stem/TA", "Secretory", "Stem/TA-like"))]
VLAB <- c(verified = "Verified", lineage_transfer_unverified = "Failed (unverified)", not_evaluable = "Not evaluable")
ver[, verdict := factor(VLAB[verdict], levels = VLAB)]
stopifnot(nrow(ver) == 52, sum(ver$verdict == "Failed (unverified)") == 12)
st_order <- sort(unique(ver$study), decreasing = TRUE)
ver[, study := factor(study, levels = st_order)]
p_a1 <- ggplot(ver, aes(x = class, y = study, fill = verdict)) +
  geom_tile(colour = "white", linewidth = 0.4) +
  scale_fill_manual(values = c("Verified" = "#3775BA", "Failed (unverified)" = "#9A9A9A", "Not evaluable" = "#EDEDED"),
                    name = NULL) +
  scale_x_discrete(position = "top", labels = c("Absorptive" = "Absorptive", "Cycling Stem/TA" = "Cycling Stem/TA",
                              "Secretory" = "Secretory", "Stem/TA-like" = "Stem/TA-like")) +
  labs(x = NULL, y = NULL, title = "Module audit") +
  theme_nat +
  theme(axis.line = element_blank(), axis.ticks = element_blank(), legend.position = "bottom",
        axis.text.x.top = element_text(size = 5, angle = 40, hjust = 0, vjust = 0), legend.box.margin = margin(-2, 0, 0, 0)) +
  guides(fill = guide_legend(ncol = 1))

comp <- rd("stage1_v03a", "G8_lineage_composition_by_study_current.tsv")
comp <- melt(comp, id.vars = "study_id", variable.name = "lineage", value.name = "frac")
CAT <- c("Absorptive differentiated-like" = "Absorptive (ref.)", "Cycling Stem/TA" = "Cycling Stem/TA",
         "Secretory differentiated-like" = "Secretory", "Transitional stem/secretory" = "Trans./rare (not audited)",
         "Transitional secretory/absorptive" = "Trans./rare (not audited)",
         "Rare lineages" = "Trans./rare (not audited)", "lineage-transfer-unverified" = "Stem/TA-like (unverified)",
         "lineage-unresolved" = "Unresolved")
comp[, cat := factor(CAT[as.character(lineage)], levels = rev(unique(CAT)))]
comp <- comp[, .(frac = sum(frac)), by = .(study_id, cat)]
comp[, study := factor(short_study(study_id), levels = st_order)]
CATCOL <- c("Absorptive (ref.)" = "#3775BA", "Cycling Stem/TA" = SIGNAL, "Secretory" = TEAL,
            "Trans./rare (not audited)" = "#9FC3D6", "Stem/TA-like (unverified)" = "#9A9A9A", "Unresolved" = "#DDDDDD")
p_a2 <- ggplot(comp, aes(x = frac, y = study, fill = cat)) +
  geom_col(width = 0.75, colour = "white", linewidth = 0.1) +
  scale_fill_manual(values = CATCOL, breaks = names(CATCOL), name = NULL) +
  scale_x_continuous(breaks = c(0, 0.5, 1), labels = c("0", "50", "100"), expand = c(0, 0)) +
  labs(x = "Epithelial cells (%)", y = NULL, title = "Composition") +
  guides(fill = guide_legend(ncol = 2)) +
  theme_nat + theme(axis.text.y = element_blank(), legend.position = "bottom", legend.box.margin = margin(-2, 0, 0, 0))

ood <- rd("stage1_v03a", "A_ood_drivers_by_study.tsv")
ood[, study := factor(short_study(study_id), levels = st_order)]
p_a3 <- ggplot(ood, aes(x = frac_ood_fail, y = study)) +
  geom_segment(aes(x = 0, xend = frac_ood_fail, yend = study), linewidth = 0.3, colour = LIGHT) +
  geom_point(size = 0.9, colour = INK) +
  scale_x_continuous(limits = c(0, 1), breaks = c(0, 0.5, 1), labels = c("0", "50", "100"), expand = c(0, 0.02)) +
  labs(x = "OOD fail (%)", y = NULL, title = "OOD") +
  theme_nat + theme(axis.text.y = element_blank(), plot.margin = margin(2, 4, 2, 1))
p_a <- (p_a1 | p_a2 | p_a3) + plot_layout(widths = c(0.55, 1, 0.32))

# ================================================================ b  score architecture (ED-B)
rw <- rd("figure", "ed", "ed_b_raw_density.tsv")
stopifnot(abs(sum(rw$patient_weight) - 1) < 1e-6)
SL <- c(pro_dominant = "pro-dominant", rev_dominant = "rev-dominant", hybrid_high = "hybrid-high",
        neither_high = "neither-high", reference = "reference")
SCOL <- c("pro-dominant" = SIGNAL, "rev-dominant" = REV, "hybrid-high" = TEAL, "neither-high" = "#BDBDBD",
          "reference" = "#E3C27A")
dom <- rw[, .(tot = sum(patient_weight), stratum = stratum[which.max(patient_weight)]), by = .(pro_lo, rev_lo, bin_width)]
dom[, stratum := factor(SL[stratum], levels = SL)]
dom[, a := pmin(1, 0.15 + 0.85 * (log10(tot) - log10(quantile(tot, 0.05))) /
               (log10(quantile(tot, 0.99)) - log10(quantile(tot, 0.05))))]
dom[, a := pmax(a, 0.15)]
p_b1 <- ggplot(dom) +
  geom_rect(aes(xmin = pro_lo, xmax = pro_lo + bin_width, ymin = rev_lo, ymax = rev_lo + bin_width,
                fill = stratum, alpha = a), colour = NA) +
  scale_fill_manual(values = SCOL, name = NULL) + scale_alpha_identity() +
  scale_x_continuous(limits = c(0, 0.7), breaks = seq(0, 0.6, 0.2), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0, 0.5), breaks = seq(0, 0.4, 0.2), expand = c(0, 0)) +
  coord_fixed() +
  labs(x = "proCSC UCell score", y = "revCSC UCell score", title = "Raw UCell scores (majority stratum per bin)") +
  guides(fill = guide_legend(ncol = 1, override.aes = list(alpha = 1))) +
  theme_nat + theme(legend.position = "right", legend.box.margin = margin(0, 0, 0, -4))

tm <- rd("stage4", "S4_mb_transition_matrix.tsv")
tm <- melt(tm, id.vars = "full", variable.name = "mb", value.name = "n")
tm <- tm[full != "reference" & mb != "reference"]
tm[, frac := n / sum(n), by = full]
L4 <- c(pro_dominant = "pro", rev_dominant = "rev", hybrid_high = "hybrid", neither_high = "neither")
tm[, `:=`(full = factor(L4[full], levels = rev(L4)), mb = factor(L4[as.character(mb)], levels = L4))]
# stage4_summary.json contains NaN (not valid JSON); read the mb_jaccard block as text.
js <- paste(readLines(file.path(tab, "stage4", "stage4_summary.json"), warn = FALSE), collapse = "")
js <- regmatches(js, regexpr('"mb_jaccard"\\s*:\\s*\\{[^}]*\\}', js))
jac <- jsonlite::fromJSON(paste0("{", js, "}"))$mb_jaccard
tm[, lab := ifelse(frac >= 0.005, sprintf("%.0f", 100 * frac), "")]
p_b2 <- ggplot(tm, aes(x = mb, y = full, fill = frac)) +
  geom_tile(colour = "white", linewidth = 0.3) +
  geom_text(aes(label = lab, colour = frac > 0.5), size = 5 / .pt, family = "Arial") +
  scale_colour_manual(values = c(`TRUE` = "white", `FALSE` = "black"), guide = "none") +
  scale_fill_gradient(low = "#F4F6FA", high = SIGNAL, limits = c(0, 1), guide = "none") +
  scale_y_discrete(labels = function(x) sprintf("%s (J = %.2f)", x,
                                                unlist(jac[paste0(names(L4)[match(x, L4)])]))) +
  labs(x = "Mechanism-blinded stratum", y = "Full-signature stratum",
       title = "Full vs blinded (row %)") +
  theme_nat + theme(axis.line = element_blank(), axis.ticks = element_blank(),
                    axis.text.x = element_text(angle = 40, hjust = 1))

sz <- rd("figure", "ed", "ed_b_stratum_sizes.tsv")[stratum %in% c("pro_dominant", "rev_dominant", "hybrid_high")]
stopifnot(sz[threshold == "p75" & stratum == "pro_dominant", n_cells] == 50539)
sz[, stratum := factor(SL[stratum], levels = SL[1:3])]
p_b3 <- ggplot(sz, aes(x = threshold, y = n_cells / 1000, fill = stratum)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.75) +
  scale_fill_manual(values = SCOL, guide = "none") +
  scale_y_continuous(limits = c(0, 60), breaks = c(0, 20, 40, 60), expand = c(0, 0)) +
  labs(x = "Within-sample threshold", y = "Cells (×1,000)", title = "Stratum size") +
  theme_nat
p_b <- (p_b1 | p_b2) + plot_layout(widths = c(1.2, 0.8))

# ================================================================ c  study-level forests (ED-C)
bs <- rd("stage3", "S3_contrasts_by_study.tsv")[estimand == "final" & family == "primary_holm"]
pl <- s4[analysis == "base" & contrast %in% c("pro_vs_ref", "rev_vs_ref", "pro_vs_rev")]
stopifnot(nrow(pl) == 3, all(table(bs$contrast) == c(13, 8, 8)[match(names(table(bs$contrast)),
                                                                   c("pro_vs_rev", "pro_vs_ref", "rev_vs_ref"))]))
bs[, `:=`(study = short_study(study_id), lo = mean - 1.96 * se, hi = mean + 1.96 * se)]
all_st <- c(sort(unique(bs$study), decreasing = TRUE))
YP <- 0; YS <- setNames(seq_along(all_st) + 1.5, all_st)
bs[, y := YS[study]]
for (d in list(bs, pl)) d[, contrast := factor(CONTRASTS[contrast], levels = CONTRASTS[1:3])]
pl[, ann := sprintf("I² = %.2f; τ² = %.4f\nPI [%s, %s]\nLOSO %s–%s", I2, tau2, fmt3(pi_low), fmt3(pi_high),
                    fmt3(loso_min), fmt3(loso_max))]
dia <- pl[, .(x = c(ci_low, estimate, ci_high, estimate), y = YP + c(0, 0.45, 0, -0.45)), by = contrast]
p_c <- ggplot() +
  geom_vline(xintercept = 0, linewidth = 0.25, linetype = "22", colour = MID) +
  geom_vline(data = pl, aes(xintercept = estimate), linewidth = 0.25, colour = LIGHT) +
  geom_segment(data = bs, aes(x = lo, xend = hi, y = y, yend = y), linewidth = 0.35, colour = INK) +
  geom_point(data = bs, aes(x = mean, y = y, size = n_patients), shape = 15, colour = INK) +
  geom_segment(data = pl, aes(x = pi_low, xend = pi_high, y = YP, yend = YP), linewidth = 0.35, colour = MID) +
  geom_polygon(data = dia, aes(x = x, y = y, group = contrast, fill = contrast), colour = NA) +
  geom_text(data = pl, aes(x = Inf, y = YS[length(YS)] + 0.2, label = ann), hjust = 1, vjust = 1, size = 5 / .pt,
            lineheight = 0.9, family = "Arial") +
  scale_fill_manual(values = CCOL, guide = "none") +
  scale_size_area(max_size = 1.8, breaks = c(5, 15, 30), name = "Patients") +
  scale_y_continuous(breaks = c(YP, YS), labels = c("Pooled (95% CI; PI)", names(YS)), expand = expansion(add = 0.7)) +
  facet_grid(. ~ contrast, scales = "free_x") +
  labs(x = "Δ predicted potency (CytoTRACE2; study mean ± 1.96 SE)", y = NULL,
       title = "Primary contrasts by study") +
  theme_nat +
  theme(axis.ticks.y = element_blank(), axis.line.y = element_blank(), legend.position = "right",
        panel.spacing.x = unit(3, "mm"))

# ================================================================ d  depth and complexity (ED-D)
DV <- c("Final (primary)", "Raw CT2", "Adjusted, full", "Adjusted, reduced", "Depth-matched (ds mean)",
        "D2 A′: final, same samples", "D2 B: final, intersection cells", "D2 C: depth-matched, intersection")
dd <- rbind(
  s3[estimand %in% c("final", "raw", "adj_full", "adj_reduced", "ds_mean"),
     .(contrast, variant = c(final = DV[1], raw = DV[2], adj_full = DV[3], adj_reduced = DV[4], ds_mean = DV[5])[estimand],
       status, k, n_patients, estimate, ci_low, ci_high)],
  s4[analysis %in% c("dsint_Aprime_final_same_samples", "dsint_B_final", "dsint_C_ds"),
     .(contrast, variant = c(dsint_Aprime_final_same_samples = DV[6], dsint_B_final = DV[7], dsint_C_ds = DV[8])[analysis],
       status, k, n_patients, estimate, ci_low, ci_high)])
dd[, note := desc_note(status, k, n_patients)]
stopifnot(nrow(dd) == 32)
p_d <- rob_forest(dd, DV, "Depth and transcriptomic complexity", base_variant = DV[1])

# ================================================================ e  definitions and references (ED-E)
EV <- c("p75 (primary)", "p70 strata", "p80 strata", "Mechanism-blinded scores", "Strict reference",
        "Broad reference (abs. + sec.)", "Common subset: primary ref.", "Common subset: strict ref.",
        "Common subset: broad ref.", "OOD-pass cells only")
ee <- rbind(
  s4[analysis %in% c("base", "p70", "p80", "mechanism_blinded", "ref_strict", "ref_broad",
                     "refcommon:base", "refcommon:ref_strict", "refcommon:ref_broad"),
     .(contrast, variant = c(base = EV[1], p70 = EV[2], p80 = EV[3], mechanism_blinded = EV[4], ref_strict = EV[5],
                             ref_broad = EV[6], `refcommon:base` = EV[7], `refcommon:ref_strict` = EV[8],
                             `refcommon:ref_broad` = EV[9])[analysis],
       status, k, n_patients, estimate, ci_low, ci_high)],
  s3[estimand == "final_ood_pass_only", .(contrast, variant = EV[10], status, k, n_patients, estimate, ci_low, ci_high)])
# Strict reference and common-subset rows do not change the pro-rev contrasts (no reference involved); the broad
# reference does, because secretory cells leave the pro/rev strata.
ee <- ee[!(contrast %in% c("pro_vs_rev", "cycling_pro_vs_rev") & variant %in% EV[c(5, 7, 8, 9)])]
ee[, note := desc_note(status, k, n_patients)]
p_e <- rob_forest(ee, EV, "Stratum and reference definitions", base_variant = EV[1])

# ================================================================ f  subsets (ED-F)
lo <- rd("stage4", "S4_loso.tsv")[left_out == "Pelka_2021_Cell"]
FV <- c("All patients (primary)", "MSS", "MSI-H", "CNV-positive cells", "Pelka 2021 excluded")
ff <- rbind(
  s4[analysis %in% c("base", "MSI=MSS", "MSI=MSI-H", "cnv_malignant"),
     .(contrast, variant = c(base = FV[1], `MSI=MSS` = FV[2], `MSI=MSI-H` = FV[3], cnv_malignant = FV[4])[analysis],
       status, k, n_patients, estimate, ci_low, ci_high)],
  lo[, .(contrast, variant = FV[5], status = "pooled", k, n_patients, estimate, ci_low, ci_high)])
ff[, note := desc_note(status, k, n_patients)]
stopifnot(nrow(ff) == 20)
mi <- rd("stage4", "S4_msi_interaction.tsv")[study_id == "POOLED"]
p_f <- rob_forest(ff, FV, "Molecular and cohort subsets", base_variant = FV[1]) +
  labs(caption = sprintf("MSI-H − MSS interaction (pro − rev; 4 studies, %d vs %d patients): %s [%s, %s], P = %.2f",
                         mi$n_msih, mi$n_mss, fmt3(mi$diff), fmt3(mi$ci_low), fmt3(mi$ci_high), mi$p)) +
  theme(plot.caption = element_text(size = 5, hjust = 0, colour = "black"), plot.caption.position = "plot")

# ================================================================ g  CT2 vs CCAT (ED-G)
GV <- c("CytoTRACE2 (primary)", "SCENT-CCAT")
gg <- s4[analysis %in% c("base", "ccat"), .(contrast, variant = c(base = GV[1], ccat = GV[2])[analysis],
                                            status, k, n_patients, estimate, ci_low, ci_high)]
gg[, note := desc_note(status, k, n_patients)]
p_g1 <- rob_forest(gg, GV, "Potency proxy", base_variant = NULL) +
  labs(x = "Δ potency proxy (proxy units)")
m2 <- rbind(rd("stage3", "S3_M2_continuous_pooled.tsv")[estimand == "partial_lineage", .(programme, proxy = "CytoTRACE2", estimate, ci_low, ci_high, n_patients)],
            rd("stage4", "S4_M2_ccat.tsv")[estimand == "partial_lineage", .(programme, proxy = "SCENT-CCAT", estimate, ci_low, ci_high, n_patients)])
stopifnot(nrow(m2) == 4, all(m2$n_patients == 216))
m2[, proxy := factor(proxy, levels = rev(GV2 <- c("CytoTRACE2", "SCENT-CCAT")))]
p_g2 <- ggplot(m2, aes(y = proxy, colour = programme)) +
  geom_vline(xintercept = 0, linewidth = 0.25, linetype = "22", colour = MID) +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high), width = 0, linewidth = 0.4, orientation = "y",
                position = position_dodge(width = 0.5)) +
  geom_point(aes(x = estimate), size = 0.9, position = position_dodge(width = 0.5)) +
  scale_colour_manual(values = c(proCSC = SIGNAL, revCSC = REV), name = NULL) +
  scale_x_continuous(limits = c(-0.1, 0.4), breaks = c(0, 0.2, 0.4), labels = c("0", "0.2", "0.4")) +
  labs(x = "Adjusted partial ρ (95% CI)", y = NULL, title = "Continuous, n = 216") +
  theme_nat + theme(axis.ticks.y = element_blank(), axis.line.y = element_blank(), legend.position = "bottom",
                    legend.box.margin = margin(-4, 0, 0, 0))
p_g <- (p_g1 | p_g2) + plot_layout(widths = c(1, 0.45))

# ================================================================ h  eligibility and reference missingness (ED-H)
fu <- rd("stage3", "S3_M1_eligibility_funnel.tsv")[contrast %in% names(CONTRASTS)]
fu <- melt(fu[, .(contrast, `All patients` = patients_total, `With both groups` = L1_patients_with_reference_or_A,
                  `≥1 eligible sample` = L2_patients_with_eligible_sample,
                  `In studies with ≥5 patients` = L3_patients_in_qualifying_studies)],
           id.vars = "contrast", variable.name = "step", value.name = "n")
fu[, contrast := factor(CONTRASTS[contrast], levels = rev(CONTRASTS))]
fu[, step := factor(step, levels = rev(levels(step)))]
FCOL <- c("All patients" = "#E6E6E6", "With both groups" = "#BDBDBD", "≥1 eligible sample" = "#8A8A8A",
          "In studies with ≥5 patients" = SIGNAL)
p_h1 <- ggplot(fu, aes(y = contrast, x = n, fill = step)) +
  geom_col(position = position_identity(), width = 0.7) +
  geom_text(data = fu[step == "In studies with ≥5 patients"], aes(label = n), hjust = 1.15, size = 5 / .pt,
            colour = "white", family = "Arial") +
  scale_fill_manual(values = FCOL, breaks = names(FCOL), name = NULL) +
  scale_x_continuous(limits = c(0, 222), breaks = c(0, 100, 200), expand = c(0, 0)) +
  labs(x = "Patients", y = NULL, title = "Eligibility funnel (222 patients)") +
  guides(fill = guide_legend(ncol = 2)) +
  theme_nat + theme(legend.position = "bottom", legend.box.margin = margin(-4, 0, 0, -20),
                    axis.text.y = element_text(lineheight = 0.9))

d1 <- rd("stage4", "S4_D1_dropout_audit.tsv")[group %in% c("ref", "pro")]
pci <- function(s) as.numeric(strsplit(gsub("\\[|\\]", "", s), ",\\s*")[[1]])
MET <- c(log_umi = "log10 UMI", log_genes = "log10 genes", whole_score = "CytoTRACE2")
d1l <- rbindlist(lapply(names(MET), function(m) d1[, {
  ci <- pci(get(paste0(m, "_ci")))
  .(metric = m, est = get(paste0(m, "_dropped_minus_retained")), lo = ci[1], hi = ci[2],
    k = get(paste0(m, "_k")), frac = median_frac_dropped)
}, by = group]))
d1l[, metric := factor(MET[metric],
                       levels = rev(c("log10 UMI", "log10 genes", "CytoTRACE2")))]
d1l[, group := factor(sprintf("%s (median %.1f%% dropped)", c(ref = "reference", pro = "pro")[group], 100 * frac),
                      levels = sprintf("%s (median %.1f%% dropped)", c("reference", "pro"),
                                       100 * d1[match(c("ref", "pro"), group), median_frac_dropped]))]
p_h2 <- ggplot(d1l, aes(y = metric, colour = group)) +
  geom_vline(xintercept = 0, linewidth = 0.25, linetype = "22", colour = MID) +
  geom_errorbar(aes(xmin = lo, xmax = hi), width = 0, linewidth = 0.4, orientation = "y",
                position = position_dodge(width = 0.55)) +
  geom_point(aes(x = est), size = 0.9, position = position_dodge(width = 0.55)) +
  scale_colour_manual(values = setNames(c("#E3A33A", SIGNAL), levels(d1l$group)), name = NULL) +
  labs(x = "Dropped − retained cells (95% CI)", y = NULL, title = "D1: cells lost on depth matching") +
  guides(colour = guide_legend(ncol = 1)) +
  theme_nat + theme(axis.ticks.y = element_blank(), axis.line.y = element_blank(), legend.position = "bottom",
                    legend.box.margin = margin(-4, 0, 0, -20))

d3 <- rd("stage4", "S4_D3_eligibility_retention.tsv")[contrast %in% c("pro_vs_ref", "rev_vs_ref")]
d3 <- melt(d3[, .(contrast, low = lost_frac_rev_low, mid = lost_frac_rev_mid, high = lost_frac_rev_high, lost, eligible_base)],
           id.vars = c("contrast", "lost", "eligible_base"), variable.name = "tertile", value.name = "frac")
d3[, contrast := factor(sprintf("%s (%d/%d lost)", CONTRASTS[contrast], lost, eligible_base))]
p_h3 <- ggplot(d3, aes(x = tertile, y = 100 * frac, fill = contrast)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.75) +
  scale_fill_manual(values = c(INK, "#9A9A9A"), name = NULL) +
  scale_y_continuous(limits = c(0, 30), breaks = c(0, 10, 20, 30), expand = c(0, 0)) +
  labs(x = "Patient revCSC tertile", y = "Patients lost (%)", title = "D3: eligibility loss, intersection") +
  guides(fill = guide_legend(ncol = 1)) +
  theme_nat + theme(legend.position = "bottom", legend.box.margin = margin(-4, 0, 0, -20))
p_h <- (p_h1 | p_h2 | p_h3) + plot_layout(widths = c(1, 0.8, 0.55))

# ================================================================ assemble
tag <- function(p) wrap_elements(full = p)
fig <- wrap_plots(
  A = tag(p_a), B = tag(p_b), C = tag(p_c), D = tag(p_d), E = tag(p_e), F = tag(p_f), G = tag(p_g), H = tag(p_h),
  design = "AB\nCC\nDE\nFG\nHH", heights = c(1.2, 0.95, 1.05, 0.8, 0.75)) +
  plot_annotation(tag_levels = "a") &
  theme(plot.tag = element_text(size = 8, face = "bold", family = "Arial"),
        plot.background = element_rect(fill = "white", colour = NA))

w <- 183 / 25.4; h <- 240 / 25.4
out <- file.path(here, "fig1c_ed")
svglite::svglite(paste0(out, ".svg"), width = w, height = h); print(fig); invisible(dev.off())
grDevices::cairo_pdf(paste0(out, ".pdf"), width = w, height = h, family = "Arial"); print(fig); invisible(dev.off())
ragg::agg_tiff(paste0(out, ".tiff"), width = w, height = h, units = "in", res = 600, compression = "lzw")
print(fig); invisible(dev.off())
ragg::agg_png(paste0(out, "_preview.png"), width = w, height = h, units = "in", res = 200); print(fig); invisible(dev.off())

# ---------------------------------------------------------------- source data (one CSV per panel)
fwrite(rbind(ver[, .(table = "audit_verdict", study, item = class, value = as.character(verdict))],
             comp[, .(table = "composition_fraction", study, item = cat, value = sprintf("%.4f", frac))],
             ood[, .(table = "ood_fail_fraction", study, item = "frac_ood_fail", value = sprintf("%.3f", frac_ood_fail))]),
       paste0(out, "_source_a.csv"))
fwrite(rbind(rw[, .(table = "raw_density", pro_lo, rev_lo, bin_width, stratum, value = patient_weight)],
             tm[, .(table = "mb_transition", pro_lo = NA, rev_lo = NA, bin_width = NA,
                    stratum = paste(full, "->", mb), value = n)],
             sz[, .(table = "stratum_size", pro_lo = NA, rev_lo = NA, bin_width = NA,
                    stratum = paste(threshold, stratum), value = n_cells)]), paste0(out, "_source_b.csv"))
fwrite(rbind(bs[, .(row = "study", contrast, study, n_patients, estimate = mean, ci_low = lo, ci_high = hi,
                    pi_low = NA, pi_high = NA, I2 = NA, tau2 = NA, loso_min = NA, loso_max = NA)],
             pl[, .(row = "pooled", contrast, study = "Pooled", n_patients, estimate, ci_low, ci_high, pi_low, pi_high,
                    I2, tau2, loso_min, loso_max)]), paste0(out, "_source_c.csv"))
for (x in list(list("d", dd), list("e", ee), list("f", ff), list("g", gg)))
  fwrite(x[[2]][, .(contrast, variant, status, k, n_patients, estimate, ci_low, ci_high)],
         paste0(out, "_source_", x[[1]], ".csv"))
fwrite(m2, paste0(out, "_source_g_m2.csv"))
fwrite(rbind(fu[, .(table = "funnel", contrast, item = step, value = n, lo = NA, hi = NA)],
             d1l[, .(table = "D1_dropped_minus_retained", contrast = group, item = metric, value = est, lo, hi)],
             d3[, .(table = "D3_lost_fraction", contrast, item = tertile, value = frac, lo = NA, hi = NA)]),
       paste0(out, "_source_h.csv"))
cat("done\n")
