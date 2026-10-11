# Fig. 1c Stage 3 review (GPT, 2026-10-11)

Conversation: https://chatgpt.com/c/6acbaf02-1bc8-83ea-a533-5d9a9c06e138. Request: scratchpad msg6 (Stage 3 results + 5 questions).
This is a condensed record of GPT's reply. Decisions and requirements are kept close to the original wording; illustrative charts are omitted.

## Decisions
- **Stage 3 results: APPROVE.** Accepted as preliminary locked-contract estimates; GPT did not independently re-check the code or raw files.
- **Stage 4: GO.**
- **Manuscript figure: HOLD.** The layout can be drafted, but the final claim and statistical panels are not frozen.
- **Preliminary branch: B**, with robustly higher predicted potency in pro-dominant than in rev-dominant strata. Formal call comes after Stage 4.
  - A (both high) is not supported.
  - C ("rev inversely associated") is not used, because the adjusted continuous rev association is about 0 rather than negative.
  - D, E and F do not fit.

## Interpretation audit
1. "pro is higher than ref and rev, robust after adjustment": APPROVE with a technical reservation (non-random loss of reference cells in ds).
2. "rev shows no detectable rise vs ref": REVISE the wording.
   - The primary contrast is not significant, but ds shows a small positive effect. Do not say "no elevation", do not claim equivalence, and do not say "revCSC has no potency".
   - Allowed: "Revival–oncofetal programme activity is not consistently associated with elevated CT2-predicted developmental potency after accounting for transcriptomic complexity and epithelial lineage."
3. "≥2 plastic states not supported by CT2": APPROVE.
   - More precisely, there is no evidence that both states have robustly elevated predicted potency. CT2 cannot test plasticity in the first place.
- **pro−rev** is the most consistent finding across studies and should be the core quantitative result of Fig. 1c. I² = 0.93, so prediction intervals and study-level forest plots are required.
- **Do not quantify the attenuation as "55–65% technical bias".** The estimands and cohorts differ. Allowed: "substantially attenuated after technical and cell-cycle adjustment but remained positive."
- **Do not derive a pro−rev effect from pro−ref minus rev−ref**; those were estimated in different populations.

## Proposed claim (working)
- **Working title:** "Distinct epithelial stem-associated programmes exhibit divergent predicted developmental potency in colorectal cancer."
- **Take-home:** distinguishable proliferative/stem-associated and revival–oncofetal configurations coexist. Elevated CT2-predicted potency is *predominantly* (not exclusively) associated with the proliferative configuration.
- **revCSC must stay** as a reproducible oncofetal transcriptional configuration. It is not to be used to prove TWEAKR causality.
- **TNFRSF12A circularity:** never write "TWEAKR enriched in revCSC validates the mechanism". Downstream TWEAKR analyses should prioritise mechanism-blinded states.

## Stage 4 requirements

| Analysis | Decision |
|---|---|
| MSI/MSS | Mandatory. Stratified effects, CIs and coverage; test the interaction only with enough within-study overlap; no MSI biological interpretation if the difference comes from study composition |
| CNV-positive subset | Mandatory attempt. Feasibility audit; MSS selection caveat; "not estimable" if insufficient |
| Pelka excluded | Mandatory. Three primary contrasts plus Cycling-restricted; eligibility and effect |
| LOSO | Mandatory. Full LOSO effect, CI and direction per study (not just the range) |
| p70/p80 strata | Mandatory. Recompute strata, eligibility and contrasts |
| Mechanism-blinded scores | Mandatory. Full vs mb correlations; p75 membership transition matrix; Jaccard for pro/rev/hybrid; eligibility; four contrasts. The primary full-signature definition is never changed |
| Reference sensitivities | Mandatory. (i) Absorptive + neither-high; (ii) Absorptive + Secretory. Recompute G5; report studies and patients gained or lost; also compare on a common eligible-patient subset |
| Reduced adjusted model | Mandatory report. Separate from the full model; covariates and eligible samples stated; compare on a common sample set if possible |
| CCAT | Conditionally mandatory. Run if the A3a technical gate passed (it did: A3a §10–11) |
| OOD-pass only | Done; kept |
| Depth-matched missingness audit (D1–D4) | New, mandatory |

### Depth audit (D1–D4)
- **D1.** Retained vs dropped cells, per group and study: log UMI, log genes, mito, original CT2 final, programme scores. In particular, do the dropped reference cells have lower CT2?
- **D2.** Complete-case intersection (cells kept in all of ds1–5):
  - A = original final, all cells;
  - B = final restricted to the intersection;
  - C = ds restricted to the intersection;
  - D = B − C on the same cells.
- **D3.** Eligibility retention after the intersection: patients and studies lost; whether high-rev tumours are systematically lost; covariate composition. If thresholds fail → descriptive only.
- **D4.** Interpretation rule:

| B vs A | C vs B | Interpretation |
|---|---|---|
| B ≈ A | C same direction, supported | Depth-robust |
| B attenuated | C ≈ B | Attenuation is mainly cell selection |
| B ≈ A | C attenuated | Depth matching changes the score itself |
| — | C unstable, or large eligibility loss | Downgrade the depth-robust claim |

- pro−rev is less affected by reference dropout, so its technical robustness is currently more credible.

## M2 in the figure
- M2 covers 216/222 patients and does not depend on reference availability. Use it as concise support in the main figure or as a core ED item.
- It shares data with the strata, so it is consistency evidence under a different estimand, not independent validation.

## Final gate before plotting
1. Full Stage 4 sensitivity matrix: 4 contrasts × the pre-specified sensitivities, with effect, CI and patient/study n.
2. D1–D4 completed.
3. Sample universe reconciliation: 360 Stage 1 samples vs 339 Stage 3 samples.
4. Meta diagnostics: forest per primary contrast, LOSO effect/CI, I², tau², and a PI wherever estimable. If the PI crosses 0, report the average effect but do not claim the same direction in any new cohort.
5. Matched-cohort robustness: unadjusted vs full-adjusted, and the reference sensitivities, on common eligible-patient subsets.
6. Figure-level denominators: patients, studies and cells, and whether they come from the same eligible set.
7. Final inference lock: Holm covers only the three primary contrasts; nothing is promoted ad hoc.
8. Wording audit:
   - CT2 is not plasticity.
   - Tumour-specimen epithelium is not all malignant.
   - Strata are not functionally validated CSC populations.

## Proposed panel map
- **Main figure.**
  - Left: proCSC × revCSC joint distribution with pro/rev/hybrid/neither and the lineage annotation composition.
  - Right: the three pre-specified patient-paired CT2 contrasts (pooled estimate, 95% CI, n), highlighting pro−rev. No large CT2 violins.
- **ED:** M2, forest plots, depth/complexity robustness, reference sensitivity, MSI/CNV+, mechanism-blinded, annotation uncertainty, eligibility funnel.
- **Recommended finding:** "Distinct stem-associated epithelial programmes are differentially coupled to predicted developmental potency in primary colorectal cancer."
