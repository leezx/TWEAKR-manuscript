# Fig. 1c analysis contract v0.3 — FROZEN 2026-10-11

## Review history

| Version | Review | Outcome |
|---|---|---|
| v0.1 | `Fig1c_contract_v0.1_review_20261011.md` | REVISE (5 P0) |
| v0.2 | `Fig1c_contract_v0.2_finalcheck_20261011.md` | REVISE (5 P0), with an explicit statement: "after these five, FREEZE v0.3 and execute Stage 1" |

v0.3 applies exactly those five fixes and changes nothing else. Any later change requires a dated amendment section that names its reason. No change to Stage 1 rules is allowed after any CT2 contact.

## 0. Objective, population, hypotheses

- **Objective:** resolve the lineage-conditioned organisation of canonical/proliferative (pro) and revival–oncofetal (rev) transcriptional programmes in treatment-naive primary CRC epithelium, and quantify how these relate to CytoTRACE2 (CT2)-predicted developmental potency.
- **Population:** cohort v1 (Fig. 1b; 13 studies, 222 patients, 285,703 L1 epithelial cells).
  - These are epithelial cells isolated from treatment-naive primary CRC tumour specimens (tumour-specimen-derived epithelium), without assuming universal malignancy.
- **H1a:** pro and rev form reproducibly identifiable stem-associated transcriptional configurations. These may present as a continuum with hybrid activation.
- **H1b:** within-patient CT2 contrasts among programme-defined strata and a lineage-defined differentiated reference. These are not functional differences between cell types.
- **Wording:**
  - CT2 = "predicted developmental potency", never plasticity.
  - Strata are "programme-defined strata", not cell types.
- **Interpretation branches:**
  - The Stage 1 decision matrix (§5) is applied first.
  - The CT2 result branches A–F (`Fig1c_design_consultation_20261011.md` §1.3) are applied after Stages 3–4.
- **Relation to A3a:** Fig. 1c uses the same Qin signatures, so it is not an independent validation of A3a.
- **Pilot independence:** DS-010 is not among the 13 studies.

## 1. CT2 inputs

- Fig. 1b outputs only: final, raw and ds1–5. No re-scoring.
- CCAT is used only if it passes the A3a technical gate.

## 2. Stage 0 — frozen inputs

### 2.1 Mechanistic holdout list H

H = TNFRSF12A + the A3a YAP core (12 genes) + TNFSF12, NFKB2, RELB, TRAF1 and BIRC3. The project has no frozen TWEAK-response set.

Observed overlaps, before any CT2 contact:

| Set | Genes in H |
|---|---|
| revCSC (32) | TNFRSF12A, ANKRD1, AREG, BASP1, CLDN4 |
| proCSC (27) | BIRC5 |

The YAP core membership is checked against the A3a private file at freeze.

### 2.2 External signatures

Mzoughi et al., Nat Genet 2025;57:402–412, Supplementary Table S1f (ESM1, SHA256 `a2ad69ef…`; retrieved 2026-10-11):

- hOnF: 16 genes;
- hStem: 25 genes.

| Pair | Shared genes |
|---|---|
| hOnF ∩ revCSC | 2 |
| hOnF ∩ proCSC | 0 |
| hStem ∩ proCSC | 1 |
| hStem ∩ revCSC | 2 |
| hOnF ∩ H, hStem ∩ H | 0 |

The **non-overlapping** versions (hOnF-no, hStem-no) remove every gene in proCSC ∪ revCSC.

### 2.3 Fixed gene lists

- Cell-cycle (CC) genes: Seurat `cc.genes.updated.2019` (S ∪ G2M).
- Stress genes: FOS, FOSB, JUN, JUNB, JUND, ATF3, EGR1, HSPA1A, HSPA1B, HSPA8, DNAJB1, DUSP1, IER2, IER3, ZFP36, KLF6, SOCS3, NR4A1.

### 2.4 Hashes

All gene lists, Pelka partitions, model hyper-grids and thresholds are written to `stage0_manifest.json` with SHA256 values before Stage 1 runs.

## 3. Stage 1 — annotation (CT2-blinded)

- **Inputs:**
  - A3a `export/counts/*.main.h5` and `export/cells/*.cells.tsv.gz`;
  - A3a `ucell/*.ucell.tsv.gz` (variant main);
  - Pelka GSE178341 h5 + cluster + metatables.
