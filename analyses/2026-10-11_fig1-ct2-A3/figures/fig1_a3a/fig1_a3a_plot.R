#!/usr/bin/env Rscript
# Fig. 1 A3a main panel (nature-figure, R). Frozen contract A3a v0.2; results approved 2026-10-11.
#
# Figure contract
# - Claim: canonical proCSC/Lgr5CSC programmes remain coupled to transcriptome-derived developmental
#   potency under two independent algorithms (CytoTRACE2, SCENT-CCAT), whereas revival-, YAP- and
#   oncofetal-associated programmes are positive only before adjustment for transcriptomic complexity.
# - Archetype: quantitative grid (two-facet forest).
# - Data: pooled within-sample Spearman rho (sample -> Fisher z -> patient -> study -> REML + Hartung-Knapp),
#   95% CI; 216 patients, 13 cohorts; tumour-derived epithelium (not CNV-confirmed malignant cells).
# - Adjusted = partial Spearman on log UMI, log detected genes, mitochondrial fraction, S and G2M scores.
# - Size: 89 mm x 62 mm (single column); text 5-7 pt; panel letter added at Figure 1 assembly.
# Inputs: ../../tables/a3a/A3a_pooled.tsv, ../../tables/a3a_ccat/A3a_ccat_pooled.tsv
suppressPackageStartupMessages({ library(ggplot2); library(data.table) })

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)])))
tab <- file.path(here, "..", "..", "tables")

PROG <- c(proCSC = "proCSC", Lgr5CSC = "Lgr5CSC", ExtCIOC = "Extended CIOC", revCSC = "revCSC", YAPcore = "YAP core")
COL <- c("CytoTRACE2" = "#0F4D92", "SCENT-CCAT" = "#42949E")

ct <- fread(file.path(tab, "a3a", "A3a_pooled.tsv"))
cc <- fread(file.path(tab, "a3a_ccat", "A3a_ccat_pooled.tsv"))
pick <- function(d, an, proxy) {
  x <- d[analysis == an & programme %in% names(PROG),
         .(programme, rho, ci_low, ci_high, k, n_patients, studies_same_sign, p_bh)]
  x[, proxy := proxy]
  x
}
d <- rbind(
  pick(ct, "ct2_final|unadjusted|ge100", "CytoTRACE2")[, estimand := "Before adjustment"],
  pick(ct, "ct2_final|adjusted|ge100", "CytoTRACE2")[, estimand := "After adjustment"],
  pick(cc, "ccat|unadjusted|ge100|primary", "SCENT-CCAT")[, estimand := "Before adjustment"],
  pick(cc, "ccat|adjusted|ge100|primary", "SCENT-CCAT")[, estimand := "After adjustment"]
)
stopifnot(nrow(d) == 20, all(d$k == 13), all(d$n_patients == 216))
d[, estimand := factor(estimand, levels = c("Before adjustment", "After adjustment"))]
d[, prog_label := factor(PROG[programme], levels = rev(PROG))]
d[, proxy := factor(proxy, levels = names(COL))]
d[, y := as.numeric(prog_label) + ifelse(proxy == "CytoTRACE2", 0.17, -0.17)]

theme_nat <- theme_classic(base_size = 6, base_family = "Arial") +
  theme(axis.line = element_line(linewidth = 0.3, colour = "#272727"),
        axis.ticks = element_line(linewidth = 0.3, colour = "#272727"),
        axis.ticks.length = unit(0.8, "mm"),
        axis.text = element_text(size = 6, colour = "black"),
        axis.title = element_text(size = 6, colour = "black"),
        strip.background = element_blank(),
        strip.text = element_text(size = 6, face = "plain", colour = "black", margin = margin(b = 1.5)),
        legend.position = "top", legend.justification = "left",
        legend.title = element_blank(), legend.text = element_text(size = 5.5),
        legend.key.size = unit(2.2, "mm"), legend.margin = margin(0, 0, 0, 0),
        legend.box.margin = margin(0, 0, -2, -6),
        panel.spacing.x = unit(3, "mm"), plot.margin = margin(2, 3, 2, 2),
        panel.grid = element_blank())

p <- ggplot(d, aes(x = rho, y = y, colour = proxy, shape = proxy)) +
  geom_vline(xintercept = 0, linewidth = 0.3, linetype = "22", colour = "#767676") +
  geom_hline(yintercept = 3.5, linewidth = 0.25, colour = "#CFCECE") +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high), width = 0, linewidth = 0.45, orientation = "y") +
  geom_text(data = data.frame(estimand = factor("Before adjustment", levels = levels(d$estimand))),
            aes(x = 0.79, y = 0.62, label = "216 patients · 13 cohorts"), inherit.aes = FALSE,
            hjust = 1, vjust = 0, size = 5 / .pt, family = "Arial", colour = "black") +
  geom_point(size = 1.5, fill = "white", stroke = 0.6) +
  facet_wrap(~estimand, nrow = 1) +
  scale_colour_manual(values = COL) +
  scale_shape_manual(values = c("CytoTRACE2" = 16, "SCENT-CCAT" = 21)) +
  scale_x_continuous(limits = c(-0.2, 0.8), breaks = c(0, 0.25, 0.5, 0.75), labels = c("0", "0.25", "0.50", "0.75"),
                     expand = c(0, 0)) +
  scale_y_continuous(breaks = seq_along(levels(d$prog_label)), labels = levels(d$prog_label),
                     limits = c(0.5, 5.5), expand = c(0, 0)) +
  labs(x = "Within-sample Spearman ρ with predicted potency (95% CI)", y = NULL) +
  coord_cartesian(clip = "off") +
  theme_nat +
  theme(axis.ticks.y = element_blank(), axis.line.y = element_blank())

w <- 89 / 25.4; h <- 62 / 25.4
out <- file.path(here, "fig1_a3a")
svglite::svglite(paste0(out, ".svg"), width = w, height = h); print(p); invisible(dev.off())
grDevices::cairo_pdf(paste0(out, ".pdf"), width = w, height = h, family = "Arial"); print(p); invisible(dev.off())
ragg::agg_tiff(paste0(out, ".tiff"), width = w, height = h, units = "in", res = 600, compression = "lzw")
print(p); invisible(dev.off())
ragg::agg_png(paste0(out, "_preview.png"), width = w, height = h, units = "in", res = 300); print(p); invisible(dev.off())

src <- d[, .(panel = "main", programme, programme_label = PROG[programme], proxy, estimand, rho, ci_low, ci_high,
             k_studies = k, n_patients, studies_same_sign, p_bh)]
fwrite(src[order(estimand, programme, proxy)], paste0(out, "_source.csv"))
cat("done\n")
