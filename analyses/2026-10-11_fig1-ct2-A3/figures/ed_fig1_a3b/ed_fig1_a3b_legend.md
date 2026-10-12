# Extended Data Fig. (A3b) | Paired normal–tumour and neoadjuvant comparisons of predicted developmental potential and stem-cell programmes in colorectal cancer epithelium

**Summary.** Across six studies, tumour-specimen epithelium had consistently positive but heterogeneous differences in CytoTRACE2-predicted developmental potential relative to paired adjacent-normal epithelium, without conclusive pooled evidence after depth matching. proCSC, revCSC and Extended CIOC programme scores were higher in tumour-specimen epithelium; YAP core was not. Exploratory neoadjuvant cohorts showed no statistically supported depth-matched change.

**a, Paired normal–primary comparison.**
- **Measure:** the patient-level difference in CytoTRACE2 potency (0–1 scale) between tumour-specimen and adjacent-normal epithelium. Epithelium is all L1/F1-qualifying epithelial cells.
- **Depth matching:** each sample was downsampled to a study-specific UMI target T_s, which is the lower of the two sides' 25th-percentile epithelial UMI counts. Scores are averaged over five seeds.
- **Summaries:** each patient value is the median of sample medians per side; samples need ≥100 cells.
- **Display:**
  - Grey points: patients.
  - Black squares and lines: study mean ± 95% CI (t distribution).
  - Blue: pooled random-effects estimate (REML with Hartung–Knapp) with its 95% CI; the capped whisker on the primary estimate is the 95% prediction interval (k−2 df).
- **Pooled primary:** k = 6 studies, n = 85 patients.
- **Studies with fewer than 5 eligible patients** (Joanito, Khaliq) are not pooled and not shown.
- **Prespecified sensitivity analyses (open diamonds):**
  - (i) original depth (k = 7, n = 97);
  - (ii) raw model score, depth-matched;
  - (iii) patient-level linear model of depth-matched CytoTRACE2 on side, log UMI, log genes, mitochondrial fraction and S and G2/M scores.
- **Frozen Atlas-label analysis** (n = 86): includes patient Chen P02. P02 is excluded from the primary cohort because, as a second-line metastatic patient, its pre-anti-PD-1 samples followed prior systemic therapy. This was inferred from the treatment line and sample stage; the per-sample treatment history was not available.

**b, Epithelial programme scores.**
- **Measure:** UCell score difference, tumour − adjacent normal, at original depth; k = 7, n = 97.
- **Display:** grey points are study means; blue shows the pooled estimate with 95% CI and 95% PI (capped whiskers).
- **Multiplicity:** P values are Benjamini–Hochberg adjusted across the four prespecified programmes.
- **Interpretation:** these are tissue-context differences. They are not attributed to malignant cells, because epithelial identity calls could not reliably separate malignant from normal epithelium.

**c, Within Axis-L lineage class (secondary, exploratory).**
- **Measure:** depth-matched CytoTRACE2 difference within cells assigned to each class by the frozen Fig. 1c Axis-L classifier (maximum probability ≥ 0.70 and margin ≥ 0.20). Patients need ≥30 cells of the class per side.
- **Exclusion:** Pelka is excluded because it overlaps the classifier's training data.
- **Statistics:** P values are nominal and not adjusted for multiplicity.

**d, Neoadjuvant cohorts (exploratory, per cohort).**
- **Measure:** patient-level Post − Pre difference in tumour-side epithelium.
- **Display:**
  - Grey points: depth-matched patient differences.
  - Blue: depth-matched primary estimate, mean ± 95% CI, with Wilcoxon signed-rank P.
  - Open diamonds: original-depth scores in the same patients, and sensitivities (ii) and (iii).
- **Qin 2023 (chemotherapy):**
  - Pre samples are colonoscopic biopsies; Post samples are surgical resections. Endoscopic Post samples are excluded.
  - Patients with complete response (TRG0) are excluded.
  - Specimen type and processing are confounded with time point.
- **Chen 2024 (anti-PD-1):** Post is the last GEO-annotated visit. Whether each Post sample is a surgical specimen was not verified.

**Statistics, replicates and abbreviations.**
- **Units:** n is the number of patients, the independent unit; cells are not treated as replicates.
- **Tests:** all tests are two-sided. CI, confidence interval; PI, prediction interval.
- **Abbreviations:** REML, restricted maximum likelihood; BH, Benjamini–Hochberg; UMI, unique molecular identifier; TRG, tumour regression grade. Programme gene sets (proCSC, revCSC, Extended CIOC, YAP core) are as defined for Fig. 1 A3a.
- **Source data:** `ed_fig1_a3b_source_a.csv` to `ed_fig1_a3b_source_d.csv`.
