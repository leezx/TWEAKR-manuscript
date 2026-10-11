# Fig. 1c Stage 1 — GPT audit and OOD amendment decision (2026-10-11)

Conversation: https://chatgpt.com/c/6acbaf02-1bc8-83ea-a533-5d9a9c06e138. The full text is in the conversation; this file is a structured record taken directly from the page text.

## Decisions

| Item | Status |
|---|---|
| Stage 1 evidence for distinguishable programmes | APPROVE |
| A: keep the strict OOD gate | REJECT |
| B: remove the OOD hard rejection | APPROVE, with validation conditions |
| C: study-specific OOD percentile | REJECT (could mask genuinely novel states) |
| Recompute G5/G6/G9 | REQUIRED |
| Freeze the amended labels now | NOT YET |
| Stage 3 before the new validation | HOLD |

## Gate verdicts

| Gate | Verdict |
|---|---|
| G1 | PASS within Pelka only; transfer to the other studies is unverified |
| G2 | PASS |
| G3 | PASS, moderate convergent evidence |
| G4 | PASS, limited to programme distinguishability; no claim of discrete cell types |
| G5 | PASS with a major selection limitation (69/222 patients; 94.6% of top-rev-tertile patients lack a reference) |
| G6 | PASS |
| G7 | HIGH technical dependence |
| G8 | FAIL as an unknown-rejection rule |
| G9 | WARNING |
| G10 | PASS |

**Hybrid.** Observed vs expected at p75 is 6.6% vs 6.3%, so there is no enrichment of co-activation. Recommended wording: "Distinguishable proliferative/stem-associated and revival–oncofetal transcriptional programmes coexist within primary CRC epithelia, with overlapping activation and substantial inter-study heterogeneity." Do not claim mutually exclusive populations or a directional continuum.

## Amendment B (contract v0.3a): scope

- **Unchanged:** the classifier, folds, calibration, Axis S, and the max-p/margin thresholds (0.70/0.20). Changing the thresholds would be a second amendment.
- **Changed:** the OOD percentile is still computed and stored, but is removed from the primary assignment rule. "Original OOD-pass only" becomes a mandatory sensitivity analysis.
- **Interpretation:** these are Pelka-like predicted lineages, not proven identities.

## Conditions before freeze and Stage 3

1. **Amendment provenance.** Record the reason, the diagnostics, the old and new rules, and the code version. Keep the v0.3 labels and their SHA256; never overwrite them.
2. **CT2-blinded lineage plausibility audit,** in the high-OOD studies (Joanito, Uhlitz, Liu, MUI, Qin):
   - marker and pseudobulk concordance for absorptive (KRT20/FABP1/ALPI…), stem/TA, cycling and secretory classes;
   - the original published annotation, if available;
   - association of OOD with UMI, genes, study, platform and lineage.
   - Markers that overlap the classifier HVGs count as a plausibility check, not independent validation.
   - A study × class pair without marker support is labelled "lineage transfer unverified" and its lineage-specific contrasts are paused.
3. **Re-run affected gates:** G1 selective metrics, G5, G6, G8, G9, G10, and the lineage-conditioned G3/G4/G7 summaries.
4. **Re-apply the decision branch.** A contrast that fails eligibility goes on HOLD.
5. **Freeze outputs:** labels, probabilities, OOD values, an old→new transition table, the OOD-pass flag and SHA256s. Explain the 285,703 vs 285,141 cell difference (562 cells).
6. **Final pre-Stage-3 checks:**
   - reference and strata are mutually exclusive;
   - same-sample eligibility;
   - multi-sample aggregation;
   - ds1–5 method;
   - the secondary continuous model is executed regardless of whether the paired contrasts are significant.

Do NOT re-select Axis S thresholds, the reference definition or any other CT2-relevant parameter. After the v0.3a freeze, the annotation is never changed whatever CT2 shows.
