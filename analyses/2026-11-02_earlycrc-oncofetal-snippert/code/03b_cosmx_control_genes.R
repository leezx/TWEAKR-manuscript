# Q3, control: script 03 found that when the ligand+ source is "all cells" and
# oncofetal cells are defined by a revCSC score decile, EVERY ligand - TNFSF12,
# TGFB1, TGFB3 and even IL36G - shows strongly positive, highly significant
# proximity to oncofetal cells (median z 4.6-7.0, 11/11 tumours). Four unrelated
# ligands cannot all be specifically recruited to the same cells. The obvious
# alternative is that cells scoring high on any transcriptional signature sit in
# regions of higher overall transcript detection, so they have more neighbours
# positive for anything.
#
# This script tests that directly: run the identical colocalisation test on
# control genes that are NOT ligands, matched to TNFSF12 on detection rate. If
# the controls land in the same z range as the ligands, the "positive" result is
# a detection-density artifact and must not be reported as colocalisation.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({
  library(Seurat); library(Matrix); library(RANN); library(dplyr); library(tidyr); library(ggplot2)
})
set.seed(20261102)

CX <- file.path(ZENODO, "extracted/Nanostring_CosMx_exp2")
CACHE2 <- file.path(ZENODO, "cosmx_exp2_control_genes.rds")
RADIUS_UM <- 50; N_PERM <- 100; N_CONTROL <- 12
LIGANDS <- c("TNFSF12", "TGFB1", "IL36G", "TGFB3")
SIGS <- load_signatures()

if (!file.exists(CACHE2)) {
  message("extracting control genes from the Seurat object ...")
  so <- readRDS(file.path(CX, "seurat/cosmx_exp2_seuratObject.rds"))
  cnt <- Seurat::GetAssayData(so, assay = DefaultAssay(so), layer = "counts")
  # detection rate per gene, computed from the sparse structure directly
  # (`cnt > 0` would densify a 6,175 x 1.26M matrix)
  det <- setNames(tabulate(cnt@i + 1L, nbins = nrow(cnt)) / ncol(cnt), rownames(cnt))
  used <- unique(c(LIGANDS, "TNFRSF12A", unlist(SIGS, use.names = FALSE)))
  # candidates: not a ligand, not in any scored signature, detection within
  # +/-20% of TNFSF12's, so the permutation null has comparable sparsity
  target <- det[["TNFSF12"]]
  cand <- names(det)[!(names(det) %in% used) &
                     det >= target * 0.8 & det <= target * 1.2]
  ctrl <- sample(cand, min(N_CONTROL, length(cand)))
  saveRDS(list(counts = cnt[c(LIGANDS, ctrl), , drop = FALSE],
               detection = det[c(LIGANDS, ctrl)], controls = ctrl,
               n_candidates = length(cand)), CACHE2)
  rm(so, cnt); gc()
}
C <- readRDS(CACHE2)
cat(sprintf("control genes (%d of %d candidates): %s\n",
            length(C$controls), C$n_candidates, paste(C$controls, collapse = ", ")))
print(round(C$detection, 4))

D <- readRDS(file.path(ZENODO, "cosmx_exp2_compact.rds"))
md <- D$meta
md$celltype <- as.character(md$cellType)
md$patient <- as.character(md$patient_ID)
md$x <- as.numeric(md$x_slide_mm) * 1000
md$y <- as.numeric(md$y_slide_mm) * 1000
md$fov <- as.character(md$fov)
md$is_epi <- md$celltype %in% c("CRC", "oncofetal")
md$oncofetal <- md$celltype == "oncofetal"
cpm <- Matrix::t(Matrix::t(D$counts) / pmax(D$total, 1)) * 1e4
g <- intersect(SIGS$revCSC, rownames(cpm))
md$revCSC <- Matrix::colMeans(log1p(cpm)[g, , drop = FALSE])
md <- md %>% group_by(patient) %>%
  mutate(oncofetal_revCSC = is_epi &
           revCSC >= quantile(revCSC[is_epi], 0.90, na.rm = TRUE)) %>% ungroup()

