# Figures OG1 and OG2 for the Ogden 2025 CRC liver-metastasis re-analysis.
#
# Reads ONLY the frozen tables from scripts 01 and 02 and computes no statistics
# of its own, so a figure cannot drift from the number quoted in the text.
#
#   OG1  the Gate A deliverable: is TNFRSF12A an oncofetal receptor, an
#        inflammatory receptor, or both?
#   OG2  the limits: what this dataset cannot answer, and the ligand negative.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(dplyr); library(tidyr); library(ggplot2)
                  library(patchwork); library(forcats)})
# Python writes booleans as the strings "True"/"False"; coerce them back on read
# so no downstream filter silently treats "False" as truthy.
rd <- function(f) {
  d <- read.delim(file.path(TAB, f), check.names = FALSE, stringsAsFactors = FALSE)
  for (j in seq_along(d)) {
    v <- d[[j]]
    if (is.character(v) && all(v[!is.na(v)] %in% c("True", "False")) &&
        any(!is.na(v))) d[[j]] <- v == "True"
  }
  d
}

theme_pub <- function(base = 8) {
  theme_classic(base_size = base) +
    theme(strip.background = element_blank(),
          strip.text = element_text(face = "bold", size = base),
          plot.title = element_text(face = "bold", size = base + 1),
          plot.subtitle = element_text(colour = "grey35", size = base - 1),
          axis.text = element_text(colour = "black"),
          panel.grid.major.y = element_line(colour = "grey92", linewidth = .3),
          legend.key.size = unit(3.2, "mm"))
}
tag <- function(p, t) p + labs(tag = t) +
  theme(plot.tag = element_text(face = "bold", size = 11))

## ------------------------------------------------------------------ OG1 (a)
## Where the receptor sits across the authors' own epithelial states.
a <- rd("Q1A_receptor_by_epithelial_subtype.tsv") %>%
  mutate(grp = case_when(subtype %in% c("REC", "iREC") ~ "regenerative (REC / iREC)",
                         subtype == "Intermediate" ~ "hybrid (Intermediate)",
                         subtype == "Stem NOTUM" ~ "Stem NOTUM",
                         TRUE ~ "other epithelial"))
pa <- ggplot(a, aes(100 * detection, fct_reorder(subtype, detection), fill = grp)) +
  geom_col(width = .7) +
  geom_text(aes(label = sprintf("%.0f%%", 100 * detection)),
            hjust = -0.2, size = 2.2, colour = "grey25") +
  scale_fill_manual(values = c("regenerative (REC / iREC)" = RED,
                               "hybrid (Intermediate)" = "#D6604D",
                               "Stem NOTUM" = BLUE,
                               "other epithelial" = GREY), name = NULL) +
  scale_x_continuous(expand = expansion(mult = c(0, .14))) +
  labs(x = "% of nuclei with TNFRSF12A detected", y = NULL,
       title = "TNFRSF12A is enriched in regenerative and hybrid states",
       subtitle = "15 patients, 16,009 epithelial nuclei; REC and iREC are indistinguishable") +
  theme_pub() + theme(legend.position = "bottom", legend.text = element_text(size = 6))

## ------------------------------------------------------------------ OG1 (b)
## THE CORE PANEL. Both associations survive mutual control; the oncofetal one
## is larger in 11 of 12 patients.
b <- rd("Q1B_patient_partial_correlations.tsv") %>%
  filter(eligible) %>%
  mutate(dimension = factor(dimension, c("onf_revCSC", "infl_IFNG"),
                            c("oncofetal\n(revCSC)", "inflammatory\n(IFN-gamma)")))
pb <- ggplot(b, aes(dimension, rho_partial)) +
  geom_hline(yintercept = 0, colour = "grey60", linewidth = .3) +
  geom_line(aes(group = patient), colour = "grey75", linewidth = .4) +
  geom_point(aes(colour = dimension), size = 2.2) +
  stat_summary(fun = median, geom = "crossbar", width = .45,
               linewidth = .4, colour = "black") +
  scale_colour_manual(values = c(RED, BLUE), guide = "none") +
  labs(x = NULL, y = "partial Spearman rho with TNFRSF12A",
       title = "Both links are real; the oncofetal link is the larger one",
       subtitle = paste("per patient, each dimension controlled for the other,",
                        "cell cycle and depth\nbar = median; 11 of 12 patients",
                        "oncofetal > inflammatory, P = 0.0015")) +
  theme_pub()

