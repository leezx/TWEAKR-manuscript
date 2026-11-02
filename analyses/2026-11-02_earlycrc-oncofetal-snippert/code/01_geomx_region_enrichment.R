# Q1: are proCSC, revCSC and the placenta/trophoblast axes enriched in a
# particular region of early-stage CRC?
#
# Data: Snippert 2026 Nanostring GeoMx bulk spatial transcriptomics (Zenodo 17671259).
#   exp1 = CTA panel, 10 patients, ~1.8k targets, high per-gene sensitivity
#   exp2 = WTA panel,  9 patients, ~18k targets, the panel the paper uses for gene sets
#   Segments: PanCK+ (tumour epithelium) and PanCK- (microenvironment)
#   Regions:  nor (adjacent normal) -> ade (adenoma) -> core (tumour core) -> inv (invasive front)
#   This is the dataset behind the paper's Fig. 1f-h.
#
# Units: the patient. Segment-level scores are averaged within patient x region
#        before any test, so repeated ROIs from one tumour cannot drive a result.
# Calibration: every regional effect is additionally compared against 200
#        expression-matched random gene sets of the same size, because signature
#        size and expression level alone can produce apparent regional structure.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))

suppressMessages({
  library(GeomxTools); library(Biobase); library(singscore)
  library(dplyr); library(tidyr); library(ggplot2)
})
set.seed(20261102)

SIGS <- load_signatures()
N_NULL <- 200
REGION_LEVELS <- c("nor", "ade", "core", "inv")

## ---- load ------------------------------------------------------------------
load_geomx <- function(exp_id) {
  rds <- file.path(ZENODO, "extracted/Nanostring_GeoMx", exp_id, "r_object",
                   sprintf("geomx_%s_target_Data_norm.RDS", exp_id))
  obj <- readRDS(rds)
  elts <- Biobase::assayDataElementNames(obj)
  elt <- if ("log_q_combat" %in% elts) "log_q_combat" else
         if ("log_q" %in% elts) "log_q" else elts[length(elts)]
  m <- Biobase::assayDataElement(obj, elt)
  pd <- Biobase::pData(obj)
  message(sprintf("%s: %d targets x %d segments, using assay '%s' (available: %s)",
                  exp_id, nrow(m), ncol(m), elt, paste(elts, collapse = ", ")))
  list(expr = m, pd = pd, elt = elt, obj = obj)
}

#' Harmonise the annotation columns across the two runs.
harmonise_pd <- function(pd) {
  nm <- names(pd)
  pick <- function(...) { for (p in c(...)) { h <- grep(p, nm, ignore.case = TRUE, value = TRUE)
                            if (length(h)) return(h[1]) }; NA_character_ }
  data.frame(
    segment_id = rownames(pd),
    patient    = as.character(pd[[pick("^Patient_ID$", "patient")]]),
    region     = tolower(as.character(pd[[pick("^tissueRegion$", "region", "segmentRegion")]])),
    segment    = as.character(pd[[pick("^segment$", "SegmentLabel", "panck")]]),
    met_label  = as.character(pd[[pick("metasta")]]),
    stringsAsFactors = FALSE)
}

## ---- scoring ---------------------------------------------------------------
#' singscore on each segment: rank-based, so it is comparable across panels and
#' insensitive to the absolute normalisation of the GeoMx counts.
score_sets <- function(mat, sets) {
  rk <- singscore::rankGenes(mat)
  res <- lapply(names(sets), function(s) {
    g <- intersect(sets[[s]], rownames(mat))
    if (length(g) < 5) return(NULL)
    sc <- singscore::simpleScore(rk, upSet = g, centerScore = TRUE)
    data.frame(signature = s, n_genes_used = length(g),
               segment_id = rownames(sc), score = sc$TotalScore)
  })
  bind_rows(res)
}

#' Size- and expression-matched random sets, used as the null for regional effects.
make_null_sets <- function(mat, k, n = N_NULL, pool_bins, template) {
  tb <- table(pool_bins[template])            # expression-decile profile of the real set
  lapply(seq_len(n), function(i) {
    unlist(lapply(names(tb), function(b) {
      cand <- names(pool_bins)[pool_bins == b]
      sample(cand, min(tb[[b]], length(cand)))
    }), use.names = FALSE)
  })
}

#' Patient-level inv-vs-core effect: mean score per patient x region, then the
#' paired difference across patients.
region_effect <- function(df, a = "inv", b = "core") {
  w <- df %>% group_by(patient, region) %>% summarise(s = mean(score), .groups = "drop") %>%
    filter(region %in% c(a, b)) %>%
    pivot_wider(names_from = region, values_from = s)
  if (!all(c(a, b) %in% names(w))) return(NULL)
  w <- w[complete.cases(w[, c(a, b)]), ]
  if (nrow(w) < 3) return(NULL)
  d <- w[[a]] - w[[b]]
  tt <- suppressWarnings(wilcox.test(d))
  list(n_patients = nrow(w), mean_diff = mean(d), median_diff = median(d),
       p = tt$p.value, n_pos = sum(d > 0))
}

