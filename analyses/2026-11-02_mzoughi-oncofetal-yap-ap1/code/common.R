# Shared paths, gene sets and helpers for the Mzoughi 2025 (Nat Genet) re-analysis.
#
# Paths come from the environment so nothing is hard-coded to this workstation
# (Stelligen AGENTS.md rule 5). Defaults match the local mount.

ROOT   <- Sys.getenv("STELLIGEN_ROOT", "/Volumes/Stelligen_SSD/Stelligen")
PROJ   <- file.path(ROOT, "DATA/2.PROJECTS/1.TWEAKR-oncoFetal")
GEO    <- Sys.getenv("MZOUGHI_DIR",
  file.path(ROOT, "DATA/HotData/TWEAKR-oncoFetal/geo_GSE237954_mzoughi_oncofetal"))
RAW    <- file.path(GEO, "raw")
PROC   <- file.path(GEO, "processed")
SUPPL  <- file.path(PROC, "suppl_tables")
OUT    <- Sys.getenv("MZOUGHI_OUT",
  file.path(ROOT, "PR/TWEAKR-manuscript/analyses/2026-11-02_mzoughi-oncofetal-yap-ap1"))

TAB <- file.path(OUT, "tables"); FIGD <- file.path(OUT, "figures")
dir.create(TAB, showWarnings = FALSE, recursive = TRUE)
dir.create(FIGD, showWarnings = FALSE, recursive = TRUE)
dir.create(PROC, showWarnings = FALSE, recursive = TRUE)

SEED <- 20261102

# Project palette, unchanged across the manuscript.
BLUE <- "#2166AC"; RED <- "#B2182B"; GREY <- "#8C8C8C"

RECEPTOR <- "Tnfrsf12a"   # TWEAKR
LIGAND   <- "Tnfsf12"     # TWEAK

read_gmt <- function(path) {
  ln <- readLines(path, warn = FALSE); ln <- ln[nzchar(ln)]
  out <- lapply(strsplit(ln, "\t"), function(x) unique(x[-c(1, 2)][nzchar(x[-c(1, 2)])]))
  names(out) <- vapply(strsplit(ln, "\t"), `[`, "", 1)
  out
}

#' Human -> mouse symbols via babelgene's curated orthologue table.
#' One-to-many orthologues are all kept; genes without an orthologue are dropped
#' and the loss is reported by `load_signatures()` so it is never silent.
to_mouse <- function(symbols) {
  o <- babelgene::orthologs(genes = symbols, species = "mouse", human = TRUE)
  unique(o$symbol)
}

