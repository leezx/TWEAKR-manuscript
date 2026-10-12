#!/usr/bin/env Rscript
# Extended Data for Fig. 1 A3b (nature-figure, R). Frozen contract A3b v0.3; Stage S FINAL APPROVED 2026-10-12
# (docs/A3b_stageS_final_approval_20261012.md); corrected tables at commit 7a2ecfc.
#
# Figure contract
# - Claim: paired tumour-specimen epithelium shows consistently positive but heterogeneous differences in
#   CytoTRACE2-predicted potential vs adjacent-normal epithelium, without conclusive pooled evidence after depth
#   matching; proCSC, revCSC and Extended CIOC are higher in tumour-specimen epithelium (YAP core not); exploratory
#   neoadjuvant cohorts show no statistically supported depth-matched change. Tissue context only.
# - Panels: a E1 forest (patients, studies, pooled CI + PI) with mandatory sensitivities; b programme differences
#   (BH-adjusted P); c E1-L classes (exploratory, nominal P); d pre/post per cohort (depth-matched primary,
#   same-patient original depth and sensitivities).
# - Size: 183 x 150 mm; text 5-6 pt; panel letters 8 pt bold.
# Inputs: ../../tables/a3b_stageS/
suppressPackageStartupMessages({ library(ggplot2); library(data.table); library(patchwork) })

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)])))
tab <- file.path(here, "..", "..", "tables", "a3b_stageS")
po <- fread(file.path(tab, "A3b_pooled.tsv")); st <- fread(file.path(tab, "A3b_study.tsv"))
co <- fread(file.path(tab, "A3b_cohort_estimates.tsv"))
pd1 <- fread(file.path(tab, "E1_patient_deltas.tsv")); pdp <- fread(file.path(tab, "E1pp_patient_deltas.tsv"))

# frozen numbers (final approval): fail loudly if the tables are not the corrected version
stopifnot(po[estimand == "E1", n_patients] == 85, po[estimand == "E1", k] == 6,
          abs(po[estimand == "E1", estimate] - 0.0571) < 5e-4,
          !any(grepl("Chen_2024_Cancer_Cell.P02$", pd1$patient_id)),
          co[estimand == "E1s_i_original_depth" & study_id == "Qin_2023_Cell_Rep_Med", n_patients] == 20,
          nrow(pdp[study_id == "Qin_2023_Cell_Rep_Med"]) == 18, nrow(pdp[study_id == "Chen_2024_Cancer_Cell"]) == 10)

STUDY <- function(s) sub("^([A-Za-z]+)_([0-9]{4}).*$", "\\1 \\2", sub("^MUI_Innsbruck$", "MUI", s))
BLUE <- "#0F4D92"; GREY <- "#767676"; LIGHT <- "#CFCECE"; DARK <- "#272727"; TEAL <- "#42949E"
theme_nat <- theme_classic(base_size = 6, base_family = "Arial") +
  theme(axis.line = element_line(linewidth = 0.3, colour = DARK),
        axis.ticks = element_line(linewidth = 0.3, colour = DARK), axis.ticks.length = unit(0.8, "mm"),
        axis.text = element_text(size = 5.5, colour = "black"), axis.title = element_text(size = 6, colour = "black"),
        strip.background = element_blank(), strip.text = element_text(size = 6, colour = "black", margin = margin(b = 1.5)),
        legend.title = element_blank(), legend.text = element_text(size = 5.5), legend.key.size = unit(2.2, "mm"),
        legend.margin = margin(0, 0, 0, 0), panel.grid = element_blank(), plot.margin = margin(3, 3, 3, 3),
        plot.title = element_text(size = 6, colour = "black", face = "plain", margin = margin(b = 2)))
zero <- geom_vline(xintercept = 0, linewidth = 0.3, linetype = "22", colour = GREY)
noy <- theme(axis.ticks.y = element_blank(), axis.line.y = element_blank())
fmt <- function(x) sprintf("%+.3f", x)

# ---- a: E1 forest + sensitivities ----
s1 <- st[estimand == "E1"][order(mean_delta)]
s1[, lab := sprintf("%s (n = %d)", STUDY(study_id), n_patients)]
sens <- data.table(
  estimand = c("E1", "E1s_i_original_depth", "E1s_ii_raw_depth_matched", "E1s_iii_adjusted", "E1_frozen_atlas_label_incl_P02"),
  lab = c("Pooled, depth-matched (primary)", "(i) Original depth", "(ii) Raw score, depth-matched",
          "(iii) Covariate-adjusted", "Frozen Atlas label (P02 included)"))
