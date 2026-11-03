# Findings — Ogden 2025 CRC liver metastasis, TWEAKR vs oncofetal identity vs inflammation

**Date:** 2026-11-02 · **Branch:** `analysis/20261102-ogden-crclm-tweakr-onf-ifn`
**Executed by:** Claude Opus 5 for Zhixin Li · **Status:** Gate A complete; Gates B and C blocked by data availability

Every number below is read from the frozen tables in `tables/`. Script names in
brackets identify what produced each.

---

## Stage 0. Data audit (performed before any analysis)

The audit changed the scope of the project, so it is reported first.

| Resource | Accession | What is actually deposited | Usable? |
|---|---|---|---|
| snRNA-seq, 15 CRC liver metastases | E-MTAB-13651 | **raw FASTQ only** (52 ENA runs, 0.23 TB) + IDF/SDRF | no processed matrix |
| snATAC-seq, paired | E-MTAB-13652 | **raw FASTQ only** (77 runs, 0.20 TB) + IDF/SDRF | **no** peaks/fragments |
| Visium spatial | E-MTAB-13655 | **raw FASTQ** (4 runs, 0.086 TB) + 3 TIFF images | **no** counts or coordinates |
| Processed GEX | Mendeley `yd7bb3shn5` | `CRCLM_multiome_GEX_decontaminated.h5ad`, 446 MB | **yes** |
| — also in that deposit | | 2 western-blot TIFFs (MAPK) | not relevant |

Checksum of the one usable file verified against the Mendeley-published hash:
`be5059381dc618e6068f917197fe98b912a478f8e6a95bee309a8e4b65c336a2` — match.

**Consequences, decided before analysis rather than after a disappointing result:**

- **Gate A (RNA) proceeds** on the 446 MB decontaminated matrix.
- **Gate B (chromatin) is blocked.** No ATAC peak matrix, fragment file or
  peak-to-gene link is deposited anywhere. Reaching the planned endpoints needs
  `cellranger-arc` from raw FASTQ (~0.20 TB, days of compute) before the first
  biological question could be asked.
- **Gate C (spatial) is blocked and additionally underpowered.** No spot counts
  or coordinates, and the spatial cohort is **3 patients**, which cannot support
  the patient-level spatial statistics the design requires.

This is not a claim that the data are unavailable — they are, as raw reads. It
is a scope decision: two of three gates would have cost a reprocessing project
to open, and one of them would still have been underpowered at the end.

The deposited matrix contains 21,284 nuclei × 36,485 genes, 15 patients, with
`Patient`, `Sample`, `Therapy`, `Tissue`, `Cell_type`, `Cell_subtype` and the
ATAC QC columns (`TSSEnrichment`, `nFrags`) confirming these are the multiome
nuclei. All tissue is liver metastasis; there is no primary-tumour arm in this
deposit, so P2-6 (primary vs metastasis conservation) could not be run here
either.

---

## Q0. Are the two dimensions separable at all? [00_freeze_signatures.R]

If the oncofetal and inflammatory gene sets largely overlapped, no partial
correlation could separate them and the whole Gate A question would be void.

- Largest Jaccard index between any oncofetal and any inflammatory set:
  **0.040** (`onf_YAP_regen` vs `infl_TNFA_NFKB` / `infl_NFKB_canon`, 9 shared
  genes: *AREG*, *FOSL1*, *ID2*, *KLF4*, *KLF6*, *HBEGF*, *PHLDA1*, *PHLDA2*,
  *GADD45B*).
- Full pairwise overlap table: `Q0_dimension_overlap.tsv`. Full membership of
  every set: `Q0_signature_membership.tsv`.

**The two dimensions are largely disjoint.** The question is well posed.

### The circularity guard

*TNFRSF12A* is a member of three frozen sets: `revCSC_human`,
`Noncanonical_NFkB_TNFR2` and `STAT3_response`. Left in place it would have
produced a guaranteed positive correlation with itself **in both dimensions at
once** — the exact artefact that would have made a dual-context answer look
inevitable. It is stripped from every set, along with *TNFSF12*, and the
removal is printed at run time:

```
CIRCULARITY GUARD: removed TNFRSF12A from onf_revCSC
CIRCULARITY GUARD: removed TNFRSF12A/TNFSF12 from infl_NFKB_noncan
```

---

## Q1. Where is the receptor? [01]

Epithelial detection overall: **21.4%** of 16,009 nuclei.

| State | n nuclei | detection |
|---|---|---|
| Intermediate | 1,319 | **35.8%** |
| iREC | 469 | **30.28%** |
| REC | 998 | **30.26%** |
| Hypoxia | 2,481 | 25.0% |
| TA2 | 162 | 22.2% |
| TA1 | 4,116 | 21.2% |
| Stem NOTUM | 1,933 | 19.9% |
| Goblet | 323 | 16.1% |
| Colonocyte | 1,913 | 14.5% |
| Stem | 1,400 | 12.6% |
| UPR | 759 | 10.1% |
| Enteroendocrine | 71 | 9.9% |
| Tuft | 65 | 1.5% |

