# Q3: do TWEAK+ macrophages co-emerge and colocalise with oncofetal tumour cells,
# and do TGFB1+ and IL36G+ cells behave the same way?
#
# Data: Snippert 2026 CosMx run 2 (Zenodo 17671259) - the dataset behind Fig. 5.
#   ~1.25M cells, 6,175-gene panel, 11 non-metastatic early CRCs captured at three
#   pseudotimed substages: intramucosal (im, n=3) -> T1 sm1 (n=5) -> T1 sm3 (n=3).
#   This is the only cohort in the paper that can separate "appears at the same
#   time" from "sits in the same place".
#
# Two distinct claims are tested separately, because they fail independently:
#   co-emergence  - per patient, does the abundance of ligand+ cells track the
#                   abundance of oncofetal tumour cells across the 11 tumours?
#   colocalisation- within a tumour, are oncofetal tumour cells closer to ligand+
#                   cells than other tumour cells are? The null permutes the
#                   ligand+ label among cells of the SAME type within the same FOV,
#                   so a positive result means ligand-specific proximity and not
#                   merely proximity to macrophages (or to fibroblasts, etc.).
#
# Units: the patient (n = 11) for every inferential statement. Cell-level counts
#        are descriptive.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({
  library(Seurat); library(Matrix); library(RANN)
  library(dplyr); library(tidyr); library(ggplot2)
})
set.seed(20261102)

CX <- file.path(ZENODO, "extracted/Nanostring_CosMx_exp2")
RADIUS_UM <- 50      # matches the neighbourhood radius the authors used
N_PERM    <- 200
LIGANDS   <- c("TNFSF12", "TGFB1", "IL36G", "TGFB3")
SIGS      <- load_signatures()
CACHE     <- file.path(ZENODO, "cosmx_exp2_compact.rds")

## ---- 1. compact extraction (done once; the full object is ~2 GB) -----------
if (!file.exists(CACHE)) {
  message("building compact cache from the Seurat object ...")
  so <- readRDS(file.path(CX, "seurat/cosmx_exp2_seuratObject.rds"))
  cnt <- Seurat::GetAssayData(so, assay = DefaultAssay(so), layer = "counts")
  md <- so@meta.data; md$cell <- rownames(md)
  want <- unique(c(LIGANDS, "TNFRSF12A",
                   unlist(SIGS[c("revCSC", "proCSC", "IFA_core", "TRA_core",
                                 "placenta_troph", "EVT_core")], use.names = FALSE)))
  keep <- intersect(want, rownames(cnt))
  saveRDS(list(counts = cnt[keep, , drop = FALSE],
               total = Matrix::colSums(cnt),
               meta = md, genes_on_panel = rownames(cnt)), CACHE)
  rm(so, cnt); gc()
}
D <- readRDS(CACHE)
md <- D$meta
cat(sprintf("cells=%d  panel=%d genes  extracted=%d\n",
            nrow(md), length(D$genes_on_panel), nrow(D$counts)))

## report which genes of interest are actually on the 6k panel
on_panel <- data.frame(gene = c(LIGANDS, "TNFRSF12A"),
                       on_panel = c(LIGANDS, "TNFRSF12A") %in% D$genes_on_panel)
print(on_panel); write_tsv(on_panel, "Q3_genes_on_cosmx_panel.tsv")

## ---- 2. resolve annotation columns ----------------------------------------
pick <- function(...) { for (p in c(...)) { h <- grep(p, names(md), ignore.case = TRUE, value = TRUE)
                          if (length(h)) return(h[1]) }; stop("column not found: ", list(...)[[1]]) }
COL <- list(celltype = pick("^cellType$", "^predicted.cellType$"),
            patient  = pick("^patient_ID$", "^patient_ID_plot$"),
            stage    = pick("^tumorStage$"),
            fov      = pick("^fov$", "FOV"),
            epi      = pick("^cellTypeEpithelium$", "^cellType$"),
            x        = pick("^x_slide_mm$", "CenterX_global", "^x_global", "^CenterX"),
            y        = pick("^y_slide_mm$", "CenterY_global", "^y_global", "^CenterY"))
