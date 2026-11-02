# Q2: cellular sources of TWEAK (TNFSF12), TGFB1 and IL36G in the early-CRC
# microenvironment, and whether a TWEAK-TWEAKR circuit is detectable there.
#
# Data: Snippert 2026 early-stage CRC TME scRNA-seq (SORT-seq, plate-based),
#       2,409 cells, 5 patients, 3 regions (nor / core / inv). TME only - the
#       sort excluded tumour epithelium, so the receptor-bearing compartment is
#       NOT in this object. Receptor localisation is handled in 01 (GeoMx) and 03 (CosMx).
#
# Units: the patient is the unit for every test. Cell-level numbers are reported
#        as descriptives only.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))

suppressMessages({library(Seurat); library(dplyr); library(ggplot2); library(tidyr)})
set.seed(1)

s <- readRDS(file.path(EARLYCRC, "scRNAseq/earlycrc_tme_scrna_seurat.rds"))
md <- s@meta.data
md$cell <- rownames(md)
expr <- Seurat::GetAssayData(s, assay = "RNA", layer = "data")
cnt  <- Seurat::GetAssayData(s, assay = "RNA", layer = "counts")

cat(sprintf("cells=%d genes=%d patients=%d\n", ncol(s), nrow(s), length(unique(md$Patient))))

## ---- 1. Per cell type: detection rate and mean expression -------------------
genes <- intersect(GENES_OF_INTEREST, rownames(expr))
long <- lapply(genes, function(g) {
  data.frame(gene = g, cell = colnames(expr),
             expr = as.numeric(expr[g, ]), pos = as.numeric(cnt[g, ]) > 0)
}) %>% bind_rows() %>% left_join(md[, c("cell", "celltypes", "tumor_region", "Patient")], by = "cell")

ct_summary <- long %>%
  group_by(gene, celltypes) %>%
  summarise(n_cells = n(), n_pos = sum(pos), pct_pos = 100 * mean(pos),
            mean_expr = mean(expr), .groups = "drop") %>%
  arrange(gene, desc(pct_pos))
write_tsv(ct_summary, "Q2_celltype_expression_summary.tsv")

## ---- 2. Share of all ligand-positive cells contributed by each cell type ----
# "Where does the ligand come from?" expressed as a composition, which is what a
# source-decomposition claim actually requires.
share <- long %>% filter(pos) %>%
  group_by(gene, celltypes) %>% summarise(n_pos = n(), .groups = "drop_last") %>%
  mutate(share_pct = 100 * n_pos / sum(n_pos)) %>% ungroup() %>%
  arrange(gene, desc(share_pct))
write_tsv(share, "Q2_ligand_source_share.tsv")

## ---- 3. Patient-level test: is any cell type the dominant TWEAK source? -----
# Per patient x cell type detection rate, then Friedman-free simple summary:
# how many of the 5 patients place each cell type in the top rank.
pat_ct <- long %>%
  group_by(gene, Patient, celltypes) %>%
  summarise(n_cells = n(), pct_pos = 100 * mean(pos), .groups = "drop") %>%
  filter(n_cells >= 5)
top_rank <- pat_ct %>% filter(pct_pos > 0) %>% group_by(gene, Patient) %>%
  slice_max(pct_pos, n = 1, with_ties = TRUE) %>% ungroup() %>%
  count(gene, celltypes, name = "n_patients_top") %>% arrange(gene, desc(n_patients_top))
write_tsv(pat_ct, "Q2_patient_celltype_detection.tsv")
write_tsv(top_rank, "Q2_top_source_per_patient.tsv")

## ---- 4. Region comparison, patient-paired ----------------------------------
# Per patient x region mean expression across all TME cells; paired Wilcoxon
# across patients for inv vs core (the contrast the paper's model rests on).
pat_reg <- long %>% group_by(gene, Patient, tumor_region) %>%
  summarise(mean_expr = mean(expr), pct_pos = 100 * mean(pos), n = n(), .groups = "drop")
write_tsv(pat_reg, "Q2_patient_region_expression.tsv")

