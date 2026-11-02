# Q2, transcriptional half. Is Tnfrsf12a (TWEAKR) downstream of YAP and AP-1,
# and do the placenta and tumour-intrinsic immune programmes move with it?
#
# The design of the original study gives both directions of causality for the
# same two factors, which is what makes this answerable rather than correlative:
#
#   gain of function   YAP(S6A) overexpression, +/- FOS, in WT organoids   GSE263050
#   loss of function   dominant-negative FOS during Apc-loss initiation    GSE263056
#                      YAP shRNA (x2) and FOS knockdown in AKSP tumoroids  GSE263055
#   progression        WT -> A -> AKSP                                     GSE239754
#   state sort         oncofetal reporter high vs negative                 GSE235205
#   RXR arm            RXR overexpression / inhibition                     GSE263045/44
#
# One relevant contrast - YAP or FOS knockdown during initiation (GSE263047) -
# has no processed counts in GEO, so it is read from the authors' own DESeq2
# output in Supplementary Table S2c instead. That is noted wherever it is used.
#
# Gene-set level inference uses cameraPR on the Wald statistics: a competitive
# test that accounts for inter-gene correlation, which a plain Wilcoxon of set
# members against the rest does not.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(DESeq2); library(limma); library(dplyr)})
set.seed(SEED)

## ---- experiment table ------------------------------------------------------
# Each entry: the GEO series, how to turn column names into condition and batch,
# and the contrasts to extract. `axis` labels which question a contrast serves.
read_counts <- function(gse, file = NULL) {
  f <- file.path(RAW, gse, file %||% paste0(gse, "_salmon_gene_counts.csv.gz"))
  d <- read.csv(gzfile(f), check.names = FALSE, stringsAsFactors = FALSE)
  # a few rows carry no gene symbol (unannotated loci); they cannot be used by
  # any symbol-keyed gene set and are dropped rather than collapsed into one row
  ok <- !is.na(d$gene_name) & nzchar(d$gene_name)
  if (any(!ok)) message(sprintf("  %s: dropped %d rows without a gene symbol", gse, sum(!ok)))
  d <- d[ok, , drop = FALSE]
  m <- round(as.matrix(d[, -(1:2)]))
  rowsum(m, group = d$gene_name, reorder = FALSE)
}
`%||%` <- function(a, b) if (is.null(a)) b else a

EXP <- list(
  progression = list(
    gse = "GSE239754",
    cond = function(x) sub("^CRC-([A-Za-z]+)-rep.*$", "\\1", x),
    batch = NULL,
    contrasts = list(
      c("A_vs_WT",    "A",    "WT",   "progression"),
      c("AKSP_vs_WT", "AKSP", "WT",   "progression"),
      c("AKSP_vs_A",  "AKSP", "A",    "progression"))),

  yap_oe = list(
    gse = "GSE263050",
    cond = function(x) sub("_batch[0-9]+$", "", x),
    batch = function(x) sub(".*_batch", "b", x),
    contrasts = list(
      c("YAPOE_vs_EV",        "WT_YAP_EV",  "WT_EV_HA",  "YAP gain"),
      c("YAPOE_FOS_vs_EV",    "WT_YAP_FOS", "WT_EV_HA",  "YAP+AP-1 gain"),
      c("YAPOE_FOS_vs_YAPOE", "WT_YAP_FOS", "WT_YAP_EV", "AP-1 gain on YAP"))),

  fos_dn = list(
    gse = "GSE263056",
    cond = function(x) sub("_batch_[0-9]+$", "", x),
    batch = function(x) sub(".*_batch_", "b", x),
    contrasts = list(
      c("Apcloss_vs_WT",        "OHT_EV",     "EV",     "progression"),
      c("FOSDN_vs_EV_in_Apcloss","OHT_FOS_DN","OHT_EV", "AP-1 loss"))),

  aksp_kd = list(
    gse = "GSE263055",
    cond = function(x) sub("_b[0-9]+$", "", x),
    batch = function(x) sub(".*_b", "b", x),
    contrasts = list(
      c("YAPsh1_vs_scr", "VAKPS_scr_yap_sh1", "VAKPS_scr", "YAP loss"),
      c("YAPsh2_vs_scr", "VAKPS_scr_yap_sh2", "VAKPS_scr", "YAP loss"),
      c("FOSkd_vs_scr",  "VAKPS_fos_kd",      "VAKPS_scr", "AP-1 loss"))),

  onf_reporter = list(
    gse = "GSE235205",
    cond = function(x) sub("_rep[0-9]+$", "", x),
    batch = function(x) sub(".*_rep", "r", x),
    contrasts = list(
      c("OnFreporter_high_vs_neg", "Fetal_high", "Fetal_neg", "oncofetal state"))),

  rxr = list(
    gse = "GSE263045",
    cond = function(x) sub("_rep[0-9]+$", "", x),
    batch = NULL,
    contrasts = list(
      c("RXROE_vs_EV_WT",      "RO_DMSO",    "EV_DMSO",    "RXR gain"),
      c("RXROE_vs_EV_Apcloss", "RO_O_IC_P2", "EV_O_IC_P2", "RXR gain"))),

  rxri_aksp = list(
    gse = "GSE263044",
    cond = function(x) sub("_B[0-9]+$", "", x),
    batch = function(x) sub(".*_B", "b", x),
    contrasts = list(
      c("RXRi_vs_DMSO_AKSP", "RXRiLow", "DMSO", "RXR loss")))
)