- No CT2 file is opened.
- Stage 1 outputs are frozen with a SHA256 before Stage 3 joins them to CT2.

### 3.1 Axis L — reference-guided lineage

- **Reference:** Pelka epithelial cells (`clTopLevel == Epi`, cE01–cE11), tumour and normal.
- **Classifier:** trained on the 11 original labels, then aggregated:

  | Aggregated class | Pelka clusters |
  |---|---|
  | Stem/TA-like | cE01 |
  | Transitional stem/secretory | cE02 |
  | Cycling Stem/TA | cE03 |
  | Absorptive differentiated-like | cE04, cE05 |
  | Secretory differentiated-like | cE06, cE08 |
  | Transitional secretory/absorptive | cE07 |
  | Rare lineages | cE09–cE11 |

  An aggregated class with held-out recall below 0.50 is reported as rare/uncertain.
- **Features and model:**
  - Input: log1p(CP10k), with CP10k computed over all genes.
  - Genes: the intersection of the Pelka and Atlas gene spaces, minus H.
  - The top 2,000 HVGs (variance of log-normalised values) are selected inside each training set.
  - Features are z-scaled with the training mean and SD, clipped at ±10.
  - Model: L2 multinomial logistic regression (sklearn 1.3.2), `class_weight=balanced`.
  - Training cells are capped at 8,000 per original class, sampled randomly with seed 14.
  - C ∈ {0.01, 0.1, 1}.
- **Nested patient-grouped CV:**
  - Outer: 5 folds by Pelka patient (PID), with all of a patient's normal and tumour samples in one fold.
  - Inner, on the training patients: 20% of patients form the calibration set; the remaining 80% are used for a 3-fold grouped search over C (macro-F1); refit on that 80%; then fit temperature scaling (NLL) on the calibration patients.
  - Pelka cells in cohort v1 receive their outer-fold predictions, matched by sample + barcode.
  - The other 12 studies receive predictions from the final model, which runs the same procedure on all Pelka patients.
- **Aggregated probability:** the sum of the member-class probabilities.
- **OOD score:**
  - 50 PCs fitted on the scaled training-80% reference.
  - Mean distance to the 15 nearest reference cells.
  - Expressed as a percentile of the same statistic in the calibration patients.
- **Assignment rule (fixed a priori, then reported on held-out Pelka):**
  - aggregated max-p ≥ 0.70;
  - margin to the second class ≥ 0.20;
  - OOD percentile ≤ 99.
  - Cells failing the rule are "lineage-unresolved".
- **Reported metrics:**
  - macro-F1 and per-class precision/recall, for 11 and for aggregated classes;
  - pooled, tumour-only and normal-only results;
  - ECE (15 bins).
- **Tissue-source check:** within each true aggregated class, the predicted-label distribution by tissue.
- **Tumour-only training sensitivity:** same outer folds, evaluated on tumour test cells.
- **Leave-one-aggregated-class-out:** the AUROC of (1 − max-p) and of the OOD percentile for detecting the held-out class.
- **Per study:** unresolved and OOD fractions.

### 3.2 Axis S — programmes

- **Primary:** A3a Qin-full proCSC (27) and revCSC (32) UCell scores (main variant), unchanged.
- **New UCell sets,** scored per sample with A3a `a3a_ucell.R` on the same main counts:
  - mechanism-blinded pro and rev (minus H);
  - pro minus CC genes;
  - pro and rev minus stress genes;
  - hOnF, hOnF-no, hStem and hStem-no;
  - 200 seeded gene-splits per set (definition half = ⌈n/2⌉ genes, stratified by Atlas mean-expression tertile);
  - leave-one-gene-out (LOGO) for each gene of pro and rev.
- **Operational strata,** computed within each sample:
  - "high" = score ≥ the sample's 75th percentile.
  - The strata are pro-dominant, rev-dominant, hybrid-high and neither-high.
  - Sensitivity thresholds: 70th and 80th percentiles.
  - The independence expectation uses the actual high fractions.
  - Strata prevalence is never used as evidence of enrichment.

### 3.3 Group construction

- **Primary reference:** ALL Axis-L Absorptive differentiated-like cells, with **no Axis-S filter**.
  - Reference cells that are pro- or rev-high stay in the reference and are flagged lineage–program discordant; their fraction is reported.
- **Reference sensitivities:**
  - Absorptive + neither-high;
  - Absorptive + Secretory.
