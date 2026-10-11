# Fig. 1c QA (2026-10-11)

- **Backend:** R 4 (ggplot2, patchwork, svglite, cairo_pdf, ragg). Rendered with `Rscript fig1c_plot.R` from this folder. No other language was used for drawing.
- **Size:** 183 × 64 mm (double column). Text is 5–6 pt. The panel letter "c" is added at Figure 1 assembly.
- **Editable text:**
  - SVG: 69 `<text>` objects, Arial.
  - PDF: ArialMT embedded (TrueType / CID TrueType).
  - TIFF: 4,322 × 1,511 px at 600 dpi, LZW.
- **Number check against the frozen tables:**
  - The c-ii values equal `tables/stage3/S3_contrasts_pooled.tsv` (estimand = final): 0.147/0.025/0.077/0.119; Holm 0.018/0.086/0.0009; n 108/106/203/59.
  - The c-iii values equal `S3_M2_continuous_pooled.tsv` (partial_lineage): 0.232 and −0.022, n = 216.
  - Stratum totals 50,539/46,048/20,334 equal `tables/stage1_v03a/strata75_lineage_composition.tsv` (asserted in the script).
  - Density weights sum to 1 over 222 patients (asserted).
- **Density source:** `code/fig1c_fig_density.py` on Argos. It writes aggregate 40 × 40 bins only; no cell or patient rows leave Argos.
- **Visual checks passed:** no overlapping text; the colour bar uses a diverging scale centred at uniform density; red and green are never the only code; one signal colour (#0F4D92) marks the hero contrast; no grid lines or frames.
- **Wording checks passed:** "predicted developmental potency" (not plasticity); "tumour-specimen-derived epithelial cells"; strata described as operational, programme-defined groups.
- **Open:**
  - The Illustrator round-trip check (fonts, clipping) is still to do at Figure 1 assembly.
  - The Extended Data panels ED-A to ED-H are not drawn yet.
