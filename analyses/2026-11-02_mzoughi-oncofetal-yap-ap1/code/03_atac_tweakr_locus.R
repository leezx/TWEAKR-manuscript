# Q2, chromatin half. Does the Tnfrsf12a locus open during CRC progression, and
# do the peaks that open carry TEAD and AP-1 motifs?
#
# Two bulk ATAC-seq experiments, both mm10:
#   GSE239752  WT / A / AKSP            the progression axis
#   GSE239755  WT / RXRi / A            the RXR axis, used as a second opinion
#
# Neither experiment perturbs YAP or AP-1 directly, so chromatin alone cannot
# establish regulation. What it can do is show (i) that the locus is one of the
# regions that opens as the oncofetal state appears, and (ii) whether the peaks
# that open there carry the motifs of the two factors that the RNA perturbations
# in script 02 show the gene responds to. Both are stated as such.
#
# Motif scanning uses consensus matches rather than PWMs, with sequence pulled
# from the UCSC REST API for the locus peaks and a width- and accessibility-
# matched background. A consensus count is cruder than a PWM scan but needs no
# 700 MB genome package, and the comparison is like-for-like against the
# background, which is what the claim rests on.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(DESeq2); library(dplyr)})
set.seed(SEED)

WINDOW <- 50000     # bp either side of the TSS
N_BG   <- 400       # background peaks for the motif comparison

GENES_MM10 <- load_mm10_genes()
tss <- GENES_MM10[GENES_MM10$symbol == RECEPTOR, ]
stopifnot(nrow(tss) == 1)
cat(sprintf("%s mm10 %s:%d-%d (%s), TSS %d\n", RECEPTOR, tss$chr, tss$start, tss$end,
            tss$strand, tss$tss))

ATAC <- list(
  progression = list(file = "GSE239752/GSE239752_atac_counts.csv.gz",
                     cond = function(x) sub("-Rep[0-9]+$", "", x),
                     contrasts = list(c("A_vs_WT", "CRC-A", "WT"),
                                      c("AKSP_vs_WT", "CRC-AKSP", "WT"),
                                      c("AKSP_vs_A", "CRC-AKSP", "CRC-A"))),
  rxr = list(file = "GSE239755/GSE239755_atac_raw_counts.csv.gz",
             cond = function(x) sub("-Rep[0-9]+_S[0-9]+$", "", x),
             contrasts = list(c("A_vs_WT", "A", "WT"),
                              c("RXRi_vs_WT", "wRXR", "WT")))
)

run_atac <- function(nm, spec) {
  d <- read.csv(gzfile(file.path(RAW, spec$file)), check.names = FALSE,
                stringsAsFactors = FALSE)
  pk <- d[, 1:4]; names(pk) <- c("peak_id", "chr", "start", "end")
  m <- round(as.matrix(d[, -(1:4)])); rownames(m) <- pk$peak_id
  cond <- factor(spec$cond(colnames(m)))
  cat(sprintf("\n[%s] %d peaks, %d libraries\n", nm, nrow(m), ncol(m)))
  print(table(cond))
  keep <- rowSums(m >= 5) >= min(table(cond))
  m <- m[keep, ]; pk <- pk[keep, ]
  dds <- DESeqDataSetFromMatrix(m, data.frame(cond = cond, row.names = colnames(m)), ~cond)
  dds <- suppressMessages(DESeq(dds, quiet = TRUE))
  list(pk = pk, dds = dds, spec = spec, nm = nm)
}
RUN <- lapply(names(ATAC), function(n) run_atac(n, ATAC[[n]]))
names(RUN) <- names(ATAC)

## ---- (A) peaks at the receptor locus ---------------------------------------
locus_rows <- function(pk) which(pk$chr == tss$chr &
                                 pk$end   >= tss$tss - WINDOW &
                                 pk$start <= tss$tss + WINDOW)