- **pro-dominant and rev-dominant strata:** non-reference cells only.
  - The lineage composition of each stratum is reported.
  - The contrasts therefore include lineage-composition differences and are not pure programme effects.
- **Mandatory within-lineage sensitivity:** pro-dominant vs rev-dominant restricted to Stem/TA-like + Cycling Stem/TA cells.

## 4. Gates

**Statistics shared by G2–G4.** Cell-level Spearman ρ is computed within each sample. A patient value is the median over that patient's samples. Pooling uses Fisher z, then patient, then study (REML+HK; A3a `reml_hk`). A sample is evaluable if it has ≥ 100 epithelial cells, as in A3a.

| Gate | Operational definition | Pass rule | Role |
|---|---|---|---|
| G1 Lineage transfer | outer-CV macro-F1 over aggregated classes, all held-out Pelka cells | ≥ 0.70; tumour-only, normal-only and per-class values reported | hard |
| G2 Programme integrity | (a) Atlas gene coverage of pro and rev. (b) Per sample and split: ρ(full, definition-half); patient = median over samples of the median over 200 splits; overall = median over patients. (c) LOGO: per gene g, overall median of ρ(full, minus-g), computed the same way | (a) ≥ 0.80; (b) overall ≥ 0.80 for pro and rev; (c) 1 − ρ ≤ 0.10 for every g | hard |
| G3 External concordance | ρ(rev, hOnF-no) and ρ(pro, hStem-no); full-overlap versions reported | rev: patient ρ > 0 in ≥ 2/3 of evaluable patients AND pooled ρ CI > 0. Unassessable if hOnF-no has < 10 genes present in the Atlas → G3-supported wording forbidden. pro: same rule with hStem-no, reported | wording |
| G4 Distinguishability | (a) ρ(pro, rev). (b) Partial ρ(rev, hOnF-no \| pro, S, G2M). (c) Partial ρ(pro, hStem-no \| rev, S, G2M). Partials use rank residuals within sample. (d) Hybrid-high fraction against the independence expectation (descriptive) | "Distinct configurations" wording is supported only if: (a) median patient ρ < 0.90; (b) pooled partial CI > 0; (c) pooled partial CI > 0. Otherwise the result is descriptive or "shared architecture" | wording |
| G5 Coverage (contrast-specific) | pro vs ref: pro ≥ 30 and ref ≥ 50 in the sample. rev vs ref: rev ≥ 30 and ref ≥ 50. pro vs rev: pro ≥ 30 and rev ≥ 30 in the same sample, no reference needed. A study enters a contrast with ≥ 5 eligible patients. Each contrast has its own funnel | per contrast: ≥ 20 patients and ≥ 3 studies. Plus an eligibility audit: included vs excluded patients by study, MSI, median UMI and lineage composition | hard (per contrast) |
| G6 Co-existence | samples with pro-dominant ≥ 30 and rev-dominant ≥ 30 cells | ≥ 20 patients and ≥ 3 studies | wording |
| G7 Technical dependence | within-sample ρ of pro, rev and stratum membership with log UMI, log genes, mito fraction, S and G2M; pooled | reported | report |
| G8 OOD | §3.1 validation; unresolved fraction per study | reported | report |
| G9 Study balance | share of each contrast's eligible patients coming from one study | > 40% → warning + LOSO | warning |
| G10 Provenance | Stage 0 manifest and Stage 1 output hashes | complete | hard |

If the G5 audit shows that more than 25% of patients in the top rev tertile (by patient-median rev) lack an eligible reference, Stage 3 adds a secondary continuous model: within-sample ρ(CT2, rev) and ρ(CT2, pro), stratified by lineage class, over all evaluable patients.

## 5. Stage 1 decision matrix (applied before any CT2 contact)

Formal operational contrasts are allowed only if **G1, G2, G5 (for that contrast) and G10** pass. G3 and G4 set the wording.

| Outcome | Allowed | Interpretation |
|---|---|---|
| G1/G2/G5/G10 pass; G3 and G4 pass | continuous landscape + contrasts | distinct transcriptional configurations, possibly a hybrid continuum |
| Same gates pass; G4 fails (a) | continuous; contrasts reported as descriptive | shared stem-associated programme architecture |
| Same gates pass; G3 rev passes; G4 (c) fails | both axes; weaker pro wording | proliferation- vs oncofetal-associated programmes |
| G1 fails; G2 passes | lineage-independent description only | programmes, lineage unresolved |
| G2 fails | stop the two-configuration claim | unable to resolve |

