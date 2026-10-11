#!/usr/bin/env Rscript
# A3a CCAT (secondary proxy, frozen contract v0.2 §3): SCENT 1.0.3 CompCCAT on the same main epithelial
# counts used for UCell. Implementation mirrors the DS-010 CSCPOT run: conservative one-to-one
# SYMBOL->ENTREZ mapping (ambiguous symbols and duplicated Entrez dropped), library-size normalisation to
# 10,000, log2(x+1), official net13Jun12 network, >=5,000 overlapping genes required.
# Usage: Rscript a3a_ccat.R <counts_dir> <sample_tag> <out.tsv.gz> [repeat]
#   repeat: if "repeat", CompCCAT is run twice and must give identical values (technical pilot only)
suppressPackageStartupMessages({ library(SCENT); library(AnnotationDbi); library(org.Hs.eg.db)
  library(hdf5r); library(Matrix); library(data.table) })
args <- commandArgs(trailingOnly = TRUE)
counts_dir <- args[1]; tag <- args[2]; out <- args[3]; rep_run <- length(args) >= 4 && args[4] == "repeat"
p <- file.path(counts_dir, sprintf("%s.main.h5", tag))
h <- H5File$new(p, mode = "r")
shape <- h[["shape"]]$read()
m <- sparseMatrix(i = h[["indices"]]$read() + 1L, p = h[["indptr"]]$read(), x = as.numeric(h[["data"]]$read()),
                  dims = shape, dimnames = list(h[["genes"]]$read(), h[["cells"]]$read()))
h$close_all()
if (ncol(m) < 50) {  # ineligible under §1; header-only output
  con <- gzfile(out, "w"); writeLines("cell_id\tCCAT", con); close(con); quit(save = "no")
}
t0 <- Sys.time()
lib <- Matrix::colSums(m); stopifnot(all(lib > 0))
sym <- toupper(rownames(m)); stopifnot(!anyDuplicated(sym)); rownames(m) <- sym
map <- AnnotationDbi::select(org.Hs.eg.db, keys = intersect(sym, keys(org.Hs.eg.db, keytype = "SYMBOL")),
                             keytype = "SYMBOL", columns = "ENTREZID")
map <- unique(map[!is.na(map$ENTREZID), ])
map <- map[!duplicated(map$SYMBOL) & !duplicated(map$SYMBOL, fromLast = TRUE), ]
map <- map[!duplicated(map$ENTREZID) & !duplicated(map$ENTREZID, fromLast = TRUE), ]
norm <- m[match(map$SYMBOL, rownames(m)), , drop = FALSE] %*% Diagonal(x = 1e4 / lib)
norm@x <- log2(norm@x + 1); rownames(norm) <- map$ENTREZID
data(net13Jun12, package = "SCENT")
overlap <- length(intersect(rownames(norm), rownames(net13Jun12.m)))
stopifnot(overlap >= 5000)
ccat <- CompCCAT(exp.m = norm, ppiA.m = net13Jun12.m)
stopifnot(length(ccat) == ncol(m), all(is.finite(ccat)), all(abs(ccat) <= 1))
identical_repeat <- NA
if (rep_run) identical_repeat <- identical(ccat, CompCCAT(exp.m = norm, ppiA.m = net13Jun12.m))
fwrite(data.table(cell_id = colnames(m), CCAT = ccat), out, sep = "\t")
cat(sprintf("%s cells=%d mapped_genes=%d ppi_overlap=%d repeat_identical=%s sec=%.0f\n", tag, ncol(m), nrow(map),
            overlap, identical_repeat, as.numeric(Sys.time() - t0, units = "secs")))
