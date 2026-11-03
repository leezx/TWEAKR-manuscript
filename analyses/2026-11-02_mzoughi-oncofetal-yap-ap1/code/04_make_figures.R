# Figures MZ1-MZ3. Reads only the frozen tables written by scripts 01-03 and
# computes no new statistics, so a figure cannot drift away from the text.
#
#  MZ1  the receptor and the oncofetal state in the A and AKSP models (scRNA-seq)
#  MZ2  YAP and AP-1 perturbation (bulk RNA-seq)
#  MZ3  the chromatin negative (bulk ATAC-seq)

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(dplyr); library(tidyr); library(ggplot2)
                  library(patchwork); library(forcats)})
rd <- function(f) read.delim(file.path(TAB, f), check.names = FALSE)

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
tag <- function(p, t) p + labs(tag = t) + theme(plot.tag = element_text(face = "bold", size = 11))
GEN <- c("WT", "A", "AKSP")

## ===== MZ1 ==================================================================
q1a <- rd("Q1A_receptor_in_oncofetal_cells.tsv") %>% mutate(genotype = factor(genotype, GEN))
q1b <- rd("Q1B_receptor_vs_lineage_plasticity.tsv") %>% filter(kind != "score") %>%
  mutate(genotype = factor(genotype, GEN))
q1c <- rd("Q1C_lineage_plasticity_deciles.tsv") %>% mutate(genotype = factor(genotype, GEN))
st  <- rd("Q1_state_summary.tsv") %>% mutate(genotype = factor(genotype, GEN))

# a. the state and the receptor rise together across the three models
a_d <- st %>% select(genotype, `oncofetal score (mOnF)` = mean_mOnF,
                     `lineage plasticity` = mean_plasticity,
                     `Tnfrsf12a, mean log` = rec_mean_log) %>%
  pivot_longer(-genotype) %>%
  mutate(name = factor(name, c("oncofetal score (mOnF)", "lineage plasticity",
                               "Tnfrsf12a, mean log")))
p1a <- ggplot(a_d, aes(genotype, value, group = 1)) +
  geom_hline(yintercept = 0, colour = "grey70", linewidth = .3) +
  geom_line(colour = RED, linewidth = .5) + geom_point(colour = RED, size = 2) +
  facet_wrap(~name, scales = "free_y") +
  labs(x = NULL, y = NULL, title = "The receptor tracks the oncofetal state across the three models",
       subtitle = "cell means per library; WT organoids, A (Apc-null) and AKSP tumoroids") +
  theme_pub()

