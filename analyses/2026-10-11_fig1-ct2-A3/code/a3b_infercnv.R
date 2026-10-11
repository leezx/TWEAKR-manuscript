#!/usr/bin/env Rscript
# A3b Stage I step 2 (r4p3 R, infercnv 1.14.0): one patient per call. Contract A3b v0.3 §5.
# Same run settings as Fig. 1b l2_infercnv.R. Differences (contract-specified): observations are grouped by
# sample ("obs__<sample>"), and the top-5% CNV profile is taken over the patient's pre/primary tumour-side
# epithelium (profile_cells.txt). Patients without such cells get cnv_cor = NA (Evidence T not evaluable).
# Usage: a3b_infercnv.R <patient_input_dir> <gene_order.tsv> <genes.txt> <out_dir> <threads>
suppressPackageStartupMessages({
  library(Matrix)
  library(infercnv)
})
args <- commandArgs(trailingOnly = TRUE)
in_dir <- args[1]; gene_order <- args[2]; genes_file <- args[3]; out_dir <- args[4]
threads <- as.integer(args[5])
top_fraction <- 0.05
set.seed(0)
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

m <- readMM(gzfile(file.path(in_dir, "counts.mtx.gz")))
rownames(m) <- readLines(genes_file)
colnames(m) <- readLines(file.path(in_dir, "cells.txt"))
m <- as(m, "CsparseMatrix")
annot <- read.delim(file.path(in_dir, "annotation.tsv"), header = FALSE, row.names = 1)
refs <- intersect(c("ref_immune", "ref_stromal"), unique(annot[[1]]))
prof_cells <- if (file.size(file.path(in_dir, "profile_cells.txt")) > 0) readLines(file.path(in_dir, "profile_cells.txt")) else character(0)

obj <- CreateInfercnvObject(raw_counts_matrix = m, annotations_file = annot, delim = "\t",
                            gene_order_file = gene_order, ref_group_names = refs)
obj <- infercnv::run(obj, cutoff = 0.1, out_dir = file.path(out_dir, "infercnv"),
                     cluster_by_groups = TRUE, denoise = TRUE, HMM = FALSE, window_length = 101,
                     analysis_mode = "samples", num_threads = threads, no_plot = TRUE,
                     no_prelim_plot = TRUE, save_rds = FALSE, save_final_rds = FALSE,
                     write_expr_matrix = FALSE)

x <- obj@expr.data
grp <- annot[colnames(x), 1]
score <- colMeans((x - 1)^2)
pc <- which(colnames(x) %in% prof_cells)
if (length(pc) > 0) {
  top <- pc[order(score[pc], decreasing = TRUE)][seq_len(max(1, ceiling(top_fraction * length(pc))))]
  profile <- rowMeans(x[, top, drop = FALSE])
  cors <- as.numeric(cor(x, profile))
} else {
  cors <- rep(NA_real_, ncol(x))
}
res <- data.frame(cell_id = colnames(x), group = grp, cnv_score = signif(score, 6),
                  cnv_cor = signif(cors, 6), n_genes_used = nrow(x), n_profile = length(pc))
con <- gzfile(file.path(out_dir, "cnv_metrics.tsv.gz"), "w")
write.table(res, con, sep = "\t", quote = FALSE, row.names = FALSE)
close(con)
unlink(file.path(out_dir, "infercnv"), recursive = TRUE)
cat("DONE\n")
