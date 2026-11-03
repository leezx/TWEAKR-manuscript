# Checkpoint 1D contract — TWEAK-associated macrophage state (DS-013, scoped reopening)

Written before analysis on 2026-10-08. User-approved scope: **snRNA-seq macrophage-state
analysis only.** No Stereo-seq; CP2 stays NOT PURSUED. Level 3 needs separate approval.

## Question

Does a Tnfsf12-associated macrophage transcriptional program, identified in a mouse AOM/DSS
colorectal tumour model, also occur in human maternal–fetal interface macrophages? Within
those macrophages, is it associated with independently measured TNFSF12 detection?

Claim ceiling: the analysis can identify a **TWEAK-associated macrophage state**. A
signature alone can never show that cells express or secrete TWEAK.

## Signatures (candidate gene sets, not validated classifiers)

Taken from the AOM/DSS Tnfsf12+ vs other TAM comparison, as transcribed by the user. Human
orthologues are upper case; all genes are present in the H5AD. TNFSF12 is **never** part of
any score; it is the independent readout.

| Module | Genes | Role |
|---|---|---|
| CORE | GPNMB, SPP1, TREM2, APOE, FABP5, PLD3 | test |
| EXTENDED | CORE + CTSD, CTSB, CTSS, ACP5, C1QA, C1QB, C1QC, LGMN, LIPA | test |
| LYSO_CONTROL | CTSD, CTSB, CTSS, ACP5, LGMN, LIPA | negative control: generic lysosomal activity |
| COMPLEMENT_CONTROL | C1QA, C1QB, C1QC | control: generic macrophage complement |
| MAC_IDENTITY | CD68, CD163, CSF1R, CD14, MRC1 | control: macrophage identity |
| MONO_LIKE | FCN1, S100A8, S100A9, LYZ, VCAN | monocyte-likeness (QC) |
| Matched random | 500 random gene sets per test module, each gene drawn from the same expression bin as its module gene | empirical null |

## Data and levels

- **Level 1.** Use the author snRNA immune labels (CD14_M, CD16_M, HB, dNK, T, B, cDC). A
  marker check found no separate monocyte or mast-cell label: CD16_M carries monocyte-like
  features and mast cells are essentially absent. Re-annotation is not needed. Outputs:
  immune UMAP (author integrated `X_umap`, subset), marker DotPlot, donor composition.
- **Level 2.**
  - Primary population: maternal decidual macrophages, CD14_M + CD16_M (n = 9,276; 23 donors).
  - Sensitivity: CD14_M only, which excludes the monocyte-like CD16_M.
  - Secondary: HB (fetal macrophages), reported separately.
- Scores: `scanpy.tl.score_genes` on per-nucleus log1p(CP10k), computed within the
  population; seed 0.

## Pre-specified tests

1. **Overlap.** Spearman correlation between module scores; Jaccard overlap of the top-quartile
   cells (quartiles taken within each donor) for CORE vs EXTENDED and CORE vs LYSO_CONTROL.
2. **TNFSF12 association.**
   - (a) Within each donor (≥40 macrophages), split at the donor median score and compare
     TNFSF12 detection in the high and low halves. Report the Mantel–Haenszel OR across
     donors, the count of donors with high > low, a sign test and a Wilcoxon test.
   - (b) Donor-stratified logistic regression (implemented as donor fixed effects, because the
     statsmodels conditional logit fails at these stratum sizes; amended before any result was seen):
     TNFSF12_detected ~ z(score) + log10(library size), reporting OR per SD. Donors without
     any TNFSF12+ macrophage are uninformative and drop out.
3. **Specificity.**
   - (a) Compare the CORE and EXTENDED OR per SD with the matched-random null (empirical
     one-sided p).
   - (b) Fit CORE + LYSO_CONTROL jointly; if CORE adds nothing beyond lysosomal activity, the
     state is not TWEAK-specific.
4. **Depth.** Compare library size between score-high and score-low halves within each donor.
   Library size is a covariate in 2b.

## Decision rule for the Level 2 → Level 3 gate

- **PASS (signature-linked TWEAK-associated state supported):** all of the following hold for
  CORE or EXTENDED.
  - MH OR > 1 with 95% CI excluding 1.
  - High > low in a majority of informative donors.
  - Conditional-logit OR per SD > 1 with CI excluding 1, after library-size adjustment.
  - OR exceeds the matched-random null (p < 0.05).
  - Remains > 1 after adjusting for LYSO_CONTROL.
  - Direction is maintained in the CD14_M-only sensitivity analysis.
- **PARTIAL:** the association is present but fails the specificity or donor-consistency criteria.
- **FAIL:** no association. The signature then marks an SPP1/TREM2/GPNMB/lysosomal state in
  decidual macrophages that is not linked to TNFSF12 in these data.

Even a PASS supports only "a TWEAK-associated macrophage state is present and linked to
TNFSF12 detection". Any Level 3 analysis would need separate approval and gestational-age
control. Level 3 donor co-occurrence would not be spatial colocalisation.
