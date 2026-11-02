# Review response. Four audits, each asking whether a reported result survives
# removing the thing that could have manufactured it.
#
# (A) Are the mOnF score and the lineage plasticity score independent?
#     They are not: 14 of the 51 mOnF genes are also in the esophagus mucosa
#     module that forms the positive arm of the plasticity score (the colon arm
#     shares none). So part of the Tnfrsf12a-vs-plasticity correlation could be
#     the Tnfrsf12a-vs-mOnF correlation seen twice. The plasticity score is
#     recomputed with the shared genes removed.
#
# (B) Is the placenta signal a placental programme, or generic YAP / oncofetal /
#     invasion biology wearing a trophoblast label? The set is stripped of genes
#     shared with the YAP target sets, the mOnF signature and revCSC, and the
#     test is repeated on what is left.
#
# (C) The immune sets are 10 and 6 genes. A competitive test on a set that small
#     can be carried by one or two genes. Every gene's Wald statistic is reported
#     per contrast, and the test is repeated leaving out the strongest gene.
#
# (D) The 15 contrasts behind the rho = 0.975 figure are not independent - some
#     share a control arm. The correlation is recomputed on a maximal mutually
#     non-overlapping subset.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(Matrix); library(Seurat); library(limma); library(dplyr)})
set.seed(SEED)

SIGS <- load_signatures()
N_QUINTILE <- 5

## ===== (A) mOnF / plasticity independence ==================================
shared <- intersect(SIGS$paper_mOnF, SIGS$paper_esophagus)
cat(sprintf("\n=== (A) mOnF n esophagus = %d of %d mOnF genes; mOnF n colon = %d ===\n",
            length(shared), length(SIGS$paper_mOnF),
            length(intersect(SIGS$paper_mOnF, SIGS$paper_colon))))
cat("  shared:", paste(shared, collapse = ", "), "\n")

EXT <- file.path(RAW, "GSE240129/ext")
LIBS <- c(WT = "GSM7682755_wt", A = "GSM7682756_a", AKSP = "GSM7682757_aksp")
read_lib <- function(pre) {
  m <- Matrix::readMM(gzfile(file.path(EXT, paste0(pre, "_matrix.mtx.gz"))))
  f <- read.delim(gzfile(file.path(EXT, paste0(pre, "_features.tsv.gz"))),
                  header = FALSE, stringsAsFactors = FALSE)
  rownames(m) <- make.unique(f[[2]])
  colnames(m) <- readLines(gzfile(file.path(EXT, paste0(pre, "_barcodes.tsv.gz"))))
  as(m, "CsparseMatrix")
}
mats <- lapply(LIBS, read_lib)
genes <- Reduce(intersect, lapply(mats, rownames))
cnt <- do.call(cbind, lapply(names(mats), function(g) {
  x <- mats[[g]][genes, ]; colnames(x) <- paste0(g, "_", colnames(x)); x }))
rm(mats); gc()
obj <- CreateSeuratObject(cnt, meta.data = data.frame(
  genotype = factor(sub("_.*", "", colnames(cnt)), levels = names(LIBS)),
  row.names = colnames(cnt)))
obj$percent_mt <- PercentageFeatureSet(obj, pattern = "^mt-")
obj <- obj[, obj$nFeature_RNA >= 500 & obj$nCount_RNA >= 1000 & obj$percent_mt < 25]
obj <- NormalizeData(obj, verbose = FALSE)

sets_A <- list(mOnF      = intersect(SIGS$paper_mOnF, rownames(obj)),
               eso_full  = intersect(SIGS$paper_esophagus, rownames(obj)),
               eso_clean = intersect(setdiff(SIGS$paper_esophagus, shared), rownames(obj)),
               colon     = intersect(SIGS$paper_colon, rownames(obj)),
               mOnF_clean = intersect(setdiff(SIGS$paper_mOnF, shared), rownames(obj)))
obj <- AddModuleScore(obj, features = sets_A, name = "sA_", seed = SEED)
colnames(obj@meta.data)[match(paste0("sA_", seq_along(sets_A)),
                              colnames(obj@meta.data))] <- names(sets_A)
md <- obj@meta.data
md$depth <- obj$nCount_RNA
md$plast_full  <- md$eso_full  - md$colon      # as published
md$plast_clean <- md$eso_clean - md$colon      # mOnF genes removed from the axis
lg <- GetAssayData(obj, layer = "data")

det <- tabulate(GetAssayData(obj, layer = "counts")@i + 1L, nbins = nrow(obj)) / ncol(obj)
names(det) <- rownames(obj)
cand <- setdiff(names(det), unique(c(unlist(SIGS), RECEPTOR, LIGAND)))
controls <- names(sort(abs(det[cand] - det[RECEPTOR])))[1:24]
GENES <- c(RECEPTOR, controls)

