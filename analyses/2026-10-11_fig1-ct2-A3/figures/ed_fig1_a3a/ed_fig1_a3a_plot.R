#!/usr/bin/env Rscript
# Extended Data companion to the Fig. 1 A3a panel (nature-figure, R). Frozen contract A3a v0.2; final review 2026-10-11.
#
# Figure contract
# - Claim: the programme-specific pattern (proCSC/Lgr5CSC retained; revival/YAP/oncofetal adjustment-sensitive)
#   is consistent across cohorts, cell subsets, depth perturbation and a second potency algorithm; TNFRSF12A
#   tracks revival/YAP/oncofetal programmes (after removing self-inclusion); macrophage TNFSF12 shows no
#   detectable sample-level association with epithelial Extended CIOC; proCSC-revCSC co-activation is heterogeneous.
# - Panels: a cohort-level estimates (CT2, CCAT; before/after adjustment); b robustness grid;
#   c MSI strata; d TNFRSF12A (P2); e macrophage TNFSF12 (P3); f proCSC-revCSC co-activation.
# - Size: 183 x 200 mm; text 5-7 pt; panel letters 8 pt bold.
# Inputs: ../../tables/{a3a,a3a_ccat,a3a_posthoc}/
suppressPackageStartupMessages({ library(ggplot2); library(data.table); library(patchwork) })

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)])))
tab <- file.path(here, "..", "..", "tables")
ct <- fread(file.path(tab, "a3a", "A3a_pooled.tsv")); cts <- fread(file.path(tab, "a3a", "A3a_study.tsv"))
cc <- fread(file.path(tab, "a3a_ccat", "A3a_ccat_pooled.tsv")); ccs <- fread(file.path(tab, "a3a_ccat", "A3a_ccat_study.tsv"))
ph <- fread(file.path(tab, "a3a_posthoc", "A3a_posthoc_pooled.tsv")); phs <- fread(file.path(tab, "a3a_posthoc", "A3a_posthoc_study.tsv"))
p3 <- fread(file.path(tab, "a3a", "P3_study.tsv")); p3p <- fread(file.path(tab, "a3a", "P3_pooled.tsv"))
coe <- fread(file.path(tab, "a3a_posthoc", "coactivation_expected_study.tsv"))

P1 <- c(proCSC = "proCSC", Lgr5CSC = "Lgr5CSC", ExtCIOC = "Extended CIOC", revCSC = "revCSC", YAPcore = "YAP core")
ALL <- c(P1, ECOS38 = "ECOS-38", YAPfetal = "YAP fetal effectors", Placenta = "Placenta trophoblast")
COL <- c("CytoTRACE2" = "#0F4D92", "SCENT-CCAT" = "#42949E")
STUDY <- function(s) sub("^([A-Za-z]+)_([0-9]{4}).*$", "\\1 \\2", sub("^MUI_Innsbruck$", "MUI", s))

theme_nat <- theme_classic(base_size = 6, base_family = "Arial") +
  theme(axis.line = element_line(linewidth = 0.3, colour = "#272727"),
        axis.ticks = element_line(linewidth = 0.3, colour = "#272727"), axis.ticks.length = unit(0.8, "mm"),
        axis.text = element_text(size = 5.5, colour = "black"), axis.title = element_text(size = 6, colour = "black"),
        strip.background = element_blank(), strip.text = element_text(size = 6, colour = "black", margin = margin(b = 1.5)),
        legend.title = element_blank(), legend.text = element_text(size = 5.5), legend.key.size = unit(2.2, "mm"),
        legend.margin = margin(0, 0, 0, 0), panel.grid = element_blank(), plot.margin = margin(3, 3, 3, 3),
        plot.title = element_text(size = 6, colour = "black", face = "plain", margin = margin(b = 2)))
zero <- geom_vline(xintercept = 0, linewidth = 0.3, linetype = "22", colour = "#767676")
EST <- c("Before adjustment", "After adjustment")

