# A3b contract v0.2: epithelial identity, clinical gate and estimands

- **Date:** 2026-10-11.
- **Status:** v0.2 for final-head check. No A3b expression, inferCNV or CT2 computation has been run.
- **Review history:**

  | Version | Review | Outcome |
  |---|---|---|
  | v0.1 (`A3b_identity_clinical_contract_v0.1_draft.md`, 3219b10) | `A3b_contract_v0.1_review_20261011.md` | REVISE: six blocking items |

  v0.2 addresses exactly those six items (§2–§6) and adds the verified clinical manifest (§3). It adds no algorithm and does not expand the cohort. A3a stays frozen.
- **Unchanged from v0.1:** the question and claim boundary.
  - The primary normal–primary estimand is a **tissue-context** comparison.
  - Malignant-cell wording is allowed only for the validated tumour-evidence subset.
  - Pre/post results are cohort-specific exploratory Extended Data, never pooled across cohorts.
  - Primary–metastasis and healthy/polyp are NO-GO.

## 1. Cells and inputs

- **Samples:**
  - normal–primary: naive adjacent-normal and naive primary-tumour samples of the patients in `tables/metadata_gate/a3b_eligibility.tsv`;
  - pre/post: the samples in `tables/metadata_gate/a3b_clinical_manifest.tsv`.
- **Exclusions:** immune-enriched samples, per `enrichment_crosswalk.tsv`.
- **Epithelium:**
  - Definition: an Atlas epithelial label, plus the frozen Fig. 1b L1 F1 panel flag (no foreign-lineage panel ≥ epithelial panel).
  - The same definition is applied to **every** A3b sample, including tumour samples already in cohort v1, so that both sides are defined identically.
  - The Fig. 1b F2 (cluster-level) flag is not used, because it requires a joint embedding that the new samples do not have. It is reported as a cross-check on the cohort-v1 tumour samples (agreement).
- **Counts:** all-gene raw counts are exported per sample, as in `a3a_export.py`.

## 2. Evidence N — normal-mucosa similarity (blocking item 1)

- **Interpretation boundary:** N measures similarity to the study's normal-mucosa reference distribution. A cell outside the 90th percentile has deviated from that reference; this does **not** mean it is malignant. N alone never produces a tumour-evidence label.
- **Reference pool R:** per study, normal-side L1 epithelium.

  | Branch | Reference |
  |---|---|
  | Normal–primary | naive adjacent-normal samples, including patients without a usable tumour side |
  | Chen | naive (Pre) normal samples |
  | Li | post-treatment normal samples (the only normals; flagged "ICI-exposed reference") |
  | Qin | post-treatment normals (5 patients; flagged) |

  A reference patient needs ≥30 normal-side epithelial cells.
- **Balancing:** each reference patient contributes at most 300 cells (random, seed 0). All of that patient's cells are used if it has fewer.
- **Cross-fitting:** for each query patient p, the fold reference is R_p = R minus p. Inside each fold:
  1. log1p(CP10k), with library size over all genes.
  2. 2,000 HVGs (seurat flavour) selected on R_p only, after removing:
     - all A3a sets (P1 five, ECOS-38, YAP fetal effectors, Placenta);
     - Fig. 1c holdout H;
     - Seurat 2019 cell-cycle genes;
     - `^MT-`, `^RP[SL]`, `^HB[AB]`;
     - Fig. 1c stress genes.
  3. z-scale with R_p mean and SD, clip ±10.
  4. 30 PCs fitted on R_p.
  - **Statistic:** d(cell) = mean Euclidean distance to the 15 nearest R_p cells.
- **Null and threshold (cross-fitted):**
  - Within fold p, each reference patient q ∈ R_p is scored against R_p minus q, in the same fold space, with its own capped cells.
  - The null is the pooled distribution of these distances, each q weighted equally.
  - τ_p is the 90th percentile of this null.
  - Patient p's cells, from all of its samples, are then scored against R_p and compared with τ_p.
  - p's own normal cells are therefore never in p's reference or p's null.
