# Ogden 2025 CRC liver metastasis — TWEAKR, oncofetal identity and inflammation

**Date:** 2026-11-02 · **Branch:** `analysis/20261102-ogden-crclm-tweakr-onf-ifn` ·
**Status:** Gate A complete; Gates B and C blocked by data availability ·
**Executed by:** Claude Opus 5 for Zhixin Li

## Question

Is *TNFRSF12A* (TWEAKR) a component of **oncofetal identity**, a responder to
**tumour-intrinsic inflammation**, or both, in human colorectal cancer liver
metastasis? Three competing models were specified in advance:

| Model | Prediction |
|---|---|
| **A** oncofetal-associated | the *TNFRSF12A*–revCSC link survives control for interferon response |
| **B** inflammation-associated | the link disappears once IFN/NF-κB is controlled |
| **C** dual-context | independent associations with both |

**Answer: Model C, with the oncofetal component dominant.** Both associations
survive mutual control in 12 of 12 patients; the oncofetal one is about twice
as large (median partial ρ 0.151 vs 0.071), larger in 11 of 12 patients
(P = 0.0015), and the only one unmatched by any detection-matched control gene.

## Why this cohort

Every cohort supporting the TWEAKR oncofetal claim so far is either mouse or
primary tumour. This is human, metastatic, and — critically — it comes from a
study whose own thesis is that the pro-metastatic states are driven by **AP-1
and NF-κB**. That makes it the right place to ask whether the receptor's
immune-related associations are separable from its oncofetal ones, rather than
assuming they are the same thing.

## Corresponding manuscript section

Supports the TWEAKR main claim in human metastatic tissue and **narrows** it:
the inflammatory association is genuine, so attributing every immune-related
observation to a TWEAKR–YAP axis is not supported. Fig. OG1 is the candidate
main panel; Fig. OG2 is the supporting limits-and-negatives panel.

## Source data

Ogden, Metic *et al.*, "Phenotypic heterogeneity and plasticity in colorectal
cancer metastasis", *Cell Genomics* **5**(7):100881 (2025).
Local root: `DATA/HotData/TWEAKR-oncoFetal/ogden2025_crclm_multiome/`.

| Layer | Accession | Deposited | Used |
|---|---|---|---|
| Decontaminated snRNA GEX, 21,284 nuclei × 36,485 genes, 15 patients | Mendeley `yd7bb3shn5` | `.h5ad`, 446 MB, sha256 verified | **yes** |
| snRNA-seq | E-MTAB-13651 | raw FASTQ only, 52 runs, 0.23 TB | no |
| snATAC-seq (paired) | E-MTAB-13652 | **raw FASTQ only**, 77 runs, 0.20 TB | **no — Gate B blocked** |
| Visium spatial, 3 patients | E-MTAB-13655 | **raw FASTQ + 3 TIFFs only**, 0.086 TB | **no — Gate C blocked** |

A Stage 0 audit established before any analysis that no processed ATAC or
spatial object is deposited anywhere, and that the spatial cohort is 3 patients.
Both downstream gates are recorded as blocked rather than attempted at low
power. See `docs/findings.md` for the full audit.

Gene sets: the project's frozen human sets (`revCSC.human.gmt`,
`YAP_targets_gmt/*.human.gmt`, `MSigDB_signaling.human.gmt`,
`Immune_Cytotoxic.human.gmt`), `proCSC` mapped from mouse with `babelgene`
(27 → 27), and MSigDB hallmark IFN-γ / IFN-α / TNFA-via-NFKB plus the REACTOME
antigen-presentation set via `msigdbr`.

## Method

- **Unit of inference is the patient.** Correlations are computed within each
  patient and aggregated with a signed-rank test over patients. Cell-level P
  values are never used as evidence.
- **Circularity guard.** *TNFRSF12A* is a member of `revCSC_human`,
  `Noncanonical_NFkB_TNFR2` and `STAT3_response` — it would have correlated with
  itself in *both* dimensions. It and *TNFSF12* are stripped from every set, and
  the removal is logged at run time, never silent.
- **The authors' state labels are not used to define the grouping**, only for
  post-hoc correspondence, so the test does not inherit their state definitions.
- **Confounder control.** Every partial correlation controls for the opposing
  dimension, S and G2M phase scores, log total counts and gene count.
- **Calibration.** Every effect is benchmarked against 24 genes matched on
  detection rate, holding *n* and sparsity fixed.
