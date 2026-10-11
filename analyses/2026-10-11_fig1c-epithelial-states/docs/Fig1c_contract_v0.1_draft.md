# Fig. 1c analysis contract v0.1 (DRAFT, not frozen)

Date: 2026-10-11. Basis: GPT design consultation (`Fig1c_design_consultation_20261011.md`). Author decisions:
1. Accept GPT framing (freeze the analysis object, not the conclusion).
2. Reference-guided annotation.
3. Draft → review → Stage 1.

## 0. Scope and hypotheses

- **Population:** cohort v1 (Fig. 1b). Treatment-naive primary CRC; 13 studies, 222 patients; L1 epithelial cells (285,703), all called "tumour-derived epithelium", never "malignant".
- **H1a, state distinctness:** proCSC-like and revCSC-like configurations are reproducibly separable and co-occur within patients.
- **H1b, potency association:** within-patient CT2 contrasts for proCSC-like vs differentiated-like, revCSC-like vs differentiated-like, and proCSC-like vs revCSC-like.
- **Result branches A–F and permitted wording:** adopted from the consultation, §1.3, unchanged.
- **Wording rule:** CT2 is "predicted developmental potency", never plasticity.
- **Independence from the pilot:** DS-010 (GSE254249) is **not** one of the 13 cohort-v1 studies, so every primary estimate is independent of the pilot data. The pilot did shape the hypotheses, and the manuscript will say so.
- **Novelty context:** Mzoughi et al., Nat Genet 2025;57:402–412 (doi 10.1038/s41588-024-02058-1) reported a canonical–oncofetal (YAP/AP-1) continuum in mouse and human CRC. Fig. 1c is therefore positioned as human multi-cohort quantification and context for the TWEAK niche, not as a discovery of two states.

## 1. CT2 input

- Use the identical Fig. 1b CT2 outputs:
  - final, raw, and ds1–5 (depth-matched);
  - same cells, model version (1.1.0) and seed.
- No re-scoring on subsets.
- CCAT is used only if it passes the A3a technical gate.

## 2. Annotation (Stage 1, CT2-blinded)

The CT2 columns are physically excluded from the Stage 1 inputs. Labels are frozen with a SHA256 before Stage 3 joins them to CT2.

### 2.1 Axis L — lineage identity (reference-guided)

- **Reference:** Pelka 2021, GSE178341, author epithelial clusters cE01–cE11. Available on Argos: `GSE178341_crc10x_full_c295v4_submit_cluster.csv.gz`, with the h5 file holding counts.
- **Collapsed classes:**

  | Class | Pelka clusters |
  |---|---|
  | Stem/TA-like | cE01, cE02 |
  | Stem/TA-like proliferating | cE03 |
  | Enterocyte-like | cE04, cE05 |
  | Goblet/secretory-like | cE06, cE07, cE08 |
  | Rare lineages | Best4, tuft and EE (cE09–cE11) |

- **Classifier:** CellTypist-style regularised logistic regression on log-normalised counts, with probabilistic output and temperature/isotonic calibration on held-out patients.
- **Leakage:** Pelka is one of the 13 cohort-v1 studies (50 patients). For Pelka patients, labels come from patient-grouped 5-fold out-of-fold predictions. The other 12 studies receive predictions from the full model.
- **Training-set handling:** the reference contains normal and tumour epithelium. Both are used for training, and tumour-only training is a sensitivity analysis.
- **Thresholds:** assigned if calibrated max p ≥ 0.70 and margin ≥ 0.20. Otherwise the cell is unassigned-L. These values are provisional and frozen after held-out evaluation.
- **Sensitivity reference:** Burclaff 2022 normal colon (DS-033).

### 2.2 Axis S — stem configuration (proCSC-like / revCSC-like)

**Problem.** No human CRC reference with proCSC/revCSC labels exists in our holdings. Qin 2023 defines them in mouse organoids. The obvious human anchors (CLU, ANXA1, SOX4, LGR5, SMOC2, TOP2A, LRIG1) are already inside the frozen Qin-derived A3a gene sets, so a "disjoint marker" definition would remove the defining genes.