Two observations: the receptor tracks the **regenerative** axis rather than the
stem axis (REC and Intermediate above Stem), and **REC and iREC are
indistinguishable** — 30.26% vs 30.28%. The second is a pooled descriptive
statistic across patients, *not* a test; the paired test is in Q4 and is
underpowered.

Per-patient detection varies 0.2% to 44.0% (`Q1A_receptor_by_patient.tsv`).
Three patients fail pre-set adequacy thresholds (≥ 100 epithelial nuclei,
≥ 5% detection): **CRC07** (0.2%), **CRC09** (2.3%), **CRC13** (n = 22). They
are excluded on those criteria, fixed in advance, not on their results. **12 of
15 patients** are analysed.

---

## Q2. Model A, B or C? [01, 02] — the main result

Per patient, partial Spearman of *TNFRSF12A* against each dimension, controlling
for the other dimension, S and G2M scores, log total counts and gene count.
Patients are the unit of inference.

| Dimension | median partial ρ | patients positive | Wilcoxon P |
|---|---|---|---|
| oncofetal (`revCSC`) | **0.151** | 12 / 12 | 0.000488 |
| inflammatory (IFN-γ) | **0.071** | 12 / 12 | 0.000488 |
| **paired difference (onf − infl)** | **0.072** | 11 / 12 | **0.0015** |

**Model C (dual-context) is supported, with the oncofetal component dominant.**

A caveat on those P values, stated because it would otherwise mislead: with
n = 12 and all signs agreeing, the two-sided signed-rank test returns its
**floor** of 0.000488. Both dimensions hit the floor, so the P value does not
discriminate between them — the effect size and the calibration below do. The
paired comparison (P = 0.0015) is the test that actually separates the models.

### Calibration against detection-matched control genes [01]

24 genes matched on detection rate (receptor detection 0.214), so *n* and
sparsity are held fixed.

| Axis | receptor ρ | control median | control max | controls above receptor |
|---|---|---|---|---|
| oncofetal | 0.151 | 0.020 | 0.117 | **0 of 24** |
| inflammatory | 0.071 | 0.019 | 0.082 | **1 of 24** (*CLTB*) |

This is the sharpest distinction in the analysis. The oncofetal association is
exceptional for a gene of this abundance; the inflammatory association is real
and perfectly reproducible across patients, but a clathrin light-chain subunit
matches it. We therefore report the inflammatory link as genuine but
**not receptor-specific in magnitude**.

### Stratification, with no correlation model [01]

Within-patient median split on both scores:

| Stratum | nuclei | receptor detection |
|---|---|---|
| OnF-low / IFN-low | 4,596 | 9.4% |
| OnF-low / IFN-high | 2,520 | 16.7% |
| OnF-high / IFN-low | 2,520 | 23.5% |
| OnF-high / IFN-high | 4,592 | 34.3% |

Both axes add; the oncofetal axis adds more. The four strata are an analysis
stratification, **not** a claim that four cell states exist.

### Robustness across signature choice [01]

| Signature | median partial ρ | patients positive |
|---|---|---|
| `onf_YAP_regen` | **0.172** | 12 / 12 |
| `onf_YAP_effectors` | 0.159 | 12 / 12 |
| `onf_revCSC` | 0.151 | 12 / 12 |
| `onf_proCSC` | 0.075 | 11 / 12 |
| `infl_TNFA_NFKB` / `infl_NFKB_canon` | 0.113 | 12 / 12 |
| `infl_IFNA` | 0.091 | 12 / 12 |
| `infl_antigen_pres` | 0.082 | 12 / 12 |
| `infl_IFNG` | 0.071 | 12 / 12 |
| `infl_NFKB_noncan` | 0.065 | 12 / 12 |
| `imm_cytotox_res` | 0.064 | 11 / 12 |
| `imm_suppression` | 0.039 | 8 / 12 |

The answer does not depend on picking IFN-γ as the inflammatory representative
or `revCSC` as the oncofetal one. The strongest association of all is the
**YAP regeneration** signature — consistent with, but not evidence for, the
YAP-dependence seen on perturbation in the Mzoughi mouse organoids.

The two tumour-intrinsic immune sets are the weakest in the table.
`imm_suppression` is positive in only 8 of 12 patients. This is consistent with
the Mzoughi review outcome, where both immune-programme claims were withdrawn
after proving to rest on single genes; nothing here revives them.

---

## Q3. Negative and uninterpretable results

### Q3.1 REC vs iREC — UNDERPOWERED, NOT NEGATIVE [02]

Only **5 patients** carry ≥ 20 nuclei of both states.

| Quantity | median REC | median iREC | paired diff | P |
|---|---|---|---|---|
| receptor detection | 0.386 | 0.320 | −0.008 | 1.00 |
| receptor expression | 1.056 | 0.504 | +0.003 | 0.81 |
| **IFN-γ score (positive control)** | **0.349** | **0.275** | **−0.144** | **0.62** |
| revCSC score | 1.162 | 0.997 | −0.190 | 1.00 |