## 6. Statistics (Stages 3–4)

- **Contrasts:**
  - Holm across: pro-dominant − ref; rev-dominant − ref; pro-dominant − rev-dominant.
  - BH across: the other aggregated lineage classes − ref.
- **Unadjusted analysis:**
  - Sample: difference of the group medians of CT2 final.
  - Patient: unweighted median over that patient's samples.
  - Study: mean, SE and REML+HK pooling (A3a `reml_hk`); report the 95% CI, PI (k − 2 df) and I².
- **Adjusted analysis:**
  - Within each sample, an OLS of **raw CT2 final** on group indicator + log UMI + log genes + mito + S + G2M, fitted on the two compared groups.
  - The coefficient is a conditional mean difference, used for direction and robustness only. No % attenuation is computed against the median difference.
  - A sample is adjusted-eligible if it has ≥ 70 cells in the two groups combined (10 per parameter); otherwise it is adjusted-ineligible.
  - A reduced model (log UMI + log genes) is a **separate** sensitivity analysis and is never mixed with the full model.
- **Depth-matched analysis:**
  - For each ds replicate r = 1–5, compute the sample-level and patient-level differences exactly as in the unadjusted analysis, on the identical cells, groups and eligibility.
  - Patient estimate = mean over the 5 replicates.
  - Study pooling as above gives the formal 95% CI.
  - Variability between replicates (SD and range of the 5 pooled replicate estimates) is reported separately and is not biological uncertainty.
  - This is a mandatory robustness endpoint. A strong potency claim needs the same direction with a CI excluding 0; otherwise the result is labelled "depth-sensitive".
- **Other sensitivities:**
  - CT2 raw;
  - CCAT, if it qualifies;
  - MSI/MSS;
  - CNV-positive subset;
  - Pelka excluded;
  - LOSO;
  - strata thresholds at the 70th/80th percentiles;
  - mechanism-blinded scores;
  - reference sensitivities;
  - within-lineage pro vs rev;
  - reduced adjusted model.
- **No equivalence claim:** no margin is prespecified.

## 7. Scope

- Normal–primary: ED, Conditional GO, after Stage 3.
- Treatment: HOLD.
- Primary–metastasis: NO-GO.

## 8. Order of work

1. Stage 0 (manifest).
2. Stage 1 (Axis L, Axis S, gates G1–G10; CT2-blinded).
3. Freeze labels and the decision branch; send them for review.
4. Stage 3.
5. Stage 4.
6. Stage 5 (wording branch).

---

## Amendment v0.3a — OOD rule (2026-10-11; approved in principle in `Fig1c_stage1_review_20261011.md`, option B)

**Reason.**
- The frozen v0.3 OOD veto (kNN distance > the Pelka calibration 99th percentile) rejected almost whole studies: Joanito 100%, Uhlitz 96%, Liu 94%.
- In those studies gene coverage was 1.0 and median max-p was 0.95–0.98.
- In the Pelka leave-one-class-out benchmark, the OOD score detected unknown classes poorly (AUROC 0.54–0.71).
- These diagnostics were obtained before any CT2 contact. No CT2 file has been opened.

**Change (the only one).**
- Primary lineage assignment = aggregated max-p ≥ 0.70 AND margin ≥ 0.20. The thresholds are unchanged.
- The OOD percentile is still computed and stored.
- The v0.3 labels (with the OOD veto) are kept unchanged as the mandatory "original OOD-pass" sensitivity analysis. Their SHA256 values are in `tables/stage1/stage1_gate_summary.json`.
- **Unchanged:** the classifier, folds, calibration, Axis S, holdouts, the reference definition, strata thresholds and all statistics.

**Lineage plausibility audit (pre-specified here, before it is computed; CT2-blinded).**
- **Marker modules:**
  - absorptive: KRT20, FABP1, ALPI, CA1, CA2, SLC26A3, CEACAM7, AQP8;
  - secretory: MUC2, TFF3, SPINK4, CLCA1, FCGBP, ZG16;
  - stem: LGR5, ASCL2, SMOC2, OLFM4, RGMB;
  - cycling: MKI67, TOP2A, CENPF, UBE2C.
