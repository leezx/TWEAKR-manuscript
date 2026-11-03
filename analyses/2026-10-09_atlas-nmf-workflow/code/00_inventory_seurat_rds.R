#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) {
  stop("Usage: 00_inventory_seurat_rds.R RDS_ROOT OUTPUT_TSV")
}

rds_root <- normalizePath(args[[1]], mustWork = TRUE)
output_tsv <- args[[2]]
dir.create(dirname(output_tsv), recursive = TRUE, showWarnings = FALSE)

suppressPackageStartupMessages({
  library(Matrix)
  library(SeuratObject)
})

collapse_values <- function(x, limit = 50L) {
  values <- sort(unique(as.character(x[!is.na(x)])))
  if (length(values) > limit) {
    values <- c(values[seq_len(limit)], sprintf("...+%d", length(values) - limit))
  }
  paste(values, collapse = "|")
}

choose_column <- function(metadata, candidates) {
  hit <- candidates[candidates %in% colnames(metadata)]
  if (length(hit) == 0L) "" else hit[[1]]
}

get_counts <- function(object, assay) {
  tryCatch(
    LayerData(object, assay = assay, layer = "counts"),
    error = function(e) GetAssayData(object, assay = assay, slot = "counts")
  )
}

files <- sort(list.files(rds_root, pattern = "[.]rds$", recursive = TRUE,
                         full.names = TRUE, ignore.case = TRUE))
if (length(files) == 0L) stop("No RDS files found under: ", rds_root)

rows <- vector("list", length(files))
dataset_candidates <- c("dataset_id", "dataset", "study_id", "study", "orig.ident")
sample_candidates <- c("sample_id", "sample", "sample_name", "patient_id", "patient")
cell_candidates <- c("malignancy", "cell_type", "celltype", "cell_type_study",
                     "atlas_cell_type_middle", "major_lineage")

for (i in seq_along(files)) {
  path <- files[[i]]
  message(sprintf("[%d/%d] %s", i, length(files), path))
  base <- data.frame(
    rds_path = path,
    file_size_bytes = file.info(path)$size,
    read_status = "error",
    object_class = "",
    n_cells = NA_integer_,
    n_features = NA_integer_,
    default_assay = "",
    assays = "",
    counts_status = "unchecked",
    counts_nonnegative = NA,
    counts_integer_like = NA,
    dataset_column = "",
    dataset_values = "",
    sample_column = "",
    n_samples = NA_integer_,
    cell_filter_candidates = "",
    metadata_columns = "",
    error_message = "",
    stringsAsFactors = FALSE
  )

  rows[[i]] <- tryCatch({
    object <- readRDS(path)
    if (!inherits(object, "Seurat")) stop("Object is not a Seurat object")
    metadata <- object[[]]
    assay <- DefaultAssay(object)
    counts <- as(get_counts(object, assay), "dgCMatrix")
    if (nrow(counts) == 0L || ncol(counts) == 0L) stop("Counts layer is empty")

    values <- counts@x
    dataset_column <- choose_column(metadata, dataset_candidates)
    sample_column <- choose_column(metadata, sample_candidates)
    cell_columns <- intersect(cell_candidates, colnames(metadata))

    base$read_status <- "ok"
    base$object_class <- paste(class(object), collapse = "|")
    base$n_cells <- ncol(object)
    base$n_features <- nrow(object)
    base$default_assay <- assay
    base$assays <- paste(Assays(object), collapse = "|")
    base$counts_status <- "ok"
    base$counts_nonnegative <- all(values >= 0)
    base$counts_integer_like <- all(abs(values - round(values)) < 1e-8)
    base$dataset_column <- dataset_column
    base$dataset_values <- if (nzchar(dataset_column)) {
      collapse_values(metadata[[dataset_column]])
    } else {
      ""
    }
    base$sample_column <- sample_column
    base$n_samples <- if (nzchar(sample_column)) {
      length(unique(metadata[[sample_column]][!is.na(metadata[[sample_column]])]))
    } else {
      NA_integer_
    }
    base$cell_filter_candidates <- paste(cell_columns, collapse = "|")
    base$metadata_columns <- paste(colnames(metadata), collapse = "|")
    base
  }, error = function(e) {
    base$error_message <- conditionMessage(e)
    base
  })
}

result <- do.call(rbind, rows)
write.table(result, output_tsv, sep = "\t", quote = TRUE, row.names = FALSE,
            na = "")
message("Wrote inventory: ", output_tsv)
