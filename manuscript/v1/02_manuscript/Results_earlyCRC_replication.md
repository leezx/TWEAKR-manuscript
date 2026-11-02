<!--
Source analysis: analyses/2026-11-02_earlycrc-oncofetal-snippert/
Figures:         analyses/2026-11-02_earlycrc-oncofetal-snippert/figures/Fig_EC1..EC3.{pdf,png}
Statistics:      .../tables/, claim ceilings and open items in .../docs/findings.md
Status:          new section, not yet reviewed or merged; not canonical evidence yet.

Placement note: this is an external replication cohort. It can run as its own
Results section, or be split with the Q1/Q2 material folded into the Figure 2
and Figure 4 sections of the main Results and the CosMx control-gene test
promoted to Methods. The author should choose; see open_items.md.
-->

# Results — An independent early-stage CRC cohort separates the revival axis from the trophoblast hypothesis

*Draft section for the TWEAKR manuscript. Figures: `../figures/Fig_EC1…EC3`.
Statistics in `../tables/`, methods and claim ceilings in `findings.md`.*

---

## The oncofetal front is a rebalancing of two stem programmes, not a gain of a placental one

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

The shift belongs to the epithelium. In PanCK⁻ segments from the same regions of
interest, the fetal-intestinal, revCSC, fetal-intestine and revival-stem scores
are flat (|Δ| ≤ 0.005, 3–5 of 10 patients, matched-null P ≥ 0.87), whereas
proCSC and proliferation fall in 0 of 10 (Fig. EC1c). A change in bulk tissue
composition at the invasive front cannot produce that pattern.

No trophoblast programme participates (Fig. EC1d). In the epithelium of the
cancer-panel cohort the pan-trophoblast axis, the curated placenta-trophoblast
set and the extravillous-trophoblast set are all unmoved (Δ = −0.005, +0.010,
−0.020; matched-null P = 0.73, 0.67, 0.36). The whole-transcriptome cohort,
which carries near-complete coverage of these sets (228 of 234 and 39 of 41
genes), is likewise negative, with the pan-trophoblast axis rising in **1 of 10**
patients (P = 0.006 in the opposite direction); in its microenvironment the axis
is significantly depleted at the front (Δ = −0.033, 0 of 10 patients,
matched-null P = 0.025). Restricting to the nine T1 tumours, as the original
authors do, does not change this.

One negative result is worth stating explicitly because it would have been a
positive under a looser design. Contrasting the invasive front against the mean
of the other three regions — rather than against the core — the
placenta-trophoblast set rises in **9 of 9 patients** (Δ = +0.026, P = 0.004,
BH q = 0.010). It does not survive the matched null (z = +0.83, P = 0.43), while
revCSC (z = +3.1), the fetal-intestinal axis (z = +5.3), YAP regeneration
(z = +8.0) and fetal intestine (z = +5.6) all do. Perfect cross-patient
consistency against a background that includes normal tissue reflects generic
expression drift into tumour, which any tumour-expressed gene set reproduces.

## TNFRSF12A marks the invasive front; TWEAK has no cellular source

Within the same patient-paired design, *TNFRSF12A* rises at the invasive front of
tumour epithelium in **10 of 10 patients** (+0.46 log, BH q = 0.004), placing it
in the same tier as *MMP7* (+1.05) and *LAMC2* (+0.95) — the two markers the
original authors use to define the oncofetal front — and above *TGFB3* (+0.18,
9 of 10, q = 0.006). Its ligand does not move: *TNFSF12* is +0.02 log and splits
5 of 10 (q = 0.625) (Fig. EC2a). The receptor rises more modestly in the
microenvironment as well (+0.15, 8 of 10, q = 0.027); the ligand does not
(7 of 10, q = 0.28).

Plate-based scRNA-seq of the sorted microenvironment from the same study
(2,409 cells, 5 patients) explains why the ligand carries no spatial
information: it has no cellular source (Fig. EC2b, EC2c). *TNFSF12* detection is
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

## TWEAK⁺ macrophages neither co-emerge nor colocalise with oncofetal cells

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

Nor are the two cell populations neighbours (Fig. EC3b). Counting ligand-positive
neighbours within 50 µm of every tumour-epithelial cell and comparing oncofetal
against other tumour epithelium — with the ligand-positive label permuted among
cells of the same class within each field of view, so that the test measures
*ligand-specific* proximity rather than proximity to macrophages — *TNFSF12*⁺
macrophages are enriched around oncofetal cells in 3 of 9 evaluable tumours
(median z = −0.13, P = 0.73). *TGFB1*, *TGFB3* and *IL36G* are equally negative.

This test required a control that we recommend be adopted for every spatial
colocalisation claim (Fig. EC3c). If oncofetal cells are instead defined by a
revCSC score decile rather than by the authors' label, the identical test
returns **every** ligand as strongly colocalised in 11 of 11 tumours (median z
4.6 to 7.3, permutation P < 0.005). That result is false. Twelve non-ligand
control genes matched to *TNFSF12* on detection rate (0.041–0.047 versus 0.046),
run through the same test, score **higher** than the ligands (median z 7.8 versus
6.3), with SHC1, ESYT1, PPP3CA and UBQLN2 each positive in 11 of 11 tumours.
Cells scoring high on any expression signature sit where transcript detection is
dense and therefore have more neighbours positive for anything. Under the
authors' label, ligands and control genes are indistinguishable (median z −0.61
for controls, +0.12 for ligands; the highest-ranked of all sixteen genes is the
control PPP3CA). A signature-score threshold combined with a within-field label
permutation is not a sufficient control for colocalisation in imaging-based
spatial transcriptomics.

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
ligands, identifying the positive result as a transcript-detection-density
artefact.