SIGS <- load_signatures()

run_series <- function(nm, spec) {
  cnt <- read_counts(spec$gse)
  cond <- factor(spec$cond(colnames(cnt)))
  cd <- data.frame(cond = cond, row.names = colnames(cnt))
  form <- ~cond
  if (!is.null(spec$batch)) {
    cd$batch <- factor(spec$batch(colnames(cnt)))
    if (nlevels(cd$batch) > 1 && all(table(cd$cond, cd$batch) > 0 | TRUE)) form <- ~batch + cond
  }
  cnt <- cnt[rowSums(cnt >= 10) >= min(table(cond)), ]
  dds <- DESeqDataSetFromMatrix(cnt, cd, form)
  dds <- suppressMessages(DESeq(dds, quiet = TRUE))
  cat(sprintf("\n[%s] %s  design %s  %d genes, %d samples\n", nm, spec$gse,
              deparse(form), nrow(cnt), ncol(cnt)))
  print(table(cd$cond))

  lapply(spec$contrasts, function(ct) {
    r <- as.data.frame(results(dds, contrast = c("cond", ct[2], ct[3])))
    r$gene <- rownames(r)
    r <- r[is.finite(r$stat), ]
    list(name = ct[1], series = nm, gse = spec$gse, axis = ct[4],
         num = ct[2], den = ct[3],
         n_num = sum(cd$cond == ct[2]), n_den = sum(cd$cond == ct[3]), res = r)
  })
}

ALL <- unlist(lapply(names(EXP), function(n) run_series(n, EXP[[n]])), recursive = FALSE)

## ---- (A) the receptor, contrast by contrast --------------------------------
gene_row <- function(co, g) {
  r <- co$res[co$res$gene == g, ]
  if (!nrow(r)) return(data.frame(log2FC = NA, lfcSE = NA, stat = NA, pvalue = NA,
                                  padj = NA, baseMean = NA, rank_abs = NA, n_genes = nrow(co$res)))
  data.frame(log2FC = r$log2FoldChange[1], lfcSE = r$lfcSE[1], stat = r$stat[1],
             pvalue = r$pvalue[1], padj = r$padj[1], baseMean = r$baseMean[1],
             rank_abs = sum(abs(co$res$stat) > abs(r$stat[1])) + 1, n_genes = nrow(co$res))
}
resA <- do.call(rbind, lapply(ALL, function(co) {
  cbind(data.frame(contrast = co$name, gse = co$gse, axis = co$axis,
                   numerator = co$num, denominator = co$den,
                   n_num = co$n_num, n_den = co$n_den, gene = RECEPTOR),
        gene_row(co, RECEPTOR))
}))
# the ligand, and the two canonical targets, for context
resA2 <- do.call(rbind, lapply(ALL, function(co) {
  do.call(rbind, lapply(c(LIGAND, "Ctgf", "Cyr61", "Fos", "Yap1"), function(g)
    cbind(data.frame(contrast = co$name, gse = co$gse, axis = co$axis,
                     numerator = co$num, denominator = co$den,
                     n_num = co$n_num, n_den = co$n_den, gene = g),
          gene_row(co, g))))
}))
resA_all <- rbind(resA, resA2)
write_tsv(resA_all, "Q2A_gene_level_per_contrast.tsv")
cat("\n=== (A) Tnfrsf12a per contrast ===\n")
print(resA[, c("contrast", "axis", "n_num", "n_den", "log2FC", "pvalue", "padj",
               "rank_abs", "n_genes")], row.names = FALSE, digits = 3)

