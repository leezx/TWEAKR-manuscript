# Findings — early-stage CRC oncofetal atlas (Snippert 2026) as an external replication cohort

2026-11-02. All numbers are patient-level. "Matched null" means 200
expression-decile-matched random gene sets of the same size drawn from the same
panel; a signature that does not beat that null is not called enriched, however
consistent it looks across patients.

---

## Q1 — Where are proCSC, revCSC and the placenta axes enriched?

**Data.** GeoMx bulk spatial transcriptomics, two independent runs.
exp1 = CTA panel, 10 patients, 1,781 targets, 276 usable segments.
exp2 = WTA panel, 10 patients (9 T1 + 1 T3), 18,441 targets, 279 usable segments.
Regions: normal → adenoma → tumour core → invasive front; compartments PanCK⁺
(tumour epithelium) and PanCK⁻ (microenvironment).

### 1.1 The answer: the invasive front, in the epithelium, and it is a rebalancing

In the CTA cohort, tumour epithelium at the invasive front shows a clean swap
between the two stem programmes (invasive front − tumour core, patient-paired):

| Signature | genes on panel | Δ | patients up | P paired | z vs matched null | P null | q null |
|---|---|---|---|---|---|---|---|
| YAP regeneration | 69 | **+0.063** | 10/10 | 0.0020 | +7.6 | 0.005 | 0.008 |
| revCSC | 12 | **+0.044** | 10/10 | 0.0020 | +3.3 | 0.010 | 0.014 |
| IFA (fetal intestinal) | 59 | **+0.034** | 10/10 | 0.0020 | +4.4 | 0.005 | 0.008 |
| revival stem (Ayyaz) | 54 | **+0.027** | 10/10 | 0.0020 | +3.5 | 0.005 | 0.008 |
| fetal intestine (Yui) | 198 | **+0.026** | 10/10 | 0.0020 | +6.5 | 0.005 | 0.008 |
| proliferation | 50 | **−0.070** | 1/10 | 0.0098 | −7.6 | 0.005 | 0.008 |
| proCSC | 8 | **−0.084** | 1/10 | 0.0098 | −3.8 | 0.005 | 0.008 |
| EVT core | 8 | −0.020 | 3/10 | 0.16 | −0.7 | 0.36 | 0.45 |
| placenta trophoblast | 7 | +0.010 | 6/10 | 0.16 | +0.7 | 0.67 | 0.73 |
| TRA (pan-trophoblast) | 21 | −0.005 | 3/10 | 0.49 | −0.2 | 0.73 | 0.73 |

Every patient moves the same way on all five regenerative sets and on both
proliferative sets. Across all four regions (Friedman, 9 patients with complete
region coverage), every fetal/revival set peaks at the **invasive front**
(q ≤ 2×10⁻⁴) and proCSC and proliferation peak at the **tumour core**
(q = 0.003 and 0.005).

**This is compartment-specific.** In PanCK⁻ stroma from the same ROIs, IFA,
revCSC, Yui-fetal and Ayyaz-revival are all flat (Δ ≈ 0, 3–5/10 patients, all
P null ≥ 0.87). What does move in stroma is proCSC (−0.082, 0/10) and
proliferation (−0.050, 0/10). So the fetal/revival gain is a property of the
tumour epithelium at the front, not of bulk tissue composition.

### 1.2 The placenta axes are not enriched anywhere

Across both panels, both compartments and all four regions, no trophoblast set
is enriched at the invasive front:

- CTA, epithelium: TRA −0.005 (3/10, P null 0.73), placenta-trophoblast +0.010 (P null 0.67), EVT −0.020 (P null 0.36).
- WTA, epithelium, full gene coverage (TRA 228/234 genes, placenta 39/41): TRA −0.007 with **1/10 patients positive** (P paired 0.006 — significantly *down*), placenta −0.003 (3/10), EVT +0.003 (6/10), none passing the matched null.
- CTA, stroma: TRA −0.033, 0/10 patients, P null 0.025 — significantly depleted at the front.