#' Drop targets that are below the limit of quantitation in almost every segment.
#' The WTA panel carries ~18k targets, most of which are not detected in a 100-um
#' segment; leaving them in dilutes any rank-based score. `LOQ` is the per-segment
#' limit of quantitation stored by GeomxTools. The CTA panel has already been
#' filtered to its 1,781 passing targets, so this is a no-op there.
detect_filter <- function(G, min_frac = 0.10) {
  if (!"LOQ" %in% names(G$pd)) return(setNames(rep(TRUE, nrow(G$expr)), rownames(G$expr)))
  qn <- Biobase::assayDataElement(G$obj, "q_norm")
  loq <- as.numeric(unlist(G$pd$LOQ, use.names = FALSE))
  det <- sweep(qn, 2, loq, ">")
  (rowMeans(det, na.rm = TRUE) >= min_frac)[rownames(G$expr)]
}

analyse_exp <- function(exp_id, apply_detect_filter = TRUE, restrict_to = NULL,
                        label = exp_id, drop_patients = NULL) {
  G <- load_geomx(exp_id)
  pd <- harmonise_pd(G$pd)
  stopifnot(all(pd$segment_id == colnames(G$expr)))

  if (!is.null(restrict_to)) {
    g <- intersect(rownames(G$expr), restrict_to)
    cat(sprintf("[%s] restricted to %d shared targets\n", label, length(g)))
    G$expr <- G$expr[g, , drop = FALSE]
  }
  if (apply_detect_filter) {
    keep_g <- detect_filter(G)
    cat(sprintf("[%s] targets kept by detection filter: %d / %d\n",
                exp_id, sum(keep_g), length(keep_g)))
    G$expr <- G$expr[keep_g, , drop = FALSE]
  }

  # keep the four histopathological regions; drop TLS/BONUS/MUS
  keep <- pd$region %in% REGION_LEVELS
  if (!is.null(drop_patients)) {
    cat(sprintf("[%s] dropping patients: %s\n", label, paste(drop_patients, collapse = ", ")))
    keep <- keep & !(pd$patient %in% drop_patients)
  }
  pd <- pd[keep, ]; mat <- G$expr[, keep, drop = FALSE]
  cat(sprintf("\n[%s] segments kept: %d\n", exp_id, ncol(mat)))
  print(table(pd$segment, pd$region))

  sc <- score_sets(mat, SIGS) %>% left_join(pd, by = "segment_id") %>% mutate(exp = label)

  # expression-decile pool for the matched nulls (same for all segments)
  mu <- rowMeans(mat)
  bins <- cut(rank(mu, ties.method = "first"), breaks = 10, labels = FALSE)
  names(bins) <- rownames(mat)

  out <- list()
  for (seg_type in unique(pd$segment)) {
    sub_pd <- pd[pd$segment == seg_type, ]
    sub_mat <- mat[, sub_pd$segment_id, drop = FALSE]
    rk <- singscore::rankGenes(sub_mat)
    for (s in names(SIGS)) {
      g <- intersect(SIGS[[s]], rownames(mat))
      if (length(g) < 5) next
      real <- sc %>% filter(signature == s, segment == seg_type)
      eff <- region_effect(real)
      if (is.null(eff)) next
      # matched null: same patient-level contrast on 200 random sets
      nulls <- make_null_sets(sub_mat, length(g), N_NULL, bins, g)
      nd <- vapply(nulls, function(gs) {
        ss <- singscore::simpleScore(rk, upSet = gs, centerScore = TRUE)
        d <- data.frame(segment_id = rownames(ss), score = ss$TotalScore) %>%
          left_join(sub_pd, by = "segment_id")
        e <- region_effect(d); if (is.null(e)) NA_real_ else e$mean_diff
      }, numeric(1))
      nd <- nd[is.finite(nd)]
      p_null <- (sum(abs(nd) >= abs(eff$mean_diff)) + 1) / (length(nd) + 1)
      out[[length(out) + 1]] <- data.frame(
        exp = label, segment = seg_type, signature = s, n_genes_used = length(g),
        n_patients = eff$n_patients, mean_diff_inv_core = eff$mean_diff,
        median_diff_inv_core = eff$median_diff, n_patients_positive = eff$n_pos,
        p_paired = eff$p, null_mean = mean(nd), null_sd = sd(nd),
        z_vs_matched_null = (eff$mean_diff - mean(nd)) / sd(nd),
        p_matched_null = p_null)
    }
  }
  list(scores = sc, stats = bind_rows(out))
}

res <- lapply(c("exp1", "exp2"), analyse_exp, apply_detect_filter = TRUE)
# sensitivity: score the WTA run inside the CTA target space, to test whether the
# CTA/WTA discordance is a reference-frame effect of rank-based scoring rather
# than a biological difference between the two patient groups.
cta_targets <- rownames(load_geomx("exp1")$expr)
res_cta <- analyse_exp("exp2", restrict_to = cta_targets, label = "exp2_in_CTA_space")
write_tsv(res_cta$stats, "Q1_geomx_region_stats_exp2_in_CTA_space.tsv")

