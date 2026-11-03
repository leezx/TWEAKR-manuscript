# TWEAKR in the Mzoughi oncofetal reprogramming models — full findings

**Source**: Mzoughi *et al.*, "Oncofetal reprogramming drives phenotypic plasticity in
WNT-dependent colorectal cancer", *Nature Genetics* 57:402–412 (2025),
doi `10.1038/s41588-024-02058-1`. GEO SuperSeries **GSE237954** (14 SubSeries).

**Date**: 2026-11-02 · **Branch**: `analysis/20261102-mzoughi-oncofetal-yap-ap1`

Three questions were put to this dataset. The first two are answered; the third
was asked to be recorded rather than run, and is in `docs/TODO_FOLFIRI.md`.

---

## Why this dataset is the right test

The TWEAKR manuscript claims that *TNFRSF12A* marks a revival/oncofetal epithelial
state. Every cohort supporting that so far has been observational. This study is
the first one available that **perturbs the two transcription factors said to
create the state** — YAP and AP-1 — in both directions, with replicates, in
isogenic organoids. If *Tnfrsf12a* is part of the oncofetal programme rather than
a correlate of it, it has to move when the programme is forced up and when it is
forced down. That is a falsifiable prediction, and this is the experiment for it.

Two design choices keep the answer from being circular:

- The oncofetal state is defined by **the authors' own mOnF signature**
  (Supplementary Table S1d, 51 genes). *Tnfrsf12a* is **not** a member of it.
- The project's `revCSC` set **does** contain *Tnfrsf12a* (1 of 32), as recorded
  in the earlyCRC analysis. It is therefore never used to define the state here,
  only reported alongside as a second programme.

---

## Q1. Is TWEAKR a marker of the oncofetal state in the A and AKSP models?

**Data**: GSE240129, three 10x libraries — WT organoids, A (*Apc*-null) tumoroids,
AKSP (*Apc*/*Kras*^G12D^/*Smad4*/*Trp53*) tumoroids. 29,534 barcodes, 23,223 after
QC (nFeature ≥ 500, nCount ≥ 1000, mt < 25%): WT 5,086, A 7,400, AKSP 10,737.

**The limitation that shapes the whole analysis.** The deposited matrices carry a
single barcode suffix per genotype — the three replicates of Supplementary Table
S1a were pooled before deposition. There is no replicate label, so no sample-level
test is possible and every cell-level p-value here is pseudoreplicated. They are
reported for completeness and are **not** treated as evidence. The evidence is:
effect size against 24 detection-matched control genes at identical *n*;
agreement in direction between the two tumour models; and the authors' own
differential expression, which we did not compute.

To be precise about what the three libraries are: they are three **genotypes**,
each sequenced once as a pool. They are not biological replicates of anything, so
"replication across libraries" here means only that an effect seen in A is also
seen in AKSP — two different genetic backgrounds, not two samples of one.

### Q1.1 The receptor rises with the state across the three models

| genotype | cells | median depth | mOnF score | plasticity score | *Tnfrsf12a* detected | *Tnfrsf12a* mean log |
|---|---|---|---|---|---|---|
| WT | 5,086 | 9,538 | −0.214 | −0.156 | 25.7% | 0.188 |
| A | 7,400 | 14,979 | +0.070 | +0.009 | 54.6% | 0.417 |
| AKSP | 10,737 | 17,448 | +0.168 | +0.037 | 81.7% | 0.947 |

Detection rises monotonically from a quarter of normal organoid cells to four
fifths of AKSP cells. Library depth also rises across the three (9.5k → 17.4k), so
this ordering alone proves nothing; it is the within-library analyses below that
control for depth.

### Q1.2 Within a tumour, the receptor marks oncofetal cells specifically

Oncofetal cells = top decile of the authors' mOnF score within genotype. The
comparison is made **within genotype × library-depth quintile**, so the two sides
are matched on sequencing depth.

| genotype | Δlog (OnF − rest) | Δdetection | depth ratio | rank among 26 genes | control median | control max | controls above receptor |
|---|---|---|---|---|---|---|---|
| WT | +0.053 | +3.7 pp | 0.96 | 2 | −0.020 | +0.062 | 1 of 24 |
| A | **+0.491** | +24.1 pp | 0.97 | **1** | −0.018 | +0.185 | **0 of 24** |
| AKSP | **+0.619** | +9.2 pp | 1.00 | **1** | −0.006 | +0.229 | **0 of 24** |

