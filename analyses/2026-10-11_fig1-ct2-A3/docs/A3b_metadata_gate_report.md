# A3b metadata gate: normal–primary, pre/post-treatment and primary–metastasis pairs

- **Date:** 2026-10-11.
- **Status:** metadata only. **No CytoTRACE2, no expression.** For review before any A3b scoring.
- **Code:** `code/sample_metadata.py` (Argos SGE 3655108, obs only) → `code/pair_gate.py` (local).
- **Tables:** `tables/metadata_gate/`:
  - `sample_metadata.tsv`: 1,552 samples, 586 patients, 37 studies, 3,812,174 cells, manuscript scope;
  - `pair_gate_patients.tsv`;
  - `pair_gate_studies.tsv`;
  - `pair_gate_overview.tsv`;
  - `unpaired_normal_polyp.tsv`.

## Gate rules (fixed before counting)

- **Pairs:**
  - A pair is two sides from the same patient.
  - Immune-enriched (CD45+/CD3+/…) samples are dropped before counting.
  - A side is usable with ≥30 epithelial cells; ≥100 is also reported.
- **Study:** a study qualifies with ≥5 usable pairs.
- **Field consistency:** every design field is constant within each sample. The one exception is `tumor_source`, which is mixed "border|core" in 7 samples.

## 1. Overview

| Design | Studies with pairs | Pairs (metadata) | Usable ≥30 | Usable ≥100 | Qualifying studies | Pairs in qualifying studies |
|---|---:|---:|---:|---:|---:|---:|
| Normal–primary, both naive | 15 | 162 | 128 | 112 | 8 | 116 |
| Normal–primary, any treatment | 18 | 183 | 149 | 132 | 10 | 135 |
| Pre/post-treatment primary | 4 | 56 | 52 | 46 | 3 | 51 |
| Primary–metastasis, any treatment | 6 | 30 | 25 | 25 | 2 | 16 |

These counts are lower than the 2026-10-10 consultation counts (227 normal + primary, 49 primary + metastasis). The earlier counts included immune-enriched studies and patients without epithelium. For example, Wu 2022 is CD45+ sorted, so it drops out.

**Normal–primary (naive) qualifying studies:**

| Study | Usable pairs (≥30) |
|---|---:|
| Pelka | 31 |
| Chen 2024 | 19 |
| Lee | 18 |
| Joanito | 12 |
| MUI | 12 |
| Uhlitz | 11 |
| Khaliq | 7 |
| Qian | 6 |

- Platform is the same on both sides in every pair.
- MSI distribution of usable pairs:
  - MSS 65, plus 14 MSS|unknown;
  - MSI or MSI-H 24, plus 17 MSI-H|unknown;
  - unknown 8.
- Median epithelial UMI is 1.47× higher on the tumour side than on the normal side. Depth control is therefore mandatory.

## 2. Critical finding: Atlas epithelial labels follow the sample type, not malignancy

| Sample type | Atlas epithelial label |
|---|---|
| Primary tumour | 100% "Cancer cell" (476,624 of 479,927 epithelial cells; the remainder are rare lineages) |
| Adjacent normal and healthy normal | normal subtypes only (Epithelial cell, progenitor, goblet, …); 0 "Cancer cell" |
| Metastasis | "CRLM" only |
| Polyp | mixed |

In other words, "Cancer cell" in the Atlas means "epithelial cell from a tumour sample".

**Consequences:**

1. **Normal–primary.**
   - Tumour-side epithelium contains normal epithelium. In the Fig. 1b cohort, 86.9% of tumour-sample epithelium was CNV-uncertain.
   - A whole-epithelium tumour − normal difference is diluted, and it mixes changes in composition with changes in cell state.
   - CNV-based malignancy calls work poorly in MSI-H tumours: only 4.5% of MSI-H patients were CNV-clear.
2. **Pre/post-treatment.**
   - RECIST complete responders still contribute a median of about 600 "Cancer cells" per post-treatment sample: Chen 2024 9/11 CR usable, Qin 6/6.
   - After a complete response, these are most likely regenerating or normal mucosa, not residual tumour.
   - A tumour-epithelium pre/post contrast would therefore confound treatment effect, tumour regression and the replacement of tumour by normal epithelium.
