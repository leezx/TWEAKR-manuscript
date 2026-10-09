#!/usr/bin/env Rscript
# Step 3b (r4p3 R, infercnv 1.14.0): one patient per call.
# Usage: l2_infercnv.R <patient_input_dir> <gene_order.tsv> <genes.txt> <out_dir> <threads>
# Writes <out_dir>/cnv_metrics.tsv.gz: per cell, group, CNV score (mean (x-1)^2) and CNV correlation
# with the mean profile of the top 5% epithelial cells by score. No CytoTRACE2 input.
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
obs <- which(grp == "obs")
top <- obs[order(score[obs], decreasing = TRUE)][seq_len(max(1, ceiling(top_fraction * length(obs))))]
profile <- rowMeans(x[, top, drop = FALSE])
cors <- as.numeric(cor(x, profile))
res <- data.frame(cell_id = colnames(x), group = grp, cnv_score = signif(score, 6),
                  cnv_cor = signif(cors, 6), n_genes_used = nrow(x))
con <- gzfile(file.path(out_dir, "cnv_metrics.tsv.gz"), "w")
write.table(res, con, sep = "\t", quote = FALSE, row.names = FALSE)
close(con)
unlink(file.path(out_dir, "infercnv"), recursive = TRUE)  # intermediate files; metrics are kept
cat("DONE\n")
