# Fig. 1c Extended Data QA (2026-10-11, WL-20261011-1C-010)

- **Backend:** R (ggplot2, patchwork, svglite, cairo_pdf, ragg). Rendered with `Rscript fig1c_ed_plot.R` from this folder. No other language was used for drawing. Python was used only for the ED-B aggregation on Argos (`code/fig1c_ed_aggregates.py`, aggregate bins and counts only).
- **Size:** 183 × 240 mm (one full page). Text 5–6 pt; panel letters a–h 8 pt bold (map to ED-A … ED-H of the frozen panel map).
- **Editable text:** SVG has 269 `<text>` objects, all Arial (228 at 5 pt, 19 at 5.5 pt, 14 at 6 pt, 8 panel letters at 8 pt). PDF embeds ArialMT and Arial-BoldMT (TrueType / CID TrueType). TIFF 4,322 × 5,669 px at 600 dpi, LZW.
- **Number checks (asserted in the script or checked against the tables):**
  - c pooled estimates, PI, I², τ², LOSO range = `tables/stage4/S4_pooled.tsv` (analysis = base); study points = `tables/stage3/S3_contrasts_by_study.tsv` (final, Holm family; 8/8/13 studies).
  - d = `S3_contrasts_pooled.tsv` (final, raw, adj_full, adj_reduced, ds_mean) + `S4_pooled.tsv` (dsint_*); 32 rows asserted.
  - e, f, g = `S4_pooled.tsv`, `S3_contrasts_pooled.tsv` (final_ood_pass_only), `S4_loso.tsv` (Pelka left out), `S4_msi_interaction.tsv` (POOLED: 0.005 [−0.052, 0.062], P = 0.81), `S3_M2_continuous_pooled.tsv` and `S4_M2_ccat.tsv` (partial_lineage; n = 216 asserted).
  - b stratum sizes: p75 pro-dominant 50,539 asserted against the main-figure table; raw-density weights sum to 1 (asserted); 285,141 cells / 222 patients in the aggregation.
  - a: 52 verdicts, 12 "lineage_transfer_unverified" asserted.
  - h: funnel = `S3_M1_eligibility_funnel.tsv`; D1 = `S4_D1_dropout_audit.tsv`; D3 = `S4_D3_eligibility_retention.tsv`.
- **Visual checks passed:** no overlapping text at 100%; one signal colour (#0F4D92) for pro − rev and pro-dominant throughout; revCSC purple as in Fig. 1c; red and green not used as codes; no grid lines or frames; truncated intervals marked with arrows; descriptive (< 3 studies) rows labelled instead of plotted.
- **Wording checks passed:** "predicted developmental potency"; CCAT shown as a proxy with different units; strata operational; Holm family limited to Fig. 1c.
- **Open:** Illustrator round-trip at Figure 1 / ED assembly; ED figure number assigned at manuscript assembly.
