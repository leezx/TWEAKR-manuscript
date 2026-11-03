# Figure MZ4: the four analyses added in review.
#   a  does the Tnfrsf12a-plasticity correlation survive removing the genes the
#      plasticity axis shares with the oncofetal signature?
#   b  does the placenta signal survive removing generic YAP target genes?
#   c  are the immune set results carried by a single gene?
#   d  is the locus occupied by TEAD and AP-1 in public ChIP-seq, and in what tissue?
#
# Reads only the frozen tables from scripts 05 and 06.

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

## (a) plasticity axis independence
a <- rd("Q5A_plasticity_axis_independence.tsv") %>%
  mutate(genotype = factor(genotype, GEN),
         axis = factor(axis, c("plast_full", "plast_clean"),
                       c("as published", "minus the 14 genes\nshared with mOnF")))
pa <- ggplot(a, aes(rho_receptor, genotype, colour = axis)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_linerange(aes(xmin = ctrl_median, xmax = ctrl_max), colour = GREY,
                 linewidth = 1.6, alpha = .35,
                 position = position_dodge(width = .5), show.legend = FALSE) +
  geom_point(size = 2.4, position = position_dodge(width = .5)) +
  scale_colour_manual(values = c(RED, BLUE), name = NULL) +
  labs(x = "partial Spearman rho with the lineage plasticity axis", y = NULL,
       title = "The plasticity association is attenuated but survives",
       subtitle = "grey bar, median to max of 24 detection-matched control genes") +
  theme_pub() + theme(legend.position = "bottom")

## (b) placenta decomposition
b <- rd("Q5B_placenta_decomposition.tsv") %>%
  filter(set %in% c("placenta_full", "placenta_minus_YAP")) %>%
  mutate(set = factor(set, c("placenta_full", "placenta_minus_YAP"),
                      c("placenta set, 34 genes", "minus 4 YAP target genes\n(Egfr, Krt19, Krt8, Phlda2)")),
         sig = FDR < .05)
pb <- ggplot(b, aes(mean_stat, fct_reorder(contrast, mean_stat), colour = set, shape = sig)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(size = 2.4, position = position_dodge(width = .55)) +
  scale_colour_manual(values = c(RED, GREY), name = NULL) +
  scale_shape_manual(values = c(`TRUE` = 16, `FALSE` = 1), name = "FDR < 0.05") +
  labs(x = "mean Wald statistic (cameraPR)", y = NULL,
       title = "The placenta signal does not survive removing generic YAP targets",
       subtitle = "no contrast remains significant once 4 of 34 genes are dropped") +
  theme_pub() + theme(legend.position = "bottom", legend.box = "vertical",
                      legend.spacing.y = unit(0, "mm"))

## (c) immune sets: one gene or many?
cc <- rd("Q5C_immune_leave_out_top.tsv") %>%
  mutate(set = sub("_", " ", set)) %>%
  select(contrast, set, top_gene, p_full, p_minus_top) %>%
  pivot_longer(c(p_full, p_minus_top), names_to = "which", values_to = "p") %>%
  mutate(which = factor(which, c("p_full", "p_minus_top"),
                        c("whole set", "minus the strongest gene")),
         lab = paste0(contrast, "\n(", top_gene, ")"))
pc <- ggplot(cc, aes(p, fct_rev(lab), colour = which)) +
  geom_vline(xintercept = .05, linetype = 2, colour = "grey55", linewidth = .3) +
  geom_line(aes(group = lab), colour = "grey80", linewidth = .4, orientation = "y") +
  geom_point(size = 2) +
  scale_x_log10() +
  scale_colour_manual(values = c(RED, GREY), name = NULL) +
  facet_wrap(~set, scales = "free_y") +
  labs(x = "cameraPR P (log scale); dashed line 0.05", y = NULL,
       title = "Both immune results are carried by a single gene",
       subtitle = "the gene named in brackets is the one removed") +
  theme_pub() + theme(legend.position = "bottom",
                      axis.text.y = element_text(size = 6))

## (d) ChIP-Atlas occupancy
d <- rd("Q6A_chipatlas_occupancy_summary.tsv") %>% filter(window_kb == 5, receptor_bound)
pd <- ggplot(d, aes(100 * receptor_pct_of_all, fct_reorder(tf, receptor_pct_of_all),
                    colour = arm)) +
  geom_vline(xintercept = 50, colour = "grey60", linewidth = .3) +
  geom_segment(aes(x = 50, xend = 100 * receptor_pct_of_all, yend = tf), linewidth = .5) +
  geom_point(size = 2.6) +
  geom_text(aes(label = sprintf("%d/%d expts", n_expt_with_peak, n_experiments)),
            hjust = -0.25, size = 2.2, colour = "grey30", show.legend = FALSE) +
  scale_colour_manual(values = c(`YAP/TEAD` = RED, `AP-1` = BLUE), name = NULL) +
  scale_x_continuous(limits = c(50, 112), breaks = c(50, 75, 100),
                     labels = c("50", "75", "100")) +
  labs(x = "percentile of the Tnfrsf12a TSS among all genes, by mean MACS2 score",
       y = NULL,
       title = "The locus is a bound TEAD and AP-1 element in public ChIP-seq",
       subtitle = "ChIP-Atlas mm10, 5 kb window; but 0 of the 4 intestinal experiments calls a peak") +
  theme_pub() + theme(legend.position = "bottom")

MZ4 <- (tag(pa, "a") | tag(pb, "b")) / (tag(pc, "c") | tag(pd, "d"))
ggsave(file.path(FIGD, "Fig_MZ4_review_audits.pdf"), MZ4, width = 11, height = 8)
ggsave(file.path(FIGD, "Fig_MZ4_review_audits.png"), MZ4, width = 11, height = 8, dpi = 300)
cat("written Fig_MZ4\n")
