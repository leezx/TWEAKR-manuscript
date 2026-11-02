# Early-stage CRC oncofetal atlas (Snippert 2026) — re-analysis for the TWEAKR manuscript

**Date:** 2026-11-02 · **Branch:** `analysis/20261102-earlycrc-oncofetal-snippert` · **Status:** analysis complete, not yet reviewed

## Question

Three questions put to the published early-CRC oncofetal dataset, treated as an
external replication cohort for the TWEAKR manuscript:

1. **Regional enrichment.** Are proCSC, revCSC and the placenta/trophoblast axes
   enriched in a particular region of an early-stage tumour? (the paper's Fig. 1f–h data)
2. **Ligand sources.** Is a TWEAK–TWEAKR circuit detectable, and where do TWEAK
   (*TNFSF12*), *TGFB1* and *IL36G* come from?
3. **Co-emergence and colocalisation.** Do TWEAK⁺ macrophages appear at the same
   time, and in the same place, as oncofetal tumour cells? Same for *TGFB1* and *IL36G*.
   (the paper's Fig. 5 data)

## Why this cohort matters

Three claims in the TWEAKR manuscript rest on cohorts the lab assembled itself:
that tumour epithelium re-engages **fetal-intestinal and not trophoblast**
programmes; that **TNFRSF12A marks the revival state**; and that **TWEAK has no
single cellular source**. This dataset is independent of all of them, has
patient-level replication built in, and captures the earliest stage of invasion,
where the manuscript's spatial claims should be most visible if they are real.

## Source data

| Layer | Accession | Local path | Used for |
|---|---|---|---|
| GeoMx CTA (exp1), 10 patients, 1,781 targets, 303 segments | Zenodo [10.5281/zenodo.17671259](https://doi.org/10.5281/zenodo.17671259) | `DATA/HotData/TWEAKR-oncoFetal/zenodo_17671259_earlyCRC_oncofetal/extracted/Nanostring_GeoMx/exp1` | Q1 |
| GeoMx WTA (exp2), 10 patients, 18,441 targets, 281 segments | same | `.../exp2` | Q1 |
| CosMx run 2, 11 patients, ~1.25M cells, 6,175-gene panel | same | `.../Nanostring_CosMx/exp2` | Q3 |
| scRNA-seq TME (SORT-seq), 2,409 cells, 5 patients | EGAD50000002203 (processed copy) | `DATA/2.PROJECTS/1.TWEAKR-oncoFetal/data/external/Perturbation/Nature2026_oncofetal_EGAD50000002202/scRNAseq` | Q2 |

Paper: Buissant des Amorie *et al.*, *Nature* (2026), `s41586-026-10344-7`.
Raw sequence data (EGA) is controlled-access and was **not** retrieved; everything
here uses the authors' processed matrices. No file under any `raw/` directory, and
no pre-existing project file, was modified.

Gene sets are the project's frozen definitions, read read-only:
`Figure1F_candidate_human_genesets.v0.3.gmt` (proCSC/revCSC/Lgr5CSC and the
fetal/revival references), `IFA_core_FINAL.gmt`, `TRA_core_FINAL.gmt`,
`placenta_trophoblast.filtered.gmt`. Membership of the restricted
Joanito-derived lists is not reproduced here.

## Method

- **Unit of analysis is the patient everywhere.** Segment-level and cell-level
  values are averaged within patient × region (or patient × cell type) before any
  test. No test treats segments or cells as independent.
- **Scoring**: singscore (rank-based, centred) per GeoMx segment; mean log-CP10K
  over set members per CosMx cell.
- **Calibration**: every regional effect is additionally compared with 200
  expression-decile-matched random gene sets of the same size, drawn from the same
  panel. A signature only counts as regionally enriched if it beats that null —
  this is what separates a real programme from a set that happens to contain
  highly expressed or tumour-drifting genes.
- **Colocalisation null**: the ligand⁺ label is permuted among cells of the same
  type within the same field of view, so a positive result means *ligand-specific*
  proximity, not proximity to macrophages in general.
- Multiplicity: Benjamini–Hochberg within each panel × compartment family.
- Seed 20261102 throughout.

## Scripts

| Script | Produces |
|---|---|
| `code/common.R` | paths (env-overridable), palette, frozen gene-set loader |
| `code/01_geomx_region_enrichment.R` | `Q1_*` — invasive front vs core, matched-null calibrated, both panels, both compartments; plus a WTA-in-CTA-space sensitivity arm |
| `code/01b_geomx_all_regions.R` | `Q1b_*` — every region vs the rest, and a Friedman test across all four regions (not null-calibrated) |
| `code/01c_geomx_inv_vs_rest_matched_null.R` | `Q1c_*` — matched-null calibration of the inv-vs-rest contrast |
| `code/02_scrna_ligand_sources.R` | `Q2_*` — ligand and receptor detection by TME cell type, source decomposition, patient-paired regional tests |
| `code/03_cosmx_coemergence_colocalisation.R` | `Q3_*` — co-emergence across 11 pseudotimed tumours and ligand-specific colocalisation |
| `code/03b_cosmx_control_genes.R` | `Q3b_*` — the same colocalisation test on twelve detection-matched non-ligand control genes; this is what shows the score-threshold version of the test to be invalid |
| `code/04_make_figures.R` | `figures/Fig_EC1…EC3.{pdf,png}` — the three manuscript figures. Reads only the frozen tables above and computes no new statistics, so the figures cannot drift from the text |

Run with `Rscript code/<script>.R`. Paths come from `STELLIGEN_ROOT`,
`EARLYCRC_DIR`, `EARLYCRC_ZENODO_DIR`, `EARLYCRC_OUT`.

Software: R 4.5.2; Seurat 5, GeomxTools, singscore, RANN, Matrix, dplyr, ggplot2.

## Outputs

| File | What it is |
|---|---|
| `docs/Results.md` | the drafted Results section with figure legends |
| `docs/findings.md` | full write-up: every number, the negative results, claim ceilings, open items |
| `figures/Fig_EC1_regional_architecture.{pdf,png}` | stem-programme rebalancing at the invasive front; compartment specificity; trophoblast axes |
| `figures/Fig_EC2_tweak_axis.{pdf,png}` | TNFRSF12A at the front; ligand sources in the microenvironment |
| `figures/Fig_EC3_coemergence_colocalisation.{pdf,png}` | co-emergence, colocalisation and the control-gene test |
| `tables/`, `manifests/` | all statistics, with checksums for outputs and source archives |

The Results section and the three figures are also copied into the manuscript
delivery layer at `manuscript/v1/02_manuscript/Results_earlyCRC_replication.md`
and `manuscript/v1/01_figures/earlyCRC_replication/`.

## Review status

Not yet reviewed. Open items are listed at the end of `docs/findings.md`.
