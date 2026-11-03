# Fig. TR2 — TWEAKR / Fn14 (TNFRSF12A, Q9NP84): 3D structure in a membrane reference frame,
# domains coloured with the frozen B32 domain map (same palette as Fig. TR1).
#
# Run from code/ AFTER render_fig_TR2_structures.py:
#   Rscript make_fig_TR2_structure_membrane.R
# Inputs : ../figures/TR2_parts/{af_membrane.png, nmr_2kmz.png, projection.json, per_residue.tsv}
# Outputs: ../figures/Fig_TR2_Fn14_structure_membrane.{pdf,svg,png}, Fig_TR2_source_data.tsv,
#          Fig_TR2_sessionInfo.txt
# Deterministic; no random numbers. Membrane is drawn, not modelled (see legend).

suppressPackageStartupMessages({
  library(ggplot2); library(ggforce); library(patchwork); library(png); library(jsonlite)
})

parts <- "../figures/TR2_parts"
outd  <- "../figures"
pj  <- fromJSON(file.path(parts, "projection.json"))
res <- read.delim(file.path(parts, "per_residue.tsv"), stringsAsFactors = FALSE)

# ---------------------------------------------------------------- self-checks
stopifnot(nrow(res) == 129, paste(res$aa, collapse = "") ==
  "MARGSLRRLLRLLVLGLWLALLRSVAGEQAPGTAPCSRGSSWSADLDKCMDCASCRARPHSDFCLGCAAAPPAPFRLLWPILGGALSLTFVLGLLSGFLVWRRCRRREKFTTPIEETGGEGCPAVALIQ")
stopifnot(res$aa[c(45, 48, 50, 62)] == c("D", "K", "M", "D"),
          all(res$aa[c(36, 49, 52, 55, 64, 67)] == "C"),
          substr(paste(res$aa, collapse = ""), 102, 109) == "RRCRRREK")
stopifnot(abs(pj$rmsd_CA_CRD36_67_AF_vs_2KMZ_model1 - 1.248) < 0.01)  # recorded value

# AlphaFold PAE: is the CRD placement relative to the TM helix (hence the bilayer) determined?
struct_dir <- Sys.getenv("FN14_STRUCT_DIR",
  "/Volumes/Stelligen_SSD/Stelligen/DATA/HotData/TWEAKR-oncoFetal/external/structures_fn14")
pae <- fromJSON(file.path(struct_dir, "AF-Q9NP84-F1-predicted_aligned_error_v6.json"))
pae <- if (is.data.frame(pae)) pae$predicted_aligned_error[[1]] else pae$predicted_aligned_error
stopifnot(all(dim(pae) == c(129, 129)))
blk <- function(a, b) mean(pae[a, b])
pae_tab <- data.frame(
  block = c("CRD-CRD", "TM-TM", "CRD(aligned)->TM", "TM(aligned)->CRD", "TM(aligned)->JM",
            "TM(aligned)->C-tail"),
  mean_PAE_A = round(c(blk(36:67, 36:67), blk(81:101, 81:101), blk(36:67, 81:101),
                       blk(81:101, 36:67), blk(81:101, 102:109), blk(81:101, 110:129)), 1))
pae_crd_tm <- mean(pae_tab$mean_PAE_A[3:4])

dom <- data.frame(
  name  = c("Signal peptide (cleaved)", "Extracellular N-segment", "CRD (TNFR-Cys, atypical)",
            "Extracellular stalk", "Transmembrane helix", "Juxtamembrane basic cluster",
            "Cytoplasmic tail (TRAF region)"),
  short = c("SP", "N-seg", "CRD", "Stalk", "TM", "JM", "C-tail"),
  start = c(1, 28, 36, 68, 81, 102, 110),
  end   = c(27, 35, 67, 80, 101, 109, 129),
  col   = c("#B3B3B3", "#A6CEE3", "#1F78B4", "#7BA7C7", "#E6550D", "#6A51A3", "#31A354"),
  stringsAsFactors = FALSE)
# darker text versions for the two pale fills
dom$txt <- c("#7F7F7F", "#3F87BD", "#1F78B4", "#4F7FA3", "#C8470A", "#6A51A3", "#238B45")
SS_TXT <- "#A67C00"; BIND <- "#D7301F"; GREY <- "#555555"
res$domain_short <- dom$short[findInterval(res$resi, dom$start)]

fs  <- 6.2 / .pt   # label font size (pt -> mm)
fam <- "Arial"

# ---------------------------------------------------------------- panel a helpers
A  <- pj$af; W <- A$width; H <- A$height; s <- A$px_per_A; cx <- A$center[1]; cy <- A$center[2]
toX <- function(x) W / 2 + (x - cx) * s
toY <- function(y) H / 2 + (y - cy) * s            # y up (ggplot space)
pY  <- function(ypx) H - ypx                       # json pixels (y down) -> ggplot space
res$X <- toX(res$x); res$Y <- toY(res$y)
at <- function(r) c(res$X[res$resi == r], res$Y[res$resi == r])
cen <- function(a, b) colMeans(res[res$resi >= a & res$resi <= b, c("X", "Y")])

