# Q1, calibration: 01b found several signatures higher at the invasive front than
# in the other three regions combined, including the placenta/trophoblast set in
# 9/9 patients. That contrast was not calibrated, and "higher at the invasive
# front than in normal + adenoma + core" is something any gene set that drifts
# with malignancy will show. This script repeats the inv-vs-rest contrast against
# 200 expression-matched random gene sets of the same size, the same way 01 does
# for inv-vs-core, so the two contrasts can be compared on equal footing.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({
  library(GeomxTools); library(Biobase); library(singscore)
  library(dplyr); library(tidyr)
})
set.seed(20261102)

SIGS <- load_signatures(); N_NULL <- 200
REGS <- c("nor", "ade", "core", "inv")

get_exp <- function(exp_id) {
  rds <- file.path(ZENODO, "extracted/Nanostring_GeoMx", exp_id, "r_object",
                   sprintf("geomx_%s_target_Data_norm.RDS", exp_id))
  o <- readRDS(rds)
  m <- Biobase::assayDataElement(o, "log_q_combat")
  pd <- Biobase::pData(o)
  nm <- names(pd)
  ann <- data.frame(segment_id = rownames(pd),
                    patient = as.character(pd[[grep("^Patient_ID$", nm)[1]]]),
                    region  = tolower(as.character(pd[[grep("^tissueRegion$", nm)[1]]])),
                    segment = as.character(pd[[grep("^segment$", nm)[1]]]))
  k <- ann$region %in% REGS
  list(expr = m[, k, drop = FALSE], ann = ann[k, ])
}

#' Patient-paired difference: invasive front minus the mean of the other regions.
#' Only patients with all four regions contribute, so each patient supplies a
#' complete contrast rather than a partial one.
inv_vs_rest <- function(score, ann) {
  w <- data.frame(segment_id = names(score), score = as.numeric(score)) %>%
    left_join(ann, by = "segment_id") %>%
    group_by(patient, region) %>% summarise(s = mean(score), .groups = "drop") %>%
    pivot_wider(names_from = region, values_from = s)
  cols <- intersect(REGS, names(w)); if (!("inv" %in% cols) || length(cols) < 4) return(NULL)
  w <- w[complete.cases(w[, cols]), ]; if (nrow(w) < 4) return(NULL)
  d <- w$inv - rowMeans(as.matrix(w[, setdiff(cols, "inv"), drop = FALSE]))
  list(n = nrow(w), diff = mean(d), n_pos = sum(d > 0),
       p = suppressWarnings(wilcox.test(d)$p.value))
}

out <- list()
for (exp_id in c("exp1", "exp2")) {
  G <- get_exp(exp_id)
  mu <- rowMeans(G$expr)
  bins <- cut(rank(mu, ties.method = "first"), breaks = 10, labels = FALSE)
  names(bins) <- rownames(G$expr)
  for (seg in unique(G$ann$segment)) {
    ann <- G$ann[G$ann$segment == seg, ]
    mat <- G$expr[, ann$segment_id, drop = FALSE]
    rk <- singscore::rankGenes(mat)
    sc1 <- function(gs) {
      ss <- singscore::simpleScore(rk, upSet = gs, centerScore = TRUE)
      setNames(ss$TotalScore, rownames(ss))
    }
    for (s in names(SIGS)) {
      g <- intersect(SIGS[[s]], rownames(mat)); if (length(g) < 5) next
      eff <- inv_vs_rest(sc1(g), ann); if (is.null(eff)) next
      tb <- table(bins[g])
      nd <- vapply(seq_len(N_NULL), function(i) {
        gs <- unlist(lapply(names(tb), function(b) {
          cand <- names(bins)[bins == b]; sample(cand, min(tb[[b]], length(cand)))
        }), use.names = FALSE)
        e <- inv_vs_rest(sc1(gs), ann); if (is.null(e)) NA_real_ else e$diff
      }, numeric(1))
      nd <- nd[is.finite(nd)]
      out[[length(out) + 1]] <- data.frame(
        exp = exp_id, segment = seg, signature = s, n_genes_used = length(g),
        n_patients = eff$n, mean_diff_inv_vs_rest = eff$diff,
        n_patients_positive = eff$n_pos, p_paired = eff$p,
        null_mean = mean(nd), null_sd = sd(nd),
        z_vs_matched_null = (eff$diff - mean(nd)) / sd(nd),
        p_matched_null = (sum(abs(nd - mean(nd)) >= abs(eff$diff - mean(nd))) + 1) / (length(nd) + 1))
    }
  }
}
stats <- bind_rows(out) %>% group_by(exp, segment) %>%
  mutate(q_paired_BH = p.adjust(p_paired, "BH"),
         q_matched_null_BH = p.adjust(p_matched_null, "BH")) %>%
  ungroup() %>% arrange(exp, segment, p_matched_null)
write_tsv(stats, "Q1c_inv_vs_rest_matched_null.tsv")

cat("\n=== inv vs rest, PanCK+ (matched-null calibrated) ===\n")
print(as.data.frame(stats %>% filter(segment == "PanCK+") %>%
  select(exp, signature, n_patients, mean_diff_inv_vs_rest, n_patients_positive,
         p_paired, z_vs_matched_null, p_matched_null, q_matched_null_BH)), digits = 3)
cat("\ndone\n")
