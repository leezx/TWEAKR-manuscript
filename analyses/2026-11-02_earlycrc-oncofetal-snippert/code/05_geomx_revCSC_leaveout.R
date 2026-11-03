# Circularity check raised during review of EC1/EC2.
#
# TNFRSF12A is a member of the revCSC gene set (1 of 32 genes; 1 of the 12 that
# are on the GeoMx CTA panel, 1 of 29 on the WTA panel). The invasive-front
# enrichment of revCSC in EC1 and the invasive-front upregulation of TNFRSF12A in
# EC2 are therefore NOT independent observations, and the manuscript must not
# present them as mutual corroboration.
#
# This script repeats the inv-vs-core contrast for revCSC with TNFRSF12A removed,
# so that the programme-level and gene-level results can be stated separately.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({
  library(GeomxTools); library(Biobase); library(singscore); library(dplyr); library(tidyr)
})
set.seed(20261102)

SIGS <- load_signatures(); N_NULL <- 200; REGS <- c("nor", "ade", "core", "inv")
SETS <- list(revCSC = SIGS$revCSC,
             revCSC_minus_TNFRSF12A = setdiff(SIGS$revCSC, "TNFRSF12A"))

get_exp <- function(e) {
  o <- readRDS(file.path(ZENODO, "extracted/Nanostring_GeoMx", e, "r_object",
                         sprintf("geomx_%s_target_Data_norm.RDS", e)))
  m <- Biobase::assayDataElement(o, "log_q_combat"); pd <- Biobase::pData(o); nm <- names(pd)
  ann <- data.frame(segment_id = rownames(pd),
                    patient = as.character(pd[[grep("^Patient_ID$", nm)[1]]]),
                    region  = tolower(as.character(pd[[grep("^tissueRegion$", nm)[1]]])),
                    segment = as.character(pd[[grep("^segment$", nm)[1]]]))
  k <- ann$region %in% REGS
  list(expr = m[, k, drop = FALSE], ann = ann[k, ])
}

inv_core <- function(score, ann) {
  w <- data.frame(segment_id = names(score), score = as.numeric(score)) %>%
    left_join(ann, by = "segment_id") %>%
    group_by(patient, region) %>% summarise(s = mean(score), .groups = "drop") %>%
    pivot_wider(names_from = region, values_from = s)
  if (!all(c("inv", "core") %in% names(w))) return(NULL)
  w <- w[complete.cases(w[, c("inv", "core")]), ]; if (nrow(w) < 3) return(NULL)
  d <- w$inv - w$core
  list(n = nrow(w), diff = mean(d), n_pos = sum(d > 0),
       p = suppressWarnings(wilcox.test(d)$p.value))
}

out <- list()
for (e in c("exp1", "exp2")) {
  G <- get_exp(e)
  bins <- cut(rank(rowMeans(G$expr), ties.method = "first"), breaks = 10, labels = FALSE)
  names(bins) <- rownames(G$expr)
  for (seg in c("PanCK+", "PanCK-")) {
    ann <- G$ann[G$ann$segment == seg, ]
    mat <- G$expr[, ann$segment_id, drop = FALSE]
    rk <- singscore::rankGenes(mat)
    sc1 <- function(gs) { ss <- singscore::simpleScore(rk, upSet = gs, centerScore = TRUE)
                          setNames(ss$TotalScore, rownames(ss)) }
    for (nm in names(SETS)) {
      g <- intersect(SETS[[nm]], rownames(mat)); if (length(g) < 5) next
      eff <- inv_core(sc1(g), ann); if (is.null(eff)) next
      tb <- table(bins[g])
      nd <- vapply(seq_len(N_NULL), function(i) {
        gs <- unlist(lapply(names(tb), function(b) {
          cand <- names(bins)[bins == b]; sample(cand, min(tb[[b]], length(cand)))
        }), use.names = FALSE)
        x <- inv_core(sc1(gs), ann); if (is.null(x)) NA_real_ else x$diff
      }, numeric(1))
      nd <- nd[is.finite(nd)]
      out[[length(out) + 1]] <- data.frame(
        exp = e, segment = seg, set = nm, n_genes_used = length(g),
        n_patients = eff$n, mean_diff_inv_core = eff$diff, n_patients_positive = eff$n_pos,
        p_paired = eff$p, z_vs_matched_null = (eff$diff - mean(nd)) / sd(nd),
        p_matched_null = (sum(abs(nd - mean(nd)) >= abs(eff$diff - mean(nd))) + 1) / (length(nd) + 1))
    }
  }
}
res <- bind_rows(out) %>% arrange(exp, segment, set)
write_tsv(res, "Q5_revCSC_leaveout_TNFRSF12A.tsv")
cat("\n=== revCSC with and without TNFRSF12A ===\n"); print(as.data.frame(res), digits = 3)
cat("\ndone\n")