- **Calibration check (genuinely out-of-sample, because p is excluded from both reference and null):**
  - For each study, report the distribution across patients of the normal-like fraction among p's own normal-side cells.
  - **Gate:** if the study median of that fraction is below 0.75, Evidence N is "not assessable" for the whole study. The cause is patient or batch structure dominating the reference. The threshold is not changed.
  - Study gate: ≥5 reference patients; otherwise N is not assessable.
- **Validation (reported, not used to tune):**
  - In clear-CNV patients, the fraction of CNV-high cells that fall outside τ_p (beyond the 90th percentile).
  - CNV-high cells that fall inside τ_p stay **ambiguous**; the cutoff is not moved.
- The threshold of 90 is fixed and will not be optimised.

## 3. Stage C — verified clinical manifest (blocking item 3)

- **Tables:**
  - `tables/metadata_gate/a3b_clinical_manifest.tsv`: one row per patient × sample, with stage, specimen, response system, response, residual tumour, regimen, MSI and source.
  - `tables/metadata_gate/a3b_eligibility.tsv`: funnel.
- **Code:** `code/a3b_clinical_manifest.py`, `code/a3b_eligibility.py`.

| Cohort | Verified facts | Source |
|---|---|---|
| **Qin 2023** (rectal, pMMR/MSS, 29 patients) | Pre = colonoscopic biopsy <2 weeks before NAC; the pre single-cell suspension was **cryopreserved**. Post = surgical resection (27) or endoscopic biopsy (XFZ21, XFZ36). No radiotherapy. Response = pathological TRG (Table S1): TRG0 = no viable cancer; TRG1 = small clusters remain. The Atlas "RECIST CR" field corresponds to TRG0–1 and is **not** pCR | PMC10591051 Methods + Table S1 |
| **Chen 2024** (20 Atlas patients) | Roman suffixes are visit indices, not stages. GEO `treatment stage` per sample: I = Pre for all; the last visit = Post; intermediate visits = On (P01, P08, P23: II/III On, IV Post; P03, P04, P14, P18–P20, P22: II On, III Post; P21: III Post; the others: II Post). The paper says that of 22 patients, 16 were resected; P08, P09 (and P11, P24, not in Atlas) watch-and-wait; P25 refused surgery; P02 second-line metastatic, died before surgery. **Post = surgical specimen is inferred** for resected patients from "blood collected paralleling each colonoscopy or surgery sample"; the per-visit specimen type (Fig. S1) is not machine-readable. Response = composite iRECIST/pathology; "CR" includes clinical CR and major pathological response (<10% viable), **not pCR** | GSE236581 sample characteristics; Chen 2024 STAR Methods |
| **Li 2023** (d-MMR/MSI-H, PICC trial) | Toripalimab ± celecoxib for 6 cycles before curative resection. Pre (−ICI) = suffix 3; Post (+ICI, resection) = suffix 1 (tumour bed) and 2 (normal). Atlas responder = pCR (15/19, matching the paper). Pre specimen = biopsy (inferred) | Li 2023 Results/Methods; GSE205506 |

**Consequences fixed now:**
- **Chen:**
  - P02 is excluded (not neoadjuvant).
  - The Chen primary contrast is **Pre vs Post among resected patients** (inferred surgical specimen). If the reviewer does not accept the inference, the Chen branch stays on HOLD and the rest freezes.
  - Pre vs On is secondary and descriptive.
  - On visits are never merged into Post.
  - Multiple tumour regions at one visit (T1/T2) are aggregated within the patient.
- **Li:** post tumour-bed samples of pCR patients contain no residual tumour by definition. Li is therefore restricted to **composition (E2-pp) and descriptive tissue context**. E3-pp is NO-GO a priori (MSI-H, no CNV evidence, 7/8 pCR).
- **Qin:**
  - Primary = surgical post only.
  - TRG0 patients go to composition only.
  - The pre/post contrast is confounded with specimen type (biopsy vs resection) and processing (cryopreserved vs fresh). This is stated in every Qin result; the effect is not attributed to chemotherapy alone.

## 4. Eligibility and depth (blocking item 4)

### Sample-level eligibility