str(COL)
md$celltype <- as.character(md[[COL$celltype]])
md$patient  <- as.character(md[[COL$patient]])
md$stage    <- as.character(md[[COL$stage]])
md$fov      <- as.character(md[[COL$fov]])
# Put coordinates in microns so that RADIUS_UM really means microns.
# This release stores slide coordinates in mm; CosMx pixels are 0.12028 um.
scale_xy <- if (grepl("_mm$", COL$x)) 1000 else
            if (grepl("px", COL$x, ignore.case = TRUE)) 0.12028 else 1
cat(sprintf("coordinate columns: %s / %s  scale=%g um per unit\n", COL$x, COL$y, scale_xy))
md$x <- as.numeric(md[[COL$x]]) * scale_xy
md$y <- as.numeric(md[[COL$y]]) * scale_xy
print(table(md$stage, useNA = "ifany"))
print(sort(table(md$celltype), decreasing = TRUE)[1:25])

## ---- 3. per-cell scores and positive calls ---------------------------------
cpm <- Matrix::t(Matrix::t(D$counts) / pmax(D$total, 1)) * 1e4
logx <- log1p(cpm)

score_cells <- function(sig) {
  g <- intersect(SIGS[[sig]], rownames(logx))
  if (length(g) < 3) return(NULL)
  Matrix::colMeans(logx[g, , drop = FALSE])
}
md$revCSC <- score_cells("revCSC"); md$proCSC <- score_cells("proCSC")
md$IFA    <- score_cells("IFA_core")
for (lg in intersect(LIGANDS, rownames(D$counts)))
  md[[paste0(lg, "_pos")]] <- as.numeric(D$counts[lg, ]) > 0
if ("TNFRSF12A" %in% rownames(D$counts))
  md$TNFRSF12A_pos <- as.numeric(D$counts["TNFRSF12A", ]) > 0

## Epithelial compartment and the oncofetal call.
## The authors already sub-clustered the epithelium into CRC / oncofetal /
## normal-undefined epithelium and carried those labels into `cellType`; their
## label is the primary definition so that this analysis does not depend on a
## threshold we chose. The revCSC-decile call is kept as a
## sensitivity arm.
md$epi_class <- as.character(md[[COL$epi]])
md$is_epi <- md$epi_class %in% c("CRC", "oncofetal")       # tumour epithelium only
md$is_mac <- grepl("macrophage|myeloid|mono", md$celltype, ignore.case = TRUE)
md$oncofetal <- md$epi_class %in% "oncofetal"
md <- md %>% group_by(patient) %>%
  mutate(oncofetal_revCSC = is_epi &
           revCSC >= quantile(revCSC[is_epi], 0.90, na.rm = TRUE)) %>% ungroup()
cat(sprintf("tumour epithelium=%d  oncofetal (authors)=%d  oncofetal (revCSC decile)=%d  macrophages=%d\n",
            sum(md$is_epi), sum(md$oncofetal), sum(md$oncofetal_revCSC), sum(md$is_mac)))
cat("agreement between the two oncofetal calls (tumour epithelium only):\n")
print(table(authors = md$oncofetal[md$is_epi], revCSC = md$oncofetal_revCSC[md$is_epi]))

## ---- 4. co-emergence across the 11 tumours ---------------------------------
STAGE_ORDER <- c("im", "T1.sm1", "T1.sm3")
pat <- md %>% group_by(patient, stage) %>%
  summarise(n_cells = n(), n_epi = sum(is_epi), n_mac = sum(is_mac),
            pct_oncofetal_of_epi = 100 * sum(oncofetal) / pmax(sum(is_epi), 1),
            across(ends_with("_pos"), list(
              pct_all = ~100 * mean(.x, na.rm = TRUE),
              pct_mac = ~100 * mean(.x[is_mac], na.rm = TRUE)), .names = "{.col}_{.fn}"),
            .groups = "drop") %>%
  mutate(stage_rank = match(stage, STAGE_ORDER))
write_tsv(pat, "Q3_patient_summary.tsv")

