<!--
FRAMEWORK ONLY. Panel titles + intended claims from GPT/Figure2.md.
CONDITIONAL TITLE: keep "TWEAKR-associated" only if Panel 2G holds. If 2G fails,
retitle to "The oncofetal/revival-like state marks poor-outcome and
treatment-persistent CRC" and introduce TWEAKR in Figure 3.
Keep prognostic (OS/RFS) and treatment-associated (chemo/ICI persistence)
claims strictly separate. "Frozen" signatures: no gene reselection for survival.
-->

# Figure 2. The TWEAKR-associated oncofetal state marks clinically aggressive and treatment-persistent CRC

**Key point:** A signature frozen from Figure 1 marks adverse survival across
independent CRC cohorts — not explained by stage/MSI/CMS — and is preferentially
retained under chemotherapy and ICI pressure.

**Status:** framework only — panel images and finalized legend text pending.

## Panels

### Figure 2A. Clinical cohort framework and frozen state signatures

![Figure 2A](Figure2/Fig2a.png)
> _Image pending: `Figure2/Fig2a.png`_

**Legend (draft):** <Schematic: the frozen oncofetal MP (Figure 1) + published
revCSC + proCSC signatures projected onto independent bulk, single-cell, and
longitudinal treatment cohorts. Emphasise "frozen": no gene/threshold
reselection downstream (avoids circularity).>

### Figure 2B. Cross-cohort OS/RFS association

![Figure 2B](Figure2/Fig2b.png)
> _Image pending: `Figure2/Fig2b.png`_

**Legend (draft):** <Forest plot of continuous-score Cox HRs, one per cohort
(OS and RFS separated), with a representative KM for visualisation. Claim:
cross-cohort prognostic consistency.>

### Figure 2C. Independence from established high-risk features (stage / MSI-MMR / CMS / stromal)

![Figure 2C](Figure2/Fig2c.png)
> _Image pending: `Figure2/Fig2c.png`_

**Legend (draft):** <Multivariable Cox adjusting for stage, MSI/MMR, CMS or
stromal content. If the oncofetal score remains independently associated →
"independent prognostic"; if not → "marks the clinically aggressive CMS4-like
axis". Do not overclaim.>

### Figure 2D. Paired chemotherapy-associated CSC-state shift

![Figure 2D](Figure2/Fig2d.png)
> _Image pending: `Figure2/Fig2d.png`_

**Legend (draft):** <Matched pre→post patient-level analysis: proCSC, revCSC,
and revCSC–proCSC balance. Likely framing: proCSC falls, revCSC/oncofetal
relatively retained → balance shifts toward revival-like. Call it "selective
persistence / relative enrichment", not "induction", unless absolute increase.>

### Figure 2E. Treatment response versus baseline / post-treatment state or state change

![Figure 2E](Figure2/Fig2e.png)
> _Image pending: `Figure2/Fig2e.png`_

**Legend (draft):** <Responder vs progressor: baseline oncofetal/balance
difference, and whether the state shift is larger in progressors. Baseline
prediction is the valuable result — phrasing: "pretreatment oncofetal state is
associated with subsequent treatment response"; not "validated predictive
biomarker".>

### Figure 2F. Independent ICI cohort shows analogous oncofetal persistence

![Figure 2F](Figure2/Fig2f.png)
> _Image pending: `Figure2/Fig2f.png`_

**Legend (draft):** <ICI as a second, orthogonal therapeutic pressure — paired
state change. Higher-order claim if it holds: "distinct therapeutic pressures
converge on a common oncofetal persistence state." ICI patient n is small; do
not hang the core conclusion on TWEAK–TAM coupling here.>

### Figure 2G. TNFRSF12A preferentially marks the adverse / treatment-persistent oncofetal compartment

![Figure 2G](Figure2/Fig2g.png)
> _Image pending: `Figure2/Fig2g.png`_

**Legend (draft):** <Priority order: TNFRSF12A vs oncofetal-MP relationship in
independent cohorts; whether oncofetal-high/TNFRSF12A-high double-high has the
worst outcome; TNFRSF12A × oncofetal-score interaction in continuous Cox;
whether post-treatment retained oncofetal cells are preferentially
TNFRSF12A-high. **If unstable → drop "TWEAKR" from the Figure 2 title.**>

## Full legend (submission form)

**Figure 2. The TWEAKR-associated oncofetal state marks clinically aggressive and treatment-persistent CRC.**
**(A)** <…> **(B)** <…> **(C)** <…> **(D)** <…> **(E)** <…> **(F)** <…> **(G)** <…>
<Global notes: cohorts and endpoints; three parallel scores (NMF-OnF, published
revCSC, proCSC) shown for key analyses; patient-level statistics (paired tests /
mixed models, repeated measures); confounders adjusted. Define OS, RFS, MSI/MMR,
CMS, ICI.>

## Source

- Data / results: `../TWEAKR-OncoPlacental/results/<step>/…` (CLIM / clinical scoring)
- Plotting code: `../TWEAKR-OncoPlacental/scripts/<step>/…`

## Related supplementary figures

- <TBD during drafting — e.g. per-cohort KM curves; sensitivity analyses; cohort tables.>

## Planning notes

Rationale: [`../GPT/Figure2.md`](../GPT/Figure2.md).
