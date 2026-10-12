# Extended Data (A3b): QA

- **Claim:** approved Results text (Stage S final approval, 2026-10-12, `docs/A3b_stageS_final_approval_20261012.md`). Data come from the corrected tables at commit 7a2ecfc.
- **Backend:** R only; ggplot2 4.0.3 + patchwork 1.3.2; svglite, cairo_pdf and ragg exports.
- **Size:** 183 × 150 mm.
- **Text:** 5–6 pt; panel letters 8 pt bold. The SVG has 76 `<text>` elements at 5, 5.5, 6 and 8 px (= pt) and none smaller. A first render produced 3.5 pt plotmath subscripts (P_BH); these were replaced with plain text.
- **Fonts:** PDF embeds ArialMT and Arial-BoldMT as TrueType.
- **Raster:** TIFF at 600 dpi (4322 px wide), LZW; preview PNG at 200 dpi.
- **Data assertions in the script:** E1 n = 85 and k = 6; estimate 0.0571; P02 absent; 85 patient points; Qin original-depth n = 20; Qin E1-pp patients = 18; Chen = 10. The script stops if the tables are the uncorrected version.
- **Content (per final approval):**
  - **a:** MUI is shown, with no exclusion; heterogeneity (I²), P = 0.068 and n = 85 are printed.
  - **b:** BH-adjusted P values.
  - **c:** both classes, with nominal P labelled.
  - **d:** depth-matched primary, plus same-patient original depth; Qin TRG0 exclusion and specimen confounding are in the legend.
- **Colour:**
  - Blue `#0F4D92` marks pooled and primary estimates; teal `#42949E` marks the exploratory E1-L; grey shows patients and studies.
  - Shape also carries meaning (filled diamond = primary, open = sensitivity), so the figure works in greyscale.
- **Not done:** Adobe Illustrator round-trip check (manual).
