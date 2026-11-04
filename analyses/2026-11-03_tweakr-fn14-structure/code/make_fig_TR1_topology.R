#!/usr/bin/env Rscript
# Fig. TR1 — TWEAKR / Fn14 (TNFRSF12A) membrane topology reference
#
# Coordinates are UniProt Q9NP84 (human), retrieved and verified 2026-11-03.
# Mouse Q9CR75 has IDENTICAL boundaries (28-80 / 81-101 / 102-129) and
# identical disulfide positions.
#
# Nothing here is fitted or inferred. Every number is a UniProt annotation,
# and every segment string is taken from the sequence by substr() rather
# than typed in, so a wrong boundary cannot silently produce a right-looking
# label.
#
# This is a TOPOLOGY CARTOON, not a structure rendering. The membrane plane
# is a drawn reference; it is not derived from any model. For the ECD fold,
# cite PDB 2KMZ (hFn14, solution NMR). Do NOT use the AlphaFold full-length
# model to define the membrane plane or the ECD-to-tail geometry: AF-Q9NP84-F1
# has a global pLDDT of only 73.19 and the tail is necessarily low-confidence.
#
# Run from this directory:  Rscript make_fig_TR1_topology.R

suppressPackageStartupMessages({
  library(ggplot2)
  library(ggforce)
  library(patchwork)
})

outdir <- "../figures"
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

## ------------------------------------------------------------------ 1. data
# UniProt Q9NP84 (TNFRSF12A_HUMAN), canonical isoform 1, 129 aa.
seq_h <- paste0(
  "MARGSLRRLLRLLVLGLWLALLRSVAGEQAPGTAPCSRGSSWSADLDKCM",
  "DCASCRARPHSDFCLGCAAAPPAPFRLLWPILGGALSLTFVLGLLSGFLV",
  "WRRCRRREKFTTPIEETGGEGCPAVALIQ")

aa <- function(i) substr(seq_h, i, i)

## --- provenance self-checks: fail loudly rather than draw a wrong figure ---
stopifnot(nchar(seq_h) == 129L)
# boundary residues, so an off-by-one in the pasted sequence cannot pass
stopifnot(aa(27)  == "G", aa(28)  == "E")   # signal peptide | ECD
stopifnot(aa(80)  == "P", aa(81)  == "I")   # ECD | TM
stopifnot(aa(101) == "W", aa(102) == "R")   # TM  | cytoplasmic
stopifnot(aa(129) == "Q")                   # C-terminus
# the four published mutagenesis / binding residues (precursor numbering)
stopifnot(aa(45) == "D", aa(48) == "K", aa(50) == "M", aa(62) == "D")
# the six CRD cysteines that form the three disulfides
stopifnot(identical(which(strsplit(substr(seq_h, 36, 67), "")[[1]] == "C") + 35L,
                    c(36L, 49L, 52L, 55L, 64L, 67L)))

ann <- data.frame(
  feature = c("Signal peptide (cleaved)",
              "Extracellular N-segment",
              "CRD (TNFR-Cys, atypical)",
              "Extracellular stalk",
              "Transmembrane helix",
              "Juxtamembrane basic cluster",
              "Cytoplasmic tail (TRAF region)"),
  start   = c(  1,  28,  36,  68,  81, 102, 110),
  end     = c( 27,  35,  67,  80, 101, 109, 129),
  stringsAsFactors = FALSE
)
ann$len <- ann$end - ann$start + 1L
ann$seq <- mapply(function(s, e) substr(seq_h, s, e), ann$start, ann$end)

# arithmetic checks against UniProt's own TOPO_DOM / TRANSMEM lengths
stopifnot(sum(ann$len[ann$start >= 28]) == 102L)             # mature chain
stopifnot(sum(ann$len[ann$feature %in%
  c("Extracellular N-segment", "CRD (TNFR-Cys, atypical)",
    "Extracellular stalk")]) == 53L)                          # ECD
stopifnot(ann$len[ann$feature == "Transmembrane helix"] == 21L)
stopifnot(sum(ann$len[ann$start >= 102]) == 28L)              # ICD

pal <- c(
  "Signal peptide (cleaved)"       = "#B3B3B3",
  "Extracellular N-segment"        = "#A6CEE3",
  "CRD (TNFR-Cys, atypical)"       = "#1F78B4",
  "Extracellular stalk"            = "#7BA7C7",
  "Transmembrane helix"            = "#E6550D",
  "Juxtamembrane basic cluster"    = "#6A51A3",
  "Cytoplasmic tail (TRAF region)" = "#31A354")
ss_col <- "#F2C300"   # disulfide

## -------------------------------------------------------- 2. geometry setup
# Membrane: outer face y = 0, inner face y = -1. One y-unit = 31.5 A, i.e.
# the 21-residue TM helix at 1.5 A rise per residue.
y_out <- 0; y_in <- -1

