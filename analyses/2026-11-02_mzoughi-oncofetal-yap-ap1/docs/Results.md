# Results — TWEAKR expression is associated with oncofetal identity and responds to YAP/AP-1 perturbation

## TWEAKR is enriched in oncofetal-like tumour cells

Every cohort that has so far linked *TNFRSF12A* to the revival/oncofetal state in
this manuscript is observational, and an association in human tumours cannot
distinguish a component of a programme from a correlate of it. We therefore
turned to a published set of isogenic mouse intestinal organoid models in which
the oncofetal state is created on demand by defined mutations and dismantled by
defined perturbations of the transcription factors said to build it
(Mzoughi *et al.*, *Nat Genet* 2025; GEO GSE237954).

Across the three single-cell libraries of that study — wild-type organoids,
*Apc*-null (A) tumoroids and *Apc*/*Kras*^G12D^/*Smad4*/*Trp53* (AKSP) tumoroids,
23,223 cells after quality control — *Tnfrsf12a* detection rises with malignancy,
from 25.7% of wild-type cells to 54.6% in A and 81.7% in AKSP (Fig. MZ1a).
Library depth also rises across these three, so all subsequent comparisons are
made within a library and within a sequencing-depth quintile; the more
informative question is whether the receptor still separates cell states *inside*
a single genetic background, where malignancy is held constant.

It does. Defining oncofetal cells by the authors' own mOnF signature — which does
not contain *Tnfrsf12a*, so the test is not circular — the receptor is higher in
oncofetal-like cells than in other malignant cells of the same library by +0.491
log in A and +0.619 log in AKSP, with the two sides matched on depth to within 3%
(Fig. MZ1b). Among 26 genes tested it ranks first in both models, and none of 24
detection-matched control genes exceeds it. In wild-type organoids, where the
oncofetal state is barely present, the same contrast falls to +0.053 and one
control gene beats it.

We describe this as enrichment rather than as marking. *Tnfrsf12a* is expressed
in all three genotypes, the comparison is against other malignant cells rather
than against a systematic panel of alternative cell states, and the authors' own
differential expression gives a more modest effect: up in their neoplastic
metacluster at log2FC +0.337 (p_adj = 8.3 × 10⁻³⁵, detected in 82% versus 54% of
cells), ranked 189th of 341 up-regulated genes, and absent from their 51-gene
oncofetal signature.

**Replication structure.** The deposited matrices carry a single barcode suffix
per genotype: the replicates were pooled before deposition. These are therefore
three pooled libraries representing three different genotypes, **not three
biological replicates** of anything, and no genotype-level test is possible. Every
cell-level p-value in this section is pseudoreplicated and none is used as
evidence. What the claims rest on is effect size against detection-matched control
genes at identical *n*, and agreement in direction between the two tumour models.

## The association with lineage plasticity is attenuated once the two scores are made independent

The original study connects oncofetal reprogramming to loss of colonic identity
with a lineage plasticity score — the esophagus mucosa module minus the colon
module — applied per patient in three human cohorts. Applied per cell here, the
score behaves as reported: the mOnF score correlates with it at ρ = 0.530 in A and
ρ = 0.616 in AKSP.

*Tnfrsf12a* tracks the same axis at partial ρ = 0.206 (A) and 0.324 (AKSP) after
removing library size, with no control gene reaching it in either model, and sits
in the middle of the control distribution in wild-type organoids (ρ = 0.034, 13 of
24 controls above).

These two scores are not independent, however: 14 of the 51 mOnF genes are also
members of the esophagus module that forms the positive arm of the plasticity
score (the colon arm shares none). Part of the correlation above could therefore
be the oncofetal association measured a second time. Removing those 14 genes from
the axis attenuates but does not abolish the result — partial ρ falls from 0.206
to 0.162 in A and from 0.324 to 0.268 in AKSP, with still 0 of 24 control genes
above it in either model (Fig. MZ4a). The relationship between the mOnF score and
the axis itself is more dependent on the shared genes (0.530 → 0.336 in A;
0.616 → 0.407 in AKSP).

We therefore report the plasticity association as supporting evidence of reduced
weight: a real but partly redundant restatement of the oncofetal association,
measured on an axis that quantifies ectopic lineage gene expression rather than
observed state conversion.

