#!/usr/bin/env Rscript
# A3a step 2 (one SGE task per sample): UCell programme scores on all-gene epithelial counts.
# Frozen contract A3a v0.2 §2: UCell per sample on raw counts of the primary-set cells (Atlas gene space).
# Variants: main and ds1..ds5 (regenerated Fig. 1b depth-matched counts; see a3a_export.py).
# Usage: Rscript a3a_ucell.R <counts_dir> <sample_tag> <genesets.tsv> <out.tsv.gz> <ncores>
#   genesets.tsv: two columns set, gene (public and restricted sets concatenated; private path only)
suppressPackageStartupMessages({ library(UCell); library(hdf5r); library(Matrix); library(data.table) })
args <- commandArgs(trailingOnly = TRUE)
counts_dir <- args[1]; tag <- args[2]; gs_file <- args[3]; out <- args[4]; ncores <- as.integer(args[5])
gs <- fread(gs_file)
sets <- split(gs$gene, gs$set)

read_h5 <- function(p) {
  h <- H5File$new(p, mode = "r")
  shape <- h[["shape"]]$read()
  m <- sparseMatrix(i = h[["indices"]]$read() + 1L, p = h[["indptr"]]$read(), x = as.numeric(h[["data"]]$read()),
                    dims = shape, dimnames = list(h[["genes"]]$read(), h[["cells"]]$read()))
  h$close_all()
  m
}

res <- list()
for (v in c("main", paste0("ds", 1:5))) {
  p <- file.path(counts_dir, sprintf("%s.%s.h5", tag, v))
  if (!file.exists(p)) next
  m <- read_h5(p)
  # samples below the frozen minimum (>=50 epithelial cells) never enter A3a; UCell also fails on 1 cell
  if (ncol(m) < 50) next
  # UCell needs >=1 cell; genes absent from the matrix are dropped by UCell and reported as coverage
  sc <- ScoreSignatures_UCell(m, features = sets, ncores = ncores, name = "")
  d <- as.data.table(sc, keep.rownames = "cell_id")
  d[, variant := v]
  res[[v]] <- d
}
res <- rbindlist(res, use.names = TRUE)
if (nrow(res) == 0) {
  # fwrite produces an invalid gzip for a zero-row table; write the header only
  con <- gzfile(out, "w"); writeLines(paste(c("cell_id", names(sets), "variant"), collapse = "\t"), con); close(con)
} else {
  fwrite(res, out, sep = "\t")
}
cat(sprintf("%s variants=%d rows=%d\n", tag, length(unique(res$variant)), nrow(res)))
