# A3a results: developmental programmes × CytoTRACE2 in CRC epithelium (frozen contract v0.2)

- **Date:** 2026-10-11.
- **Contract:** `A3a_contract.md` (frozen; approved text at 9104fc8).
- **Code:** commit 13a8c3e, plus two output-only fixes, in `a3a_ucell.R` only:
  - samples with fewer than 50 cells are skipped (both affected samples had 1 epithelial cell and are ineligible under §1);
  - an empty output is written as a valid gzip.
  - No estimand, covariate, threshold or set was changed.
- **SGE jobs:**
  - 3655116: export, 13/13 studies;
  - 3655117 + 3655125: UCell, 360/360 samples with epithelium;
  - 3655127: statistics.
- **Depth regeneration:** 1,800 of 1,800 regenerated depth-matched matrices are identical to the Fig. 1b ds exports, element by element.
- **Tables:** `tables/a3a/` holds public study-level and pooled tables only.
- **Not run:** CCAT. The secondary family is technically pending (§3 gate); no substitute was used.

**Eligibility.**
- 216 patients from 13 studies at ≥100 epithelial cells per sample; 222 patients at ≥50.
- Gene-set coverage was ≥70% everywhere (Atlas gene space: Lgr5CSC 0.741; model features: Placenta 0.707). The rule therefore selects **`ds_both`** as the depth perturbation. `ds_ct2_fixed_programme` is also reported.

## 1. Primary family: unadjusted ρ with CT2 final, BH over 5 sets

Pooled across studies by REML + Hartung–Knapp, then back-transformed from Fisher z.

| Programme | ρ (95% CI) | 95% PI | I² | Studies with same sign | LOSO | BH p |
|---|---|---|---:|---|---|---|
| proCSC | **+0.611** (0.563, 0.656) | 0.434, 0.743 | 0.85 | 13/13 | 0.601–0.621 | <1e-9 |
| Lgr5CSC | **+0.348** (0.291, 0.403) | 0.146, 0.522 | 0.82 | 13/13 | 0.335–0.364 | 9e-8 |
| Extended CIOC | **+0.303** (0.239, 0.365) | 0.082, 0.496 | 0.80 | 13/13 | 0.290–0.316 | 7e-7 |
| revCSC | **+0.203** (0.131, 0.273) | −0.051, 0.433 | 0.88 | 12/13 | 0.188–0.221 | 7e-5 |
| YAP core | **+0.104** (0.049, 0.158) | −0.074, 0.276 | 0.77 | 11/13 | 0.086–0.120 | 0.0014 |

## 2. Mandatory robustness

| Programme | Adjusted ρ | Raw score, unadjusted | Raw score, adjusted | ds_both, unadjusted | ds_both, adjusted | §5 classification |
|---|---|---|---|---|---|---|
| proCSC | +0.311 (0.272, 0.349) | +0.636 | +0.355 | +0.401 (0.319, 0.476) | +0.225 | **robust** |
| Extended CIOC | +0.111 (0.076, 0.146) | +0.255 | +0.083 | +0.128 (0.052, 0.204) | +0.093 | **robust** |
| Lgr5CSC | +0.081 (0.040, 0.121) | +0.327 | +0.080 | +0.100 (0.025, 0.174) | +0.062 (0.002, 0.121) | **robust** (the depth-matched adjusted CI only just excludes 0) |
| revCSC | −0.026 (−0.060, 0.009) | +0.130 | −0.074 | −0.080 (−0.114, −0.044) | −0.062 | **positive, but substantially attenuated after adjustment** for transcriptomic complexity and cell-cycle covariates; negative after depth matching |
| YAP core | −0.034 (−0.068, −0.001) | +0.020 (ns) | −0.099 | −0.087 (−0.131, −0.043) | −0.066 | **positive, but substantially attenuated after adjustment**; negative after adjustment and after depth matching |

- All CIs in this table are 95%, and k = 13 for every estimate.
- Patients: 216 for the adjusted and raw-score estimates, 212 for ds_both.
- `ds_ct2_fixed_programme` gives the same pattern: proCSC +0.412, Extended CIOC +0.114, Lgr5CSC +0.091, revCSC −0.050, YAP core −0.055.

**Other sensitivity analyses (unadjusted / adjusted ρ):**

| Analysis | proCSC | revCSC | Lgr5CSC | Extended CIOC | YAP core |
|---|---|---|---|---|---|
| ≥50 cells (222 patients) | +0.612 / — | +0.196 / — | +0.349 / — | +0.304 / — | +0.101 / — |
| F1-clean | +0.611 / +0.305 | +0.213 / −0.026 | +0.353 / +0.078 | +0.316 / +0.114 | +0.111 / −0.035 |
| Non-cycling (201 patients) | +0.447 / +0.274 | +0.217 / +0.002 | +0.291 / +0.076 | +0.287 / +0.137 | +0.076 / −0.043 |
| Malignant subset (6 studies / 61 patients) | +0.564 / +0.305 | +0.145 / −0.029 | +0.300 / +0.107 | +0.169 / +0.034 (ns) | +0.065 / −0.028 |

**Excluding Khaliq** (Extended CIOC was selected partly on Khaliq):
- Extended CIOC +0.294 unadjusted / +0.101 adjusted (12 studies). Unchanged.

