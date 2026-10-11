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

## 8. Interpretation (approved wording, results review 2026-10-11)

**Review status:**

| Item | Decision |
|---|---|
| P1 primary tests | APPROVED |
| P1 robust classification | APPROVED; robustness is stated for Extended CIOC-222 only |
| revCSC / YAP sign reversal | APPROVED; must be written as reversal, not only attenuation |
| P2 | APPROVED as descriptive |
| P3 | CONDITIONAL on the QC in §9 |
| Co-activation | APPROVED, with the expected share clarified |
| CCAT | PENDING its technical gate |
| Figure production | GO for P1 |

1. **Core finding.** Canonical proCSC is strongly and consistently coupled to CT2. Revival- and YAP-associated programmes show much weaker relationships that are sensitive to adjustment or depth: revCSC and YAP core are positive unadjusted but **negative after depth matching** (revCSC −0.080, YAP core −0.087; both CIs below 0), and YAP core is also negative after adjustment. This does not show lower true plasticity of revCSC/YAP cells.
2. **Oncofetal signatures diverge.** Associations with CT2-predicted developmental potential varied substantially across oncofetal gene signatures:
   - the broader Extended CIOC programme kept a modest positive association after adjustment and depth perturbation;
   - the more restricted ECOS-38 signature did not;
   - in the high-confidence malignant subset, the adjusted Extended CIOC association was +0.034 (CI −0.059 to 0.126).

   "Oncofetal programmes are robustly associated with higher developmental potential" is **not** an allowed statement.
3. **P2.** TNFRSF12A expression was more strongly associated with revival, YAP-associated and oncofetal transcriptional programmes than with canonical proCSC signatures. Its modest association with CT2-predicted developmental potential was lost after adjustment for transcriptomic complexity.
   - These are stronger *observed* associations; no formal paired test or equivalence test was done.
   - P2 covers 8 studies / 140 patients where TNFRSF12A varied enough to estimate a correlation.
   - This is a transcriptional-state association. It does not show causality, YAP dependence or state transition.
   - TNFRSF12A is one of the 32 revCSC genes; see the post-hoc check in §9.
4. **P3.** No detectable sample-level association. This does not refute a macrophage–TWEAKR relationship, because samples cannot measure spatial proximity or ligand activity.
5. **CCAT.** Until CCAT is done, all A3a conclusions are CT2-specific. Even a positive unadjusted CCAT result would not, on its own, show that CT2 misses revival plasticity.

## 9. Post-hoc checks requested by the review (labelled post hoc; frozen sets unchanged)

1. **revCSC without TNFRSF12A** (31 genes), to address self-inclusion. Tested:
   - TNFRSF12A vs revCSC_noTN;
   - revCSC_noTN vs CT2.
2. **P3:**
   - enforce ≥100 epithelial cells per sample;
   - run a patient-level version, because the sample-level SE ignored within-patient correlation.
3. **Co-activation:** observed co-high share against the per-sample expected share, P(pro-high) × P(rev-high).

Results (SGE 3655128/3655129; `tables/a3a_posthoc/`):

| Check | Unadjusted | Adjusted |
|---|---|---|
| TNFRSF12A vs revCSC without TNFRSF12A (8 studies / 140 patients) | +0.378 (0.298, 0.451) | **+0.213 (0.142, 0.282)**, 8/8 studies |
| revCSC without TNFRSF12A vs CT2 (216 patients) | +0.203 | −0.025 |

- **Self-inclusion:** with TNFRSF12A in the set, the adjusted value was +0.327. Self-inclusion explains part of that, but the TNFRSF12A–revival association remains clearly positive. revCSC × CT2 is unchanged.
- **P3 with ≥100 epithelial cells:** ρ +0.003 (−0.207, 0.212); 11 studies, 271 samples.
- **P3 at patient level:** ρ −0.015 (−0.256, 0.227); 11 studies, 170 patients.
- The P3 null holds under both QC versions.
- **Co-activation:** the per-sample expected share is 6.26% (ties are negligible). Observed / expected per study (median) is 0.69–1.81 and is above 1 in 10 of 13 studies, but below 1 in Joanito (0.69), Li (0.86) and Pelka (0.92). There is no consistent co-activation beyond independence.

## 10. CCAT technical pilot (A3a secondary proxy; gate for review)

| Item | Result |
|---|---|
| Implementation | SCENT 1.0.3 `CompCCAT(exp.m, ppiA.m = net13Jun12.m)`, as in the DS-010 CSCPOT run. Normalisation to 10,000 per cell, then log2(x+1) on a sparse matrix. One-to-one SYMBOL→ENTREZ mapping; this A3a version also drops ambiguous symbols, which DS-010 did not (DS-010 dropped duplicated Entrez only) |
| Network coverage | 24,021 genes mapped; **8,403** overlapping net13Jun12 (gate ≥5,000) |
| Output checks | finite values, \|CCAT\| ≤ 1, one per cell; asserted |
| Repeat stability | two runs gave **identical** values on all 3 pilot samples (CompCCAT is deterministic) |
| Pilot samples | smallest (102 cells), median (649) and largest (4,586) eligible samples |
| Resources | about 50 s wall time per sample; peak virtual memory 35–37 GB (independent of cell number, dominated by loading the network and annotation); 24 GB `m_mem_free` was sufficient |
| DS-010 | 26/26 samples, 8,283 network genes in every sample, buckets 3–5 min, ≤8.3 GB |
| Full run plan | 360 samples × about 1 min; then the frozen secondary family (5 P1 sets × CCAT, unadjusted, BH) plus the adjusted estimate, with the same aggregation |


