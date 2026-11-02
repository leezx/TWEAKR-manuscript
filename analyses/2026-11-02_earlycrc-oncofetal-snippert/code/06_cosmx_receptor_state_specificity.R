# P0 (review priority): is TNFRSF12A specific to the oncofetal cell STATE, or is
# it just an invasive-front marker?
#
# EC2 showed TNFRSF12A rising at the invasive front of bulk epithelial segments
# in 10/10 patients. That is a regional result. It is equally compatible with the
# receptor being raised in every invasive epithelial state, oncofetal or not.
# The cell-state claim requires a within-tumour, within-region comparison.
#
# Design, following the review:
#   - malignant epithelium only (authors' CRC + oncofetal labels); normal and
#     undefined epithelium excluded
#   - oncofetal defined by the ORIGINAL AUTHORS' label, which derives from the
#     published HRC signature and not from any gene set of ours. This matters:
#     TNFRSF12A is itself a member of our revCSC set, so defining the state with
#     revCSC and then testing the receptor would be circular. A revCSC-decile
#     sensitivity arm is run with TNFRSF12A removed from the set.
#   - comparison is stratified by field of view AND by transcript-detection
#     quintile, so an oncofetal cell is only ever compared with malignant cells
#     imaged in the same field at a similar sequencing depth
#   - twelve detection-matched non-ligand control genes are carried through the
#     identical pipeline, so the receptor's effect is read against what an
#     arbitrary gene of the same detection rate produces
#   - the patient is the unit: strata are aggregated within patient, then tested
#     across patients
#
# Reports detection-rate difference, log-expression difference and Cliff's delta.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(Matrix); library(dplyr); library(tidyr); library(ggplot2)})
set.seed(20261102)

N_QUINTILE <- 5
MIN_STRATUM <- 10      # cells of each class needed for a stratum to contribute

D <- readRDS(file.path(ZENODO, "cosmx_exp2_compact.rds"))
C <- readRDS(file.path(ZENODO, "cosmx_exp2_control_genes.rds"))
SIGS <- load_signatures()

md <- D$meta
md$patient  <- as.character(md$patient_ID)
md$fov      <- as.character(md$fov)
md$celltype <- as.character(md$cellType)
md$stage    <- as.character(md$tumorStage)
md$depth    <- as.numeric(md$nCount_RNA)
md$is_malig <- md$celltype %in% c("CRC", "oncofetal")
md$onf_authors <- md$celltype == "oncofetal"

# revCSC score WITHOUT TNFRSF12A, for the sensitivity definition
cpm <- Matrix::t(Matrix::t(D$counts) / pmax(D$total, 1)) * 1e4
g_rev <- setdiff(intersect(SIGS$revCSC, rownames(cpm)), "TNFRSF12A")
md$revCSC_noRec <- Matrix::colMeans(log1p(cpm)[g_rev, , drop = FALSE])
cat(sprintf("revCSC genes used for the sensitivity definition (TNFRSF12A removed): %d\n",
            length(g_rev)))
md <- md %>% group_by(patient) %>%
  mutate(onf_revCSC = is_malig &
           revCSC_noRec >= quantile(revCSC_noRec[is_malig], 0.90, na.rm = TRUE)) %>% ungroup()

GENES <- c("TNFRSF12A", "TNFSF12", setdiff(rownames(C$counts), c("TNFSF12")))
GENES <- intersect(GENES, c(rownames(D$counts), rownames(C$counts)))
getg <- function(g) if (g %in% rownames(D$counts)) as.numeric(D$counts[g, ]) else
                    as.numeric(C$counts[g, colnames(D$counts)])
KIND <- ifelse(GENES == "TNFRSF12A", "receptor",
        ifelse(GENES %in% c("TNFSF12", "TGFB1", "TGFB3", "IL36G"), "ligand", "control"))
names(KIND) <- GENES
cat(sprintf("genes tested: %d (%d control)\n", length(GENES), sum(KIND == "control")))

cliffs <- function(a, b) {   # delta on the raw counts, robust to the zero inflation
  if (!length(a) || !length(b)) return(NA_real_)
  r <- rank(c(a, b)); n1 <- length(a); n2 <- length(b)
  (2 * (sum(r[seq_len(n1)]) - n1 * (n1 + 1) / 2) / (n1 * n2)) - 1
}

