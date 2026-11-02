# Results — An independent early-stage CRC cohort ties TWEAKR to the oncofetal state and withholds support from a macrophage-TWEAK niche

*Draft section for the TWEAKR manuscript. Figures: `../figures/Fig_EC1…EC4`.
Statistics in `../tables/`, methods and claim ceilings in `findings.md`.*

---

## The invasive front carries a different stem programme from the tumour core, and not a placental one

To test the manuscript's spatial claims in tissue the laboratory had no part in
generating, we re-analysed a published atlas of early-stage colorectal cancer
that captures the earliest moment of invasion (Buissant des Amorie *et al.*,
*Nature* 2026). Two GeoMx bulk spatial runs profile tumour epithelium (PanCK⁺)
and microenvironment (PanCK⁻) separately along the sequence normal → adenoma →
tumour core → invasive front: a cancer transcriptome panel in ten patients
(1,781 targets) and a whole transcriptome panel in ten more (18,441 targets).
Because segments are repeatedly sampled within a tumour, every statistic below
takes the patient as its unit, and every regional effect is additionally
calibrated against 200 expression-matched random gene sets of the same size —
without that calibration, gene sets that merely drift with malignancy pass as
spatially organised programmes.

Tumour epithelium at the invasive front carries a reproducible shift (Fig. EC1a,
EC1b). Relative to the tumour core of the same patient, the YAP-regeneration,
revCSC, fetal-intestinal, revival-stem and fetal-intestine signatures all rise
in **10 of 10 patients** (Δ = +0.063, +0.044, +0.034, +0.027 and +0.026;
P = 0.002 each; all passing the matched null at P ≤ 0.010), while proliferation
and proCSC fall in 9 of 10 (Δ = −0.070 and −0.084, P = 0.0098, matched-null
P = 0.005). Across all four regions the fetal and revival sets peak at the
invasive front and the proliferative sets peak in the core (Friedman,
BH q ≤ 0.005, nine patients with complete region coverage). The front is
therefore not simply "more tumour-like" than the core: the two stem programmes
move in opposite directions across the same tissue.

We state this as regional difference, not as plasticity. These are bulk segments
compared across space within a patient, so they establish that invasive front and
tumour core run different transcriptional programmes. They cannot show that
individual cells converted from one state to the other; no lineage, time course
or clonal information enters this analysis.

The shift belongs to the epithelium. In PanCK⁻ segments from the same regions of
interest, the fetal-intestinal, revCSC, fetal-intestine and revival-stem scores
are flat (|Δ| ≤ 0.005, 3–5 of 10 patients, matched-null P ≥ 0.87), whereas
proCSC and proliferation fall in 0 of 10 (Fig. EC1c). A change in bulk tissue
composition at the invasive front cannot produce that pattern.

No trophoblast programme is stably enriched at the front (Fig. EC1d). In the epithelium of the
cancer-panel cohort the pan-trophoblast axis, the curated placenta-trophoblast
set and the extravillous-trophoblast set are all unmoved (Δ = −0.005, +0.010,
−0.020; matched-null P = 0.73, 0.67, 0.36). The whole-transcriptome cohort,
which carries near-complete coverage of these sets (228 of 234 and 39 of 41
genes), is likewise negative, with the pan-trophoblast axis rising in **1 of 10**
patients (P = 0.006 in the opposite direction); in its microenvironment the axis
is significantly depleted at the front (Δ = −0.033, 0 of 10 patients,
matched-null P = 0.025). Restricting to the nine T1 tumours, as the original
authors do, does not change this.

The scope of that negative needs stating precisely, because it is narrower than
it first appears. What fails here is the proposition that trophoblast programmes
are a general feature of the invasive front. It is not a demonstration that
trophoblast-associated transcription is absent from these tumours, and it does
not test the hypothesis the placenta work was built around — that a particular
oncofetal subpopulation runs a placenta-like immune-tolerance programme. Bulk
segments averaging hundreds of cells cannot detect a programme confined to a
minority state, and the immune-tolerance axis is a different gene set from the
trophoblast-identity axes tested here. That hypothesis remains open and needs a
cell-state-resolved test, not another regional contrast.