## 11. CCAT secondary family (complete; SGE 3655132/3655133, commit 1c5f048)

- **Run:** 360/360 samples; all 361 tasks exit 0; maxvmem ≤41 GB.
- **Scope:** frozen secondary family = 5 P1 sets × CCAT (unadjusted, BH), with the adjusted estimate as mandatory robustness. Aggregation is identical to CT2. CCAT has no raw-score or depth variants.
- **Tables:** `tables/a3a_ccat/`.
- **Sample:** 216 patients / 13 studies; TNFRSF12A: 8 studies / 140 patients.

| Programme | CT2 unadjusted | **CCAT unadjusted** (BH) | CT2 adjusted | **CCAT adjusted** |
|---|---|---|---|---|
| proCSC | +0.611 | **+0.728** (0.690, 0.761), 13/13 | +0.311 | **+0.415** (0.350, 0.475), 13/13 |
| Lgr5CSC | +0.348 | **+0.566** (0.498, 0.627), 13/13 | +0.081 | **+0.158** (0.080, 0.234), 13/13 |
| Extended CIOC | +0.303 | **+0.425** (0.325, 0.515), 13/13 | +0.111 (0.076, 0.146) | **+0.037 (−0.012, 0.087)**, 9/13 |
| revCSC | +0.203 | **+0.446** (0.335, 0.545), 13/13 | −0.026 (ns) | **−0.015 (−0.073, 0.043)**, 8/13 |
| YAP core | +0.104 | **+0.251** (0.159, 0.338), 13/13 | −0.034 | **−0.039 (−0.065, −0.013)**, 11/13 |
| ECOS-38 | +0.121 | +0.208 | +0.016 (ns) | −0.039 (ns) |
| YAP fetal | +0.163 | +0.445 | −0.058 | +0.003 (ns) |
| Placenta | +0.148 | +0.415 | −0.076 | −0.022 (ns) |
| TNFRSF12A | +0.155 | +0.292 | −0.008 (ns) | +0.042 (0.011, 0.072) |

- **Primary CCAT family:** all 5 sets are positive with BH p < 1e-4.
- **Heterogeneity:** I² is 0.91–0.97, higher than for CT2. 95% PIs: revCSC −0.010 to 0.749, YAP core −0.088 to 0.537.
- **Cell sets (adjusted CCAT):** consistent across F1-clean, non-cycling and the malignant subset.
  - proCSC: +0.39 to +0.44;
  - revCSC: −0.02 to +0.01;
  - Extended CIOC: −0.02 to +0.06.

**CT2–CCAT comparison under §5** (written before any CCAT result):

1. **proCSC and Lgr5CSC:** concordant and robust under both proxies.
2. **revCSC and YAP core:** concordant.
   - Under both proxies the unadjusted association is positive.
   - After adjustment for transcriptomic complexity and cell cycle it is about 0 (revCSC) or slightly negative (YAP core).
   - The unadjusted association is **stronger** with CCAT (revCSC +0.45 vs +0.20). That extra coupling sits in the complexity-related component and disappears after adjustment under both algorithms.
   - Under the §0 rule, the revCSC/YAP null **cannot** be attributed to a CT2-specific defect.
3. **Extended CIOC:** same sign under both proxies, so this is not "proxy-dependent" under the §5 definition. However, the adjusted association that was robust with CT2 (+0.111) is **not reproduced** by CCAT (+0.037; CI includes 0).
4. **TNFRSF12A:** a small positive adjusted association with CCAT (+0.042), against none with CT2 (−0.008). Descriptive only.

**Consequence for the conclusions (final review, 2026-10-11: APPROVED, with wording revised):**
- **Supported by both algorithms:** proCSC and, more weakly, Lgr5CSC keep a positive adjusted association. CCAT has no depth-matched variant, so CCAT depth robustness is not shown.
- **revCSC / YAP:** under both proxies the associations are positive before adjustment and **sensitive to adjustment for transcriptomic complexity** (attenuated or reversed). The adjustment cannot tell whether this reflects mediation by complexity or a technical effect.
- **CT2-specific defect:** the hypothesis that a CT2-specific defect explains the revCSC/YAP result is **not supported**. This does not exclude other model biases shared by both algorithms.
- **Extended CIOC:** the broader programme kept a modest adjusted association with CytoTRACE2, but SCENT-CCAT did not independently support it. The two proxies were not formally tested against each other.
- **TNFRSF12A:** CCAT adjusted +0.042 vs CT2 −0.008 is a small, descriptive proxy-dependent association.
- **Allowed main claim:** canonical stemness and oncofetal-associated programmes show distinct relationships with transcriptome-derived developmental potency estimates. These associations do not measure cellular plasticity or state-transition capacity.
- **Discussion only:** the strong attenuation after covariate adjustment raises the possibility that transcriptomic complexity contributes to these relationships. The present analysis cannot separate technical variation from biologically meaningful transcriptional diversity.
- **Status:** A3a analysis branch CLOSED; figure production GO; A3b CT2 scoring still not authorised.
