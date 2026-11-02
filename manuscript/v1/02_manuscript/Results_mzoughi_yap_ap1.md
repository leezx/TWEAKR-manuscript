<!--
Provenance: analyses/2026-11-02_mzoughi-oncofetal-yap-ap1/docs/Results.md
Branch:     analysis/20261102-mzoughi-oncofetal-yap-ap1
Source:     Mzoughi et al., Nat Genet 57:402-412 (2025), GEO GSE237954
Figures:    manuscript/v1/01_figures/mzoughi_yap_ap1/Fig_MZ1..MZ3.pdf
Placement:  Fig. MZ1 and MZ2 proposed as main-figure panels (TWEAKR is YAP/AP-1
            dependent); Fig. MZ3 as supporting evidence for the claim ceiling.
Status:     not yet reviewed. Claim ceiling and open items in the analysis
            directory's docs/findings.md. Keep this copy in sync with that file.
-->

# Results — TWEAKR is a YAP- and AP-1-dependent component of the oncofetal programme

## The receptor marks oncofetal cells in two genetically defined tumour models

Every cohort that has so far linked *TNFRSF12A* to the revival/oncofetal state in
this manuscript is observational, and an association in human tumours cannot
distinguish a component of a programme from a correlate of it. We therefore
turned to a published set of isogenic mouse intestinal organoid models in which
the oncofetal state is created on demand by defined mutations and dismantled by
defined perturbations (Mzoughi *et al.*, *Nat Genet* 2025; GEO GSE237954).

Across the three single-cell libraries of that study — wild-type organoids,
*Apc*-null (A) tumoroids and *Apc*/*Kras*^G12D^/*Smad4*/*Trp53* (AKSP) tumoroids,
23,223 cells after quality control — *Tnfrsf12a* detection rises monotonically
with malignancy, from 25.7% of wild-type cells to 54.6% in A and 81.7% in AKSP
(Fig. MZ1a). Library depth also rises across these three, so all subsequent
comparisons are made within a library and within a sequencing-depth quintile.

Defining oncofetal cells by the authors' own mOnF signature — which does not
contain *Tnfrsf12a*, so the test is not circular — the receptor is higher in
oncofetal cells than in other malignant cells by +0.491 log in A and +0.619 log
in AKSP, with the two sides matched on depth to within 3% (Fig. MZ1b). Among 26
genes tested it ranks first in both models, and none of 24 detection-matched
control genes exceeds it. In wild-type organoids, where the oncofetal state is
barely present, the same contrast collapses to +0.053 and one control gene beats
it. That collapse is the specificity control: the association appears where the
state appears, and not otherwise.

The same pattern holds on the lineage plasticity axis the original study uses to
connect oncofetal reprogramming to loss of colonic identity (esophagus mucosa
module minus colon module). We first confirmed that the axis behaves as reported:
the mOnF score correlates with the plasticity score at ρ = 0.53 in A and ρ = 0.62
in AKSP. *Tnfrsf12a* then tracks that axis at ρ = 0.215 (A) and ρ = 0.328 (AKSP),
essentially unchanged after removing library size as a partial correlate (0.209
and 0.325), while no control gene reaches it in either model (Fig. MZ1c, d). In
wild-type organoids the receptor sits in the middle of the control distribution
(ρ = 0.031, 13 of 24 controls above).

The authors' own differential expression supports this at a more modest effect
size: *Tnfrsf12a* is up in their neoplastic metacluster (log2FC +0.337,
p_adj = 8.3 × 10⁻³⁵, detected in 82% vs 54% of cells), ranked 189th of 341
up-regulated genes. We therefore describe the receptor as associated with, and
specific to, the oncofetal state — not as one of its defining genes.

Two limitations bound this section. The deposited matrices carry a single barcode
suffix per genotype, so the replicates were pooled before deposition and no
sample-level test is possible; cell-level p-values are pseudoreplicated and are
not the basis of any claim here, which rests instead on effect size against
control genes at identical *n* and on agreement across three independent
libraries. And the plasticity score is applied per cell in mouse models, whereas
the original study applies it per patient in human cohorts.

## Forcing the oncofetal programme up or down moves TWEAKR with it

The same study perturbs YAP and AP-1 — the two factors it identifies as driving
oncofetal reprogramming — in both directions, in replicate, which allows the
association above to be tested as a dependency.

