# Figure EC4: the three analyses added in review.
#   a  TNFRSF12A in oncofetal vs other malignant cells, per tumour, against the
#      detection-matched control-gene distribution
#   b  the same effect for the receptor, the ligands and the controls
#   c  the detection-density audit: where the EC3c inflation goes under
#      stratification, score residualisation and three radii
#   d  receptor-conditioned proximity, the negative that closes the branch
#
# Reads only the frozen tables from scripts 06 and 07.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({
  library(dplyr); library(tidyr); library(ggplot2); library(patchwork); library(forcats)
})
FIGOUT <- file.path(OUT, "figures")
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

pp <- rd("Q6_receptor_state_specificity_per_patient.tsv")
sm <- rd("Q6_receptor_state_specificity_summary.tsv")
cal <- rd("Q6_receptor_vs_control_genes.tsv")

## (a) per tumour: receptor against its own control-gene distribution
a_d <- pp %>% filter(definition == "onf_authors") %>%
  mutate(kind = factor(kind, c("receptor", "ligand", "control")))
pa <- ggplot(a_d, aes(d_log, fct_reorder(patient, d_log * (kind == "receptor")))) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(data = subset(a_d, kind == "control"), colour = GREY, size = 1.2, alpha = .7) +
  geom_point(data = subset(a_d, kind == "ligand"), colour = BLUE, size = 1.4) +
  geom_point(data = subset(a_d, kind == "receptor"), colour = RED, size = 2.6) +
  labs(x = "oncofetal - other malignant cells (log expression, FOV x depth stratified)",
       y = NULL,
       title = "TNFRSF12A in oncofetal cells, tumour by tumour",
       subtitle = "red TNFRSF12A | blue ligands | grey 12 detection-matched control genes") +
  theme_pub()

## (b) effect by gene, both state definitions
b_d <- sm %>% mutate(kind = factor(kind, c("receptor", "ligand", "control")),
  definition = factor(definition, c("onf_authors", "onf_revCSC"),
                      c("oncofetal = authors' label", "oncofetal = revCSC decile\n(TNFRSF12A removed)")))
pb <- ggplot(b_d, aes(median_d_log, kind, colour = kind)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(position = position_jitter(height = .18, width = 0), size = 1.6, alpha = .85) +
  geom_text(data = subset(b_d, gene == "TNFRSF12A"),
            aes(label = sprintf("%d/%d tumours", n_pos, n_patients)),
            hjust = 1.18, size = 2.3, colour = RED, show.legend = FALSE) +
  scale_colour_manual(values = c(receptor = RED, ligand = BLUE, control = GREY), guide = "none") +
  scale_y_discrete(expand = expansion(add = c(.5, .9))) +
  scale_x_continuous(expand = expansion(mult = c(.08, .12))) +
  facet_wrap(~definition) +
  labs(x = "median across tumours of the stratified difference (log expression)", y = NULL,
       title = "The receptor separates from ligands and from control genes",
       subtitle = "one point per gene") +
  theme_pub()

## (c) the density audit
au <- rd("Q7_density_audit_and_receptor_niche.tsv")
ec3 <- rd("Q3b_control_gene_colocalisation.tsv") %>%
  filter(oncofetal_def == "oncofetal_revCSC") %>%
  transmute(radius = 50, contrast = "EC3c as published\n(revCSC decile, unstratified)",
            kind, z)
c_d <- au %>% filter(source == "all_cells",
                     contrast %in% c("revCSCraw_strat", "revCSCresid_strat", "authors_strat")) %>%
  mutate(contrast = recode(contrast,
          revCSCraw_strat = "revCSC decile\n+ FOV x depth strata",
          revCSCresid_strat = "score residualised\n+ FOV x depth strata",
          authors_strat = "authors' label\n+ FOV x depth strata")) %>%
  select(radius, contrast, kind, z) %>% bind_rows(ec3) %>%
  mutate(contrast = factor(contrast, c("EC3c as published\n(revCSC decile, unstratified)",
                                       "revCSC decile\n+ FOV x depth strata",
                                       "score residualised\n+ FOV x depth strata",
                                       "authors' label\n+ FOV x depth strata")),
         radius = factor(radius, c(20, 50, 100), c("20 um", "50 um", "100 um")))
pc <- ggplot(c_d, aes(z, contrast, colour = kind)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(position = position_jitterdodge(jitter.height = .16, dodge.width = .55),
             size = .9, alpha = .5) +
  stat_summary(fun = median, geom = "point", shape = 23, size = 2.6, stroke = .7,
               colour = "black", aes(fill = kind),
               position = position_dodge(width = .55)) +
  scale_fill_manual(values = c(ligand = BLUE, control = GREY), guide = "none") +
  scale_colour_manual(values = c(ligand = BLUE, control = GREY), name = NULL) +
  facet_wrap(~radius) +
  labs(x = "z versus field-permuted gene label", y = NULL,
       title = "Where the spurious colocalisation comes from",
       subtitle = "diamonds, medians; the published EC3c test exists at 50 um only; stratifying on field and detection quintile removes most of the inflation, but not all") +
  theme_pub() + theme(legend.position = "bottom")

## (d) receptor-conditioned proximity
d_d <- au %>% filter(contrast == "receptor_in_onf", source == "macrophage") %>%
  mutate(radius = factor(radius, c(20, 50, 100), c("20 um", "50 um", "100 um")),
         kind = factor(kind, c("ligand", "control")))
pd <- ggplot(d_d, aes(z, kind, colour = kind)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(position = position_jitter(height = .2, width = 0), size = 1, alpha = .55) +
  stat_summary(fun = median, geom = "point", colour = "black", shape = 18, size = 2.6) +
  scale_colour_manual(values = c(ligand = BLUE, control = GREY), guide = "none") +
  facet_wrap(~radius) +
  labs(x = "z: TNFRSF12A+ minus TNFRSF12A- oncofetal cells, ligand+ macrophage neighbours",
       y = NULL,
       title = "Conditioning on the receptor does not recover a niche",
       subtitle = "one point per tumour x gene; black diamond, median") +
  theme_pub()

EC4 <- (tag(pa, "a") | tag(pb, "b")) / tag(pc, "c") / tag(pd, "d") +
  plot_layout(heights = c(1, 1.15, .8))
ggsave(file.path(FIGOUT, "Fig_EC4_receptor_state_and_audit.pdf"), EC4, width = 10, height = 10)
ggsave(file.path(FIGOUT, "Fig_EC4_receptor_state_and_audit.png"), EC4, width = 10, height = 10, dpi = 300)
cat("written Fig_EC4\n")
