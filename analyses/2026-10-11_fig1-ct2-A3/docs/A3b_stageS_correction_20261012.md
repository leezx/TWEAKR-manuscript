# A3b Stage S — minimal correction (response to `A3b_stageS_review_20261012.md`)

- **Date:** 2026-10-12.
- **Code:** `a3b_estimands.py`, the only file changed. No CT2 or UCell rescoring.
- **Tables:** corrected tables are in `tables/a3b_stageS/`; the first-run tables are kept unchanged in `tables/a3b_stageS/audit_v1_20261012/`.
- **Job:** SGE 3655611.

## 1. Changes (all eligibility filters; no threshold, depth target, identity or model change)

1. **Qin TRG0 (contract §3; reviewer finding).** TRG0 patients are removed from `E1_prematch`, `E1` and `E3` before any readout. This affects Qin original-depth and the four programmes: n 22 → 20 (XFZ07, XFZ48).
2. **Chen P02 clinical-eligibility amendment (dated 2026-10-12).**
   - **Evidence:**
     - Chen 2024 STAR Methods describes P02 as a second-line metastatic patient who died before surgery.
     - "Second-line" means P02 had received prior first-line systemic therapy.
     - The Atlas/GEO label "naive" refers only to anti-PD-1 exposure (stage Pre = before pembrolizumab).
     - So P02's normal–primary samples were taken after prior systemic therapy and fail the treatment-naive criterion.
   - **Caveat:** this is inferred from the definition of second-line. The supplementary per-patient regimen table (Fig. S1) is still not machine-readable here.
   - **Action:**
     - P02 is excluded from all normal–primary estimands.
     - The frozen Atlas-label E1 (86 patients, P02 included) is kept as the traceable sensitivity `E1_frozen_atlas_label_incl_P02`.
     - The decision was made from clinical status, before the corrected numbers were seen. P02's own Δ (−0.007) was not used.
3. **Same-class eligibility gaps found during the fix (disclosed):**
   - E1-L applied no patient-eligibility filter; it now uses E1 eligibility.
   - E3 applied no patient-eligibility filter; it now uses E3 eligibility.
   - E1-L n changes: Absorptive 36 → 35; Cycling Stem/TA 37 → 35.
   - E3 is unchanged.
4. **Descriptive addition (reviewer request):** `E1pp_desc_original_depth_same_patients`, the original-depth CT2 in exactly the E1-pp (depth-matched) patients.

## 2. Corrected results

### Normal–primary (pooled REML/HK)

| Estimand | k / n | Estimate | 95% CI | p | 95% PI | Same sign | LOSO |
|---|---|---|---|---|---|---|---|
| **E1 (primary; P02 excluded)** | 6 / 85 | **+0.057** | −0.006 to 0.120 | 0.068 | −0.106 to 0.220 | 6/6 | 0.035–0.067 |
| E1 frozen Atlas-label (P02 incl.) | 6 / 86 | +0.057 | −0.007 to 0.120 | 0.069 | −0.107 to 0.221 | 6/6 | 0.035–0.067 |
| (i) original depth | 7 / 97 | +0.044 | −0.007 to 0.094 | 0.079 | −0.072 to 0.159 | 7/7 | 0.030–0.051 |
| (ii) raw, depth-matched | 6 / 85 | +0.049 | −0.033 to 0.130 | 0.19 | −0.171 to 0.268 | 6/6 | 0.019–0.058 |
| (iii) adjusted | 6 / 85 | +0.039 | −0.002 to 0.081 | 0.060 | −0.065 to 0.144 | 6/6 | 0.025–0.046 |
| proCSC | 7 / 97 | +0.056 | 0.018–0.094 | p_BH 0.015 | −0.053 to 0.165 | 7/7 | |
| revCSC | 7 / 97 | +0.028 | 0.010–0.046 | p_BH 0.015 | −0.019 to 0.075 | 7/7 | |
| ExtCIOC | 7 / 97 | +0.019 | 0.013–0.025 | p_BH 0.001 | 0.002–0.036 | 7/7 | |
| YAPcore | 7 / 97 | +0.007 | −0.007 to 0.021 | p_BH 0.27 | −0.025 to 0.038 | 5/7 | |
| E1-L Absorptive differentiated-like | 4 / 35 | +0.031 | −0.026 to 0.088 | 0.18 | −0.129 to 0.191 | 3/4 | |
| E1-L Cycling Stem/TA | 4 / 35 | +0.043 | 0.0004–0.085 | 0.049 | −0.066 to 0.151 | 4/4 | |

Chen per-study E1 is now n=16, +0.015 (CI 0.004–0.027). The other five studies are unchanged.

### Pre/post (per cohort; Post − Pre)

| Estimand | Qin | Chen |
|---|---|---|
| **E1-pp, depth-matched** | n=18: −0.014 (−0.031 to 0.004), p=0.13 | n=10: −0.008 (−0.032 to 0.017), p=0.77 |
| Original depth, same patients (descriptive) | n=18: −0.033 (−0.073 to 0.007) | n=10: −0.027 (−0.084 to 0.029) |
| (i) original depth | **n=20:** −0.034 (−0.070 to 0.002), Wilcoxon p=0.012 | n=11: −0.029 (−0.079 to 0.021) |
| (ii) raw, depth-matched | −0.018 (−0.037 to 0.001) | −0.004 |
| (iii) adjusted | −0.009 (−0.026 to 0.008) | −0.004 |
| proCSC | **n=20:** −0.036 (−0.070 to −0.003), Wilcoxon p=0.044 | −0.030 (−0.078 to 0.019) |
| revCSC / ExtCIOC / YAPcore | −0.013 / −0.003 / −0.010 (all CIs include 0) | +0.003 / −0.004 / +0.010 |

**Reading:**
- In the same 18 Qin patients, original depth gives −0.033 and depth matching gives −0.014.
- So the larger original-depth decrease is depth-sensitive and not a patient-selection effect.
- Its cause (depth, specimen type or processing) is not resolved.

## 3. Request

- Confirm the corrections and the P02 amendment.
- Grant A3b final approval and Stage S closure.
- Approve figure lock on the corrected inclusion list.
