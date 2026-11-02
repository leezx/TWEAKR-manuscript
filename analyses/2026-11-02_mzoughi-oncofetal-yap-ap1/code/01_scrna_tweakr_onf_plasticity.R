# Q1. Is TWEAKR (Tnfrsf12a) a marker of the oncofetal state in the A and AKSP
#     models, and does it track the lineage plasticity score of Fig. 1j-l?
#
# Data: GSE240129, three 10x libraries - WT organoids, A (Apc-null) and AKSP
#       (Apc/Kras/Smad4/Trp53) tumoroids.
#
# DESIGN NOTE, and the main limitation of this script.
# The deposited matrices carry a single barcode suffix per genotype: the three
# replicates reported in Supplementary Table S1a were pooled before deposition.
# There is therefore NO replicate label and no sample-level test is possible.
# Cell-level p-values here are pseudoreplicated and are not treated as evidence.
# What is treated as evidence instead:
#   1. effect sizes benchmarked against detection-matched control genes, which
#      holds the number of cells fixed, so the only thing that differs between
#      the receptor and a control gene is the gene;
#   2. consistency across the three independent libraries;
#   3. the authors' own differential expression for the neoplastic metacluster
#      (Supplementary Table S1c), which is independent of anything we compute.
#
# The oncofetal state is defined by the AUTHORS' mOnF signature (Table S1d),
# which does NOT contain Tnfrsf12a. The receptor IS a member of the project's
# revCSC set, so revCSC is never used to define the state here.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(Matrix); library(Seurat); library(dplyr)})
set.seed(SEED)

N_QUINTILE <- 5
N_CONTROL  <- 24     # detection-matched control genes
MIN_CELLS  <- 20     # per stratum, per side

EXT <- file.path(RAW, "GSE240129/ext")
LIBS <- c(WT = "GSM7682755_wt", A = "GSM7682756_a", AKSP = "GSM7682757_aksp")

## ---- load ------------------------------------------------------------------
read_lib <- function(pre) {
  m <- Matrix::readMM(gzfile(file.path(EXT, paste0(pre, "_matrix.mtx.gz"))))
  f <- read.delim(gzfile(file.path(EXT, paste0(pre, "_features.tsv.gz"))),
                  header = FALSE, stringsAsFactors = FALSE)
  b <- readLines(gzfile(file.path(EXT, paste0(pre, "_barcodes.tsv.gz"))))
  rownames(m) <- make.unique(f[[2]]); colnames(m) <- b
  as(m, "CsparseMatrix")
}
mats <- lapply(LIBS, read_lib)
genes <- Reduce(intersect, lapply(mats, rownames))
cnt <- do.call(cbind, lapply(names(mats), function(g) {
  x <- mats[[g]][genes, ]; colnames(x) <- paste0(g, "_", colnames(x)); x
}))
geno <- factor(sub("_.*", "", colnames(cnt)), levels = names(LIBS))
rm(mats); gc()

obj <- CreateSeuratObject(cnt, meta.data = data.frame(genotype = geno,
                                                      row.names = colnames(cnt)))
obj$percent_mt <- PercentageFeatureSet(obj, pattern = "^mt-")
keep <- obj$nFeature_RNA >= 500 & obj$nCount_RNA >= 1000 & obj$percent_mt < 25
cat(sprintf("QC: %d of %d cells kept (%.1f%%)\n", sum(keep), ncol(obj), 100 * mean(keep)))
obj <- obj[, keep]
obj <- NormalizeData(obj, verbose = FALSE)
print(table(obj$genotype))

## ---- scores, using the authors' definitions --------------------------------
SIGS <- load_signatures()
present <- lapply(SIGS, intersect, rownames(obj))
cat("\nsignature genes present in the panel:\n")
print(data.frame(set = names(SIGS), n_set = lengths(SIGS), n_present = lengths(present)),
      row.names = FALSE)

obj <- AddModuleScore(obj, features = present[lengths(present) >= 3],
                      name = "sig_", seed = SEED)
sn <- names(present)[lengths(present) >= 3]
colnames(obj@meta.data)[match(paste0("sig_", seq_along(sn)), colnames(obj@meta.data))] <- sn

# the Fig. 1j-l score, exactly as the paper defines it:
#   lineage plasticity = esophagus mucosa module - colon module
obj$lineage_plasticity <- obj$paper_esophagus - obj$paper_colon

md <- obj@meta.data
md$depth <- obj$nCount_RNA
md$quint <- ave(log(md$depth), md$genotype, FUN = function(x)
  as.integer(cut(rank(x, ties.method = "first"), breaks = N_QUINTILE, labels = FALSE)))
lg <- GetAssayData(obj, layer = "data")