| Use | Threshold |
|---|---|
| E1 (CT2 tissue context) | ≥100 epithelial cells per sample |
| Composition (E2) | ≥30 |
| E3 / E4 | ≥30 identity-qualified cells per side |

- Samples below threshold are dropped. A side is eligible if ≥1 sample qualifies.
- Multiple qualifying samples on one side are aggregated as the per-sample median, then the unweighted median across samples.
- A study enters a pooled normal–primary estimate with ≥5 eligible patients; pooling needs ≥3 studies.

### Funnel (metadata; E3/E4 counts follow Stage I)

| Contrast | ≥100 (E1) | ≥30 (E2) |
|---|---|---|
| Normal–primary (naive) | 110 patients; 98 in 7 qualifying studies (Pelka 30, Chen 18, Lee 17, MUI 12, Uhlitz 11, Joanito 5, Qian 5) | 127; 115 in 8 studies |
| Qin, Pre vs Post (surgical) | 22 (TRG0 2, TRG1 2, TRG2 13, TRG3 5) | 25 |
| Chen, Pre vs Post (resected) | 9 (MSI 6, MSS 3; CR 4, PR 5) | 11 |
| Chen, Pre vs On | 7 | 8 |
| Li, Pre vs Post | 8 (pCR 7, non-pCR 1) | 8 |

### CT2 and depth

- **Runs:** CytoTRACE2 1.1.0 whole-sample runs, identical to the Fig. 1b pipeline, for every A3b sample.
  - Tumour samples already scored in Fig. 1b reuse their original-depth scores after a hash and version check.
  - All other samples are scored new.
- **Depth-matched target:** T_s^A3b is the smallest of the 25th-percentile epithelial library sizes across the A3b sides of study s (normal and tumour; or pre and post).
  - Cells below T_s are dropped; cells above are downsampled to T_s. Seeds 1–5; the per-cell score is the mean over seeds.
  - The CT2 depth-matched run downsamples **all** cells of the sample at T_s, so the whole-sample smoothing sees the same depth on both sides.
- **Single primary CT2 estimand (E1):** within-patient difference (tumour side − normal side) of the sample-median **depth-matched CT2 final** over L1 epithelium.
- **Mandatory sensitivities, never co-primary:**
  - (i) original-depth CT2 final;
  - (ii) depth-matched **raw** model score (whole-sample smoothing differs between sides because cell number and lineage composition differ, so the raw score is mandatory);
  - (iii) complexity-adjusted: within patient, a cell-level OLS of the CT2 final rank on side, log UMI, log detected genes, mitochondrial fraction, S and G2M; the side coefficient is the patient estimate.
- **Aggregation:**
  - Normal–primary: patient → study mean with t-CI → REML + Hartung–Knapp, with PI (k−2 df), I² and LOSO.
  - Pre/post: per cohort, patient-level mean Δ with t-CI and Wilcoxon signed-rank (descriptive).

## 5. Evidence T — joint inferCNV (blocking item 2)

- **Run:** one inferCNV run per patient (infercnv 1.14.0, `r4p3`).
  - Observations: all L1 epithelial cells from every A3b sample of that patient, grouped by sample.
  - Reference: the patient's immune and stromal cells pooled over those samples, ≤1,500 cells, half immune and half stromal, seed 0.
  - All other parameters as frozen in Fig. 1b L2: cutoff 0.1, window 101, denoise, no HMM, chromosomes 1–22, reference P99/P95 calls.
- A patient with <100 reference cells is "CNV not assessable".
- **Clear-CNV patient:** ≥20% of the pre/primary tumour-side epithelial cells are CNV-high.
- **Separate output:** this is A3b `identity_v1`. Fig. 1b `annotation_v1` stays frozen and is not modified.
- **Concordance gate (per patient, pre-specified):**
  - Computed on tumour cells present in both runs: Cohen's κ over {high, intermediate, low} and clear-CNV status.
  - If κ < 0.40, **or** clear-CNV status flips, that patient's Evidence T is set to "not evaluable". Its cells cannot be tumour-evidence. The cause is investigated and reported; the result is not accepted silently.
