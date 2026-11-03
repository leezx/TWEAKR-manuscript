# CP1A_TNFRSF12A_dotplot — QA

- Backend: Python 3 / matplotlib 3.10.9 only. Script: `code/plot_checkpoint1a_dotplots.py`.
  It reads only `tables/expression_by_trimester_celltype.csv` and `tables/author_celltype_origin_map.tsv`.
- Size: 89 × 118 mm (single column). Text is 6 pt; gene title is 7 pt bold. No panel letter,
  because this is a standalone checkpoint figure.
- Fonts: Arial. SVG text is editable (`svg.fonttype=none`). PDF embeds ArialMT and
  Arial-BoldMT as TrueType (CID) fonts. Checked with pdffonts.
- TIFF: 600 dpi, 2102 px = 89.0 mm wide, LZW. A PNG preview is provided at 300 dpi.
- Colour: one sequential blue map (#F4F4F4→#0A2F5C, project main blue #0F4D92) and black
  text. The x-axis does not encode red/green or origin; origin is shown with black group
  headers only.
- Encoding check: zero-detection strata (open circles) are distinguished from strata with
  fewer than 20 nuclei (blank).
- Data check: summary tables cover 36 cell types and 193,202 nuclei per gene. Detection
  counts were re-derived independently via anndata (TNFSF12 1,825; TNFRSF12A 16,161;
  CD14_M 181 / 211) and match exactly.
- Known risks: small strata (e.g. aEC T1, ciliated T2) give unstable percentages. Check n in
  the source CSV. T3 has higher TNFRSF12A in nearly all types (5 donors).
- Illustrator check not yet performed (manual step).
