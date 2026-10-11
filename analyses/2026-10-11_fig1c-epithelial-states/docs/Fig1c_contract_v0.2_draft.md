# Fig. 1c analysis contract v0.2 (DRAFT; addresses audit of v0.1)

Date: 2026-10-11.

- v0.1 audit: `Fig1c_contract_v0.1_review_20261011.md` (REVISE; 5 P0 items).
- Unchanged and already approved: §0 scope, §1 CT2 inputs, §4 scope.

## 0. Objective, population, hypotheses

- **Objective:** resolve the lineage-conditioned organisation of canonical/proliferative and revival–oncofetal transcriptional programmes in treatment-naive primary CRC epithelium, and quantify how these relate to CT2-predicted developmental potency.
- **Population:** cohort v1, i.e. epithelial cells isolated from treatment-naive primary CRC tumour specimens (tumour-specimen-derived epithelium), without assuming universal malignancy.
  - 13 studies, 222 patients, 285,703 L1 epithelial cells.
- **H1a (programme architecture):** canonical/proliferative (pro) and revival–oncofetal (rev) programmes form reproducibly identifiable stem-associated transcriptional configurations. These may present as a continuum with hybrid activation.
- **H1b (potency):** within-patient CT2 contrasts among programme-defined strata (pro-dominant, rev-dominant) and a lineage-defined differentiated reference. These contrasts are **not** functional differences between cell types.
- **Result branches:** the Stage 1 decision matrix (§5) is applied first. The CT2 branches A–F (consultation §1.3) are applied after Stages 3–4.
- **Relation to A3a:** S uses the same Qin signatures as A3a, so Fig. 1c is not an independent validation of A3a. Its increment is:
  - lineage conditioning;
  - joint pro × rev architecture and co-activation;
  - patient-level strata contrasts against a lineage reference.

## 1. CT2 inputs (FROZEN in v0.1)

- Fig. 1b outputs only: final, raw and ds1–5. No re-scoring.
- CCAT is used only if it passes the A3a technical gate.

## 2. Stage 1 — annotation (CT2-blinded)

- Inputs: A3a `export/` all-gene epithelial counts and cell covariates, and A3a UCell outputs. None of these contains CT2.
- Labels and scores are frozen (SHA256) before any join to CT2.

### 2.1 Holdout and feature provenance (P0-5)

- **Mechanistic holdout list H, frozen as a file:**
  - TNFRSF12A;
  - the A3a YAP core (12 genes);
  - TWEAK–Fn14 signalling genes TNFSF12, NFKB2, RELB, TRAF1 and BIRC3. The project has no frozen TWEAK-response gene set (checked genesets/), so this explicit list is used and stays fixed.
- H is excluded from:
  - the Axis L classifier features;
  - the "mechanism-blinded" variants of all S scores.
- **Version and hash records:** gene IDs (GENCODE v44), symbol mapping, Qin ortholog file SHA256 (A3a), retained genes per set, and the huOnF source table.

### 2.2 Axis L — reference-guided lineage (P0-2)

- **Reference:** Pelka 2021 (GSE178341), with epithelial cells carrying the original labels cE01–cE11. Tumour and normal cells are both used.
- **Training labels:** all 11 original labels. After prediction they are aggregated by a pre-set hierarchy:

  | Aggregated class | Pelka clusters |
  |---|---|
  | Stem/TA-like | cE01 |
  | Transitional stem/secretory | cE02 |
  | Cycling Stem/TA | cE03 |
  | Absorptive differentiated-like | cE04, cE05 |
  | Secretory differentiated-like | cE06, cE08 |
  | Transitional secretory/absorptive | cE07 |
  | Rare lineages | cE09–cE11 |

  Any class whose held-out recall is below 0.50 is reported as rare/uncertain.
- **Model:** L2-regularised multinomial logistic regression (sklearn 1.3.2).
  - Input: log1p(CP10k).
  - Features: HVGs selected inside each training fold, minus list H.
  - Only C is tuned.
