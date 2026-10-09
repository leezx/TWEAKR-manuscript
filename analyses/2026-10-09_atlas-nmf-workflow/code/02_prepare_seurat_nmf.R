#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) {
  stop("Usage: 02_prepare_seurat_nmf.R DATASET_PLAN ROW_INDEX OUTPUT_ROOT")
}

plan_path <- args[[1]]
row_index <- as.integer(args[[2]])
output_root <- args[[3]]

suppressPackageStartupMessages({
  library(Matrix)
  library(SeuratObject)
})

plan <- read.delim(plan_path, check.names = FALSE, stringsAsFactors = FALSE,
                   quote = "\"")
if (is.na(row_index) || row_index < 1L || row_index > nrow(plan)) {
  stop("ROW_INDEX is outside dataset plan")
}
entry <- plan[row_index, , drop = FALSE]
if (as.character(entry$enabled) != "1" || entry$review_status != "approved") {
  stop("Plan row is not enabled and approved: row ", row_index)
}

safe_name <- function(x) gsub("[^A-Za-z0-9._-]+", "_", as.character(x))

get_counts <- function(object, assay) {
  tryCatch(
    LayerData(object, assay = assay, layer = "counts"),
    error = function(e) GetAssayData(object, assay = assay, slot = "counts")
  )
}

preprocess_counts <- function(counts, min_detected_cells, scale_factor) {
  if (length(min_detected_cells) != 1L || !is.finite(min_detected_cells) ||
      min_detected_cells < 1 || min_detected_cells != floor(min_detected_cells)) {
    stop("MIN_DETECTED_CELLS must be a positive integer")
  }
  if (length(scale_factor) != 1L || !is.finite(scale_factor) || scale_factor <= 0) {
    stop("SCALE_FACTOR must be positive and finite")
  }
  counts <- as(counts, "dgCMatrix")
  if (any(!is.finite(counts@x))) stop("Counts contain non-finite values")
  if (any(counts@x < 0)) stop("Counts contain negative values")
  if (any(abs(counts@x - round(counts@x)) > 1e-8)) {
    stop("Counts are not integer-like")
  }
  if (is.null(rownames(counts)) || anyDuplicated(rownames(counts))) {
    stop("Feature names are missing or duplicated")
  }
  if (is.null(colnames(counts)) || anyDuplicated(colnames(counts))) {
    stop("Cell names are missing or duplicated")
  }

  library_size <- Matrix::colSums(counts)
  keep_cells <- library_size > 0
  counts <- counts[, keep_cells, drop = FALSE]
  library_size <- library_size[keep_cells]
  keep_genes <- Matrix::rowSums(counts > 0) >= min_detected_cells
  counts <- counts[keep_genes, , drop = FALSE]
  if (nrow(counts) == 0L || ncol(counts) == 0L) stop("No matrix remains after QC")

  normalized <- counts %*% Matrix::Diagonal(x = scale_factor / library_size)
  normalized@x <- log1p(normalized@x)
  gene_means <- Matrix::rowMeans(normalized)
  normalized@x <- pmax(normalized@x - gene_means[normalized@i + 1L], 0)
  normalized <- drop0(normalized)
  list(matrix = normalized, dropped_zero_library = sum(!keep_cells))
}

min_cells <- as.integer(Sys.getenv("MIN_CELLS", "200"))
if (is.na(min_cells) || min_cells < 1L) stop("MIN_CELLS must be positive")
min_detected_cells <- as.integer(Sys.getenv("MIN_DETECTED_CELLS", "1"))
scale_factor <- as.numeric(Sys.getenv("SCALE_FACTOR", "10000"))

object <- readRDS(entry$rds_path)
if (!inherits(object, "Seurat")) stop("RDS is not a Seurat object")
metadata <- object[[]]
assay <- as.character(entry$assay)
if (!assay %in% Assays(object)) stop("Assay not found: ", assay)

