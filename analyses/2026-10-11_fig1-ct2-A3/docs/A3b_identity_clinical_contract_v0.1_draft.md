# A3b contract v0.1 (DRAFT): epithelial identity call + clinical gate

- **Date:** 2026-10-11.
- **Status:** draft for review. No expression, CNV or CT2 computation for A3b has been run.
- **Scope:** identity call (Stage I), clinical gate (Stage C) and the estimands that would later be scored (Stage S, outline only; scoring is still not authorised).
- **Basis:**
  - review of `A3b_metadata_gate_report.md` (§5–7 of `A3_review_20261011.md`);
  - A3a closed (Fig. 1 claim approved).

## 0. Question and claim boundary

- **Question:** in the same patient, does predicted developmental potency (CT2) and the developmental programmes (proCSC, revCSC, Extended CIOC, YAP core) differ between:
  - (i) tumour-specimen epithelium and matched normal-mucosa epithelium; and
  - (ii) before and after neoadjuvant therapy?
- **Claim boundary:**
  - The primary normal–primary estimand is a **tissue-context** comparison.
  - Malignant-cell-intrinsic wording is allowed only for the tumour-evidence subset, and only where that subset is validated.
  - Pre/post results are cohort-specific exploratory ED.

## 1. Facts found while drafting (new; need review)

### F1 — Chen 2024 has four time points, not two

Atlas sample suffixes are I / II / III / IV. GEO GSE236581 records the treatment stage as Pre / On / Post.

| Suffix | Atlas status | Tumour samples | Normal samples | Median tumour epithelial cells |
|---|---|---:|---:|---:|
| I | naive | 20 | 19 | 1,318 |
| II | treated | 20 (T1 and T2, two regions) | 15 | 569 |
| III | treated | 11 | 11 | 1,018 |
| IV | treated | 3 | 3 | 788 |

- I = Pre is consistent with GEO.
- The mapping of II, III and IV to On or Post, and which of them is the surgical specimen, is **unverified**.
- The metadata gate summed all "treated" samples into "post", so it mixes on-treatment with post-treatment samples. **The Chen pre/post count of 16 must be recomputed per time point.**

### F2 — Li 2023 (GSE205506, PMID 37172580)

- All patients are d-MMR/MSI-H and received toripalimab ± celecoxib.
- The 10 Atlas "naive" tumour samples (suffix 3) are the pre-treatment samples. The "treated" tumour (suffix 1) and normal (suffix 2) samples are post-treatment.
- 8 patients have both.
- Biopsy versus resection is **unverified**. The pre sample is presumably an endoscopic biopsy and the post sample the resection.

### F3 — Qin 2023 (Cell Rep Med, doi 10.1016/j.xcrm.2023.101231)

- Rectal cancer, neoadjuvant chemotherapy without radiation.
- Pre = biopsy and post = surgical resection, according to the accompanying commentary (doi 10.1016/j.xcrm.2023.101232). Not yet checked against the primary Methods.
- The response grading system is unverified. Atlas carries RECIST.

### F4 — Pelka GEO object has no malignant labels

- The Pelka GEO object (GSE178341) labels every epithelial cell as cE01–cE11, including tumour-sample cells.
- There are no cM / malignant labels, so Pelka cannot supply an external malignant reference. The positive reference must come from CNV.

### F5 — Overlap with the Fig. 1b CNV calls

- Usable naive normal–primary pairs: 128.
- 105 of these patients already have Fig. 1b per-patient inferCNV on the tumour side; 56 of them have clear CNV structure.

| Study | Clear-CNV patients / usable pairs |
|---|---|
| Chen 2024 | 7/19 |
| Joanito | 9/12 |
| Khaliq | 2/7 |
| Lee | 9/18 |
| MUI | 8/12 |
| Pelka | 6/31 |
| Qian | 1/6 |
| Uhlitz | 8/11 |

- Pre/post clear-CNV patients (pre side): Qin 12/27, Chen 7/16, Li 0/8.

## 2. Stage I — epithelial identity (CT2- and programme-blind)

### I0. Cells

- All samples of eligible patients: normal side, tumour or pre side, and post side.
- Cells are L1 epithelium under the frozen Fig. 1b L1 rules (F1/F2 panel flags), applied unchanged to the new samples.
- Immune-enriched samples are excluded.

### I1. Evidence T — CNV (tumour evidence)

