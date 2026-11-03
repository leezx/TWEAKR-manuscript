# Results — TWEAKR is associated with oncofetal identity and, independently but more weakly, with interferon response in human CRC liver metastasis

## TNFRSF12A is enriched in regenerative and hybrid tumour-cell states

We re-analysed the paired single-nucleus multiome cohort of Ogden, Metic *et al.*
(*Cell Genomics* 5:100881, 2025): 15 patients with colorectal cancer liver
metastasis, 21,284 nuclei, of which 16,009 are epithelial. *TNFRSF12A* is
detected in 21.4% of epithelial nuclei, which is sparse but workable; the
ligand *TNFSF12* is not (below).

Across the authors' own epithelial state labels, *TNFRSF12A* detection is
highest in the Intermediate state (35.8% of 1,319 nuclei), which the authors
describe as a hybrid of regenerative and stem phenotypes, followed by iREC
(30.3%, n = 469) and REC (30.3%, n = 998). It is lowest in differentiated and
stem-like states: Colonocyte 14.5%, Stem 12.6%, Tuft 1.5%. Stem NOTUM, the
authors' WNT-high state, sits in the middle at 19.9%.

Two features of this ranking matter. First, the receptor tracks the
regenerative axis rather than the stem axis — it is higher in REC and
Intermediate than in Stem. Second, **REC and iREC are indistinguishable**
(30.26% vs 30.28%), even though the two states differ precisely in their
inflammatory character. That observation motivates the rest of this section,
and it is also the one we are least able to test formally (below).

## The oncofetal and inflammatory associations are both real and separable

The central question is whether *TNFRSF12A* is a marker of oncofetal identity,
a responder to inflammation, or both. Three design choices make the question
answerable rather than circular.

*TNFRSF12A* is itself a member of our frozen `revCSC` set and of the
non-canonical NF-κB set, so it would have been correlated with itself in **both**
dimensions. It was removed from every gene set before scoring, and the removal
is logged by the code rather than assumed. The authors' REC/iREC labels are not
used to define the grouping, so the test does not inherit their state
definitions. And the two dimensions are nearly disjoint in membership: the
largest Jaccard index between any oncofetal and any inflammatory set is 0.040
(9 shared genes, *AREG*, *FOSL1*, *ID2*, *KLF4*, *KLF6*, *HBEGF*, *PHLDA1*,
*PHLDA2*, *GADD45B*), so neither score is a relabelling of the other.

Within each of the 12 patients that pass pre-set adequacy thresholds (≥ 100
epithelial nuclei and ≥ 5% receptor detection; CRC07, CRC09 and CRC13 are
excluded on those criteria, not on their results), we computed the partial
Spearman correlation of *TNFRSF12A* with each dimension, controlling for the
other dimension, cell-cycle phase scores and two measures of detection depth.
Patients, not cells, are the unit of inference.

Both associations survive mutual control. The oncofetal association has median
partial ρ = 0.151 and is positive in 12 of 12 patients; the interferon
association has median partial ρ = 0.071, also positive in 12 of 12. This is
the pattern predicted by a **dual-context receptor** — neither dimension
explains the other away.

But the two are not equal. The oncofetal correlation exceeds the inflammatory
one in 11 of 12 patients (median paired difference 0.072, P = 0.0015), and the
calibration against control genes separates them further. Benchmarked against
24 genes matched on detection rate, so that *n* and sparsity are held fixed,
*TNFRSF12A* has the highest oncofetal partial correlation of all 25 genes
(0 of 24 controls above it; control median 0.020, maximum 0.117). On the
inflammatory axis it ranks second: one control gene, *CLTB*, exceeds it
(0.082 vs 0.071). The inflammatory association is therefore real and
reproducible, but it is not exceptional for a gene of this abundance, whereas
the oncofetal association is.

Stratifying each patient's cells on both scores gives the same answer without
any correlation model. Receptor detection rises from 9.4% in OnF-low/IFN-low
nuclei to 16.7% with interferon alone, 23.5% with oncofetal identity alone, and
34.3% with both. Both axes contribute; the oncofetal axis contributes more.

The association is not specific to one definition of oncofetal identity. All
four oncofetal signatures tested are positive in 11–12 of 12 patients after
control, and the strongest is not `revCSC` but the **YAP regeneration**
signature (median partial ρ = 0.172), with the YAP fetal/oncofetal effector set
next (0.159). That the YAP-defined axis gives the strongest association in human
liver metastasis is consistent with — though it does not demonstrate — the
YAP-dependence we observed on perturbation in mouse organoids.

## What this dataset could not answer