filter_column <- as.character(entry$cell_filter_column)
if (!filter_column %in% colnames(metadata)) stop("Cell filter column not found")
filter_values <- strsplit(as.character(entry$cell_filter_values), "[|]", perl = TRUE)[[1]]
keep <- as.character(metadata[[filter_column]]) %in% filter_values
keep[is.na(keep)] <- FALSE
if (!any(keep)) stop("No cells match the approved cell filter")

object <- subset(object, cells = rownames(metadata)[keep])
metadata <- object[[]]
sample_column <- as.character(entry$sample_column)
if (sample_column == "__all__") {
  if (!"single_biological_sample_verified" %in% names(entry) ||
      as.character(entry$single_biological_sample_verified) != "1") {
    stop("__all__ requires reviewed single_biological_sample_verified=1")
  }
  sample_ids <- rep("all_cells", nrow(metadata))
} else {
  if (!sample_column %in% colnames(metadata)) stop("Sample column not found")
  sample_ids <- as.character(metadata[[sample_column]])
}
names(sample_ids) <- rownames(metadata)
available_samples <- sort(unique(sample_ids[!is.na(sample_ids) & nzchar(sample_ids)]))
if (length(available_samples) == 0L) stop("No non-empty sample IDs remain")
if (anyDuplicated(safe_name(available_samples))) {
  stop("Sample IDs collide after filesystem-safe normalization")
}

dataset_id <- safe_name(entry$dataset_id)
source_id <- sprintf("source_%04d", row_index)
dataset_dir <- file.path(output_root, "prepared", dataset_id, source_id)
dir.create(dataset_dir, recursive = TRUE, showWarnings = FALSE)
manifest <- list()

for (sample_id in available_samples) {
  cells <- names(sample_ids)[!is.na(sample_ids) & sample_ids == sample_id]
  status <- "prepared"
  reason <- ""
  outfile <- ""
  n_features <- NA_integer_
  dropped <- NA_integer_
  retained_cells <- NA_integer_

  if (length(cells) < min_cells) {
    status <- "skipped_too_few_cells"
    reason <- sprintf("%d cells < MIN_CELLS=%d", length(cells), min_cells)
  } else {
    counts <- get_counts(object, assay)[, cells, drop = FALSE]
    prepared <- preprocess_counts(counts, min_detected_cells, scale_factor)
    retained_cells <- ncol(prepared$matrix)
    if (retained_cells < min_cells) {
      status <- "skipped_too_few_cells_after_qc"
      reason <- sprintf("%d retained cells < MIN_CELLS=%d", retained_cells, min_cells)
    } else if (sum(Matrix::rowSums(prepared$matrix) > 0) < 50L) {
      status <- "skipped_too_few_effective_genes"
      reason <- "Fewer than 50 nonzero genes after centering"
    } else {
      outfile <- file.path(dataset_dir,
                         paste0(safe_name(sample_id), ".gc.NonNegCenterMat.rds"))
      saveRDS(prepared$matrix, outfile, compress = FALSE)
    }
    n_features <- nrow(prepared$matrix)
    dropped <- prepared$dropped_zero_library
  }

  manifest[[length(manifest) + 1L]] <- data.frame(
    dataset_id = as.character(entry$dataset_id),
    source_id = source_id,
    sample_id = sample_id,
    rds_path = as.character(entry$rds_path),
    matrix_path = outfile,
    n_input_cells = length(cells),
    n_cells = retained_cells,
    n_features = n_features,
    dropped_zero_library_cells = dropped,
    status = status,
    reason = reason,
    stringsAsFactors = FALSE
  )
}

manifest <- do.call(rbind, manifest)
manifest_path <- file.path(dataset_dir, paste0("prepare_manifest.row", row_index, ".tsv"))
write.table(manifest, manifest_path, sep = "\t", quote = TRUE, row.names = FALSE,
            na = "")
message("Wrote preparation manifest: ", manifest_path)