One trap worth recording. In the looser contrast of invasive front against the
*mean of the other three regions*, the placenta-trophoblast set rises in **9/9
patients** (+0.026, P = 0.004, BH q = 0.010) — a result that would read as a
clean positive. It does not survive the matched null (z = +0.83, P null = 0.43),
whereas revCSC (z = +3.1), IFA (z = +5.3), YAP regeneration (z = +8.0),
Yui-fetal (z = +5.6) and Ayyaz-revival (z = +4.7) all do. The 9/9 consistency
reflects generic expression drift from normal tissue into tumour, which any set
of tumour-expressed genes shows. This is the same failure mode the project's
earlier "placenta-like" claim ran into, reproduced here in a new cohort.

**Power caveat.** On the CTA panel the trophoblast sets are small (7–21 genes),
so that cohort alone could not have detected a modest effect. The WTA cohort
carries near-complete coverage and is the one that matters for the negative
claim, and it is negative.

### 1.3 Cross-panel discordance, stated plainly

The CTA and WTA runs are different patients profiled on different panels, and
they do not agree equally on everything.

| Contrast | CTA (exp1) | WTA (exp2, T1 only, n = 9) |
|---|---|---|
| YAP regeneration | +0.063, 10/10, P null 0.005 | +0.012, 8/9, P null 0.005 |
| revCSC | +0.044, 10/10, P null 0.010 | +0.012, 6/9, P null 0.040 |
| proCSC | −0.084, 1/10, P null 0.005 | −0.013, 2/9, P null 0.080 |
| Lgr5CSC | (20 genes) | −0.014, 2/9, P null 0.040 |
| proliferation | −0.070, 1/10, P null 0.005 | −0.016, 3/9, P null 0.005 |
| IFA | +0.034, 10/10, P null 0.005 | +0.003, 6/9, P null 0.80 |
| revival (Ayyaz) | +0.027, 10/10, P null 0.005 | **−0.010, 2/9, P null 0.005** |
| fetal (Yui) | +0.026, 10/10, P null 0.005 | −0.001, 4/9, n.s. |

The **proliferative → YAP-regenerative / revCSC rebalancing replicates in both
cohorts**. The broad fetal-intestinal sets replicate strongly only in CTA, and
the Ayyaz revival set reverses sign in WTA. Two sensitivity arms were run and
neither rescues the discordance: scoring the WTA matrix restricted to the CTA
target space (so that rank-based scoring uses the same reference frame) recovers
YAP regeneration (P null 0.02) but not IFA or the fetal sets; and the WTA object
is already QC-filtered (18,441/18,441 targets detected in ≥10% of segments), so
the gap is not undetected-target dilution. Note that the paper's own
invasive-front oncofetal GSEA (its Extended Data Fig. 1j) is run on the CTA
cohort, so our exp1 result replicates the authors' analysis and exp2 does not
reproduce it either.

**Claim ceiling for Q1.** Supported: *in early-stage CRC, tumour epithelium at
the invasive front runs a YAP-regenerative/revCSC programme where the core runs a
proliferative/proCSC one; this is epithelium-specific and survives matched-null
calibration in two independent cohorts.* These are bulk segments compared across
space, so this is regional difference, NOT plasticity: no cell is observed
changing state, and nothing here licenses "state switching". Supported:
*trophoblast and placenta programmes are not stably enriched at the invasive
front in either cohort.* NOT supported, and corrected from the first draft: that
trophoblast programmes are absent from these tumours. The negative is specific to
invasive-front enrichment of trophoblast-IDENTITY axes in bulk segments; it does
not test whether a minority oncofetal subpopulation runs a placenta-like
IMMUNE-TOLERANCE programme, which is a different gene set and needs a
cell-state-resolved test. Not supported: that the fetal-intestinal axis
specifically is enriched in *all* early CRCs — that holds in the CTA cohort only.