test_gene <- function(dp, pos, onco) {
  epi <- which(dp$is_epi)
  if (sum(onco[epi]) < 20 || sum(!onco[epi]) < 20 || sum(pos) < 10) return(NULL)
  nn <- RANN::nn2(dp[, c("x", "y")], dp[epi, c("x", "y")],
                  k = 200, searchtype = "radius", radius = RADIUS_UM)
  idx <- nn$nn.idx
  nz <- which(idx > 0, arr.ind = TRUE)
  M <- Matrix::sparseMatrix(i = nz[, 1], j = idx[idx > 0], x = 1,
                            dims = c(nrow(idx), nrow(dp)))
  o <- onco[epi]
  stat <- function(lab) { v <- as.numeric(M %*% lab); mean(v[o]) - mean(v[!o]) }
  d_obs <- stat(pos)
  grp <- split(seq_len(nrow(dp)), dp$fov)
  d_null <- vapply(seq_len(N_PERM), function(i) {
    lab <- pos
    for (ix in grp) if (length(ix) > 1) lab[ix] <- sample(pos[ix])
    stat(lab)
  }, numeric(1))
  data.frame(diff_obs = d_obs, null_mean = mean(d_null), null_sd = sd(d_null),
             z = (d_obs - mean(d_null)) / sd(d_null))
}

res <- list()
for (p in unique(md$patient)) {
  k <- md$patient == p
  dp <- data.frame(x = md$x[k], y = md$y[k], fov = md$fov[k],
                   is_epi = md$is_epi[k])
  ok <- is.finite(dp$x) & is.finite(dp$y)
  dp <- dp[ok, ]
  cells <- which(k)[ok]
  for (gn in rownames(C$counts)) {
    pos <- as.numeric(C$counts[gn, cells]) > 0
    for (oc in c("oncofetal", "oncofetal_revCSC")) {
      onco <- md[[oc]][cells]
      r <- test_gene(dp, pos, onco)
      if (!is.null(r)) res[[length(res) + 1]] <- cbind(
        data.frame(patient = p, gene = gn,
                   kind = ifelse(gn %in% LIGANDS, "ligand", "control"),
                   oncofetal_def = oc, pct_pos = 100 * mean(pos)), r)
    }
  }
  cat(".", sep = "")
}
cat("\n")
res <- bind_rows(res)
write_tsv(res, "Q3b_control_gene_colocalisation.tsv")

summ <- res %>% group_by(oncofetal_def, kind, gene) %>%
  summarise(n_patients = n(), median_z = median(z), n_pos_z = sum(z > 0), .groups = "drop") %>%
  arrange(oncofetal_def, desc(median_z))
write_tsv(summ, "Q3b_control_gene_summary.tsv")

cmp <- res %>% group_by(oncofetal_def, kind) %>%
  summarise(n = n(), median_z = median(z), q25 = quantile(z, .25),
            q75 = quantile(z, .75), .groups = "drop")
write_tsv(cmp, "Q3b_ligand_vs_control_z.tsv")
cat("\n=== ligands vs detection-matched control genes ===\n"); print(as.data.frame(cmp), digits = 3)
cat("\n=== per gene ===\n"); print(as.data.frame(summ), digits = 3)

pl <- res %>% ggplot(aes(kind, z, colour = kind)) +
  geom_hline(yintercept = 0, colour = GREY) +
  geom_jitter(width = .2, alpha = .6, size = 1) +
  scale_colour_manual(values = c(ligand = RED, control = GREY), guide = "none") +
  facet_wrap(~oncofetal_def) +
  labs(x = NULL, y = "z vs FOV-permuted label",
       title = "Are the ligands special? Detection-matched control genes run through the same test",
       subtitle = "one point per tumour x gene") +
  theme_bw(base_size = 9)
ggsave(file.path(FIGD, "Q3b_ligand_vs_control.pdf"), pl, width = 8, height = 4)
cat("\ndone\n")