## ------------------------------------------------------------------ OG1 (c)
## Calibration against detection-matched control genes, on both axes at once.
cc <- rd("Q1D_control_gene_calibration.tsv")
pc <- ggplot(cc, aes(median_rho_onf, median_rho_infl)) +
  geom_hline(yintercept = 0, colour = "grey80", linewidth = .3) +
  geom_vline(xintercept = 0, colour = "grey80", linewidth = .3) +
  geom_abline(slope = 1, intercept = 0, linetype = 3, colour = "grey65", linewidth = .3) +
  geom_point(data = ~filter(.x, !is_receptor), colour = GREY, size = 1.8, alpha = .75) +
  geom_point(data = ~filter(.x, is_receptor), colour = RED, size = 3) +
  annotate("text", x = cc$median_rho_onf[cc$is_receptor],
           y = cc$median_rho_infl[cc$is_receptor],
           label = "TNFRSF12A", colour = RED, size = 2.4, hjust = 1.15) +
  labs(x = "partial rho, oncofetal axis", y = "partial rho, inflammatory axis",
       title = "Specific on the oncofetal axis; matched by a control gene on the other",
       subtitle = paste("vs 24 detection-matched control genes: 0 of 24 exceed the",
                        "receptor on the oncofetal\naxis, but 1 of 24 (CLTB) does on",
                        "the inflammatory axis. Dotted line = equal association.")) +
  theme_pub()

## ------------------------------------------------------------------ OG1 (d)
## The 2x2 stratification. Presented as a stratification, not as four states.
d <- rd("Q1E_2x2_stratification.tsv") %>%
  mutate(onf = ifelse(onf_high, "OnF-high", "OnF-low"),
         ifn = ifelse(ifn_high, "IFN-high", "IFN-low"),
         onf = factor(onf, c("OnF-low", "OnF-high")),
         ifn = factor(ifn, c("IFN-low", "IFN-high")))
pd <- ggplot(d, aes(onf, 100 * detection, colour = ifn, group = interaction(patient, ifn))) +
  geom_line(linewidth = .35, alpha = .45) +
  geom_point(size = 1.5, alpha = .75) +
  stat_summary(aes(group = ifn), fun = median, geom = "line", linewidth = 1.3) +
  stat_summary(aes(group = ifn), fun = median, geom = "point", size = 3) +
  scale_colour_manual(values = c("IFN-low" = BLUE, "IFN-high" = RED), name = NULL) +
  labs(x = NULL, y = "% of nuclei with TNFRSF12A detected",
       title = "Both axes add; neither explains the other",
       subtitle = paste("within-patient median split on each score.",
                        "Thin lines, patients; thick lines, median.\n",
                        "9.4% -> 16.7% (IFN alone) -> 23.5% (OnF alone) -> 34.3% (both)")) +
  theme_pub() + theme(legend.position = "bottom")

OG1 <- (tag(pa, "a") | tag(pb, "b")) / (tag(pc, "c") | tag(pd, "d"))
ggsave(file.path(FIGD, "Fig_OG1_tweakr_onf_vs_inflammation.pdf"), OG1,
       width = 11, height = 8.4)
ggsave(file.path(FIGD, "Fig_OG1_tweakr_onf_vs_inflammation.png"), OG1,
       width = 11, height = 8.4, dpi = 300)
cat("written Fig_OG1\n")

## ------------------------------------------------------------------ OG2 (a)
## The REC/iREC test, shown WITH its failed positive control.
e <- rd("Q2B_REC_vs_iREC_with_positive_control.tsv") %>%
  mutate(q = sub("  \\[POSITIVE CONTROL\\]", "", quantity),
         is_ctrl = grepl("POSITIVE CONTROL", quantity)) %>%
  select(q, is_ctrl, median_REC, median_iREC, wilcoxon_p) %>%
  mutate(q = sprintf("%s\nP = %.2f", q, wilcoxon_p)) %>%
  pivot_longer(c(median_REC, median_iREC), names_to = "state", values_to = "v") %>%
  mutate(state = sub("median_", "", state),
         state = factor(state, c("REC", "iREC")))
pe <- ggplot(e, aes(state, v, group = q, colour = is_ctrl)) +
  geom_line(linewidth = .6) + geom_point(size = 2.4) +
  scale_colour_manual(values = c(`FALSE` = GREY, `TRUE` = RED),
                      labels = c("receptor / revCSC", "IFN-gamma (positive control)"),
                      name = NULL) +
  facet_wrap(~q, scales = "free_y", nrow = 1) +
  labs(x = NULL, y = "median across the 5 patients with both states",
       title = "The REC vs iREC comparison is underpowered, not negative",
       subtitle = paste("only 5 patients carry >=20 cells of both states. The IFN",
                        "difference that DEFINES\nthe two states is itself not",
                        "recovered (P = 0.62, wrong direction), so the receptor\n",
                        "result here carries no evidential weight either way.")) +
  theme_pub() + theme(legend.position = "bottom", strip.text = element_text(size = 6))

