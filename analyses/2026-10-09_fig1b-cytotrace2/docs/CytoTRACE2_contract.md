# Fig. 1B CytoTRACE2 contract (draft v2.1 with amendments A1–A2.1, pending review)

- **Written:** 2026-10-09, before any CytoTRACE2 score was computed.
- **Amendments:**
  - **A1** (depth-matched sensitivity) followed input validation.
  - **A2** (harmonized annotation, revised depth rule, CytoTRACE2 internals, contrast family)
    followed user review.
  - **A2.1** (raw-score invariance test, matched-cell depth control, sample-wise vs patient-pooled
    diagnostic, paired-patient and meta-analysis details, malignancy confidence) followed review of
    A2. A2.1 was written while the technical pilot was running; **no pilot score had been inspected**.
  - A1 and A2 were written **before any score existed**.
- **Technical pilot:** started after A2 was drafted. Its outputs are technical only (see the Pilot
  section). Any later change made after scores exist must be logged as a dated amendment that states
  which results had been seen.

## Question and claim ceiling

**Question:** Across patients and studies, how is predicted developmental potential distributed
across harmonized epithelial and tumour-microenvironment cell types of treatment-naive primary CRC?

**Intended Fig. 1B statement:** *A harmonized, study-aware landscape of predicted developmental
potential across CRC epithelial and tumour-microenvironment cell states.*

**Claim ceiling:**
- CytoTRACE2 predicts transcriptional developmental potential. It does not measure plasticity or
  state-transition capacity.
- Cross-lineage differences may reflect lineage-specific programmes. Immune differentiation and
  epithelial differentiation are different hierarchies.
- Which compartments or types score higher is a finding, not a hypothesis.
- Statements about cancer-cell plasticity need the later epithelial-state analyses.
- Nothing in the annotation, depth handling or statistics is chosen to reproduce an expected ordering
  (for example stem > fibroblast > immune).

## Cohort (frozen; not changed by this contract)

- Cohort v1: 13 studies, 222 patients, 361 treatment-naive primary tumour samples, 1,003,249 cells.
- Source: `analyses/2026-10-09_fig1b-dataset-screen/cohort/` (manifest with SHA256; screen commit
  `43bbebb`).
- Sensitivity membership comes from the frozen `in_*` flags.

## Annotation (A2)

- **L1 (Epithelial / Immune / Stromal):** Atlas harmonized labels plus QC flags. Used for the primary
  compartment contrasts.
- **L2 (harmonized consensus cell types) and L3 (states):** see `Harmonized_annotation_plan.md`.
  - L2 is required for the lineage-level panel.
  - L2 must be frozen and reviewed **before** CytoTRACE2 results are interpreted by cell type.
  - Malignant epithelial cells form one L2 type, described in L3 by continuous programmes.
- **Independence:** no CytoTRACE2 output is used to define, merge or split any label.

## Input

- **Matrix:** DS-001 Atlas `layers/counts`, i.e. raw integer UMI per study in a common GENCODE v44
  gene space. Not integrated, corrected, SCT or log-normalised data. Integrated embeddings are used
  only for annotation.
- **Input validation (passed):** see the results section at the end.
- **Gene subset:** each sample is passed with the Atlas genes that map to a CytoTRACE2 model feature.
  - CytoTRACE2 discards all other genes in preprocessing.
  - Equivalence with an all-gene input is checked on one pilot sample.
- **Software:** CytoTRACE2 R 1.1.0, `species = "human"`, `seed = 14`, `batch_size = 10000`,
  `smooth_batch_size = 1000`, `ncores = 4`.

## CytoTRACE2 internals that determine the design (A2; from the 1.1.0 source)

| Step | Depends on the other cells in the same input? |
|---|---|
| Preprocessing: within-cell gene ranks and log2 CPM over model features | no |
| Model prediction: raw potency score and potency category (argmax of averaged class probabilities) | **no**: cell-intrinsic |
| Diffusion smoothing: random subsets of ≤1,000 cells, correlation graph on the batch's top-1,000 dispersed genes | yes |
| `binData`: within each potency category, the score is replaced by the cell's **rank among same-category cells in the batch**, spread uniformly over that category's sixth of [0, 1] | **yes, strongly** |
| kNN smoothing: 30 neighbours in a 30-PC space of the batch | yes |
| Batching: inputs >10,000 cells split into random batches | yes |