# sensitivity: the WTA run carries one T3 tumour (T1_NANO_013) that the authors
# excluded from most analyses for risk of confounding. Repeat without it.
res_t1 <- analyse_exp("exp2", label = "exp2_T1_only", drop_patients = "T1_NANO_013")
write_tsv(res_t1$stats, "Q1_geomx_region_stats_exp2_T1_only.tsv")

scores <- bind_rows(lapply(res, `[[`, "scores"))
stats  <- bind_rows(lapply(res, `[[`, "stats")) %>%
  group_by(exp, segment) %>%
  mutate(q_paired_BH = p.adjust(p_paired, "BH"),
         q_matched_null_BH = p.adjust(p_matched_null, "BH")) %>% ungroup() %>%
  arrange(exp, segment, p_matched_null)

write_tsv(scores, "Q1_geomx_segment_scores.tsv")
write_tsv(stats,  "Q1_geomx_region_stats.tsv")

## ---- per-region profile (all four regions, patient means) ------------------
profile <- scores %>% group_by(exp, segment, signature, patient, region) %>%
  summarise(score = mean(score), .groups = "drop")
write_tsv(profile, "Q1_geomx_patient_region_profile.tsv")

## ---- gene-level readout for the TWEAK axis ---------------------------------
gene_rows <- lapply(c("exp1", "exp2"), function(e) {
  G <- load_geomx(e); pd <- harmonise_pd(G$pd)
  keep <- pd$region %in% REGION_LEVELS; pd <- pd[keep, ]; m <- G$expr[, keep, drop = FALSE]
  g <- intersect(c("TNFSF12", "TNFRSF12A", "TGFB1", "TGFB3", "IL36G", "LAMC2", "MMP7", "EMP1"),
                 rownames(m))
  lapply(g, function(x) data.frame(exp = e, gene = x, segment_id = colnames(m),
                                   expr = as.numeric(m[x, ]))) %>% bind_rows() %>%
    left_join(pd, by = "segment_id")
}) %>% bind_rows()
write_tsv(gene_rows, "Q1_geomx_tweak_axis_genes.tsv")

gene_stats <- gene_rows %>% group_by(exp, gene, segment) %>%
  group_modify(function(d, k) {
    e <- region_effect(d %>% rename(score = expr))
    if (is.null(e)) return(tibble::tibble())
    tibble::tibble(n_patients = e$n_patients, mean_diff_inv_core = e$mean_diff,
                   n_patients_positive = e$n_pos, p_paired = e$p)
  }) %>% ungroup() %>% group_by(exp, segment) %>%
  mutate(q_BH = p.adjust(p_paired, "BH")) %>% ungroup() %>% arrange(exp, segment, p_paired)
write_tsv(gene_stats, "Q1_geomx_tweak_axis_gene_stats.tsv")

## ---- figures ---------------------------------------------------------------
show <- c("proCSC", "revCSC", "IFA_core", "TRA_core", "EVT_core", "placenta_troph",
          "fetal_Yui", "revival_Ayyaz", "YAP_regeneration", "proliferation")
p1 <- profile %>% filter(signature %in% show) %>%
  mutate(region = factor(region, REGION_LEVELS)) %>%
  ggplot(aes(region, score)) +
  geom_line(aes(group = patient), colour = GREY, alpha = .6) +
  geom_point(aes(colour = region), size = 1.4) +
  scale_colour_manual(values = c(nor = GREY, ade = "#9970AB", core = BLUE, inv = RED),
                      guide = "none") +
  facet_grid(segment + exp ~ signature, scales = "free_y") +
  labs(x = NULL, y = "singscore (patient mean)",
       title = "Regional profile of CSC and developmental signatures, GeoMx early-stage CRC",
       subtitle = "one line per patient; nor -> ade -> core -> inv") +
  theme_bw(base_size = 8)
ggsave(file.path(FIGD, "Q1_region_profiles.pdf"), p1, width = 16, height = 8)

p2 <- stats %>% filter(signature %in% show) %>%
  ggplot(aes(reorder(signature, mean_diff_inv_core), mean_diff_inv_core,
             fill = p_matched_null < 0.05)) +
  geom_col() + coord_flip() + facet_grid(segment ~ exp, scales = "free_x") +
  scale_fill_manual(values = c(`TRUE` = RED, `FALSE` = GREY),
                    name = "passes matched null (P<0.05)") +
  labs(x = NULL, y = "invasive front - tumour core (patient-level mean difference)",
       title = "Invasive-front enrichment against expression-matched random gene sets") +
  theme_bw(base_size = 9)
ggsave(file.path(FIGD, "Q1_inv_vs_core_effects.pdf"), p2, width = 10, height = 6)

cat("\n=== inv vs core, PanCK+ segments ===\n")
print(as.data.frame(stats %>% filter(grepl("\\+", segment) | grepl("PanCK\\+", segment)) %>%
      select(exp, signature, n_patients, mean_diff_inv_core, n_patients_positive,
             p_paired, z_vs_matched_null, p_matched_null)), digits = 3)
cat("\ndone\n")