# b. receptor in mOnF-high cells, against detection-matched control genes
p1b <- ggplot(q1a, aes(d_log, genotype)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(data = subset(q1a, kind == "control"), colour = GREY, size = 1.3, alpha = .7) +
  geom_point(data = subset(q1a, kind == "ligand"), colour = BLUE, size = 1.5) +
  geom_point(data = subset(q1a, kind == "receptor"), colour = RED, size = 2.8) +
  labs(x = "oncofetal-high minus other cells (log expression, depth-quintile stratified)",
       y = NULL, title = "Tnfrsf12a separates oncofetal cells, and only where they exist",
       subtitle = "red Tnfrsf12a | blue Tnfsf12 | grey 24 detection-matched control genes") +
  theme_pub()

# c. the receptor along the lineage plasticity axis of Fig. 1j-l
c_d <- q1c %>% filter(kind %in% c("receptor", "control")) %>%
  group_by(genotype, decile, kind) %>%
  summarise(mean_log = mean(mean_log), .groups = "drop") %>%
  group_by(genotype, kind) %>% mutate(rel = mean_log - mean_log[decile == 1]) %>% ungroup()
p1c <- ggplot(c_d, aes(decile, rel, colour = kind)) +
  geom_hline(yintercept = 0, colour = "grey70", linewidth = .3) +
  geom_line(linewidth = .6) + geom_point(size = 1.4) +
  scale_colour_manual(values = c(receptor = RED, control = GREY),
                      labels = c(receptor = "Tnfrsf12a", control = "control-gene mean"),
                      name = NULL) +
  scale_x_continuous(breaks = c(1, 5, 10)) +
  facet_wrap(~genotype) +
  labs(x = "decile of lineage plasticity score (esophagus mucosa - colon)",
       y = "log expression, relative to decile 1",
       title = "Along the lineage plasticity axis the paper uses in Fig. 1j-l",
       subtitle = "the axis is flat in WT and rises in both tumour models") +
  theme_pub() + theme(legend.position = "bottom")

# d. correlation with plasticity, receptor against controls
p1d <- ggplot(q1b, aes(rho_partial_depth, genotype)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(data = subset(q1b, kind == "control"), colour = GREY, size = 1.3, alpha = .7) +
  geom_point(data = subset(q1b, kind == "ligand"), colour = BLUE, size = 1.5) +
  geom_point(data = subset(q1b, kind == "receptor"), colour = RED, size = 2.8) +
  labs(x = "partial Spearman rho with lineage plasticity, library size removed", y = NULL,
       title = "Correlation with lineage plasticity",
       subtitle = "cells are not independent; the claim is the gap from the control genes, at identical n") +
  theme_pub()

MZ1 <- (tag(p1a, "a") / (tag(p1b, "b") | tag(p1d, "d")) / tag(p1c, "c")) +
  plot_layout(heights = c(.85, 1, 1))
ggsave(file.path(FIGD, "Fig_MZ1_receptor_oncofetal_state.pdf"), MZ1, width = 10, height = 10)
ggsave(file.path(FIGD, "Fig_MZ1_receptor_oncofetal_state.png"), MZ1, width = 10, height = 10, dpi = 300)

## ===== MZ2 ==================================================================
q2a <- rd("Q2A_gene_level_per_contrast.tsv") %>% filter(gene == RECEPTOR)
AXIS <- c("YAP gain", "YAP+AP-1 gain", "AP-1 gain on YAP", "YAP loss", "AP-1 loss",
          "progression", "oncofetal state", "RXR gain", "RXR loss")
q2a <- q2a %>% mutate(axis = factor(axis, AXIS),
                      sig = ifelse(!is.na(padj) & padj < .05, "padj < 0.05", "n.s."))
p2a <- ggplot(q2a, aes(log2FC, fct_reorder(contrast, log2FC), colour = sig)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_errorbarh(aes(xmin = log2FC - 1.96 * lfcSE, xmax = log2FC + 1.96 * lfcSE),
                 height = 0, linewidth = .4) +
  geom_point(size = 2.2) +
  scale_colour_manual(values = c(`padj < 0.05` = RED, `n.s.` = GREY), name = NULL) +
  facet_grid(axis ~ ., scales = "free_y", space = "free_y", switch = "y") +
  labs(x = "Tnfrsf12a log2 fold change (DESeq2, 95% CI)", y = NULL,
       title = "Tnfrsf12a responds to YAP and to AP-1, in both directions",
       subtitle = "3-4 organoid replicates per arm; batch in the model where present") +
  theme_pub() +
  theme(strip.placement = "outside", strip.text.y.left = element_text(angle = 0, hjust = 1),
        legend.position = "bottom")

# b. programmes, same contrasts
q2b <- rd("Q2B_programme_level_per_contrast.tsv")
SETS <- c(paper_mOnF = "oncofetal (authors')", project_revCSC = "revCSC",
          project_YAP_regen = "YAP regeneration", paper_mStem = "Lgr5 stem",
          mapped_placenta_troph = "placenta / trophoblast", mapped_EVT_core = "EVT core",
          mapped_IFA_core = "IFA core", mapped_TRA_core = "TRA core",
          project_Immune_suppression = "immune suppression",
          project_Cytotoxic_resistance = "cytotoxic resistance")
KEEP <- c("YAPOE_vs_EV", "YAPOE_FOS_vs_EV", "YAPOE_FOS_vs_YAPOE",
          "YAPsh1_vs_scr", "YAPsh2_vs_scr", "FOSDN_vs_EV_in_Apcloss", "FOSkd_vs_scr")
b_d <- q2b %>% filter(contrast %in% KEEP, set %in% names(SETS)) %>%
  mutate(set = factor(SETS[set], rev(unname(SETS))),
         contrast = factor(contrast, KEEP),
         star = ifelse(FDR_global < .001, "***",
                ifelse(FDR_global < .01, "**", ifelse(FDR_global < .05, "*", ""))))
lim <- max(abs(b_d$mean_stat))
p2b <- ggplot(b_d, aes(contrast, set, fill = mean_stat)) +
  geom_tile(colour = "white", linewidth = .6) +
  geom_text(aes(label = star), size = 2.6, vjust = .78) +
  scale_fill_gradient2(low = BLUE, mid = "white", high = RED, midpoint = 0,
                       limits = c(-lim, lim), name = "mean Wald\nstatistic") +
  labs(x = NULL, y = NULL,
       title = "The placenta and tumour-intrinsic immune programmes move with YAP and AP-1 too",
       subtitle = "cameraPR, competitive test; stars are global BH FDR (* .05, ** .01, *** .001)") +
  theme_pub() + theme(axis.text.x = element_text(angle = 30, hjust = 1),
                      panel.grid.major.y = element_blank())

# c. the receptor against the programme, across every contrast
q2c <- rd("Q2C_receptor_vs_onf_across_contrasts.tsv")
p2c <- ggplot(q2c, aes(onf_stat, rec_stat)) +
  geom_hline(yintercept = 0, colour = "grey70", linewidth = .3) +
  geom_vline(xintercept = 0, colour = "grey70", linewidth = .3) +
  geom_smooth(method = "lm", se = FALSE, colour = GREY, linewidth = .4, formula = y ~ x) +
  geom_point(colour = RED, size = 2) +
  ggrepel::geom_text_repel(aes(label = contrast), size = 2, colour = "grey25",
                           max.overlaps = 20, seed = SEED) +
  labs(x = "mOnF programme, mean Wald statistic",
       y = "Tnfrsf12a, Wald statistic",
       title = "Across 15 contrasts the receptor moves with the programme",
       subtitle = "Spearman rho = 0.975") +
  theme_pub()

MZ2 <- (tag(p2a, "a") | (tag(p2b, "b") / tag(p2c, "c"))) + plot_layout(widths = c(1, 1.1))
ggsave(file.path(FIGD, "Fig_MZ2_yap_ap1_perturbation.pdf"), MZ2, width = 12, height = 8.5)
ggsave(file.path(FIGD, "Fig_MZ2_yap_ap1_perturbation.png"), MZ2, width = 12, height = 8.5, dpi = 300)

## ===== MZ3 ==================================================================
q3b <- rd("Q3B_locus_classes.tsv")
EXPL <- c(progression = "GSE239752 (WT / A / AKSP)", rxr = "GSE239755 (WT / RXRi / A)")
b3 <- q3b %>% filter(cls != "other") %>%
  mutate(cls = factor(cls, c("Tnfrsf12a_locus", "mOnF_locus", "mStem_locus"),
                      c("Tnfrsf12a locus", "mOnF gene loci", "Lgr5 stem loci")),
         experiment = EXPL[experiment])
p3a <- ggplot(b3, aes(median_log2FC, contrast, colour = cls)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(size = 2.2, position = position_dodge(width = .5)) +
  scale_colour_manual(values = c(`Tnfrsf12a locus` = RED, `mOnF gene loci` = BLUE,
                                 `Lgr5 stem loci` = GREY), name = NULL) +
  facet_wrap(~experiment, scales = "free_y") +
  labs(x = "median peak log2 fold change", y = NULL,
       title = "The oncofetal loci open in both experiments; the receptor locus in only one",
       subtitle = "peaks within 50 kb of a TSS, against all other peaks in the same contrast") +
  theme_pub() + theme(legend.position = "bottom")

q3b2 <- rd("Q3B2_window_ladder.tsv") %>% mutate(experiment = EXPL[experiment])
p3b <- ggplot(q3b2, aes(window_kb, median_log2FC, colour = contrast)) +
  geom_hline(yintercept = 0, colour = "grey70", linewidth = .3) +
  geom_line(linewidth = .5) + geom_point(size = 1.5) +
  scale_x_log10(breaks = c(10, 25, 50, 100, 250, 500)) +
  scale_colour_brewer(palette = "Dark2", name = NULL) +
  facet_wrap(~experiment) +
  labs(x = "window around the Tnfrsf12a TSS (kb, log scale)",
       y = "median peak log2 fold change",
       title = "and the discordance is proximal, not a distal element the window missed",
       subtitle = "window size scanned as a ladder, not chosen after seeing the answer; GSE239755 opens at 10-25 kb, GSE239752 does not") +
  theme_pub() + theme(legend.position = "bottom")

q3c <- rd("Q3C_motif_counts.tsv") %>%
  mutate(set = factor(set, c("Tnfrsf12a_locus", "matched_background"),
                      c("Tnfrsf12a locus", "width- and depth-matched background")),
         TEAD_kb = 1000 * TEAD / n_bp, AP1_kb = 1000 * AP1 / n_bp) %>%
  select(set, TEAD_kb, AP1_kb) %>%
  pivot_longer(-set, names_to = "motif", values_to = "per_kb") %>%
  mutate(motif = recode(motif, TEAD_kb = "TEAD (GGAATG)", AP1_kb = "AP-1 (TGA[CG]TCA)"))
p3c <- ggplot(q3c, aes(per_kb, set, colour = set)) +
  geom_point(position = position_jitter(height = .18, width = 0), size = .9, alpha = .45) +
  stat_summary(fun = mean, geom = "point", shape = 23, size = 2.6, stroke = .7,
               colour = "black", aes(fill = set)) +
  scale_colour_manual(values = c(RED, GREY), guide = "none") +
  scale_fill_manual(values = c(RED, GREY), guide = "none") +
  facet_wrap(~motif) +
  labs(x = "consensus matches per kb", y = NULL,
       title = "The locus peaks carry no excess of TEAD or AP-1 consensus sites",
       subtitle = "diamonds, means; 24 locus peaks vs 408 matched background peaks") +
  theme_pub()

MZ3 <- (tag(p3a, "a") / tag(p3b, "b") / tag(p3c, "c"))
ggsave(file.path(FIGD, "Fig_MZ3_chromatin_negative.pdf"), MZ3, width = 10, height = 9)
ggsave(file.path(FIGD, "Fig_MZ3_chromatin_negative.png"), MZ3, width = 10, height = 9, dpi = 300)

cat("written Fig_MZ1, Fig_MZ2, Fig_MZ3\n")