**Consequences:**
- **Primary run unit = whole sample** (all cells of one sample together). Cells of different
  compartments in the same sample are ranked within the same batch, so their within-category
  positions are comparable. Studies and patients are never mixed in one run.
- **Compartment-split runs are not valid for between-compartment contrasts.** `binData` re-spreads
  each compartment's within-category ranks to a uniform distribution, which removes the within-band
  differences between compartments by construction. They are run in the pilot only as a diagnostic.
- **Raw model score sensitivity (pre-specified; named in A2.1):** the model's raw score and potency
  category from `preprocessData` + `predictData`, before any smoothing or binning (code columns
  `intrinsic_*`).
  - It is called the *raw model score*, never an "intrinsic plasticity" score: a model output is not
    a cell's true plasticity.
  - By source it is per-cell: `BinaryModule` applies only stored parameters (weights,
    `running_mean`, `running_var`, `scale.factors`, background gene sets) to each cell's ranks and
    log2 CPM, with no statistic computed across cells. This is verified empirically by the A2.1
    invariance test.
  - A primary contrast that is absent from the raw model score is reported as depending on
    CytoTRACE2's within-sample postprocessing.

## Outputs and metrics

- **Per cell:** `CytoTRACE2_Score` (primary), `CytoTRACE2_Potency`, pre-kNN score, intrinsic raw score
  and category, detected model genes, library size, Atlas S/G2M scores and phase.
- **Primary metric:** the continuous `CytoTRACE2_Score`. Potency categories are descriptive only.
- **Aggregation:**
  1. Median per sample × compartment (or × L2 type).
  2. Per patient: the unweighted median across samples. In Joanito, several samples per patient are
     common (99 samples for 30 patients).
  3. Each patient × compartment needs ≥30 cells.
- **Statistical unit:** the patient. Cell-level tests are not used for inference.

## Statistics (A2)

- **Patients:** all three contrasts use the **same frozen 222 complete patients**, each contributing
  all three compartments. A contrast is never computed on a different patient subset from the others.
  Sensitivity sets re-apply this rule within their own patient sets.
- **Contrasts:** within-patient Δ = patient median(A) − patient median(B).
  - **Primary:** Epithelial − Immune; Epithelial − Stromal.
  - **Secondary:** Stromal − Immune.
  - **All three form one confirmatory family with Holm correction**, regardless of the
    primary/secondary label.
- **Study level:** the mean Δ over the study's patients with a 95% CI (t-interval; patient bootstrap as
  a check). Every study's direction and effect size are shown for all three contrasts, not only the
  pooled p-value.
- **Pooled (two-stage):**
  - Stage 1: each study's mean Δ and its standard error from that study's patients.
  - Stage 2: random-effects meta-analysis of the 13 study estimates (REML) with the Hartung–Knapp
    adjustment, because several studies have only 5–7 patients and their SEs are unstable.
  - Reported: study-specific effects with 95% CIs, pooled effect with 95% CI, τ², I², 95% prediction
    interval, and leave-one-study-out stability. The pooled p-value is never reported alone.
  - Weights follow each study's own uncertainty, so Qi 2022 (5 patients) is not given Pelka's
    precision.
- **Supporting model:** patient-median score ~ compartment + (1 | study) + (1 | study:patient).
- **Lineage level (L2, secondary):** within-patient contrasts between L2 types with CIs. These are
  descriptive, entered under the L2 eligibility rules.

## Pre-specified sensitivity analyses

