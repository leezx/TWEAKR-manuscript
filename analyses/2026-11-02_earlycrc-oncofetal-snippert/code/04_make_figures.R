# Publication-style figures for the early-CRC (Snippert 2026) replication.
#
# Reads only the frozen result tables written by scripts 01-03b; it performs no
# new statistics, so the figures cannot drift from the numbers in docs/Results.md.
# Three figures:
#   EC1  regional architecture of the stem programmes (GeoMx)
#   EC2  the TWEAK axis: receptor position and ligand sources (GeoMx + scRNA-seq)
#   EC3  co-emergence and colocalisation (CosMx), with the control-gene test
#
# Conventions: red = revival/fetal/high, blue = proliferative/core/low,
# grey = control or not significant. One measure per axis, no dual axes.
# Every panel states its unit of analysis in the caption (docs/Results.md).

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

REGS <- c("nor", "ade", "core", "inv")
REGLAB <- c(nor = "normal", ade = "adenoma", core = "core", inv = "front")
REGCOL <- c(nor = "#BFBFBF", ade = "#9970AB", core = BLUE, inv = RED)

# display names, so the figures do not carry internal set identifiers
NICE <- c(proCSC = "proCSC", revCSC = "revCSC", Lgr5CSC = "Lgr5 CSC",
          proliferation = "proliferation", YAP_regeneration = "YAP regeneration",
          revival_Ayyaz = "revival stem", fetal_Yui = "fetal intestine",
          IFA_core = "fetal-intestinal axis", TRA_core = "trophoblast axis",
          EVT_core = "EVT", placenta_troph = "placenta trophoblast")
ORDER <- names(NICE)

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

## ===========================================================================
## Figure EC1 - regional architecture
## ===========================================================================
prof <- rd("Q1_geomx_patient_region_profile.tsv")
st   <- rd("Q1_geomx_region_stats.tsv")

# (a) patient-paired profiles across the four regions, tumour epithelium, CTA
sel_a <- c("proCSC", "revCSC", "proliferation", "YAP_regeneration", "IFA_core")
pa <- prof %>% filter(exp == "exp1", segment == "PanCK+", signature %in% sel_a) %>%
  mutate(region = factor(region, REGS, REGLAB),
         signature = factor(NICE[signature], NICE[sel_a])) %>%
  ggplot(aes(region, score)) +
  geom_line(aes(group = patient), colour = "grey75", linewidth = .35) +
  geom_point(aes(colour = region), size = 1.3) +
  stat_summary(fun = mean, geom = "line", aes(group = 1), colour = "black", linewidth = .7) +
  scale_colour_manual(values = setNames(REGCOL, REGLAB), guide = "none") +
  facet_wrap(~signature, nrow = 1, scales = "free_y") +
  labs(x = NULL, y = "signature score", title = "Tumour epithelium across tumour architecture",
       subtitle = "one grey line per patient (n = 10); black line, cohort mean") +
  theme_pub() + theme(axis.text.x = element_text(angle = 45, hjust = 1))

# (b) invasive front - core effect, calibrated against matched random gene sets
pb_d <- st %>% filter(exp == "exp1", segment == "PanCK+") %>%
  mutate(signature = factor(NICE[signature], rev(NICE[ORDER])),
         call = ifelse(p_matched_null < 0.05,
                       ifelse(mean_diff_inv_core > 0, "up", "down"), "not significant"))
