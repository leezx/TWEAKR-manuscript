# Fig. 1 (A3a panel) legend (draft; panel letter assigned at Figure 1 assembly)

**Canonical CSC and oncofetal-associated programmes relate differently to developmental potency estimated from gene expression.**

**What is plotted.**

- Each point is the pooled within-sample Spearman correlation between a programme score and predicted developmental potency.
- Programme scores are UCell scores.
- Predicted potency comes from two independent algorithms:
  - CytoTRACE2 (filled circles);
  - SCENT-CCAT (open circles).
- The cells are tumour-derived epithelial cells from 216 patients in 13 cohorts of treatment-naive primary CRC. They are tumour-derived epithelium, not CNV-confirmed malignant cells.
- Bars show 95% confidence intervals.

**Pooling.**

- Correlations were Fisher z-transformed.
- They were averaged first within each patient, then within each cohort.
- Cohort estimates were combined by random-effects meta-analysis (REML with Hartung–Knapp adjustment).

**Adjustment.**

- Left: before adjustment.
- Right: after adjustment, i.e. partial Spearman correlation controlling for log UMI count, log detected genes, mitochondrial fraction, and S and G2M cell-cycle scores.

**Statistics.**

- Before adjustment, every association was positive for both algorithms. The pre-specified families (five programmes per algorithm) had Benjamini–Hochberg-adjusted *P* < 0.002.
- After adjustment:
  - proCSC and Lgr5CSC remained positive with both algorithms;
  - revCSC and YAP core were close to zero or slightly negative;
  - Extended CIOC remained positive with CytoTRACE2 but not with SCENT-CCAT (95% CI −0.012 to 0.087).
- CytoTRACE2 and SCENT-CCAT estimates were not formally compared with each other.

**Caveat.** The scores are transcriptome-derived estimates of developmental potency. They do not measure cellular plasticity or the capacity for state transition.

Cohort-level estimates, depth-matched and subset analyses, the stricter ECOS-38 oncofetal signature, MSI strata, TNFRSF12A and macrophage TNFSF12 analyses are shown in Extended Data.
