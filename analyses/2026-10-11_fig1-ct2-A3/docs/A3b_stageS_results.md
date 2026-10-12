# A3b Stage S — results for final review (contract v0.3; identity_v1 limited GO)

- **Date:** 2026-10-12.
- **Code:** `a3b_ct2_prep.py`, `a3b_ct2_check.py` and `a3b_estimands.py`. Run commit `dbcc966`; the only change after deployment was a path fix for the depth-matched score folder.
- **Public tables:** `tables/a3b_stageS/`.
- **Delta definition:** tumour − normal (normal–primary) or Post − Pre (pre/post), on the 0–1 CytoTRACE2 (CT2) potency score.
- **Unit and pooling:** each patient's value is the median of sample medians, computed per side. Studies are then pooled by REML with Hartung–Knapp. The prediction interval uses k−2 df.

## 0. Process disclosure

1. **Smoke test.** A run on the completed normal–primary scores (pre/post was then ~30% scored) caught a path bug: depth-matched scores were read from `scores_ds_*` instead of `scores_*`.
   - The fix changed only that path.
   - The normal–primary numbers from the smoke test are identical to the final ones.
   - No inclusion, depth, model or endpoint rule was changed after any result was seen.
2. **Reruns.** Five CT2 tasks failed on a transient out-of-memory error (`mcfork` in R): one original-depth file (Qin XFZ32_PRET) and four Qin pre/post depth-matched seeds. They were rerun with more memory, unchanged otherwise. The final run is 447/447, 1,455/1,455 and 960/960 files scored.

## 1. QC (before estimands)

| Check | Result |
|---|---|
| CT2 scoring (`A3b_ct2_qc.tsv`) | Main 447/447 (1,504,693 cells); normal–primary depth-matched 1,455/1,455 (5 seeds); pre/post 960/960 |
| Equality with Fig. 1b full-run scores (`A3b_ct2_fig1b_equality.tsv`) | 189/189 overlapping tumour samples; identical cell sets; max \|Δ\| 2×10⁻¹³ (whole), 0 (intrinsic) |
| Join (`A3b_stageS_join_qc.tsv`) | Normal–primary: 222,629 epithelial cells, 172,643 retained after depth matching, UCell 222,353, 0 duplicates. Pre/post: 167,243 / 126,548 / 167,210 / 0 |

## 2. Primary: E1 normal–primary (depth-matched CT2)

| Estimand | k | n patients | Estimate | 95% CI | p | 95% PI | I² | Same sign | LOSO range |
|---|---|---|---|---|---|---|---|---|---|
| **E1 (primary)** | 6 | 86 | **+0.057** | −0.007 to 0.120 | 0.069 | −0.107 to 0.221 | 0.90 | 6/6 | 0.035–0.067 |
| (i) original depth | 7 | 98 | +0.044 | −0.007 to 0.094 | 0.078 | −0.071 to 0.158 | 0.90 | 7/7 | 0.030–0.051 |
| (ii) raw score, depth-matched | 6 | 86 | +0.048 | −0.033 to 0.130 | 0.19 | −0.171 to 0.268 | 0.93 | 6/6 | 0.019–0.058 |
| (iii) adjusted (side + log UMI + log genes + mito + S + G2M) | 6 | 86 | +0.039 | −0.003 to 0.082 | 0.062 | −0.066 to 0.144 | 0.84 | 6/6 | 0.025–0.046 |

Per-study E1 values (`A3b_study.tsv`), tumour − normal, with 95% CIs:

| Study | n | Δ | 95% CI |
|---|---|---|---|
| Chen | 17 | +0.014 | 0.003–0.025 |
| Lee | 12 | +0.051 | 0.021–0.080 |
| **MUI** | 12 | **+0.193** | 0.123–0.263 |
| Pelka | 30 | +0.044 | 0.034–0.055 |
| Qian | 5 | +0.022 | −0.011–0.054 |
| Uhlitz | 10 | +0.050 | 0.025–0.075 |

**Reading:**
- All 6 studies are positive, and 5/6 study CIs exclude 0.
- The pooled CI includes 0. With k=6 and Hartung–Knapp, the between-study variance driven by MUI (Δ≈0.19, about 4× the others) widens the interval.
- Under the frozen rule, E1 is **not significant** (p=0.069).
- All three sensitivities agree in direction and magnitude, so depth and QC covariates do not explain the shift.