- **Module score:** within each study, the pseudobulk module value of a predicted class is the mean over module genes of log2(1 + pseudobulk CP10k). Pseudobulk = sum of the class's counts / sum of its library sizes × 10⁴.
- **Comparator classes:**

  | Class | Module | Compared against |
  |---|---|---|
  | Absorptive | absorptive | Stem/TA-like ∪ Cycling Stem/TA |
  | Secretory | secretory | Absorptive ∪ Stem/TA-like |
  | Stem/TA-like | stem | Absorptive |
  | Cycling Stem/TA | cycling | Stem/TA-like |

- **Pass rule:** for each study × class with ≥ 50 cells in both the class and its comparator, the module difference must be ≥ 1 (≥ 2-fold).
  - The rule is evaluated on all v0.3a-assigned cells, AND separately on the cells the old OOD rule rejected. Both must pass, or the latter must be not evaluable (< 50 cells).
  - A failing study × class is labelled "lineage transfer unverified". That class from that study is excluded from every lineage-specific contrast; for the absorptive class, the study contributes no reference. Lineage-independent continuous analyses are unaffected.
- **Classifier-feature overlap:** markers that are among a fold model's HVGs are reported. Because of this overlap the audit is a plausibility check, not independent validation.
- **Original published annotation:** the Atlas obs carries only the sample-type label "Cancer cell" for tumour epithelium (A3b report), so it is not usable here. This is recorded as such.
- **OOD drivers:** within-sample Spearman of the OOD percentile with log UMI and log genes, plus the median OOD by study and platform.

**Re-run after amendment.**
- G1 selective metrics under v0.3a;
- G5, G6, G8, G9 and G10;
- the lineage-conditioned summaries;
- an old→new label transition table;
- the decision branch re-applied;
- any contrast failing eligibility goes on HOLD.

**Cell universe.** 285,703 cohort L1 epithelial cells − 562 cells = 285,141. The 562 cells are in samples with < 50 epithelial cells, which the reused A3a UCell script skips (A3a frozen minimum). Every such sample is also below the ≥ 100-cell evaluability threshold.

## Freeze record v0.3a (2026-10-11)

- **Decision (GPT, `docs/Fig1c_v03a_freeze_review_20261011.md`):** v0.3a annotation APPROVED and FROZEN, including the lineage audit verdict. Stage 1 annotation decisions are closed: lineage audit, OOD handling and p75 strata will not be revisited after CT2 is joined, whatever the CT2 results.
- **Stem/TA-like:** the pre-specified failure is accepted with no threshold rescue. All Stem/TA-like cells keep their predicted label plus the flag "lineage-transfer-unverified". They are excluded from verified-lineage contrasts and retained in programme-defined contrasts and continuous models. The within-stem contrast is renamed "Cycling Stem/TA-restricted pro-versus-rev contrast", a planned sensitivity outside the Holm family. Any analysis including Stem/TA-like cells is post hoc.
- **Wording branch:** "distinct transcriptional configurations, possibly with overlapping activation". A hybrid continuum is not claimed. The pro vs rev contrast is described as "programme-defined strata", not independent of lineage composition.
- **Stage 3 = CONDITIONAL GO after M1–M5:**
  - **M1:** G5 patient accounting at three levels: reference available; reference plus stratum thresholds; final meta-analysis eligibility. The current tables give pro vs ref 120 patients with an eligible sample, 108 in qualifying studies (≥5 patients per study). For rev vs ref the figures are 117 and 106.
  - **M2:** secondary continuous model.
    - Within each sample, a partial Spearman correlation of CT2 with proCSC and, separately, with revCSC.
    - Each model adjusts for the other programme, log UMI, log genes, mito fraction, S/G2M, and the verified Axis-L lineage categories.
    - Unverified, unresolved and unaudited (transitional or rare) cells enter as separate annotation-status categories.
    - Terms with no variation in a sample are dropped. If the design matrix is singular, the sample is marked conditional-model ineligible.
    - Aggregation: Fisher z, then sample → patient → study, then REML+HK.
    - Sensitivity: an all-epithelium model without Axis L.
  - **M3:** OOD-pass-only sensitivity, using the same frozen pipeline restricted to cells that pass the v0.3 OOD rule. It is descriptive if G5 fails.
  - **M4:** all four contrasts are run on CT2 final, CT2 raw, ds1–5 (averaged within patient) and adjusted CT2. The Holm family is pro−ref, rev−ref and pro−rev. ds missingness is reported.
  - **M5:** join integrity.
    - Unique 1:1 cell_id match between CT2 and the v0.3a labels.
    - Discordant reference cells belong to the reference only, never to pro/rev strata.
    - Status categories are kept separate.
    - All label versions and hashes are archived without overwriting.

