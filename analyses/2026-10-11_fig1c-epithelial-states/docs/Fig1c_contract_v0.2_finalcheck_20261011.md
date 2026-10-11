# Fig. 1c contract v0.2 — GPT final check (2026-10-11)

Conversation: https://chatgpt.com/c/6acbaf02-1bc8-83ea-a533-5d9a9c06e138. The page text was saved directly from the page; the content is in English, with GPT's own verdict words kept.

**Verdict: REVISE.** After the 5 fixes below, v0.3 can be frozen and Stage 1 run immediately; no redesign is needed. GPT notes that the fixes come from internal consistency of the contract, not from the direction of the A3a results.

1. **P0 §2.4 reference is self-contradictory.**
   - Primary reference = ALL Axis-L Absorptive cells, with no Axis-S filter.
   - Absorptive cells that are pro- or rev-high stay in the reference and are flagged as lineage–program discordant.
   - Absorptive + neither-high becomes a sensitivity analysis.
   - The pro/rev strata are drawn from non-reference cells.
   - The comparison includes lineage composition and is not a pure programme effect, so the within-lineage pro-vs-rev sensitivity stays mandatory.
2. **P0 adjusted estimand.**
   - Use OLS on raw CT2, not rank-CT2. The coefficient is a conditional mean difference: use it for direction and robustness only, not for % attenuation against the median difference.
   - One covariate model for every pooled sample. Samples that cannot fit it are adjusted-ineligible.
   - A reduced model may only be a separate sensitivity analysis; never pool mixed models.
3. **P0 depth-matched CI.**
   - Per ds replicate, compute the sample- and patient-level contrasts.
   - Average the 5 replicates within each patient to give one patient-level estimate.
   - Pool per study with mean, SE and REML+HK to get a formal CI.
   - Report replicate variability separately; it is not biological uncertainty.
4. **P0 G5 contrast-specific eligibility.**
   - pro vs ref: pro ≥30 and ref ≥50.
   - rev vs ref: rev ≥30 and ref ≥50.
   - pro vs rev: pro ≥30 and rev ≥30 in the same sample, with no reference needed.
   - Each contrast needs ≥20 patients and ≥3 studies, and each study entering a contrast needs ≥5 eligible patients.
   - Each contrast has its own funnel; do not use the intersection of the three.
5. **P0 operationalisation of G2/G3/G4 and §5.**
   - G2: define the Spearman unit (within-patient cells), the comparison objects, and how the 200 splits are summarised.
   - G4: predefine the control variables, the method and the result criterion. Without a numeric rule, G4 is descriptive only.
   - G3: freeze huOnF in Stage 0. If it cannot be obtained or the non-overlap test cannot be run, G3 is unassessable and G3-supported wording is forbidden.
   - §5: formal operational contrasts require G1, G2, G5 and G10 to pass. G3 and G4 only set the wording.
