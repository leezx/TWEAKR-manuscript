# Two review items in one pass, because both need the same neighbour graphs.
#
# (A) Detection-density audit of the EC3c result.
#     EC3c showed that defining oncofetal cells by a revCSC score decile makes
#     every ligand appear colocalised, and that detection-matched control genes
#     score even higher. The review asked, correctly, that we not call this an
#     artefact until the mechanism is pinned down. So:
#       1. the state score is recomputed with per-cell detection depth, gene
#          count and cell area regressed out
#       2. the comparison set is stratified by field of view AND detection
#          quintile, so oncofetal cells are only compared with malignant cells
#          imaged in the same field at similar depth
#       3. the test is repeated at 20, 50 and 100 um rather than at a single
#          pre-chosen scale
#       4. the question is whether the ligand-versus-control-gene gap survives
#     TNFRSF12A is removed from the revCSC set wherever the set defines the
#     state, because the receptor is a member of it.
#
# (B) Receptor-conditioned proximity, conditional on P0 (script 06) being
#     positive. Whole-tumour averages can dilute a small local niche. Among
#     oncofetal cells only, do the TNFRSF12A-positive ones sit closer to
#     TWEAK-positive macrophages than the TNFRSF12A-negative ones do? Control
#     genes go through the identical test.
#
# Unit: the patient. Nulls permute the gene-positive label within field of view
# among cells of the same source class, so tissue architecture and the number of
# positive cells are held fixed.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(Matrix); library(RANN); library(dplyr); library(tidyr)})
set.seed(20261102)

RADII <- c(20, 50, 100)
KMAX  <- c(`20` = 120, `50` = 300, `100` = 700)
N_PERM <- 100
MAX_QUERY <- 20000      # malignant cells sampled per patient, fixed across radii
N_QUINTILE <- 5
MIN_STRATUM <- 10

D <- readRDS(file.path(ZENODO, "cosmx_exp2_compact.rds"))
C <- readRDS(file.path(ZENODO, "cosmx_exp2_control_genes.rds"))
SIGS <- load_signatures()

md <- D$meta
md$patient <- as.character(md$patient_ID); md$fov <- as.character(md$fov)
md$celltype <- as.character(md$cellType)
md$x <- as.numeric(md$x_slide_mm) * 1000; md$y <- as.numeric(md$y_slide_mm) * 1000
md$depth <- as.numeric(md$nCount_RNA)
md$ngene <- as.numeric(md$nFeature_RNA)
md$area  <- as.numeric(md$Area.um2)
md$is_malig <- md$celltype %in% c("CRC", "oncofetal")
md$is_mac <- grepl("macrophage|myeloid|mono", md$celltype, ignore.case = TRUE)
md$onf_authors <- md$celltype == "oncofetal"

cpm <- Matrix::t(Matrix::t(D$counts) / pmax(D$total, 1)) * 1e4
g_rev <- setdiff(intersect(SIGS$revCSC, rownames(cpm)), "TNFRSF12A")
md$score_raw <- Matrix::colMeans(log1p(cpm)[g_rev, , drop = FALSE])

# depth-, complexity- and area-residualised version of the same score
md$score_resid <- NA_real_
for (p in unique(md$patient)) {
  k <- which(md$patient == p)
  d <- data.frame(s = md$score_raw[k], a = log1p(md$depth[k]),
                  b = log1p(md$ngene[k]), c = log1p(md$area[k]))
  ok <- complete.cases(d)
  fit <- lm(s ~ a + b + c, data = d[ok, ])
  md$score_resid[k[ok]] <- residuals(fit)
}
md <- md %>% group_by(patient) %>%
  mutate(onf_raw   = is_malig & score_raw   >= quantile(score_raw[is_malig], .90, na.rm = TRUE),
         onf_resid = is_malig & score_resid >= quantile(score_resid[is_malig], .90, na.rm = TRUE)) %>%
  ungroup()
cat(sprintf("score residualised on depth, gene count and area; agreement of the two deciles: %.1f%%\n",
            100 * mean(md$onf_raw[md$is_malig] == md$onf_resid[md$is_malig])))

GENES <- unique(c("TNFSF12", "TGFB1", "TGFB3", "IL36G", rownames(C$counts)))
GENES <- GENES[GENES %in% c(rownames(D$counts), rownames(C$counts))]
KIND <- ifelse(GENES %in% c("TNFSF12", "TGFB1", "TGFB3", "IL36G"), "ligand", "control")
names(KIND) <- GENES
getg <- function(g) {
  if (g %in% rownames(C$counts)) as.numeric(C$counts[g, colnames(D$counts)])
  else as.numeric(D$counts[g, ])
}
rec_pos_all <- as.numeric(D$counts["TNFRSF12A", ]) > 0

#' Weight vector for a stratified group difference.
#' The statistic
#'     sum_s (n_s / N) * ( mean_{a in s} v - mean_{b in s} v )
#' is LINEAR in v, so it can be written as crossprod(w, v) for a fixed w that
#' depends only on the strata and the two groups. Precomputing w turns each
#' permutation into one matrix-vector product instead of a re-split of the data.
strat_weights <- function(grpA, grpB, stratum) {
  w <- numeric(length(stratum))
  tot <- 0
  for (ix in split(seq_along(stratum), stratum)) {
    a <- ix[grpA[ix]]; b <- ix[grpB[ix]]
    if (length(a) < MIN_STRATUM || length(b) < MIN_STRATUM) next
    n <- length(a); tot <- tot + n
    w[a] <- w[a] + n / length(a)
    w[b] <- w[b] - n / length(b)
  }
  if (tot == 0) return(NULL)
  w / tot
}

