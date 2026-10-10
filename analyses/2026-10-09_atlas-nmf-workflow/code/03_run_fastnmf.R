#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4L) {
  stop("Usage: 03_run_fastnmf.R MATRIX_RDS RANK OUTPUT_DIR SEED")
}

matrix_path <- args[[1]]
rank <- as.integer(args[[2]])
output_dir <- args[[3]]
seed <- as.integer(args[[4]])

suppressPackageStartupMessages({
  library(Matrix)
  library(RcppML)
})

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
matrix <- readRDS(matrix_path)
matrix <- as(matrix, "dgCMatrix")

if (is.na(rank) || rank < 2L) stop("Rank must be an integer >= 2")
if (rank > ncol(matrix)) stop("Rank exceeds the number of cells")
if (is.null(rownames(matrix)) || is.null(colnames(matrix))) stop("Matrix lacks dimnames")
if (anyDuplicated(rownames(matrix)) || anyDuplicated(colnames(matrix))) {
  stop("Matrix dimnames are duplicated")
}
if (any(!is.finite(matrix@x)) || any(matrix@x < 0)) {
  stop("NMF matrix must be finite and non-negative")
}

set.seed(seed)
fit <- RcppML::nmf(A = matrix, k = rank, tol = 1e-5,
                   L1 = c(0.01, 0.01), seed = seed)
W <- fit$w
H <- fit$h
rownames(W) <- rownames(matrix)
colnames(W) <- paste0("fNMF", seq_len(rank))
rownames(H) <- colnames(W)
colnames(H) <- colnames(matrix)

saveRDS(fit, file.path(output_dir, "fastNMF_result_object.rds"))
saveRDS(W, file.path(output_dir, "W.matrix.rds"))
saveRDS(H, file.path(output_dir, "H.matrix.rds"))

factor_assignment <- rownames(H)[max.col(t(H), ties.method = "first")]
names(factor_assignment) <- colnames(H)
saveRDS(factor_assignment, file.path(output_dir, "deliver.cell_best_nmf.rds"))

marker_by_tolerance <- function(loadings, tolerance = 0L) {
  factors <- colnames(loadings)
  is_max <- max.col(loadings, ties.method = "first")
  names(is_max) <- rownames(loadings)
  result <- lapply(seq_along(factors), function(j) {
    ordered <- names(sort(loadings[, j], decreasing = TRUE, na.last = TRUE))
    violations <- 0L
    selected <- character()
    for (gene in ordered) {
      if (is_max[[gene]] != j) violations <- violations + 1L
      if (violations > tolerance) break
      if (is_max[[gene]] == j) selected <- c(selected, gene)
    }
    selected
  })
  names(result) <- factors
  result
}

repeated_top <- function(loadings, n) {
  result <- lapply(seq_len(ncol(loadings)), function(j) {
    head(names(sort(loadings[, j], decreasing = TRUE)), n)
  })
  names(result) <- colnames(loadings)
  result
}

unique_top <- function(loadings, n) {
  owner <- max.col(loadings, ties.method = "first")
  result <- lapply(seq_len(ncol(loadings)), function(j) {
    genes <- rownames(loadings)[owner == j]
    head(genes[order(loadings[genes, j], decreasing = TRUE)], n)
  })
  names(result) <- colnames(loadings)
  result
}

write_gene_sets <- function(gene_sets, path) {
  rows <- do.call(rbind, lapply(names(gene_sets), function(factor) {
    genes <- gene_sets[[factor]]
    data.frame(factor = rep(factor, length(genes)), rank = seq_along(genes),
               gene = genes, stringsAsFactors = FALSE)
  }))
  if (is.null(rows)) rows <- data.frame(factor = character(), rank = integer(), gene = character())
  write.table(rows, path, sep = ",", quote = TRUE, row.names = FALSE, na = "")
}

for (tolerance in 0:2) {
  markers <- marker_by_tolerance(W, tolerance)
  saveRDS(markers, file.path(output_dir, sprintf("deliver.nmf_markers.tol%d.rds", tolerance)))
  write_gene_sets(markers, file.path(output_dir, sprintf("deliver.nmf_markers.tol%d.csv", tolerance)))
}

for (n in c(50L, 100L, 200L)) {
  repeated <- repeated_top(W, n)
  unique <- unique_top(W, n)
  saveRDS(repeated, file.path(output_dir, sprintf("deliver.nmf_top%d.repeated.rds", n)))
  saveRDS(unique, file.path(output_dir, sprintf("deliver.nmf_top%d.unique.rds", n)))
  write_gene_sets(repeated, file.path(output_dir, sprintf("deliver.nmf_top%d.repeated.csv", n)))
  write_gene_sets(unique, file.path(output_dir, sprintf("deliver.nmf_top%d.unique.csv", n)))
}

reconstruction_error <- tryCatch(
  RcppML::mse(matrix, fit$w, fit$d, fit$h),
  error = function(e) NA_real_
)
writeLines(as.character(reconstruction_error), file.path(output_dir, "reconstruction_err.txt"))
status <- data.frame(
  matrix_path = matrix_path,
  rank = rank,
  seed = seed,
  n_features = nrow(matrix),
  n_cells = ncol(matrix),
  reconstruction_error = reconstruction_error,
  status = "complete",
  stringsAsFactors = FALSE
)
write.table(status, file.path(output_dir, "status.tsv"), sep = "\t", quote = TRUE,
            row.names = FALSE, na = "")