HALF <- 15                                  # Å, half hydrophobic thickness (drawn)
yo <- toY(HALF); yi <- toY(-HALF)
rh <- 2.6 * s                               # head-group radius
memx <- c(-420, 1980)
xs <- seq(memx[1] + rh, memx[2] - rh, by = 2 * rh + 14)
heads <- rbind(data.frame(x0 = xs, y0 = yo + rh), data.frame(x0 = xs, y0 = yi - rh))
tails <- do.call(rbind, lapply(xs, function(x) data.frame(
  x = c(x - rh * .35, x + rh * .35, x - rh * .35, x + rh * .35),
  y = c(yo, yo, yi, yi), yend = c(toY(1.5), toY(1.5), toY(-1.5), toY(-1.5)))))

img_af <- as.raster(readPNG(file.path(parts, "af_membrane.png")))

lab <- function(txt, col, lx, ly, ax, ay, hj = 0, seg = TRUE, face = "plain") {
  list(if (seg) annotate("segment", x = lx + ifelse(hj == 0, -25, 25), y = ly, xend = ax, yend = ay,
                         colour = "#8A8A8A", linewidth = 0.22),
       annotate("text", x = lx, y = ly, label = txt, hjust = hj, vjust = 0.5, colour = col,
                size = fs, family = fam, lineheight = 0.95, fontface = face))
}

crd <- cen(36, 67); stalk <- at(75); nseg <- at(31); tmmid <- at(91); jm <- at(106)
tail <- at(116); cterm <- at(129); n28 <- at(28)
b45 <- c(A$anchors_px[["45"]][1], pY(A$anchors_px[["45"]][2]))
ss1 <- c(A$disulfide_mid_px[["36-49"]][1], pY(A$disulfide_mid_px[["36-49"]][2]))
RX <- 2060  # right label column

pa <- ggplot() +
  annotate("rect", xmin = memx[1], xmax = memx[2], ymin = yi - 2 * rh, ymax = yo + 2 * rh,
           fill = "#F4EEE2", colour = NA) +
  geom_segment(data = tails, aes(x = x, xend = x, y = y, yend = yend),
               colour = "#D9CDB4", linewidth = 0.25) +
  geom_circle(data = heads, aes(x0 = x0, y0 = y0, r = rh), fill = "#C9B99A", colour = NA) +
  annotation_raster(img_af, xmin = 0, xmax = W, ymin = 0, ymax = H, interpolate = TRUE) +
  # compartments
  annotate("text", x = -420, y = toY(52), label = "Extracellular", hjust = 0, size = 7 / .pt,
           fontface = "bold", colour = "#444444", family = fam) +
  annotate("text", x = -420, y = toY(-44), label = "Cytoplasm", hjust = 0, size = 7 / .pt,
           fontface = "bold", colour = "#444444", family = fam) +
  annotate("text", x = -420, y = toY(0), label = "Lipid\nbilayer", hjust = 0, size = fs,
           colour = "#8C7B5A", family = fam, lineheight = 0.95) +
  # right-hand callouts
  lab("TWEAK-binding residues\nD45 · K48 · M50 · D62", BIND, RX, pY(250), b45[1], b45[2]) +
  lab("Cysteine-rich domain\n(CRD, TNFR-Cys) 36–67", dom$txt[3], RX, pY(500), crd[1] + 180, crd[2]) +
  lab("3 disulfides: C36–C49,\nC52–C67, C55–C64", SS_TXT, RX, pY(760), ss1[1], ss1[2]) +
  lab("N-terminus (E28)\nN-segment 28–35", dom$txt[2], RX, pY(1110), n28[1] + 20, n28[2]) +
  lab("Transmembrane helix\n81–101 (21 aa)", dom$txt[5], RX, tmmid[2], tmmid[1] + 110, tmmid[2]) +
  lab("Juxtamembrane basic\ncluster 102–109\nRRCRRREK", dom$txt[6], RX, jm[2] - 40, jm[1] + 90, jm[2]) +
  # left-hand callouts
  lab("Stalk 68–80", dom$txt[4], 380, stalk[2] + 140, stalk[1] - 60, stalk[2], hj = 1) +
  lab("Cytoplasmic tail 110–129\n(TRAF-binding region)", dom$txt[7], 700, pY(2930),
      tail[1] - 40, tail[2], hj = 1) +
  lab("C-terminus (Q129)*", dom$txt[7], 380, cterm[2] + 20, cterm[1] - 40, cterm[2], hj = 1) +
  # scale bar 10 Å
  annotate("segment", x = 1700, xend = 1700 + 10 * s, y = pY(2960), yend = pY(2960),
           linewidth = 0.4, colour = "#333333") +
  annotate("text", x = 1700 + 5 * s, y = pY(2960) - 60, label = "10 Å", size = fs,
           family = fam, vjust = 1, colour = "#333333") +
  coord_fixed(xlim = c(-440, 2900), ylim = c(pY(3420), pY(130)), expand = FALSE, clip = "off") +
  theme_void(base_family = fam) +
  annotate("text", x = -420, y = pY(3200), hjust = 0, vjust = 1, size = 5.6 / .pt, family = fam,
           colour = GREY, lineheight = 1,
           label = paste0("Bilayer is drawn, not modelled: placed on the TM-helix (81–101) axis, ",
                          "hydrophobic core ±15 Å.\nCRD placement relative to the bilayer is ",
                          sprintf("not determined (CRD↔TM mean PAE %.0f Å; within-domain ≤ %.0f Å).",
                                  pae_crd_tm, max(pae_tab$mean_PAE_A[1:2])),
                          "\n* AlphaFold places 124–129 inside the bilayer ",
                          "(pLDDT < 50); not a physical position.")) +
  labs(title = "AlphaFold model AF-Q9NP84-F1 (v6), mature chain 28–129") +
  theme(plot.title = element_text(size = 6.5, colour = GREY, hjust = 0,
                                  margin = margin(0, 0, 2, 0)))