#' Unstratified difference, same linear form.
plain_weights <- function(grpA, grpB) {
  if (!sum(grpA) || !sum(grpB)) return(NULL)
  grpA / sum(grpA) - grpB / sum(grpB)
}

out <- list()
for (p in unique(md$patient)) {
  kp <- which(md$patient == p & is.finite(md$x) & is.finite(md$y))
  mal <- kp[md$is_malig[kp]]
  if (length(mal) < 200) next
  q <- if (length(mal) > MAX_QUERY) sort(sample(mal, MAX_QUERY)) else mal
  qd <- data.frame(fov = md$fov[q], depth = md$depth[q])
  qd$quint <- ave(qd$depth, qd$fov, FUN = function(x)
    as.integer(cut(rank(x, ties.method = "first"), breaks = N_QUINTILE, labels = FALSE)))
  stratum <- paste(qd$fov, qd$quint)

  A <- md$onf_authors[q]; R <- md$onf_raw[q]; S <- md$onf_resid[q]
  rec <- rec_pos_all[q]
  # the five contrasts, as fixed weight vectors over the query cells
  W <- list(authors_plain      = plain_weights(A, !A),
            authors_strat      = strat_weights(A, !A, stratum),
            revCSCraw_strat    = strat_weights(R, !R, stratum),
            revCSCresid_strat  = strat_weights(S, !S, stratum),
            receptor_in_onf    = strat_weights(A & rec, A & !rec, stratum))
  keep_w <- !vapply(W, is.null, logical(1))
  if (!any(keep_w)) next
  W <- W[keep_w]
  Wm <- do.call(rbind, W)

  src_sets <- list(all_cells = kp, macrophage = kp[md$is_mac[kp]])
  for (rad in RADII) {
    for (sname in names(src_sets)) {
      src <- src_sets[[sname]]
      if (length(src) < 50) next
      nn <- RANN::nn2(cbind(md$x[src], md$y[src]), cbind(md$x[q], md$y[q]),
                      k = min(length(src), KMAX[[as.character(rad)]]),
                      searchtype = "radius", radius = rad)
      idx <- nn$nn.idx
      nzi <- which(idx > 0, arr.ind = TRUE)
      if (!nrow(nzi)) next
      M <- Matrix::sparseMatrix(i = nzi[, 1], j = idx[idx > 0], x = 1,
                                dims = c(nrow(idx), length(src)))
      truncated <- mean(rowSums(idx > 0) >= ncol(idx) - 1)
      # collapse the contrast weights through the neighbour graph once:
      # every statistic is then a single product against the gene label
      WM <- as.matrix(Wm %*% M)
      grp <- split(seq_along(src), md$fov[src])

      for (g in GENES) {
        lab <- as.numeric(getg(g)[src] > 0)
        if (sum(lab) < 10) next
        obs <- as.numeric(WM %*% lab)
        nullm <- vapply(seq_len(N_PERM), function(i) {
          l <- lab
          for (ix in grp) if (length(ix) > 1) l[ix] <- lab[sample(ix)]
          as.numeric(WM %*% l)
        }, numeric(nrow(WM)))
        z <- (obs - rowMeans(nullm)) / apply(nullm, 1, sd)
        out[[length(out) + 1]] <- data.frame(
          patient = p, radius = rad, source = sname, gene = g, kind = KIND[[g]],
          contrast = rownames(Wm), obs = obs, z = z,
          frac_truncated = truncated, n_query = length(q), n_source = length(src),
          row.names = NULL)
      }
    }
    cat(".", sep = "")
  }
  cat("|", p, "\n")
}
res <- bind_rows(out)
write_tsv(res, "Q7_density_audit_and_receptor_niche.tsv")

## ---- (A) does the ligand-vs-control gap survive depth control? -------------
gap <- res %>% filter(source == "all_cells", is.finite(z)) %>%
  group_by(radius, contrast, kind) %>%
  summarise(n = n(), median_z = median(z), .groups = "drop") %>%
  pivot_wider(names_from = kind, values_from = c(n, median_z)) %>%
  mutate(ligand_minus_control = median_z_ligand - median_z_control) %>%
  arrange(contrast, radius)
write_tsv(gap, "Q7A_ligand_vs_control_gap.tsv")
cat("\n=== (A) ligand vs control median z, by definition and radius ===\n")
print(as.data.frame(gap), digits = 3)

## ---- (B) receptor-conditioned proximity ------------------------------------
nicheB <- res %>% filter(contrast == "receptor_in_onf", is.finite(z)) %>%
  group_by(radius, source, gene, kind) %>%
  summarise(n_patients = n(), n_pos = sum(z > 0), median_z = median(z),
            p_wilcox = suppressWarnings(wilcox.test(z)$p.value), .groups = "drop") %>%
  group_by(radius, source) %>% mutate(q_BH = p.adjust(p_wilcox, "BH")) %>% ungroup()
write_tsv(nicheB, "Q7B_receptor_conditioned_proximity.tsv")
cat("\n=== (B) TNFRSF12A+ vs TNFRSF12A- oncofetal cells: ligand+ neighbours ===\n")
print(as.data.frame(nicheB %>% filter(kind == "ligand") %>% arrange(source, radius, gene)), digits = 3)
cat("\n=== (B) control-gene distribution for the same contrast ===\n")
print(as.data.frame(nicheB %>% filter(kind == "control") %>% group_by(radius, source) %>%
        summarise(n_genes = n(), median_of_medians = median(median_z),
                  max = max(median_z), n_sig = sum(q_BH < 0.05), .groups = "drop")), digits = 3)
cat("\ntruncation check (fraction of query cells hitting the neighbour cap):\n")
print(res %>% group_by(radius, source) %>% summarise(max_frac = max(frac_truncated), .groups = "drop"))
cat("\ndone\n")