sens <- merge(sens, po, by = "estimand", sort = FALSE)
sens[, lab := sprintf("%s (k = %d, n = %d)", lab, k, n_patients)]
rows <- c(rev(sens$lab[-1]), sens$lab[1], s1$lab)
ya <- setNames(c(1:4, 5.6, 6.8 + seq_len(nrow(s1)) - 1), rows)
s1[, y := ya[lab]]; sens[, y := ya[lab]]
pts <- merge(pd1, s1[, .(study_id, y)], by = "study_id")  # pooled studies only (Joanito, Khaliq < 5 patients)
stopifnot(nrow(pts) == 85)
set.seed(1); pts[, yj := y + runif(.N, -0.25, 0.25)]
e1 <- sens[estimand == "E1"]
pA <- ggplot() + zero +
  geom_point(data = pts, aes(x = delta_E1, y = yj), colour = GREY, size = 0.5, alpha = 0.7, stroke = 0) +
  geom_errorbar(data = s1, aes(xmin = ci_low, xmax = ci_high, y = y), width = 0, linewidth = 0.45,
                colour = DARK, orientation = "y") +
  geom_point(data = s1, aes(x = mean_delta, y = y), shape = 15, size = 1.3, colour = DARK) +
  geom_errorbar(data = e1, aes(xmin = pi_low, xmax = pi_high, y = y), width = 0.35, linewidth = 0.3,
                colour = BLUE, orientation = "y") +
  geom_errorbar(data = sens, aes(xmin = ci_low, xmax = ci_high, y = y), width = 0, linewidth = 0.6,
                colour = BLUE, orientation = "y") +
  geom_point(data = sens, aes(x = estimate, y = y, shape = estimand == "E1"), size = 2, colour = BLUE, fill = "white",
             stroke = 0.5) +
  scale_shape_manual(values = c(`TRUE` = 18, `FALSE` = 23), guide = "none") +
  geom_hline(yintercept = c(4.8, 6.2), linewidth = 0.2, colour = LIGHT) +
  annotate("text", x = 0.36, y = 5.6, hjust = 1, size = 5.5 / .pt, family = "Arial",
           label = sprintf("Δ = %s, P = %.3f\nI² = %.0f%%", fmt(e1$estimate), e1$p, 100 * e1$I2), lineheight = 0.9) +
  scale_y_continuous(breaks = ya, labels = names(ya), expand = expansion(add = 0.6)) +
  scale_x_continuous(limits = c(-0.15, 0.37), breaks = c(-0.1, 0, 0.1, 0.2, 0.3)) +
  labs(x = "Δ CytoTRACE2 potency, tumour − adjacent normal", y = NULL,
       title = "Normal–primary epithelium, depth-matched CytoTRACE2") +
  theme_nat + noy

# ---- b: programme differences ----
PR <- c(R_proCSC = "proCSC", R_revCSC = "revCSC", R_ExtCIOC = "Extended CIOC", R_YAPcore = "YAP core")
pb <- po[estimand %in% names(PR)][, prog := factor(PR[estimand], levels = rev(PR))]
sb <- st[estimand %in% names(PR)][, prog := factor(PR[estimand], levels = rev(PR))]
set.seed(2); sb[, yj := as.numeric(prog) + runif(.N, -0.2, 0.2)]
pb[, txt := sprintf("BH-adjusted P = %s", formatC(p_bh, format = "g", digits = 2))]
pB <- ggplot() + zero +
  geom_point(data = sb, aes(x = mean_delta, y = yj), colour = GREY, size = 0.6, alpha = 0.8, stroke = 0) +
  geom_errorbar(data = pb, aes(xmin = pi_low, xmax = pi_high, y = as.numeric(prog)), width = 0.3, linewidth = 0.3,
                colour = BLUE, orientation = "y") +
  geom_errorbar(data = pb, aes(xmin = ci_low, xmax = ci_high, y = as.numeric(prog)), width = 0, linewidth = 0.6,
                colour = BLUE, orientation = "y") +
  geom_point(data = pb, aes(x = estimate, y = as.numeric(prog)), shape = 18, size = 2.1, colour = BLUE) +
  geom_text(data = pb, aes(x = 0.2, y = as.numeric(prog) + 0.32, label = txt), hjust = 1,
            size = 5 / .pt, family = "Arial") +
  scale_y_continuous(breaks = 1:4, labels = rev(PR), expand = expansion(add = 0.5)) +
  scale_x_continuous(limits = c(-0.08, 0.2), breaks = c(-0.05, 0, 0.05, 0.1, 0.15)) +
  labs(x = "Δ UCell score, tumour − adjacent normal", y = NULL,
       title = sprintf("Epithelial programmes (k = %d, n = %d)", pb$k[1], pb$n_patients[1])) +
  theme_nat + noy

