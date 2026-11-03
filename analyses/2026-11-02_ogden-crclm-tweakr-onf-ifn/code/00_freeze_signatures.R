# Freeze the two signature dimensions to a GMT the Python analysis reads.
#
# Owning the gene lists here, in one place, means: the orthologue mapping and
# the MSigDB pull happen once; the exact lists are auditable on disk; and the
# analysis script has no network dependency at run time.
#
# Run:  Rscript code/00_freeze_signatures.R

.here <- local({
  a <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(.here, "common.R"))
set.seed(SEED)

sigs <- load_signatures(verbose = TRUE)

out <- file.path(PROC, "signatures_human.gmt")
con <- file(out, "w")
for (n in names(sigs))
  writeLines(paste(c(n, "ogden2025_tweakr_analysis", sigs[[n]]), collapse = "\t"), con)
close(con)
cat("wrote", out, "with", length(sigs), "sets\n")

# A human-readable record of membership, committed with the analysis.
memb <- do.call(rbind, lapply(names(sigs), function(n)
  data.frame(set = n, n_genes = length(sigs[[n]]),
             genes = paste(sigs[[n]], collapse = ","), row.names = NULL)))
write_tsv(memb, "Q0_signature_membership.tsv")

# The overlap between the two dimensions is reported up front: if the oncofetal
# and inflammatory sets shared most of their genes, no amount of partial
# correlation could separate them, and the whole Gate A question would be void.
onf <- grep("^onf_", names(sigs), value = TRUE)
inf <- grep("^infl_", names(sigs), value = TRUE)
ov <- expand.grid(onf = onf, infl = inf, stringsAsFactors = FALSE)
ov$n_onf <- lengths(sigs[ov$onf]); ov$n_infl <- lengths(sigs[ov$infl])
ov$n_shared <- mapply(function(a, b) length(intersect(sigs[[a]], sigs[[b]])),
                      ov$onf, ov$infl)
ov$jaccard <- mapply(function(a, b)
  length(intersect(sigs[[a]], sigs[[b]])) / length(union(sigs[[a]], sigs[[b]])),
  ov$onf, ov$infl)
ov$shared_genes <- mapply(function(a, b)
  paste(intersect(sigs[[a]], sigs[[b]]), collapse = ","), ov$onf, ov$infl)
write_tsv(ov[order(-ov$jaccard), ], "Q0_dimension_overlap.tsv")

cat("\nmax Jaccard between an oncofetal and an inflammatory set:",
    sprintf("%.3f", max(ov$jaccard)), "\n")
cat("the two dimensions are", ifelse(max(ov$jaccard) < 0.1, "largely disjoint",
                                     "NOT disjoint - interpret with care"), "\n")