coem <- lapply(grep("_pos_pct_(all|mac)$", names(pat), value = TRUE), function(v) {
  ok <- is.finite(pat[[v]]) & is.finite(pat$pct_oncofetal_of_epi)
  if (sum(ok) < 5) return(NULL)
  ct <- suppressWarnings(cor.test(pat[[v]][ok], pat$pct_oncofetal_of_epi[ok], method = "spearman"))
  tr <- suppressWarnings(cor.test(pat[[v]][ok], pat$stage_rank[ok], method = "spearman"))
  data.frame(measure = v, n_patients = sum(ok),
             rho_vs_oncofetal = unname(ct$estimate), p_vs_oncofetal = ct$p.value,
             rho_vs_stage = unname(tr$estimate), p_vs_stage = tr$p.value)
}) %>% bind_rows()
# the oncofetal fraction itself against pseudostage, as the positive control
oc <- suppressWarnings(cor.test(pat$pct_oncofetal_of_epi, pat$stage_rank, method = "spearman"))
coem <- bind_rows(coem, data.frame(measure = "pct_oncofetal_of_epi (control)",
  n_patients = nrow(pat), rho_vs_oncofetal = NA, p_vs_oncofetal = NA,
  rho_vs_stage = unname(oc$estimate), p_vs_stage = oc$p.value))
coem$q_vs_oncofetal_BH <- p.adjust(coem$p_vs_oncofetal, "BH")
coem$q_vs_stage_BH <- p.adjust(coem$p_vs_stage, "BH")
write_tsv(coem, "Q3_coemergence.tsv")
cat("\n=== co-emergence ===\n"); print(as.data.frame(coem), digits = 3)

## ---- 5. colocalisation with a ligand-label permutation null ----------------
#' For one patient and one ligand: count ligand+ cells of `source_type` within
#' RADIUS_UM of every epithelial cell, then compare oncofetal vs other epithelium.
#' The null permutes the ligand+ label among `source_type` cells inside each FOV,
#' which holds both tissue architecture and the number of ligand+ cells fixed.
coloc_one <- function(dp, ligand_col, source_mask, onco_col = "oncofetal", n_perm = N_PERM) {
  src <- which(source_mask)
  epi <- which(dp$is_epi)
  if (length(src) < 20 || length(epi) < 50) return(NULL)
  if (sum(dp[[ligand_col]][src]) < 10) return(NULL)
  nn <- RANN::nn2(dp[src, c("x", "y")], dp[epi, c("x", "y")],
                  k = min(length(src), 200), searchtype = "radius", radius = RADIUS_UM)
  idx <- nn$nn.idx                                  # 0 where no neighbour
  obs_lab <- dp[[ligand_col]][src]
  # incidence matrix (epithelial cell x source cell) built once; counting
  # ligand+ neighbours is then one sparse multiply per permutation.
  nz <- which(idx > 0, arr.ind = TRUE)
  M <- Matrix::sparseMatrix(i = nz[, 1], j = idx[idx > 0],
                            x = 1, dims = c(nrow(idx), length(src)))
  count_pos <- function(lab) as.numeric(M %*% lab)
  n_any <- Matrix::rowSums(M)
  obs <- count_pos(obs_lab)
  onco <- dp[[onco_col]][epi]
  if (sum(onco) < 20 || sum(!onco) < 20) return(NULL)
  stat <- function(v) mean(v[onco]) - mean(v[!onco])
  d_obs <- stat(obs)
  d_null <- vapply(seq_len(n_perm), function(i) {
    lab <- obs_lab
    perm <- unlist(lapply(split(seq_along(src), dp$fov[src]), function(ix) {
      if (length(ix) < 2) return(lab[ix]); sample(lab[ix])
    }), use.names = FALSE)
    lab[unlist(split(seq_along(src), dp$fov[src]), use.names = FALSE)] <- perm
    stat(count_pos(lab))
  }, numeric(1))
  data.frame(
    n_epi = length(epi), n_source = length(src), n_source_pos = sum(obs_lab),
    mean_neighbours_any = mean(n_any),
    mean_pos_oncofetal = mean(obs[onco]), mean_pos_other = mean(obs[!onco]),
    diff_obs = d_obs, null_mean = mean(d_null), null_sd = sd(d_null),
    z = (d_obs - mean(d_null)) / sd(d_null),
    p_perm = (sum(abs(d_null - mean(d_null)) >= abs(d_obs - mean(d_null))) + 1) / (n_perm + 1))
}

