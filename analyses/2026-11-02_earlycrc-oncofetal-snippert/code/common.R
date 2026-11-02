# Shared paths and gene sets for the early-CRC (Snippert 2026) re-analysis.
# Paths come from the environment so the scripts are portable; the defaults match this workstation.

ROOT     <- Sys.getenv("STELLIGEN_ROOT", "/Volumes/Stelligen_SSD/Stelligen")
PROJ     <- file.path(ROOT, "DATA/2.PROJECTS/1.TWEAKR-oncoFetal")
EARLYCRC <- Sys.getenv("EARLYCRC_DIR",
  file.path(PROJ, "data/external/Perturbation/Nature2026_oncofetal_EGAD50000002202"))
ZENODO   <- Sys.getenv("EARLYCRC_ZENODO_DIR",
  file.path(ROOT, "DATA/HotData/TWEAKR-oncoFetal/zenodo_17671259_earlyCRC_oncofetal"))
OUT      <- Sys.getenv("EARLYCRC_OUT",
  file.path(ROOT, "PR/TWEAKR-manuscript/analyses/2026-11-02_earlycrc-oncofetal-snippert"))

TAB <- file.path(OUT, "tables"); FIGD <- file.path(OUT, "figures")
dir.create(TAB, showWarnings = FALSE, recursive = TRUE)
dir.create(FIGD, showWarnings = FALSE, recursive = TRUE)

# Fixed project palette (blue = low/proliferative, red = high/revival, grey = control)
BLUE <- "#2166AC"; RED <- "#B2182B"; GREY <- "#8C8C8C"

read_gmt <- function(path) {
  ln <- readLines(path, warn = FALSE)
  ln <- ln[nzchar(ln)]
  out <- lapply(strsplit(ln, "\t"), function(x) unique(x[-c(1, 2)][nzchar(x[-c(1, 2)])]))
  names(out) <- vapply(strsplit(ln, "\t"), `[`, "", 1)
  out
}

#' The frozen signature panel used throughout this analysis.
#' proCSC/revCSC are the project's human Qin-2023 sets; IFA/TRA/EVT are the frozen
#' cancer-naive developmental axes; placenta_trophoblast is the curated trophoblast set.
load_signatures <- function() {
  g1 <- read_gmt(file.path(PROJ, "results/tables/Figure1F_program_annotation",
                           "Figure1F_candidate_human_genesets.v0.3.gmt"))
  g2 <- read_gmt(file.path(PROJ, "results/2026-10-07_placenta_axes_v0.1/IFA_core_FINAL.gmt"))
  g3 <- read_gmt(file.path(PROJ, "results/2026-10-07_placenta_axes_v0.1/TRA_core_FINAL.gmt"))
  g4 <- read_gmt(file.path(PROJ, "genesets/placenta_trophoblast.filtered.gmt"))
  list(
    proCSC            = g1$Qin_2023_proCSC,
    revCSC            = g1$Qin_2023_revCSC,
    Lgr5CSC           = g1$Qin_2023_Lgr5CSC,
    fetal_Yui         = g1$Yui_2018_fetal_intestine,
    revival_Ayyaz     = g1$Ayyaz_2019_revival_stem,
    YAP_regeneration  = g1$Gregorieff_2015_YAP_regeneration,
    proliferation     = g1$MerlosSuarez_2011_proliferation,
    IFA_core          = g2$IFA_core,
    TRA_core          = g3$TRA_core,
    EVT_core          = g3$EVT_core,
    placenta_troph    = g4$placenta_trophoblast_filtered
  )
}

GENES_OF_INTEREST <- c("TNFSF12", "TNFRSF12A", "TGFB1", "TGFB3", "IL36G",
                       "LAMC2", "EMP1", "MMP7", "ANXA1")

write_tsv <- function(x, name) {
  utils::write.table(x, file.path(TAB, name), sep = "\t", quote = FALSE, row.names = FALSE)
  invisible(file.path(TAB, name))
}