## ---- (B) programme level ---------------------------------------------------
resB <- do.call(rbind, lapply(ALL, function(co) {
  st <- setNames(co$res$stat, co$res$gene)
  idx <- lapply(SIGS, function(s) which(names(st) %in% s))
  idx <- idx[lengths(idx) >= 5]
  cm <- cameraPR(st, idx, use.ranks = FALSE)
  data.frame(contrast = co$name, gse = co$gse, axis = co$axis,
             set = rownames(cm), n_genes = cm$NGenes, direction = cm$Direction,
             p = cm$PValue, FDR = cm$FDR,
             mean_stat = vapply(rownames(cm), function(s) mean(st[idx[[s]]]), 0),
             row.names = NULL)
}))
resB$FDR_global <- p.adjust(resB$p, "BH")
write_tsv(resB, "Q2B_programme_level_per_contrast.tsv")

cat("\n=== (B) programmes in the YAP / AP-1 contrasts (cameraPR) ===\n")
key <- resB %>% filter(axis %in% c("YAP gain", "YAP+AP-1 gain", "AP-1 gain on YAP",
                                   "AP-1 loss", "YAP loss"),
                       set %in% c("paper_mOnF", "paper_mStem", "project_revCSC",
                                  "project_YAP_regen", "mapped_placenta_troph",
                                  "mapped_IFA_core", "mapped_TRA_core", "mapped_EVT_core",
                                  "project_Immune_suppression",
                                  "project_Cytotoxic_resistance")) %>%
  select(contrast, axis, set, n_genes, direction, mean_stat, p, FDR_global) %>%
  arrange(axis, contrast, set)
print(as.data.frame(key), row.names = FALSE, digits = 3)

## ---- (C) does the receptor move with the oncofetal programme? --------------
# Across contrasts, the receptor's Wald statistic against the mOnF programme's.
onf <- resB %>% filter(set == "paper_mOnF") %>% select(contrast, onf_stat = mean_stat)
cc <- resA %>% select(contrast, axis, rec_stat = stat, rec_log2FC = log2FC, rec_padj = padj) %>%
  left_join(onf, by = "contrast")
ct <- cor.test(cc$rec_stat, cc$onf_stat, method = "spearman")
write_tsv(as.data.frame(cc), "Q2C_receptor_vs_onf_across_contrasts.tsv")
cat(sprintf("\n=== (C) receptor Wald stat vs mOnF programme stat across %d contrasts ===\n  Spearman rho = %.3f, P = %.4f\n",
            nrow(cc), unname(ct$estimate), ct$p.value))
print(as.data.frame(cc), row.names = FALSE, digits = 3)

## ---- (D) the contrast with no deposited counts -----------------------------
# GSE263047: YAP shRNA / FOS knockdown during initiation. Read from the authors'
# DESeq2 output. The table is pre-filtered to significant genes, so absence of a
# gene means "not significant", not "not tested" - recorded explicitly.
s2 <- read.delim(file.path(SUPPL, "Table_S2c.tsv"), header = FALSE,
                 stringsAsFactors = FALSE, check.names = FALSE, na.strings = character(0))
# the sheet is a row of contrast labels over side-by-side DESeq2 blocks separated
# by a blank column; anchor on the field names rather than on the blank columns
h2 <- as.character(unlist(s2[2, ], use.names = FALSE))
blocks <- which(h2 == "baseMean")
labels <- vapply(blocks, function(j) as.character(s2[1, j]), "")
resD <- do.call(rbind, lapply(seq_along(blocks), function(i) {
  cols <- blocks[i]:(blocks[i] + 7)
  b <- s2[-(1:2), cols, drop = FALSE]
  names(b) <- h2[cols]
  b <- b[nzchar(b$gene_name), ]
  hit <- b[b$gene_name == RECEPTOR, ]
  data.frame(contrast = labels[i], source = "Supplementary Table S2c",
             n_significant_genes = nrow(b),
             receptor_present = nrow(hit) > 0,
             log2FC = if (nrow(hit)) as.numeric(hit$log2FoldChange[1]) else NA,
             padj = if (nrow(hit)) as.numeric(hit$padj[1]) else NA,
             status = if (nrow(hit)) hit$status[1] else "not in significant list",
             row.names = NULL)
}))
write_tsv(resD, "Q2D_initiation_YAP_FOS_from_supplementary.tsv")
cat("\n=== (D) YAP / FOS knockdown during initiation (authors' DESeq2, GSE263047) ===\n")
print(resD, row.names = FALSE, digits = 3)

saveRDS(lapply(ALL, function(co) c(co[c("name", "series", "gse", "axis")],
                                   list(stat = setNames(co$res$stat, co$res$gene)))),
        file.path(PROC, "bulk_contrast_stats.rds"))
cat("\ndone\n")
