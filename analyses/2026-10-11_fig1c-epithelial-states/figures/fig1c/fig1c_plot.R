#!/usr/bin/env Rscript
# Fig. 1c main panel (nature-figure, R). Contract v0.3a; Stage 4 approved and claim frozen 2026-10-11
# (docs/Fig1c_stage4_final_review_20261011.md).
#
# Figure contract
# - Claim: distinguishable proliferative/stem-associated (proCSC) and revival-oncofetal (revCSC) epithelial
#   programmes display differential associations with CytoTRACE2-predicted developmental potency in
#   treatment-naive primary CRC.
# - Role: discovery/characterisation (epithelial-state transition between Fig. 1b and the TWEAK-Fn14 figures).
# - Archetype: asymmetric mixed quantitative composite; hero = c-ii (pro-rev direct contrast).
# - c-i  programme architecture: patient-equal-weighted density of within-sample percentile ranks of proCSC and
#        revCSC (all 285,141 labelled tumour-specimen epithelial cells, 222 patients, 13 studies); p75 lines are
#        the frozen within-sample strata cut-offs; bars = annotation composition of each operational stratum.
# - c-ii three pre-specified within-patient CT2 contrasts (Holm family) + Cycling-restricted planned sensitivity;
#        group-median difference, sample -> patient median -> study mean -> REML + Hartung-Knapp, 95% CI.
# - c-iii secondary continuous model (M2): within-sample partial Spearman rho of CT2 with each programme adjusted
#        for the other programme, log UMI, log genes, mito fraction, S, G2M and lineage/annotation status.
# - Size: 183 mm x 62 mm (double column); text 5-7 pt; panel letter "c" added at Figure 1 assembly.
# Inputs: ../../tables/figure/fig1c_ci_density.tsv, ../../tables/stage1_v03a/strata75_lineage_composition.tsv,
#         ../../tables/stage3/S3_contrasts_pooled.tsv, ../../tables/stage3/S3_contrasts_by_study.tsv,
#         ../../tables/stage3/S3_M2_continuous_pooled.tsv
suppressPackageStartupMessages({ library(ggplot2); library(data.table); library(patchwork) })

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)])))
tab <- file.path(here, "..", "..", "tables")

INK <- "#272727"; MID <- "#767676"; LIGHT <- "#CFCECE"; SIGNAL <- "#0F4D92"
theme_nat <- theme_classic(base_size = 6, base_family = "Arial") +
  theme(axis.line = element_line(linewidth = 0.3, colour = INK),
        axis.ticks = element_line(linewidth = 0.3, colour = INK),
        axis.ticks.length = unit(0.8, "mm"),
        axis.text = element_text(size = 6, colour = "black"),
        axis.title = element_text(size = 6, colour = "black"),
        plot.title = element_text(size = 6, colour = "black", face = "plain", margin = margin(b = 1.5)),
        legend.title = element_text(size = 5.5), legend.text = element_text(size = 5.5),
        legend.key.size = unit(2.2, "mm"), legend.margin = margin(0, 0, 0, 0),
        plot.margin = margin(2, 3, 2, 2), panel.grid = element_blank())

# ---------------------------------------------------------------- c-i density
g <- fread(file.path(tab, "figure", "fig1c_ci_density.tsv"))
stopifnot(nrow(g) == 1600, abs(sum(g$patient_weight) - 1) < 1e-6)
g[, fold := patient_weight / (1 / 1600)]
g[, l2 := pmax(pmin(log2(pmax(fold, 1e-6)), 2), -2)]
q <- data.frame(x = c(87.5, 37.5, 87.5, 37.5), y = c(37.5, 87.5, 87.5, 37.5),
                lab = c("pro-\ndominant", "rev-dominant", "hybrid-\nhigh", "neither-high"))
p_i <- ggplot(g) +
  geom_rect(aes(xmin = pro_pct_lo, xmax = pro_pct_hi, ymin = rev_pct_lo, ymax = rev_pct_hi, fill = l2), colour = NA) +
  geom_vline(xintercept = 75, linewidth = 0.3, linetype = "22", colour = INK) +
  geom_hline(yintercept = 75, linewidth = 0.3, linetype = "22", colour = INK) +
  geom_label(data = q, aes(x = x, y = y, label = lab), size = 5 / .pt, family = "Arial", colour = "black",
             fill = "white", linewidth = 0, label.padding = unit(0.4, "mm"), alpha = 0.85, lineheight = 0.85) +
  scale_fill_gradient2(low = "#3775BA", mid = "white", high = "#B64342", midpoint = 0, limits = c(-2, 2),
                       breaks = c(-2, -1, 0, 1, 2), labels = c("≤¼", "½", "1", "2", "≥4"),
                       name = "Cell density\n(fold vs uniform)") +
  scale_x_continuous(limits = c(0, 100), breaks = c(0, 25, 50, 75, 100), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0, 100), breaks = c(0, 25, 50, 75, 100), expand = c(0, 0)) +
  coord_fixed() +
  labs(x = "proCSC score (within-sample percentile)", y = "revCSC score\n(within-sample percentile)",
       title = "285,141 cells · 222 patients · 13 studies") +
  theme_nat +
  theme(legend.position = "right", legend.key.width = unit(1.6, "mm"), legend.key.height = unit(4.5, "mm"),
        legend.box.margin = margin(0, 0, 0, -4))