## ------------------------------------------------------------------ OG2 (b)
## The ligand: not macrophage-specific, and too sparse to pursue.
g <- rd("Q1G_ligand_by_cell_type.tsv")
pg <- ggplot(g, aes(100 * ligand_detection, fct_reorder(cell_type, ligand_detection))) +
  geom_col(fill = GREY, width = .7) +
  geom_vline(xintercept = 10, linetype = 2, colour = RED, linewidth = .4) +
  annotate("text", x = 9.6, y = 1.4, label = "stop-rule threshold",
           colour = RED, size = 2.2, hjust = 1) +
  scale_x_continuous(limits = c(0, 11), expand = expansion(mult = c(0, .02))) +
  labs(x = "% of nuclei with TNFSF12 detected", y = NULL,
       title = "The ligand is too sparse, and has no consistent source",
       subtitle = paste("no cell type reaches 10% detection (max 7.0%, myeloid).",
                        "Across the 12 patients with\n>=10 positive nuclei the top",
                        "source is epithelial in 6, myeloid in 5, T/NK in 1 ->",
                        "stop rule met.")) +
  theme_pub()

## ------------------------------------------------------------------ OG2 (c)
## Per-patient receptor detection: the heterogeneity, stated openly.
h <- rd("Q1A_receptor_by_patient.tsv") %>%
  mutate(eligible = n_epithelial >= 100 & receptor_detection >= 0.05)
ph <- ggplot(h, aes(100 * receptor_detection, fct_reorder(patient, receptor_detection),
                    fill = eligible)) +
  geom_col(width = .7) +
  scale_fill_manual(values = c(`TRUE` = BLUE, `FALSE` = GREY),
                    labels = c("excluded", "analysed"), name = NULL) +
  scale_x_continuous(expand = expansion(mult = c(0, .1))) +
  labs(x = "% of epithelial nuclei with TNFRSF12A detected", y = NULL,
       title = "Receptor detection varies widely between patients",
       subtitle = paste("3 of 15 patients excluded before testing (CRC07 0.2%,",
                        "CRC09 2.3%, CRC13 n=22),\non pre-set thresholds, not on",
                        "their results.")) +
  theme_pub() + theme(legend.position = "bottom")

## ------------------------------------------------------------------ OG2 (d)
## Therapy: a null, reported as a null.
## Plotted as every patient, not as two medians: with n = 7 vs 8 the spread is
## the whole story, and a two-point line on a free axis would make a null look
## like an effect.
kp <- rd("Q2D_therapy_per_patient.tsv")
ks <- rd("Q2D_therapy_exploratory.tsv")
lab <- c(receptor_detection = "TNFRSF12A detection",
         revcsc = "revCSC score", ifng = "IFN-gamma score")
k <- kp %>%
  pivot_longer(c(receptor_detection, revcsc, ifng),
               names_to = "quantity", values_to = "v") %>%
  left_join(ks[, c("quantity", "mannwhitney_p")], by = "quantity") %>%
  mutate(q = sprintf("%s\nP = %.2f", lab[quantity], mannwhitney_p),
         therapy = factor(therapy, c("Naive", "Treated")))
pk <- ggplot(k, aes(therapy, v)) +
  geom_boxplot(width = .5, outlier.shape = NA, colour = "grey55", fill = NA,
               linewidth = .4) +
  geom_jitter(width = .14, height = 0, size = 1.7, colour = BLUE, alpha = .85) +
  facet_wrap(~q, scales = "free_y", nrow = 1) +
  expand_limits(y = 0) +
  labs(x = NULL, y = "patient-level mean",
       title = "Prior chemotherapy does not shift the receptor or either axis",
       subtitle = paste("every patient shown; 7 treated vs 8 naive, all P > 0.33.",
                        "These are not paired\npre/post samples, so this is",
                        "exploratory and cannot speak to treatment-induced\nplasticity.")) +
  theme_pub() + theme(strip.text = element_text(size = 6))

OG2 <- (tag(pe, "a") | tag(pg, "b")) / (tag(ph, "c") | tag(pk, "d"))
ggsave(file.path(FIGD, "Fig_OG2_limits_and_negatives.pdf"), OG2, width = 11, height = 8.4)
ggsave(file.path(FIGD, "Fig_OG2_limits_and_negatives.png"), OG2, width = 11, height = 8.4, dpi = 300)
cat("written Fig_OG2\n")