One negative result is worth stating explicitly because it would have been a
positive under a looser design. Contrasting the invasive front against the mean
of the other three regions — rather than against the core — the
placenta-trophoblast set rises in **9 of 9 patients** (Δ = +0.026, P = 0.004,
BH q = 0.010). It does not survive the matched null (z = +0.83, P = 0.43), while
revCSC (z = +3.1), the fetal-intestinal axis (z = +5.3), YAP regeneration
(z = +8.0) and fetal intestine (z = +5.6) all do. Perfect cross-patient
consistency against a background that includes normal tissue reflects generic
expression drift into tumour, which any tumour-expressed gene set reproduces.

## TNFRSF12A marks the invasive front; TWEAK is broadly expressed without a dominant source

Within the same patient-paired design, *TNFRSF12A* rises at the invasive front of
tumour epithelium in **10 of 10 patients** (+0.46 log, BH q = 0.004), placing it
in the same tier as *MMP7* (+1.05) and *LAMC2* (+0.95) — the two markers the
original authors use to define the oncofetal front — and above *TGFB3* (+0.18,
9 of 10, q = 0.006). Its ligand does not move: *TNFSF12* is +0.02 log and splits
5 of 10 (q = 0.625) (Fig. EC2a). The receptor rises more modestly in the
microenvironment as well (+0.15, 8 of 10, q = 0.027); the ligand does not
(7 of 10, q = 0.28).

These two results are not independent and must not be presented as mutual
corroboration: *TNFRSF12A* is itself a member of the revCSC gene set, one of the
twelve revCSC genes carried on the cancer panel. Removing it and rescoring, the
revCSC enrichment at the front is essentially unchanged (Δ = +0.042 versus
+0.044, still 10 of 10 patients, matched-null P = 0.005), so the programme-level
result does not rest on the receptor — but the programme and the gene are one
observation reported two ways, not two converging lines of evidence.

Plate-based scRNA-seq of the sorted microenvironment from the same study
(2,409 cells, 5 patients) shows why the ligand carries little spatial
information: it is expressed broadly, without a dominant cell type of origin
(Fig. EC2b, EC2c). *TNFSF12* detection is
near-identical in every cell type — trophocyte-like CAF MMP⁻ 38.0%, MMP⁺ 35.7%,
trophocyte 34.4%, telocyte 33.9%, **macrophage 33.7%**, pericyte 33.5% — and
macrophages supply **7.1%** of all ligand-positive cells, behind pericytes
(15.0%) and myofibroblasts (12.0%) and close to their share of the dataset.
Across the five patients the top-ranked source is a different cell type each
time. This is not an assay limitation: *TGFB1*, scored identically in the same
cells, is strongly source-structured (telocyte-like CAF 92.3%, trophocyte-like
CAF MMP⁺ 73.8%, endothelial tip 60.5%, macrophage 46.2%). *IL36G* is detected in
0 of 2,409 cells, consistent with an epithelial origin that this sorted dataset
cannot sample.

The claim this supports is that *TNFSF12* expression is distributed across
stromal and immune populations without a dominant, macrophage-specific source in
this dataset. It is not a claim that TWEAK has no source, which the data
contradict — the ligand is detectable in a third of the cells of most cell types.
Nor does it exclude a macrophage contribution that matters: five patients and
2,409 microenvironmental cells cannot rule out a source confined to particular
patients, to a macrophage subset that this sorting strategy under-samples, or to
a spatial compartment that dissociation discards.

## TNFRSF12A is enriched in oncofetal cells themselves, not only in the region they occupy

A regional result cannot distinguish a receptor that marks the oncofetal state
from one raised in every invasive epithelial state. We therefore moved to the
single-cell spatial cohort and asked the cell-state question directly, comparing
*TNFRSF12A* between oncofetal and other malignant epithelial cells **within the
same tumour, the same field of view and the same transcript-detection quintile**
(Fig. EC4a, EC4b). Normal and undefined epithelium were excluded. The oncofetal
label is the original authors', derived from the published high-relapse-cell
signature rather than from any gene set of ours — necessary here, because
defining the state with revCSC and then testing *TNFRSF12A* would be circular.
Twelve non-ligand control genes matched to *TNFSF12* on detection rate run
through the identical pipeline, so the receptor is read against what an
arbitrary gene of similar abundance produces under the same stratification.