- **Validation: nested, patient-grouped CV on Pelka.**
  - The outer 5 folds are grouped by patient, with all of a patient's normal and tumour samples kept together.
  - The inner loop tunes C and fits temperature-scaling calibration on held-out patients from the training folds.
  - Pelka patients in cohort v1 receive their outer-fold (out-of-fold) predictions. The 12 other studies receive predictions from the final model fit with the same procedure.
  - The overlap between Pelka and cohort v1 is checked by actual patient and sample IDs.
- **Reported metrics:**
  - macro-F1 and per-class precision/recall, for 11 classes and for aggregated classes;
  - pooled, tumour-only and normal-only results;
  - calibration (ECE);
  - a tissue-source check: does a classifier of normal vs tumour explain the predicted labels within each aggregated class?
- **Sensitivity:** a tumour-only training set.
- **OOD handling:**
  - OOD score = distance to the k nearest Pelka reference cells in PCA space (k = 15; PCs fitted on the reference), expressed as a percentile of the within-reference held-out distance distribution.
  - Unknown-rejection validation: leave-one-class-out on Pelka, reporting the AUROC of max-p and of the OOD score for detecting the held-out class.
  - The assignment rule (max-p, margin and OOD percentile cutoffs) is chosen on Pelka held-out data only, then frozen.
  - Cells that fail are labelled "lineage-unresolved".
  - Unresolved and OOD fractions are reported per study.

### 2.3 Axis S — programmes (P0-1)

- **Primary: S3 continuous.**
  - Qin-full proCSC (27 genes) and revCSC (32 genes) UCell scores, identical to A3a.
  - Mechanism-blinded variants exclude list H, and any divergence from the full scores is reported.
  - The joint pro × rev distribution is described per patient and per lineage class.
- **Operational strata,** used only for the CT2 contrasts:
  - Within each sample, a cell is "high" if its score is at or above the sample's 75th percentile.
  - The four strata are pro-dominant, rev-dominant, hybrid-high and neither-high.
  - The independence expectation uses each sample's actual high fractions.
  - Threshold sensitivity at the 70th and 80th percentiles.
  - Strata prevalence is never used as evidence of enrichment.
- **S1, robustness (ED):**
  - 200 repeated stratified gene-splits (seeded);
  - patient-level concordance between full and split scores;
  - stability of strata assignment across splits;
  - variants with S/G2M genes removed and with stress genes removed;
  - a leave-one-gene-out check for single-gene drivers.
- **S2, external (ED):**
  - Mzoughi 2025 huOnF signature (Supplementary Table 1f, to be retrieved and verified).
  - Report its overlap with revCSC, and its concordance using non-overlapping genes only.
  - Check whether its source cohorts overlap cohort v1.
  - If too few non-overlapping genes remain (fewer than 10), the result is labelled "non-independent convergent evidence".
- **pro-axis anchors:** Pelka cE01/cE03 identity, and a cell-cycle-adjusted pro score (partial on S/G2M). This tests whether pro carries information beyond proliferation.

### 2.4 Group construction (P0-4)

- **Primary differentiated reference:** cells with Axis L = Absorptive differentiated-like, defined independently of Axis S.
  - Those that are also pro-high or rev-high are labelled "lineage–program discordant". They are excluded from the strict reference and from the pro/rev strata, and their fraction is reported.
- **Reference sensitivities:**
  - Absorptive cells that are also neither-high;
  - all differentiated lineages (absorptive + secretory).
- **Strata membership:** pro-dominant and rev-dominant strata take cells of any lineage except the discordant ones and the reference.
  - The lineage composition of each stratum is reported.
  - A lineage-restricted sensitivity uses Stem/TA-like and Cycling cells only.

## 3. Gates (P0-3)

