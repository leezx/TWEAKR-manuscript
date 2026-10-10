#!/usr/bin/env Rscript
# Read-only candidate audit, not preprocessing or NMF execution.
args <- commandArgs(TRUE)
suppressPackageStartupMessages({library(SeuratObject); library(Matrix)})
root <- args[[1]]
out <- args[[2]]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
inventory <- list()
mapping <- list()
for (i in seq_along(c("CRC23_tissue", "CRC13_tissue"))) {
  sample <- c("CRC23_tissue", "CRC13_tissue")[[i]]
  path <- file.path(root, "GSE254249", paste0(sample, "_counts_meta.rds"))
  obj <- readRDS(path)
  md <- obj[[]]
  stopifnot(all(c("group", "sample_id", "PatientID", "Ident", "Tissue", "SampleTimePoint") %in% names(md)))
  stopifnot(identical(unique(as.character(md$sample_id)), sample),
            identical(unique(as.character(md$Ident)), sample))
  x <- LayerData(obj, assay = "RNA", layer = "counts")
  malignant <- as.character(md$group) == "Cancer"
  malignant[is.na(malignant)] <- FALSE
  libs <- Matrix::colSums(x[, rownames(md)[malignant], drop = FALSE])
  patients <- unique(as.character(md$PatientID))
  stopifnot(length(patients) == 1L, nzchar(patients))
  inventory[[i]] <- data.frame(dataset_id = "GSE254249", source_id = sprintf("source_%04d", i),
    sample_id = sample, rds_path = path, assay = "RNA", assays = paste(Assays(obj), collapse = "|"),
    sample_column = "sample_id", malignant_column = "group", malignant_value = "Cancer",
    n_all_cells = ncol(x), n_malignant_annotation = sum(malignant),
    n_malignant_nonzero_library = sum(libs > 0), n_zero_library_malignant = sum(libs == 0),
    counts_finite = all(is.finite(x@x)), counts_nonnegative = all(x@x >= 0),
    counts_integer_like = all(abs(x@x - round(x@x)) < 1e-8),
    tissue = paste(unique(md$Tissue), collapse = "|"),
    timepoint = paste(unique(md$SampleTimePoint), collapse = "|"),
    patient_source_column = "PatientID", review_status = "pending", stringsAsFactors = FALSE)
  mapping[[i]] <- data.frame(dataset_id = "GSE254249", source_id = sprintf("source_%04d", i),
    sample_id = sample, biological_sample_id = paste("GSE254249", sample, sep = ":"),
    patient_id = paste("GSE254249", patients, sep = ":"), patient_id_status = "confirmed",
    identity_evidence = "Original metadata PatientID/Ident/Tissue/SampleTimePoint; within-study confirmed",
    cross_study_duplicate_review = "pending", review_status = "pending", stringsAsFactors = FALSE)
}
write.table(do.call(rbind, inventory), file.path(out, "pilot_dataset_inventory.tsv"), sep = "\t", quote = TRUE, row.names = FALSE)
write.table(do.call(rbind, mapping), file.path(out, "cohort_identity_mapping.tsv"), sep = "\t", quote = TRUE, row.names = FALSE)
cat("Read-only pilot candidate inventory complete; no NMF executed\n")
