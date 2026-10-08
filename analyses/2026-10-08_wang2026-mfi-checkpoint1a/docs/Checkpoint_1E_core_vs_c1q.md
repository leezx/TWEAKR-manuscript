# Checkpoint 1E — CORE versus C1Q specificity (DS-013)

**Question:** Does the CORE signature provide TNFSF12-associated information beyond the C1Q
macrophage program?

CORE (GPNMB, SPP1, TREM2, APOE, FABP5, PLD3) is the pre-defined primary signature. C1Q (C1QA,
C1QB, C1QC) is an independent comparator; the two are not merged. Neither signature was
re-selected in this dataset, and TNFSF12 is not part of either.

**No new run was needed.** M1–M3 were already fitted in CP1D: single-module models plus the
post hoc CORE + C1Q joint model, with the same donor fixed effects, log10 library size and
CD14_M-only sensitivity population. This document assembles them as the CP1E answer and adds
the collinearity check. Table: `tables/cp1d/cp1e_core_vs_c1q_models.csv`.

Model: logistic regression, TNFSF12 detected (UMI > 0) ~ z-scored module score(s) + log10
library size + donor fixed effects. Fitted on donors with ≥1 TNFSF12+ macrophage; Wald 95% CI.

| Population | Model | Term | OR per SD (95% CI) | p |
|---|---|---|---|---|
| CD14_M + CD16_M (n = 9,276) | M1 | CORE | 1.29 (1.11–1.50) | 0.0008 |
| | M2 | C1Q | 1.42 (1.25–1.62) | <0.0001 |
| | M3 | CORE | 1.21 (1.04–1.41) | 0.013 |
| | M3 | C1Q | 1.38 (1.22–1.57) | <0.0001 |
| CD14_M only (n = 7,261) | M1 | CORE | 1.23 (1.03–1.46) | 0.020 |
| | M2 | C1Q | 1.38 (1.20–1.59) | <0.0001 |
| | M3 | CORE | 1.18 (0.99–1.40) | 0.067 |
| | M3 | C1Q | 1.36 (1.18–1.57) | <0.0001 |

Collinearity between the CORE and C1Q scores: Pearson r = 0.22, Spearman ρ = 0.18, VIF = 1.05
(CD14_M only: 0.21 / 0.20 / 1.04). The joint-model coefficients are therefore not destabilised by
collinearity.

## Reading against the pre-stated criteria

- **C1Q:** stable and the stronger association in every model and population.
- **CORE:**
  - Keeps an independent association after C1Q adjustment in the primary population
    (1.21, CI excludes 1).
  - In CD14_M only, the estimate is almost unchanged (1.18 vs 1.21), but the CI includes 1
    (p = 0.067).
  - Moving from CD14_M+CD16_M to CD14_M changes the CORE estimates little (M1 1.29 → 1.23;
    M3 1.21 → 1.18). The loss of significance mainly reflects fewer cells and positives
    (181 vs 212). It does not show that CD14_M/CD16_M composition drives the association,
    although composition cannot be excluded.
- **Classification:** CORE does **not** meet "stable independent association" in the strict
  sense, because it is not robust in the sensitivity population. It also does not "lose its
  association" while C1Q stays stable: the effect size persists at about 1.2 per SD.
  Conclusion: modest incremental information that is not robustly established.
- Even the primary-population M3 result shows only statistical incremental association, not
  TWEAK specificity.

## Statistical scope notes (from review)

- Directional consistency (12 higher, 2 lower; exact two-sided sign test p = 0.013) was
  evaluated among the **14 donors with detectable TNFSF12 in macrophages**, not all 23 donors.
- The 9 donors with zero TNFSF12+ macrophages carry no high/low directional information. They
  are not evidence against an association.

## Recommended wording

*A macrophage transcriptional program originally associated with Tnfsf12 expression in murine
colorectal tumours (SPP1/TREM2/GPNMB/APOE core) is modestly associated with TNFSF12 detection in
human maternal decidual macrophages. This association overlaps with, and is weaker than, a
C1Q-associated macrophage program; the core program's independent contribution is small and not
robust in the CD14+ macrophage subset.*

Use CORE as an exploratory macrophage-state score, **not** as a TWEAK+ macrophage classifier.
