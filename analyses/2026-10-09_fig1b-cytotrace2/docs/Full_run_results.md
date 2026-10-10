# Fig. 1B — full 13-study CytoTRACE2 results (A2.1)

- **Date:** 2026-10-10.
- **Inputs:**
  - frozen `annotation_v1` (SHA256 `1d8148063d83…`);
  - cohort v1: 13 studies, 222 patients, 361 samples;
  - CytoTRACE2 1.1.0, seed 14, whole-sample runs.
- **Runs:**
  - main run: 361/361 samples (SGE 3654877);
  - depth-matched run: 1,805/1,805 tasks (3654878);
  - statistics: 3654888.
  - **0 failed tasks.**
- **Cells scored:** 1,000,926 (all L1 Epithelial / Immune / Stromal cells; the 2,323 "Other" cells are excluded).
- **Code:** `code/fig1b_stats.py`. Tables: `tables/full/` (light; per-cell scores stay on Argos `full/`).
- **Method:** every analysis below was pre-specified in the contract or added by the 2026-10-10 review (F1-clean). Nothing was added or changed after the results were seen.

## 1. Primary result (L1, 222 patients, 13 studies; REML + Hartung–Knapp; Holm over 3 contrasts)

| Contrast | Pooled Δ (95% CI) | 95% PI | τ² | I² | Holm p | Studies with same sign | LOSO range |
|---|---|---|---|---|---|---|---|
| Epithelial − Immune | **+0.073** (0.056, 0.089) | 0.036, 0.109 | 0.0004 | 0.74 | <0.001 | 13/13 | 0.071–0.077 |
| Epithelial − Stromal | **−0.162** (−0.206, −0.117) | −0.315, −0.009 | 0.004 | 0.88 | <0.001 | 13/13 | −0.171 to −0.149 |
| Stromal − Immune | **+0.244** (0.197, 0.290) | 0.080, 0.408 | 0.005 | 0.90 | <0.001 | 13/13 | 0.231–0.255 |

**Patient medians (CytoTRACE2 score, 0–1):**

| Compartment | Median | IQR |
|---|---:|---|
| Stromal | 0.287 | 0.203–0.385 |
| Epithelial | 0.131 | 0.113–0.148 |
| Immune | 0.062 | 0.054–0.070 |

The ordering is **Stromal > Epithelial > Immune**, and it holds within every study. The study-level estimates and 95% CIs are in `study_contrasts.csv`.

Notes on individual studies:

- MUI (BD Rhapsody) has the largest Epithelial − Immune difference: 0.254, against 0.03–0.11 elsewhere.
- Uhlitz Epithelial − Immune (0.026; CI −0.005 to 0.058) and MUI Epithelial − Stromal (−0.082; CI −0.184 to 0.019) are the only study CIs that cross 0.

**Supporting mixed model** (patient median ~ compartment + (1|study) + (1|study:patient)):

| Term | Estimate (95% CI) |
|---|---|
| Epithelial vs Immune | +0.083 (0.068, 0.097) |
| Stromal vs Immune | +0.247 (0.232, 0.261) |

statsmodels warned that the study variance is on the boundary, so this model is supporting only.

**Potency categories (descriptive):** median per-study share of cells labelled Differentiated:

| Compartment | Differentiated |
|---|---:|
| Immune | 98.0% |
| Epithelial | 82.6% |
| Stromal | 37.3% |

In stromal cells, 24.4% are Multipotent, 18.9% Oligopotent and 18.1% Unipotent.

## 2. Pre-specified sensitivity analyses (pooled Δ, 95% CI)

| Analysis | Patients / studies | E − I | E − S | S − I |
|---|---|---|---|---|
| Primary | 222 / 13 | +0.073 (0.056, 0.089) | −0.162 (−0.206, −0.117) | +0.244 (0.197, 0.290) |
| Raw model score (pre-smoothing/binning) | 222 / 13 | +0.067 (0.023, 0.112) | −0.157 (−0.210, −0.104) | +0.231 (0.178, 0.283) |
| Depth-matched, 5 seeds (range of estimates) | 220 / 13 | +0.041 to +0.042 | −0.070 to −0.073 | +0.114 to +0.117 |
| Depth-matched raw score, 5 seeds | 220 / 13 | +0.012 (CI ≈ 0.004, 0.020) | −0.058 to −0.060 | +0.076 to +0.078 |
| Detection-adjusted (secondary) | 222 / 13 | +0.058 (0.045, 0.071) | −0.173 (−0.235, −0.112) | +0.135 (0.075, 0.195) |
| Stringent 50/10 | 162 / 7 | +0.089 (0.017, 0.161) | −0.166 (−0.242, −0.090) | +0.259 (0.190, 0.328) |
| Unsorted only | 205 / 12 | +0.073 | −0.158 | +0.241 |
| F1-clean L1 (review) | 217 / 13 | +0.074 | −0.157 | +0.240 |
| Cycling-negative cells | 222 / 13 | +0.071 | −0.165 | +0.242 |
| Low-gene (<500 model genes) excluded | 220 / 13 | +0.079 | −0.172 | +0.261 |
| Fibroblast (L2) instead of Stromal | 154 / 12 | +0.072 | **E − F −0.338** (−0.393, −0.284) | **F − I +0.425** (0.377, 0.472) |
| Leave-one-study-out (primary) | 12 studies each | 0.071–0.077 | −0.171 to −0.149 | 0.231–0.255 |