---

## Q2 — Is there a TWEAK–TWEAKR circuit, and where do the ligands come from?

**Data.** Early-CRC TME scRNA-seq (SORT-seq), 2,409 cells, 5 patients, regions
normal / core / invasive front. This is a **sorted microenvironment** dataset:
tumour epithelium was excluded, so the receptor-bearing compartment is not in it.
The epithelial side comes from the GeoMx segments above.

### 2.1 TWEAK has no cellular source — in a fourth independent cohort

*TNFSF12* is detected at a nearly identical rate in every TME cell type:
trophocyte-like CAF MMP⁻ 38.0%, trophocyte-like CAF MMP⁺ 35.7%, trophocyte
34.4%, telocyte 33.9%, **macrophage 33.7%**, pericytes 33.5%, endothelial tip
31.6%. Expressed as a source decomposition, macrophages contribute **7.1%** of
all ligand-positive cells — behind pericytes (15.0%), myofibroblast.1 (12.0%),
telocytes (7.7%), CD8 T cells (7.5%) and Tregs (7.5%) — roughly their share of
the dataset. Across the 5 patients, the top-ranked *TNFSF12* source is a
different cell type every time (macrophage, pericyte, telocyte, trophocyte-like
CAF MMP⁺, MKI67⁺ lymphocyte: 1 patient each).

*TGFB1*, by contrast, **does** have sources: telocyte-like CAF 92.3%,
trophocyte-like CAF MMP⁺ 73.8%, endothelial tip 60.5%, macrophage 46.2% versus
~20–37% elsewhere. So the flatness of *TNFSF12* is not a limitation of the assay
or of the cell-type labels — the same cells, scored the same way, show clear
structure for a different ligand.

This independently reproduces the manuscript's position that TWEAK is
multi-sourced and that "macrophage-derived TWEAK" is not supportable.

### 2.2 IL36G is absent from the microenvironment

*IL36G* is detected in **0 of 2,409 cells**, in every cell type. IL-36γ is an
epithelial cytokine and this dataset has no epithelium, so its source cannot be
addressed here. In the GeoMx data it is on the WTA panel only (not CTA) and
rises at the invasive front in the **stromal** compartment (+0.33, 9/10 patients,
P = 0.020) with a weaker epithelial trend (+0.12, 8/10, P = 0.19). Treat the
IL36G question as **unanswered** pending the CosMx analysis.

### 2.3 Nothing regional in the TME ligands themselves

Patient-paired invasive front vs core across all TME cells: no gene reaches
significance after BH (*TNFSF12* P = 0.63, *TGFB1* P = 1.0, *TGFB3* P = 0.44,
ANXA1 P = 0.063). With 5 patients this is underpowered; it is reported as a
non-result, not as evidence of absence.

### 2.4 The receptor is where the manuscript says it is

This is the strongest new result in the GeoMx data. Invasive front vs core,
patient-paired, CTA cohort, **tumour epithelium**:

| Gene | Δ (log) | patients up | P | BH q |
|---|---|---|---|---|
| MMP7 | +1.05 | 10/10 | 0.0020 | 0.004 |
| LAMC2 | +0.95 | 10/10 | 0.0020 | 0.004 |
| **TNFRSF12A** | **+0.46** | **10/10** | **0.0020** | **0.004** |
| TGFB3 | +0.18 | 9/10 | 0.0039 | 0.006 |
| TGFB1 | +0.13 | 8/10 | 0.16 | 0.19 |
| **TNFSF12** | **+0.025** | **5/10** | **0.63** | **0.63** |

