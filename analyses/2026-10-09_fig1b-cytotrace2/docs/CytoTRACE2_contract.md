# Fig. 1B CytoTRACE2 contract (draft, pending review)

Written on 2026-10-09 before any CytoTRACE2 score was computed. Changes after scores exist must be
logged as dated amendments that state whether results had been seen.

## Question and claim ceiling

**Question:** Across patients and studies, how is predicted developmental potential distributed
across the major cellular compartments of treatment-naive primary CRC?

**Claim ceiling:**
- CytoTRACE2 predicts transcriptional developmental potential. It does not measure plasticity or
  state-transition capacity.
- Differences between lineages may reflect lineage-specific programmes. Immune differentiation
  hierarchies and epithelial differentiation are not the same process.
- The intended Fig. 1B statement is: *a study-aware landscape of predicted developmental potential
  across CRC cellular compartments*.
- Which compartments are higher is a finding of the analysis, not a hypothesis. Statements about
  cancer-cell plasticity require the later epithelial-state analyses.

## Cohort (frozen; not changed by this contract)

- **Cohort v1:** 13 studies, 222 patients, 361 treatment-naive primary tumour samples, 1,003,249
  cells.
- Source: `analyses/2026-10-09_fig1b-dataset-screen/cohort/` (manifest with SHA256; screen commit
  `43bbebb`).
- Compartments use the harmonized Atlas labels. Epithelial / Immune / Stromal are primary; the
  7 lineages are secondary.
- Sensitivity membership comes from the frozen `in_*` flags. The permissive 20/5 extras are taken
  from the manifest.

## Input

- **Matrix:** DS-001 Atlas `layers/counts` (raw integer UMI per study, mapped by the Atlas to a
  common GENCODE v44 gene space). It is not integrated, batch-corrected, SCT or log-normalized
  data.
- **No study-specific re-download:** the per-study original matrices are not re-downloaded. The
  Atlas counts are the study counts re-annotated to one gene space; this is checked in the input
  validation below.
- **Genes:** Atlas `var_names` (unique symbols; Ensembl ID where no symbol exists).
  - CytoTRACE2 maps human symbols to its mouse model features with its own dictionary and aliases.
  - Model features without a mapped input gene are set to 0 by CytoTRACE2.
  - Per-study coverage of the model features by genes detected in that study is reported. A gene
    the study never measured looks identical to one it measured but did not detect.
- **Software:** CytoTRACE2 R 1.1.0 (`/home/zz950/softwares/R_lib_4`), `species = "human"`,
  `seed = 14`, defaults `batch_size = 10000`, `smooth_batch_size = 1000`.

## Run unit

- **Primary:** one CytoTRACE2 call per sample (patient × sample), with all cells of that sample,
  including lineage "Other".
- **Rationale:**
  - CytoTRACE2 smooths predictions by diffusion and kNN among the cells in the same call, so the
    call must not mix studies or patients.
  - Samples with more than 10,000 cells are processed in random batches of 10,000 (package
    default; seed fixed).
- **Pilot check of smoothing:** re-run each pilot sample split by broad compartment. Compare the
  per-cell and per-patient scores with the whole-sample run.

## Outputs and metrics

- **Per cell:** `CytoTRACE2_Score` (continuous 0–1, postprocessed), `CytoTRACE2_Potency` (discrete
  category), the pre-kNN score, library size, detected genes, and S/G2M scores from the Atlas obs.
- **Primary metric:** the continuous `CytoTRACE2_Score`. Potency categories are descriptive only.
- **Aggregation:**
  1. Median score per sample × compartment.
  2. Per patient × compartment: the unweighted median across that patient's samples, so a deeply
     sequenced sample does not dominate.
  3. Each patient × compartment needs ≥30 cells, as in the frozen cohort.

## Statistics

- **Primary estimand:** within-patient compartment contrasts, Δ = patient median(A) − patient
  median(B), for Epithelial − Immune, Epithelial − Stromal and Stromal − Immune.
- **Study level:** the mean Δ over the study's patients, with a 95% CI (t-interval; patient
  bootstrap as a check).
- **Pooled:** random-effects meta-analysis across the 13 studies (REML), reporting the 95% CI, I²,
  τ² and the 95% prediction interval.
  - Each study's weight reflects its own uncertainty, so Qi 2022 (5 patients) is not given the
    precision of Pelka (50).
- **Supporting model:** a linear mixed model, patient-median score ~ compartment + (1 | study) +
  (1 | study:patient).
- **Multiplicity:** three primary contrasts, with Holm correction on the pooled p-values. Effect sizes
  and intervals are the main reported quantities.
- **Secondary (lineage level):**
  - The 7 lineages, entered per patient when ≥30 cells and per study when ≥5 such patients. No
    study needs all 7.
  - Within-patient contrasts as above, reported descriptively with CIs.
- **Technical covariates** (always reported, never used to choose studies):
  - Within-study Spearman correlation of cell scores with log detected genes and log library
    size, per compartment.
  - Sensitivity: the contrast after adjusting the patient medians for the compartment difference in
    median log detected genes (meta-regression term).
  - Cell cycle: the contrast recomputed after excluding cells with phase S/G2M.

## Pre-specified sensitivity analyses

