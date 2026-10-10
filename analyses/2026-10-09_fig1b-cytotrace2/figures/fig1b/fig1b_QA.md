# Fig. 1b QA

- **Claim:** across 222 patients from 13 cohorts, predicted developmental potential is ordered Stromal > Epithelial > Immune. The ordering survives depth matching, but the effects shrink by about 43–55%. Results review (2026-10-10) approved this claim.
- **Archetype:** quantitative grid. The hero panel (patient distribution) is paired with a robustness panel (pooled contrasts, original vs depth-matched).
- **Backend:** Python only; matplotlib 3.11.1 renders the plot, preview and every export.
- **Size:** 120 × 52 mm. This is a sub-panel of Figure 1 on a 183 mm page. Text is 5–6 pt; the panel label is 8 pt bold lowercase.
- **Editable text:**
  - SVG: 25 `<text>` objects, Arial (`svg.fonttype = none`).
  - PDF: ArialMT and Arial-BoldMT embedded as TrueType (`pdf.fonttype = 42`).
- **Raster:** `fig1b.tiff` is 600 dpi (2,832 × 1,224 px = 119.9 mm). `fig1b_preview.png` is 300 dpi.
- **Colour:** project palette.
  - Stromal `#42949E`, Epithelial `#0F4D92`, Immune `#767676`.
  - Original vs depth-matched estimates are distinguished by marker fill, not colour.
  - No red/green, so it stays readable in greyscale.
- **Statistics:** n, unit (patient), centre and spread, test, correction and the meaning of the interval are all stated in `fig1b_legend.md`. PIs are excluded from this panel by the review decision and are shown in Extended Data.
- **Source data:** `fig1b_source_left.csv` (patient medians), `fig1b_source_right.csv` (pooled estimates, CI, PI, seed range, Holm p). Generated from `tables/full/` by `fig1b_plot.py`.
- **Not yet checked:** opening the SVG/PDF in Adobe Illustrator. That has to be done by hand.