Stratification balanced the confounder it was built for: oncofetal and
comparison cells differ in mean detection depth by a factor of 1.00. Against
that background *TNFRSF12A* is higher in oncofetal cells in 7 of 8 evaluable
tumours (median +3.18 percentage points of detection, median Δlog = +0.097,
Cliff's δ = +0.044, Wilcoxon P = 0.016, BH q = 0.19 across the seventeen genes
tested). The control genes place that effect: their median effect is +0.014 and
their largest is +0.027, none significant, and in **6 of 8 tumours the receptor
exceeds all twelve controls** (z = +2.4 to +24.1 against the control
distribution). The two exceptions are informative rather than fatal — one is the
tumour whose epithelium is 87% oncofetal by the authors' label, where the
contrast has almost no comparison cells left.

The same test under a revCSC score decile with *TNFRSF12A* removed from the set
gives a stronger result across all eleven tumours (11 of 11 positive, median
+5.63 percentage points, Δlog = +0.112, δ = +0.077, P = 0.00098, q = 0.008), and
there the receptor exceeds all twelve control genes in **11 of 11 tumours**.
That arm retains an 11% residual depth imbalance after stratification, so we
report the authors'-label result as primary and this one as supporting.

This is the strongest statement the data license: *TNFRSF12A* expression is
associated with the oncofetal cell state, not merely with the invasive front.
It remains an association. Receptor transcript abundance is not receptor
protein, not receptor clustering and not pathway activity, and nothing here
orders the receptor and the state in time.

## No cross-patient-stable TWEAK⁺ macrophage–oncofetal association is detectable

The decisive test is the single-cell spatial arm: 1,257,627 cells on a
6,175-gene panel across eleven non-metastatic tumours staged immediately before
and after malignant transformation (intramucosal, n = 3; T1 sm1, n = 5;
T1 sm3, n = 3). *TNFSF12*, *TNFRSF12A*, *TGFB1*, *TGFB3* and *IL36G* are all on
the panel, and the original authors' own epithelial sub-clustering supplies the
oncofetal label, so neither the gene panel nor the cell-state definition is ours.

The positive control behaves as published: the oncofetal fraction of tumour
epithelium rises across the pseudotime axis (Spearman ρ = +0.62, P = 0.040), and
the two tumours containing no oncofetal cells at all are both intramucosal
(Fig. EC3a). Against that axis the TWEAK⁺ macrophage fraction is flat — 6.9% to
9.8% of macrophages in every tumour, including the two with no oncofetal cells
(ρ = +0.08 versus substage, P = 0.82; ρ = +0.11 versus the oncofetal fraction,
P = 0.74). No ligand measure survives correction. The only measure trending the
way a ligand-driven model predicts is the *TNFRSF12A*⁺ fraction rising with
substage (ρ = +0.54, P = 0.083), which does not reach significance in eleven
tumours.

Nor is there detectable ligand-specific proximity (Fig. EC3b). Counting ligand-positive
neighbours within 50 µm of every tumour-epithelial cell and comparing oncofetal
against other tumour epithelium — with the ligand-positive label permuted among
cells of the same class within each field of view, so that the test measures
*ligand-specific* proximity rather than proximity to macrophages — *TNFSF12*⁺
macrophages are enriched around oncofetal cells in 3 of 9 evaluable tumours
(median z = −0.13, P = 0.73). *TGFB1*, *TGFB3* and *IL36G* are equally negative.

This is a bounded negative, and we state its bounds. It argues against a
*general* TWEAK⁺ macrophage–oncofetal niche: one that would be visible as a
cross-patient-stable excess of ligand-positive neighbours above the matched
spatial background. It does not exclude TWEAK signalling. Two of eleven tumours
carry too few oncofetal cells to enter the test; transcript detection is not
protein availability, and a ligand that is secreted, cleaved and diffusible need
not be transcribed by the cell that delivers it; 50 µm is one pre-chosen scale;
and a whole-tumour average will dilute a niche confined to a small region. The
proposition that survives is that ligand–receptor co-occurrence cannot carry the
mechanistic claim, not that the interaction does not occur.