It is one. Ectopic YAP(S6A) in wild-type organoids induces *Tnfrsf12a* by +2.39
log2 (p_adj = 1.8 × 10⁻³⁶), and YAP together with FOS by +2.71
(p_adj = 3.6 × 10⁻⁴⁷). In the opposite direction, a dominant-negative FOS during
*Apc*-loss-driven initiation reduces it by −1.39 (p_adj = 1.0 × 10⁻⁹), and in
established AKSP tumoroids two independent YAP shRNAs reduce it by −0.76 and
−0.99 (p_adj = 8.3 × 10⁻⁸, 2.4 × 10⁻¹²) and FOS knockdown by −0.82
(p_adj = 1.2 × 10⁻⁷) (Fig. MZ2a). Seven of seven perturbations move the gene in
the predicted direction. Gain of YAP alone is sufficient to induce it and loss of
AP-1 alone is sufficient to reduce it; adding FOS on top of YAP adds nothing
further (+0.32, p = 0.20), consistent with the two acting on one axis at this
locus rather than additively.

Across all fifteen contrasts assembled here — including progression, RXR
manipulation and state sorting — the receptor's Wald statistic tracks the mOnF
programme's at Spearman ρ = 0.975 (Fig. MZ2c). Wherever the programme moves, by
whatever means, the receptor moves with it and in proportion.

One contrast does not support the receptor. The study's oncofetal fluorescent
reporter, sorted high versus negative, shows no difference in *Tnfrsf12a*
(+0.14 log2, p_adj = 0.81, three replicates per arm). The reporter is a synthetic
locus control region assembled from a defined set of transcription-factor binding
sites, so it reports on those sites rather than on the programme as a whole, and
the comparison has little power for an effect of this size — but it is the one
state-sorting experiment available and we report it as a negative rather than
omitting it.

## The placenta programme follows, weakly; the immune programmes only in one direction

Scoring the same contrasts at programme level (cameraPR on Wald statistics,
global Benjamini–Hochberg) separates three behaviours that should not be merged
(Fig. MZ2b).

The oncofetal and revCSC programmes are bidirectionally controlled: up in both
gain-of-function contrasts and down in all four loss-of-function contrasts, every
comparison significant. This replicates the original study's claim on our own
gene sets.

The placenta/trophoblast programme is co-regulated, but weakly. It rises under
YAP (mean Wald +3.87, FDR = 1.3 × 10⁻³) and under YAP+FOS (+4.75,
FDR = 3.0 × 10⁻³), and falls in all four loss contrasts — but only two of those
reach FDR < 0.05, and the effect sizes are three to four times smaller than the
oncofetal programme's. The interstitial-fetal (IFA) axis behaves the same way.
This is consistent with what we found at the invasive front of early human
tumours, where no trophoblast axis survived null calibration: the placenta
programme appears to be a weak passenger of oncofetal reprogramming rather than a
programme with its own control.

The tumour-intrinsic immune programmes behave asymmetrically. Cytotoxic
resistance and immune suppression are induced by YAP gain (FDR = 2.3 × 10⁻³ and
9.9 × 10⁻³), but no loss-of-function contrast reduces either, and four of eight
loss comparisons point the wrong way. YAP activation is sufficient to switch
these on; removing YAP or AP-1 from an established tumoroid does not switch them
off. These two sets are also the smallest tested (6 and 8 genes after orthologue
mapping) and are correspondingly the least robust result in the panel. We
therefore record the immune-tolerance hypothesis as neither supported nor refuted
by this cohort.

Throughout, the Lgr5 stem programme moves opposite to the oncofetal one — the
same rebalancing, rather than a general gain of stemness, that we observe at the
invasive front.

## The dependency is not shown to be direct

If YAP and AP-1 acted at the *Tnfrsf12a* locus, the locus should open as the
oncofetal state is established and its peaks should carry the corresponding
motifs. Neither follows cleanly (Fig. MZ3).