# ---------------------------------------------------------------- panel b (2KMZ)
B <- pj$nmr2kmz; W2 <- B$width; H2 <- B$height
img_nmr <- as.raster(readPNG(file.path(parts, "nmr_2kmz.png")))
tip  <- B$sidechain_tip_px; ssm <- B$disulfide_mid_px; anc <- B$anchors_px
bl <- function(t, p, dx, dy, col, hj = 0.5)
  annotate("text", x = p[1] + dx, y = H2 - p[2] + dy, label = t, colour = col, size = fs,
           family = fam, fontface = "bold", hjust = hj)
pb <- ggplot() +
  annotation_raster(img_nmr, xmin = 0, xmax = W2, ymin = 0, ymax = H2, interpolate = TRUE) +
  bl("D45", tip[["45"]], 120, 70, BIND) + bl("K48", tip[["48"]], 230, -20, BIND) +
  bl("M50", tip[["50"]], -230, 40, BIND) + bl("D62", tip[["62"]], 170, -40, BIND) +
  bl("C36–C49", ssm[["36-49"]], 170, -60, SS_TXT, 0) +
  bl("C52–C67", ssm[["52-67"]], -110, -40, SS_TXT, 1) +
  bl("C55–C64", ssm[["55-64"]], -230, -60, SS_TXT, 1) +
  bl("N (E28)", anc[["28"]], -200, 110, dom$txt[2]) +
  bl("P80", anc[["80"]], -40, 0, dom$txt[4], 1) +
  annotate("text", x = 1000, y = 330, hjust = 0, vjust = 0, size = fs, family = fam, colour = GREY,
           lineheight = 0.95,
           label = sprintf("Same orientation as a\n(CRD superposed).\nCRD Cα RMSD vs AF: %.2f Å\n(32 Cα, 36–67)",
                           pj$rmsd_CA_CRD36_67_AF_vs_2KMZ_model1)) +
  coord_fixed(xlim = c(60, W2 - 60), ylim = c(230, H2 - 120), expand = FALSE, clip = "off") +
  theme_void(base_family = fam) +
  labs(title = "Experimental ECD: PDB 2KMZ (solution NMR, model 1 of 20)") +
  theme(plot.title = element_text(size = 6.5, colour = GREY, hjust = 0,
                                  margin = margin(0, 0, 2, 0)))

# ---------------------------------------------------------------- panel c (linear map + pLDDT)
ss_df <- data.frame(a = c(36, 52, 55), b = c(49, 67, 64))
pc1 <- ggplot() +
  geom_rect(data = dom, aes(xmin = start - 0.5, xmax = end + 0.5, ymin = 0, ymax = 1, fill = name),
            colour = "white", linewidth = 0.2) +
  scale_fill_manual(values = setNames(dom$col, dom$name), breaks = dom$name, name = NULL) +
  geom_curve(data = ss_df, aes(x = a, xend = b, y = 1.05, yend = 1.05), curvature = -0.45,
             colour = "#F2C300", linewidth = 0.4, ncp = 10) +
  annotate("point", x = c(45, 48, 50, 62), y = -0.28, shape = 17, size = 1.1, colour = BIND) +
  annotate("text", x = 66, y = -0.28, label = "TWEAK-binding residues", hjust = 0,
           colour = BIND, size = 5.4 / .pt, family = fam) +
  annotate("text", x = 69, y = 1.55, label = "disulfides", hjust = 0,
           colour = SS_TXT, size = 5.4 / .pt, family = fam) +
  annotate("text", x = (dom$start + dom$end) / 2, y = 0.5, label = dom$short,
           colour = c("black", "black", "white", "black", "white", "white", "white"),
           size = 5.2 / .pt, family = fam) +
  scale_x_continuous(limits = c(0.5, 129.5), breaks = c(1, 28, 36, 67, 81, 101, 110, 129),
                     expand = c(0, 0), position = "top") +
  scale_y_continuous(limits = c(-0.5, 2.1), expand = c(0, 0)) +
  theme_void(base_family = fam) +
  theme(axis.text.x.top = element_text(size = 5.5, colour = GREY, margin = margin(0, 0, 1, 0)),
        legend.position = "none")