Two things had to be checked before that negative could be trusted: that it is
not an artefact of the single 50 µm radius, and that the comparison is not
confounded by transcript-detection depth. Repeating the test at 20, 50 and
100 µm, with the comparison stratified by field of view **and** detection
quintile, leaves it unchanged: *TNFSF12*⁺ macrophages are enriched around
oncofetal cells in 5 of 8, 5 of 8 and 6 of 8 tumours (median z = +0.42, +0.34,
+0.34; P ≥ 0.38), and at every radius the ligands sit *below* the twelve control
genes (median z: ligands −0.12, +0.09, +0.20; controls +0.07, +0.26, +0.40).

## A signature-score definition of cell state inflates spatial colocalisation

The same analysis exposed a methodological problem that we think is the most
transferable result here (Fig. EC3c, EC4c). Defining oncofetal cells by a revCSC
score decile instead of by the authors' label turns the identical test strongly
positive for **every** ligand — 11 of 11 tumours, median z 4.6 to 7.3,
permutation P < 0.005. Twelve non-ligand control genes matched to *TNFSF12* on
detection rate (0.041–0.047 versus 0.046) score *higher* than the ligands under
that definition (median z 7.8 versus 6.3), with SHC1, ESYT1, PPP3CA and UBQLN2
each positive in 11 of 11 tumours.

The positive is therefore not ligand-specific, and it is acutely sensitive to how
the cell state is defined. We audited where it comes from. Stratifying the
comparison by field of view and detection quintile removes most of it: the median
control z falls from +7.8 to **+1.5** at 50 µm. Additionally regressing per-cell
transcript count, detected-gene count and cell area out of the score before
taking the decile adds little beyond that (+1.1), and changes the decile
membership by only 8%. Under the authors' label the same stratified test is
centred below zero (median control z −0.93).

So detection density accounts for most of the inflation but not all of it: a
residual bias of roughly +1 to +1.7 z persists under score-based definitions
after both corrections, and it grows with radius, which points to tissue
architecture — signature-high cells clustering in locally dense regions — rather
than to sequencing depth alone. We therefore state this as a demonstrated lack
of ligand specificity with a largely identified cause, not as a fully
characterised artefact. The practical consequence stands either way: a
signature-score threshold combined with a within-field label permutation is not
an adequate control for colocalisation in imaging-based spatial transcriptomics,
and any such claim needs detection-matched control genes carried through the same
pipeline.

## No receptor-conditioned niche either

A whole-tumour average can hide a small local structure, so we asked the
narrower question the data can still answer: among oncofetal cells only, do the
*TNFRSF12A*-positive ones sit closer to *TNFSF12*-positive macrophages than the
*TNFRSF12A*-negative ones do (Fig. EC4d)? Stratified by field of view and
detection quintile, at 20, 50 and 100 µm, the answer is no — 5 of 9, 4 of 9 and
2 of 9 tumours positive (median z = +0.06, −0.15, −0.37; P ≥ 0.43), with the
control genes again indistinguishable and nothing significant after correction
in any of the 96 gene × radius × source combinations tested. Conditioning on the
receptor does not recover a niche, and on the strength of this we are closing
this line rather than subdividing further.

## Summary

In an external cohort of twenty bulk-profiled tumours across two runs (nineteen
of them stage T1) and eleven single-cell-profiled early colorectal cancers, the invasive front is defined by a proliferative →
YAP-regenerative/revCSC rebalancing of the tumour epithelium, *TNFRSF12A* marks
that front in every patient examined, and TWEAK is a uniformly expressed ligand
with no cellular source, no co-emergence with the oncofetal state and no spatial
association with it. The trophoblast and placenta programmes are absent from the
front in both bulk cohorts. The one claim this cohort does not reproduce in full
is the fetal-intestinal axis specifically, which is strongly enriched in the
cancer-panel cohort (10 of 10 patients) and absent in the whole-transcriptome
cohort (6 of 10, matched-null P = 0.80); the proCSC ↔ revCSC rebalancing
replicates in both.

---

# Figure legends