# ---------------------------------------------------------------- c-i composition
cm <- fread(file.path(tab, "stage1_v03a", "strata75_lineage_composition.tsv"))
cm <- melt(cm, id.vars = "stratum", variable.name = "lineage", value.name = "n")
cat_of <- c("Cycling Stem/TA" = "Cycling Stem/TA", "Secretory differentiated-like" = "Secretory",
            "Transitional stem/secretory" = "Transitional/rare (not audited)", "Transitional secretory/absorptive" = "Transitional/rare (not audited)",
            "Rare lineages" = "Transitional/rare (not audited)", "lineage-transfer-unverified" = "Stem/TA-like (unverified)",
            "lineage-unresolved" = "Unresolved")
cm[, cat := factor(cat_of[as.character(lineage)], levels = rev(c("Cycling Stem/TA", "Secretory", "Transitional/rare (not audited)",
                                                                  "Stem/TA-like (unverified)", "Unresolved")))]
cm <- cm[, .(n = sum(n)), by = .(stratum, cat)]
cm[, frac := n / sum(n), by = stratum]
tot <- cm[, .(n = sum(n)), by = stratum]
stopifnot(tot[stratum == "pro_dominant", n] == 50539, tot[stratum == "rev_dominant", n] == 46048)
SL <- c(pro_dominant = "pro", rev_dominant = "rev", hybrid_high = "hybrid")
cm <- cm[stratum %in% names(SL)]
tot <- tot[stratum %in% names(SL)]
SL <- setNames(paste0(SL, "\n", sprintf("%.1fk", tot$n[match(names(SL), tot$stratum)] / 1000)), names(SL))
cm[, st := factor(SL[stratum], levels = SL)]
CATCOL <- c("Cycling Stem/TA" = "#0F4D92", "Secretory" = "#42949E", "Transitional/rare (not audited)" = "#9FC3D6",
            "Stem/TA-like (unverified)" = "#9A9A9A", "Unresolved" = "#DDDDDD")
p_i2 <- ggplot(cm, aes(x = st, y = frac, fill = cat)) +
  geom_col(width = 0.78, colour = "white", linewidth = 0.15) +
  scale_fill_manual(values = CATCOL, breaks = rev(levels(cm$cat)), name = NULL) +
  scale_y_continuous(limits = c(0, 1), breaks = c(0, 0.5, 1), labels = c("0", "50", "100"), expand = c(0, 0)) +
  labs(x = NULL, y = "Cells in stratum (%)") +
  theme_nat +
  labs(title = "Stratum composition") +
  theme(legend.position = "right", legend.key.size = unit(1.8, "mm"), legend.text = element_text(size = 5),
        legend.box.margin = margin(0, 0, 0, -6), axis.text.x = element_text(size = 5, lineheight = 0.85))

# ---------------------------------------------------------------- c-ii contrasts
pc <- fread(file.path(tab, "stage3", "S3_contrasts_pooled.tsv"))
CL <- c(pro_vs_ref = "pro − reference", rev_vs_ref = "rev − reference",
        pro_vs_rev = "pro − rev", cycling_pro_vs_rev = "pro − rev (Cycling Stem/TA)")
d <- pc[estimand == "final" & contrast %in% names(CL),
        .(contrast, family, k, n_patients, estimate, ci_low, ci_high, pi_low, pi_high, p, p_adj, I2, studies_same_sign)]
stopifnot(nrow(d) == 4)
d[, lab := CL[contrast]]
d[, y := c(pro_vs_ref = 4, rev_vs_ref = 3, pro_vs_rev = 2, cycling_pro_vs_rev = 0.8)[contrast]]
d[, role := ifelse(contrast == "pro_vs_rev", "hero", ifelse(family == "primary_holm", "primary", "sensitivity"))]
fmtp <- function(p) ifelse(p < 0.001, sprintf("%.4f", p), sprintf("%.3f", p))
d[, ann := ifelse(family == "primary_holm",
                  sprintf("n = %d; %d/%d studies > 0\nHolm P = %s", n_patients, studies_same_sign, k, fmtp(p_adj)),
                  sprintf("n = %d; %d/%d studies > 0\nplanned sensitivity", n_patients, studies_same_sign, k))]
