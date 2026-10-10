# L2 annotation — quality report (pre-freeze)

Date: 2026-10-10. Run root (Argos): `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/l2_annotation/`.
Candidate table: `final/annotation_v1.tsv.gz`, SHA256 `1d8148063d83cdcc4dcbdd9429326c088fd6add9eaccfb29c0c9ea3623b2809b` (1,003,249 cells).
Status: **candidate; not frozen**. No CytoTRACE2 output has been computed or read. No parameter was changed after the run.
Light tables: `tables/l2/` (all numbers below come from them).

## 1. Run completion

| Step | Result |
|---|---|
| Build | 1,003,249 cells; F1 (cross-lineage marker conflict) = 33,510 (3.3%) |
| scVI | All 3 lineages pass C3 (table below) |
| Labelling | 3 lineages; F2 (cluster-level contamination) flagged **0 clusters / 0 cells** |
| infercnv | 222/222 patients assessable, 222/222 outputs present |
| Finalize | Exit 0; SHA256 written |

### scVI convergence (C3)

| Lineage | Cells | Attempts | Epochs | Rel. change (last 3 vs previous 3 validation ELBO) | Converged |
|---|---:|---|---:|---:|---|
| Epithelial | 265,780 | 1 | 30 | 0.21% | yes |
| Stromal | 88,061 | 1 | 91 | 0.10% | yes |
| Immune | 613,575 | 2 (13 → 26) | 26 | **0.496%** | yes, **by a small margin** (limit 0.5%) |

Immune passes the frozen rule, but only just. Early stopping never fired in any lineage. The curves are in `tables/l2/scvi_convergence.png`. Stability checks on Immune (§3) show no sign of under-training. We do not propose re-training under a different rule.

## 2. Final L2 composition

| L2 label | Cells | Eligible patients / studies | LOSO |
|---|---:|---|---|
| CD4 T | 167,343 | 219 / 13 | pan-CRC |
| Plasma | 121,680 | 187 / 13 | pan-CRC |
| CD8 T | 104,902 | 216 / 13 | pan-CRC |
| B | 61,503 | 175 / 13 | pan-CRC |
| Macrophage | 49,263 | 183 / 13 | pan-CRC |
| Fibroblast | 41,088 | 158 / 13 | pan-CRC |
| **Malignant epithelial (high confidence)** | **34,764** | **76 / 8** | pan-CRC |
| Monocyte | 29,044 | 165 / 12 | pan-CRC |
| Endothelial | 25,761 | 173 / 13 | pan-CRC |
| Neutrophil | 19,729 | 47 / 9 | pan-CRC |
| NK | 16,386 | 153 / 13 | pan-CRC |
| Pericyte | 13,710 | 106 / 13 | pan-CRC |
| Mast | 11,435 | 113 / 12 | pan-CRC |
| Smooth muscle | 5,196 | 45 / 12 | pan-CRC |
| Dendritic cell | 1,763 | 13 / 5 | pan-CRC (recall weak, §4) |
| Enteroendocrine | 20 | not eligible | — |
| Tuft | merged | — | study-specific → merged into Unclassified |

| Excluded / unresolved | Cells | Share of all cells |
|---|---:|---:|
| Epithelial, malignancy uncertain | 230,946 | 23.0% |
| L1_flagged (F1) | 33,510 | 3.3% |
| Unclassified immune | 30,527 | 3.0% |
| Unclassified stromal | 2,306 | 0.2% |
| Other (not annotated) | 2,323 | 0.2% |
| Unclassified epithelial | 50 | <0.01% |

## 3. Annotation stability and integration checks

| Lineage | Consensus unchanged vs r=1.0 (r0.5 / r1.5 / r2.0) | ARI, scVI vs Harmony Leiden | Confidence (high / medium / low / flagged) |
|---|---|---:|---|
| Immune | 97.9 / 97.7 / 97.4% | 0.58 | 78.7 / 15.4 / 4.9 / 0.9% |
| Stromal | 97.0 / 98.5 / 98.2% | 0.54 | 76.4 / 13.0 / 2.4 / 8.2% |
| Epithelial | 93.7 / 92.1 / 87.1% | **0.26** | 12.2 / 0.0 / 80.8 / 7.0% (low = malignancy uncertain) |

The low Epithelial ARI is expected: tumour epithelium clusters by patient, and Harmony and scVI correct patient structure differently. Epithelial L2 does not depend on clustering, because the malignancy call is made per cell from CNV and the atlas label.

Marker specificity (`l2_marker_specificity.csv`; median per-study detection in the type vs the rest of its lineage):

| Type | Markers: in type vs rest |
|---|---|
| NK | NKG7 0.81 vs 0.19; KLRD1 0.69 vs 0.09; CD3D 0.10 vs 0.44 |
| Neutrophil | FCGR3B 0.55 vs 0.01; CSF3R 0.62 vs 0.04; S100A8/9 ≈ 0.8 |
| Dendritic cell | CD1C 0.89; CLEC10A 0.90; FCER1A 0.84 — mostly cDC2; XCR1/CLEC9A (cDC1) ~0.05–0.08 |

## 4. Cross-study label reproducibility (LOSO)

Weighted mean recall is ≥0.89 for every immune and stromal type except Dendritic cell: 0.75 weighted, minimum 0.26 in one held-out study. Malignant epithelial recall is 1.00.

Tuft was recovered in only 1 study, so it was merged per the pre-registered rule.

