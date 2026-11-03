#!/usr/bin/env Rscript
# Read-only QC: no normalization, CNV or NMF.
suppressPackageStartupMessages({library(Matrix); library(SeuratObject)})
args <- commandArgs(TRUE)
draft <- read.delim(args[1], check.names=FALSE, stringsAsFactors=FALSE)
root <- args[2]
out <- args[3]
dir.create(out, recursive=TRUE, showWarnings=FALSE)
draft <- draft[draft$n_source_label_cells >= 200, ]
draft <- draft[order(draft$dataset_id, draft$sample_id), ]
rows <- list()
for (i in seq_len(nrow(draft))) {
  r <- draft[i, ]
  cat(i, '/', nrow(draft), r$dataset_id, r$sample_id, '\n'); flush.console()
  path <- file.path(root, r$dataset_id, paste0(r$sample_id, '_counts_meta.rds'))
  obj <- readRDS(path); md <- obj[[]]
  stopifnot(all(c('Ident', 'sample_id', r$malignant_column, r$patient_source_column) %in% names(md)))
  x <- LayerData(obj, assay='RNA', layer='counts')
  keep <- as.character(md[[r$malignant_column]]) == r$malignant_value
  keep[is.na(keep)] <- FALSE
  cells <- rownames(md)[keep]
  libs <- Matrix::colSums(x[, cells, drop=FALSE])
  retained <- cells[libs > 0]
  patient <- unique(as.character(md[retained, r$patient_source_column]))
  patient <- patient[!is.na(patient) & nzchar(patient)]
  samples <- unique(as.character(md$Ident))
  sample_ok <- length(samples)==1 && samples==r$sample_id &&
    identical(unique(as.character(md$sample_id)), r$sample_id)
  valid <- all(is.finite(x@x)) && all(x@x>=0) && all(abs(x@x-round(x@x))<1e-8)
  n <- length(retained)
  state <- if (n<200 || !valid) 'excluded' else 'pending'
  reason <- if (n<200) 'post_zero_library_lt200' else if (!valid) 'invalid_counts' else
    if (!sample_ok) 'sample_identity_conflict' else 'eligible_QC_pass_human_review_pending'
  tissue_col <- intersect(c('Tissue','tissue'), names(md))
  time_col <- intersect(c('SampleTimePoint','Treatment','timepoint'), names(md))
  rows[[i]] <- data.frame(dataset_id=r$dataset_id, source_id=sprintf('source_%04d',i),
    sample_id=r$sample_id, biological_sample_id=if(sample_ok) paste(r$dataset_id,r$sample_id,sep=':') else '',
    patient_id=if(length(patient)==1) paste(r$dataset_id,patient,sep=':') else '',
    patient_id_status=if(length(patient)==1) 'confirmed' else 'unknown',
    patient_source_column=r$patient_source_column, original_patient_id=paste(patient,collapse='|'),
    assay='RNA', malignant_column=r$malignant_column, malignant_value=r$malignant_value,
    n_source_cells=r$n_source_label_cells, n_RDS_label_cells=sum(keep),
    n_retained_cells=n, n_zero_library=sum(libs==0), counts_valid=valid,
    source_count_matches=sum(keep)==r$n_source_label_cells, sample_identity_consistent=sample_ok,
    tissue=if(length(tissue_col)) paste(unique(md[[tissue_col[1]]]),collapse='|') else '',
    timepoint=if(length(time_col)) paste(unique(md[[time_col[1]]]),collapse='|') else '',
    review_status=state, reason=reason, enabled=0, rds_path=path)
  write.table(do.call(rbind,rows),file.path(out,'final_sample_inventory.DRAFT.tsv'),sep='\t',quote=TRUE,row.names=FALSE)
  rm(obj,x,md);gc()
}
cat('QC_COMPLETE; all execution enabled=0\n')
