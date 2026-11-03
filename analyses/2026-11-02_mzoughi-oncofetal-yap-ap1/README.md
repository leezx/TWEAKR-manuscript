# Mzoughi 2025 oncofetal reprogramming models — TWEAKR, YAP and AP-1

**Date:** 2026-11-02 · **Branch:** `analysis/20261102-mzoughi-oncofetal-yap-ap1` ·
**Status:** analysis complete, not yet reviewed · **Executed by:** Claude Opus 5 for Zhixin Li

## Question

Three questions put to Mzoughi *et al.*, *Nature Genetics* 57:402–412 (2025),
"Oncofetal reprogramming drives phenotypic plasticity in WNT-dependent colorectal
cancer":

1. **Is TWEAKR a marker of oncofetal cells** in the A and AKSP models, and does it
   correlate with the lineage plasticity score of the paper's Fig. 1j–l?
2. **Is TWEAKR regulated by YAP and AP-1** — using the paper's YAP and AP-1
   perturbations and its ATAC-seq — and are the placenta and tumour-intrinsic
   immune (cytotoxic resistance, immune suppression) programmes also regulated?
3. **FOLFIRI (Fig. 4)** — record the experimental design as a to-do rather than
   analyse it.

## Why this cohort matters

The TWEAKR manuscript claims *TNFRSF12A* marks a revival/oncofetal epithelial
state. Every cohort supporting that so far is observational. This study creates
the oncofetal state on demand with defined mutations and dismantles it with
defined perturbations of YAP and AP-1, in replicate, in isogenic organoids. It is
the first dataset available that can test the claim by perturbation rather than
by association.

Two choices keep the test from being circular:

- The oncofetal state is defined by **the authors' own mOnF signature**
  (Supplementary Table S1d, 51 genes), which does **not** contain *Tnfrsf12a*.
- The project's `revCSC` set **does** contain *Tnfrsf12a* (1 of 32, as recorded in
  the earlyCRC analysis), so it is never used to define the state here.

## Corresponding manuscript section

Supports the TWEAKR main claim and supplies the upstream mechanism. Intended as a
Results subsection with Fig. MZ1 and MZ2 as candidate main-figure panels and
Fig. MZ3 as the supporting chromatin negative. The placenta result bears directly
on the placenta arm of Figure 1; the immune result is recorded as open.

## Source data

All from GEO SuperSeries **GSE237954** (14 SubSeries) unless noted.
Local root: `DATA/HotData/TWEAKR-oncoFetal/geo_GSE237954_mzoughi_oncofetal/`.

| Layer | Accession | Used for |
|---|---|---|
| scRNA-seq, WT / A / AKSP organoids, 29,534 barcodes | GSE240129 | Q1 |
| Bulk RNA-seq, WT / A / AKSP progression, 9 | GSE239754 | Q2 |
| Bulk RNA-seq, YAP(S6A)-OE ± FOS in WT, 12 | GSE263050 | Q2 |
| Bulk RNA-seq, dominant-negative FOS during initiation, 12 | GSE263056 | Q2 |
| Bulk RNA-seq, YAP shRNA ×2 and FOS knockdown in AKSP, 15 | GSE263055 | Q2 |
| Bulk RNA-seq, oncofetal reporter high vs negative, 6 | GSE235205 | Q2 |
| Bulk RNA-seq, RXR overexpression along malignancy, 12 | GSE263045 | Q2 |
| Bulk RNA-seq, RXR inhibition in AKSP, 6 | GSE263044 | Q2 |
| Bulk ATAC-seq, WT / A / AKSP, 166,913 peaks | GSE239752 | Q2 |
| Bulk ATAC-seq, WT / RXRi / A, 212,463 peaks | GSE239755 | Q2 |
| Supplementary Tables S1c–S1g, S2c–S2e, S3i, S4c | MOESM1 (Springer) | Q1, Q2 |
| mm10 refGene | UCSC | peak-to-gene mapping |
| mm10 sequence, 432 peaks | UCSC REST API | motif scan |
| Bulk RNA-seq, VAKPS DMSO vs FOLFIRI, 6 | GSE237837 | **to-do only** |
| 10x Multiome AKSP (GEX + ATAC) | GSE237938 | downloaded, not used |