In both tumour models the receptor is the single most oncofetal-enriched gene of
the 26 tested, and no control gene comes close. In WT organoids — where the
oncofetal state barely exists — the effect collapses to +0.053 and one control
gene beats it. **That contrast is the specificity control**: the association is
not a generic property of the gene, it appears where the state appears.

*Tnfsf12* (the ligand) is flat in all three (Δlog ≤ 0.001).

### Q1.3 The Fig. 1j–l lineage plasticity score

Computed exactly as the paper defines it: `AddModuleScore(esophagus mucosa) −
AddModuleScore(colon)`, using the authors' own lineage signatures
(Supplementary Table S1g: `lkts_esophagus_mucosa` 217 genes, `lkts_colon_transverse`
29 genes). Note the paper's Fig. 1j–l applies this to three **human** cohorts at
patient level; here it is applied per cell in the mouse models, which is a
different unit and is labelled as such everywhere.

Axis positive control — mOnF score vs plasticity score, same cells:
ρ = 0.300 (WT), **0.528 (A)**, **0.616 (AKSP)**. The relationship the paper
reports in patients is reproduced within these models.

*Tnfrsf12a* vs plasticity:

| genotype | ρ | partial ρ (depth removed) | control median (partial) | controls above receptor |
|---|---|---|---|---|
| WT | 0.015 | 0.031 | +0.040 | **13 of 24** |
| A | 0.215 | **0.209** | −0.027 | **0 of 24** |
| AKSP | 0.328 | **0.325** | −0.016 | **0 of 24** |

Removing library size changes nothing (0.215 → 0.209; 0.328 → 0.325), so this is
not a depth artefact. In WT the receptor sits in the middle of the control
distribution — again, no state, no association.

The decile profile (`Q1C`) shows the same thing without a correlation
coefficient: across deciles of plasticity the receptor gains +0.50 log in A and
+0.75 log in AKSP, while the control-gene mean is flat (≤ 0.03) in all three.

**Audit added in review — the two scores are not independent.** Fourteen of the
51 mOnF genes are also in the esophagus module that forms the positive arm of the
plasticity score (*Syt8, Serpinb5, Samd5, Anxa1, Anxa3, S100a14, Emp1, Ier3,
Krt7, Emp2, Ccnd1, Ly6d, Fabp5, Msln*); the colon arm shares none. So part of the
correlation above is the oncofetal association measured twice. Recomputing the
axis without those genes:

| genotype | partial ρ, axis as published | partial ρ, axis minus shared genes | controls above |
|---|---|---|---|
| WT | 0.034 | 0.031 | 13 / 24 → 13 / 24 |
| A | 0.206 | **0.162** | 0 / 24 → **0 / 24** |
| AKSP | 0.324 | **0.268** | 0 / 24 → **0 / 24** |

The receptor association is attenuated by about 20% but survives, with still no
control gene above it. The mOnF-score-vs-axis relationship depends on the shared
genes considerably more (A 0.530 → 0.336; AKSP 0.616 → 0.407), which is worth
knowing about the paper's own Fig. 1j–l framing.

The axis measures ectopic lineage gene expression, not observed state conversion.
It is reported here as supporting evidence of reduced weight, not as independent
confirmation.

### Q1.4 The authors' own statistic

Supplementary Table S1c, neoplastic metacluster vs rest, computed by the authors:

> *Tnfrsf12a*, avg_log2FC **+0.337**, pct.1 0.818 vs pct.2 0.538, p_adj **8.25 × 10⁻³⁵**,
> ranked 189th of 341 up-regulated genes.

Significant and consistent in direction, but a **modest** effect — the receptor is
not among their top markers, and it is not in their 51-gene mOnF signature.
*Tnfsf12* does not appear in their differential expression table at all.

### Q1 claim ceiling

*Tnfrsf12a* is **enriched in oncofetal-like tumour cells** in both models, is the
strongest such gene among 26 tested, tracks the paper's own lineage plasticity
axis (attenuated but surviving the independence audit above), and does none of
this in normal organoids.

The supportable statement is *"enriched in oncofetal-like tumour cells"*. Not
*"specifically marks oncofetal cells"*: the gene is expressed in all three
genotypes, the comparison is against other malignant cells rather than a
systematic panel of alternative cell states, it is not in the authors' 51-gene
signature, and its effect in their own metacluster test is modest (189th of 341).

