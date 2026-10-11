# Fig. 1c Stage 4 final review and claim freeze (GPT, 2026-10-11)

Conversation: https://chatgpt.com/c/6acbaf02-1bc8-83ea-a533-5d9a9c06e138. Request: scratchpad msg7 (Stage 4 results + 4 questions).
This is a condensed record; the frozen wording is quoted verbatim. GPT reviewed only the summary results it was given, without access to code or raw outputs, so this approves the interpretation and the figure plan, not computational reproducibility.

## Decisions
- **Stage 4: APPROVE.**
- **Result branch: B, FINAL.** Robust pro-dominant > rev-dominant potency, with modest reference- and proxy-dependent rev-dominant elevation.
  - C is rejected: rev shows no robust negative effect.
  - D is rejected: the pro-related differences persist after adjustment.
- **Figure production: GO.**

## Frozen wording
- **Core claim:** "Distinguishable proliferative/stem-associated and revival–oncofetal epithelial programmes display differential associations with predicted developmental potency in treatment-naive primary CRC."
- **Figure title:** "Proliferative and revival–oncofetal epithelial programmes are differentially associated with predicted developmental potency in CRC"
- **One-sentence conclusion:** "Across treatment-naive primary CRC cohorts, proCSC-dominant epithelial cells exhibited higher CytoTRACE2-predicted developmental potency than revCSC-dominant cells (203 patients, 13 studies; pooled within-patient difference = 0.077, 95% CI 0.044–0.111; Holm-adjusted P = 0.0009), whereas revCSC-dominant versus differentiated-like contrasts were modest and reference- and proxy-dependent, with no detectable positive association for the revCSC programme in covariate-adjusted continuous analyses."
- **Depth:** "The observed attenuation following depth matching was driven primarily by changes in inferred CT2 scores rather than differential cell retention." Do not claim that all of the attenuation is technical artefact.
- **rev vs reference:** "The magnitude and statistical support of rev-dominant versus differentiated-like contrasts are proxy-dependent." Do not call the whole revCSC biology CT2–CCAT inconsistent: the continuous conditional associations agree between the two proxies. Do not compare absolute CT2 and CCAT magnitudes.
- **Discussion only, not a demonstrated claim:** "Conventional transcriptome-derived potency estimates do not fully capture revival–oncofetal programme identity."
- **Avoid → use instead:**

| Avoid | Use instead |
|---|---|
| two highly plastic CSC populations | distinguishable stem-associated transcriptional programmes |
| revCSC has low/no potency | weak or inconsistent independent associations with transcriptome-derived potency estimates |
| proCSC has higher functional stemness | pro-dominant cells have higher CT2-predicted potency than rev-dominant cells |
| universal across CRC | positive pooled contrast with consistent directions in the 13 included studies, despite substantial effect-size heterogeneity |

- **Provenance wording:** "prespecified sensitivity analyses with implementation details documented after the primary analysis".
- **Confirmatory vs sensitivity:** only the Holm family is confirmatory. Sensitivity results whose CI excludes 0 are not confirmatory.
- **Population and measure:** "tumour-specimen-derived epithelial cells", "programme-defined strata", "predicted developmental potency".

## Panel map (frozen)

**Main Fig. 1c**
- **c-i, programme architecture:**
  - pro × rev plotted as *within-sample percentile ranks*, so that the p75 lines have one consistent meaning. If raw UCell scores are used instead, colour by the frozen sample-specific strata and draw no global cutoff lines.
  - Use patient-balanced sampling or equal weighting for display, and state it in the legend.
  - Show the verified/unresolved lineage composition.
- **c-ii, the three pre-specified patient-paired CT2 contrasts:** pooled estimate, 95% CI and n; highlight pro−rev; annotate "13/13 studies positive".
- **c-iii, small M2 inset:** CT2 adjusted + lineage, proCSC +0.232 [0.200, 0.263] and revCSC −0.022 [−0.052, 0.009]. It gets its own axis (within-sample partial Spearman ρ). Do not imply that the two ρ were formally tested against each other.
- No forest plot in the main figure.

**Extended Data**

| Panel | Content |
|---|---|
| ED-A | Pelka transfer, OOD amendment, lineage audit, unverified/unresolved proportions |
| ED-B | pro × rev raw score distributions, hybrid and threshold sensitivity, mechanism-blinded membership |
| ED-C | Study-level forests for the three primary contrasts; I², τ², PI, LOSO |
| ED-D | Depth audit D1–D4, intersection, adjusted and reduced models |
| ED-E | p70/p80, alternative references, common subsets, OOD-pass |
| ED-F | MSS/MSI-H, CNV+, Pelka exclusion, Cycling restriction |
| ED-G | CT2 vs CCAT, categorical and M2 |
| ED-H | Eligibility funnel, reference missingness and selection (required) |

## Final gate
- **PASS:**
  - Stage 1 freeze;
  - Stage 3 primary contrasts;
  - Stage 4 package;
  - depth audit;
  - reference-selection audit;
  - sample universe;
  - heterogeneity reporting.
- **Pending at file level:**
  - final reporting table: effect, CI, P, patient/study n and analysis version for every analysis;
  - figure and legend: every number checked against the frozen tables.
- **The analysis line is closed.** Do not add computational proxies to try to show that revCSC has higher CT2.