xs <- seq(-1.85, 1.85, by = 0.105)
# Must match the TM backing rect below (+/-0.135), otherwise the strip
# between the two is neither lipid nor helix and renders as a gap in the
# membrane.
xs <- xs[abs(xs) > 0.135]
lip_out <- data.frame(x0 = xs, y0 = y_out - 0.075, r = 0.052)
lip_in  <- data.frame(x0 = xs, y0 = y_in  + 0.075, r = 0.052)
tails <- rbind(
  data.frame(x = xs - 0.02, xend = xs - 0.02, y = y_out - 0.12, yend = -0.46),
  data.frame(x = xs + 0.02, xend = xs + 0.02, y = y_out - 0.12, yend = -0.46),
  data.frame(x = xs - 0.02, xend = xs - 0.02, y = y_in  + 0.12, yend = -0.54),
  data.frame(x = xs + 0.02, xend = xs + 0.02, y = y_in  + 0.12, yend = -0.54))

# TM helix: 21 aa / 3.6 aa per turn = 5.83 turns
t  <- seq(0, 1, length.out = 600)
tm <- data.frame(x = 0.085 * sin(2 * pi * 5.83 * t), y = y_out - t)

stalk <- data.frame(x = c(0, 0.0, 0.02), y = c(y_out, 0.30, 0.52))
crd   <- data.frame(x0 = 0.02, y0 = 1.12, a = 0.46, b = 0.56, angle = 0)
nseg  <- data.frame(x = c(-0.22, -0.42, -0.60), y = c(1.60, 1.80, 1.92))

basic <- data.frame(x = c(0, 0.06, 0.16), y = c(y_in, -1.16, -1.30))
dtail <- data.frame(x = c(0.16, 0.34, 0.20, 0.40, 0.30),
                    y = c(-1.30, -1.46, -1.62, -1.78, -1.94))

ss <- data.frame(
  pair = c("36-49", "52-67", "55-64"),
  x    = c(-0.26,  0.26, -0.06),
  xend = c( 0.10, -0.10,  0.30),
  y    = c( 1.44,  1.12,  0.80),
  yend = c( 1.16,  0.84,  1.34))

mut <- data.frame(
  lab = c("D45", "K48", "M50", "D62"),
  x   = c(-0.22, -0.02,  0.20,  0.26),
  y   = c( 1.40,  1.52,  1.38,  1.00))
# All four dots must sit clearly INSIDE the CRD ellipse, not on its stroke:
# a point on the boundary reads as "outside the domain", which would be wrong.
stopifnot(all(((mut$x - crd$x0) / crd$a)^2 +
              ((mut$y - crd$y0) / crd$b)^2 < 0.80))

## ----------------------------------------------------------------- 3. plot
p <- ggplot() +
  annotate("rect", xmin = -1.95, xmax = 1.95, ymin = y_in, ymax = y_out,
           fill = "#F4EEE2", colour = NA) +
  geom_segment(data = tails, aes(x, y, xend = xend, yend = yend),
               colour = "#D9CDB4", linewidth = 0.28) +
  geom_circle(data = lip_out, aes(x0 = x0, y0 = y0, r = r),
              fill = "#C9B99A", colour = NA) +
  geom_circle(data = lip_in, aes(x0 = x0, y0 = y0, r = r),
              fill = "#C9B99A", colour = NA) +

  geom_path(data = stalk, aes(x, y), colour = pal["Extracellular stalk"],
            linewidth = 2.6, lineend = "round") +
  geom_ellipse(data = crd, aes(x0 = x0, y0 = y0, a = a, b = b, angle = angle),
               fill = pal["CRD (TNFR-Cys, atypical)"], colour = "white",
               linewidth = 0.5, alpha = 0.95) +
  geom_segment(data = ss, aes(x, y, xend = xend, yend = yend),
               colour = ss_col, linewidth = 1.0, lineend = "round") +
  # Dots mark that the four residues lie inside the CRD. Their placement
  # within the blob is schematic, so they are NOT labelled individually:
  # labelling them would imply positional information this cartoon does
  # not carry. The identities go in one annotation instead.
  geom_point(data = mut, aes(x, y), shape = 21, size = 2.1,
             fill = "white", colour = "#333333", stroke = 0.45) +
  annotate("text", x = 0.62, y = 1.26, hjust = 0, size = 1.95,
           colour = "#111111", lineheight = 1.15,
           label = "TWEAK-binding\nresidues (schematic\nplacement):\nD45 · K48 · M50 · D62") +
  geom_path(data = nseg, aes(x, y), colour = pal["Extracellular N-segment"],
            linewidth = 2.6, lineend = "round") +

  annotate("rect", xmin = -0.135, xmax = 0.135, ymin = y_in, ymax = y_out,
           fill = pal["Transmembrane helix"], alpha = 0.10, colour = NA) +
  geom_path(data = tm, aes(x, y), colour = pal["Transmembrane helix"],
            linewidth = 2.2, lineend = "round") +

  geom_path(data = basic, aes(x, y),
            colour = pal["Juxtamembrane basic cluster"],
            linewidth = 2.8, lineend = "round") +
  geom_path(data = dtail, aes(x, y),
            colour = pal["Cytoplasmic tail (TRAF region)"],
            linewidth = 2.6, lineend = "round") +

  annotate("text", x = -1.90, y = 2.14, label = "Extracellular",
           hjust = 0, size = 2.6, fontface = "bold", colour = "#444444") +
  annotate("text", x = -1.90, y = -2.14, label = "Cytoplasm",
           hjust = 0, size = 2.6, fontface = "bold", colour = "#444444") +

  annotate("text", x = -0.70, y = 1.99, label = "N  28", hjust = 1,
           size = 2.1, colour = "#222222") +
  annotate("text", x = -0.56, y = 1.56, label = "36", hjust = 1,
           size = 2.1, colour = "#222222") +
  # 67 sits where the stalk (68-80) leaves the CRD, i.e. at the bottom,
  # so the chain reads in at upper-left (36) and out at the bottom (67).
  annotate("text", x = -0.10, y = 0.50, label = "67", hjust = 1,
           size = 2.1, colour = "#222222") +
  annotate("text", x =  0.17, y = 0.08, label = "80 | 81", hjust = 0,
           size = 2.1, colour = "#222222") +
  annotate("text", x =  0.17, y = -1.06, label = "101 | 102", hjust = 0,
           size = 2.1, colour = "#222222") +
  annotate("text", x =  0.36, y = -2.02, label = "129  C", hjust = 0,
           size = 2.1, colour = "#222222") +

  annotate("segment", x = 1.70, xend = 1.70, y = y_out, yend = y_in,
           colour = "#777777", linewidth = 0.3,
           arrow = grid::arrow(ends = "both",
                               length = grid::unit(0.035, "in"))) +
  annotate("text", x = 1.76, y = -0.5, hjust = 0, size = 1.95,
           colour = "#777777", label = "21 aa helix\n~31.5 Å") +

  coord_fixed(xlim = c(-1.95, 2.55), ylim = c(-2.35, 2.35), expand = FALSE) +
  theme_void(base_size = 7) +
  theme(plot.margin = margin(4, 4, 4, 4))