Dendritic cell passes the eligibility rule (≥3 studies) but is small: 1,763 cells, 13 eligible patients in 5 studies. Its cross-study reproducibility is weak.

## 5. Main issue: epithelial malignancy calls (C4)

- Of 265,780 epithelial cells (after F1), the pre-registered CNV rule gives:
  - **34,764 high-confidence malignant** (13.1%), from 78 patients in 8 studies;
  - **70 high-confidence non-malignant**;
  - **230,946 Uncertain** (86.9%).
- The C1 sensitivity class "putative non-malignant epithelial" holds 3,206 cells.
- Nearly all epithelial cells carry an Atlas `Cancer *` label. This cohort contains essentially no normal epithelium, so normal epithelial subtypes (stem-like, goblet-like and so on) are effectively empty.

### Where the Uncertain cells come from

**1. Study-level gate.** 5 studies fall below the 0.50 study rule (fraction of CNV-clear patients) and are excluded entirely:

| Study | Fraction of patients CNV-clear |
|---|---:|
| Pelka 2021 | 0.34 |
| Qin 2023 | 0.44 |
| Chen 2024 | 0.37 |
| Li 2023 | 0.00 |
| Qian 2020 | 0.29 |

Together these 5 studies hold 170,953 epithelial cells, which is 74% of the Uncertain cells. In them every cell is Uncertain.

**2. Patient-level gate** in the remaining 8 studies, then the per-cell P99 cut-off against the reference.

### The gates are confounded with microsatellite status

| Microsatellite status | Patients CNV-clear | Patients |
|---|---:|---:|
| MSS | 67.5% | 151 |
| MSI | 33% | 15 |
| MSI-H | **4.5%** | 44 |

This is the known near-diploid MSI-H genome, not a technical failure. Consequences:

- The high-confidence malignant set is strongly enriched for MSS tumours.
- The study-level gate removes studies partly because they contain MSI-H patients (Pelka 2021, for example). Even MSS patients inside the gated studies are only 52% CNV-clear.
- Any Fig. 1B epithelial-vs-stromal or epithelial-vs-immune comparison built on "Malignant epithelial" therefore describes MSS-enriched, CNV-high tumour cells from 8/13 studies and 76 eligible patients. It does not describe CRC epithelium in general.

## 6. Decisions requested from review (nothing implemented)

The pre-registered rule was applied unchanged. Options for Fig. 1B:

- **A. Keep the rule as frozen (recommended as primary).**
  - Epithelial compartment = high-confidence malignant only: 76 patients, 8 studies.
  - State the MSS enrichment explicitly, and report MSI status for every epithelial contrast.
  - Report Uncertain cells as excluded with counts (C4).
- **B. Add a pre-declared descriptive sensitivity row**, "all tumour-derived epithelium" (L1 Epithelial, not F1-flagged; 265,780 cells, 222 patients, 13 studies).
  - It is labelled as not malignancy-resolved and is not used for claims.
  - Because it is being declared after seeing the malignancy result, it would be a dated amendment.
- **C. Amend the malignancy rule** (for example drop the study-level gate, or exempt MSI-H).
  - We advise against this, because it would be a change made after the malignancy results were seen.

Other items to confirm:

1. **Immune scVI**: accept convergence at 0.496% (we propose yes, under the frozen rule).
2. **Dendritic cell**: keep in the main panel with the weak-reproducibility note, or move to Extended Data.
3. **F2 (cluster-level contamination)** flagged nothing at threshold 0.5. We propose reporting this as is; F1 already removed 3.3% of cells.
4. **Freeze**: freeze `annotation_v1` at the SHA256 above, then run full 13-study CytoTRACE2 under A2.1.

## 7. Review outcome (2026-10-10): GO, annotation_v1 frozen

The annotation-quality review in the same ChatGPT review conversation approved the freeze and the full 13-study CytoTRACE2 run.

**Epithelial option:** neither A nor C. B's whole-epithelium framing is used within the original A2.1 primary analysis:

| Level | Cells used | Status |
|---|---|---|
| Primary L1 | Atlas Epithelial / Immune / Stromal, frozen 222 patients | unchanged (A2.1) |
| L1 QC sensitivity | the same, excluding F1-flagged cells | supporting sensitivity |
| Malignant L2 | 34,764 high-confidence malignant cells | selected L2 subset; never substituted for the epithelial compartment |

Review rulings on the other items:

- **Immune scVI:** PASS.
- **Dendritic cell:** kept in the main panel, with the note "mainly cDC2, weak reproducibility in some studies".
- **F2 = 0:** reported as is.
- **F1:** study-dependent (for example Joanito epithelial 18.0%, Qian stromal 18.9%), so it is handled by the F1-clean sensitivity, not by re-thresholding.
- **Epithelial ARI 0.26:** not a freeze blocker. It is a limitation for any future malignant-state discovery.

**Figure guidance:**

- Fig. 1B shows the L1 compartments (222 patients).
- The L2 landscape goes in Fig. 1C or Extended Data, with patient and study coverage shown per type. If L1 and L2 are mixed in one panel, the different annotation resolution must be marked.
- Malignant epithelial states are described by continuous L3 programmes.

**Freeze:**

- SHA256 was re-verified on Argos (`1d8148063d83…`).
- The files were made read-only.
- `final/FROZEN.txt` records the decision.
- No annotation parameter or label was changed.
