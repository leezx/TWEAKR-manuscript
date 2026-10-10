# Fig. 1b — Results and Methods text (draft for manuscript)

Extended Data figure numbering is provisional ("Extended Data Fig. 1b" = `figures/ed_fig1b`).
Status: draft built from the approved results (`Full_run_results.md` §6, review 2026-10-10). Wording follows
the reviewer's required revisions. Numbers come from `tables/full/`; do not edit them by hand.

## Results paragraph

To place epithelial cells within the developmental hierarchy of the tumour ecosystem, we applied
CytoTRACE2, a model that predicts transcriptional developmental potential from single-cell profiles, to
1,000,926 cells from 361 treatment-naive primary colorectal tumours (222 patients, 13 cohorts) and compared
compartments within each patient (Fig. 1b). Predicted potential was highest in the stromal compartment
(median of patient medians 0.287), intermediate in epithelium (0.131) and lowest in immune cells (0.062).
In random-effects meta-analysis of within-patient differences, epithelium scored higher than immune cells
(+0.073, 95% CI 0.056–0.089) and lower than stroma (−0.162, −0.206 to −0.117), and stroma exceeded immune
cells (+0.244, 0.197–0.290; all Holm-adjusted *P* < 0.001). The direction of all three differences was the
same in every cohort (Extended Data Fig. 1b panel a) and was preserved across the completed sensitivity analyses,
including the uncalibrated model score, restriction to unsorted samples, exclusion of cycling or low-complexity
cells and leave-one-cohort-out analysis (panel b). The differences were, however, sensitive to
sequencing depth: matching library size across compartments within each study attenuated them by
approximately 43–55% (epithelium − immune +0.042; epithelium − stroma −0.072; stroma − immune +0.116), and
on the uncalibrated score the depth-matched epithelium − immune difference was small (+0.012) with a
prediction interval that included zero. Among fine cell types, fibroblasts showed the highest predicted
potential (0.495), whereas the high-confidence malignant epithelial subset (0.138) fell within the range of
total epithelium (panels c, d). The high fibroblast score may reflect lineage-specific
mesenchymal programmes learned from developmental tissues rather than a primitive cell state. Thus, at the
compartment level, CRC epithelium occupies an intermediate position in predicted developmental potential,
motivating analysis of transcriptional states within malignant epithelial cells.

> Do not write: "fibroblasts are the primary source of cellular plasticity"; "epithelium shows elevated
> plasticity"; "unaffected by depth".

## Methods — Developmental potential (CytoTRACE2)

**Cohort and annotation.** Analyses used cohort v1 (13 studies, 222 patients, 361 treatment-naive primary
tumour samples) from the harmonized CRC atlas (DS-001). Compartments (epithelial, immune, stromal) were the
atlas level-1 labels. Fine (L2) cell types were harmonized and frozen (annotation v1, SHA256 recorded) before
any CytoTRACE2 score was examined; no CytoTRACE2 output was used to define, merge or split any label.

**Scoring.** Raw integer UMI counts (GENCODE v44 gene space; not integrated, corrected or normalised) were
scored per sample with CytoTRACE2 v1.1.0 (`species = "human"`, seed 14). The calibrated (smoothed) score was
primary; the cell-intrinsic raw model score was a pre-specified sensitivity analysis.

**Summaries and contrasts.** For each sample and compartment the median cell score was computed; the patient
value was the unweighted median across that patient's samples. A patient × compartment required ≥30 cells,
and a study was pooled only when it contributed ≥5 patients with all three compartments. Within-patient
differences (epithelial − immune, epithelial − stromal, stromal − immune) were averaged per study (t-based
95% CI) and pooled by random-effects meta-analysis (REML estimate of τ², Hartung–Knapp adjustment). 95%
prediction intervals used *k* − 2 degrees of freedom; heterogeneity is reported as Higgins' *I*². The three
contrasts were pooled separately (their estimates need not sum) and Holm-corrected as one family. A linear
mixed model (patient median ~ compartment + (1 | study) + (1 | study:patient)) was fitted as supporting
analysis.

**Depth matching.** For each study, the target depth *T*ₛ was the smallest of the three compartments'
25th-percentile library sizes (651–1,818 UMI). Cells below *T*ₛ were removed and all other cells were
downsampled without replacement to exactly *T*ₛ UMI; CytoTRACE2 was re-run per sample and eligibility
re-applied (220 patients, 13 studies). This was repeated with five random seeds; estimates are reported as
the seed mean (seed-to-seed range ≤0.003). Depth matching tests technical robustness and cannot remove
intrinsic differences in transcriptome complexity between lineages.

**Sensitivity analyses** (all pre-specified, or added at the L2 annotation review before results were
seen): raw model score; stringent eligibility (≥50 cells, ≥10 patients per study); unsorted samples only;
L1 compartments restricted to cells concordant with L2 (F1-clean); cycling-negative cells; exclusion of cells
with <500 detected model genes; fibroblasts (L2) in place of the stromal compartment; leave-one-study-out;
and a detection-adjusted estimate. The detection-adjusted estimate is the per-study regression intercept at
zero difference in median detected genes; because gene detection may itself carry the signal the model
uses, it risks over-adjustment and is secondary and exploratory. A permissive eligibility analysis (≥20
cells, ≥5 patients) and an external HTAPP–HTAN estimate were pre-specified but not performed (the additional
patients were outside the cohort v1 exports).

**L2 landscape.** Patient medians per L2 type (≥30 cells per patient × type) are descriptive; malignant
epithelial cells are the high-confidence CNV-supported subset (76 patients, 8 studies) and are enriched for
MSS tumours.

**Software and code.** CytoTRACE2 1.1.0 (R 4.x); statistics in Python (statsmodels; REML/Hartung–Knapp
implementation validated against metafor). Code: `analyses/2026-10-09_fig1b-cytotrace2/code/`.
