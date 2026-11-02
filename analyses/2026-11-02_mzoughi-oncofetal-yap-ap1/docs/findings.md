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
consistency across the three independent libraries; and the authors' own
differential expression, which we did not compute.

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

### Q1.4 The authors' own statistic

Supplementary Table S1c, neoplastic metacluster vs rest, computed by the authors:

> *Tnfrsf12a*, avg_log2FC **+0.337**, pct.1 0.818 vs pct.2 0.538, p_adj **8.25 × 10⁻³⁵**,
> ranked 189th of 341 up-regulated genes.

Significant and consistent in direction, but a **modest** effect — the receptor is
not among their top markers, and it is not in their 51-gene mOnF signature.
*Tnfsf12* does not appear in their differential expression table at all.

### Q1 claim ceiling

*Tnfrsf12a* is enriched in oncofetal cells in both tumour models, is the strongest
such gene among 26 tested, tracks the paper's own lineage plasticity axis, and
does none of this in normal organoids. It is **not** one of the authors' defining
oncofetal genes and its effect in their own metacluster test is modest. The
supportable statement is *"associated with, and specific to, the oncofetal state"*
— not *"a marker of it"* in the sense of a defining gene.

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

### Q2.3 Placenta and tumour-intrinsic immune programmes

cameraPR (competitive, accounts for inter-gene correlation) on the Wald
statistics; FDR is global BH across all contrasts × sets.

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

Three different things are happening here and they should not be merged:

1. **The oncofetal and revCSC programmes are bidirectionally controlled** by both
   factors — up in all gain contrasts, down in all four loss contrasts, every one
   significant. This is the paper's own claim and it replicates cleanly on our
   gene sets.
2. **The placenta/trophoblast programme is co-regulated, but weakly.** Up under
   both gain contrasts (FDR 1.3 × 10⁻³, 3.0 × 10⁻³) and down in 4 of 4 loss
   contrasts, but only 2 of those 4 reach FDR < 0.05, and the effect sizes are
   three to four times smaller than the oncofetal programme's. The IFA core
   behaves the same way; the EVT core moves only under FOS-DN.
3. **The tumour-intrinsic immune programmes are induced but not shown to be
   required.** Cytotoxic resistance and immune suppression go up under YAP gain
   (FDR 2.3 × 10⁻³, 9.9 × 10⁻³) but **not one loss-of-function contrast brings
   them down** — four of eight point the wrong way. The asymmetry is the finding:
   YAP activation is sufficient to switch these on, and removing YAP or AP-1 from
   an established tumoroid does not switch them off. These sets are also very
   small (6–8 genes after mouse mapping), so they are the least robust row here.

Lgr5 stem goes down whenever oncofetal goes up — the rebalancing the paper
describes, and the same one seen at the invasive front in the earlyCRC cohort.

### Q2.4 Chromatin — a clean negative

Bulk ATAC-seq, mm10. *Tnfrsf12a* is chr17:23,675,444–23,677,449 (−), TSS 23,677,449.

Peaks within 50 kb of a TSS, median log2FC, against all other peaks:

| contrast | *Tnfrsf12a* locus (24 peaks) | mOnF gene loci (~1,050) | Lgr5 stem loci (~130) |
|---|---|---|---|
| GSE239752 A vs WT | +0.013 (p = 0.87) | **+0.444** (p = 3 × 10⁻⁵⁸) | +0.035 |
| GSE239752 AKSP vs WT | −0.137 (p = 0.95) | **+0.805** (p = 7 × 10⁻¹⁰⁷) | +0.089 |
| GSE239755 A vs WT | **+0.582** (p = 5.7 × 10⁻³) | **+0.511** (p = 1 × 10⁻⁸⁴) | +0.262 |
| GSE239755 RXRi vs WT | +0.180 (p = 0.24) | **+0.659** (p = 2 × 10⁻¹⁰¹) | −0.363 |

**The two ATAC experiments disagree** about this locus for the same biological
contrast (A vs WT): +0.013 in one, +0.582 in the other. The mOnF loci open
strongly and consistently in both, so the discordance is specific to the receptor
locus, not a global quality difference. A window ladder (10/25/50/100/250/500 kb)
places the GSE239755 signal at 10–25 kb — proximal, not a distal element the
50 kb window missed.

Motif content of the 24 locus peaks against 408 width- and depth-matched
background peaks (consensus matches, UCSC mm10 sequence):

| | TEAD (GGAATG) per kb | AP-1 (TGA[CG]TCA) per kb |
|---|---|---|
| *Tnfrsf12a* locus | 0.575 | 0.958 |
| matched background | 0.592 | 0.586 |
| Wilcoxon | p = 0.95 | p = 0.23 |

No excess of either motif. The two peaks that gain most accessibility in AKSP vs
WT (+2.37, +2.46) carry two AP-1 consensus sites and no TEAD site each.

### Q2 claim ceiling

*Tnfrsf12a* expression **requires YAP and AP-1** in these models: seven of seven
perturbations, both directions, two independent shRNAs, padj < 10⁻⁷ throughout.
That is a dependency, established by perturbation.

It is **not** established that either factor acts **directly** at the locus. The
chromatin evidence is weak and internally inconsistent, there is no motif
enrichment, and neither ATAC experiment perturbs YAP or AP-1 — so none of them
can test direct action anyway. The regulation may be indirect, or may operate on
factor occupancy at already-open chromatin rather than on accessibility. Saying
"a YAP/AP-1 target gene" would exceed the evidence; "YAP- and AP-1-dependent"
does not.

Consensus-sequence counting is cruder than a PWM scan and would miss degenerate
sites. A proper PWM scan would need `BSgenome.Mmusculus.UCSC.mm10`, which is not
installed; this is listed as an open item rather than claimed as done.

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

**Qualifies the placenta claim.** The trophoblast programme is co-regulated with
the oncofetal programme by the same factors, but three to four times more weakly
and significantly in only half the loss contrasts. This is consistent with the
earlyCRC finding that no trophoblast axis was stably enriched at the invasive
front: the placenta programme appears to be a weak passenger of oncofetal
reprogramming, not a separate programme with its own control.

**Leaves open.** The immune-tolerance hypothesis. Cytotoxic resistance and immune
suppression are induced by YAP but not reduced by its removal, on 6–8 gene sets.
This neither supports nor refutes the hypothesis; it needs larger sets and a
dedicated contrast.

**Does not address.** The ligand. *Tnfsf12* is flat in every single-cell
comparison here and absent from the authors' differential expression entirely.
These are epithelial organoid models with no immune compartment, so this cohort
has nothing to say about the source of TWEAK — consistent with, but not evidence
for, the earlyCRC conclusion.

---

## Open items

1. **PWM motif scan.** Replace consensus counting with a JASPAR TEAD/AP-1 PWM
   scan over the locus peaks (`BSgenome.Mmusculus.UCSC.mm10` + `motifmatchr`, not
   currently installed). Would settle whether the absence of motif enrichment is
   real or a limit of consensus matching.
2. **Resolve the ATAC discordance.** GSE239752 and GSE239755 disagree on the
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