**Options for review:**

- **S1, gene-split (proposed primary):**
  - Split each Qin human-mapped set into a definition half and a validation half. The split is fixed by seed and stratified by expression level.
  - Score the definition half with UCell, against an expression-bin-matched random-gene null computed per sample.
  - **proCSC-like:** definition score above the 95th percentile of the sample's null, while rev is below it. revCSC-like is defined the same way in reverse. Cells above the null on both are **hybrid**.
  - The validation half must reproduce the separation, as an AUC within patients.
  - Cell-cycle genes are removed from the proCSC definition half, so that proCSC is not just S/G2M.
- **S2, external human anchors:** use the human oncofetal (OnF) programme from Mzoughi 2025 and/or EMP1-high relapse-cell signatures as the revCSC definition, with Qin sets for validation only. This depends on provenance verification of the published human gene lists.
- **S3, continuous only:** a two-axis landscape (pro × rev) with hybrid occupancy and no hard pro/rev classes. Contrasts would use the top versus bottom within-sample quintile of each axis.

### 2.3 Final state assignment

- **Precedence:**
  1. QC flag (doublet or stromal admixture);
  2. Axis S (proCSC-like, revCSC-like, hybrid);
  3. Axis L class;
  4. unassigned.
- **EMT-like:** ED only, and only after doublet and stromal-admixture QC. It is not a primary state.
- **Differentiated-like reference:** Axis L Enterocyte-like cells that are negative on Axis S.
- **Held out from every definition:** TNFRSF12A, the YAP core set, and TWEAK-response genes.

### 2.4 Stage 1 gate (annotation only, no CT2)

| Gate | Criterion |
|---|---|
| G1. L classifier performance | Pelka patient-held-out macro-F1 ≥ 0.70; per-class recall reported |
| G2. Coverage | Each primary state has ≥30 cells in ≥20 patients across ≥3 studies |
| G3. Co-occurrence | proCSC-like and revCSC-like both have ≥30 cells in the same sample in ≥20 patients across ≥3 studies |
| G4. Separation | Validation-half AUC ≥ 0.70 within patients (S1); hybrid fraction reported |
| G5. Complexity audit | AUC of log UMI / log genes for predicting each state; if > 0.75, flag the state and require the depth-matched contrast as a co-primary |
| G6. Study balance | No single study contributes > 40% of any state's eligible patients |

If G3 or G4 fails, Fig. 1c falls back to S3 (continuous) and branch F wording.

## 3. Statistics (Stage 3–4)

- Statistics follow the consultation §4, with no changes:
  - sample-level state medians;
  - patient-level paired differences;
  - study level REML + HK;
  - Holm across the 3 planned contrasts; BH across the secondary states;
  - eligibility: ≥150 epithelial cells per sample, ≥30 cells per state, ≥50 differentiated-like cells, ≥5 patients per study, ≥3 studies and ≥20 patients per contrast.
- **Mandatory sensitivities:**
  - depth-matched CT2 (ds1–5);
  - CT2 raw;
  - complexity- and cell-cycle-adjusted contrasts;
  - CCAT, if it passed its gate;
  - MSI/MSS;
  - CNV-positive subset;
  - LOSO;
  - Pelka excluded.

## 4. Scope

- **Normal–primary:** ED, Conditional GO, after Stage 3. Uses the 48-study epithelial CT2 run (`2026-10-09_fig1c-epithelial-cytotrace2`) only if its CT2 settings match Fig. 1b; otherwise it requires re-scoring.
- **Treatment:** HOLD.
- **Primary–metastasis:** NO-GO.

## 5. Order of work

Stage 0 (freeze inputs) → Stage 1 (annotation gate) → wait for A3a → Stage 3 → Stage 4 → Stage 5 (choose the wording branch).
