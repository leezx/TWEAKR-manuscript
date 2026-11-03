# Shared paths, gene sets and helpers for the Ogden 2025 (Cell Genomics) re-analysis.
#
# Ogden, Metic et al., "Phenotypic heterogeneity and plasticity in colorectal
# cancer metastasis", Cell Genomics 5(7):100881 (2025).
#
# Paths come from the environment so nothing is hard-coded to this workstation
# (Stelligen AGENTS.md rule 5). Defaults match the local mount.

ROOT <- Sys.getenv("STELLIGEN_ROOT", "/Volumes/Stelligen_SSD/Stelligen")
PROJ <- file.path(ROOT, "DATA/2.PROJECTS/1.TWEAKR-oncoFetal")
OGD  <- Sys.getenv("OGDEN_DIR",
  file.path(ROOT, "DATA/HotData/TWEAKR-oncoFetal/ogden2025_crclm_multiome"))
RAW  <- file.path(OGD, "raw")
PROC <- file.path(OGD, "processed")
OUT  <- Sys.getenv("OGDEN_OUT",
  file.path(ROOT, "PR/TWEAKR-manuscript/analyses/2026-11-02_ogden-crclm-tweakr-onf-ifn"))

TAB <- file.path(OUT, "tables"); FIGD <- file.path(OUT, "figures")
for (d in c(TAB, FIGD, PROC)) dir.create(d, showWarnings = FALSE, recursive = TRUE)

SEED <- 20261102

# Project palette, unchanged across the manuscript.
BLUE <- "#2166AC"; RED <- "#B2182B"; GREY <- "#8C8C8C"

RECEPTOR <- "TNFRSF12A"   # TWEAKR
LIGAND   <- "TNFSF12"     # TWEAK

read_gmt <- function(path) {
  ln <- readLines(path, warn = FALSE); ln <- ln[nzchar(ln)]
  out <- lapply(strsplit(ln, "\t"), function(x) unique(x[-c(1, 2)][nzchar(x[-c(1, 2)])]))
  names(out) <- vapply(strsplit(ln, "\t"), `[`, "", 1)
  out
}

write_tsv <- function(x, f) {
  write.table(x, file.path(TAB, f), sep = "\t", quote = FALSE, row.names = FALSE)
  message("  wrote ", f, "  (", nrow(x), " rows)")
}