resA <- do.call(rbind, lapply(RUN, function(R) {
  li <- locus_rows(R$pk)
  do.call(rbind, lapply(R$spec$contrasts, function(ct) {
    r <- as.data.frame(results(R$dds, contrast = c("cond", ct[2], ct[3])))
    r <- r[is.finite(r$stat), ]
    lp <- intersect(R$pk$peak_id[li], rownames(r))
    data.frame(experiment = R$nm, contrast = ct[1], peak_id = lp,
               chr = tss$chr,
               start = R$pk$start[match(lp, R$pk$peak_id)],
               end   = R$pk$end[match(lp, R$pk$peak_id)],
               dist_to_tss = R$pk$start[match(lp, R$pk$peak_id)] +
                 (R$pk$end[match(lp, R$pk$peak_id)] -
                  R$pk$start[match(lp, R$pk$peak_id)]) / 2 - tss$tss,
               baseMean = r[lp, "baseMean"], log2FC = r[lp, "log2FoldChange"],
               pvalue = r[lp, "pvalue"], padj = r[lp, "padj"],
               # where this peak's change sits in the genome-wide distribution
               pct_genomewide = vapply(r[lp, "log2FoldChange"], function(x)
                 mean(r$log2FoldChange <= x, na.rm = TRUE), 0),
               n_peaks_tested = nrow(r), row.names = NULL)
  }))
}))
write_tsv(resA, "Q3A_receptor_locus_peaks.tsv")
cat(sprintf("\n=== (A) peaks within %d kb of the %s TSS ===\n", WINDOW / 1000, RECEPTOR))
print(resA %>% arrange(experiment, contrast, dist_to_tss) %>%
        select(experiment, contrast, dist_to_tss, baseMean, log2FC, padj, pct_genomewide),
      row.names = FALSE, digits = 3)

## ---- (B) is the locus unusual, or is everything opening? -------------------
# Benchmark: peaks at the TSS of the authors' mOnF genes (which by construction
# mark the state) and peaks at the TSS of all other genes.
SIGS <- load_signatures()
tss_class <- function(pk) {
  g <- GENES_MM10
  onf <- g[g$symbol %in% SIGS$paper_mOnF, ]
  stem <- g[g$symbol %in% SIGS$paper_mStem, ]
  cls <- rep("other", nrow(pk))
  near <- function(sub) {
    if (!nrow(sub)) return(logical(nrow(pk)))
    idx <- rep(FALSE, nrow(pk))
    for (i in seq_len(nrow(sub))) {
      idx <- idx | (pk$chr == sub$chr[i] & pk$end >= sub$tss[i] - WINDOW &
                      pk$start <= sub$tss[i] + WINDOW)
    }
    idx
  }
  cls[near(stem)] <- "mStem_locus"
  cls[near(onf)]  <- "mOnF_locus"
  cls[pk$chr == tss$chr & pk$end >= tss$tss - WINDOW & pk$start <= tss$tss + WINDOW] <-
    "Tnfrsf12a_locus"
  cls
}
resB <- do.call(rbind, lapply(RUN, function(R) {
  cls <- tss_class(R$pk)
  do.call(rbind, lapply(R$spec$contrasts, function(ct) {
    r <- as.data.frame(results(R$dds, contrast = c("cond", ct[2], ct[3])))
    ok <- is.finite(r$log2FoldChange)
    d <- data.frame(cls = cls[ok], lfc = r$log2FoldChange[ok])
    s <- d %>% group_by(cls) %>%
      summarise(n_peaks = n(), median_log2FC = median(lfc),
                frac_up = mean(lfc > 0), .groups = "drop")
    s$p_vs_other <- vapply(s$cls, function(k)
      if (k == "other") NA_real_ else
        suppressWarnings(wilcox.test(d$lfc[d$cls == k], d$lfc[d$cls == "other"])$p.value), 0)
    cbind(experiment = R$nm, contrast = ct[1], as.data.frame(s))
  }))
}))
write_tsv(resB, "Q3B_locus_classes.tsv")
cat("\n=== (B) locus classes vs the rest of the genome ===\n")
print(resB, row.names = FALSE, digits = 3)