In the first bulk ATAC-seq experiment, the 24 peaks within 50 kb of the
*Tnfrsf12a* transcription start site do not change during progression (median
log2FC +0.013 for A versus wild type, −0.137 for AKSP versus wild type; p ≥ 0.87
against all other peaks), while peaks at the mOnF gene loci open strongly in the
same contrasts (+0.444 and +0.805, p = 3 × 10⁻⁵⁸ and 7 × 10⁻¹⁰⁷). In the second
experiment, the same A versus wild-type contrast gives +0.582 at the receptor
locus (p = 5.7 × 10⁻³). The two experiments therefore disagree about this locus
while agreeing about the oncofetal loci, so the discordance is specific rather
than a global quality difference. A window ladder from 10 kb to 500 kb places the
positive signal at 10–25 kb, so it is not a distal element that a narrower window
missed.

Nor is there motif evidence. Against 408 width- and accessibility-matched
background peaks, the locus peaks carry no excess of TEAD (0.58 versus 0.59
consensus matches per kb, p = 0.95) or AP-1 sites (0.96 versus 0.59, p = 0.23).

We state the conclusion at the level the evidence supports: *Tnfrsf12a*
expression requires YAP and AP-1 in these models, established by perturbation in
both directions with two independent shRNAs. Whether either factor acts directly
at the locus is not established — neither chromatin experiment perturbs YAP or
AP-1, so none of them can test direct action, and the regulation may be indirect
or may operate on factor occupancy at already-accessible chromatin rather than on
accessibility itself. Consensus-sequence counting is also cruder than a
position-weight-matrix scan and would miss degenerate sites.

## Summary

This cohort **supports** the manuscript's claim that TWEAKR belongs to the
oncofetal programme rather than merely correlating with it: the receptor marks
oncofetal cells specifically in two tumour models and not in normal organoids,
tracks the study's own lineage plasticity axis, and responds to seven of seven
perturbations of the two transcription factors that build the state.

It **adds** an upstream placement — YAP- and AP-1-dependence — while **withholding
support** from the stronger statement that either factor acts directly at the
locus.

It **qualifies** the placenta arm: the trophoblast programme is co-regulated by
the same factors but several-fold more weakly, and significantly in only half the
loss contrasts.

It **leaves open** the immune-tolerance hypothesis, which this design can induce
but cannot test for necessity, and it says **nothing** about the TWEAK ligand:
*Tnfsf12* is flat in every comparison here and absent from the original study's
differential expression, as expected in epithelial organoid models that contain
no immune compartment.

---

# Figure legends

**Fig. MZ1 | TWEAKR marks the oncofetal state in the A and AKSP models.**
**a**, Per-library cell means for the authors' mOnF oncofetal score, the lineage
plasticity score (esophagus mucosa module minus colon module) and *Tnfrsf12a*
expression, across wild-type organoids, A (*Apc*-null) and AKSP tumoroids
(GSE240129; 5,086 / 7,400 / 10,737 cells after quality control).
**b**, *Tnfrsf12a* (red) in mOnF-high cells versus other cells of the same
library, stratified by sequencing-depth quintile, against *Tnfsf12* (blue) and 24
detection-matched control genes (grey). **c**, Expression along deciles of the
lineage plasticity score, relative to decile 1; grey is the control-gene mean.
**d**, Partial Spearman correlation with the plasticity score after removing
library size. Cells within a library are not independent, so the comparison with
control genes at identical *n*, not the per-cell p-value, is the inference.

**Fig. MZ2 | TWEAKR is YAP- and AP-1-dependent.**
**a**, *Tnfrsf12a* log2 fold change (DESeq2, 95% confidence interval) in fifteen
contrasts grouped by perturbation axis; 3–4 organoid replicates per arm, batch
included in the model where the deposited sample names carry one. **b**,
Programme-level effects in the YAP and AP-1 contrasts (cameraPR on Wald
statistics; stars are global Benjamini–Hochberg FDR). **c**, *Tnfrsf12a* Wald
statistic against the mOnF programme's mean Wald statistic across all fifteen
contrasts (Spearman ρ = 0.975).

**Fig. MZ3 | The chromatin evidence does not establish direct regulation.**
**a**, Median peak log2 fold change within 50 kb of a transcription start site,
for the *Tnfrsf12a* locus, the authors' mOnF gene loci and the Lgr5 stem loci, in
two independent bulk ATAC-seq experiments. **b**, The same quantity across a
ladder of window sizes around the *Tnfrsf12a* transcription start site; window
sizes were fixed as a ladder rather than chosen after inspecting the result.
**c**, TEAD and AP-1 consensus match density in the 24 locus peaks against 408
width- and accessibility-matched background peaks; diamonds are means.