#' Every gene set used here, in HUMAN symbols.
#'
#' THE CIRCULARITY RULE. TNFRSF12A is itself a member of three frozen sets:
#'   revCSC_human, Noncanonical_NFkB_TNFR2 and STAT3_response.
#' Leaving it in any of them would guarantee a positive correlation with itself.
#' It is therefore dropped from EVERY set here, and the drop is reported, never
#' silent. The same rule is applied to TNFSF12 for symmetry.
#'
#' Two dimensions are kept deliberately separate, because the whole point of
#' this analysis is to ask whether they are separable:
#'   onf_*     oncofetal / regenerative identity
#'   infl_*    interferon and NF-kB inflammatory response
load_signatures <- function(verbose = TRUE) {
  gs <- file.path(PROJ, "genesets")
  rev <- read_gmt(file.path(gs, "revCSC.human.gmt"))
  csc <- read_gmt(file.path(gs, "CSC_subtypes.mouse.gmt"))   # proCSC: mouse only
  sig <- read_gmt(file.path(gs, "MSigDB_signaling.human.gmt"))
  imm <- read_gmt(file.path(gs, "Immune_Cytotoxic.human.gmt"))
  yap_r <- read_gmt(file.path(gs, "YAP_targets_gmt/YAP_regenerative_GSVA.human.gmt"))
  yap_f <- read_gmt(file.path(gs, "YAP_targets_gmt/YAP_fetal_oncofetal_effectors.human.gmt"))

  # proCSC exists only as a mouse set; map it up to human orthologues.
  pro_h <- babelgene::orthologs(genes = csc$proCSC, species = "mouse", human = FALSE)
  pro_h <- unique(pro_h$human_symbol)
  if (verbose)
    message(sprintf("  ortholog map proCSC  %3d mouse -> %3d human",
                    length(csc$proCSC), length(pro_h)))

  # MSigDB hallmark inflammatory axes, and antigen presentation.
  hm <- msigdbr::msigdbr(species = "Homo sapiens", collection = "H")
  hs <- function(n) unique(hm$gene_symbol[hm$gs_name == n])
  cp <- msigdbr::msigdbr(species = "Homo sapiens", collection = "C2",
                         subcollection = "CP:REACTOME")
  ag <- unique(cp$gene_symbol[cp$gs_name ==
         "REACTOME_ANTIGEN_PROCESSING_CROSS_PRESENTATION"])

  sigs <- list(
    # ---- dimension 1: oncofetal / regenerative identity ----
    onf_revCSC        = rev$revCSC_human,
    onf_proCSC        = pro_h,
    onf_YAP_regen     = yap_r[[1]],
    onf_YAP_effectors = yap_f[[1]],
    # ---- dimension 2: inflammatory response ----
    infl_IFNG         = hs("HALLMARK_INTERFERON_GAMMA_RESPONSE"),
    infl_IFNA         = hs("HALLMARK_INTERFERON_ALPHA_RESPONSE"),
    infl_TNFA_NFKB    = hs("HALLMARK_TNFA_SIGNALING_VIA_NFKB"),
    infl_NFKB_canon   = sig$Canonical_NFkB_response,
    infl_NFKB_noncan  = sig$Noncanonical_NFkB_TNFR2,
    infl_antigen_pres = ag,
    # ---- tumour-intrinsic immune programmes (audited in the Mzoughi work) ----
    imm_suppression   = imm$Immune_suppression,
    imm_cytotox_res   = imm$Cytotoxic_resistance
  )

  # Drop the receptor and ligand from every set. Report, never silent.
  drop <- c(RECEPTOR, LIGAND)
  for (n in names(sigs)) {
    hit <- intersect(sigs[[n]], drop)
    if (length(hit)) {
      sigs[[n]] <- setdiff(sigs[[n]], drop)
      if (verbose) message(sprintf("  CIRCULARITY GUARD: removed %s from %s",
                                   paste(hit, collapse = "/"), n))
    }
  }
  if (verbose) for (n in names(sigs))
    message(sprintf("  %-18s %4d genes", n, length(sigs[[n]])))
  sigs
}

#' Partial Spearman correlation of x and y given the columns of Z.
#'
#' Computed as the Pearson correlation of the residuals of the RANKS, which is
#' the standard definition of a partial Spearman coefficient. Returns NA rather
#' than erroring when a vector has no variance (constant covariate, or a gene
#' detected in every cell or in none).
pcor_spearman <- function(x, y, Z = NULL) {
  ok <- is.finite(x) & is.finite(y)
  if (!is.null(Z)) ok <- ok & apply(is.finite(as.matrix(Z)), 1, all)
  x <- x[ok]; y <- y[ok]
  if (length(x) < 20 || sd(x) == 0 || sd(y) == 0) return(NA_real_)
  rx <- rank(x); ry <- rank(y)
  if (is.null(Z) || ncol(as.matrix(Z)) == 0) return(suppressWarnings(cor(rx, ry)))
  Zr <- apply(as.matrix(Z)[ok, , drop = FALSE], 2, rank)
  Zr <- Zr[, apply(Zr, 2, sd) > 0, drop = FALSE]
  if (ncol(Zr) == 0) return(suppressWarnings(cor(rx, ry)))
  ex <- residuals(lm(rx ~ Zr)); ey <- residuals(lm(ry ~ Zr))
  if (sd(ex) == 0 || sd(ey) == 0) return(NA_real_)
  suppressWarnings(cor(ex, ey))
}

#' Genes whose detection rate matches the receptor's, as a null distribution
#' that holds n and sparsity fixed. Restricted to the given universe (e.g. all
#' annotated cell-surface receptors) when one is supplied.
matched_null_genes <- function(det, target, n = 24, tol = 0.02, universe = NULL) {
  cand <- names(det)
  if (!is.null(universe)) cand <- intersect(cand, universe)
  cand <- setdiff(cand, c(RECEPTOR, LIGAND))
  d <- abs(det[cand] - det[[target]])
  keep <- cand[d <= tol]
  if (length(keep) < n) keep <- cand[order(d)][seq_len(min(n, length(cand)))]
  set.seed(SEED)
  if (length(keep) > n) keep <- sample(keep, n)
  sort(keep)
}
