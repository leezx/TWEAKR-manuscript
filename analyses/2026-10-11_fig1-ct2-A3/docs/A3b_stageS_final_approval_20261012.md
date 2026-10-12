# A3b Stage S — FINAL APPROVED · STAGE S CLOSED (ChatGPT "Fig.1b-CT2 plasticity", 2026-10-12, on commit 7a2ecfc)

- **Verdict:** accepts all minimal corrections in `A3b_stageS_correction_20261012.md`, closes Stage S and authorises Extended Data figure lock.
- **What was checked:** the reviewer read the correction note, `a3b_estimands.py`, the corrected pooled/study/cohort tables, the patient-level data and `audit_v1_20261012/`.
- **Scope of the change:** clinical-eligibility and eligibility-rule fixes only. No change to CT2/UCell scoring, identity_v1, depth targets, models or thresholds.
- **Format:** a condensed record. Wording is quoted.

## Correction audit (all PASS)

- Qin TRG0 is excluded: n 22 → 20.
- Chen P02 is excluded: E1 86 → 85; Chen 17 → 16. The 86-patient analysis is kept as an audit sensitivity.
- E1-L uses the E1 patient gate (35 patients per class).
- E3 uses the E3 patient gate (unchanged).
- The same-patient depth comparisons are correct (Qin 18, Chen 10).
- The v1 tables are preserved.
- **P02:** accepted as a conservative choice. It remains a clinical inference from treatment line and sample stage, not direct per-sample treatment history; record this in Methods or the audit trail.

## Final status

| Module | Status |
|---|---|
| A3b contract v0.3 | FROZEN |
| identity_v1 | FROZEN |
| CT2 / UCell scoring | COMPLETE |
| E1 primary + sensitivities | FINAL APPROVED |
| Normal–primary programmes | FINAL APPROVED (tissue context; not malignant-cell-intrinsic) |
| E1-L | APPROVED as exploratory; both classes shown together; Cycling Stem/TA must not be called a validated within-lineage increase |
| Qin / Chen E1-pp | APPROVED as exploratory |
| E3 | Descriptive only |
| E4 / identity composition | QA / descriptive only |
| A3b Stage S | **CLOSED** |
| Extended Data figures | **GO / FIGURE LOCK AUTHORIZED** |

- **Corrected Qin readouts:** original depth n=20, Wilcoxon p=0.012; proCSC n=20, p=0.044. Exploratory only.
- **Same-patient analysis:** it shows the estimates are depth-sensitive, but cannot say whether depth, specimen type or composition is the cause.

## Figure lock (source: corrected tables at commit 7a2ecfc)

| Panel | Content | Must state |
|---|---|---|
| ED-A | E1 six-study forest, pooled CI/PI, three mandatory sensitivities | MUI, heterogeneity, p=0.068, n=85 |
| ED-B | Four programme differences; both E1-L classes | Distinguish BH-adjusted from nominal exploratory p |
| ED-C | Qin/Chen paired depth-matched CT2; same-patient original-depth comparison | Qin TRG0 excluded; biopsy/resection and processing confounding; Chen GEO-stage limitation |

- **Document hygiene:** mark `A3b_stageS_results.md` as SUPERSEDED by the correction note, so that figure scripts and Results text do not cite the old n=86 or n=22 numbers. This does not block lock.

## Approved Results text (for the Extended Data Results)

> "Across six independent colorectal cancer studies comprising 85 patients, paired tumour-specimen epithelium exhibited consistently positive but heterogeneous differences in CytoTRACE2-predicted developmental potential relative to adjacent-normal epithelium (pooled Δ = 0.057, 95% CI −0.006 to 0.120; P = 0.068). Positive estimates were retained across prespecified sensitivity analyses, although none yielded conclusive pooled evidence. In contrast, proCSC, revCSC and Extended CIOC transcriptional programme scores were significantly higher in tumour-specimen epithelium, whereas YAP-core scores showed no statistically supported pooled difference. Exploratory analyses of neoadjuvant treatment cohorts did not detect significant depth-matched changes in predicted developmental potential. These comparisons reflect tissue-context differences and do not establish malignant-cell-intrinsic developmental potency or functional cellular plasticity."

- Complementary to A3a. Do not escalate it to a continuous developmental trajectory of cancer progression.

## Directive

**FREEZE** corrected results at 7a2ecfc → **CLOSE** A3b Stage S → **GENERATE AND LOCK** Extended Data figures → draft Methods, Results and legends.

- No new cohorts, potency algorithms, post-hoc exclusions or CNV identity schemes.
- The Chen surgical-specimen branch stays on HOLD; this does not affect closure.