Every pooled CI excludes 0, and every Holm-adjusted p is ≤0.023. The sign never changes in any analysis.

**Depth matters.** Depth matching at the study target T_s reduces:

- Epithelial − Stromal by about 55%;
- Stromal − Immune by about 53%;
- Epithelial − Immune by about 43%.

On the raw model score after depth matching, Epithelial − Immune is only +0.012. Its prediction interval crosses 0 (−0.011 to 0.035), and so do those of the other raw depth-matched contrasts.

The contract notes that depth matching cannot remove intrinsic differences in transcriptome complexity between lineages. This attenuation is the main limit on interpretation.

**Detection-adjusted.** Stromal − Immune is halved (+0.135; PI −0.026 to 0.296). Epithelial − Stromal is unchanged. The contract says this adjustment risks over-adjustment and is never the primary result.

**Not run** (recorded in `stats_notes.json`):

- Permissive 20/5: the 11 extra patients are outside cohort v1 and were not exported.
- HTAPP HTAN: not part of the cohort v1 exports.

**Fibroblast patient set.** It has 154 patients, not the 162 in the cohort flag. The flag uses Atlas fibroblast counts; this analysis applies ≥30 L2 Fibroblast cells, and studies need ≥5 patients.

## 3. L2 landscape (secondary, descriptive; patient medians, ≥30 cells per patient × type)

| L2 type | Patients / studies | Median (IQR) |
|---|---|---|
| Fibroblast | 158 / 13 | 0.495 (0.404–0.573) |
| Smooth muscle | 45 / 12 | 0.264 (0.185–0.313) |
| Pericyte | 106 / 13 | 0.242 (0.164–0.308) |
| Endothelial | 173 / 13 | 0.163 (0.157–0.220) |
| Malignant epithelial (high-confidence subset) | 76 / 8 | 0.138 (0.123–0.152) |
| Plasma | 187 / 13 | 0.105 (0.088–0.124) |
| Monocyte | 165 / 12 | 0.080 |
| Mast | 113 / 12 | 0.078 |
| Macrophage | 183 / 13 | 0.076 |
| Dendritic cell (mainly cDC2) | 13 / 5 | 0.075 |
| B | 175 / 13 | 0.070 |
| Neutrophil | 47 / 9 | 0.060 |
| NK | 153 / 13 | 0.044 |
| CD4 T | 219 / 13 | 0.044 |
| CD8 T | 216 / 13 | 0.034 |

- The stromal compartment signal is driven by fibroblasts. Endothelial cells score close to epithelium.
- The malignant epithelial subset is MSS-enriched and covers 8 of 13 studies. It sits within the full-epithelium range (0.138 vs 0.131).
- Study × type medians for the Extended Data heatmap are in `L2_study_heatmap.csv`.

## 4. Interpretation within the claim ceiling (proposed wording; for review)

**What the data support:**

> Across 222 patients from 13 studies, CytoTRACE2-predicted developmental potential was highest in the stromal compartment and lowest in immune cells, with epithelium intermediate. The ordering was consistent in every study and in all pre-specified sensitivity analyses. Effect sizes were about halved by depth matching.

**What they do not support:**

- That CRC epithelium shows elevated plasticity relative to the TME. The score is a model prediction, not plasticity. In addition:
  - most epithelial cells are scored Differentiated;
  - the depth-matched raw-score Epithelial − Immune difference is small, and its prediction interval crosses 0.
- Any ordering of immune hierarchies (review constraint).
- That fibroblasts are developmentally primitive. The fibroblast score may reflect lineage-specific programmes, such as mesenchymal and ECM genes, that the model learned from developmental mesenchyme. The contract's claim ceiling already states this.

## 5. Questions for review

1. Does the proposed wording in §4 stay within the claim ceiling?
2. **Fig. 1B layout** (per the 2026-10-10 review):
   - **B1:** patient medians by L1 compartment, with study summaries.
   - **B2:** forest plot of the three contrasts (13 studies plus pooled, with PI), with depth-matched and raw-score pooled estimates shown as secondary rows.
   - **Fig. 1C / Extended Data:** the L2 landscape with patient and study counts.
   - Is showing depth-matched rows inside B2 preferred, or should they move to Extended Data?
3. Should the MUI Epithelial − Immune outlier (BD Rhapsody) be flagged in the legend? It does not change the pooled estimate (LOSO 0.071–0.077).
4. Are the permissive and HTAPP gaps acceptable as "not run", or should we export the 11 patients for permissive (a dated amendment)?
