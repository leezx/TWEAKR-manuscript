# Q1, continued: the user's question is whether the signatures are enriched in
# *some* region, not only at the invasive front. This reads the patient x region
# score profile written by 01 and tests each region against the rest.
#
# Caveat carried into the write-up: these region-vs-rest tests are NOT calibrated
# against expression-matched random gene sets (script 01 does that for the single
# pre-specified inv-vs-core contrast). They are descriptive and BH-corrected only.

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
suppressMessages({library(dplyr); library(tidyr); library(ggplot2)})

prof <- read.delim(file.path(TAB, "Q1_geomx_patient_region_profile.tsv"))
REGS <- c("nor", "ade", "core", "inv")

## one region vs the mean of the others, paired within patient
res <- prof %>% group_by(exp, segment, signature) %>% group_modify(function(d, k) {
  w <- d %>% select(patient, region, score) %>%
    pivot_wider(names_from = region, values_from = score)
  lapply(intersect(REGS, names(w)), function(r) {
    others <- setdiff(intersect(REGS, names(w)), r)
    ok <- complete.cases(w[, c(r, others), drop = FALSE])
    if (sum(ok) < 4) return(NULL)
    d1 <- w[[r]][ok] - rowMeans(as.matrix(w[ok, others, drop = FALSE]))
    tt <- suppressWarnings(wilcox.test(d1))
    data.frame(region = r, n_patients = sum(ok), mean_diff_vs_rest = mean(d1),
               n_patients_positive = sum(d1 > 0), p = tt$p.value)
  }) %>% bind_rows()
}) %>% ungroup() %>%
  group_by(exp, segment) %>% mutate(q_BH = p.adjust(p, "BH")) %>% ungroup() %>%
  arrange(exp, segment, p)
write_tsv(res, "Q1b_region_vs_rest.tsv")

## Friedman test: does the signature vary across the four regions at all?
fr <- prof %>% group_by(exp, segment, signature) %>% group_modify(function(d, k) {
  w <- d %>% select(patient, region, score) %>%
    pivot_wider(names_from = region, values_from = score)
  cols <- intersect(REGS, names(w)); w <- w[complete.cases(w[, cols]), ]
  if (nrow(w) < 4 || length(cols) < 3) return(tibble::tibble())
  ft <- stats::friedman.test(as.matrix(w[, cols]))
  tibble::tibble(n_patients = nrow(w), n_regions = length(cols),
                 chisq = unname(ft$statistic), p = ft$p.value,
                 top_region = cols[which.max(colMeans(w[, cols]))])
}) %>% ungroup() %>% group_by(exp, segment) %>%
  mutate(q_BH = p.adjust(p, "BH")) %>% ungroup() %>% arrange(exp, segment, p)
write_tsv(fr, "Q1b_friedman_across_regions.tsv")

cat("\n=== PanCK+ : which region does each signature peak in? ===\n")
print(as.data.frame(fr %>% filter(segment == "PanCK+") %>%
  select(exp, signature, n_patients, chisq, p, q_BH, top_region)), digits = 3)

cat("\n=== PanCK+ : invasive front vs the other three regions ===\n")
print(as.data.frame(res %>% filter(segment == "PanCK+", region == "inv") %>%
  select(exp, signature, n_patients, mean_diff_vs_rest, n_patients_positive, p, q_BH)), digits = 3)

p <- res %>% filter(segment == "PanCK+") %>%
  mutate(region = factor(region, REGS)) %>%
  ggplot(aes(region, reorder(signature, mean_diff_vs_rest), fill = mean_diff_vs_rest)) +
  geom_tile() +
  geom_text(aes(label = ifelse(q_BH < 0.05, "*", "")), colour = "white", size = 4, vjust = .75) +
  scale_fill_gradient2(low = BLUE, mid = "white", high = RED, midpoint = 0,
                       name = "score vs\nother regions") +
  facet_wrap(~exp) +
  labs(x = NULL, y = NULL, title = "Where is each signature enriched? Tumour epithelium (PanCK+)",
       subtitle = "patient-paired difference vs the mean of the other regions; * BH q < 0.05") +
  theme_bw(base_size = 9)
ggsave(file.path(FIGD, "Q1b_region_heatmap.pdf"), p, width = 9, height = 4.5)
cat("\ndone\n")