**Fig. EC1 | The invasive front of early-stage CRC is a rebalancing of stem
programmes confined to the epithelium.**
**(a)** Signature scores in PanCK⁺ tumour-epithelial segments across the four
histopathological regions, cancer-panel cohort. Grey lines, individual patients
(n = 10); black line, cohort mean; points coloured by region. Scores are
rank-based (singscore), averaged within patient × region.
**(b)** Patient-level mean difference between invasive front and tumour core for
all ten signatures, PanCK⁺ segments, cancer-panel cohort. Labels give the number
of patients moving up; fill indicates whether the effect exceeds 200
expression-matched random gene sets of the same size (P < 0.05). Red, up; blue,
down; grey, not significant.
**(c)** The same contrast in tumour epithelium and microenvironment. Point size,
−log₁₀ of the matched-null P; red, passes the null.
**(d)** Trophoblast and fetal/revival signatures across both GeoMx cohorts and
the nine-patient T1-only subset of the whole-transcriptome cohort, PanCK⁺
segments, on a common x scale. Labels give patients moving up.

**Fig. EC2 | TNFRSF12A tracks the oncofetal front while its ligand is
uniformly and uninformatively expressed.**
**(a)** Patient-paired expression in PanCK⁺ tumour epithelium, tumour core versus
invasive front, cancer-panel cohort (n = 10). Inset text gives the mean paired
difference, patients moving up, and the BH-adjusted P from a paired Wilcoxon
test over patients.
**(b)** Detection rate of *TNFSF12*, *TGFB1* and *IL36G* by microenvironment cell
type in plate-based scRNA-seq (2,409 cells, 5 patients). Cell types ordered by
*TGFB1* detection. Cell-level descriptive.
**(c)** Share of all ligand-positive cells contributed by each cell type, for the
eight largest *TNFSF12* sources, with the same ordering in both panels.

**Fig. EC3 | TWEAK⁺ macrophages do not co-emerge or colocalise with oncofetal
tumour cells, and a score-threshold definition manufactures the opposite
result.**
**(a)** Per-tumour abundances across the three pseudotimed substages in CosMx
(n = 11 tumours, 1,257,627 cells). Inset, Spearman correlation with substage
rank. Oncofetal cells are the original authors' epithelial sub-cluster label.
**(b)** Ligand-specific proximity. For each tumour-epithelial cell, ligand-positive
neighbours within 50 µm were counted; the statistic is the difference in mean
count between oncofetal and other tumour-epithelial cells, standardised against
200 permutations of the ligand-positive label among cells of the same class
within each field of view. Grey, one tumour (n = 9 with ≥ 20 cells on both
sides); red diamond, median.
**(c)** The same test applied to twelve non-ligand control genes matched to
*TNFSF12* on detection rate, under the authors' oncofetal label (left) and under
a revCSC score-decile definition (right). One point per tumour × gene; black
diamond, median. Under the score-decile definition control genes outscore the
ligands, showing the positive result to lack ligand specificity. Its origin is
audited in Fig. EC4c.

**Fig. EC4 | TNFRSF12A is associated with the oncofetal cell state, and the
spurious colocalisation signal is traced to detection density and local
architecture.**
**(a)** Per tumour, the difference in *TNFRSF12A* expression between oncofetal
and other malignant epithelial cells, stratified by field of view and
transcript-detection quintile so that cells are compared only with cells imaged
in the same field at similar depth. Red, *TNFRSF12A*; blue, the four ligands;
grey, twelve non-ligand control genes matched to *TNFSF12* on detection rate.
Oncofetal cells carry the original authors' label. Eight tumours have enough
cells of both classes to contribute.
**(b)** The same quantity summarised across tumours, one point per gene, under
the authors' label (left) and under a revCSC score decile with *TNFRSF12A*
removed from the set (right). Labels give the number of tumours in which the
receptor is higher in oncofetal cells.
**(c)** Audit of the EC3c result. The published test (bottom row, 50 µm only) is
compared with the same test after stratifying on field of view and detection
quintile, after additionally regressing per-cell transcript count, gene count
and area out of the score before taking the decile, and under the authors'
label — each at 20, 50 and 100 µm. One point per tumour × gene; diamonds,
medians. Stratification removes most of the inflation; a residual positive bias
that grows with radius remains under score-based definitions and affects control
genes as much as ligands.
**(d)** Receptor-conditioned proximity: among oncofetal cells only, the
difference between *TNFRSF12A*-positive and *TNFRSF12A*-negative cells in the
number of ligand-positive macrophage neighbours, at three radii, with the same
stratification and the same field-permutation null. One point per tumour × gene;
black diamond, median.