partial_sp <- function(x, y, z)
  cor(residuals(lm(rank(x) ~ rank(z))), residuals(lm(rank(y) ~ rank(z))))

resA <- do.call(rbind, lapply(levels(md$genotype), function(g) {
  k <- which(md$genotype == g); dp <- log(md$depth[k])
  do.call(rbind, lapply(c("plast_full", "plast_clean"), function(ax) {
    lp <- md[[ax]][k]
    rho <- vapply(GENES, function(gg) partial_sp(as.numeric(lg[gg, k]), lp, dp), 0)
    data.frame(genotype = g, axis = ax, n_axis_genes = length(sets_A[[
                 if (ax == "plast_full") "eso_full" else "eso_clean"]]) + length(sets_A$colon),
               rho_receptor = rho[[RECEPTOR]],
               ctrl_median = median(rho[-1]), ctrl_max = max(rho[-1]),
               n_ctrl_above = sum(rho[-1] > rho[[RECEPTOR]]),
               rho_mOnF_vs_axis = cor(md$mOnF[k], lp, method = "spearman"),
               rho_mOnFclean_vs_axis = cor(md$mOnF_clean[k], lp, method = "spearman"),
               row.names = NULL)
  }))
}))
write_tsv(resA, "Q5A_plasticity_axis_independence.tsv")
cat("\n--- Tnfrsf12a vs the plasticity axis, before and after removing the 14 shared genes ---\n")
print(resA, row.names = FALSE, digits = 3)

## ===== (B) placenta decomposition ==========================================
CON <- readRDS(file.path(PROC, "bulk_contrast_stats.rds"))
yap_targets <- union(SIGS$project_YAP_regen, SIGS$project_YAP_effectors)
drop <- unique(c(yap_targets, SIGS$paper_mOnF, SIGS$project_revCSC))

pla_variants <- list(
  placenta_full          = SIGS$mapped_placenta_troph,
  placenta_minus_YAP     = setdiff(SIGS$mapped_placenta_troph, yap_targets),
  placenta_minus_OnF_YAP = setdiff(SIGS$mapped_placenta_troph, drop),
  EVT_full               = SIGS$mapped_EVT_core,
  EVT_minus_OnF_YAP      = setdiff(SIGS$mapped_EVT_core, drop),
  TRA_minus_OnF_YAP      = setdiff(SIGS$mapped_TRA_core, drop),
  IFA_minus_OnF_YAP      = setdiff(SIGS$mapped_IFA_core, drop))
cat("\n=== (B) placenta-family sets after removing YAP targets / mOnF / revCSC ===\n")
print(data.frame(set = names(pla_variants), n = lengths(pla_variants)), row.names = FALSE)

KEY <- c("YAPOE_vs_EV", "YAPOE_FOS_vs_EV", "FOSDN_vs_EV_in_Apcloss",
         "YAPsh1_vs_scr", "YAPsh2_vs_scr", "FOSkd_vs_scr")
camera_on <- function(sets) {
  do.call(rbind, lapply(CON, function(co) {
    if (!co$name %in% KEY) return(NULL)
    st <- co$stat
    idx <- lapply(sets, function(s) which(names(st) %in% s))
    idx <- idx[lengths(idx) >= 5]
    if (!length(idx)) return(NULL)
    cm <- cameraPR(st, idx, use.ranks = FALSE)
    data.frame(contrast = co$name, axis = co$axis, set = rownames(cm),
               n_genes = cm$NGenes, direction = cm$Direction, p = cm$PValue,
               mean_stat = vapply(rownames(cm), function(s) mean(st[idx[[s]]]), 0),
               row.names = NULL)
  }))
}
resB <- camera_on(pla_variants)
resB$FDR <- p.adjust(resB$p, "BH")
write_tsv(resB, "Q5B_placenta_decomposition.tsv")
cat("\n--- does the placenta signal survive? ---\n")
print(as.data.frame(resB %>% filter(grepl("^placenta|^EVT", set)) %>%
        select(contrast, set, n_genes, mean_stat, p, FDR) %>% arrange(set, contrast)),
      row.names = FALSE, digits = 3)

## ===== (C) immune set audit ================================================
imm <- list(Immune_suppression = SIGS$project_Immune_suppression,
            Cytotoxic_resistance = SIGS$project_Cytotoxic_resistance)