| Analysis | Definition |
|---|---|
| Stringent | 50 cells / 10 patients (7 studies, 162 patients) |
| Unsorted-only | unsorted samples only; eligibility recomputed (205 patients; Liu 2024 drops out) |
| Fibroblast-specific | Fibroblast instead of broad Stromal (162 patients) |
| Leave-one-study-out | pooled contrasts with each of the 13 studies removed in turn |
| Permissive | 20 cells / 5 patients (222 + 11 patients) |
| Depth / genes | adjustment for the compartment difference in detected genes |
| Depth-matched (A1) | per-study binomial downsampling to a common UMI target, CytoTRACE2 re-run, contrasts recomputed |
| Cell cycle | cycling cells excluded |
| HTAPP HTAN | separate exploratory estimate; never pooled; flagged for possible Pelka overlap |

A conclusion that disappears when one study is removed (for example Pelka or Chen 2024) is reported
as not robust across studies.

## Pilot (gate before the full run)

**Studies:** Joanito 2022, Lee 2020 and Qin 2023 (85 patients). They test the pipeline across three
platforms (10x 3'/5' and DNBelab C4); they are not assumed to be higher quality.

| Pilot question | Reported as |
|---|---|
| Does CytoTRACE2 run for every sample? | failures, warnings, runtime, memory |
| How many model genes map per study? | coverage table; CytoTRACE2 warns below 9,000 |
| Are score distributions plausible per compartment and lineage? | per-study distributions; potency category shares |
| Are there systematic study differences? | per-compartment medians by study |
| Can within-patient contrasts be estimated stably? | patient bootstrap of cells: CI width of patient medians |
| Do scores depend on depth or detected genes? | within-study, within-compartment Spearman ρ |
| Does smoothing across compartments matter? | whole-sample vs compartment-split runs |

The pilot results go to the user for review. The full 13-study run starts only after approval. The
pilot does not test the biological contrast against a significance threshold.

## Outputs and storage

- **Per-cell scores:** Argos `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/`.
- **Patient and sample summaries, statistics and figure source data:**
  `analyses/2026-10-09_fig1b-cytotrace2/`.
- **Figure:** forest-style dot plot (`nature-figure`, Python backend). It shows study estimates, the
  pooled estimate with 95% CI, and studies identified by colour. A study × compartment heatmap goes
  to Extended Data.

## Input validation (results, SGE job 3654250; no CytoTRACE2 scores computed)

Tables: `tables/input_validation/`. Per-cell QC and per-gene detection stay on Argos
(`input_validation/cohort_cell_qc.tsv.gz`, `study_gene_detection.tsv.gz`).

1. **Raw counts:**
   - All 1,003,249 cohort cells were found in the H5AD.
   - All nonzero values are non-negative integers (0 violations).
   - No cell has a zero library.
2. **Gene identifiers:**
   - 28,476 Atlas genes (GENCODE v44 Ensembl index; `var_names` unique, so no duplicated symbols).
   - CytoTRACE2 1.1.0 has 14,271 model features. 13,969 (97.9%) map to some Atlas gene, and no
     model feature is hit by more than one Atlas gene.
3. **Per-study model-feature coverage** (features whose mapped gene is detected in ≥1 cohort cell of
   the study):
   - The range is 90.3% to 97.7%, i.e. 12,885 to 13,947 features. Every study is well above
     CytoTRACE2's 9,000-gene warning level.
   - Lowest: Guo 2022 90.3%, MUI 92.3%, Uhlitz 92.5%, Liu 94.0%, Khaliq 95.0%. All others ≥95.6%.
   - Detection-based coverage also falls with fewer cells (Guo has the smallest cohort). It is an
     upper bound on "not measured", not a direct measure.
4. **Depth differs strongly between compartments within a study** (median detected genes,
   Epithelial / Immune / Stromal):

   | Study | Median genes (Epi / Imm / Str) |
   |---|---|
   | Joanito | 4,824 / 1,314 / 3,103 |
   | MUI | 4,958 / 1,497 / 2,925 |
   | Pelka | 3,432 / 1,100 / 2,503 |
   | Li 2023 | 3,157 / 758 / 2,192 |
   | Qi 2022 | 627 / 1,494 / 4,209 |
   | Qian 2020 | 724 / 993 / 1,970 |
   | Qin 2023 | 1,165 / 664 / 1,179 |

   - The direction is not consistent across studies: epithelial cells are deepest in most studies
     but shallowest in Qi and Qian.
   - The share of cells with fewer than 500 detected genes (CytoTRACE2 reports these) reaches 41%
     (Qian epithelial) and 33% (Qin immune).
   - Table: `tables/input_validation/depth_by_study_compartment.csv`.

**Consequence (amendment A1, written before any score):**
- Because CytoTRACE2 scores can track gene counts, compartment depth differences are the main
  technical confound for the primary contrasts.
- A **depth-matched sensitivity analysis** is added to the pre-specified set:
  - Within each study, every cell is binomially downsampled to a common UMI target: the study's
    5th percentile of library size across the three compartments, floored at 1,000 UMI.
  - Cells below the target are dropped.
  - CytoTRACE2 is re-run per sample and the contrasts are recomputed. Patient eligibility (≥30
    cells) is re-applied after dropping.
- The pilot also reports within-study, within-compartment Spearman ρ between score and detected
  genes, before and after downsampling.
- A primary contrast whose sign changes under depth matching will be reported as not robust to
  sequencing depth.