| Gate | Criterion | Role |
|---|---|---|
| G1 | Pelka patient-held-out macro-F1 ≥ 0.70 for aggregated classes; per-class metrics; tumour-only metrics; ECE reported | hard |
| G2 | pro and rev each have ≥ 80% gene coverage; median within-patient full-vs-split Spearman ≥ 0.80; no single gene changes the patient-level median score rank correlation by more than 0.1 | hard |
| G3 | rev vs huOnF: within-patient Spearman > 0 in ≥ 2/3 of evaluable patients (full and non-overlapping genes); pro vs cE01/cE03 identity reported | wording |
| G4 | pro–rev within-patient correlation distribution, joint occupancy, hybrid fraction and conditional specificity (rev on oncofetal genes beyond shared stemness; pro beyond the cell-cycle partial); median r ≥ 0.9 triggers a redundancy review | wording |
| G5 | each planned contrast has ≥ 30 cells per stratum, ≥ 50 reference cells, ≥ 20 patients and ≥ 3 studies; plus an eligibility / reference-availability audit (included vs excluded patients by study, MSI, depth and composition) | hard |
| G6 | pro-dominant and rev-dominant each ≥ 30 cells in one sample, in ≥ 20 patients across ≥ 3 studies | wording |
| G7 | technical dependence: association of continuous scores and strata with log UMI, log genes, mito fraction and S/G2M; reported | report |
| G8 | OOD validation as in §2.2; unresolved fraction per study | report / rule |
| G9 | one study contributing > 40% of a stratum's eligible patients → warning + LOSO | warning |
| G10 | all lists, partitions, thresholds and hashes frozen in a manifest | hard |

If many tumours with high rev lack a reference (G5 audit), Stage 3 adds a secondary continuous model: within-sample Spearman of CT2 with the pro/rev scores, conditioned on lineage class, over all evaluable patients.

## 4. Statistics (Stages 3–4; applied after Stage 1 is frozen)

- **Contrasts.** All three are prespecified, with a Holm correction across them:
  - pro-dominant − reference;
  - rev-dominant − reference;
  - pro-dominant − rev-dominant (same-sample pairs only).
  - The other lineage classes versus the reference form a BH family.
- **Unadjusted analysis:**
  - Within each sample, the median CT2 per group gives the paired difference.
  - Multiple samples from one patient are combined by an unweighted median of the sample differences.
  - Study level: mean, SE and REML + HK pooling; report the PI and I².
- **Adjusted analysis:**
  - Within each sample, an OLS of rank-CT2 on group + log UMI + log genes + mito + S + G2M gives the adjusted group contrast.
  - Fallback, if a sample has fewer than 10 cells per parameter: drop S and G2M first, then mito. The fallback is pre-set, and the fraction of samples using it is reported.
  - Pooling as for the unadjusted analysis.
- **Depth-matched analysis:**
  - The ds1–5 CT2 scores are used on identical cells, groups and patients.
  - Each replicate is pooled separately; the main ds estimate is the mean of the 5 pooled estimates, with their range reported.
  - This is a mandatory robustness endpoint. A strong potency claim must keep its direction with a CI excluding 0; otherwise the result is labelled "depth-sensitive".
- **Other sensitivities:**
  - CT2 raw;
  - CCAT, if it qualifies;
  - MSI/MSS;
  - CNV-positive subset;
  - Pelka excluded;
  - LOSO;
  - strata thresholds at the 70th/80th percentiles;
  - mechanism-blinded scores;
  - reference definitions (§2.4).
- **Equivalence:** pro and rev are not claimed to have similar potency unless an equivalence margin is prespecified. No margin is set, so no similarity claim is made.

## 5. Stage 1 decision matrix (applied before any CT2 contact)

| Outcome | Allowed | Interpretation |
|---|---|---|
| G1 pass; G2 pass; G3 and G4 support | continuous landscape + operational contrasts | distinct transcriptional configurations, possibly a hybrid continuum |
| G1 pass; G4 redundancy | continuous only | shared stem-associated programme architecture |
| G1 pass; G3 rev concordant; pro ≈ cycling | both axes; weaker pro wording | proliferation- vs oncofetal-associated programmes |
| G1 fail; G2 pass | lineage-independent description; no lineage-stratified claims | programmes, lineage unresolved |
| G2 fail | stop the two-configuration claim | unable to resolve |

## 6. Scope (FROZEN)

- Normal–primary: ED, Conditional GO.
- Treatment: HOLD.
- Primary–metastasis: NO-GO.

## 7. Order of work

1. Stage 0: freeze H, the gene sets, the Pelka partitions and the hashes.
2. Stage 1: build Axis L and Axis S and evaluate G1–G10 (CT2-blinded).
3. Freeze labels and decision branch, and review them.
4. Stage 3.
5. Stage 4.
6. Stage 5: choose the wording branch.