## Stage 3 analysis specification lock (2026-10-11; written before any CT2 file is opened)

Implements GPT M1–M5 and contract §6. All inputs come from the frozen v0.3a Stage 1 (`stage1_v03a/phase1/*.cell_labels.tsv.gz` and `*.sample_stats.tsv`), the A3a cell covariates, and the Fig. 1b CT2 outputs (`fig1b_cytotrace2_20261009/full/scores` and `full/scores_ds`). Nothing is re-scored.

**CT2 variables.**
- final = `whole_score`.
- raw = `intrinsic_score`.
- ds r = `whole_score` from `scores_ds/<tag>.ds<r>.scores.tsv.gz`, r = 1–5.

**Groups (p75, v0.3a, per sample; taken from Stage 1 and not recomputed).**
- pro = `stratum75 == pro_dominant`; rev = `rev_dominant`; ref = `reference`. ref includes discordant absorptive cells, which are never in pro/rev.
- Cycling-restricted: pro and rev groups limited to `lineage == Cycling Stem/TA`.
- BH family, other classes vs ref: class = `lineage == c` for c in {Cycling Stem/TA, Secretory differentiated-like, Transitional stem/secretory, Transitional secretory/absorptive, Rare lineages}. Transitional and Rare are flagged "not module-audited". Cells of class c that fall in the ref group cannot occur, because ref is Absorptive only.

**Sample eligibility.**
- Contrasts use exactly the frozen G5 rule: there is no extra ≥ 100-cell sample filter, so that the counts match the approved G5 funnel. The ≥ 100-cell rule (contract §4) applies to the M2 correlations only. (Corrected before CT2 contact; an earlier draft of this lock had applied ≥ 100 to the contrasts.)
- Group thresholds as in G5: pro/rev/class ≥ 30 and ref ≥ 50.
- A study enters a contrast with ≥ 5 eligible patients; pooling needs ≥ 3 studies, otherwise the contrast is descriptive.
- Eligibility is fixed from Stage 1 counts and is identical across CT2 variables.

**Estimators.**
- **Unadjusted:**
  - Sample: median(CT2 | group A) − median(CT2 | group B).
  - Patient: median over its eligible samples.
  - Study: mean and SE = SD/√n of patient values.
  - REML+HK (`fig1b_stats.reml_hk`): 95% CI, PI (k − 2 df), I².
  - Holm over {pro−ref, rev−ref, pro−rev} for CT2 final unadjusted; BH over the five class−ref contrasts. Cycling-restricted is a planned sensitivity outside both families.
- **CT2 raw:** same as unadjusted.
- **Depth-matched:**
  - For each r, compute the same unadjusted sample difference on main-defined groups, using cells present in ds r.
  - Patient value per r = median over samples. Patient estimate = mean over the available r.
  - Pool the patient estimates. Also report each r pooled separately (SD and range).
  - Missingness per contrast: fraction of eligible-group cells absent from ds r, and samples lacking ds r. A sample with no ds replicate is missing for ds and is reported, not imputed. A group dropping below its threshold in ds r is reported but kept, because eligibility is fixed.
- **Adjusted:**
  - Within each sample, OLS of untransformed CT2 final on indicator(A) + log10 UMI + log10 genes + mito + S + G2M, fitted on A ∪ B cells only. Requires ≥ 70 cells; constant covariates are dropped.
  - Coefficient = conditional mean difference; patient = median; pooled as above.
  - Reduced model (log UMI + log genes) is a separate sensitivity.
  - No % attenuation is computed.

**M2 secondary continuous model.**
- Population: all samples with ≥ 100 cells, no reference requirement.
- Per sample, partial Spearman between CT2 final and proCSC, and separately revCSC, using rank residuals (A3a `corr_pair` method). Covariates:
  - the other programme;
  - log UMI, log genes, mito, S, G2M;
  - dummies for every v0.3a lineage/status category present (verified classes; lineage-transfer-unverified; lineage-unresolved; Transitional/Rare flagged unaudited), with one reference level dropped and constant dummies dropped.