# ---- a: cohort-level estimates, CT2 and CCAT, before/after adjustment ----
sa <- rbind(cts[analysis %in% c("ct2_final|unadjusted|ge100", "ct2_final|adjusted|ge100") & programme %in% names(P1)][, proxy := "CytoTRACE2"],
            ccs[analysis %in% c("ccat|unadjusted|ge100|primary", "ccat|adjusted|ge100|primary") & programme %in% names(P1)][, proxy := "SCENT-CCAT"],
            fill = TRUE)
sa[, est := factor(ifelse(estimand == "unadjusted", EST[1], EST[2]), levels = EST)]
pa <- rbind(ct[analysis %in% c("ct2_final|unadjusted|ge100", "ct2_final|adjusted|ge100") & programme %in% names(P1)][, proxy := "CytoTRACE2"],
            cc[analysis %in% c("ccat|unadjusted|ge100|primary", "ccat|adjusted|ge100|primary") & programme %in% names(P1)][, proxy := "SCENT-CCAT"],
            fill = TRUE)
pa[, est := factor(ifelse(estimand == "unadjusted", EST[1], EST[2]), levels = EST)]
for (x in list(sa, pa)) {
  x[, prog := factor(P1[programme], levels = rev(P1))]
  x[, proxy := factor(proxy, levels = names(COL))]
}
set.seed(1)
sa[, yj := as.numeric(prog) + runif(.N, -0.22, 0.22)]
pA <- ggplot() + zero +
  geom_point(data = sa, aes(x = rho, y = yj), colour = "#767676", size = 0.55, alpha = 0.7, stroke = 0) +
  geom_errorbar(data = pa, aes(xmin = ci_low, xmax = ci_high, y = as.numeric(prog), colour = proxy),
                width = 0, linewidth = 0.5, orientation = "y") +
  geom_point(data = pa, aes(x = rho, y = as.numeric(prog), colour = proxy), shape = 18, size = 2.1) +
  facet_grid(proxy ~ est) + scale_colour_manual(values = COL, guide = "none") +
  scale_y_continuous(breaks = 1:5, labels = rev(P1), expand = expansion(add = 0.5)) +
  scale_x_continuous(limits = c(-0.45, 0.95), breaks = c(-0.25, 0, 0.25, 0.5, 0.75)) +
  labs(x = "Spearman ρ with predicted potency", y = NULL,
       title = "Cohort estimates (grey; 13 cohorts) and pooled ρ with 95% CI (diamond)") +
  theme_nat + theme(axis.ticks.y = element_blank(), axis.line.y = element_blank(),
                    strip.text.y = element_text(angle = 0, hjust = 0), panel.spacing = unit(2.5, "mm"))

# ---- b: robustness grid (pooled rho; white = 95% CI includes 0) ----
rows <- list(
  c("ct2_final|unadjusted|ge100", "CT2 primary, before adjustment", "ct"),
  c("ct2_final|adjusted|ge100", "CT2 primary, after adjustment", "ct"),
  c("ct2_raw|unadjusted|ge100", "CT2 raw model score, before", "ct"),
  c("ct2_raw|adjusted|ge100", "CT2 raw model score, after", "ct"),
  c("ds_both|unadjusted|ge100", "CT2 depth-matched, before", "ct"),
  c("ds_both|adjusted|ge100", "CT2 depth-matched, after", "ct"),
  c("ct2_final|unadjusted|ge50", "CT2, samples with ≥50 cells", "ct"),
  c("ct2_final|unadjusted|ge100|F1clean", "CT2 F1-clean, before", "ct"),
  c("ct2_final|adjusted|ge100|F1clean", "CT2 F1-clean, after", "ct"),
  c("ct2_final|unadjusted|ge100|noncycling", "CT2 non-cycling, before", "ct"),
  c("ct2_final|adjusted|ge100|noncycling", "CT2 non-cycling, after", "ct"),
  c("ct2_final|unadjusted|ge100|malignant", "CT2 malignant subset*, before", "ct"),
  c("ct2_final|adjusted|ge100|malignant", "CT2 malignant subset*, after", "ct"),
  c("ct2_final|unadjusted|ge100|noKhaliq", "CT2 excluding Khaliq, before", "ct"),
  c("ct2_final|adjusted|ge100|noKhaliq", "CT2 excluding Khaliq, after", "ct"),
  c("ccat|unadjusted|ge100|primary", "CCAT, before adjustment", "cc"),
  c("ccat|adjusted|ge100|primary", "CCAT, after adjustment", "cc"),
  c("ccat|unadjusted|ge100|malignant", "CCAT malignant subset*, before", "cc"),
  c("ccat|adjusted|ge100|malignant", "CCAT malignant subset*, after", "cc"))