**The positive control fails.** iREC is *defined* by elevated interferon
signalling, and the comparison cannot recover that difference — it returns the
wrong sign at P = 0.62. A test that cannot detect the effect that defines its
own groups cannot be read as a negative for anything else. Recorded as carrying
no evidential weight in either direction. `Q2B_power_verdict.json` stores the
verdict in machine-readable form.

This is the one question we most wanted to answer — whether the receptor
separates inflammatory from non-inflammatory regenerative cells — and this
dataset cannot answer it.

### Q3.2 The ligand — stop rule triggered on both criteria [02]

| Criterion | Threshold (set in advance) | Observed | Met? |
|---|---|---|---|
| detection adequate | any cell type > 10% | max **7.0%** (myeloid) | no |
| source consistent | one type top in ≥ 70% of patients | epithelial 6/12, myeloid 5/12, T-NK 1/12 | no |

Detection by cell type: myeloid 7.0%, stromal 3.9%, endothelial 3.7%, T-NK-ILC
2.9%, B 1.9%, hepatocyte 1.3%, epithelial 0.8%, plasma 0%.

Two conclusions, carefully separated:

1. **Not macrophage-restricted.** This is a second independent cohort in which
   *TNFSF12* fails to be macrophage-specific, after the early-CRC data. Myeloid
   cells have the highest *rate*, but epithelial cells contribute 36.0% of all
   ligand-positive nuclei simply because there are 16,009 of them — the
   composition control the review asked for changes the picture.
2. **A nuclear-transcript negative is not a protein negative.** These are single
   nuclei and *TNFSF12* is a secreted ligand; low nuclear detection cannot
   exclude a protein-level source. This is an assay limit.

Per the stop rule we did **not** re-cluster myeloid cells at higher resolution
to look for a TWEAK⁺ subset.

### Q3.3 Chemotherapy — a null [02]

7 treated vs 8 naive patients: receptor detection P = 0.34, revCSC P = 0.54,
IFN-γ P = 0.69. Not paired pre/post; confounded by patient selection, tumour
genotype and sampling time. Exploratory only; this cannot speak to
treatment-induced plasticity, and GSE178318 remains the better cohort for that.

---

## What this does and does not establish

**Does:**

- *TNFRSF12A* is associated with oncofetal identity in human CRC liver
  metastasis, in 12 of 12 patients, after controlling for interferon response,
  cell cycle and depth, and above all 24 detection-matched control genes.
- The association is independent of inflammatory response, and roughly twice
  its size.
- An independent inflammatory association also exists, in 12 of 12 patients,
  but is matched in magnitude by a control gene.
- The receptor is highest in the hybrid Intermediate state.
- The association is strongest for the YAP-defined oncofetal axis.

**Does not:**

- Show that *TNFRSF12A* marks oncofetal cells. Detection is 21% overall and 36%
  at its highest; this is enrichment, not a marker.
- Show whether the receptor separates REC from iREC — underpowered, positive
  control failed.
- Say anything about chromatin, regulatory elements or TF occupancy at the
  human locus. No ATAC data were analysed.
- Say anything about spatial niches, SPP1 TAM co-localisation or CD8 exclusion.
  No spatial data were analysed.
- Establish direction or causality anywhere.
- Support any functional immune claim. Transcript-level association with
  interferon programmes is not immune evasion or immunosuppression.

**Known weaknesses:**

- 15 patients, of which 12 analysed; liver metastasis only, no primary arm in
  this deposit.
- snRNA-seq: nuclear transcripts, sparse, and biased against cytoplasmic and
  secreted messages.
- The oncofetal and inflammatory scores are not perfectly orthogonal (max
  Jaccard 0.040); 9 shared genes remain between the YAP and NF-κB arms.
- Signed-rank P values are at their n = 12 floor and do not discriminate.
- The proCSC set was mapped from mouse (27 → 27 genes) and is the weakest
  oncofetal set; it is reported but not relied on.
- Cell-type and state labels are the authors', inherited unexamined except
  where used only for correspondence.

---

## Open items

Ordered by what would most change the conclusion.

1. **Settle REC vs iREC in a cohort that can.** The most interesting question
   here was not answerable. It needs a cohort with many patients carrying both
   states — or primary-tumour scRNA (not snRNA) with better receptor detection.
2. **Test the YAP axis result against our own TWEAKR activation data.** The
   YAP regeneration signature gave the strongest association (ρ = 0.172). If
   TWEAKR activation in our own system moves that same signature, the
   association and the perturbation point the same way in two species. This is
   the same open item carried from the Mzoughi analysis, now with a second
   motivation.
3. **Primary vs metastasis conservation (P2-6)** using the primary CRC cohorts
   already local (Pelka, Lee, Qin), run through this exact pipeline. Cheap,
   because the pipeline exists; the deposit here has no primary arm.
4. **Chromatin (Gate B)** only if someone reprocesses E-MTAB-13652 from FASTQ,
   or if the authors are asked for peak matrices and peak-to-gene links. Worth
   an email before worth 0.2 TB of compute.
5. **Spatial (Gate C)** — not worth pursuing in this dataset at n = 3 patients
   even if the counts were deposited.
6. Ask the authors whether processed ATAC and spatial objects exist; the paper's
   analysis clearly produced them.