## Perturbing YAP or AP-1 moves TWEAKR in both directions

The same study perturbs YAP and AP-1 in both directions, in replicate, which
allows the association above to be tested as a dependency — and this is the
strongest result in the analysis.

Ectopic YAP(S6A) in wild-type organoids induces *Tnfrsf12a* by +2.39 log2
(p_adj = 1.8 × 10⁻³⁶), and YAP together with FOS by +2.71 (p_adj = 3.6 × 10⁻⁴⁷).
In the opposite direction, a dominant-negative FOS during *Apc*-loss-driven
initiation reduces it by −1.39 (p_adj = 1.0 × 10⁻⁹), and in established AKSP
tumoroids two independent YAP shRNAs reduce it by −0.76 and −0.99
(p_adj = 8.3 × 10⁻⁸, 2.4 × 10⁻¹²) and FOS knockdown by −0.82
(p_adj = 1.2 × 10⁻⁷) (Fig. MZ2a). Seven of seven perturbations move the gene in
the predicted direction, with three to four organoid replicates per arm.

Gain of YAP alone is sufficient to induce the gene and loss of AP-1 alone is
sufficient to reduce it. Adding FOS on top of YAP produces no further significant
increase (+0.32, p = 0.20), but we draw no mechanistic conclusion from that:
non-additivity is equally consistent with saturation of the response, with the
FOS construct not raising effective AP-1 activity, with convergence on a shared
downstream programme, and with two separate mechanisms sharing a common output
limit. It cannot distinguish between them, and in particular it is not evidence
that the two factors act on a common regulatory element.

The supportable statement is that *Tnfrsf12a* expression is regulated by YAP- and
AP-1-associated transcriptional programmes in these organoid models. Whether
either factor acts on the gene directly, or through the oncofetal programme it
establishes, is addressed below and is not resolved.

Across all fifteen contrasts assembled here the receptor's Wald statistic tracks
the mOnF programme's at Spearman ρ = 0.975 (Fig. MZ2c). Because several of these
contrasts share an experimental arm, we repeated the correlation on a maximal
arm-disjoint subset of eight contrasts; it is unchanged (ρ = 0.976, P = 4 × 10⁻⁴).
This is nonetheless consistency evidence rather than independent mechanistic
support: the Wald statistic reflects estimation precision as well as effect size,
and the contrasts span different biological settings — progression, transcription
factor perturbation and RXR manipulation.

One contrast does not support the receptor, and we report it as a genuine
conflict rather than resolving it. The study's oncofetal fluorescent reporter,
sorted high versus negative, shows no difference in *Tnfrsf12a* (+0.14 log2,
p_adj = 0.81). This disagrees with the single-cell result in the same study,
where mOnF-high cells show the largest receptor difference of any gene tested.
The two experiments use different definitions of the oncofetal state — a
synthetic locus control region assembled from a defined set of transcription
factor binding sites, versus a 51-gene expression signature — and we do not have
evidence to say which definition the receptor fails to follow, or whether the
reporter is simply insensitive. The discrepancy stands unexplained and bounds how
far the marker claim can be taken.

## The placenta and immune signals do not survive auditing

Scoring the same contrasts at programme level (cameraPR on Wald statistics)
initially suggested that the placenta/trophoblast programme and two
tumour-intrinsic immune programmes move with YAP and AP-1 (Fig. MZ2b). Both
findings fail when the gene sets are audited, and we report them as negative.

**Placenta.** The 34-gene trophoblast set rose under YAP (mean Wald +3.87) and
YAP+FOS (+4.75) and fell in all four loss-of-function contrasts. But four of its
34 genes — *Egfr*, *Krt19*, *Krt8*, *Phlda2* — are also members of the project's
YAP target sets. Removing those four genes removes the result: no contrast
remains significant, and the YAP gain-of-function effect falls from +3.87 to
+2.08 and from +4.75 to +1.93 (Fig. MZ4b). The enrichment was carried by generic
YAP-responsive epithelial genes, not by a trophoblast programme. We therefore do
not claim that YAP or AP-1 regulates a placental programme in these models, and
nothing here supports a placenta-like immune tolerance phenotype. This is
consistent with our finding in early human tumours, where no trophoblast axis
survived expression-matched null calibration at the invasive front.