gb <- rbindlist(lapply(rows, function(r) {
  src <- if (r[3] == "ct") ct else cc
  x <- src[analysis == r[1] & programme %in% names(ALL), .(programme, rho, ci_low, ci_high, k)]
  x[, row := r[2]]
}))
gb <- gb[!is.na(rho)]
gb[, sig := ci_low > 0 | ci_high < 0]
gb[, row := factor(row, levels = rev(vapply(rows, `[`, "", 2)))]
gb[, col := factor(ALL[programme], levels = ALL)]
gb[, fillv := ifelse(sig, rho, NA_real_)]
pB <- ggplot(gb, aes(x = col, y = row)) +
  geom_tile(aes(fill = fillv), colour = "white", linewidth = 0.4) +
  geom_text(aes(label = sprintf("%.2f", rho)), size = 5 / .pt, family = "Arial", colour = "black") +
  geom_vline(xintercept = 5.5, linewidth = 0.3, colour = "#272727") +
  scale_fill_gradient2(low = "#B64342", mid = "#F7F7F7", high = "#0F4D92", midpoint = 0, limits = c(-0.8, 0.8),
                       na.value = "white", name = "ρ", breaks = c(-0.5, 0, 0.5)) +
  scale_x_discrete(position = "top", expand = c(0, 0)) + scale_y_discrete(expand = c(0, 0)) +
  labs(x = NULL, y = NULL, title = "Pooled ρ (white cell: 95% CI includes 0)") +
  theme_nat + theme(axis.line = element_blank(), axis.ticks = element_blank(),
                    axis.text.x.top = element_text(angle = 40, hjust = 0, vjust = 0),
                    legend.position = "right", legend.key.width = unit(1.6, "mm"), legend.key.height = unit(5, "mm"),
                    legend.title = element_text(size = 5.5))

# ---- c: MSI strata (CT2 primary, before adjustment) ----
gc <- ct[analysis %in% c("ct2_final|unadjusted|ge100|MSI=MSS", "ct2_final|unadjusted|ge100|MSI=MSI-H") & programme %in% names(P1)]
gc[, grp := ifelse(grepl("MSS", analysis), sprintf("MSS (%d patients, %d cohorts)", n_patients[1], k[1]), NA_character_), by = analysis]
gc[grepl("MSI-H", analysis), grp := sprintf("MSI-H (%d patients, %d cohorts)", n_patients, k)]
gc[, prog := factor(P1[programme], levels = rev(P1))]
gc[, y := as.numeric(prog) + ifelse(grepl("MSS", analysis), 0.15, -0.15)]
pC <- ggplot(gc, aes(x = rho, y = y, shape = grp)) + zero +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high), width = 0, linewidth = 0.45, colour = "#0F4D92", orientation = "y") +
  geom_point(size = 1.4, colour = "#0F4D92", fill = "white", stroke = 0.55) +
  scale_shape_manual(values = c(16, 21)) +
  scale_y_continuous(breaks = 1:5, labels = rev(P1), expand = expansion(add = 0.5)) +
  scale_x_continuous(limits = c(-0.2, 0.8), breaks = c(0, 0.25, 0.5, 0.75)) +
  labs(x = "Spearman ρ with CytoTRACE2 (before adjustment)", y = NULL, title = "MSI status") +
  guides(shape = guide_legend(ncol = 1)) +
  theme_nat + theme(axis.ticks.y = element_blank(), axis.line.y = element_blank(), legend.position = "bottom",
                    legend.box.margin = margin(-4, 0, 0, -30))