**The REC vs iREC comparison is underpowered, not negative.** The cleanest test
of whether the receptor distinguishes inflammatory from non-inflammatory
regenerative cells is a paired within-patient comparison of REC and iREC. Only
5 patients carry ≥ 20 nuclei of both states. In those 5, receptor detection does
not differ (median paired difference −0.008, P = 1.0) — but neither does the
interferon score that *defines* the distinction (P = 0.62, and in the wrong
direction). **The positive control fails.** We therefore report this comparison
as carrying no evidential weight in either direction rather than as a negative
result, and the pooled observation that REC and iREC have near-identical
receptor detection remains a descriptive statement, not a test.

**The ligand line is closed by its stop rule.** *TNFSF12* is detected in at most
7.0% of nuclei of any cell type (myeloid), below the 10% adequacy threshold set
in advance. Among the 12 patients with ≥ 10 ligand-positive nuclei, the top
cellular source is epithelial in 6, myeloid in 5 and T/NK in 1 — no consistent
source across patients. Both stop-rule criteria are met and we did not pursue
the ligand further. Two things follow. This is a second, independent failure to
find macrophage-restricted *TNFSF12*, after the early-CRC cohort. And because
these are single *nuclei*, low detection of a secreted ligand cannot exclude a
protein-level source; this is a limit of the assay, not evidence of absence.

**Prior chemotherapy shifts nothing measurable.** Seven treated and eight naive
patients do not differ in receptor detection (P = 0.34), oncofetal score
(P = 0.54) or interferon score (P = 0.69). These are not paired pre/post
samples, so the comparison is confounded by patient selection, tumour genotype
and sampling time; it is reported as exploratory and cannot speak to
treatment-induced plasticity.

**Chromatin and spatial analyses were not possible.** A data audit performed
before any analysis found that E-MTAB-13652 (snATAC) and E-MTAB-13655 (Visium)
contain only raw FASTQ and metadata — no peak matrices, fragment files, spot
counts or spatial coordinates — and the Mendeley deposit contains only the
decontaminated gene-expression matrix. Reaching the planned chromatin and
spatial endpoints would require reprocessing ≈ 0.29 TB of raw sequencing from
scratch. The spatial cohort is in any case only 3 patients (CRC08, CRC09,
CRC11), which cannot support the patient-level spatial statistics the design
requires. Both lines are recorded as blocked by data availability rather than
attempted at low power.

## Summary

In human CRC liver metastasis, *TNFRSF12A* is associated with oncofetal
identity and, independently, with interferon response: a dual-context receptor
in which the oncofetal component is roughly twice as large, present in every
patient tested, and unmatched by any detection-matched control gene, while the
inflammatory component is reproducible but of a magnitude a control gene also
reaches. The receptor is highest in the hybrid Intermediate state and does not
distinguish REC from iREC, although that last comparison is underpowered. This
replicates the receptor's oncofetal association in human metastatic tissue and
in a second species, and it narrows the earlier claim: the inflammatory
association is genuine, so attributing every immune-related observation to a
TWEAKR–YAP axis is not supported.

**Claim ceiling.** "Associated with oncofetal identity in human CRC liver
metastasis, independently of interferon response, and more strongly than with
interferon response." **Not** "marks oncofetal cells", **not** "distinguishes
REC from iREC", **not** any statement about chromatin, spatial niches, direct
regulation or causal direction — none of those were testable here.

---

# Figure legends

**Figure OG1. *TNFRSF12A* is associated with oncofetal identity and,
independently but more weakly, with interferon response.**
(**a**) Percentage of epithelial nuclei with *TNFRSF12A* detected, by the
authors' own epithelial state labels; 15 patients, 16,009 nuclei. Bars coloured
by state group. (**b**) Within-patient partial Spearman correlation of
*TNFRSF12A* with the oncofetal (`revCSC`) and inflammatory (hallmark
IFN-γ) dimensions, each controlled for the other, for cell-cycle S and G2M
scores and for two depth measures. One line per patient (n = 12 eligible);
black bar, median. (**c**) The same two partial correlations for *TNFRSF12A*
(red) and for 24 detection-matched control genes (grey). Dotted line, equal
association on both axes. (**d**) Receptor detection by within-patient median
split on both scores; thin lines, individual patients; thick lines, median
across patients.

**Figure OG2. The limits of this dataset, and the negative results.**
(**a**) Paired REC vs iREC comparison in the 5 patients carrying ≥ 20 nuclei of
both states, shown with its positive control. The IFN-γ difference that defines
the two states is not recovered (red), so the receptor comparison (grey) is
uninterpretable rather than negative. Wilcoxon P above each panel.
(**b**) *TNFSF12* detection by cell type; dashed line, the 10% adequacy
threshold set in advance. (**c**) Per-patient receptor detection in epithelial
nuclei; grey, the 3 patients excluded on pre-set thresholds before testing.
(**d**) Patient-level means by prior chemotherapy exposure; every patient shown,
boxplots are median and quartiles, Mann–Whitney P above each panel.