# ---- c: E1-L classes (exploratory) ----
CL <- c(`E1L_Cycling Stem/TA` = "Cycling Stem/TA", `E1L_Absorptive differentiated-like` = "Absorptive\ndifferentiated-like")
pc <- po[estimand %in% names(CL)][, cl := factor(CL[estimand], levels = rev(CL))]
sc <- st[estimand %in% names(CL)][, cl := factor(CL[estimand], levels = rev(CL))]
set.seed(3); sc[, yj := as.numeric(cl) + runif(.N, -0.18, 0.18)]
pc[, txt := sprintf("nominal P = %.3f; k = %d, n = %d", p, k, n_patients)]
pC <- ggplot() + zero +
  geom_point(data = sc, aes(x = mean_delta, y = yj), colour = GREY, size = 0.6, alpha = 0.8, stroke = 0) +
  geom_errorbar(data = pc, aes(xmin = pi_low, xmax = pi_high, y = as.numeric(cl)), width = 0.25, linewidth = 0.3,
                colour = TEAL, orientation = "y") +
  geom_errorbar(data = pc, aes(xmin = ci_low, xmax = ci_high, y = as.numeric(cl)), width = 0, linewidth = 0.6,
                colour = TEAL, orientation = "y") +
  geom_point(data = pc, aes(x = estimate, y = as.numeric(cl)), shape = 18, size = 2.1, colour = TEAL) +
  geom_text(data = pc, aes(x = 0.2, y = as.numeric(cl) + 0.34, label = txt), hjust = 1, size = 5 / .pt,
            family = "Arial") +
  scale_y_continuous(breaks = 1:2, labels = rev(CL), expand = expansion(add = 0.55)) +
  scale_x_continuous(limits = c(-0.15, 0.2), breaks = c(-0.1, 0, 0.1, 0.2)) +
  labs(x = "Δ CytoTRACE2 potency within class", y = NULL,
       title = "Within Axis-L class (exploratory)") +
  theme_nat + noy

# ---- d: pre/post per cohort ----
CO <- c(Qin_2023_Cell_Rep_Med = "Qin 2023 (chemotherapy)", Chen_2024_Cancer_Cell = "Chen 2024 (anti-PD-1)")
ES <- c(E1 = "Depth-matched (primary)", E1pp_desc_original_depth_same_patients = "Original depth, same patients",
        E1s_ii_raw_depth_matched = "(ii) Raw score, depth-matched", E1s_iii_adjusted = "(iii) Covariate-adjusted")
cd <- co[branch == "pre_post" & estimand %in% names(ES)]
cd[, `:=`(cohort = factor(CO[study_id], levels = CO), es = factor(ES[estimand], levels = rev(ES)))]
pp <- copy(pdp)[, cohort := factor(CO[study_id], levels = CO)]
set.seed(4); pp[, yj := 4 + runif(.N, -0.22, 0.22)]
cd[, txt := ifelse(estimand == "E1", sprintf("n = %d, P = %.2f", n_patients, wilcoxon_p), sprintf("n = %d", n_patients))]
pD <- ggplot() + zero +
  geom_point(data = pp, aes(x = delta_E1pp, y = yj), colour = GREY, size = 0.6, alpha = 0.8, stroke = 0) +
  geom_errorbar(data = cd, aes(xmin = ci_low, xmax = ci_high, y = as.numeric(es),
                               colour = estimand == "E1"), width = 0, linewidth = 0.55, orientation = "y") +
  geom_point(data = cd, aes(x = mean_delta, y = as.numeric(es), colour = estimand == "E1",
                            shape = estimand == "E1"), size = 1.8, fill = "white", stroke = 0.5) +
  geom_text(data = cd, aes(x = 0.1, y = as.numeric(es) + 0.33, label = txt), hjust = 1, size = 5 / .pt,
            family = "Arial") +
  scale_colour_manual(values = c(`TRUE` = BLUE, `FALSE` = DARK), guide = "none") +
  scale_shape_manual(values = c(`TRUE` = 18, `FALSE` = 23), guide = "none") +
  facet_wrap(~cohort, nrow = 1) +
  scale_y_continuous(breaks = 1:4, labels = rev(ES), expand = expansion(add = 0.5)) +
  scale_x_continuous(limits = c(-0.12, 0.1), breaks = c(-0.1, -0.05, 0, 0.05, 0.1)) +
  labs(x = "Δ CytoTRACE2 potency, post − pre treatment (tumour side)", y = NULL,
       title = "Neoadjuvant cohorts (exploratory)") +
  theme_nat + noy + theme(panel.spacing = unit(4, "mm"))

