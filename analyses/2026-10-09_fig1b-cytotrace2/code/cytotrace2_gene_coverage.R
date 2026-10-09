#!/usr/bin/env Rscript
# CytoTRACE2 1.1.0 gene-space coverage of the Atlas and of each Fig. 1B study.
#
# Re-implements the human branch of CytoTRACE2:::preprocessData (human symbol -> mouse model gene,
# with alias rescue) so the mapping can be inspected. The model uses a fixed list of training
# features; any feature without a mapped input gene is filled with 0 by CytoTRACE2.
#
# Usage: Rscript cytotrace2_gene_coverage.R <study_gene_detection.tsv.gz> <out_dir>
suppressPackageStartupMessages({ library(CytoTRACE2); library(data.table) })
args <- commandArgs(trailingOnly = TRUE)
det <- fread(args[1])
out <- args[2]

ext <- function(f) system.file("extdata", f, package = "CytoTRACE2")
features <- read.csv(ext("features_model_training_17.csv"), row.names = 1, check.names = FALSE)[[1]]
mt_dict <- fread(ext("mt_dict_human_to_mouse.csv"), header = TRUE, check.names = FALSE)
rescue <- read.csv(ext("mt_human_alias.csv"), header = TRUE, check.names = FALSE)

# Same steps as CytoTRACE2:::preprocessData (species = "human"), 1.1.0.
gene_names <- gsub(".", "-", det$gene, fixed = TRUE)
mapping <- unlist(plyr::mapvalues(gene_names, colnames(mt_dict), mt_dict[1, ], warn_missing = FALSE))
map_df <- data.frame(original_gene = gene_names, mapped_gene = mapping,
                     mapped = ifelse(mapping %in% mt_dict[1, ], "1", "0"))
mapped_genes <- map_df[map_df$mapped == 1, ]$original_gene
unmapped_genes <- map_df[map_df$mapped == 0, ]$original_gene
is_alias <- intersect(unmapped_genes, rescue$alias)
original_to_alias <- rescue[rescue$alias %in% is_alias, ]$hsgene
mapped_original_to_alias <- intersect(original_to_alias, mapped_genes)
alias_to_unmapped_original <- rescue[rescue$hsgene %in% setdiff(original_to_alias, mapped_original_to_alias), ]$alias
rownames(rescue) <- rescue$alias
unmapped_original_with_alias <- map_df[map_df$original_gene %in% alias_to_unmapped_original, ]$mapped_gene
map_df[map_df$original_gene %in% alias_to_unmapped_original, ]$mapped_gene <- rescue[unmapped_original_with_alias, ]$mmgene
map_df$model_feature <- map_df$mapped_gene %in% features

studies <- setdiff(colnames(det), c("gene", "ensembl"))
in_model <- map_df$model_feature
dup_targets <- names(which(table(map_df$mapped_gene[in_model]) > 1))
rows <- lapply(studies, function(s) {
  detected <- det[[s]] > 0
  data.frame(study = s,
             atlas_genes_detected = sum(detected),
             model_features = length(features),
             model_features_with_detected_gene = length(unique(map_df$mapped_gene[in_model & detected])),
             pct_model_features_covered = round(100 * length(unique(map_df$mapped_gene[in_model & detected])) / length(features), 2))
})
cov <- do.call(rbind, rows)
cov <- rbind(data.frame(study = "ATLAS_ALL_GENES", atlas_genes_detected = nrow(det), model_features = length(features),
                        model_features_with_detected_gene = length(unique(map_df$mapped_gene[in_model])),
                        pct_model_features_covered = round(100 * length(unique(map_df$mapped_gene[in_model])) / length(features), 2)),
             cov)
fwrite(cov, file.path(out, "cytotrace2_model_gene_coverage_by_study.csv"))
fwrite(map_df, file.path(out, "cytotrace2_atlas_gene_mapping.tsv.gz"), sep = "\t")
cat("model features:", length(features), "\n")
cat("model features hit by >1 Atlas gene:", length(dup_targets), "\n")
print(cov)
