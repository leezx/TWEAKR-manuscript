#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
script <- normalizePath(args[[1]])
suppressPackageStartupMessages({library(Matrix); library(SeuratObject)})
expressions <- parse(script)
for (expr in expressions) {
  if (is.call(expr) && identical(expr[[1]], as.name("<-")) &&
      identical(expr[[2]], as.name("preprocess_counts"))) eval(expr)
}
set.seed(42)
x <- matrix(0, 60, 205, dimnames = list(paste0("G", 1:60), paste0("C", 1:205)))
x[, 1:185] <- sample(1:5, 60 * 185, replace = TRUE)
counts <- as(x, "dgCMatrix")
prepared <- preprocess_counts(counts, 1, 10000)
stopifnot(ncol(prepared$matrix) == 185, prepared$dropped_zero_library == 20,
          identical(rownames(prepared$matrix), rownames(counts)),
          identical(colnames(prepared$matrix), colnames(counts)[1:185]),
          all(is.finite(prepared$matrix@x)), all(prepared$matrix@x >= 0))
expect_error <- function(expr) stopifnot(inherits(tryCatch(expr, error = identity), "error"))
bad <- counts
bad@x[1] <- Inf
expect_error(preprocess_counts(bad, 1, 10000))
expect_error(preprocess_counts(counts, -1, 10000))
expect_error(preprocess_counts(counts, 1, NA_real_))
root <- tempfile("nmf_synthetic_")
dir.create(root)
object <- CreateSeuratObject(counts = counts, min.cells = 0, min.features = 0)
object$malignancy <- "malignant"
saveRDS(object, file.path(root, "synthetic.rds"))
plan <- data.frame(dataset_id = "SYNTHETIC", rds_path = file.path(root, "synthetic.rds"),
  sample_column = "__all__", single_biological_sample_verified = 1,
  cell_filter_column = "malignancy", cell_filter_values = "malignant",
  assay = "RNA", enabled = 1, review_status = "approved")
write.table(plan, file.path(root, "plan.tsv"), sep = "\t", row.names = FALSE)
status <- system2(file.path(R.home("bin"), "Rscript"),
  c(shQuote(script), shQuote(file.path(root, "plan.tsv")), "1", shQuote(root)),
  env = "MIN_CELLS=200")
stopifnot(status == 0)
manifest <- read.delim(file.path(root, "prepared/SYNTHETIC/source_0001/prepare_manifest.row1.tsv"))
stopifnot(manifest$n_input_cells == 205, manifest$n_cells == 185,
  manifest$status == "skipped_too_few_cells_after_qc", is.na(manifest$matrix_path))
unlink(root, recursive = TRUE)
cat("PASS: finite/parameter checks, sparse normalization, post-QC 200-cell gate; synthetic only\n")