## ---- detection-matched control genes ---------------------------------------
# Matched on the fraction of cells with a non-zero count, which is the quantity
# that drives spurious associations in sparse data.
det <- tabulate(GetAssayData(obj, layer = "counts")@i + 1L, nbins = nrow(obj)) / ncol(obj)
names(det) <- rownames(obj)
rec_det <- det[RECEPTOR]
excl <- unique(c(unlist(SIGS), RECEPTOR, LIGAND))
cand <- setdiff(names(det), excl)
controls <- names(sort(abs(det[cand] - rec_det)))[seq_len(N_CONTROL)]
cat(sprintf("\nTnfrsf12a detected in %.1f%% of cells; %d control genes at %.1f-%.1f%%\n",
            100 * rec_det, N_CONTROL, 100 * min(det[controls]), 100 * max(det[controls])))
GENES <- c(RECEPTOR, LIGAND, controls)
KIND <- setNames(c("receptor", "ligand", rep("control", N_CONTROL)), GENES)

## ---- (A) is the receptor enriched in oncofetal cells? ----------------------
# Oncofetal cells = top decile of the authors' mOnF score, within genotype.
# The comparison is made within genotype x detection quintile so the two sides
# are matched on library size, which is the confounder that manufactures this
# kind of result in sparse data.
md$onf <- ave(md$paper_mOnF, md$genotype, FUN = function(x) x >= quantile(x, .90)) > 0

strat_diff <- function(v, A, B, stratum) {
  tot <- 0; acc_log <- 0; acc_det <- 0; dr_n <- 0; dr_d <- 0
  for (ix in split(seq_along(stratum), stratum)) {
    a <- ix[A[ix]]; b <- ix[B[ix]]
    if (length(a) < MIN_CELLS || length(b) < MIN_CELLS) next
    n <- length(a); tot <- tot + n
    acc_log <- acc_log + n * (mean(v[a]) - mean(v[b]))
    acc_det <- acc_det + n * (mean(v[a] > 0) - mean(v[b] > 0))
    dr_n <- dr_n + n * mean(md$depth[a]); dr_d <- dr_d + n * mean(md$depth[b])
  }
  if (!tot) return(c(d_log = NA, d_det = NA, depth_ratio = NA, n = 0))
  c(d_log = acc_log / tot, d_det = acc_det / tot,
    depth_ratio = (dr_n / tot) / (dr_d / tot), n = tot)
}

resA <- do.call(rbind, lapply(levels(md$genotype), function(g) {
  k <- which(md$genotype == g)
  st <- md$quint[k]
  do.call(rbind, lapply(GENES, function(gene) {
    v <- as.numeric(lg[gene, k])
    s <- strat_diff(v, md$onf[k], !md$onf[k], st)
    data.frame(genotype = g, gene = gene, kind = KIND[[gene]],
               d_log = s[["d_log"]], d_det = s[["d_det"]],
               depth_ratio = s[["depth_ratio"]], n_onf = s[["n"]], row.names = NULL)
  }))
}))
write_tsv(resA, "Q1A_receptor_in_oncofetal_cells.tsv")

sumA <- resA %>% group_by(genotype) %>%
  mutate(rank_of_receptor = rank(-d_log)[gene == RECEPTOR],
         ctrl_med = median(d_log[kind == "control"], na.rm = TRUE),
         ctrl_max = max(d_log[kind == "control"], na.rm = TRUE),
         n_ctrl_above = sum(d_log[kind == "control"] > d_log[gene == RECEPTOR], na.rm = TRUE)) %>%
  filter(gene == RECEPTOR) %>%
  select(genotype, d_log, d_det, depth_ratio, n_onf, rank_of_receptor,
         ctrl_med, ctrl_max, n_ctrl_above) %>% ungroup()
write_tsv(as.data.frame(sumA), "Q1A_summary.tsv")
cat("\n=== (A) Tnfrsf12a in mOnF-high vs other cells, within genotype x depth quintile ===\n")
print(as.data.frame(sumA), digits = 3)

## ---- (B) correlation with the lineage plasticity score ---------------------
# Spearman at the cell level is pseudoreplicated, so it is reported but is not
# the claim. The claim is the comparison with control genes at identical n, and
# the partial correlation that removes library size.
partial_sp <- function(x, y, z) {
  rx <- residuals(lm(rank(x) ~ rank(z))); ry <- residuals(lm(rank(y) ~ rank(z)))
  cor(rx, ry)
}
resB <- do.call(rbind, lapply(levels(md$genotype), function(g) {
  k <- which(md$genotype == g)
  lp <- md$lineage_plasticity[k]; dp <- log(md$depth[k])
  do.call(rbind, lapply(GENES, function(gene) {
    v <- as.numeric(lg[gene, k])
    ct <- suppressWarnings(cor.test(v, lp, method = "spearman"))
    data.frame(genotype = g, gene = gene, kind = KIND[[gene]], n_cells = length(k),
               rho = unname(ct$estimate), p_cell_level = ct$p.value,
               rho_partial_depth = partial_sp(v, lp, dp), row.names = NULL)
  }))
}))
# the same for the OnF score itself, as a positive control on the axis
resB_onf <- do.call(rbind, lapply(levels(md$genotype), function(g) {
  k <- which(md$genotype == g)
  data.frame(genotype = g, gene = "paper_mOnF_score", kind = "score",
             n_cells = length(k),
             rho = cor(md$paper_mOnF[k], md$lineage_plasticity[k], method = "spearman"),
             p_cell_level = NA, rho_partial_depth = NA, row.names = NULL)
}))
resB <- rbind(resB, resB_onf)
write_tsv(resB, "Q1B_receptor_vs_lineage_plasticity.tsv")