# ---- assemble ----
design <- "
AAAAAABBBB
CCCCDDDDDD
"
fig <- pA + pB + pC + pD +
  plot_layout(design = design, heights = c(1.25, 1)) +
  plot_annotation(tag_levels = "a") &
  theme(plot.tag = element_text(size = 8, face = "bold", family = "Arial"), plot.tag.position = c(0, 1))

w <- 183 / 25.4; h <- 150 / 25.4
out <- file.path(here, "ed_fig1_a3b")
svglite::svglite(paste0(out, ".svg"), width = w, height = h); print(fig); invisible(dev.off())
grDevices::cairo_pdf(paste0(out, ".pdf"), width = w, height = h, family = "Arial"); print(fig); invisible(dev.off())
ragg::agg_tiff(paste0(out, ".tiff"), width = w, height = h, units = "in", res = 600, compression = "lzw"); print(fig); invisible(dev.off())
ragg::agg_png(paste0(out, "_preview.png"), width = w, height = h, units = "in", res = 200); print(fig); invisible(dev.off())

fwrite(rbind(pts[, .(level = "patient", row = study_id, unit = patient_id, delta = delta_E1, ci_low = NA_real_, ci_high = NA_real_,
                     pi_low = NA_real_, pi_high = NA_real_, k = NA_integer_, n = NA_integer_, p = NA_real_)],
             s1[, .(level = "study", row = study_id, unit = study_id, delta = mean_delta, ci_low, ci_high,
                    pi_low = NA_real_, pi_high = NA_real_, k = NA_integer_, n = n_patients, p = NA_real_)],
             sens[, .(level = "pooled", row = estimand, unit = "pooled", delta = estimate, ci_low, ci_high, pi_low, pi_high,
                      k, n = n_patients, p)]), paste0(out, "_source_a.csv"))
fwrite(rbind(sb[, .(level = "study", programme = estimand, study_id, delta = mean_delta, ci_low, ci_high,
                    pi_low = NA_real_, pi_high = NA_real_, n = n_patients, p_bh = NA_real_)],
             pb[, .(level = "pooled", programme = estimand, study_id = "pooled", delta = estimate, ci_low, ci_high, pi_low,
                    pi_high, n = n_patients, p_bh)]), paste0(out, "_source_b.csv"))
fwrite(rbind(sc[, .(level = "study", class = estimand, study_id, delta = mean_delta, ci_low, ci_high,
                    pi_low = NA_real_, pi_high = NA_real_, n = n_patients, p_nominal = NA_real_)],
             pc[, .(level = "pooled", class = estimand, study_id = "pooled", delta = estimate, ci_low, ci_high, pi_low,
                    pi_high, n = n_patients, p_nominal = p)]), paste0(out, "_source_c.csv"))
fwrite(rbind(pp[, .(level = "patient", estimand = "E1", study_id, unit = patient_id, delta = delta_E1pp,
                    ci_low = NA_real_, ci_high = NA_real_, n = NA_integer_, wilcoxon_p = NA_real_)],
             cd[, .(level = "cohort", estimand, study_id, unit = study_id, delta = mean_delta, ci_low, ci_high,
                    n = n_patients, wilcoxon_p)]), paste0(out, "_source_d.csv"))
cat("done\n")