Bounding this further, the authors' oncofetal **reporter** sort does not separate
on *Tnfrsf12a* at all (Q2.1). That conflict is unresolved and is not explained
away as reporter insensitivity or low power, neither of which we can demonstrate.

---

## Q2. Is TWEAKR regulated by YAP and AP-1?

### Q2.1 Transcriptional perturbation — the answer is yes, in both directions

DESeq2 on the authors' salmon counts, batch in the model where the deposited
sample names carry one. 15 contrasts, 3–4 organoid replicates per arm.

| contrast | axis | *Tnfrsf12a* log2FC | padj |
|---|---|---|---|
| YAP(S6A)-OE vs EV, WT organoids | **YAP gain** | **+2.39** | 1.8 × 10⁻³⁶ |
| YAP(S6A)+FOS-OE vs EV | **YAP + AP-1 gain** | **+2.71** | 3.6 × 10⁻⁴⁷ |
| YAP+FOS vs YAP alone | AP-1 added on YAP | +0.32 | 0.20 |
| dominant-negative FOS vs EV, during *Apc* loss | **AP-1 loss** | **−1.39** | 1.0 × 10⁻⁹ |
| YAP shRNA-1 vs scramble, AKSP | **YAP loss** | **−0.76** | 8.3 × 10⁻⁸ |
| YAP shRNA-2 vs scramble, AKSP | **YAP loss** | **−0.99** | 2.4 × 10⁻¹² |
| FOS knockdown vs scramble, AKSP | **AP-1 loss** | **−0.82** | 1.2 × 10⁻⁷ |
| A vs WT | progression | +1.90 | 3.0 × 10⁻¹¹ |
| AKSP vs WT | progression | +1.92 | 1.1 × 10⁻¹¹ |
| AKSP vs A | progression | +0.02 | 0.98 |
| *Apc* loss (OHT) vs WT | progression | +1.02 | 9.9 × 10⁻⁶ |
| **oncofetal reporter high vs negative** | **oncofetal state** | **+0.14** | **0.81** |
| RXR-OE vs EV, WT | RXR gain | −0.05 | 0.98 |
| RXR-OE vs EV, *Apc*-null | RXR gain | −0.38 | 0.13 |
| RXR inhibition vs DMSO, AKSP | RXR loss | +0.09 | 0.50 |

Seven of seven YAP/AP-1 perturbations move the gene in the predicted direction,
all with padj < 10⁻⁷. Two independent YAP shRNAs agree. Loss of AP-1 alone is
sufficient to bring it down (−1.39 under dominant-negative FOS, −0.82 under FOS
knockdown), and gain of YAP alone is sufficient to drive it up (+2.39). Adding
FOS on top of YAP adds nothing significant (+0.32, p = 0.20), which is consistent
with the two acting on the same axis rather than additively at this locus.

The authors' own DESeq2 output for the one contrast with no deposited counts
(GSE263047, Supplementary Table S2c) agrees: *Apc* loss induces *Tnfrsf12a*
(+1.33, padj 1.1 × 10⁻²⁰), and after YAP shRNA-1, YAP shRNA-2 or FOS knockdown it
is no longer in the significant gene list. That table is pre-filtered to
significant genes, so this is an absence-of-evidence inference, weaker than the
contrasts above, and is reported as such.

**The one negative that matters**: the authors' oncofetal fluorescent reporter,
sorted high vs negative (GSE235205), does **not** separate on *Tnfrsf12a*
(+0.14, padj 0.81, n = 3 vs 3). The reporter is a synthetic locus control region
built from a specific set of transcription-factor binding sites (Supplementary
Table S4a), so it reports on those sites rather than on the whole programme, and
n = 3 per arm has little power for a 0.14 log2 effect. Still, it is the one
state-sorting experiment in the paper and it does not support the receptor.

### Q2.2 Across contrasts, the receptor tracks the programme

Receptor Wald statistic vs mOnF programme mean Wald statistic, over all 15
contrasts: **Spearman ρ = 0.975, P < 10⁻⁴**. Wherever the oncofetal programme
moves, by whatever means, the receptor moves with it and in proportion.

### Q2.3 Placenta and tumour-intrinsic immune programmes — WITHDRAWN in review

The first draft reported these as real, if weak. Both fail an audit of gene set
composition and are now reported as negative. The original panel is kept below
so the retraction is auditable.

cameraPR on the Wald statistics; FDR is global BH across all contrasts × sets.