pb <- ggplot(pb_d, aes(mean_diff_inv_core, signature, fill = call)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_col(width = .68) +
  geom_text(aes(label = sprintf("%d/%d", n_patients_positive, n_patients),
                hjust = ifelse(mean_diff_inv_core > 0, -0.15, 1.15)),
            size = 2.4, colour = "grey25") +
  scale_fill_manual(values = c(up = RED, down = BLUE, `not significant` = GREY), name = NULL) +
  scale_x_continuous(expand = expansion(mult = .18)) +
  labs(x = "invasive front - core (patient-level)", y = NULL,
       title = "Front versus core, matched-null calibrated",
       subtitle = "labels: patients moving up, of 10; fill: passes expression-matched null") +
  theme_pub() + theme(legend.position = "bottom")

# (c) the same effect in epithelium versus microenvironment
pc_d <- st %>% filter(exp == "exp1") %>%
  mutate(signature = factor(NICE[signature], rev(NICE[ORDER])),
         segment = factor(segment, c("PanCK+", "PanCK-"),
                          c("tumour epithelium", "microenvironment")))
pc <- ggplot(pc_d, aes(mean_diff_inv_core, signature)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(aes(colour = p_matched_null < 0.05, size = -log10(p_matched_null))) +
  scale_colour_manual(values = c(`TRUE` = RED, `FALSE` = GREY),
                      labels = c("no", "yes"), name = "passes null") +
  scale_size_continuous(range = c(.8, 3), name = expression(-log[10]~P)) +
  facet_wrap(~segment) +
  labs(x = "invasive front - core (patient-level)", y = NULL,
       title = "The shift is confined to the epithelium") +
  theme_pub()

# (d) the trophoblast axes, both cohorts, both contrasts
pd_d <- bind_rows(
    st %>% filter(segment == "PanCK+") %>% mutate(cohort = exp),
    rd("Q1_geomx_region_stats_exp2_T1_only.tsv") %>% filter(segment == "PanCK+") %>%
      mutate(cohort = "exp2_T1_only")) %>%
  filter(signature %in% c("TRA_core", "placenta_troph", "EVT_core", "revCSC", "IFA_core")) %>%
  mutate(signature = factor(NICE[signature], NICE[c("revCSC", "IFA_core", "TRA_core",
                                                    "placenta_troph", "EVT_core")]),
         cohort = factor(cohort, c("exp1", "exp2", "exp2_T1_only"),
                         c("CTA (n = 10)", "WTA (n = 10)", "WTA, T1 only (n = 9)")),
         family = ifelse(signature %in% NICE[c("revCSC", "IFA_core")],
                         "fetal / revival", "trophoblast"))
pd <- ggplot(pd_d, aes(mean_diff_inv_core, cohort, colour = family)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(size = 2) +
  geom_text(aes(label = sprintf("%d/%d", n_patients_positive, n_patients)),
            vjust = -1.1, size = 2.2, colour = "grey25", show.legend = FALSE) +
  scale_colour_manual(values = c(`fetal / revival` = RED, trophoblast = GREY), name = NULL) +
  scale_x_continuous(limits = range(pd_d$mean_diff_inv_core) + c(-.012, .012)) +
  scale_y_discrete(expand = expansion(add = c(.5, .95))) +
  facet_wrap(~signature, nrow = 1) +
  labs(x = "invasive front - core (patient-level)", y = NULL,
       title = "No trophoblast programme is enriched at the invasive front",
       subtitle = "common x scale across panels; labels: patients moving up") +
  theme_pub() + theme(legend.position = "bottom")

EC1 <- (tag(pa, "a")) / (tag(pb, "b") | tag(pc, "c")) / (tag(pd, "d")) +
  plot_layout(heights = c(1, 1.25, .95))
ggsave(file.path(FIGOUT, "Fig_EC1_regional_architecture.pdf"), EC1, width = 9.5, height = 10.5)
ggsave(file.path(FIGOUT, "Fig_EC1_regional_architecture.png"), EC1, width = 9.5, height = 10.5, dpi = 300)

## ===========================================================================
## Figure EC2 - the TWEAK axis
## ===========================================================================
gx <- rd("Q1_geomx_tweak_axis_genes.tsv")
gs <- rd("Q1_geomx_tweak_axis_gene_stats.tsv")
GENES <- c("MMP7", "LAMC2", "TNFRSF12A", "TGFB3", "TGFB1", "TNFSF12")

# (a) patient-paired core -> front for each gene, tumour epithelium, CTA
ga <- gx %>% filter(exp == "exp1", segment == "PanCK+", gene %in% GENES,
                    region %in% c("core", "inv")) %>%
  group_by(gene, patient, region) %>% summarise(expr = mean(expr), .groups = "drop") %>%
  mutate(region = factor(region, c("core", "inv"), c("core", "front")),
         gene = factor(gene, GENES))
ga_lab <- gs %>% filter(exp == "exp1", segment == "PanCK+", gene %in% GENES) %>%
  mutate(gene = factor(gene, GENES),
         lab = sprintf("%+.2f  |  %d/10  |  q = %.3f", mean_diff_inv_core, n_patients_positive, q_BH))
pa2 <- ggplot(ga, aes(region, expr)) +
  geom_line(aes(group = patient), colour = "grey75", linewidth = .35) +
  geom_point(aes(colour = region), size = 1.3) +
  geom_text(data = ga_lab, aes(x = 1.5, y = Inf, label = lab), vjust = 1.4,
            size = 2.2, colour = "grey25", inherit.aes = FALSE) +
  scale_colour_manual(values = c(core = BLUE, front = RED), guide = "none") +
  facet_wrap(~gene, nrow = 1, scales = "free_y") +
  scale_y_continuous(expand = expansion(mult = c(.05, .22))) +
  labs(x = NULL, y = "normalised expression (log)",
       title = "The receptor tracks the oncofetal front; the ligand does not",
       subtitle = "GeoMx CTA, tumour epithelium, patient-paired (n = 10)") +
  theme_pub()

# (b) detection by microenvironment cell type: a ligand with sources, and one without
ct <- rd("Q2_celltype_expression_summary.tsv")
ord <- ct %>% filter(gene == "TGFB1") %>% arrange(pct_pos) %>% pull(celltypes)
pb2 <- ct %>% filter(gene %in% c("TNFSF12", "TGFB1", "IL36G")) %>%
  mutate(celltypes = factor(celltypes, ord),
         gene = factor(gene, c("TNFSF12", "TGFB1", "IL36G"),
                       c("TNFSF12 (TWEAK)", "TGFB1", "IL36G"))) %>%
  ggplot(aes(pct_pos, celltypes)) +
  geom_segment(aes(x = 0, xend = pct_pos, yend = celltypes), colour = "grey80", linewidth = .4) +
  geom_point(aes(colour = gene), size = 1.6) +
  scale_colour_manual(values = c(RED, BLUE, GREY), guide = "none") +
  facet_wrap(~gene, nrow = 1) +
  labs(x = "% of cells with >= 1 count", y = NULL,
       title = "A ligand with sources, a ligand without, and one that is absent",
       subtitle = "cell types ordered by TGFB1 detection; early-CRC microenvironment scRNA-seq, 2,409 cells, 5 patients") +
  theme_pub() + theme(panel.grid.major.y = element_blank())

# (c) source decomposition
sh <- rd("Q2_ligand_source_share.tsv")
ord_c <- sh %>% filter(gene == "TNFSF12") %>% arrange(share_pct) %>% pull(celltypes)
top_c <- sh %>% filter(gene == "TNFSF12") %>% slice_max(share_pct, n = 8) %>% pull(celltypes)
pc2 <- sh %>% filter(gene %in% c("TNFSF12", "TGFB1"), celltypes %in% top_c) %>%
  mutate(celltypes = factor(celltypes, ord_c),
         gene = factor(gene, c("TNFSF12", "TGFB1"), c("TNFSF12 (TWEAK)", "TGFB1"))) %>%
  ggplot(aes(share_pct, celltypes, fill = gene)) +
  geom_col(width = .68) +
  scale_fill_manual(values = c(RED, BLUE), guide = "none") +
  facet_wrap(~gene) +
  labs(x = "% of all ligand-positive cells", y = NULL,
       title = "Where the ligand-positive cells are",
       subtitle = "top eight TNFSF12 sources, same order in both panels; macrophages supply 7.1% of TNFSF12+ cells") +
  theme_pub() + theme(panel.grid.major.y = element_blank())

EC2 <- tag(pa2, "a") / (tag(pb2, "b")) / (tag(pc2, "c")) + plot_layout(heights = c(1, 1.15, .85))
ggsave(file.path(FIGOUT, "Fig_EC2_tweak_axis.pdf"), EC2, width = 9.5, height = 10)
ggsave(file.path(FIGOUT, "Fig_EC2_tweak_axis.png"), EC2, width = 9.5, height = 10, dpi = 300)

## ===========================================================================
## Figure EC3 - co-emergence and colocalisation
## ===========================================================================
ps <- rd("Q3_patient_summary.tsv")
STAGE <- c("im", "T1.sm1", "T1.sm3")
STAGECOL <- c(im = GREY, T1.sm1 = BLUE, T1.sm3 = RED)

# (a) what does rise with pseudostage, and what does not
pa3_d <- ps %>%
  select(patient, stage, `oncofetal cells\n(% of tumour epithelium)` = pct_oncofetal_of_epi,
         `TWEAK+ macrophages\n(% of macrophages)` = TNFSF12_pos_pct_mac,
         `TWEAKR+ cells\n(% of all cells)` = TNFRSF12A_pos_pct_all) %>%
  pivot_longer(-c(patient, stage), names_to = "measure", values_to = "pct") %>%
  mutate(stage = factor(stage, STAGE))
pa3_lab <- rd("Q3_coemergence.tsv") %>%
  filter(measure %in% c("pct_oncofetal_of_epi (control)", "TNFSF12_pos_pct_mac",
                        "TNFRSF12A_pos_pct_all")) %>%
  mutate(measure = c(`pct_oncofetal_of_epi (control)` = "oncofetal cells\n(% of tumour epithelium)",
                     TNFSF12_pos_pct_mac = "TWEAK+ macrophages\n(% of macrophages)",
                     TNFRSF12A_pos_pct_all = "TWEAKR+ cells\n(% of all cells)")[measure],
         lab = sprintf("rho = %+.2f, P = %.3f", rho_vs_stage, p_vs_stage))
pa3 <- ggplot(pa3_d, aes(stage, pct)) +
  geom_point(aes(colour = stage), size = 2, position = position_jitter(width = .1, height = 0)) +
  geom_text(data = pa3_lab, aes(x = 2, y = Inf, label = lab), vjust = 1.5, size = 2.3,
            colour = "grey25", inherit.aes = FALSE) +
  scale_colour_manual(values = STAGECOL, guide = "none") +
  scale_y_continuous(expand = expansion(mult = c(.08, .25))) +
  facet_wrap(~measure, scales = "free_y") +
  labs(x = NULL, y = "% of cells",
       title = "Co-emergence across 11 pseudotimed early CRCs",
       subtitle = "the oncofetal state rises with substage; the TWEAK+ macrophage fraction does not") +
  theme_pub()

# (b) colocalisation per tumour, authors' oncofetal label
cz <- rd("Q3_colocalisation_per_patient.tsv") %>% filter(oncofetal_def == "oncofetal")
cs <- rd("Q3_colocalisation_summary.tsv") %>% filter(oncofetal_def == "oncofetal")
pb3 <- cz %>% mutate(source = factor(source, c("macrophage", "all_cells"),
                                     c("macrophage sources", "any cell type"))) %>%
  ggplot(aes(z, fct_rev(factor(ligand)))) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(colour = GREY, size = 1.5, position = position_jitter(height = .12, width = 0)) +
  stat_summary(fun = median, geom = "point", colour = RED, size = 2.6, shape = 18) +
  facet_wrap(~source) +
  labs(x = "z versus field-permuted ligand label", y = NULL,
       title = "No ligand-specific proximity to oncofetal cells",
       subtitle = "grey, one tumour (n = 9); red diamond, median") +
  theme_pub()

# (c) the control-gene test that invalidates the score-threshold version
cg <- rd("Q3b_control_gene_colocalisation.tsv") %>%
  mutate(oncofetal_def = factor(oncofetal_def, c("oncofetal", "oncofetal_revCSC"),
           c("oncofetal = authors' label", "oncofetal = revCSC score decile")),
         kind = factor(kind, c("ligand", "control"),
                       c("ligands", "detection-matched\ncontrol genes")))
pc3 <- ggplot(cg, aes(z, kind, colour = kind)) +
  geom_vline(xintercept = 0, colour = "grey60", linewidth = .3) +
  geom_point(position = position_jitter(height = .22, width = 0), size = 1, alpha = .55) +
  stat_summary(fun = median, geom = "point", colour = "black", size = 2.6, shape = 18) +
  scale_colour_manual(values = c(RED, GREY), guide = "none") +
  facet_wrap(~oncofetal_def, scales = "free_x") +
  labs(x = "z versus field-permuted label", y = NULL,
       title = "Control genes score as high as the ligands, so the positive result is an artefact",
       subtitle = "one point per tumour x gene; black diamond, median") +
  theme_pub()

EC3 <- tag(pa3, "a") / tag(pb3, "b") / tag(pc3, "c") + plot_layout(heights = c(1, .85, .8))
ggsave(file.path(FIGOUT, "Fig_EC3_coemergence_colocalisation.pdf"), EC3, width = 9, height = 9.5)
ggsave(file.path(FIGOUT, "Fig_EC3_coemergence_colocalisation.png"), EC3, width = 9, height = 9.5, dpi = 300)

cat("written:\n"); print(list.files(FIGOUT, pattern = "^Fig_EC"))