*TNFRSF12A* rises at the invasive front in every single patient, in the same
tier as MMP7 and LAMC2 — the two markers the authors use to define the oncofetal
front — while its ligand is flat and splits 5/5. The receptor also rises more
modestly in stroma (+0.15, 8/10, q = 0.027); the ligand does not (7/10, q = 0.28).
In the WTA cohort the receptor is directionally up but not significant (+0.17,
7/10, P = 0.32) and *TNFSF12* is weakly up (+0.25, 9/10, P = 0.049, BH q = 0.13) —
the one place in this analysis where the ligand shows regional structure, and it
does not replicate in CTA.

**Claim ceiling for Q2.** Supported: *TNFRSF12A marks the invasive front of
early-stage CRC epithelium in 10/10 patients, co-ordinately with MMP7 and LAMC2*;
and *TNFSF12 is broadly expressed across stromal and immune populations without
a dominant, macrophage-specific source in this dataset, while TGFB1 in the same
cells is strongly source-structured*. NOT supported, and corrected from the first
draft: "TWEAK has no cellular source" — the ligand is detected in roughly a third
of the cells of most cell types, and 5 patients / 2,409 sorted cells cannot
exclude a macrophage contribution confined to particular patients, to a subset
this sort under-samples, or to a compartment dissociation discards. Also not
supported: any ligand-driven mechanism, since co-expression carries no direction,
and the two cohorts disagree on whether *TNFSF12* is regionally patterned.

**Circularity, found in review.** TNFRSF12A is a member of the revCSC gene set
(1 of 32; 1 of the 12 on the CTA panel, 1 of 29 on WTA). The Q1 revCSC result and
the Q2 receptor result are therefore one observation reported twice. Removing the
gene and rescoring leaves revCSC essentially unchanged (exp1 PanCK+ Δ +0.0423 vs
+0.0443, 10/10 patients, matched-null P = 0.005; `Q5_revCSC_leaveout_TNFRSF12A.tsv`),
so the programme-level result does not depend on the receptor — but they must not
be presented as converging evidence.

---

## Q3 — Do TWEAK⁺ macrophages co-emerge and colocalise with oncofetal cells?