## 3. Secondary (normal–primary)

**Programmes (UCell, original depth; BH across 4):**

| Programme | k / n | Estimate | 95% CI | p_BH | Same sign | 95% PI |
|---|---|---|---|---|---|---|
| proCSC | 7 / 98 | +0.056 | 0.018–0.094 | 0.015 | 7/7 | −0.053 to 0.165 |
| revCSC | 7 / 98 | +0.028 | 0.011–0.045 | 0.015 | 7/7 | −0.017 to 0.073 |
| ExtCIOC | 7 / 98 | +0.019 | 0.013–0.025 | 0.001 | 7/7 | 0.002–0.036 |
| YAPcore | 7 / 98 | +0.007 | −0.006–0.020 | 0.22 | 5/7 | −0.021 to 0.036 |

**E1-L (Axis-L v0.3a class, depth-matched CT2; Pelka excluded):**

| Class | k / n | Estimate | 95% CI |
|---|---|---|---|
| Absorptive differentiated-like | 4 / 36 | +0.033 | −0.025 to 0.090 |
| Cycling Stem/TA | 4 / 37 | +0.043 | 0.002–0.084 (p=0.044) |

**E3 (descriptive, tumour-evidence vs normal):**

| Study | n | Δ | 95% CI | Patients positive |
|---|---|---|---|---|
| Lee | 5 | +0.060 | 0.024–0.097 | 5/5 |
| Pelka | 6 | +0.038 | 0.014–0.062 | 6/6 |

## 4. Pre/post (per cohort, exploratory; Post − Pre, tumour side)

| Estimand | Qin (surgical Post, TRG0 excluded) | Chen (GEO-annotated Post) |
|---|---|---|
| E1-pp, depth-matched | n=18: −0.014 (−0.031 to 0.004), Wilcoxon p=0.13 | n=10: −0.008 (−0.032 to 0.017), p=0.77 |
| (i) original depth | n=22: −0.035 (−0.068 to −0.003), p=0.004 | n=11: −0.029 (−0.079 to 0.021) |
| (ii) raw, depth-matched | −0.018 (−0.037 to 0.001) | −0.004 |
| (iii) adjusted | −0.009 (−0.026 to 0.008) | −0.004 |
| proCSC | −0.035 (−0.065 to −0.004) | −0.030 (−0.078 to 0.019) |
| revCSC / ExtCIOC / YAPcore | −0.014 / −0.003 / −0.012 (all CIs include 0) | +0.003 / −0.004 / +0.010 |

**Reading:**
- The primary pre/post contrast, depth-matched CT2, is null in both cohorts.
- The original-depth decrease in Qin shrinks after depth matching (−0.035 → −0.014) and after covariate adjustment (−0.009). This is consistent with a depth or tissue-quality difference between biopsy and resection.

## 5. Questions for review

1. **E1 wording.** E1 misses the frozen threshold (p=0.069), but the direction is 6/6, LOSO stays positive and the sensitivities agree. Is "directionally consistent but not statistically supported higher CT2 potency in tumour vs matched normal epithelium" the right ceiling? Should MUI's large effect be described, with no post-hoc exclusion?
2. **Programmes.** proCSC, revCSC and ExtCIOC are BH-significant, 7/7 same-sign, but with wide PIs (only ExtCIOC's PI excludes 0). These are tissue-context differences, not identity-resolved. Is wording at the level of "tumour-specimen epithelium" acceptable?
3. **E1-L Cycling Stem/TA** (p=0.044, k=4). Should it be reported as a secondary without multiplicity claims?
4. **Pre/post.** Report as "no depth-robust change in CT2 potency after neoadjuvant therapy in either cohort", with the original-depth Qin decrease shown as depth-sensitive?
5. **Chen P02.** P02's naive samples are in the normal–primary branch (frozen eligibility; Chen 18 pre-match). P02 was excluded from pre/post as a second-line patient, so its "naive" samples may follow first-line chemotherapy. Keep as frozen, or add a descriptive E1 sensitivity excluding P02? Its patient Δ is −0.007; the Chen median is +0.022 (n=17).
6. **GO for figures?** Proposed ED panel: E1 forest (studies + pooled + PI) with sensitivities (i)–(iii), the programme forest, and the pre/post per-cohort paired plot.