sumB <- resB %>% filter(kind != "score") %>% group_by(genotype) %>%
  mutate(ctrl_med = median(rho[kind == "control"]),
         ctrl_max = max(rho[kind == "control"]),
         n_ctrl_above = sum(rho[kind == "control"] > rho[gene == RECEPTOR]),
         ctrl_med_partial = median(rho_partial_depth[kind == "control"]),
         n_ctrl_above_partial = sum(rho_partial_depth[kind == "control"] >
                                      rho_partial_depth[gene == RECEPTOR])) %>%
  filter(gene == RECEPTOR) %>%
  select(genotype, n_cells, rho, p_cell_level, rho_partial_depth, ctrl_med, ctrl_max,
         n_ctrl_above, ctrl_med_partial, n_ctrl_above_partial) %>% ungroup()
write_tsv(as.data.frame(sumB), "Q1B_summary.tsv")
cat("\n=== (B) Tnfrsf12a vs lineage plasticity (esophagus - colon), per genotype ===\n")
print(as.data.frame(sumB), digits = 3)
cat("\n  mOnF score vs lineage plasticity, same cells (axis positive control):\n")
print(as.data.frame(resB_onf[, c("genotype", "rho")]), digits = 3)

## ---- (C) the axis itself, as deciles --------------------------------------
# Reports the receptor along the plasticity axis in a form that does not depend
# on a correlation coefficient, and shows the control-gene band on the same axis.
decile_profile <- function(gene) {
  do.call(rbind, lapply(levels(md$genotype), function(g) {
    k <- which(md$genotype == g)
    d <- cut(rank(md$lineage_plasticity[k], ties.method = "first"), 10, labels = FALSE)
    v <- as.numeric(lg[gene, k])
    data.frame(genotype = g, gene = gene, kind = KIND[[gene]], decile = 1:10,
               mean_log = tapply(v, d, mean), det_frac = tapply(v > 0, d, mean),
               mean_depth = tapply(md$depth[k], d, mean),
               mean_onf = tapply(md$paper_mOnF[k], d, mean), row.names = NULL)
  }))
}
resC <- do.call(rbind, lapply(GENES, decile_profile))
write_tsv(resC, "Q1C_lineage_plasticity_deciles.tsv")

## ---- (D) the authors' own statistic ---------------------------------------
s1c <- read.delim(file.path(SUPPL, "Table_S1c.tsv"), stringsAsFactors = FALSE)
s1c <- s1c[!is.na(s1c$avg_log2FC), ]
up <- s1c[s1c$status == "Up Reg", ]
rec <- s1c[s1c$gene == RECEPTOR, c("gene", "avg_log2FC", "pct.1", "pct.2", "p_val_adj", "status")]
rec$rank_by_log2FC_among_up <- if (nrow(rec)) sum(up$avg_log2FC > rec$avg_log2FC[1]) + 1 else NA
rec$n_up_genes <- nrow(up)
rec$ligand_present <- LIGAND %in% s1c$gene
write_tsv(rec, "Q1D_authors_metacluster_DE.tsv")
cat("\n=== (D) authors' DE, neoplastic metacluster vs rest (Supplementary Table S1c) ===\n")
print(rec, row.names = FALSE, digits = 3)

## ---- per-genotype summary of the state itself ------------------------------
md$rec_v <- as.numeric(lg[RECEPTOR, rownames(md)])
state <- md %>% group_by(genotype) %>%
  summarise(n_cells = n(), median_depth = median(depth),
            mean_mOnF = mean(paper_mOnF), mean_mStem = mean(paper_mStem),
            mean_plasticity = mean(lineage_plasticity),
            rec_det = mean(rec_v > 0), rec_mean_log = mean(rec_v),
            .groups = "drop")
write_tsv(as.data.frame(state), "Q1_state_summary.tsv")
cat("\n=== state summary ===\n"); print(as.data.frame(state), digits = 3)

saveRDS(list(meta = md[, c("genotype", "depth", "quint", "onf", "paper_mOnF",
                           "paper_mStem", "lineage_plasticity")],
             expr = as.matrix(lg[GENES, ]), kind = KIND, det = det[GENES]),
        file.path(PROC, "scrna_compact.rds"))
cat("\ndone\n")