## ---- (B2) how far out would one have to look? ------------------------------
# The gene is strongly induced by YAP and AP-1 in the RNA data, so if its
# promoter-proximal chromatin does not move, the obvious next question is
# whether a distal element does. Scanned at a ladder of window sizes rather
# than picking one after seeing the answer.
WINDOWS <- c(10e3, 25e3, 50e3, 100e3, 250e3, 500e3)
resB2 <- do.call(rbind, lapply(RUN, function(R) {
  do.call(rbind, lapply(R$spec$contrasts, function(ct) {
    r <- as.data.frame(results(R$dds, contrast = c("cond", ct[2], ct[3])))
    ok <- is.finite(r$log2FoldChange)
    rr <- r[ok, ]; pk <- R$pk[ok, ]
    do.call(rbind, lapply(WINDOWS, function(w) {
      i <- which(pk$chr == tss$chr & pk$end >= tss$tss - w & pk$start <= tss$tss + w)
      if (length(i) < 3) return(NULL)
      data.frame(experiment = R$nm, contrast = ct[1], window_kb = w / 1000,
                 n_peaks = length(i), median_log2FC = median(rr$log2FoldChange[i]),
                 max_log2FC = max(rr$log2FoldChange[i]),
                 n_padj05_up = sum(rr$padj[i] < .05 & rr$log2FoldChange[i] > 0, na.rm = TRUE),
                 p_vs_genome = suppressWarnings(
                   wilcox.test(rr$log2FoldChange[i], rr$log2FoldChange[-i])$p.value),
                 row.names = NULL)
    }))
  }))
}))
write_tsv(resB2, "Q3B2_window_ladder.tsv")
cat("\n=== (B2) accessibility around the receptor at increasing window size ===\n")
print(resB2, row.names = FALSE, digits = 3)

## ---- (C) motif content of the locus peaks ----------------------------------
# Sequence is fetched once and cached outside the repository.
CACHE <- file.path(PROC, "ucsc_seq_cache.rds")
seq_cache <- if (file.exists(CACHE)) readRDS(CACHE) else list()
get_seq <- function(chr, start, end) {
  key <- sprintf("%s:%d-%d", chr, start, end)
  if (!is.null(seq_cache[[key]])) return(seq_cache[[key]])
  url <- sprintf("https://api.genome.ucsc.edu/getData/sequence?genome=mm10;chrom=%s;start=%d;end=%d",
                 chr, start, end)
  txt <- tryCatch(paste(readLines(url, warn = FALSE), collapse = ""), error = function(e) "")
  # the API emits `"dna": "ACGT..."` - note the space after the colon
  s <- toupper(sub('.*"dna":[[:space:]]*"([acgtACGTnN]*)".*', "\\1", txt))
  if (!grepl("^[ACGTN]+$", s)) return("")   # never cache a failed fetch
  seq_cache[[key]] <<- s
  s
}
# TEAD: GGAATG (the MCAT element). AP-1 / TRE: TGA(C|G)TCA.
MOTIF <- c(TEAD = "GGAATG", AP1 = "TGA[CG]TCA")
revcomp <- function(s) chartr("ACGT", "TGCA", paste(rev(strsplit(s, "")[[1]]), collapse = ""))
count_motif <- function(s, pat) {
  if (!nchar(s)) return(NA_integer_)
  lengths(regmatches(s, gregexpr(pat, s))) + lengths(regmatches(revcomp(s), gregexpr(pat, revcomp(s))))
}

R <- RUN$progression
r_ak <- as.data.frame(results(R$dds, contrast = c("cond", "CRC-AKSP", "WT")))
li <- locus_rows(R$pk)
loc <- R$pk[li, ]
loc <- loc[loc$peak_id %in% rownames(r_ak), ]
loc$log2FC <- r_ak[loc$peak_id, "log2FoldChange"]
loc$baseMean <- r_ak[loc$peak_id, "baseMean"]
loc$width <- loc$end - loc$start