Not retrieved: GSE263047 (YAP/FOS knockdown during initiation) has no processed
counts in GEO; the authors' DESeq2 output for that contrast is read from
Supplementary Table S2c instead, and the limitation is stated where it is used.

Gene sets: the authors' mOnF/mStem and lineage signatures from Supplementary
Table 1; the project's frozen mouse sets (`CSC_subtypes.mouse.gmt`,
`Immune_Cytotoxic.mouse.gmt`, `YAP_targets_gmt/*.mouse.gmt`); and the project's
human placenta/IFA/TRA/EVT sets mapped to mouse orthologues with `babelgene`
(41→34, 352→352, 234→216, 39→40 genes; loss reported at run time, never silent).

## Method

- **Unit of analysis.** Bulk experiments are tested at the replicate level
  (3–4 organoid replicates per arm, DESeq2, batch in the model where present).
  The single-cell libraries carry **no replicate label** — the replicates were
  pooled before deposition — so no sample-level test is possible there. Cell-level
  p-values are reported but are not the basis of any claim; the inference is the
  effect size against 24 detection-matched control genes at identical *n*, plus
  agreement across the three independent libraries.
- **Confounder control.** All single-cell comparisons are made within
  genotype × library-depth quintile; the realised depth ratio between the two
  sides is reported with every result (0.96–1.00).
- **Calibration.** Every single-cell effect is benchmarked against detection-matched
  control genes. Every ATAC locus effect is benchmarked against all other peaks in
  the same contrast and against width- and accessibility-matched background peaks.
- **Programme level.** `cameraPR` on DESeq2 Wald statistics — a competitive test
  that accounts for inter-gene correlation — with global Benjamini–Hochberg across
  all contrasts × sets.
- **Window choice.** The ATAC window ladder (10/25/50/100/250/500 kb) was fixed in
  advance rather than selected after seeing the answer.
- Seed 20261102 throughout. R 4.5.2; DESeq2, limma, Seurat 5, Matrix, babelgene,
  dplyr, ggplot2, patchwork; Python 3 with openpyxl for the supplementary workbook.

## Scripts

| Script | Produces |
|---|---|
| `code/common.R` | env-overridable paths, palette, gene-set loader with orthologue mapping, mm10 gene models, matched-null helper |
| `code/00_extract_supplementary.py` | the authors' reference tables (signatures, lineage sets, their own DESeq2 output) from the 44 MB supplementary workbook into the HotData `processed/` tree |
| `code/01_scrna_tweakr_onf_plasticity.R` | `Q1*` — receptor in oncofetal cells, the Fig. 1j–l plasticity axis, control-gene calibration, the authors' own metacluster statistic |
| `code/02_bulk_perturbation.R` | `Q2*` — 15 DESeq2 contrasts, gene level and programme level, plus the one contrast that exists only as supplementary output |
| `code/03_atac_tweakr_locus.R` | `Q3*` — locus accessibility in two ATAC experiments, the window ladder, and the TEAD/AP-1 consensus scan against matched background |
| `code/04_make_figures.R` | `figures/Fig_MZ1…MZ3.{pdf,png}`. Reads only the frozen tables and computes no statistics, so figures cannot drift from the text |
| `code/05_signature_audits.R` | `Q5*` — review audits: is the plasticity axis independent of the mOnF signature; does the placenta signal survive removing generic YAP targets; are the immune results one gene; are the 15 contrasts independent |
| `code/06_chipatlas_occupancy.R` | `Q6*` — TEAD/YAP and AP-1 occupancy at the Tnfrsf12a TSS in all public mouse ChIP-seq, benchmarked against all genes and against the authors' oncofetal genes |
| `code/07_make_figure_MZ4.R` | `figures/Fig_MZ4_review_audits.{pdf,png}` |

Run with `Rscript code/<script>.R`. Paths come from `STELLIGEN_ROOT`,
`MZOUGHI_DIR`, `MZOUGHI_OUT`. Script 00 takes the workbook and an output
directory as arguments and runs under `python3 -I`.

## Outputs