#' Stratified comparison inside one patient.
#' Strata are field of view x detection quintile; each stratum contributes the
#' oncofetal-minus-other difference, weighted by its oncofetal cell count.
strat_patient <- function(dp, cnt, tot, onf) {
  dp$q <- ave(dp$depth, dp$fov, FUN = function(x)
    as.integer(cut(rank(x, ties.method = "first"),
                   breaks = N_QUINTILE, labels = FALSE)))
  key <- paste(dp$fov, dp$q)
  lg <- log1p(cnt / pmax(tot, 1) * 1e4)
  pos <- cnt > 0
  rows <- lapply(split(seq_len(nrow(dp)), key), function(ix) {
    a <- ix[onf[ix]]; b <- ix[!onf[ix]]
    if (length(a) < MIN_STRATUM || length(b) < MIN_STRATUM) return(NULL)
    data.frame(n_onf = length(a), n_other = length(b),
               d_det = mean(pos[a]) - mean(pos[b]),
               d_log = mean(lg[a]) - mean(lg[b]),
               delta = cliffs(cnt[a], cnt[b]),
               depth_ratio = mean(dp$depth[a]) / mean(dp$depth[b]))
  })
  rows <- bind_rows(rows)
  if (!nrow(rows)) return(NULL)
  w <- rows$n_onf / sum(rows$n_onf)
  data.frame(n_strata = nrow(rows), n_onf = sum(rows$n_onf), n_other = sum(rows$n_other),
             d_det = sum(w * rows$d_det), d_log = sum(w * rows$d_log),
             delta = sum(w * rows$delta), depth_ratio = sum(w * rows$depth_ratio))
}

res <- list()
for (defn in c("onf_authors", "onf_revCSC")) {
  for (p in unique(md$patient)) {
    k <- which(md$patient == p & md$is_malig)
    onf <- md[[defn]][k]
    if (sum(onf) < 50 || sum(!onf) < 50) next
    dp <- data.frame(fov = md$fov[k], depth = md$depth[k])
    tot <- D$total[k]
    for (g in GENES) {
      r <- strat_patient(dp, getg(g)[k], tot, onf)
      if (is.null(r)) next
      res[[length(res) + 1]] <- cbind(
        data.frame(definition = defn, patient = p, stage = md$stage[k][1],
                   gene = g, kind = KIND[[g]]), r)
    }
  }
  cat(".", sep = "")
}
cat("\n")
res <- bind_rows(res)
write_tsv(res, "Q6_receptor_state_specificity_per_patient.tsv")

## patient-level tests, per gene
summ <- res %>% group_by(definition, gene, kind) %>%
  summarise(n_patients = n(), n_pos = sum(d_log > 0),
            median_d_det_pp = 100 * median(d_det), median_d_log = median(d_log),
            median_delta = median(delta), median_depth_ratio = median(depth_ratio),
            p_wilcox = suppressWarnings(wilcox.test(d_log)$p.value),
            p_sign = suppressWarnings(binom.test(sum(d_log > 0), n(), 0.5)$p.value),
            .groups = "drop") %>%
  group_by(definition) %>% mutate(q_BH = p.adjust(p_wilcox, "BH")) %>% ungroup() %>%
  arrange(definition, desc(median_d_log))
write_tsv(summ, "Q6_receptor_state_specificity_summary.tsv")

## is the receptor outside the control-gene distribution?
calib <- res %>% group_by(definition, patient) %>%
  summarise(rec = d_log[gene == "TNFRSF12A"][1],
            ctrl_mean = mean(d_log[kind == "control"]),
            ctrl_sd = sd(d_log[kind == "control"]),
            n_ctrl_exceeding = sum(d_log[kind == "control"] >= d_log[gene == "TNFRSF12A"][1]),
            n_ctrl = sum(kind == "control"), .groups = "drop") %>%
  mutate(z_vs_controls = (rec - ctrl_mean) / ctrl_sd)
write_tsv(calib, "Q6_receptor_vs_control_genes.tsv")

cat("\n=== TNFRSF12A and the ligands, authors' oncofetal label ===\n")
print(as.data.frame(summ %>% filter(definition == "onf_authors", kind != "control")), digits = 3)
cat("\n=== control-gene distribution, authors' label ===\n")
print(as.data.frame(summ %>% filter(definition == "onf_authors", kind == "control") %>%
        summarise(n = n(), median_of_medians = median(median_d_log),
                  max = max(median_d_log), n_sig = sum(q_BH < 0.05))), digits = 3)
cat("\n=== receptor vs its own control distribution, per patient ===\n")
print(as.data.frame(calib %>% filter(definition == "onf_authors")), digits = 3)
cat("\n=== sensitivity: revCSC decile (TNFRSF12A removed from the set) ===\n")
print(as.data.frame(summ %>% filter(definition == "onf_revCSC", kind != "control")), digits = 3)
cat("\ndone\n")