3. **Metastasis.** "CRLM" epithelium may include hepatocyte or cholangiocyte contamination. This was not checked.

**Gate implication.** A3b cannot use Atlas "Cancer cell" as tumour epithelium. Before any CT2 scoring it needs a per-cell epithelial identity that does not depend on CT2. Options for review:
- (a) a normal-epithelium reference classifier trained on the adjacent-normal subtypes (stem, TA, colonocyte, goblet, …) and applied to tumour-sample epithelium, so that each cell is called normal-like or tumour-like;
- (b) CNV on the post-treatment samples. This is limited in MSI-H, and most ICI patients are MSI;
- (c) both, with discordant cells excluded.

## 3. Pre/post-treatment detail

| Study | Treatment (post) | Usable pairs | MSI | Response (post) |
|---|---|---:|---|---|
| Qin 2023 Cell Rep Med | chemotherapy: FOLFOX / FOLFOXIRI ± bevacizumab, XELOX | 27 | MSS | 20 responders / 5 non-responders / 2 NA; RECIST CR 6, PR 14, SD 5 |
| Chen 2024 Cancer Cell | anti-PD-1 (pembrolizumab / sintilimab / camrelizumab); 4 MSS patients with anti-PD-1 + CapeOx | 16 (10 MSI ICI, 2 MSS ICI, 4 MSS chemo+ICI) | mostly MSI | 14 responders / 2 non-responders among usable; CR 11, PR 6, SD 3 across all 20 metadata pairs |
| Li 2023 Cancer Cell | anti-PD-1 (± celecoxib) | 8 | 5 MSI-H, 3 NA | 7 responders / 1 non-responder |
| Yang 2023 | FOLFOX + bevacizumab | 1 | NA | responder |

- Treatment type and MSI are confounded: chemotherapy is given to MSS patients, ICI to MSI patients. Each therapy is effectively one study, so no cross-study pooling within a therapy is possible.
- Non-responders are few among usable pairs: 5 (chemo), 3 (ICI). Response-stratified inference is not feasible; descriptive only.
- Biopsy vs resection for the pre side is not recorded (`tumor_source` empty) and needs to be checked against the papers.
- Treatment type was read from Atlas `treatment_drug`, not verified per paper.

## 4. Primary–metastasis

- Only Liu 2024 (11 usable, all naive, liver) and Che 2021 (5 usable, mixed treatment) qualify. The rest have 1–4 pairs each.
- All metastases are in the liver.
- Treatment status differs between sides in some patients.

Recommendation: no A3b metastasis module now (consistent with the consultation).

## 5. Healthy normal and polyp (not pairable)

| Source | Samples / patients | Epithelial cells | Platform |
|---|---|---:|---|
| Healthy normal: Chen 2021 Cell | 90 / 59 | 69,976 | TruDrop |
| Polyp: Chen 2021 Cell | 113 / 94 | 87,326 | TruDrop |
| Polyp: Zheng 2022 | 3 / 3 | 5,198 | — |

Single-study and single-platform: descriptive only.

## 6. Proposed gate decisions (for review)

| Branch | Proposed decision |
|---|---|
| Normal–primary (naive), 8 studies / 116 pairs | **Conditional GO.** Only after a CT2-independent normal-like vs tumour-like epithelial call is frozen; primary comparison on the tumour-like cells; depth control mandatory |
| Pre/post, chemotherapy (Qin, 27, MSS) | **Exploratory GO** as a single-study ED, conditional on the same epithelial call; CR patients analysed separately or excluded from the tumour-cell contrast |
| Pre/post, ICI (Chen 2024 + Li 2023, 24 usable, mostly MSI) | **Exploratory** single-study estimates. With MSI, CNV cannot confirm malignancy, so the reference classifier is essential |
| Primary–metastasis | **NO-GO** for now |
| Healthy normal / polyp | descriptive only; NO-GO for inference |