reg_test <- lapply(genes, function(g) {
  w <- pat_reg %>% filter(gene == g) %>%
    select(Patient, tumor_region, mean_expr) %>%
    pivot_wider(names_from = tumor_region, values_from = mean_expr)
  if (!all(c("core", "inv") %in% names(w))) return(NULL)
  w <- w[complete.cases(w[, c("core", "inv")]), ]
  if (nrow(w) < 3) return(data.frame(gene = g, n_pairs = nrow(w), median_diff = NA, p = NA))
  tt <- suppressWarnings(wilcox.test(w$inv, w$core, paired = TRUE))
  data.frame(gene = g, n_pairs = nrow(w),
             median_diff_inv_minus_core = median(w$inv - w$core), p = tt$p.value)
}) %>% bind_rows()
reg_test$q_BH <- p.adjust(reg_test$p, "BH")
write_tsv(reg_test, "Q2_region_paired_test.tsv")

## ---- 5. Is there a TWEAK-TWEAKR circuit inside the TME? --------------------
# Both partners must be detectable for an intra-TME circuit to be possible.
circuit <- ct_summary %>% filter(gene %in% c("TNFSF12", "TNFRSF12A")) %>%
  select(gene, celltypes, n_cells, pct_pos, mean_expr) %>%
  pivot_wider(names_from = gene, values_from = c(pct_pos, mean_expr, n_cells)) %>%
  arrange(desc(pct_pos_TNFSF12))
write_tsv(circuit, "Q2_tweak_tweakr_circuit_by_celltype.tsv")

## ---- 6. Figures -------------------------------------------------------------
plot_genes <- c("TNFSF12", "TGFB1", "IL36G", "TNFRSF12A", "TGFB3")
p1 <- ct_summary %>% filter(gene %in% plot_genes) %>%
  mutate(celltypes = factor(celltypes, levels = rev(sort(unique(celltypes))))) %>%
  ggplot(aes(celltypes, pct_pos)) +
  geom_col(fill = GREY) + coord_flip() + facet_wrap(~gene, nrow = 1, scales = "free_x") +
  labs(x = NULL, y = "% of cells with >=1 count",
       title = "Ligand and receptor detection by TME cell type (early-stage CRC scRNA-seq)",
       subtitle = sprintf("%d cells, %d patients; cell-level descriptives", ncol(s), length(unique(md$Patient)))) +
  theme_bw(base_size = 9)
ggsave(file.path(FIGD, "Q2_detection_by_celltype.pdf"), p1, width = 12, height = 5)

p2 <- share %>% filter(gene %in% c("TNFSF12", "TGFB1", "IL36G")) %>%
  group_by(gene) %>% slice_max(share_pct, n = 10) %>% ungroup() %>%
  ggplot(aes(reorder(celltypes, share_pct), share_pct)) +
  geom_col(fill = RED) + coord_flip() + facet_wrap(~gene, scales = "free") +
  labs(x = NULL, y = "% of all ligand-positive cells",
       title = "Source decomposition of ligand-positive cells") +
  theme_bw(base_size = 9)
ggsave(file.path(FIGD, "Q2_source_share.pdf"), p2, width = 10, height = 4)

p3 <- pat_reg %>% filter(gene %in% plot_genes) %>%
  mutate(tumor_region = factor(tumor_region, c("nor", "core", "inv"))) %>%
  ggplot(aes(tumor_region, mean_expr, group = Patient)) +
  geom_line(colour = GREY) + geom_point(aes(colour = tumor_region), size = 2) +
  scale_colour_manual(values = c(nor = GREY, core = BLUE, inv = RED), guide = "none") +
  facet_wrap(~gene, nrow = 1, scales = "free_y") +
  labs(x = NULL, y = "mean normalised expression (all TME cells)",
       title = "Patient-paired regional expression", subtitle = "one line per patient") +
  theme_bw(base_size = 9)
ggsave(file.path(FIGD, "Q2_region_paired.pdf"), p3, width = 11, height = 3.2)

cat("\n--- TNFSF12 top sources (cell level) ---\n")
print(head(ct_summary %>% filter(gene == "TNFSF12"), 8))
cat("\n--- TNFRSF12A in TME ---\n")
print(head(ct_summary %>% filter(gene == "TNFRSF12A"), 8))
cat("\n--- region paired test ---\n"); print(reg_test)
cat("\ndone\n")