coloc <- list()
for (p in unique(md$patient)) {
  dp <- md %>% filter(patient == p) %>%
    select(x, y, fov, is_epi, is_mac, oncofetal, oncofetal_revCSC, celltype,
           ends_with("_pos")) %>%
    as.data.frame()
  dp <- dp[is.finite(dp$x) & is.finite(dp$y), ]
  for (lg in intersect(LIGANDS, sub("_pos$", "", grep("_pos$", names(dp), value = TRUE)))) {
    lc <- paste0(lg, "_pos")
    for (src_name in c("macrophage", "all_cells")) {
      mask <- if (src_name == "macrophage") dp$is_mac else rep(TRUE, nrow(dp))
      for (oc in c("oncofetal", "oncofetal_revCSC")) {
        r <- coloc_one(dp, lc, mask, onco_col = oc)
        if (!is.null(r)) coloc[[length(coloc) + 1]] <-
          cbind(data.frame(patient = p, ligand = lg, source = src_name,
                           oncofetal_def = oc), r)
      }
    }
  }
  cat(".", sep = "")
}
cat("\n")
coloc <- bind_rows(coloc)
write_tsv(coloc, "Q3_colocalisation_per_patient.tsv")

## patient-level summary: how many tumours show ligand-specific proximity?
coloc_sum <- coloc %>% group_by(ligand, source, oncofetal_def) %>%
  summarise(n_patients = n(), n_positive_z = sum(z > 0),
            n_sig = sum(p_perm < 0.05 & z > 0),
            median_z = median(z),
            p_sign = suppressWarnings(binom.test(sum(z > 0), n(), 0.5)$p.value),
            p_wilcox_z = suppressWarnings(wilcox.test(z)$p.value), .groups = "drop") %>%
  mutate(q_BH = p.adjust(p_wilcox_z, "BH")) %>% arrange(p_wilcox_z)
write_tsv(coloc_sum, "Q3_colocalisation_summary.tsv")
cat("\n=== colocalisation (patient-level) ===\n"); print(as.data.frame(coloc_sum), digits = 3)

## ---- 6. figures ------------------------------------------------------------
p1 <- pat %>% select(patient, stage, pct_oncofetal_of_epi,
                     matches("_pos_pct_all$")) %>%
  pivot_longer(matches("_pos_pct_all$"), names_to = "measure", values_to = "pct") %>%
  mutate(measure = sub("_pos_pct_all$", "", measure)) %>%
  ggplot(aes(pct, pct_oncofetal_of_epi, colour = stage)) +
  geom_point(size = 2) + facet_wrap(~measure, scales = "free_x") +
  scale_colour_manual(values = c(im = GREY, T1.sm1 = BLUE, T1.sm3 = RED)) +
  labs(x = "% of cells positive for the ligand", y = "% oncofetal of epithelium",
       title = "Co-emergence across 11 pseudotimed early CRCs (CosMx run 2)") +
  theme_bw(base_size = 9)
ggsave(file.path(FIGD, "Q3_coemergence.pdf"), p1, width = 9, height = 4)

p2 <- coloc %>% filter(oncofetal_def == "oncofetal") %>%
  ggplot(aes(ligand, z, colour = source)) +
  geom_hline(yintercept = 0, colour = GREY) +
  geom_point(position = position_dodge(width = .5), alpha = .8) +
  scale_colour_manual(values = c(macrophage = RED, all_cells = BLUE)) +
  labs(x = NULL, y = "z vs FOV-permuted ligand label",
       title = "Ligand-specific proximity to oncofetal tumour cells",
       subtitle = "one point per tumour; positive = ligand+ neighbours enriched around oncofetal cells") +
  theme_bw(base_size = 9)
ggsave(file.path(FIGD, "Q3_colocalisation.pdf"), p2, width = 7, height = 4)

cat("\ndone\n")