## ---------------------------------------------------------- 4. domain key
leg <- ann
leg$feature <- factor(leg$feature, levels = rev(ann$feature))
leg$label <- sprintf("%s  (%d–%d, %d aa)",
                     as.character(leg$feature), leg$start, leg$end, leg$len)

pl <- ggplot(leg, aes(x = 1, y = feature, fill = feature)) +
  geom_tile(width = 0.42, height = 0.60, colour = "white", linewidth = 0.4) +
  geom_text(aes(x = 1.3, label = label), hjust = 0, size = 2.25,
            colour = "#111111") +
  scale_fill_manual(values = pal, guide = "none") +
  coord_cartesian(xlim = c(0.7, 5.6), expand = FALSE) +
  theme_void(base_size = 7)

## -------------------------------------------------------------- 5. output
fig <- p / pl + plot_layout(heights = c(3.1, 1))

ggsave(file.path(outdir, "Fig_TR1_Fn14_topology.pdf"), fig,
       width = 95, height = 125, units = "mm", device = cairo_pdf)
ggsave(file.path(outdir, "Fig_TR1_Fn14_topology.svg"), fig,
       width = 95, height = 125, units = "mm", device = svglite::svglite)
ggsave(file.path(outdir, "Fig_TR1_Fn14_topology.png"), fig,
       width = 95, height = 125, units = "mm", dpi = 600,
       device = ragg::agg_png)

## --------------------------------------------------- 6. source data + audit
write.table(ann[, c("feature", "start", "end", "len", "seq")],
            file.path(outdir, "Fig_TR1_source_data.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)
write.table(data.frame(disulfide = c("36-49", "52-67", "55-64"),
                       residues  = c("C36-C49", "C52-C67", "C55-C64")),
            file.path(outdir, "Fig_TR1_disulfides.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

cat("\n--- Fig_TR1 audit ---\n")
print(ann[, c("feature", "start", "end", "len")])
cat(sprintf("mature chain 28-129  : %d aa\n", 129 - 28 + 1))
cat(sprintf("ECD  28-80           : %d aa\n", 80 - 28 + 1))
cat(sprintf("TM   81-101          : %d aa\n", 101 - 81 + 1))
cat(sprintf("ICD  102-129         : %d aa\n", 129 - 102 + 1))
cat("disulfides           : 36-49, 52-67, 55-64\n")
cat("binding residues     : D45 K48 M50 D62 (all within CRD 36-67)\n")
cat(sprintf("ECD   28-80  seq     : %s\n", substr(seq_h, 28, 80)))
cat(sprintf("TM    81-101 seq     : %s\n", substr(seq_h, 81, 101)))
cat(sprintf("ICD  102-129 seq     : %s\n", substr(seq_h, 102, 129)))
cat(sprintf("basic cluster 102-109: %s\n", substr(seq_h, 102, 109)))
writeLines(capture.output(sessionInfo()),
           file.path(outdir, "Fig_TR1_sessionInfo.txt"))
cat("sessionInfo written to figures/Fig_TR1_sessionInfo.txt\n")