| File | What it is |
|---|---|
| `docs/Results.md` | the drafted Results section with figure legends |
| `docs/findings.md` | every number, the negatives, claim ceilings, open items |
| `docs/TODO_FOLFIRI.md` | the Fig. 4 design recorded as a to-do, with the data already in hand |
| `figures/Fig_MZ1_receptor_oncofetal_state.{pdf,png}` | the receptor and the oncofetal state across three models |
| `figures/Fig_MZ2_yap_ap1_perturbation.{pdf,png}` | YAP and AP-1 perturbation, gene and programme level |
| `figures/Fig_MZ3_chromatin_negative.{pdf,png}` | the chromatin accessibility result and the motif scan |
| `figures/Fig_MZ4_review_audits.{pdf,png}` | the four review audits, including the ChIP-seq occupancy result |
| `tables/` | 24 TSVs, every statistic quoted anywhere |
| `manifests/` | checksums for outputs and for every source file |

## Results in one paragraph

*Tnfrsf12a* is the most oncofetal-enriched of 26 genes tested in both A
(+0.491 log) and AKSP (+0.619 log) tumoroids, beaten by none of 24 control genes,
and falls to +0.053 in wild-type organoids where the state is absent. It tracks
the paper's lineage plasticity axis (partial ρ 0.206 and 0.324), attenuated to
0.162 and 0.268 once the 14 genes that axis shares with the oncofetal signature
are removed, still with no control gene above it. Seven of seven YAP and AP-1
perturbations move it in the predicted direction — YAP-OE +2.39, YAP+FOS +2.71,
dominant-negative FOS −1.39, two YAP shRNAs −0.76 and −0.99, FOS knockdown −0.82,
all p_adj < 10⁻⁷ — and across 15 contrasts its Wald statistic tracks the
oncofetal programme's at ρ = 0.975 (0.976 on an arm-disjoint subset of 8). Public
ChIP-seq shows the promoter is a strongly bound TEAD and AP-1 element (83rd–97th
percentile of all genes), but none of the 4 intestinal experiments in the panel
calls a peak, so direct regulation remains open. Withdrawn in review: the
placenta result (gone once 4 of 34 genes that are generic YAP targets are
dropped) and the two immune-programme results (each carried by one gene, *Nt5e*
and *Serpinb9*). Other negatives: the authors' oncofetal reporter does not
separate on *Tnfrsf12a* (p_adj = 0.81), an unresolved conflict; and the locus
shows no consistent accessibility gain, which is uninformative about mechanism
rather than evidence against it.

## Verification, negative results and claim ceiling

- Every number in `docs/Results.md` and `docs/findings.md` was re-read from the
  frozen tables in `tables/` after the text was written.
- Reported negatives: the reporter sort; the chromatin discordance between the
  two ATAC experiments; the absence of motif enrichment; the immune programmes'
  one-directional behaviour; the ligand *Tnfsf12*, flat everywhere.
- Claim ceiling: **"enriched in oncofetal-like tumour cells, and responsive to
  YAP/AP-1 perturbation"**. **Not** "specifically marks oncofetal cells", **not**
  "a direct YAP/TEAD or AP-1 target gene", **not** "YAP and AP-1 act on a common
  element" — no experiment here perturbs either factor while measuring chromatin
  or occupancy, so direct action is untestable in this dataset.
- Known weaknesses, stated in `findings.md`: no replicate labels in the
  single-cell data; consensus motif counting instead of a PWM scan; 6–8 gene
  immune sets after orthologue mapping; mouse models throughout.

## Review status

Reviewed once (2026-11-02), outcome REQUEST_CHANGES with the analysis line
retained. All four requested changes are made; see the "Review response" section
of `docs/findings.md` for the item-by-item record.

Three of the changes were decided by running an audit rather than by rewording:

1. the mOnF / plasticity-score independence reservation — tested, association
   attenuates ~20% and survives;
2. the placenta result — tested, **does not survive** removing 4 of 34 genes that
   are generic YAP targets, so withdrawn;
3. the immune results — tested, each **carried by a single gene**, so withdrawn
   at programme level and kept as two single-gene observations.

New work prompted by the review: ChIP-Atlas occupancy at the *Tnfrsf12a* locus
(the review's P0). Positive — the promoter is a strongly bound TEAD and AP-1
element — but context-mismatched, so P0 is advanced rather than closed.

Open items are listed at the end of `docs/findings.md`, ordered by the review's
own priorities.
