# Checkpoint 1C — Stereo-seq assay feasibility (DS-013)

**Decision (human review, 2026-10-08): PASS — NOT EVALUABLE.** Not evaluable for the
proposed TWEAK–TWEAKR cell-type-resolved spatial interaction analysis using currently
accessible public data. CP2: NOT PURSUED. This is a limitation of data accessibility and
annotation resolution, **not a negative biological result**.

Scope: metadata and gene-detection feasibility only. No spatial statistics, neighbourhood
or colocalisation analysis. No spatial matrix was downloaded. The COSMOS Stereo-seq explorer
(`build5/stereo_host`) was read by HTTP byte range (schema, obs, spatial embedding, 12 gene
vectors). Only aggregate tables were written. Script: `code/cp1c_spatial_feasibility.py`;
outputs: `tables/cp1c/`.

## Q1. Do the Stereo-seq data contain valid TNFSF12 / TNFRSF12A signal?

**Cannot be determined from public data.**

- Both genes are present in the explorer var list (25,794 genes; 1,077,690 cells).
- The transformation and interpretation of the publicly accessible spatial expression
  values could not be established. The values are not raw counts and are not consistent with
  conventional log-normalised counts:
  - only ~1% of nonzero values are integers;
  - nonzero values form a continuous range (TNFSF12: 0.05–3.85);
  - only 14.9% of 20,000 tested cells have values whose expm1 are integer multiples of a
    common unit, which is what log-normalised counts would require;
  - nonzero fractions are high (CD163 30.8%, LYVE1 31.3%, PECAM1 68.0%, KRT7 57.3% of all
    cells). This does not prove the data are wrong: transformation, smoothing, imputation or
    cell-type prediction can all produce it. It does prevent reading the values as per-cell
    transcript detection.
- So the explorer nonzero fractions (TNFSF12 9.1%, TNFRSF12A 31.8%) are **not detection
  rates**. They are stored as `pct_nonzero_explorer` for provenance only.
- Raw spatial counts are not publicly reachable: the portal's `STOMICS.h5ad` link returns
  HTTP 404 (2026-10-08), and the portal's Box link contains only `CODEX.zip`.
- Design factors that would limit detection even with raw counts (Supp Table 4c): 400–1,900
  mean counts per cell vs ~3,700 UMIs per nucleus in snRNA-seq. In snRNA-seq TNFSF12 is
  detected in only 0.94% of nuclei.

## Q2. Can EVT, maternal macrophage, endothelial and stromal compartments be distinguished?

**Partly.**

| Compartment | Author label(s) | Cells | Resolved? |
|---|---|---|---|
| EVT | EVT, iEVT, eEVT, EVTpro | 20,346 / 101,825 / 4,469 / 5,661 | Yes |
| Maternal macrophage | — (pooled in `Immune`, 32,717 cells) | — | **No.** No macrophage label; HB (fetal macrophage, 69,193) is separate |
| Endothelial | mVEC (maternal), fVEC (fetal) | 5,547 / 116,628 | Yes; mVEC is sparse (min 17 per section) |
| Stromal | DSC, DSC3, DSC4, FB, PV | 77,198 / 764 / 1,031 / 82,327 / 21,054 | Yes |

A macrophage subset could only be defined by re-annotating `Immune` from raw counts. Marker
values in the explorer are transformed, so they cannot support re-annotation either.

## Q3. Are cell-level coordinates, annotation and sample ID available?

**Yes.**

- All 1,077,690 cells have `spatial` x/y (no missing values, no duplicate xy within a section).
- Each cell has `subclass`, `celltype` and `sample_id`.
- The 16 sections are laid out without overlap on one shared canvas; within-section
  coordinates are usable. Coordinate units are not documented.
- The sections come from 16 sample IDs (001–016), all mid-gestation basal plate (GW18+6–24+1;
  Supp Table 4a). There is no first- or third-trimester spatial data.

## Implications

- Large-scale ligand–receptor colocalisation is **not justified** with the public spatial
  data: there is no valid gene-level detection, no macrophage label, and ligand detection is
  likely to be limiting.
- To answer Q1 and Q2, the raw Stereo-seq cell-bin count matrix (the object behind the
  broken `STOMICS.h5ad` link) would be needed. It could be added as an optional item to the
  author request. The request was **not sent** because DS-013 was closed. Even with raw
  counts, the TNFSF12 arm may be uninformative at this depth.
- Otherwise, DS-013 can rest as a snRNA-level expression observation (CP1A). That is the
  outcome already anticipated in the review.