| Analysis | Definition |
|---|---|
| Stringent | 50 cells / 10 patients (7 studies, 162 patients) |
| Unsorted-only | unsorted samples only; eligibility recomputed (205 patients; Liu 2024 drops out) |
| Fibroblast-specific | Fibroblast (L2) instead of broad Stromal (162 patients) |
| Leave-one-study-out | pooled contrasts with each study removed in turn |
| Permissive | 20 cells / 5 patients (222 + 11 patients) |
| Raw model score (A2/A2.1) | raw model score and category before smoothing and binning |
| Depth-matched (A1, revised in A2) | see below |
| Detection-adjusted (secondary) | contrast adjusted for the compartment difference in median log detected genes (meta-regression). Gene detection may itself carry signal the model uses, so this risks over-adjustment and is never the primary result |
| Cycling | cycling-positive and cycling-negative cells reported separately; contrasts recomputed on cycling-negative cells |
| Low-gene cells (A2.1) | cells with <500 detected model genes excluded; eligibility re-applied |
| HTAPP HTAN | separate exploratory estimate; never pooled; flagged for possible Pelka overlap |

**Depth-matched rule (A2 replaces the A1 rule; written before any score):**
- **Study-specific target:** T_s is the smallest of the three compartments' 25th-percentile library
  sizes, so every compartment keeps ≥75% of its cells. There is **no global UMI floor**.
- **Pre-computed retention** (`tables/input_validation/depth_targets.csv`; no CytoTRACE2 involved):

  | Study | T_s (UMI) | Patients still complete |
  |---|---|---|
  | Qian | 651 | 7 |
  | Qi | 770 | 5 |
  | Qin | 933 | 27 |
  | Khaliq | 1,043 | 7 |
  | Guo | 1,125 | 6 |
  | Li 2023 | 1,148 | 9 |
  | Liu | 1,263 | 12 |
  | Chen 2024 | 1,674 | 19 |
  | MUI | 1,741 | 12 |
  | Lee | 1,756 | 28 |
  | Joanito | 1,766 | 30 |
  | Pelka | 1,786 | 48 (of 50) |
  | Uhlitz | 1,818 | 10 |

  All 13 studies stay eligible.
- **Procedure:**
  - Cells below T_s are dropped. Every other cell is downsampled to exactly T_s UMI, without
    replacement.
  - CytoTRACE2 is re-run per sample, eligibility is re-applied, and the contrasts are recomputed.
  - **5 random seeds** are used; the Monte Carlo spread is reported.
  - A study with fewer than 5 complete patients after dropping is excluded from this analysis only.
- **Limit:** depth matching tests technical robustness only. It cannot remove intrinsic differences
  in transcriptome complexity between lineages, so it does not establish that cross-lineage scores
  are fully comparable.

**Cycling definition:**
- Independent of CytoTRACE2: Atlas `phase` (S/G2M from canonical cell-cycle genes) together with
  MKI67/TOP2A detection, fixed in the annotation plan as an L3 state.
- CytoTRACE2 is never used to define cycling or stem-like states.

## A2.1 technical diagnostics (pilot studies; technical only)

| Diagnostic | Design | Question |
|---|---|---|
| Raw-score invariance | fixed cells (150 per compartment, one Lee sample) scored alone and with +3,000 epithelial, +3,000 immune, +3,000 stromal or all three background cells from other Lee samples | is the raw model score identical per cell (expected max diff 0)? How much do the final score and category change? |
| Matched-cell depth control | per sample, three runs on the same retained cells (library ≥ T_s): (i) full sample, original counts; (ii) retained cells only, original counts (`sel`); (iii) retained cells downsampled to T_s (5 seeds) | (i) vs (ii) = selection effect of dropping shallow cells; (ii) vs (iii) = depth effect on identical cells |
| Sample-wise vs patient-pooled | patients with ≥2 tumour samples: all samples pooled into one run, compared with sample-wise runs | does the binning reference population (sample vs patient) change per-cell scores and patient medians? |
| Batching repeats | samples >10,000 cells (one Qin sample, 11,345 cells) re-run with seeds 1, 2, 3 | Monte Carlo variability from random batching |
| Low-gene cells | cells with <500 detected genes per study × compartment × sample (`tables/input_validation/low_gene_cells_by_*.csv`) | where are they concentrated? Do they pass Atlas QC? |

