# Fig. 1 A3a panel: QA

- **Claim:** approved wording (final review, 2026-10-11).
- **Backend:** R only. ggplot2 4.0.3; svglite, cairo_pdf and ragg exports. R 4.5.2.
- **Size:** 89 × 62 mm (single column). Text 5–6 pt. The panel letter is added when Figure 1 is assembled.
- **Fonts:** PDF embeds ArialMT as TrueType. The SVG keeps text as `<text>` elements with font sizes of 5, 5.5 and 6 px (= pt).
- **Raster:** TIFF at 600 dpi with LZW compression; PNG preview at 300 dpi.
- **Colour:**
  - CytoTRACE2 `#0F4D92`, SCENT-CCAT `#42949E` (project palette).
  - The two algorithms are also told apart by marker fill (filled vs open), so the figure works in greyscale.
- **Content:** all five pre-specified programmes are shown, not only significant ones. Before- and after-adjustment results sit side by side on an identical x range, as the review required.
- **Statistics:** n = 216 patients / 13 cohorts is asserted in the script; source data are in `fig1_a3a_source.csv`.
- **Not done:** opening the file in Adobe Illustrator (manual).
