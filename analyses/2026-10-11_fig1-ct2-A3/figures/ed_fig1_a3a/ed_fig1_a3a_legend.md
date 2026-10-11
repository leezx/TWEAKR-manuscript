# Extended Data Fig. (A3a companion) legend (draft)

**Robustness of programme–potency associations in CRC epithelium.**

**a, Cohort-level and pooled estimates.**
- Grey dots: cohort-level within-sample Spearman ρ between programme scores and CytoTRACE2 (top) or SCENT-CCAT (bottom), before and after adjustment (13 cohorts).
- Diamonds with bars: pooled ρ with 95% CI (REML with Hartung–Knapp adjustment).
- Heterogeneity was high: I² was 0.77–0.88 for CytoTRACE2 and 0.91–0.97 for SCENT-CCAT.

**b, Pooled ρ across pre-specified analyses.**
- Coloured cells have a 95% CI that excludes zero; white cells have a 95% CI that includes zero.
- The vertical line separates the five pre-specified programmes from the descriptive signatures.
- Analyses shown:
  - raw model score, i.e. CytoTRACE2 before smoothing;
  - depth-matched: cells downsampled to a cohort-specific UMI target, with programme scores recomputed on the same downsampled counts; mean of five seeds;
  - F1-clean: cells without a cross-lineage marker conflict;
  - non-cycling: G1 cells;
  - excluding Khaliq: shown only for the oncofetal signatures, because Extended CIOC was selected partly using Khaliq data.
- *Malignant subset: the high-confidence CNV-supported malignant subset. It covers 6 cohorts and 61 patients and is enriched for MSS tumours.

**c, MSI strata.** CytoTRACE2, before adjustment. Patients with unknown MSI status are not shown.

**d, TNFRSF12A.**
- Adjusted within-sample Spearman ρ between TNFRSF12A expression (log1p CPM) and each programme, CytoTRACE2 or SCENT-CCAT.
- 8 cohorts and 140 patients; samples in which TNFRSF12A did not vary were not estimable.
- †TNFRSF12A is one of the 32 revCSC genes. "revCSC without TNFRSF12A" is a post hoc check of this self-inclusion.

**e, Macrophage TNFSF12 versus epithelial Extended CIOC.**
- Within-cohort Spearman ρ across samples between macrophage TNFSF12 pseudobulk (log1p CPM; ≥30 macrophages per sample) and the sample median of epithelial Extended CIOC scores.
- Filled symbols: all samples. Open symbols: patient-level means over samples with ≥100 epithelial cells.
- Symbol size reflects the number of samples or patients.
- Blue: pooled ρ with 95% CI.
- No detectable association: −0.007 (−0.192 to 0.179) for all samples; −0.015 (−0.256 to 0.227) at patient level.

**f, proCSC–revCSC co-activation.**
- Within each sample, a cell is "high" for a programme if it is at or above that sample's 75th percentile.
- Plotted value: the median, across samples, of the observed co-high share divided by the share expected under independence.
- Symbol size reflects the number of samples.
- This is a descriptive measure of relative co-expression. It is not evidence of state transition.

All associations are transcriptome-derived and do not measure cellular plasticity.
