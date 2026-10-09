# Fig. 1B harmonized cell annotation plan (amendment A2; draft, pending review)

Written on 2026-10-09, before any CytoTRACE2 score was inspected. The L2 annotation is frozen before
CytoTRACE2 results are interpreted biologically. The annotation is designed **without reference to
CytoTRACE2**: no CytoTRACE2 output is used to define, merge or split any label, and the taxonomy is
not shaped to reproduce any expected ordering of developmental potential.

## Scope

- **Cells:** cohort v1 (13 studies, 222 patients, 1,003,249 cells).
- **New columns:** annotation is added as new columns. Existing Atlas and study labels are kept for
  validation and never overwritten.

| Column | Content |
|---|---|
| `celltype_L1` | Epithelial / Immune / Stromal (from Atlas harmonized labels; QC only) |
| `celltype_L2` | consensus cell type (below) |
| `cellstate_L3` | state within a type (cycling, IFN response, myofibroblast-like, malignant programmes, ...) |
| `malignancy` | Malignant / Non-malignant / Uncertain (epithelial only) |
| `annotation_confidence` | high / medium / low; low-confidence cells stay `Unclassified` |
| `annotation_method` | which evidence assigned the label |
| `original_celltype` | Atlas `atlas_cell_type_fine` and study `cell_type_study`, carried for validation |

## L1: keep the Atlas major lineage, with QC

- Keep the Atlas lineage. New clustering is **not** allowed to reassign L1, except for flags.
- **Flag (not reassign):**
  - cells whose marker scores contradict their L1 (likely doublets or mislabels), for example
    epithelial cells with high PTPRC + CD3E or LYZ + C1QA;
  - cells in clusters dominated by another lineage.
- Flagged cells are excluded from L2 and counted in the QC report.
- Cross-check: agreement of Atlas L1 with the independent heuristic marker lineage computed for the
  whole Atlas (`atlas_major_lineage_20261009`, WL-20261009-003).

## L2 taxonomy (human genes)

The marker panels are fixed here, written in human symbols with human orthologues (not upper-cased
mouse genes).

### Epithelial

First split by malignancy (section below). Only **non-malignant** epithelial cells get the normal
differentiation types:

| L2 | Markers |
|---|---|
| Stem-like | LGR5, OLFM4, ASCL2, SMOC2, AXIN2 |
| Enterocyte/colonocyte-like | KRT20, SLC26A3, CA1, CA2, FABP1, CEACAM7 (BEST4+ colonocytes kept as L3: BEST4, OTOP2, CA7) |
| Goblet-like | MUC2, TFF3, CLCA1, FCGBP, SPINK4, ZG16 |
| Enteroendocrine | CHGA, CHGB, NEUROD1, PYY, GCG |
| Tuft | POU2F3, TRPM5, DCLK1, SH2D6 |
| Paneth-like | DEFA5, DEFA6, REG3A, PLA2G2A (rare in colon; reported only if reproducible) |
| Unclassified epithelial | no stable pattern |

- TA/cycling is **not** an L2 type. Proliferation is the L3 state `Cycling`.
- **Malignant epithelial** is one L2 type. Its heterogeneity is described in L3 by continuous
  programme scores, not forced into normal types:
  - canonical stem (LGR5, ASCL2, OLFM4, SMOC2);
  - proliferation (MKI67, TOP2A, UBE2C, CDK1);
  - enterocyte (KRT20, SLC26A3, CA1, FABP1);
  - goblet (MUC2, TFF3, CLCA1, SPINK4);
  - secretory/endocrine (CHGA, NEUROD1, ATOH1);
  - oncofetal/revival: the project's previously validated revCSC signature, not an ad-hoc list.
    It is used **only** as an L3 descriptor. CytoTRACE2 is never used to define revCSC/proCSC
    states (to avoid circularity).

### Immune

| L2 | Markers (combinations required, not single genes) |
|---|---|
| CD4 T | CD3D, CD3E, CD4, IL7R (CD8A/CD8B low) |
| CD8 T | CD3D, CD3E, CD8A, CD8B |
| NK | NKG7, KLRD1, NCR1, GNLY, with CD3D/CD3E low |
| B | MS4A1, CD79A, CD79B, CD19 |
| Plasma | JCHAIN, MZB1, XBP1, SDC1 |
| Macrophage | C1QA, C1QB, C1QC, CD68, MERTK, APOE |
| Monocyte | FCN1, VCAN, S100A8, S100A9, CD14 |
| Dendritic cell | FCER1A, CD1C, CLEC10A (cDC2); CLEC9A, XCR1 (cDC1); LILRA4 (pDC) |
| Neutrophil | FCGR3B, CSF3R, CXCR2 |
| Mast | TPSAB1, TPSB2, CPA3, KIT |
| Unclassified immune | — |

