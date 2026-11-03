# P0, the review's top priority: is there direct regulatory evidence that
# YAP/TEAD and AP-1 act at the Tnfrsf12a locus?
#
# Script 03 showed that chromatin ACCESSIBILITY at the locus does not change.
# The review correctly pointed out that this does not exclude binding: YAP/TEAD
# can occupy regulatory elements that are already open, in which case ATAC sees
# nothing. The right question is occupancy, not accessibility, and the right
# evidence is ChIP-seq.
#
# The original study has no ChIP-seq or CUT&RUN. We therefore query ChIP-Atlas,
# which reprocesses all public mouse ChIP-seq uniformly and publishes, per
# transcription factor, the MACS2 score of the strongest peak within a fixed
# window of each gene's TSS, experiment by experiment.
#
# WHAT THIS CAN AND CANNOT SHOW.
# It can show whether the locus is a bound element for these factors at all, and
# whether it is bound more strongly than a typical gene. It cannot show that
# binding happens in intestinal epithelium during oncofetal reprogramming, and
# it cannot show that the bound element is required for expression. Both limits
# are reported with the result, including the tissue of every experiment used.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(dplyr); library(tidyr)})
set.seed(SEED)

TFS <- c("Tead1", "Tead2", "Tead4", "Yap1",          # YAP/TEAD arm
         "Fos", "Fosl1", "Fosl2", "Jun", "Junb", "Jund")   # AP-1 arm
ARM <- c(Tead1 = "YAP/TEAD", Tead2 = "YAP/TEAD", Tead4 = "YAP/TEAD", Yap1 = "YAP/TEAD",
         Fos = "AP-1", Fosl1 = "AP-1", Fosl2 = "AP-1", Jun = "AP-1",
         Junb = "AP-1", Jund = "AP-1")
WINDOWS <- c(1, 5, 10)   # kb either side of the TSS, ChIP-Atlas' own bins

CACHE <- file.path(PROC, "chipatlas")
dir.create(CACHE, showWarnings = FALSE, recursive = TRUE)

fetch <- function(tf, w) {
  f <- file.path(CACHE, sprintf("%s.%d.tsv", tf, w))
  if (!file.exists(f) || file.size(f) < 1000) {
    url <- sprintf("https://chip-atlas.dbcls.jp/data/mm10/target/%s.%d.tsv", tf, w)
    ok <- tryCatch({ download.file(url, f, quiet = TRUE); TRUE }, error = function(e) FALSE)
    if (!ok || !file.exists(f) || file.size(f) < 1000) { unlink(f); return(NULL) }
  }
  read.delim(f, check.names = FALSE, stringsAsFactors = FALSE)
}

SIGS <- load_signatures()
onf <- SIGS$paper_mOnF

rows <- list(); expt <- list()
for (tf in TFS) for (w in WINDOWS) {
  d <- fetch(tf, w)
  if (is.null(d)) { message(sprintf("  no data: %s at %d kb", tf, w)); next }
  sym <- d[[1]]
  avg <- suppressWarnings(as.numeric(d[[2]]))
  names(avg) <- sym
  # per-experiment columns, named SRX|cell type
  cols <- names(d)[-(1:2)]
  i <- match(RECEPTOR, sym)
  bound_any <- !is.na(i)
  sc <- if (bound_any) suppressWarnings(as.numeric(unlist(d[i, -(1:2)]))) else numeric(0)

  # benchmarks: all listed genes, and the authors' oncofetal genes
  onf_avg <- avg[intersect(onf, names(avg))]
  rows[[length(rows) + 1]] <- data.frame(
    tf = tf, arm = ARM[[tf]], window_kb = w,
    n_experiments = length(cols),
    n_genes_listed = length(sym),
    receptor_bound = bound_any,
    receptor_avg_score = if (bound_any) avg[[i]] else NA_real_,
    receptor_pct_of_all = if (bound_any) mean(avg <= avg[[i]], na.rm = TRUE) else NA_real_,
    n_expt_with_peak = if (bound_any) sum(sc > 0, na.rm = TRUE) else 0L,
    max_expt_score = if (bound_any && any(sc > 0, na.rm = TRUE)) max(sc, na.rm = TRUE) else NA_real_,
    onf_genes_listed = length(onf_avg),
    onf_median_score = if (length(onf_avg)) median(onf_avg, na.rm = TRUE) else NA_real_,
    all_median_score = median(avg, na.rm = TRUE),
    row.names = NULL)

  if (bound_any && length(cols)) {
    expt[[length(expt) + 1]] <- data.frame(
      tf = tf, arm = ARM[[tf]], window_kb = w,
      experiment = sub("\\|.*", "", cols), tissue = sub(".*\\|", "", cols),
      score = sc, row.names = NULL)
  }
}
res <- bind_rows(rows); ex <- bind_rows(expt)
write_tsv(res, "Q6A_chipatlas_occupancy_summary.tsv")
write_tsv(ex, "Q6B_chipatlas_per_experiment.tsv")

cat("\n=== (A) occupancy at the Tnfrsf12a TSS, ChIP-Atlas mm10 ===\n")
print(as.data.frame(res %>%
        select(tf, arm, window_kb, n_experiments, receptor_bound, receptor_avg_score,
               receptor_pct_of_all, n_expt_with_peak, max_expt_score,
               onf_median_score, all_median_score)),
      row.names = FALSE, digits = 3)

cat("\n=== (B) which tissues carry the signal (5 kb window, experiments with a peak) ===\n")
tis <- ex %>% filter(window_kb == 5, score > 0) %>%
  group_by(arm, tf, tissue) %>%
  summarise(n = n(), max_score = max(score), .groups = "drop") %>%
  arrange(arm, tf, desc(max_score))
print(as.data.frame(tis), row.names = FALSE, digits = 3)

cat("\n=== (C) tissue coverage of the whole ChIP-Atlas panel used ===\n")
cov <- ex %>% filter(window_kb == 5) %>%
  group_by(arm, tissue) %>%
  summarise(n_experiments = n(), n_with_peak = sum(score > 0), .groups = "drop") %>%
  arrange(arm, desc(n_experiments))
print(as.data.frame(cov), row.names = FALSE)
intest <- grepl("intestin|colon|crc|colorect|gut|organoid", cov$tissue, ignore.case = TRUE)
cat(sprintf("\nexperiments in intestinal / colorectal tissue: %d of %d\n",
            sum(cov$n_experiments[intest]), sum(cov$n_experiments)))
cat("  -> any occupancy reported here is from other tissues and is context-mismatched.\n")

## ---- is the receptor unusual among the oncofetal genes? --------------------
rank_tab <- do.call(rbind, lapply(TFS, function(tf) {
  d <- fetch(tf, 5); if (is.null(d)) return(NULL)
  avg <- suppressWarnings(as.numeric(d[[2]])); names(avg) <- d[[1]]
  og <- avg[intersect(onf, names(avg))]
  r <- if (RECEPTOR %in% names(avg)) avg[[RECEPTOR]] else NA_real_
  data.frame(tf = tf, arm = ARM[[tf]], receptor_score = r,
             onf_n = length(og), onf_median = median(og, na.rm = TRUE),
             onf_pct_below_receptor = if (is.na(r)) NA_real_ else mean(og <= r, na.rm = TRUE),
             row.names = NULL)
}))
write_tsv(rank_tab, "Q6C_receptor_vs_oncofetal_genes.tsv")
cat("\n=== (D) the receptor against the authors' oncofetal genes, 5 kb ===\n")
print(rank_tab, row.names = FALSE, digits = 3)
cat("\ndone\n")