# background matched on width and baseMean decile, drawn from peaks on other
# chromosomes so no locus peak can be its own control
pool <- R$pk[R$pk$chr != tss$chr & R$pk$peak_id %in% rownames(r_ak), ]
pool$width <- pool$end - pool$start
pool$baseMean <- r_ak[pool$peak_id, "baseMean"]
pool$log2FC <- r_ak[pool$peak_id, "log2FoldChange"]
pool <- pool[is.finite(pool$baseMean) & is.finite(pool$log2FC), ]
bg_idx <- unlist(lapply(seq_len(nrow(loc)), function(i) {
  d <- abs(log(pmax(pool$baseMean, 1)) - log(max(loc$baseMean[i], 1))) +
    abs(log(pool$width) - log(loc$width[i]))
  head(order(d), ceiling(N_BG / nrow(loc)))
}))
bg <- pool[unique(bg_idx), ]
cat(sprintf("\nfetching sequence for %d locus peaks and %d matched background peaks\n",
            nrow(loc), nrow(bg)))

scan_set <- function(df, label) {
  s <- mapply(get_seq, df$chr, df$start, df$end)
  out <- data.frame(set = label, peak_id = df$peak_id, width = df$width,
                    baseMean = df$baseMean, log2FC = df$log2FC,
                    n_bp = nchar(s), row.names = NULL)
  for (m in names(MOTIF)) out[[m]] <- vapply(s, count_motif, 0, MOTIF[[m]])
  out
}
mo <- rbind(scan_set(loc, "Tnfrsf12a_locus"), scan_set(bg, "matched_background"))
saveRDS(seq_cache, CACHE)
mo <- mo[mo$n_bp > 0, ]
write_tsv(mo, "Q3C_motif_counts.tsv")

motif_sum <- mo %>% group_by(set) %>%
  summarise(n_peaks = n(), total_kb = sum(n_bp) / 1000,
            TEAD_per_kb = 1000 * sum(TEAD) / sum(n_bp),
            AP1_per_kb  = 1000 * sum(AP1)  / sum(n_bp),
            frac_with_TEAD = mean(TEAD > 0), frac_with_AP1 = mean(AP1 > 0),
            .groups = "drop")
pv <- c(TEAD = suppressWarnings(wilcox.test(
          mo$TEAD[mo$set == "Tnfrsf12a_locus"] / mo$n_bp[mo$set == "Tnfrsf12a_locus"],
          mo$TEAD[mo$set != "Tnfrsf12a_locus"] / mo$n_bp[mo$set != "Tnfrsf12a_locus"])$p.value),
        AP1 = suppressWarnings(wilcox.test(
          mo$AP1[mo$set == "Tnfrsf12a_locus"] / mo$n_bp[mo$set == "Tnfrsf12a_locus"],
          mo$AP1[mo$set != "Tnfrsf12a_locus"] / mo$n_bp[mo$set != "Tnfrsf12a_locus"])$p.value))
motif_sum$p_TEAD_vs_bg <- c(NA, pv[["TEAD"]])[match(motif_sum$set, c("matched_background", "Tnfrsf12a_locus"))]
motif_sum$p_AP1_vs_bg  <- c(NA, pv[["AP1"]])[match(motif_sum$set, c("matched_background", "Tnfrsf12a_locus"))]
write_tsv(as.data.frame(motif_sum), "Q3C_motif_summary.tsv")
cat("\n=== (C) consensus motif density, AKSP vs WT peak set ===\n")
print(as.data.frame(motif_sum), row.names = FALSE, digits = 3)
cat("\nper-peak detail at the locus:\n")
print(mo[mo$set == "Tnfrsf12a_locus",
         c("peak_id", "width", "log2FC", "TEAD", "AP1")], row.names = FALSE, digits = 3)
cat("\ndone\n")