**MSI (descriptive, unadjusted):**

| Programme | MSS (11 studies, 146 patients) | MSI-H (5 studies, 55 patients) |
|---|---|---|
| proCSC | +0.595 | +0.648 |
| revCSC | +0.210 | +0.074 (ns) |
| Extended CIOC | +0.303 | +0.181 |
| YAP core | +0.123 | +0.012 (ns) |

## 3. Secondary sets (descriptive)

| Set | Unadjusted | Adjusted | ds_both | Note |
|---|---|---|---|---|
| ECOS-38 (oncofetal validation set) | +0.121 (0.068, 0.173) | +0.016 (ns) | −0.009 (ns) | attenuated: the stricter oncofetal set does not keep the Extended CIOC association |
| YAP fetal/oncofetal effectors | +0.163 | −0.058 | −0.138 | attenuated, then negative |
| Placenta trophoblast | +0.148 | −0.076 | −0.138 | attenuated, then negative |

## 4. Programme contrasts (descriptive, Fisher-z scale, CT2 final)

Each contrast is a per-patient difference, then pooled.

| Contrast | Unadjusted Δz | Adjusted Δz |
|---|---|---|
| revCSC − proCSC | −0.48 (−0.58, −0.39) | −0.34 (−0.40, −0.29) |
| Extended CIOC − proCSC | −0.37 (−0.47, −0.26) | −0.19 (−0.24, −0.14) |
| YAP core − proCSC | −0.59 (−0.69, −0.49) | −0.36 (−0.41, −0.30) |

proCSC is more strongly coupled to CT2 than any other programme, within patients and in every pooled comparison.

## 5. Co-activation (Extended Data, descriptive)

Within each sample, "high" means at or above that sample's 75th percentile for the programme. The expected co-high share under independence is 6.25%.

- **Co-high share:** the median per-study share of proCSC-high/revCSC-high cells is 4.3–11.3%.
- **CT2 by group, per-study medians:**
  - co-high cells (0.13–0.58) are similar to proCSC-only cells (0.12–0.59);
  - revCSC-only cells (0.10–0.32) are only slightly above neither-high cells (0.09–0.16).
- This is relative co-expression, not state transition.

## 6. P2 (TWEAKR)

- **Gate passed:** TNFRSF12A is detected in 18–61% of epithelial cells in every study (gate: ≥5% in ≥3 studies).
- Many samples are non-estimable because the TNFRSF12A CPM has IQR = 0 (sparse detection). As a result, 8 studies / 140 patients are pooled.

| Comparison | Unadjusted ρ | Adjusted ρ |
|---|---|---|
| TNFRSF12A vs CT2 final (P2 primary) | +0.155 (0.085, 0.223), 8/8 studies | −0.008 (−0.023, 0.006) |

Positive, but substantially attenuated after adjustment.

**Descriptive: TNFRSF12A vs programmes (unadjusted / adjusted):**

| Programme | Unadjusted | Adjusted |
|---|---|---|
| revCSC | +0.463 | **+0.327** |
| YAP fetal | +0.396 | +0.249 |
| Placenta | +0.367 | +0.195 |
| YAP core | +0.334 | +0.228 |
| Extended CIOC | +0.329 | +0.179 |
| ECOS-38 | +0.268 | +0.184 |
| proCSC | +0.200 | **+0.008 (ns)** |
| Lgr5CSC | +0.179 | **−0.049** |

TNFRSF12A tracks the revival/YAP/oncofetal/placenta axis, not the proCSC/Lgr5 axis.

## 7. P3 (macrophage TNFSF12)

- **Gate passed:** TNFSF12 is detected in ≥5% of macrophages in 12/13 studies; Uhlitz 0.3%.
- **Result:** across samples, macrophage TNFSF12 pseudobulk vs the epithelial Extended CIOC sample median is pooled ρ **−0.007 (−0.192, 0.179)**, k = 12, I² 0.32.
- **Conclusion:** no detectable sample-level co-occurrence.

## 8. Interpretation (within the §5 rules)

1. **proCSC, Lgr5CSC and the broad oncofetal programme (Extended CIOC)** are robustly associated with higher CT2-predicted developmental potential. The associations hold:
   - after adjustment for complexity and cell cycle;
   - on the raw model score;
   - after depth matching;
   - in all 13 studies.

   proCSC is by far the strongest.
2. **revCSC and YAP core** are positively associated before adjustment. The association is substantially attenuated after adjustment for transcriptomic complexity and cell-cycle covariates, and turns negative after depth matching. This replicates the DS-010 revCSC pattern in 13 independent studies. The stricter ECOS-38 set, YAP fetal effectors and the placenta set behave the same way.
3. **TNFRSF12A** is coupled to the revCSC/YAP/oncofetal axis (adjusted ρ +0.33 with revCSC) and not to proCSC. Its link to CT2 disappears after adjustment.
4. **Macrophage TNFSF12** shows no sample-level co-occurrence with the epithelial oncofetal programme.
5. **CCAT is not yet available.** Under §0, CT2 limitations can be invoked for the revCSC/YAP null only if CCAT disagrees. Until then, the statement is: "revCSC/YAP programmes are not associated with higher CT2-predicted developmental potential independently of transcriptomic complexity".