Low-gene cells (computed; no CytoTRACE2):
- All cohort cells pass the Atlas QC: the minimum is 200 detected genes in every study except MUI
  (100, BD Rhapsody). Chen 2024 (561) and Uhlitz (487) carry their original studies' stricter
  filters.
- Cells with <500 genes are concentrated in specific study × compartment combinations: Qian epithelial
  41%, Qi epithelial 39%, Qin immune 33%, Li 2023 immune 20%, Khaliq epithelial 20%. They are 0% in
  Chen 2024 and Joanito epithelial.
- They are **not excluded** in the primary analysis, because they pass QC and exclusion would be a
  post hoc filter. A sensitivity analysis excluding cells with <500 detected model genes is added,
  with eligibility re-applied.

The depth-target table already reports per-compartment cell retention at T_s
(`depth_targets.csv`: `*_retained_pct`).

## Pilot (technical; Joanito 2022, Lee 2020, Qin 2023)

- **Scope:** 85 patients, 165 samples, 421,649 cells; platforms 10x 3'/5' and DNBelab C4.
- **Status:** the pilot may run before the annotation freeze. Its outputs are **technical diagnostics,
  not biological results**. No compartment contrast from the pilot is reported as a finding or used
  to choose a method.

| Pilot question | Reported as |
|---|---|
| Does CytoTRACE2 run on every sample? | failures, warnings, runtime |
| Is the gene subset equivalent to the full gene input? | per-cell score agreement on one sample |
| How do whole-sample, intrinsic and split runs relate? | per-cell Spearman ρ; category agreement; how much the split run compresses between-compartment differences |
| Are there systematic study differences? | potency category shares per study and compartment |
| Can patient medians be estimated stably? | bootstrap of cells within patient: CI width |
| Do scores depend on depth? | within-study, within-compartment Spearman ρ with detected genes; depth-matched rerun on the pilot |

The full 13-study run waits for (1) approval of this contract and (2) the frozen L2 annotation.

## Outputs, storage, figure

- **Per-cell scores:** Argos `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/`.
- **Summaries, statistics and figure source data:** `analyses/2026-10-09_fig1b-cytotrace2/`.
- **Fig. 1B (`nature-figure`, Python):**
  - **B1:** L2 types on the x-axis, grouped by compartment, with CytoTRACE2 score on the y-axis.
    The plotting unit is the **patient median**, never pooled cells, with study-level summaries
    overlaid.
  - **B2:** forest plot of the within-patient compartment contrasts. One estimate per study with
    95% CI, then the pooled estimate.
  - **Extended Data:** study × L2 heatmap; sensitivity analyses.

## Input validation (results, SGE job 3654250; no CytoTRACE2 scores computed)

Tables: `tables/input_validation/`. Per-cell QC and per-gene detection stay on Argos.

1. **Raw counts:**
   - All 1,003,249 cohort cells were found in the H5AD.
   - All nonzero values are non-negative integers (0 violations).
   - No cell has a zero library.
2. **Gene identifiers:**
   - 28,476 Atlas genes (unique `var_names`).
   - 13,969 of the 14,271 CytoTRACE2 model features (97.9%) map to an Atlas gene, and no feature is
     hit by more than one Atlas gene.
3. **Per-study model-feature coverage:**
   - Coverage by genes detected in that study ranges from 90.3% (Guo) to 97.7%, i.e. 12,885 to
     13,947 features. Every study is above CytoTRACE2's 9,000-gene warning level.
   - Detection-based coverage also falls with fewer cells. It is an upper bound on "not measured".
4. **Depth differs strongly between compartments within a study** (median detected genes,
   Epithelial / Immune / Stromal):
   - Joanito 4,824 / 1,314 / 3,103
   - Pelka 3,432 / 1,100 / 2,503
   - Qi 627 / 1,494 / 4,209
   - Qian 724 / 993 / 1,970
   - Qin 1,165 / 664 / 1,179
   - The direction differs between studies.
   - Cells with fewer than 500 detected genes reach 41% (Qian epithelial).
   - This motivated A1 and the revised depth rule in A2.