band <- data.frame(lo = c(0, 50, 70, 90), hi = c(50, 70, 90, 100),
                   col = c("#FF7D45", "#FFDB13", "#65CBF3", "#0053D6"),
                   lab = c("<50", "50–70", "70–90", ">90"))
res$band <- cut(res$plddt, c(0, 50, 70, 90, 100), labels = band$lab, right = FALSE)
pc2 <- ggplot(res, aes(resi, plddt)) +
  annotate("rect", xmin = 0.5, xmax = 27.5, ymin = 0, ymax = 100, fill = "#EFEFEF") +
  annotate("text", x = 14, y = 12, label = "cleaved", size = 5.2 / .pt, colour = "#8A8A8A",
           family = fam) +
  geom_hline(yintercept = c(50, 70, 90), linewidth = 0.2, colour = "#C8C8C8", linetype = 2) +
  geom_line(linewidth = 0.3, colour = "#555555") +
  geom_point(aes(colour = band), size = 0.55) +
  scale_colour_manual(values = setNames(band$col, band$lab), drop = FALSE, name = "pLDDT") +
  scale_x_continuous(limits = c(0.5, 129.5), expand = c(0, 0), breaks = NULL) +
  scale_y_continuous(limits = c(0, 100), breaks = c(0, 50, 70, 90), expand = c(0, 0)) +
  labs(x = NULL, y = "AF pLDDT") +
  theme_classic(base_size = 6, base_family = fam) +
  theme(axis.line = element_line(linewidth = 0.25), axis.ticks = element_line(linewidth = 0.25),
        axis.text = element_text(size = 5.5, colour = GREY), legend.position = "bottom",
        legend.key.size = unit(2, "mm"), legend.text = element_text(size = 5.5),
        legend.title = element_text(size = 5.5), legend.margin = margin(0, 0, 0, 0),
        legend.box.margin = margin(-4, 0, 0, 0))
pc <- pc1 / pc2 + plot_layout(heights = c(1, 1.5))

# ---------------------------------------------------------------- assemble
right <- wrap_elements(full = pb) / wrap_elements(full = pc) + plot_layout(heights = c(1.15, 1))
fig <- (wrap_elements(full = pa) | right) + plot_layout(widths = c(1.3, 1)) +
  plot_annotation(tag_levels = "a") &
  theme(plot.tag = element_text(size = 8, face = "bold", family = fam))

wmm <- 180; hmm <- 122
ggsave(file.path(outd, "Fig_TR2_Fn14_structure_membrane.pdf"), fig, width = wmm, height = hmm,
       units = "mm", device = cairo_pdf)
ggsave(file.path(outd, "Fig_TR2_Fn14_structure_membrane.svg"), fig, width = wmm, height = hmm,
       units = "mm", device = svglite::svglite)
ggsave(file.path(outd, "Fig_TR2_Fn14_structure_membrane.png"), fig, width = wmm, height = hmm,
       units = "mm", dpi = 600, device = ragg::agg_png, bg = "white")

# ---------------------------------------------------------------- source data
src <- res[, c("resi", "aa", "domain_short", "plddt", "x", "y", "z")]
src$domain <- dom$name[findInterval(src$resi, dom$start)]
src$tweak_binding_site <- src$resi %in% c(45, 48, 50, 62)
src$disulfide_cys <- src$resi %in% c(36, 49, 52, 55, 64, 67)
names(src)[5:7] <- c("x_membrane_frame_A", "y_membrane_frame_A", "z_membrane_frame_A")
write.table(src, file.path(outd, "Fig_TR2_source_data.tsv"), sep = "\t", quote = FALSE,
            row.names = FALSE)
write.table(pae_tab, file.path(outd, "Fig_TR2_pae_blocks.tsv"), sep = "\t", quote = FALSE,
            row.names = FALSE)
writeLines(capture.output(sessionInfo()), file.path(outd, "Fig_TR2_sessionInfo.txt"))
cat("done\n")