# ---- d: TNFRSF12A (P2), after adjustment ----
d1 <- ct[analysis == "P2desc|adjusted" & proxy %in% paste0("prog:", names(ALL))]
d1[, lab := ALL[sub("prog:", "", proxy)]]
d2 <- ph[test == "TNFRSF12A_vs_revCSC_noTN" & estimand == "adjusted"][, lab := "revCSC without TNFRSF12A†"]
d3 <- ct[analysis == "P2|adjusted"][, lab := "CytoTRACE2"]
d4 <- cc[analysis == "ccat|adjusted|ge100|primary" & programme == "TNFRSF12A_cpm"][, lab := "SCENT-CCAT"]
gd <- rbind(d1[, .(lab, rho, ci_low, ci_high, kind = "Programme")], d2[, .(lab, rho, ci_low, ci_high, kind = "Programme")],
            d3[, .(lab, rho, ci_low, ci_high, kind = "Potency estimate")], d4[, .(lab, rho, ci_low, ci_high, kind = "Potency estimate")])
ordr <- c(gd[kind == "Programme"][order(rho)]$lab, "CytoTRACE2", "SCENT-CCAT")
gd[, lab := factor(lab, levels = rev(unique(c("CytoTRACE2", "SCENT-CCAT", rev(gd[kind == "Programme"][order(rho)]$lab)))))]
gd[, colr := ifelse(kind == "Programme", "#272727", ifelse(lab == "SCENT-CCAT", COL[2], COL[1]))]
pD <- ggplot(gd, aes(x = rho, y = lab)) + zero +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high, colour = colr), width = 0, linewidth = 0.45, orientation = "y") +
  geom_point(aes(colour = colr), size = 1.3) + scale_colour_identity() +
  scale_x_continuous(limits = c(-0.1, 0.4), breaks = c(0, 0.2, 0.4)) +
  labs(x = "Adjusted Spearman ρ with TNFRSF12A\n(8 cohorts, 140 patients)", y = NULL, title = "TNFRSF12A") +
  theme_nat + theme(axis.ticks.y = element_blank(), axis.line.y = element_blank())

# ---- e: macrophage TNFSF12 vs epithelial Extended CIOC (P3) ----
e1 <- p3[, .(study = STUDY(study_id), rho, n = n_samples, version = "All samples")]
e2 <- phs[analysis == "P3_epi_ge100_patients", .(study = STUDY(study_id), rho, n = n_units, version = "Patient level")]
ge <- rbind(e1, e2)
pool_e <- rbind(
  data.table(version = "All samples", rho = p3p$rho, ci_low = p3p$ci_low, ci_high = p3p$ci_high),
  ph[analysis == "P3_epi_ge100_patients", .(version = "Patient level", rho, ci_low, ci_high)])
lv <- rev(sort(unique(ge$study)))
ge[, study := factor(study, levels = c("Pooled", lv))]
pool_e[, study := factor("Pooled", levels = levels(ge$study))]
pE <- ggplot(ge, aes(x = rho, y = study, shape = version)) + zero +
  geom_point(aes(size = n), colour = "#767676", fill = "white", stroke = 0.45,
             position = position_dodge(width = 0.55)) +
  geom_errorbar(data = pool_e, aes(xmin = ci_low, xmax = ci_high, group = version), width = 0, linewidth = 0.45,
                colour = "#0F4D92", orientation = "y", position = position_dodge(width = 0.55)) +
  geom_point(data = pool_e, colour = "#0F4D92", fill = "white", size = 1.5, stroke = 0.55,
             position = position_dodge(width = 0.55)) +
  scale_shape_manual(values = c("All samples" = 16, "Patient level" = 21)) +
  scale_size_continuous(range = c(0.5, 1.8), guide = "none") +
  scale_x_continuous(limits = c(-1, 1), breaks = c(-1, -0.5, 0, 0.5, 1)) +
  labs(x = "Spearman ρ, macrophage TNFSF12 vs\nepithelial Extended CIOC", y = NULL, title = "Macrophage TNFSF12") +
  guides(shape = guide_legend(ncol = 1)) +
  theme_nat + theme(axis.ticks.y = element_blank(), axis.line.y = element_blank(), legend.position = "bottom",
                    legend.box.margin = margin(-4, 0, 0, -20))