d[, ylab := paste0(lab, "\n", ann)]
ROLECOL <- c(hero = SIGNAL, primary = INK, sensitivity = MID)
p_ii <- ggplot(d, aes(y = y)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = 1.55, ymax = 2.45, fill = "#EEF2F8", colour = NA) +
  geom_vline(xintercept = 0, linewidth = 0.3, linetype = "22", colour = MID) +
  geom_hline(yintercept = 1.4, linewidth = 0.25, colour = LIGHT) +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high, colour = role), width = 0, linewidth = 0.5, orientation = "y") +
  geom_point(aes(x = estimate, colour = role, shape = role), size = 1.6, fill = "white", stroke = 0.6) +
  scale_colour_manual(values = ROLECOL, guide = "none") +
  scale_shape_manual(values = c(hero = 16, primary = 16, sensitivity = 21), guide = "none") +
  scale_x_continuous(limits = c(-0.04, 0.26), breaks = c(0, 0.1, 0.2), labels = c("0", "0.1", "0.2"), expand = c(0, 0)) +
  scale_y_continuous(breaks = d$y, labels = d$ylab, limits = c(0.3, 4.5), expand = c(0, 0)) +
  labs(x = "Δ predicted potency\n(CytoTRACE2; 95% CI)", y = NULL,
       title = "Within-patient contrasts") +
  coord_cartesian(clip = "off") +
  theme_nat +
  theme(axis.text.y = element_text(size = 5.3, lineheight = 0.95, colour = "black"), axis.ticks.y = element_blank(),
        axis.line.y = element_blank())

# ---------------------------------------------------------------- c-iii M2 inset
m2 <- fread(file.path(tab, "stage3", "S3_M2_continuous_pooled.tsv"))
m <- m2[estimand == "partial_lineage", .(programme, estimate, ci_low, ci_high, k, n_patients)]
stopifnot(nrow(m) == 2, all(m$n_patients == 216), all(m$k == 13))
m[, y := ifelse(programme == "proCSC", 2, 1)]
PCOL <- c(proCSC = SIGNAL, revCSC = "#9A4D8E")
p_iii <- ggplot(m, aes(y = y, colour = programme)) +
  geom_vline(xintercept = 0, linewidth = 0.3, linetype = "22", colour = MID) +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high), width = 0, linewidth = 0.5, orientation = "y") +
  geom_point(aes(x = estimate), size = 1.6) +
  scale_colour_manual(values = PCOL, guide = "none") +
  scale_x_continuous(limits = c(-0.1, 0.3), breaks = c(0, 0.2), labels = c("0", "0.2"),
                     expand = c(0, 0)) +
  scale_y_continuous(breaks = c(2, 1), labels = c("proCSC", "revCSC"), limits = c(0.4, 2.6), expand = c(0, 0)) +
  labs(x = "Adjusted partial ρ\n(95% CI)", y = NULL,
       title = "Continuous\nmodel, n = 216") +
  coord_cartesian(clip = "off") +
  theme_nat +
  theme(axis.ticks.y = element_blank(), axis.line.y = element_blank(), plot.title = element_text(lineheight = 0.9),
        plot.margin = margin(2, 4, 2, 0))

# ---------------------------------------------------------------- assemble
fig <- (p_i | p_i2 | p_ii | p_iii) +
  plot_layout(widths = c(1.0, 0.50, 0.85, 0.42)) &
  theme(plot.background = element_rect(fill = "white", colour = NA))

w <- 183 / 25.4; h <- 64 / 25.4
out <- file.path(here, "fig1c")
svglite::svglite(paste0(out, ".svg"), width = w, height = h); print(fig); invisible(dev.off())
grDevices::cairo_pdf(paste0(out, ".pdf"), width = w, height = h, family = "Arial"); print(fig); invisible(dev.off())
ragg::agg_tiff(paste0(out, ".tiff"), width = w, height = h, units = "in", res = 600, compression = "lzw")
print(fig); invisible(dev.off())
ragg::agg_png(paste0(out, "_preview.png"), width = w, height = h, units = "in", res = 300); print(fig); invisible(dev.off())

# ---------------------------------------------------------------- source data
fwrite(g[, .(subpanel = "c-i density", pro_pct_lo, pro_pct_hi, rev_pct_lo, rev_pct_hi, patient_weight,
             fold_vs_uniform = fold)], paste0(out, "_source_ci_density.csv"))
fwrite(cm[, .(subpanel = "c-i composition", stratum, category = cat, n_cells = n, fraction = frac)],
       paste0(out, "_source_ci_composition.csv"))
fwrite(d[, .(subpanel = "c-ii", contrast, family, estimate, ci_low, ci_high, pi_low, pi_high, p, p_holm = p_adj, I2,
             k_studies = k, n_patients, studies_same_sign)], paste0(out, "_source_cii.csv"))
fwrite(m[, .(subpanel = "c-iii", programme, partial_rho = estimate, ci_low, ci_high, k_studies = k, n_patients)],
       paste0(out, "_source_ciii.csv"))
cat("done\n")