- Treg (FOXP3, IL2RA), exhaustion (PDCD1, HAVCR2, TOX), cytotoxicity, naive/memory (TCF7, LEF1,
  CCR7) and cycling are L3 states.
- MALAT1, ADGRE1 and mouse H2 genes are not used.
- ILC and γδ T cells are kept as L3 under NK or T when they are too rare for L2.

### Stromal

| L2 | Markers |
|---|---|
| Fibroblast | DCN, LUM, COL1A1, COL1A2, PDGFRA |
| Endothelial | PECAM1, VWF, CDH5, EMCN |
| Pericyte | RGS5, PDGFRB, CSPG4, MCAM, with MYH11 low |
| Smooth muscle | MYH11, ACTG2, CNN1, DES |
| Unclassified stromal | — |

- Mural cells (pericyte, smooth muscle) are separated before fibroblast states are called. ACTA2
  and TAGLN alone define nothing.
- L3 states:
  - myofibroblast-like / myCAF-like (ACTA2, TAGLN, POSTN within fibroblasts);
  - iCAF-like;
  - cycling fibroblast;
  - lymphatic (PROX1, LYVE1, CCL21) vs vascular endothelial.
- Schwann/glial cells and ICC are not L2 types for Fig. 1B. ICC is not expected to be identifiable
  reliably; such cells are reported as Other.

## Malignancy calls (epithelial)

Evidence is combined:
1. The Atlas label (Cancer cell vs normal epithelial types).
2. CNV inference per patient with infercnv (R, installed on Argos): epithelial cells against the
   same patient's immune and stromal cells as reference. Output: a per-cell CNV score and per-patient
   clone structure.
3. The sample type (all cohort cells are primary tumour; adjacent normal is not in the cohort).
4. Normal-differentiation marker coherence.

| Call | Rule |
|---|---|
| Malignant | Atlas Cancer cell and CNV-high, **or** CNV-high clone in a patient with clear CNV structure |
| Non-malignant | Atlas normal epithelial type and CNV-low, in a patient whose malignant cells are CNV-high |
| Uncertain | discordant evidence, or a patient without detectable CNV structure (near-diploid tumours) |

CNV-negative is not taken as proof of non-malignancy. Uncertain cells are reported separately and
excluded from both malignant and non-malignant L2 estimates.

## Procedure

1. **L1 QC** as above.
2. **Per-lineage integration**, used **only** for clustering and label transfer, never as CytoTRACE2
   input:
   - Separate epithelial, immune and stromal objects.
   - scVI (`r4p3` env, scvi-tools) with study and sample as batch keys on raw counts; Harmony on PCA
     as a check.
3. **Clustering:** Leiden at several resolutions per lineage.
4. **Labelling:** combine
   - (a) cluster-level marker scores against the fixed panels;
   - (b) label transfer from the Atlas reference labels (`atlas_cell_type_fine/predicted`) on the
     same embedding;
   - (c) per-cell marker scores.
   - A cell gets an L2 label when the cluster and per-cell evidence agree (high), when two of three
     sources agree (medium), or else stays Unclassified (low).
5. **Validation:**
   - Agreement with the original study labels (`cell_type_study`) and with Atlas fine labels:
     per-study confusion tables.
   - Marker specificity per L2 type and study (detection rate in the type vs the rest).
   - Patient and study coverage per L2 type.
6. **Cross-study reproducibility (leave-one-study-out):**
   - Train a kNN classifier on the integrated embedding without study *s*, predict *s*, and compare
     with the consensus label.
   - An L2 type that is stably recovered in only one study is **not** a pan-CRC consensus type and is
     merged into its parent or reported as study-specific.
7. **Freeze:** annotation table v1 with SHA256, plus the code commit. User review happens before
   CytoTRACE2 results are interpreted by L2.

## Eligibility at L2 (for Fig. 1B panel B1 and lineage contrasts)

- A patient enters an L2 type with ≥30 cells.
- An L2 type is shown in the main panel when it has ≥5 eligible patients in ≥3 studies. Otherwise it
  goes to Extended Data with counts.
- No study is required to contain every L2 type.

## Outputs

- **Per cell** (Argos): `annotation_v1.tsv.gz` with the columns above.
- **Light** (repo):
  - per study × L2 counts and patient coverage;
  - confidence distribution;
  - confusion tables vs original labels;
  - marker specificity;
  - leave-one-study-out recovery;
  - malignancy-call summary per patient.

## Known limitations

- Atlas L1 errors that are not flagged propagate.
- The quality of the CNV reference depends on the number of immune and stromal cells per patient.
- Label transfer from Atlas labels is not independent of the Atlas annotation. The original study
  labels are the independent check, but they use heterogeneous schemes.
