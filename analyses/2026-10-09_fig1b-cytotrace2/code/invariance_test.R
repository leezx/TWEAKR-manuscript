#!/usr/bin/env Rscript
# A2.1 raw-score invariance test (CytoTRACE2 1.1.0).
# A fixed set of cells (150 per broad compartment from one Lee 2020 sample) is scored:
#   alone; + 3,000 epithelial; + 3,000 immune; + 3,000 stromal (or all available); + all three.
# The background cells come from other Lee 2020 samples. For the fixed cells we report:
#   raw model score (preprocessData + predictData): max |difference| vs alone (expected 0);
#   final CytoTRACE2_Score: per-cell |difference|, median shift per compartment, potency agreement.
# Usage: Rscript invariance_test.R <counts_dir> <out_dir> <ncores>
suppressPackageStartupMessages({ library(CytoTRACE2); library(hdf5r); library(Matrix); library(data.table) })
args <- commandArgs(trailingOnly = TRUE)
cdir <- args[1]; out <- args[2]; ncores <- as.integer(args[3])
dir.create(out, showWarnings = FALSE, recursive = TRUE)
set.seed(14)
read_h5 <- function(f) {
  h <- H5File$new(f, mode = "r")
  m <- sparseMatrix(i = h[["indices"]]$read() + 1L, p = h[["indptr"]]$read(), x = as.numeric(h[["data"]]$read()),
                    dims = h[["shape"]]$read(), dimnames = list(h[["genes"]]$read(), h[["cells"]]$read()))
  h$close_all(); m
}
man <- fread(file.path(cdir, "export_manifest.tsv"))[study_id == "Lee_2020_Nat_Genet" & variant == "model"]
lab <- fread(file.path(cdir, "cell_labels.tsv"))[study_id == "Lee_2020_Nat_Genet" & broad %in% c("Epithelial", "Immune", "Stromal")]
cnt <- dcast(lab[, .N, by = .(sample_id, broad)], sample_id ~ broad, value.var = "N", fill = 0)
cnt[, min_n := pmin(Epithelial, Immune, Stromal)]
target <- cnt[order(-min_n)][1, sample_id]
n_fix <- min(150L, cnt[sample_id == target, min_n])
fixed <- lab[sample_id == target, .SD[sample(.N, n_fix)], by = broad]
bg_pool <- lab[sample_id != target]
bg <- lapply(c(Epithelial = "Epithelial", Immune = "Immune", Stromal = "Stromal"), function(b) {
  x <- bg_pool[broad == b]; x[sample(.N, min(3000L, .N))]
})
need <- unique(c(target, unlist(lapply(bg, function(x) x$sample_id))))
mats <- lapply(man[sample_id %in% need, file], function(f) read_h5(file.path(cdir, f)))
M <- do.call(cbind, mats)
score <- function(cells) {
  d <- as.data.frame(as.matrix(M[, cells, drop = FALSE]))
  w <- cytotrace2(d, species = "human", ncores = ncores, seed = 14)
  ns <- asNamespace("CytoTRACE2")
  pre <- ns$preprocessData(d, "human")
  params <- readRDS(system.file("extdata", "parameter_dict_19.rds", package = "CytoTRACE2"))
  r <- ns$predictData(params, pre[[1]], pre[[2]], TRUE, ncores = ncores)
  data.table(cell_id = fixed$cell_id, final = w[fixed$cell_id, "CytoTRACE2_Score"],
             potency = as.character(w[fixed$cell_id, "CytoTRACE2_Potency"]),
             raw = r[fixed$cell_id, "preKNN_CytoTRACE2_Score"])
}
conds <- list(alone = fixed$cell_id,
              plus_epithelial = c(fixed$cell_id, bg$Epithelial$cell_id),
              plus_immune = c(fixed$cell_id, bg$Immune$cell_id),
              plus_stromal = c(fixed$cell_id, bg$Stromal$cell_id),
              plus_all = c(fixed$cell_id, bg$Epithelial$cell_id, bg$Immune$cell_id, bg$Stromal$cell_id))
res <- rbindlist(lapply(names(conds), function(k) score(conds[[k]])[, condition := k]))
res <- merge(res, fixed[, .(cell_id, broad)], by = "cell_id")
fwrite(res, file.path(out, "invariance_cells.tsv.gz"), sep = "\t")
ref <- res[condition == "alone", .(cell_id, raw0 = raw, final0 = final, pot0 = potency)]
s <- merge(res, ref, by = "cell_id")[condition != "alone",
  .(cells = .N, raw_max_abs_diff = max(abs(raw - raw0)),
    final_median_abs_diff = median(abs(final - final0)), final_max_abs_diff = max(abs(final - final0)),
    final_median_shift = median(final) - median(final0), potency_agreement = mean(potency == pot0)),
  by = .(condition, broad)]
s[, `:=`(target_sample = target, background_sizes = paste(sapply(bg, nrow), collapse = "/"))]
fwrite(s, file.path(out, "invariance_summary.csv"))
print(s)