**Tumour-intrinsic immune programmes.** Immune suppression (10 genes) and
cytotoxic resistance (6 genes) were induced by YAP gain. Both results are carried
by one gene each: removing *Nt5e* takes immune suppression from P = 0.0036 to
P = 0.39, and removing *Serpinb9* takes cytotoxic resistance from P = 0.0007 to
P = 0.16 (Fig. MZ4c). No loss-of-function contrast reduced either set in the
first place. These sets are too small for a competitive test to be informative,
and the names are functional assertions that transcript-level enrichment cannot
support: a change in *Nt5e* or *Serpinb9* transcript is not evidence that tumour
cells suppress T cells or resist cytotoxic killing. We record this as two
single-gene observations worth following up — *Nt5e* and *Serpinb9* are both
plausible YAP-responsive immune-evasion effectors — and not as a programme-level
finding.

Throughout, the Lgr5 stem programme moves opposite to the oncofetal one — the
same rebalancing, rather than a general gain of stemness, that we observe at the
invasive front.

## Direct regulation: occupancy evidence exists, but not in the right tissue

Bulk ATAC-seq does not show the *Tnfrsf12a* locus opening as the oncofetal state
is established. In the first experiment the 24 peaks within 50 kb of the
transcription start site do not change during progression (median log2FC +0.013
for A versus wild type, −0.137 for AKSP versus wild type; p ≥ 0.87 against all
other peaks), while peaks at the mOnF gene loci open strongly in the same
contrasts (+0.444 and +0.805). In the second experiment the same A versus
wild-type contrast gives +0.582 at the receptor locus (p = 5.7 × 10⁻³). The two
experiments disagree about this locus while agreeing about the oncofetal loci
(Fig. MZ3a, b).

This is not evidence against direct regulation. Transcription factor binding does
not require a change in chromatin accessibility: YAP/TEAD and AP-1 can occupy
elements that are already open, in which case ATAC-seq registers nothing. Neither
ATAC experiment perturbs YAP or AP-1, so neither can test direct action at all.

We therefore asked the occupancy question directly, using ChIP-Atlas's uniform
reprocessing of public mouse ChIP-seq. The *Tnfrsf12a* transcription start site is
a bound element for both arms: TEAD1 (mean MACS2 320, 94th percentile of all
genes, a peak in 19 of 24 experiments), TEAD4 (96, 83rd percentile, 12 of 32),
YAP1 (46, 65th percentile, 7 of 37), and all five AP-1 members tested — FOSL1
(604, 97th percentile), JUND (386, 97th), FOSL2 (254, 94th), FOS (144, 94th),
JUNB (124, 90th) and JUN (101, 87th) (Fig. MZ4d). The locus scores above 70–89%
of the authors' own oncofetal genes for every factor tested.

Two limits keep this from closing the question. First, of 349 experiments in the
panel only four are intestinal, and **none of those four calls a peak** at the
locus; the positive signal comes from liver, fibroblasts, macrophages,
trophoblast stem cells and tumour lines. The evidence is therefore
context-mismatched, and the few in-context experiments are negative. Second,
occupancy is not function: even a bound element need not be required for
expression, which would take CRISPR interference or enhancer deletion to
establish. Our earlier consensus-motif scan, which found no TEAD or AP-1 excess
in the locus peaks, is superseded by this analysis and should be read as a limit
of consensus matching rather than as evidence of absence.

## Summary

This cohort **supports** the claim that *TNFRSF12A* is associated with oncofetal
identity: the receptor is enriched in oncofetal-like cells in two tumour models
and not in normal organoids, and is the strongest of 26 genes tested in both.

Its **strongest contribution** is perturbational: seven of seven gain- and
loss-of-function manipulations of YAP and AP-1 move *Tnfrsf12a* in the predicted
direction, including two independent shRNAs. *Tnfrsf12a* expression responds to
YAP- and AP-1-associated transcriptional programmes.

It **does not establish** that YAP/TEAD or AP-1 acts directly at the locus.
Public ChIP-seq shows the promoter is a bound TEAD and AP-1 element, which makes
direct regulation plausible, but no intestinal experiment supports it and
occupancy is not functional dependence.