- If the design matrix is rank deficient after dropping, the sample is "conditional-model ineligible" (counted).
- Sensitivity: an all-epithelium model without lineage dummies. The unadjusted Spearman is also reported.
- Aggregation: Fisher z, patient = mean z (A3a convention for correlations), study mean/SE, REML+HK; ≥ 5 patients per study and ≥ 3 studies.

**M3 OOD-pass-only sensitivity.**
- Restrict each group to `ood_pass` cells (v0.3 rule ood_pct ≤ 99) and recompute eligibility with the same thresholds. Report patients and studies per contrast and composition changes.
- Run the unadjusted CT2 final contrast for comparison with full v0.3a. If G5 fails, it is descriptive only.

**M5 join integrity (checked before any statistic is written; failure stops the run).**
- cell_id unique in the labels and in CT2 main.
- Every labelled cell has a CT2 final and raw value (report n missing).
- ref ∩ (pro ∪ rev) = ∅.
- Label status categories kept separate.
- SHA256 of the v0.3a labels recorded and compared with the Stage 1 hash.

## Stage 4 specification (2026-10-11; implements contract §6 sensitivities and GPT Stage 3 review `docs/Fig1c_stage3_review_20261011.md`)

Written after the Stage 3 results were seen. Every item is either already listed in contract §6 or was required by the GPT review. No item was added or dropped because of its expected direction. The Stage 3 estimator, thresholds and families are unchanged unless stated otherwise. All items are sensitivity analyses; Holm still covers only the three primary contrasts.

**Contrasts in every item:** pro−ref, rev−ref, pro−rev and Cycling-restricted pro−rev. The CT2 measure is final, unadjusted, unless stated otherwise.

| Item | Definition |
|---|---|
| MSI/MSS | Patient `msi_status` from the cohort metadata. Pooled separately in MSI-H and MSS (unknown is reported only). The interaction is described, not tested, unless at least 3 studies contribute ≥ 5 patients to both strata |
| CNV-positive subset | Cells with celltype_L2 = "Malignant epithelial" (the Atlas high-confidence malignant call). Groups keep their p75 membership and are restricted to these cells; eligibility is recomputed with the same thresholds. A feasibility table is always written |
| Pelka excluded and LOSO | Study-level re-pooling with each study left out: effect, CI and direction per left-out study |
| p70 / p80 | Stage 1 `stratum70` / `stratum80`; eligibility recomputed |
| Mechanism-blinded | `proCSC_mb` / `revCSC_mb`, with p75 strata recomputed within sample exactly as in Stage 1 (percentile over all sample cells; Absorptive lineage = reference). Reported: membership transition matrix, Jaccard per stratum, eligibility, the four contrasts |
| Reference: strict | ref = Absorptive & neither-high (the discordant cells leave both groups) |
| Reference: broad | ref = Absorptive ∪ Secretory differentiated-like; Secretory cells are removed from pro/rev to keep the groups mutually exclusive |
| Reference: common subset | Both reference contrasts are also reported on patients eligible under all three reference definitions |
| Reduced vs full adjusted; unadjusted vs full adjusted | Compared on the common set of samples where both are estimable |
| CCAT | A3a gate passed (A3a §10–11). The four contrasts and M2 (lineage-adjusted partial) are rerun with CCAT in place of CT2 final |
| Depth audit D1 | Cells absent from ds output vs retained ones, per group (pro, rev, ref): sample-level median difference (dropped − retained) in log UMI, log genes, mito, CT2 final, proCSC, revCSC; pooled descriptively |
| Depth audit D2 | Intersection = cells present in all of ds1–5. A = Stage 3 final; A' = final on the D2 patient population; B = final on intersection cells; C = mean over r of ds on intersection cells; D = B − C |
| Depth audit D3 | Eligibility recomputed on intersection cells; patients and studies lost; loss by patient revCSC tertile |
| Depth audit D4 | Interpreted by the rule in the review |
| Sample universe | Every Stage 1 sample absent from Stage 3 is listed with its cell count and reason |
| Meta diagnostics | The by-study table (forest input), tau², PI and LOSO for every primary contrast |

## Claim freeze (2026-10-11)

- The Stage 4 results were approved and Branch B is final, as recorded in `docs/Fig1c_stage4_final_review_20261011.md`. That file also holds the frozen core claim, legend sentence, wording constraints and panel map.
- The analysis line is closed. No new proxies, strata, references or annotation changes will be made.
- Every number in the figure and legend must trace to `tables/stage3/` or `tables/stage4/`.