- **Normal-side CNV-high gate:**
  - Per patient: the share of the patient's normal-side epithelial cells that are CNV-high.
  - Evaluated over patients with ≥30 normal-side epithelial cells and CNV assessable. ≥3 such patients are needed, otherwise the study is "uncalibrated" and excluded from E3.
  - If the study median exceeds 2%, Evidence T is void for the whole study. No looser cutoff is tried.
  - This is the empirical normal-side CNV-high rate, **not** a true false-positive rate.

## 6. Three-class call, Axis-L and readouts (blocking items 5–6)

### Three-class rule (unchanged)

| Class | Rule |
|---|---|
| **Normal-like** | d ≤ τ_p **and** not CNV-high |
| **Tumour-evidence** | CNV-high, in a clear-CNV patient with T evaluable and a calibrated study, **and** d > τ_p |
| **Ambiguous** | everything else |

- "Everything else" includes CNV-high cells with d ≤ τ_p, MSI-H/CNV-low cells with d > τ_p, and studies where N is not assessable without T.
- Freeze: the per-cell identity table gets a SHA256 before any CT2 or programme join.

### Evidence C

**Deleted.** There is no supervised tumour classifier and no optional branch.

### Axis-L (secondary composition sensitivity, E1-L)

- **Model:** the frozen Fig. 1c v0.3 final Axis-L model, applied unchanged.
  - It was trained on Pelka cE01–cE11 labels, with features = the Pelka ∩ Atlas genes minus H.
  - It was **not** trained on CT2 or programme scores. Programme genes are present in its feature space; this is disclosed.
- **Pre-specified classes:**
  - Absorptive differentiated-like;
  - Cycling Stem/TA.
- **Descriptive only:**
  - Stem/TA-like (lineage transfer unverified in Fig. 1c v0.3a);
  - Secretory;
  - Transitional;
  - Rare.
- **Exclusion:** Pelka is excluded from E1-L, because its normal cells were Axis-L training data.
- **E1-L:** within-class sample medians, with ≥30 class cells per side.
- **Stop rule:** a class needs ≥20 patients and ≥3 studies, otherwise it is descriptive.
- **E3-L:** exploratory, descriptive only.
- E1-L never replaces E1.

### Secondary readouts (fixed now)

- A3a UCell scores, same gene-set versions and UCell 1.3.1 definition: proCSC, revCSC, Extended CIOC-222, YAP core.
- Normal–primary: E1-type within-patient Δ of the sample-median UCell; BH over these 4 as one secondary family.
- Pre/post: descriptive.
- No proCSC→revCSC "conversion" language.

## 7. Estimand table (final)

| ID | Branch | Definition | Status |
|---|---|---|---|
| E1 | N–P | depth-matched CT2 final Δ, all L1 epithelium | **primary** |
| E1-s | N–P | original-depth, raw, complexity-adjusted | mandatory sensitivity |
| E1-L | N–P | within Axis-L class | secondary sensitivity |
| E2 | N–P | normal-like / tumour-evidence / ambiguous fractions on tumour side | descriptive |
| E3 | N–P | tumour-evidence (tumour side) vs normal-like (normal side); clear-CNV, calibrated studies | secondary selected subset (MSS-enriched; labelled) |
| E4 | N–P | normal-like cells, tumour side vs normal side | secondary |
| R | N–P | 4 programme Δ (BH family of 4) | secondary |
| E1-pp | Qin (surgical), Chen (resected Pre vs Post) | as E1, per cohort | exploratory ED |
| E2-pp | Qin, Chen, Li | composition shift | descriptive |
| E3-pp | Qin, Chen | tumour-evidence ≥30 on both sides | exploratory, only if ≥5 patients |

## 8. Execution order after FREEZE

Each step's QA goes to review before the next CT2 contact.

1. Export (all-gene counts, L1 epithelium).
2. Joint inferCNV and the concordance and normal-side gates.
3. Evidence N with cross-fitting and the calibration gate.
4. Three-class call, Axis-L projection, identity SHA256, E2 composition.
5. QA review.
6. CT2 (new samples; depth-matched both sides) and UCell.
7. Estimands.