#' Every gene set used here, in mouse symbols.
#'
#' Three provenances, deliberately kept separate:
#'   paper_*    the authors' own definitions (Supplementary Table 1d, 1g). Using
#'              these is what makes the TWEAKR result non-circular: the oncofetal
#'              state is defined by them, not by us.
#'   project_*  the TWEAKR manuscript's frozen mouse sets.
#'   mapped_*   the manuscript's human sets mapped to mouse orthologues.
load_signatures <- function(verbose = TRUE) {
  s1d <- read.delim(file.path(SUPPL, "Table_S1d.tsv"), header = FALSE,
                    stringsAsFactors = FALSE)[-c(1, 2), , drop = FALSE]
  s1g <- read.delim(file.path(SUPPL, "Table_S1g.tsv"), stringsAsFactors = FALSE)
  nz  <- function(x) unique(x[nzchar(x) & !is.na(x)])
  lk  <- function(k) nz(s1g$gene_name[s1g$marker_type == k])

  csc <- read_gmt(file.path(PROJ, "genesets/CSC_subtypes.mouse.gmt"))
  imm <- read_gmt(file.path(PROJ, "genesets/Immune_Cytotoxic.mouse.gmt"))
  yap <- read_gmt(file.path(PROJ, "genesets/YAP_targets_gmt/YAP_regenerative_GSVA.mouse.gmt"))
  yfe <- read_gmt(file.path(PROJ, "genesets/YAP_targets_gmt/YAP_fetal_oncofetal_effectors.mouse.gmt"))
  pla <- read_gmt(file.path(PROJ, "genesets/placenta_trophoblast.filtered.gmt"))
  ifa <- read_gmt(file.path(PROJ, "results/2026-10-07_placenta_axes_v0.1/IFA_core_FINAL.gmt"))
  tra <- read_gmt(file.path(PROJ, "results/2026-10-07_placenta_axes_v0.1/TRA_core_FINAL.gmt"))

  hs <- list(placenta_troph = pla$placenta_trophoblast_filtered,
             IFA_core = ifa$IFA_core, TRA_core = tra$TRA_core, EVT_core = tra$EVT_core)
  ms <- lapply(hs, to_mouse)
  if (verbose) for (n in names(hs))
    message(sprintf("  ortholog map %-16s %3d human -> %3d mouse", n, length(hs[[n]]), length(ms[[n]])))

  sigs <- list(
    paper_mOnF            = nz(s1d[[1]]),
    paper_mStem           = nz(s1d[[2]]),
    paper_esophagus       = lk("lkts_esophagus_mucosa"),
    paper_colon           = lk("lkts_colon_transverse"),
    paper_small_intestine = lk("lkts_small_intestine"),
    paper_stomach         = lk("lkts_stomach"),
    project_proCSC        = csc$proCSC,
    project_revCSC        = csc$revCSC,
    project_Lgr5CSC       = csc$Lgr5CSC,
    project_YAP_regen     = yap[[1]],
    project_YAP_effectors = yfe[[1]],
    project_Immune_suppression   = imm$Immune_suppression,
    project_Cytotoxic_resistance = imm$Cytotoxic_resistance,
    mapped_placenta_troph = ms$placenta_troph,
    mapped_IFA_core       = ms$IFA_core,
    mapped_TRA_core       = ms$TRA_core,
    mapped_EVT_core       = ms$EVT_core)
  lapply(sigs, function(x) unique(x[nzchar(x) & !is.na(x)]))
}

#' mm10 gene models from the UCSC refGene dump, collapsed to one span per symbol.
load_mm10_genes <- function() {
  f <- file.path(RAW, "annotation/mm10_refGene.txt.gz")
  r <- read.delim(gzfile(f), header = FALSE, stringsAsFactors = FALSE)
  r <- r[, c(3, 4, 5, 6, 13)]
  names(r) <- c("chr", "strand", "start", "end", "symbol")
  r <- r[grepl("^chr[0-9XY]+$", r$chr), ]
  g <- do.call(rbind, lapply(split(r, r$symbol), function(d) {
    d <- d[d$chr == names(sort(table(d$chr), decreasing = TRUE))[1], ]
    data.frame(symbol = d$symbol[1], chr = d$chr[1], strand = d$strand[1],
               start = min(d$start), end = max(d$end), stringsAsFactors = FALSE)
  }))
  g$tss <- ifelse(g$strand == "+", g$start, g$end)
  rownames(g) <- NULL
  g
}

write_tsv <- function(x, name) {
  utils::write.table(x, file.path(TAB, name), sep = "\t", quote = FALSE, row.names = FALSE)
  invisible(file.path(TAB, name))
}

#' Draw `n` random gene sets matched to `genes` on size and expression decile.
#'
#' This is the project convention for every signature claim: a set of the same
#' size drawn from the same expression range is the only honest reference for
#' "this programme moved", because highly expressed genes drift together.
matched_null_sets <- function(genes, universe_expr, n = 200, seed = SEED) {
  set.seed(seed)
  universe_expr <- universe_expr[is.finite(universe_expr)]
  dec <- cut(rank(universe_expr, ties.method = "first"),
             breaks = quantile(rank(universe_expr, ties.method = "first"),
                               probs = seq(0, 1, .1)),
             include.lowest = TRUE, labels = FALSE)
  names(dec) <- names(universe_expr)
  g <- intersect(genes, names(dec))
  if (!length(g)) return(list())
  want <- table(dec[g])
  pool <- split(setdiff(names(dec), g), dec[setdiff(names(dec), g)])
  lapply(seq_len(n), function(i)
    unlist(lapply(names(want), function(d) {
      p <- pool[[d]]
      if (is.null(p)) character(0) else sample(p, min(want[[d]], length(p)))
    }), use.names = FALSE))
}
