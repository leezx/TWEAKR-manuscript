# Read historical artifacts only; no NMF or preprocessing.
args <- commandArgs(TRUE)
tasks <- read.delim(args[1], stringsAsFactors=FALSE)
rows <- list()
for (i in seq_len(nrow(tasks))) {
  r <- tasks[i,]; d <- r$output_dir
  error <- ''
  result <- tryCatch({
    w <- readRDS(file.path(d,'W.matrix.rds'))
    h <- readRDS(file.path(d,'H.matrix.rds'))
    model <- readRDS(file.path(d,'fastNMF_result_object.rds'))
    marker <- file.path(d,'deliver.nmf_markers.csv')
    m <- if(file.info(marker)$size > 0) read.csv(marker) else data.frame()
    data.frame(n_genes=nrow(w), n_components=ncol(w), n_cells=ncol(h),
      dimensions_match=ncol(w)==nrow(h), finite=all(is.finite(w)) && all(is.finite(h)),
      nonnegative=all(w>=0) && all(h>=0), gene_names_present=!is.null(rownames(w)),
      cell_names_present=!is.null(colnames(h)), marker_rows=nrow(m),
      model_readable=TRUE)
  }, error=function(e) {error <<- conditionMessage(e); NULL})
  if(is.null(result)) result <- data.frame(n_genes=NA,n_components=NA,n_cells=NA,
    dimensions_match=FALSE,finite=FALSE,nonnegative=FALSE,gene_names_present=FALSE,
    cell_names_present=FALSE,marker_rows=NA,model_readable=FALSE)
  rows[[i]] <- cbind(r[c('dataset_id','sample_id')],rank=basename(d),result,
    read_error=error, cell_identity_equivalence='not_verified',
    selector_equivalence='not_verified_regex_vs_exact',reuse_status='direct_reuse_not_approved',enabled=0)
  cat(i,'/',nrow(tasks),r$sample_id,'readable=',result$model_readable,'\n')
  rm(result);gc()
}
write.table(do.call(rbind,rows),args[2],sep='\t',row.names=FALSE,quote=TRUE)
cat('READABILITY_COMPLETE; no NMF executed\n')