- **Run:** one inferCNV run per patient, with every sample of the patient included as observation groups.
- **Reference:** the patient's immune and stromal cells, using the frozen Fig. 1b L2 parameters (≤1,500 cells, half immune and half stromal, seed 0, cutoff 0.1, window 101, denoise, no HMM).
- **Calls:** CNV-high, CNV-low and intermediate, with the same reference P99/P95 rule.
- **Clear-CNV patient:** ≥20% of the **pre / primary-side** epithelial cells are CNV-high.
- **Calibration (new):** the CNV-high rate in matched normal-side epithelium is the empirical false-positive rate. A study whose median normal-side CNV-high rate exceeds 2% has its tumour-evidence calls voided.
- **Concordance:** with Fig. 1b calls for overlapping tumour samples (Cohen's κ), reported only.

### I2. Evidence N — normal-mucosa similarity (open-set, not a malignancy classifier)

- **Reference:** normal-side epithelium of the **same study**, leave-patient-out (patient p is scored against the other patients' normal epithelium).
- **Features:**
  - log1p(CP10k) over all genes;
  - 2,000 HVGs selected on the reference;
  - **excluded:** all A3a gene sets (P1 + ECOS + secondary), holdout H (Fig. 1c), cell-cycle genes (Seurat 2019), `^MT-`, `^RP[SL]`, and the Fig. 1c stress genes;
  - z-scaled; 30 PCs fitted on the reference.
- **Statistic:** mean Euclidean distance to the 15 nearest reference cells.
- **Normal similarity percentile:** relative to the null from the patients' own held-out normal-side cells (leave-patient-out distances).
- **Study gate:** ≥5 patients with ≥30 normal-side epithelial cells; otherwise the study gets "N not assessable".

### I3. Three-class rule (fixed a priori)

| Class | Rule |
|---|---|
| Normal-like | similarity percentile ≤ 90 **and** not CNV-high |
| Tumour-evidence | CNV-high in a clear-CNV patient **and** similarity percentile > 90 |
| Ambiguous | everything else, including conflicts (CNV-high but normal-like) and N not assessable without T |

- MSI-H tumours mostly lack T, so their non-normal-like cells are **ambiguous, not tumour**. This is reported, not imputed.
- **Option, for review:** Evidence C, a supervised tumour-vs-normal classifier.
  - Positives: CNV-high cells from clear-CNV patients. Negatives: normal-side epithelium.
  - L2 logistic regression, leave-study-out validation.
  - It would add a separate tier, "transcriptomic tumour-like", reported only and never merged into tumour-evidence.
  - Default: **not included**, because positives are MSS/CNV-selected and the negatives differ in tissue context.

### I4. Validation and QA (reported before any CT2 contact)

- Normal-side cells called normal-like: expected ≈90% by construction. Per study.
- CNV-high cells (clear-CNV patients) called non-normal-like: sensitivity of N for overt tumour.
- Tumour-side composition per patient (normal-like / tumour-evidence / ambiguous) by MSI and study.
- Pre/post: composition shift, especially in RECIST CR patients.
- Freeze: SHA256 of the per-cell identity table before CT2 or programme scores are joined.

## 3. Stage C — clinical gate (per cohort, from primary papers / GEO)

| Field | Qin 2023 | Chen 2024 | Li 2023 |
|---|---|---|---|
| Regimen | FOLFOX / FOLFOXIRI ± bevacizumab, XELOX (Atlas) | anti-PD-1 ± CapeOx (Atlas) | toripalimab ± celecoxib (GEO) |
| MSI | MSS (Atlas) | MSI-H majority, plus MSS | d-MMR/MSI-H (GEO) |
| Pre sample | biopsy (commentary) | I | suffix 3 |
| Post sample | resection (commentary) | II / III / IV, **mapping unverified** | suffix 1 (+ normal suffix 2) |
| Response | RECIST (Atlas); TRG? | RECIST (Atlas); pCR? | pCR (paper) |

All "unverified" cells are completed before the cohort is frozen. A patient's pair is defined by the **verified** time points only.

## 4. Stage S — estimands (outline; scoring requires a separate GO)

### Normal–primary (naive)

| Estimand | Type | Definition |
|---|---|---|
| E1 | primary, tissue context | within-patient Δ (tumour-sample epithelium − normal-sample epithelium) of the sample-median CT2 final; depth-matched by downsampling both sides to a patient-common T, plus the complexity-adjusted version; patient → study → REML + HK |
| E2 | composition | normal-like / tumour-evidence / ambiguous fractions on the tumour side; association with E1 |
| E3 | secondary, cell identity | tumour-evidence cells (tumour side) vs normal-like cells (normal side); clear-CNV patients only (≈56, MSS-enriched; labelled as such) |
| E4 | field / context | normal-like cells, tumour side vs normal side |
| Readouts | — | CT2 final (primary); proCSC, revCSC, Extended CIOC, YAP core UCell (secondary) |

### Pre/post (per cohort, never pooled across cohorts)

- **E1-pp:** tissue context, post − pre.
- **E2-pp:** composition shift.
- **E3-pp:** tumour-evidence cells on both sides; patient eligible only with ≥30 tumour-evidence cells on each side.
- RECIST CR / pCR patients go to E2-pp only.

## 5. Questions for review

1. **Evidence N:** Is a leave-patient-out, same-study, open-set kNN similarity to normal-side epithelium acceptable as the normal-like criterion? Are the 90th-percentile threshold and the gene exclusions right?
2. **CNV:** Rerun per patient with all samples, or reuse the Fig. 1b tumour-side calls and run only the new samples? (A rerun changes the reference subsample.) Is the 2% normal-side false-positive gate appropriate?
3. **Evidence C:** Include as a reported-only tier, or drop entirely?
4. **Chen 2024:** Which time-point contrasts should be primary? Pre (I) vs surgical post (III/IV, n ≈ 11–14) as primary, with I vs II (on-treatment, n ≈ 20, two regions) as secondary?
5. **Lineage matching:** Should E1/E3 also be run within the Fig. 1c Axis-L lineage classes (e.g. stem/TA-like only), so that normal–tumour differences are not just a differentiated-colonocyte composition effect?
6. **Readouts:** Are the A3a programmes allowed as secondary readouts in A3b? (They are excluded from identity features, so they are not circular.)
7. Anything that should stop A3b now (NO-GO)?