- **Pre-set thresholds.** Patient adequacy (≥ 100 epithelial nuclei, ≥ 5%
  receptor detection) and the ligand stop rule (> 10% detection; one source in
  ≥ 70% of patients) were fixed before results were seen.
- **Positive controls on negatives.** The REC/iREC comparison carries a positive
  control; it fails, so the result is reported as underpowered, not negative.
- Seed 20261102. Python 3.12 (scanpy 1.12.3, anndata 0.13.2, pandas, scipy);
  R 4.5.2 (msigdbr, babelgene, dplyr, ggplot2, patchwork, forcats).

## Scripts

| Script | Produces |
|---|---|
| `code/common.R` | env-overridable paths, palette, gene-set loader with the circularity guard, partial-Spearman and matched-null helpers |
| `code/00_freeze_signatures.R` | `Q0*` — freezes both signature dimensions to a GMT and reports their overlap |
| `code/01_gateA_onf_vs_inflammation.py` | `Q1*` — scoring, per-patient partial correlations, control-gene calibration, the 2×2 stratification, REC/iREC, ligand sources |
| `code/02_model_discrimination.py` | `Q2*` — the Model A/B/C call, the REC/iREC power verdict, the ligand stop rule, therapy |
| `code/03_make_figures.R` | `figures/Fig_OG1`, `Fig_OG2`. Reads only frozen tables and computes no statistics, so figures cannot drift from the text |

Run order: `00` → `01` → `02` → `03`. Paths come from `STELLIGEN_ROOT`,
`OGDEN_DIR`, `OGDEN_OUT`. Scripts 01 and 02 take the h5ad and the tables
directory as arguments.

## Outputs

| File | What it is |
|---|---|
| `docs/Results.md` | the drafted Results section with figure legends |
| `docs/findings.md` | the Stage 0 audit, every number, the negatives, claim ceilings, open items |
| `figures/Fig_OG1_tweakr_onf_vs_inflammation.{pdf,png}` | the Gate A deliverable |
| `figures/Fig_OG2_limits_and_negatives.{pdf,png}` | the limits and the negative results |
| `tables/` | 19 TSVs plus 3 JSON verdicts; every statistic quoted anywhere |
| `manifests/` | checksums for outputs and for every source file |

`tables/Q1_percell_scores.tsv.gz` holds the per-cell scores behind the figures.

## Results in one paragraph

*TNFRSF12A* is detected in 21.4% of 16,009 epithelial nuclei, highest in the
hybrid Intermediate state (35.8%) and in REC/iREC (both 30.3%), lowest in Stem
(12.6%) and Colonocyte (14.5%). Within each of 12 eligible patients it is
associated with oncofetal identity after controlling for interferon response,
cell cycle and depth (median partial ρ 0.151, 12/12 patients, above all 24
detection-matched control genes) and, independently, with interferon response
(0.071, 12/12, but matched by one control gene, *CLTB*). The oncofetal
association is the larger in 11 of 12 patients (P = 0.0015), and the strongest
of all signatures tested is YAP regeneration (0.172). Receptor detection rises
9.4% → 16.7% (IFN alone) → 23.5% (oncofetal alone) → 34.3% (both). Negatives
and limits: the REC vs iREC comparison is **underpowered, not negative** — its
positive control fails; the ligand *TNFSF12* triggers its stop rule on both
criteria (max 7.0% detection, no consistent source across patients) and is again
**not** macrophage-restricted; prior chemotherapy shifts nothing (all P > 0.33);
and chromatin and spatial analyses were impossible because only raw FASTQ is
deposited.

## Verification, negative results and claim ceiling

- Every number in `docs/Results.md` and `docs/findings.md` was re-read from the
  frozen tables in `tables/` after the text was written.
- Both figures were rendered and visually inspected; three presentation defects
  were corrected (a clipped threshold label, and two panels where free y-scales
  made null results look like effects — now shown with every patient and with
  P values on the panel).
- Reported negatives and non-results: the REC/iREC comparison and its failed
  positive control; the ligand stop rule; the chemotherapy null; the two
  tumour-intrinsic immune sets as the weakest in the table; and the inflammatory
  association being matched by a control gene.
- **Claim ceiling:** "associated with oncofetal identity in human CRC liver
  metastasis, independently of interferon response and more strongly than with
  it". **Not** "marks oncofetal cells", **not** "distinguishes REC from iREC",
  **not** any statement about chromatin, spatial niches, direct regulation or
  causal direction.

## Review status

Not yet reviewed.