resC_genes <- do.call(rbind, lapply(CON, function(co) {
  if (!co$name %in% KEY) return(NULL)
  do.call(rbind, lapply(names(imm), function(sn) {
    g <- intersect(imm[[sn]], names(co$stat))
    data.frame(contrast = co$name, set = sn, gene = g,
               stat = unname(co$stat[g]), row.names = NULL)
  }))
}))
write_tsv(resC_genes, "Q5C_immune_gene_level.tsv")

# leave out the single strongest gene per set per contrast
resC <- do.call(rbind, lapply(CON, function(co) {
  if (!co$name %in% KEY) return(NULL)
  st <- co$stat
  do.call(rbind, lapply(names(imm), function(sn) {
    g <- intersect(imm[[sn]], names(st))
    if (length(g) < 5) return(NULL)
    top <- g[which.max(abs(st[g]))]
    full <- cameraPR(st, list(s = which(names(st) %in% g)), use.ranks = FALSE)
    lo   <- cameraPR(st, list(s = which(names(st) %in% setdiff(g, top))), use.ranks = FALSE)
    data.frame(contrast = co$name, set = sn, n_genes = length(g),
               mean_stat_full = mean(st[g]), p_full = full$PValue,
               top_gene = top, top_stat = unname(st[top]),
               mean_stat_minus_top = mean(st[setdiff(g, top)]), p_minus_top = lo$PValue,
               n_same_sign = sum(sign(st[g]) == sign(mean(st[g]))), row.names = NULL)
  }))
}))
write_tsv(resC, "Q5C_immune_leave_out_top.tsv")
cat("\n=== (C) immune sets: does the signal survive dropping the strongest gene? ===\n")
print(as.data.frame(resC), row.names = FALSE, digits = 3)

## ===== (D) contrast non-independence =======================================
cc <- read.delim(file.path(TAB, "Q2C_receptor_vs_onf_across_contrasts.tsv"))
# arms behind each contrast, so overlapping ones can be identified
ARMS <- list(
  A_vs_WT = c("GSE239754:A", "GSE239754:WT"),
  AKSP_vs_WT = c("GSE239754:AKSP", "GSE239754:WT"),
  AKSP_vs_A = c("GSE239754:AKSP", "GSE239754:A"),
  YAPOE_vs_EV = c("GSE263050:YAP", "GSE263050:EV"),
  YAPOE_FOS_vs_EV = c("GSE263050:YAPFOS", "GSE263050:EV"),
  YAPOE_FOS_vs_YAPOE = c("GSE263050:YAPFOS", "GSE263050:YAP"),
  Apcloss_vs_WT = c("GSE263056:OHT_EV", "GSE263056:EV"),
  FOSDN_vs_EV_in_Apcloss = c("GSE263056:OHT_FOSDN", "GSE263056:OHT_EV"),
  YAPsh1_vs_scr = c("GSE263055:sh1", "GSE263055:scr"),
  YAPsh2_vs_scr = c("GSE263055:sh2", "GSE263055:scr"),
  FOSkd_vs_scr = c("GSE263055:foskd", "GSE263055:scr"),
  OnFreporter_high_vs_neg = c("GSE235205:high", "GSE235205:neg"),
  RXROE_vs_EV_WT = c("GSE263045:RO_DMSO", "GSE263045:EV_DMSO"),
  RXROE_vs_EV_Apcloss = c("GSE263045:RO_OIC", "GSE263045:EV_OIC"),
  RXRi_vs_DMSO_AKSP = c("GSE263044:RXRi", "GSE263044:DMSO"))
# greedy maximal subset sharing no experimental arm
chosen <- character(0); used <- character(0)
for (nm in cc$contrast[order(-abs(cc$rec_stat))]) {
  a <- ARMS[[nm]]
  if (!any(a %in% used)) { chosen <- c(chosen, nm); used <- c(used, a) }
}
sub <- cc[cc$contrast %in% chosen, ]
ct_all <- cor.test(cc$rec_stat, cc$onf_stat, method = "spearman")
ct_sub <- cor.test(sub$rec_stat, sub$onf_stat, method = "spearman")
resD <- data.frame(
  subset = c("all contrasts", "arm-disjoint subset"),
  n = c(nrow(cc), nrow(sub)),
  rho = c(unname(ct_all$estimate), unname(ct_sub$estimate)),
  p = c(ct_all$p.value, ct_sub$p.value),
  contrasts = c(paste(cc$contrast, collapse = "; "), paste(sort(chosen), collapse = "; ")))
write_tsv(resD, "Q5D_contrast_independence.tsv")
cat("\n=== (D) receptor vs programme, all contrasts and an arm-disjoint subset ===\n")
print(resD[, 1:4], row.names = FALSE, digits = 3)
cat("  arm-disjoint subset:", paste(sort(chosen), collapse = ", "), "\n")
cat("\ndone\n")
