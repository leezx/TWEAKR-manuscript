# Fig. 1c legend (draft; wording follows the frozen claim of 2026-10-11)

**c, Proliferative and revival–oncofetal epithelial programmes are differentially associated with predicted developmental potency in CRC.**

- **Left (programme architecture).**
  - Density of within-sample percentile ranks of the proCSC and revCSC programme scores (UCell; Qin et al. signatures) for 285,141 tumour-specimen-derived epithelial cells from 222 treatment-naive primary CRC patients in 13 studies.
  - Each patient contributes equal total weight. Colour shows density relative to a uniform distribution (log2 scale, truncated at ¼ and 4).
  - Dashed lines mark the 75th within-sample percentile used to define the operational strata (pro-dominant, rev-dominant, hybrid-high and neither-high). Cells assigned to the absorptive differentiated-like lineage form the reference group and are not assigned to strata; they are included in the density.
  - Bars show the annotation composition of the pro-dominant, rev-dominant and hybrid-high strata (cell numbers below). Lineage was transferred from the Pelka et al. reference by a patient-grouped cross-validated classifier and audited with marker modules.
    - "Stem/TA-like (unverified)": cells predicted as Stem/TA-like, a class that did not pass the pre-specified lineage audit.
    - "Unresolved": below the classifier confidence thresholds.
    - "Transitional/rare (not audited)": transitional and rare classes, which were not module-audited.
- **Middle (within-patient contrasts).**
  - Differences in CytoTRACE2-predicted developmental potency between programme-defined strata and the absorptive differentiated-like reference.
  - Estimation: the difference of group medians within each sample, then the median per patient, then the mean per study, pooled across studies by REML random-effects meta-analysis with the Hartung–Knapp adjustment. Points and bars show pooled estimates and 95% CIs.
  - n = patients in studies with ≥ 5 eligible patients. "Studies > 0" = studies with a positive pooled within-study mean difference.
  - Eligibility: samples with ≥ 30 cells in each stratum compared and ≥ 50 reference cells.
  - The three upper contrasts form the pre-specified primary family, with Holm-adjusted P values. The contrast restricted to Cycling Stem/TA cells is a planned sensitivity analysis (open symbol). The shaded row is the direct pro-dominant versus rev-dominant contrast.
- **Right (continuous model).**
  - Within-sample partial Spearman correlation between CytoTRACE2 score and each programme score, adjusted for the other programme, log UMI, log detected genes, mitochondrial fraction, S and G2M scores, and lineage/annotation status.
  - Pooled as Fisher z (sample, then patient, then study; REML with Hartung–Knapp) over 216 patients in 13 studies with ≥ 100 epithelial cells per sample. No reference group is required. Points and bars show the pooled estimate and 95% CI.
- **Notes.**
  - CytoTRACE2 estimates transcriptome-derived developmental potency and does not measure plasticity.
  - Strata are operational, programme-defined groups, not functionally validated cancer stem cell populations.
  - Prediction intervals, study-level estimates and all sensitivity analyses are in Extended Data. These include depth matching, covariate adjustment, alternative thresholds and references, mechanism-blinded signatures, MSI/MSS, CNV-positive cells, leave-one-study-out and SCENT-CCAT.
  - The sensitivity analyses were pre-specified; their implementation details were documented after the primary analysis.

Source data: `fig1c_source_ci_density.csv`, `fig1c_source_ci_composition.csv`, `fig1c_source_cii.csv`, `fig1c_source_ciii.csv`.