It **withdraws** the placenta and immune results. Both were artefacts of gene set
composition — four generic YAP targets in the trophoblast set, one gene each in
the two immune sets.

It **leaves open** a question this analysis creates rather than answers. The
manuscript's working model places TWEAKR upstream of YAP; this dataset shows YAP
activation raising *Tnfrsf12a*. TWEAKR upstream of YAP, TWEAKR downstream of YAP,
and a positive feedback loop between them are all compatible with what we have.
Distinguishing them is a more productive next step than any further signature
analysis.

It says **nothing** about the TWEAK ligand: *Tnfsf12* is flat in every comparison
here and absent from the original study's differential expression, as expected in
epithelial organoid models that contain no immune compartment.

---

# Figure legends

**Fig. MZ1 | TWEAKR is enriched in oncofetal-like cells in the A and AKSP models.**
**a**, Per-library cell means for the authors' mOnF oncofetal score, the lineage
plasticity score (esophagus mucosa module minus colon module) and *Tnfrsf12a*
expression, across wild-type organoids, A (*Apc*-null) and AKSP tumoroids
(GSE240129; 5,086 / 7,400 / 10,737 cells after quality control). The three
libraries are three genotypes, not biological replicates.
**b**, *Tnfrsf12a* (red) in mOnF-high cells versus other cells of the same
library, stratified by sequencing-depth quintile, against *Tnfsf12* (blue) and 24
detection-matched control genes (grey). **c**, Expression along deciles of the
lineage plasticity score, relative to decile 1; grey is the control-gene mean.
**d**, Partial Spearman correlation with the plasticity score after removing
library size. Cells within a library are not independent, so the comparison with
control genes at identical *n*, not the per-cell p-value, is the inference.

**Fig. MZ2 | TWEAKR responds to YAP and AP-1 perturbation.**
**a**, *Tnfrsf12a* log2 fold change (DESeq2, 95% confidence interval) in fifteen
contrasts grouped by perturbation axis; 3–4 organoid replicates per arm, batch
included in the model where the deposited sample names carry one. **b**,
Programme-level effects in the YAP and AP-1 contrasts (cameraPR on Wald
statistics; stars are global Benjamini–Hochberg FDR). The placenta and immune
rows of this panel do not survive the gene set audits in Fig. MZ4b, c and are
retained only to show what was tested. **c**, *Tnfrsf12a* Wald statistic against
the mOnF programme's mean Wald statistic across all fifteen contrasts
(Spearman ρ = 0.975; ρ = 0.976 on an arm-disjoint subset of eight).

**Fig. MZ3 | Chromatin accessibility at the locus is unchanged and discordant.**
**a**, Median peak log2 fold change within 50 kb of a transcription start site,
for the *Tnfrsf12a* locus, the authors' mOnF gene loci and the Lgr5 stem loci, in
two independent bulk ATAC-seq experiments. **b**, The same quantity across a
ladder of window sizes around the *Tnfrsf12a* transcription start site; window
sizes were fixed as a ladder rather than chosen after inspecting the result.
**c**, TEAD and AP-1 consensus match density in the 24 locus peaks against 408
width- and accessibility-matched background peaks; diamonds are means. Panel c is
superseded by the ChIP-seq occupancy analysis in Fig. MZ4d: absence of consensus
enrichment is a limit of consensus matching, not evidence of absent binding.

**Fig. MZ4 | Audits of the four results the first draft over-read.**
**a**, *Tnfrsf12a* partial Spearman correlation with the lineage plasticity axis
as published and after removing the 14 genes the axis shares with the mOnF
signature; grey bars span the median to the maximum of 24 detection-matched
control genes. **b**, The placenta/trophoblast programme before and after
removing the four genes it shares with the project's YAP target sets; filled
points are FDR < 0.05 within this table. **c**, cameraPR P for the two immune
sets with the whole set and after removing the single strongest gene (named in
brackets). **d**, Percentile of the *Tnfrsf12a* transcription start site among
all mouse genes by mean MACS2 score in ChIP-Atlas, for four YAP/TEAD and six AP-1
factors at a 5 kb window; labels give the number of experiments calling a peak.
None of the four intestinal experiments in the panel calls a peak.
