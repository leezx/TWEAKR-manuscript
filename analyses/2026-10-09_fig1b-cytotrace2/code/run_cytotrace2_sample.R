#!/usr/bin/env Rscript
# CytoTRACE2 1.1.0 on one exported sample, in three technical-pilot modes:
#   whole     - official cytotrace2() on all cells of the sample (primary run unit)
#   intrinsic - CytoTRACE2:::preprocessData + predictData only: per-cell model score and potency,
#               before diffusion smoothing, within-category rank binning and kNN smoothing. It does
#               not depend on which other cells are in the input.
#   split     - official cytotrace2() run separately per broad compartment (Epithelial/Immune/Stromal)
# Usage: Rscript run_cytotrace2_sample.R <sample.h5> <cell_labels.tsv> <out.tsv.gz> <ncores> [modes]
#   modes: comma-separated subset of whole,intrinsic,split (default all three)
#   seed : CytoTRACE2 seed (default 14; other values only for the A2.1 batching-repeat diagnostic)
# Note: `intrinsic_*` columns are the raw model score/category (pre-smoothing, pre-binning).
suppressPackageStartupMessages({ library(CytoTRACE2); library(hdf5r); library(Matrix); library(data.table) })
args <- commandArgs(trailingOnly = TRUE)
h <- H5File$new(args[1], mode = "r")
shape <- h[["shape"]]$read()
m <- sparseMatrix(i = h[["indices"]]$read() + 1L, p = h[["indptr"]]$read(), x = as.numeric(h[["data"]]$read()),
                  dims = shape, dimnames = list(h[["genes"]]$read(), h[["cells"]]$read()))
h$close_all()
ncores <- as.integer(args[4])
modes <- if (length(args) >= 5) strsplit(args[5], ",")[[1]] else c("whole", "intrinsic", "split")
seed <- if (length(args) >= 6) as.integer(args[6]) else 14L
labels <- fread(args[2])[cell_id %in% colnames(m)]
setkey(labels, cell_id)
dense <- as.data.frame(as.matrix(m))
t0 <- Sys.time()

res <- data.table(cell_id = colnames(m), n_model_genes_detected = colSums(m > 0))
if ("whole" %in% modes) {
  whole <- cytotrace2(dense, species = "human", ncores = ncores, seed = seed)
  res[, `:=`(whole_score = whole[cell_id, "CytoTRACE2_Score"],
             whole_potency = as.character(whole[cell_id, "CytoTRACE2_Potency"]),
             whole_preknn_score = whole[cell_id, "preKNN_CytoTRACE2_Score"])]
}
t1 <- Sys.time()

if ("intrinsic" %in% modes) {
  ns <- asNamespace("CytoTRACE2")
  set.seed(14)
  pre <- ns$preprocessData(dense, "human")
  params <- readRDS(system.file("extdata", "parameter_dict_19.rds", package = "CytoTRACE2"))
  intr <- ns$predictData(params, pre[[1]], pre[[2]], TRUE, ncores = ncores)
  res[, `:=`(intrinsic_score = intr[cell_id, "preKNN_CytoTRACE2_Score"],
             intrinsic_potency = as.character(intr[cell_id, "preKNN_CytoTRACE2_Potency"]))]
}
t2 <- Sys.time()

split <- list()
for (b in if ("split" %in% modes) c("Epithelial", "Immune", "Stromal") else character(0)) {
  cells <- labels[broad == b, cell_id]
  if (length(cells) >= 2) {
    r <- cytotrace2(dense[, cells, drop = FALSE], species = "human", ncores = ncores, seed = 14)
    split[[b]] <- data.table(cell_id = rownames(r), split_score = r$CytoTRACE2_Score,
                             split_potency = as.character(r$CytoTRACE2_Potency))
  }
}
split <- rbindlist(split)
t3 <- Sys.time()

if (nrow(split) > 0) res <- merge(res, split, by = "cell_id", all.x = TRUE)
fwrite(res, args[3], sep = "\t")
cat(sprintf("cells=%d whole_sec=%.0f intrinsic_sec=%.0f split_sec=%.0f\n", ncol(m),
            as.numeric(t1 - t0, units = "secs"), as.numeric(t2 - t1, units = "secs"),
            as.numeric(t3 - t2, units = "secs")))