# ---- f: proCSC-revCSC co-activation relative to independence ----
gf <- coe[, .(study = STUDY(study_id), ratio = obs_over_exp_median, samples)]
gf[, study := factor(study, levels = gf[order(ratio)]$study)]
pF <- ggplot(gf, aes(x = ratio, y = study)) +
  geom_vline(xintercept = 1, linewidth = 0.3, linetype = "22", colour = "#767676") +
  geom_segment(aes(x = 1, xend = ratio, yend = study), linewidth = 0.4, colour = "#CFCECE") +
  geom_point(aes(size = samples), colour = "#0F4D92") +
  scale_size_continuous(range = c(0.6, 2), guide = "none") +
  scale_x_continuous(limits = c(0.5, 2), breaks = c(0.5, 1, 1.5, 2)) +
  labs(x = "Observed / expected co-high share\n(median of samples)", y = NULL, title = "proCSC–revCSC co-activation") +
  theme_nat + theme(axis.ticks.y = element_blank(), axis.line.y = element_blank())

# ---- assemble ----
design <- "
AAAAAA
BBBBCC
DDEEFF
"
fig <- pA + pB + pC + pD + pE + pF +
  plot_layout(design = design, heights = c(0.95, 1.15, 0.95), widths = rep(1, 6)) +
  plot_annotation(tag_levels = "a") &
  theme(plot.tag = element_text(size = 8, face = "bold", family = "Arial"), plot.tag.position = c(0, 1))

w <- 183 / 25.4; h <- 205 / 25.4
out <- file.path(here, "ed_fig1_a3a")
svglite::svglite(paste0(out, ".svg"), width = w, height = h); print(fig); invisible(dev.off())
grDevices::cairo_pdf(paste0(out, ".pdf"), width = w, height = h, family = "Arial"); print(fig); invisible(dev.off())
ragg::agg_tiff(paste0(out, ".tiff"), width = w, height = h, units = "in", res = 600, compression = "lzw"); print(fig); invisible(dev.off())
ragg::agg_png(paste0(out, "_preview.png"), width = w, height = h, units = "in", res = 200); print(fig); invisible(dev.off())

fwrite(rbind(sa[, .(proxy, est, programme, study_id, rho, rho_ci_low, rho_ci_high, n_patients)][, level := "cohort"],
             pa[, .(proxy, est, programme, study_id = "pooled", rho, rho_ci_low = ci_low, rho_ci_high = ci_high, n_patients)][, level := "pooled"]),
       paste0(out, "_source_a.csv"))
fwrite(gb[, .(analysis_row = row, programme, rho, ci_low, ci_high, k, ci_excludes_0 = sig)], paste0(out, "_source_b.csv"))
fwrite(gc[, .(stratum = grp, programme, rho, ci_low, ci_high, k, n_patients)], paste0(out, "_source_c.csv"))
fwrite(gd[, .(label = lab, kind, rho, ci_low, ci_high)], paste0(out, "_source_d.csv"))
fwrite(rbind(ge[, .(version, study, rho, ci_low = NA_real_, ci_high = NA_real_, n_units = n)],
             pool_e[, .(version, study, rho, ci_low, ci_high, n_units = NA_integer_)]),
       paste0(out, "_source_e.csv"))
fwrite(gf, paste0(out, "_source_f.csv"))
cat("done\n")