| programme | YAP-OE | YAP+FOS-OE | FOS-DN | YAPsh1 | YAPsh2 | FOSkd |
|---|---|---|---|---|---|---|
| oncofetal (authors') | **+14.2** \*\*\* | **+19.8** \*\*\* | **−5.3** \*\*\* | **−2.9** \*\*\* | **−3.1** \*\*\* | **−3.3** \*\*\* |
| revCSC (project) | **+7.3** \*\*\* | **+9.8** \*\*\* | **−4.2** \*\*\* | **−1.5** \*\* | **−2.2** \*\*\* | **−2.0** \*\* |
| placenta / trophoblast | **+3.9** \*\* | **+4.8** \*\* | **−1.4** \* | −1.0 | **−1.4** \* | −1.2 |
| IFA core | **+3.6** \*\*\* | **+4.7** \*\*\* | **−1.7** \*\*\* | −0.3 | −0.5 | −0.05 |
| TRA core | +1.7 | **+2.9** \*\* | −0.7 | −0.5 | **−0.9** \*\* | −0.8 |
| EVT core | +2.1 | +1.6 | **−1.7** \* | +0.2 | −0.6 | +0.8 |
| immune suppression | **+5.3** \*\* | +4.6 | −2.0 | −1.4 | −1.2 | +0.1 |
| cytotoxic resistance | **+6.5** \*\* | **+7.8** \*\* | −1.9 | +0.4 | −0.7 | +1.7 |
| Lgr5 stem | −3.2 | −3.9 | −1.3 | +1.3 | +0.8 | +0.9 |

(\* FDR < 0.05, \*\* < 0.01, \*\*\* < 0.001; values are mean Wald statistic.)

**Audit 1 — the placenta set carries four generic YAP targets.** Of the 34 mouse
trophoblast genes, four are also in the project's YAP target sets: *Egfr*,
*Krt19*, *Krt8*, *Phlda2*. (None overlaps the mOnF signature, so oncofetal
contamination is not the issue; YAP-target contamination is.) Dropping those
four:

| contrast | full, 34 genes | minus 4 YAP targets, 30 | FDR full | FDR minus |
|---|---|---|---|---|
| YAP-OE | +3.87 | +2.08 | 0.0039 | 0.122 |
| YAP+FOS-OE | +4.75 | +1.93 | 0.0084 | 0.404 |
| YAPsh2 | −1.40 | −1.08 | 0.027 | 0.340 |
| FOS-DN | −1.43 | −1.28 | 0.063 | 0.149 |
| YAPsh1 | −0.97 | −0.65 | 0.149 | 0.213 |
| FOSkd | −1.16 | −0.58 | 0.181 | 0.499 |

**No contrast remains significant.** The trophoblast result was carried by four
genes whose YAP responsiveness has nothing to do with placental identity. The
claim is withdrawn. (FDR here is BH within the decomposition table, a different
family from the global FDR in the panel above; both are reported so neither is
cherry-picked.)

The EVT core shares nothing with either YAP targets or mOnF, so its values are
unchanged by the same removal; only the FOS-DN contrast was ever significant
(−1.70, FDR 0.027), which on its own is not a finding.

**Audit 2 — each immune result is one gene.** Removing the single
strongest-moving gene from each set:

| contrast | set | P whole set | strongest gene (Wald) | P minus that gene |
|---|---|---|---|---|
| YAP-OE | immune suppression | 0.0036 | *Nt5e* (+24.9) | 0.387 |
| YAP-OE | cytotoxic resistance | 0.0007 | *Serpinb9* (+22.9) | 0.158 |
| YAP+FOS-OE | cytotoxic resistance | 0.0026 | *Serpinb9* (+23.2) | 0.111 |
| YAP+FOS-OE | immune suppression | 0.069 | *Nt5e* (+19.1) | 0.486 |

Set means are +5.3 and +6.5 while the top gene is +24.9 and +22.9 — the sets are
10 and 6 genes, so one outlier dominates the mean. No loss-of-function contrast
reduced either set to begin with.

The sets are also named for functions that transcript enrichment cannot
demonstrate. Their membership is:

- immune suppression: *Cd274*, *Pdcd1lg2*, *Lgals9*, *Pvr*, *Tnfrsf14*, *Fgl1*,
  *H2-T23*, *Ido1*, *Tdo2*, *Nt5e*
- cytotoxic resistance: *Cd47*, *Cd24a*, *Serpinb9*, *Birc3*, *Cflar*, *Tnfaip3*

These are genuine immune-regulatory genes, but a change in their transcripts is
not evidence that tumour cells suppress T cells or resist killing. The
programme-level claim is withdrawn.

**What survives.** Two single-gene observations: YAP overexpression strongly
induces *Nt5e* (CD73, adenosine production) and *Serpinb9* (granzyme B
inhibitor). Both are plausible immune-evasion effectors and both are worth a
targeted follow-up, but they are two genes, not a programme.

### Q2.4 Chromatin and occupancy

**Accessibility (bulk ATAC-seq, mm10).** *Tnfrsf12a* is chr17:23,675,444–23,677,449
(−), TSS 23,677,449. Peaks within 50 kb of a TSS, median log2FC, against all
other peaks:

| contrast | *Tnfrsf12a* locus (24 peaks) | mOnF gene loci (~1,050) | Lgr5 stem loci (~130) |
|---|---|---|---|
| GSE239752 A vs WT | +0.013 (p = 0.87) | **+0.444** (p = 3 × 10⁻⁵⁸) | +0.035 |
| GSE239752 AKSP vs WT | −0.137 (p = 0.95) | **+0.805** (p = 7 × 10⁻¹⁰⁷) | +0.089 |
| GSE239755 A vs WT | **+0.582** (p = 5.7 × 10⁻³) | **+0.511** (p = 1 × 10⁻⁸⁴) | +0.262 |
| GSE239755 RXRi vs WT | +0.180 (p = 0.24) | **+0.659** (p = 2 × 10⁻¹⁰¹) | −0.363 |

The two ATAC experiments disagree about this locus for the same A vs WT contrast
while agreeing about the mOnF loci, so the discordance is locus-specific. A
window ladder (10/25/50/100/250/500 kb) puts the GSE239755 signal at 10–25 kb.

**Correction made in review.** The first draft treated this as evidence against
direct regulation. That was wrong: transcription factor binding does not require
an accessibility change — YAP/TEAD and AP-1 can occupy already-open elements, and
ATAC would register nothing. Neither experiment perturbs YAP or AP-1, so neither
can test direct action at all. The accessibility result is uninformative about
mechanism, not negative evidence.

**Occupancy (ChIP-Atlas, mm10, new in review).** Mean MACS2 score of the
strongest peak within 5 kb of the *Tnfrsf12a* TSS, across all uniformly
reprocessed public mouse ChIP-seq:

| factor | arm | mean score | percentile of all genes | experiments with a peak | above this % of mOnF genes |
|---|---|---|---|---|---|
| FOSL1 | AP-1 | 604 | 96.8 | 5 / 6 | 82 |
| JUND | AP-1 | 386 | 96.8 | 26 / 34 | 87 |
| TEAD1 | YAP/TEAD | 320 | 93.6 | 19 / 24 | 75 |
| FOSL2 | AP-1 | 254 | 94.0 | 11 / 20 | 78 |
| FOS | AP-1 | 144 | 93.6 | 22 / 51 | 89 |
| JUNB | AP-1 | 124 | 90.1 | 15 / 58 | 71 |
| JUN | AP-1 | 101 | 86.7 | 32 / 87 | 78 |
| TEAD4 | YAP/TEAD | 96 | 83.4 | 12 / 32 | 70 |
| YAP1 | YAP/TEAD | 46 | 65.1 | 7 / 37 | 80 |
| TEAD2 | YAP/TEAD | — | — | 0 / 3 | — |

The locus is a bound element for both arms, above the 83rd percentile of all
genes for every factor except YAP1 itself, and above 70–89% of the authors' own
oncofetal genes.

**Two limits that keep this open.** Of 349 experiments in the panel, only four
are intestinal (2 intestinal crypt, 1 intestinal organoid, 1 intestine) and
**none of the four calls a peak** at the locus. The positive signal comes from
liver (30 experiments), MEF, macrophages, trophoblast stem cells and tumour
lines. So the occupancy evidence is context-mismatched and the in-context
experiments are negative — though four experiments is far too few to be a real
negative. And occupancy is not function: establishing that a bound element is
required would take CRISPRi or enhancer deletion.

The earlier consensus-motif scan (no TEAD or AP-1 excess in the locus peaks,
p = 0.95 and 0.23 against 408 matched background peaks) is superseded. Given that
ChIP-seq finds strong occupancy, the motif result is a limit of consensus
matching, not evidence of absent binding.

### Q2 claim ceiling

*Tnfrsf12a* expression **responds to YAP- and AP-1-associated transcriptional
programmes** in these models: seven of seven perturbations, both directions, two
independent shRNAs, padj < 10⁻⁷ throughout. That is a dependency established by
perturbation and it is the strongest result in this analysis.

**Not** established:

- that YAP/TEAD or AP-1 acts **directly** at the locus. Public ChIP-seq makes it
  plausible — the promoter is a strongly bound TEAD and AP-1 element — but no
  intestinal experiment supports it and occupancy is not functional dependence.
- that YAP and AP-1 act **on a common regulatory element**. The first draft
  inferred this from the absence of added effect when FOS is overexpressed on top
  of YAP (+0.32, p = 0.20). That inference is withdrawn: non-additivity is equally
  consistent with response saturation, with the FOS construct failing to raise
  effective AP-1 activity, with convergence on a shared downstream programme, and
  with two mechanisms sharing an output limit.
- that YAP or AP-1 regulates a **placental** programme (Audit 1) or a
  **tumour-intrinsic immune** programme (Audit 2).

---


## Q3. FOLFIRI

Recorded as requested rather than analysed — see `docs/TODO_FOLFIRI.md`. The data
(GSE237837, VAKPS tumoroids, DMSO vs FOLFIRI, 3 vs 3) is already downloaded and
checksummed, so the work is ready to start.

---

## What this does and does not do for the TWEAKR manuscript

**Strengthens.** The manuscript's central claim — that *TNFRSF12A* belongs to the
oncofetal/revival state rather than merely correlating with it — now has
perturbational support. Forcing the state up drives the receptor up; removing
either transcription factor that builds the state drives it down. No prior cohort
in the project could test this.

**Adds a mechanism, with a ceiling.** YAP and AP-1 dependence is a concrete
upstream placement. Direct regulation at the locus is not shown.

**Withdraws the placenta claim.** The trophoblast enrichment disappears when four
generic YAP target genes are removed from a 34-gene set. Nothing here supports
YAP or AP-1 regulating a placental programme, and nothing supports a
placenta-like immune tolerance phenotype. This is consistent with the earlyCRC
finding that no trophoblast axis survived expression-matched null calibration at
the invasive front — in both cohorts the placenta signal evaporates under
calibration.

**Withdraws the immune programme claim, keeps two genes.** Immune suppression and
cytotoxic resistance each collapse on removal of one gene. What remains is that
YAP overexpression strongly induces *Nt5e* (CD73) and *Serpinb9* (granzyme B
inhibitor) — two plausible immune-evasion effectors, worth a targeted test, not a
programme.

**Creates a question it cannot answer.** The manuscript's working model places
TWEAKR upstream of YAP (TWEAK → TWEAKR → YAP → oncofetal state). This dataset
shows the reverse arrow too: YAP activation raises *Tnfrsf12a*. Three models are
compatible with the evidence — TWEAKR upstream of YAP, TWEAKR a YAP target, or a
positive feedback loop in which TWEAK signalling raises YAP activity while YAP
raises receptor abundance and hence sensitivity to further TWEAK. The third would
be the most interesting and none can currently be excluded. This is a testable
hypothesis, not a mechanism we have shown.

**Does not address.** The ligand. *Tnfsf12* is flat in every single-cell
comparison here and absent from the authors' differential expression entirely.
These are epithelial organoid models with no immune compartment, so this cohort
has nothing to say about the source of TWEAK — consistent with, but not evidence
for, the earlyCRC conclusion.

---

## Review response (2026-11-02)

Reviewed once, outcome REQUEST_CHANGES with the analysis line retained. All four
requested changes are made, and three audits were run to decide them rather than
settling them by wording alone.

| # | Requested | Done |
|---|---|---|
| 1 | Downgrade the title to separate association from perturbation evidence | title is now "TWEAKR expression is associated with oncofetal identity and responds to YAP/AP-1 perturbation" |
| 2 | Delete the inference that YAP and AP-1 act on a common axis at this locus | removed from Results and listed as withdrawn in the Q2 claim ceiling; the four alternative explanations for non-additivity are stated |
| 3 | Lower the placenta and immune-tolerance interpretation | both **withdrawn** on the evidence of Audits 1 and 2 (`05`, Fig. MZ4b, c) — further than the review asked, because the audits came out negative |
| 4 | Keep the oncofetal reporter negative, do not explain it away | kept as an unresolved conflict; the draft no longer attributes it to reporter sensitivity or power |

Also changed, from points made elsewhere in the review:

- "specifically marks oncofetal cells" → "enriched in oncofetal-like tumour cells".
- "three independent libraries" → three pooled libraries of three genotypes,
  explicitly **not** biological replicates.
- The mOnF / plasticity-score independence reservation was tested, not just
  acknowledged: 14 of 51 mOnF genes are in the esophagus arm, and removing them
  attenuates the receptor correlation by ~20% without abolishing it.
- The ρ = 0.975 figure is demoted to consistency evidence, and the
  non-independence of contrasts was tested: ρ = 0.976 on an arm-disjoint subset
  of eight, so the number is not an artefact of shared control arms, but the
  caveats about Wald statistics and mixed biological settings are now stated.
- The ATAC section no longer reads as evidence against direct regulation.

New analysis prompted by the review (P0): ChIP-Atlas occupancy at the locus
(`06`, Fig. MZ4d). This is the one place where the review's priority produced a
positive result — the promoter is a strongly bound TEAD and AP-1 element — but
with two limits that keep P0 open, recorded in Q2.4.

Not done, and why: the review's second retained direction — integrating YAP
perturbation with our own TWEAKR activation data to look for a shared
oncofetal–immune response — needs the project's TWEAKR perturbation datasets,
which are outside this analysis directory. It is open item 1 below.

---

## Open items

Ordered by the review's own priorities. The review asked that only two directions
be pursued; items 1 and 2 are those, and the rest are recorded but not proposed.

1. **(review P2) Shared oncofetal–immune response across the two perturbation
   systems.** Take *Nt5e* and *Serpinb9* — the two genes that survived Audit 2 —
   and ask whether the project's own TWEAKR activation data induces them too. A
   gene induced by both YAP activation and TWEAKR activation, and not a generic
   stress response, would be the start of a real tumour-intrinsic immune axis.
   Needs datasets outside this analysis directory.
2. **(review P0, partly done) Close the direct-regulation question.** ChIP-Atlas
   shows the promoter is a bound TEAD and AP-1 element, but no intestinal
   experiment calls a peak and occupancy is not dependence. Next steps, in order
   of cost: look for YAP/TEAD CUT&RUN in intestinal organoids or CRC lines beyond
   the ChIP-Atlas panel; intersect the bound region with the ATAC peaks from
   script 03 to name a candidate element; then CRISPRi or deletion of that element.
3. **(review P1) The direction of the TWEAKR–YAP arrow.** The feedback model is
   the most interesting of the three compatible models and the most tractable:
   does TWEAK stimulation raise YAP activity in a system where *Tnfrsf12a* levels
   can be set independently?
4. **PWM motif scan.** Now lower value, since ChIP-seq supersedes consensus
   matching; would only be worth it to locate the bound element precisely.
5. **Resolve the ATAC discordance.** GSE239752 and GSE239755 disagree on the
   receptor locus for the same A vs WT contrast. Check whether the two peak
   atlases (166,913 vs 212,463 master peaks) call the same regions there, and
   whether library complexity differs.
3. **The multiome.** GSE237938 (AKSP, paired snRNA + snATAC, 325 MB, downloaded)
   can link per-cell *Tnfrsf12a* accessibility to per-cell expression, and give a
   chromVAR TEAD/AP-1 activity per cell. Not used here.
4. **Human side.** Supplementary Table S1f carries the authors' human OnF/Stem
   signatures; GSE132465 and GSE178341 are the cohorts behind Fig. 1j–l. Testing
   *TNFRSF12A* against the plasticity score at **patient level** in those cohorts
   would give the replicate-level test this mouse data cannot.
5. **The reporter negative.** Ask whether the oncofetal reporter's synthetic
   locus control region (Supplementary Table S4a) contains TEAD/AP-1 sites, and
   whether its failure to separate on *Tnfrsf12a* is informative or just underpowered.
6. **GSE263047 raw.** The one YAP/FOS-during-initiation contrast with no processed
   counts. Could be quantified from SRA if the absence-of-evidence inference in
   Q2.1 ever needs to be firmed up.
7. **Replicate structure.** Ask the authors whether per-replicate barcodes exist
   for GSE240129; that would convert every Q1 result into a properly replicated test.