**Data.** CosMx run 2 (the paper's Fig. 5 dataset): 1,257,627 QC-passing cells,
6,175-gene panel, 11 non-metastatic early CRCs at three pseudotimed substages —
intramucosal (n = 3), T1 sm1 (n = 5), T1 sm3 (n = 3). *TNFSF12*, *TNFRSF12A*,
*TGFB1*, *TGFB3* and *IL36G* are all on the panel. Oncofetal cells are the
authors' own `cellType` label (15,927 cells); tumour epithelium is CRC +
oncofetal (417,238 cells); macrophages, 30,601.

### 3.1 Co-emergence: the oncofetal state tracks pseudostage, the ligands do not

The positive control behaves: the oncofetal fraction of tumour epithelium rises
across the pseudotime axis (Spearman ρ = 0.62, P = 0.040), and the two tumours
with **zero** oncofetal cells are both intramucosal — reproducing the paper's
central co-emergence claim.

Against that axis, no ligand measure survives correction (BH over 10 measures):

| Measure | ρ vs oncofetal fraction | P | ρ vs pseudostage | P |
|---|---|---|---|---|
| *TNFSF12*⁺ of all cells | +0.52 | 0.098 | +0.19 | 0.57 |
| *TNFSF12*⁺ of macrophages | +0.11 | 0.74 | +0.08 | 0.82 |
| *TGFB1*⁺ of all cells | +0.51 | 0.105 | +0.39 | 0.24 |
| *TGFB1*⁺ of macrophages | +0.44 | 0.17 | −0.04 | 0.91 |
| *TGFB3*⁺ of all cells | +0.51 | 0.105 | +0.43 | 0.19 |
| *IL36G*⁺ of all cells | +0.39 | 0.24 | +0.08 | 0.82 |
| *IL36G*⁺ of macrophages | −0.50 | 0.12 | −0.82 | 0.0021 (q = 0.023) |
| *TNFRSF12A*⁺ of all cells | +0.21 | 0.55 | +0.54 | 0.083 |
| *TNFRSF12A*⁺ of macrophages | +0.23 | 0.49 | +0.58 | 0.059 |

The *TWEAK⁺ macrophage* fraction is essentially constant across the whole series
(6.9–9.8% of macrophages in every tumour, including the two with no oncofetal
cells at all). Whatever brings oncofetal cells into existence, the abundance of
TWEAK⁺ macrophages is not tracking it. The only BH-significant result is *IL36G*
in macrophages going **down** with pseudostage, which has no mechanistic reading
and is reported because it is in the table, not because it is believed.
*TNFRSF12A*⁺ fraction rising with pseudostage (ρ = 0.54–0.58, P ≈ 0.06–0.08) is
the one trend pointing the way the manuscript would predict, and it does not
reach significance in 11 tumours.

### 3.2 Colocalisation: no ligand-specific proximity, and a trap worth recording

Test: for every tumour-epithelial cell, count ligand⁺ neighbours within 50 µm;
compare oncofetal against other tumour epithelium; null permutes the ligand⁺
label among cells of the same class within the same field of view.

Using the authors' oncofetal label (9 tumours with enough cells on both sides):

| Ligand | Source | tumours with z > 0 | median z | P |
|---|---|---|---|---|
| *TNFSF12* | macrophages | 3/9 | −0.13 | 0.73 |
| *TNFSF12* | all cells | 6/9 | +1.51 | 0.25 |
| *TGFB1* | macrophages | 6/9 | +0.28 | 0.65 |
| *TGFB1* | all cells | 4/9 | −0.16 | 1.00 |
| *IL36G* | macrophages | 7/9 | +0.75 | 0.20 |
| *TGFB3* | all cells | 4/9 | −1.03 | 0.43 |

Nothing. **TWEAK⁺ macrophages are not preferentially found next to oncofetal
tumour cells.**

The trap: if oncofetal cells are instead defined by a revCSC score decile, the
same test returns *every* ligand as strongly colocalised — 11/11 tumours,
median z 4.6 (*IL36G*) to 7.3 (*TGFB1*), permutation P < 0.005 throughout. That
result is false. Running twelve non-ligand control genes matched to *TNFSF12* on
detection rate (0.038–0.048 vs 0.046) through the identical test gives **higher**
z than the ligands: median z 7.8 for controls vs 6.3 for ligands, with SHC1
(11.7), ESYT1 (11.5), PPP3CA (11.4) and UBQLN2 (11.4) all positive in 11/11
tumours. Cells that score high on any expression signature sit where transcript
detection is dense, so they have more neighbours positive for anything. Under the
authors' label the controls and the ligands are likewise indistinguishable
(median z: controls −0.61, ligands +0.12; the top-ranked gene of all sixteen is
the control PPP3CA at +2.08, ahead of *TNFSF12* at +1.79).

This is the single most useful methodological result here: **a signature-score
threshold plus a within-FOV label permutation is not a sufficient control for
spatial colocalisation in imaging-based spatial data.** Any colocalisation claim
in the manuscript built that way needs a detection-matched control gene panel.

**Claim ceiling for Q3.** Supported: *oncofetal tumour cells emerge with
pseudostage and are absent from two of three intramucosal carcinomas.* Supported
as a bounded negative: *no cross-patient-stable, ligand-specific proximity between
TWEAK⁺ macrophages and oncofetal cells is detectable above the matched spatial
background, at 20, 50 or 100 µm, and conditioning on receptor-positive oncofetal
cells does not recover one.* NOT supported, and corrected from the first draft:
"TWEAK⁺ macrophages do not colocalise with oncofetal cells" as an unqualified
statement. Two of eleven tumours cannot enter the test; transcript detection is
not protein availability; a whole-tumour average dilutes a local niche. Not
supported: any colocalisation claim derived from a score-threshold definition
without detection-matched controls.

---

## Q4 (added in review) — Is TNFRSF12A specific to the oncofetal cell state?

The Q2 result is regional and cannot distinguish a receptor that marks the
oncofetal state from one raised in every invasive epithelial state. Tested in
CosMx by comparing oncofetal with other malignant epithelial cells **within the
same tumour, the same field of view and the same detection quintile**, with the
authors' oncofetal label (independent of our gene sets) and with twelve
detection-matched control genes carried through the same pipeline
(`Q6_*`, Fig. EC4a,b).

Stratification balanced depth exactly (oncofetal/comparison depth ratio 1.00).
TNFRSF12A is higher in oncofetal cells in **7 of 8** evaluable tumours: median
+3.18 percentage points of detection, Δlog +0.097, Cliff's δ +0.044, Wilcoxon
P = 0.016, BH q = 0.19 over 17 genes. Control genes: median effect +0.014, max
+0.027, none significant; the receptor exceeds all twelve controls in **6 of 8**
tumours (z +2.4 to +24.1). The two exceptions include the tumour whose epithelium
is 87% oncofetal, where almost no comparison cells remain.

Sensitivity with a revCSC decile (TNFRSF12A removed from the set): 11/11 tumours,
+5.63 points, Δlog +0.112, δ +0.077, P = 0.00098, q = 0.008, receptor above all
twelve controls in 11/11. That arm retains an 11% depth imbalance, so it is
reported as supporting, not primary.

**Claim ceiling.** Supported: *TNFRSF12A expression is associated with the
oncofetal cell state, not only with the invasive front.* Not supported: receptor
protein, receptor clustering, pathway activity, or any temporal ordering between
receptor and state.

## Q5 (added in review) — Where does the EC3c inflation come from?

Audit of the score-threshold colocalisation positive, at 20/50/100 µm, under four
definitions, with FOV × detection-quintile stratification and a depth-,
complexity- and area-residualised score (`Q7A_*`, Fig. EC4c).

| Definition (50 µm, all-cell sources) | median z, controls | median z, ligands |
|---|---|---|
| revCSC decile, unstratified (as published in EC3c) | +7.8 | +6.3 |
| revCSC decile + FOV × depth strata | +1.48 | +0.91 |
| score residualised on depth, genes, area + strata | +1.13 | +0.75 |
| authors' label + strata | −0.93 | −0.33 |

Conclusions: (i) the positive is not ligand-specific under any definition or
radius — controls match or exceed ligands throughout; (ii) stratifying on field
and detection quintile removes most of the inflation, from z ≈ 7.8 to ≈ 1.5;
(iii) residualising the score adds little and changes decile membership by only
8%; (iv) a residual bias of ≈ +1 to +1.7 z persists under score-based
definitions and **grows with radius**, which points to tissue architecture —
signature-high cells clustering in locally dense regions — rather than to
sequencing depth alone. Neighbour-cap truncation is negligible (≤ 0.07% of query
cells at 100 µm).

**Claim ceiling.** Supported: *the score-threshold colocalisation positive lacks
ligand specificity, and most of it is attributable to within-field detection
density.* NOT supported, and corrected from the first draft: calling it simply
"an artefact" — the residual, radius-growing component is not explained by
detection depth and has not been fully characterised.

## Q6 (added in review) — Is there a receptor-conditioned niche?

Among oncofetal cells only, do TNFRSF12A⁺ cells have more TNFSF12⁺ macrophage
neighbours than TNFRSF12A⁻ cells (`Q7B_*`, Fig. EC4d)? At 20/50/100 µm with the
same stratification and null: 5/9, 4/9 and 2/9 tumours positive, median z +0.06,
−0.15, −0.37, P ≥ 0.43; control genes indistinguishable; nothing significant
after correction in any of the 96 gene × radius × source combinations.

**Decision.** Negative. Per the review's stopping rule, this line is closed: no
further ligand-receptor prediction, no further source hunting in the 2,409-cell
dataset, no further regional placenta contrasts.

## What this cohort does and does not do for the manuscript

| Manuscript claim | Verdict here |
|---|---|
| Tumour epithelium re-engages fetal/regenerative, **not** trophoblast, programmes | **Supported for invasive-front enrichment.** Trophoblast identity axes null or negative in both GeoMx cohorts, with full gene coverage in one. Does not test a cell-state-specific placenta-like immune-tolerance programme. |
| The programme is organised toward the invasive front | **Supported**, epithelium-specific, 10/10 patients, matched-null calibrated. |
| proCSC ↔ revCSC rebalancing | **Supported** in both cohorts. |
| TNFRSF12A marks the revival state | **Supported** — +0.46 log at the invasive front in 10/10 patients, alongside MMP7 and LAMC2. |
| TWEAK has no single cellular source | **Supported** in a fourth independent cohort; TGFB1 in the same cells shows clear sources, so this is not an assay limitation. |
| Macrophage-derived TWEAK drives the oncofetal state | **Not supported.** No co-emergence, no ligand-specific proximity at 20/50/100 µm, none after conditioning on receptor-positive cells, flat TWEAK⁺ macrophage fraction across the series. This bounds the claim; it does not disprove TWEAK signalling. |
| TNFRSF12A marks the oncofetal cell *state*, not just the region | **Supported** at single-cell resolution: 7/8 tumours, above all 12 detection-matched controls in 6/8. |
| Fetal-intestinal (IFA) axis specifically | **Partly supported** — strong in the CTA cohort, absent in the WTA cohort. |

---

## Open items

1. The CTA/WTA discordance on the fetal-intestinal sets is unexplained. The two
   runs are different patients, so a cohort difference is as plausible as a
   technical one. Worth checking whether metastatic status (exp2 contains three
   T1N0M1 tumours) accounts for it.
2. The region-vs-rest contrast in `Q1b_*` is deliberately *not* null-calibrated;
   `Q1c_*` calibrates it. Do not quote `Q1b` numbers on their own.
3. *IL36G* is absent from the CTA panel and from the sorted TME, so only the WTA
   and CosMx data speak to it.
4. The small CTA gene-set sizes (proCSC 8, revCSC 12, placenta 7, EVT 8) mean the
   CTA cohort's *negative* trophoblast result is underpowered on its own.
5. One CosMx tumour (T1_NANO_023, T1 sm3) is 87.0% oncofetal by the authors' own
   label, against 0–25% in the other ten. Either that tumour is genuinely
   dominated by the state or its epithelial sub-clustering went wrong. The
   co-emergence correlations should be re-checked with it excluded.
6. One intramucosal tumour (T1_NANO_026) carries 23.0% oncofetal cells, which sits
   uneasily with the paper's statement that oncofetal states are absent before
   invasion. Worth raising if this cohort is cited.
7. Script `03b`/`07` should be generalised into a reusable detection-matched
   control for every spatial colocalisation claim in the manuscript, not just
   this one. The residual radius-growing bias in Q5 is unexplained and would
   need a density- or architecture-aware null to characterise.
8. The Q4 primary result sits at BH q = 0.19 with 8 tumours. It is consistent
   and far outside the control-gene distribution, but it is not a
   multiplicity-corrected significant finding and should not be reported as one.
   A larger oncofetal-labelled cohort would settle it.
9. Q4 assumes the authors' oncofetal label, derived from the published
   high-relapse-cell signature, does not itself contain TNFRSF12A. That gene list
   is not in the paper's text and we could not verify it. If it does, Q4 is
   circular and must be withdrawn — worth one email to the authors.
10. Closed by the review's stopping rule: further ligand-receptor prediction
    (CellChat/CellPhoneDB/NicheNet), further TNFSF12 source hunting in the
    2,409-cell dataset, further regional placenta contrasts, and further generic
    spatial colocalisation maps.
11. Nothing here has been reviewed or merged; per the repository rules these
    results are not canonical manuscript evidence yet.
