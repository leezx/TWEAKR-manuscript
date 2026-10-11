# A3a contract (v0.2, FROZEN 2026-10-11): developmental programmes × potency proxies in CRC epithelium

- **Date:** 2026-10-11.
- **Status: FROZEN** on 2026-10-11. The reviewer's final check of the text at commit `9104fc8` returned **"FREEZE / GO — A3a v0.2 APPROVED"**, authorising P1, P2 and P3; the CCAT branch remains subject to its technical gate. A3b scoring is not authorised.
- **Changes after freeze:** dated amendments only. Endpoints, covariates and signatures are never adjusted to the observed direction of an association.
- **Content:** this file is the approved text at `9104fc8`, renamed from `A3a_contract_draft.md`. Only this header was changed at freeze.
- **No computation has been run.** Any change after freeze is a dated amendment.
- **Parent:** Fig. 1b CytoTRACE2 (contract A2.1, results approved 2026-10-10).
- **Review record:**
  - consultation: `../2026-10-09_fig1b-cytotrace2/docs/A3_next_questions_consultation_20261010.md`;
  - v0.1 review: `A3_review_20261011.md`.
- **Working Result:** `manuscript/Figures/Figure1/Figure1.CT2-CSCprograms.result.md`.

## Changes from v0.1 (all from the review)

| # | v0.1 | v0.2 |
|---|---|---|
| 1 | Partial ρ primary | **Unadjusted ρ is the single primary estimand**; adjusted partial ρ is a mandatory robustness estimand (not a second significance gate) |
| 2 | CCAT co-primary, called "signalling entropy" | CCAT is a **secondary**, independent-algorithm proxy with its own BH family. Description corrected: SCENT-CCAT is the correlation between expression and PPI-network connectivity. Signalling entropy rate is SCENT-SR, which is not used |
| 3 | — | One descriptive **proCSC–revCSC co-activation** readout added (Extended Data). It is not a plasticity metric and not in any testing family |
| 4 | Gene counts as mouse rows (33/42/30) | **Unique human genes: proCSC 27, revCSC 32, Lgr5CSC 27.** Same file and version; `revCSC.human.gmt` (32) is identical to the CSV revCSC human column. SHA256s recorded |
| 5 | ≥100 cells only | ≥100 primary; ≥50 as a fixed coverage sensitivity; samples with near-zero variance flagged non-estimable |
| 6 | Depth-matched programme scores ambiguous | Two named cases, kept separate in outputs (§3) |
| 7 | Programme contrasts loosely defined | Paired on the Fisher-z scale within patient, then meta-analysed; **descriptive** (CI only) |
| 8 | P2/P3 several predictors | One fixed predictor and one fixed outcome per module; the rest descriptive |

## 0. Question, estimand and stated prior

**Question.** Are oncofetal and canonical CSC programmes associated with CT2-predicted developmental potential in CRC epithelium? To what extent are these associations sensitive to transcriptomic complexity?

**Stated prior** (recorded before any A3a computation).
- The PI expects developmental/oncofetal programmes to mark more plastic cells, and expects CT2 to under-detect this. The reasons:
  - CT2 is depth- and complexity-sensitive (Fig. 1b effects shrank 43–55% with depth matching);
  - the final score depends on sample composition through smoothing;
  - the training reference may not cover oncofetal/regenerative states.
- DS-010 prior (GSE254249, 21 patients; mean of patient-level Spearman ρ; adjusted = rank residuals on depth, genes, mito, ribosomal, cycle and stress):

  | Programme | Proxy | Unadjusted ρ | Adjusted ρ |
  |---|---|---:|---:|
  | proCSC | CT2 | +0.59 | +0.32 |
  | proCSC | CCAT | +0.69 | +0.37 |
  | revCSC | CT2 | +0.18 | −0.05 |
  | revCSC | CCAT | +0.47 | −0.06 |

- A3a therefore replicates in 13 independent studies; it is not a hypothesis-free discovery.
- Its adjustment set (§4) is **not identical** to DS-010's: DS-010 also adjusted for ribosomal fraction and stress. The two adjusted ρ are different estimands and are not compared as if equal.

**Rule.** No proxy, covariate, signature or threshold may be added, dropped or changed after results are seen.
- A null or negative result is reported as such.
- It may be attributed to CT2 limitations only when the complementary proxy (CCAT) disagrees with CT2.

## 1. Cohort and cells

- **Patients and samples:** cohort v1 (13 studies, 222 patients, 361 treatment-naive primary tumour samples), unchanged.
- **Primary cell set:** L1 Epithelial cells (285,703) with existing CT2 scores from the Fig. 1b main run. No new CT2.
- **Wording:** these cells are "tumour-derived epithelium", never "malignant". The Atlas epithelial label follows sample origin; see `A3b_metadata_gate_report.md` §2.
- **Sensitivity cell sets** (fixed):
  1. F1-clean epithelium;
  2. the high-confidence malignant subset (`annotation_v1`; 76 patients / 8 studies, MSS-enriched);
  3. non-cycling epithelium, i.e. cells in G1 by the Atlas `phase` call.
- **Eligibility:**
  - A sample enters with ≥100 primary-set cells. ≥50 is a fixed coverage sensitivity analysis.
  - A sample × programme whose programme score or proxy has an IQR of 0 is flagged non-estimable and is not computed.
  - A patient enters with ≥1 eligible sample.
  - A study is pooled with ≥5 eligible patients.
  - A pooled estimate needs ≥3 eligible studies; otherwise per-study results are reported as exploratory.

## 2. Programme scores (frozen; independent of CT2/CCAT)

| Role | Set | Unique human genes | File (SHA256, first 12) |
|---|---|---:|---|
| P1 core | proCSC | 27 | `genesets/genesets/CSC_subtype_signatures.csv` human column (`b8754d69ae64`) |
| P1 core | revCSC | 32 | same file; identical to `genesets/revCSC.human.gmt` (`a482536728b8`) |
| P1 core | Lgr5CSC | 27 | same file |
| P1 core | Extended CIOC v2.0 | 222 | oncofetal_signature `core_oncofetal/results/Extended_CIOC.gmt` (`d7a5bb22411e`; restricted, git-ignored) |
| P1 core | YAP core | 12 | `genesets/YAP_targets_gmt/YAP_core_heatmap.human.gmt` (`0d54858d6feb`) |
| Validation of the oncofetal set | ECOS-38 | 38 | `core_oncofetal/results/ECOS_38.gmt` (`8b4b5f5c4fbe`; restricted) |
| Secondary (descriptive) | YAP fetal/oncofetal effectors | 34 | `YAP_fetal_oncofetal_effectors.human.gmt` (`b2a05033980b`) |
| Secondary (descriptive) | Placenta trophoblast (filtered) | 41 | `genesets/placenta_trophoblast.filtered.gmt` (`5835506a1388`) |

**Overlap between P1 sets** (unique human genes):

| Pair | Shared genes |
|---|---:|
| proCSC ∩ revCSC | 0 |
| proCSC ∩ Lgr5CSC | 1 |
| proCSC ∩ YAP core | 1 |
| revCSC ∩ YAP core | 4 |
| Extended CIOC ∩ revCSC | 3 |
| Extended CIOC ∩ YAP core | 2 |
| Extended CIOC ∩ proCSC | 0 |
| Extended CIOC ∩ Lgr5CSC | 0 |

The revCSC–YAP and revCSC–Extended CIOC overlaps are reported. No gene is removed.

**Provenance.**
- CSC_subtype_signatures comes from mouse CSC clusters (Lgr5CSC / proCSC / revCSC) mapped to human symbols. Concept source: REF-012 (Qin et al., Cell 2023). Derivation of this exact file from that paper is not verified.
- Extended CIOC / ECOS-38 are the frozen oncofetal_signature objects. Extended CIOC is defined as: genome-wide H/M/C gates ∩ epithelial detectability (≥5% of tumour-derived epithelial cells in ≥1 atlas) ∩ positive CIOC coherence in Khaliq and Che.
- **Independence caveat:** Khaliq is one of the 13 A3a studies. Extended CIOC was selected partly on Khaliq tumour-derived epithelium (detectability and coherence). A3a therefore also reports P1 with Khaliq excluded for Extended CIOC and ECOS-38.

**Scoring.**
- UCell per sample on the raw counts of primary-set cells, in the Atlas GENCODE v44 space.
- Coverage per set is reported. A set with <70% coverage is reported, not interpreted.

## 3. Potency proxies

| Proxy | Role |
|---|---|
| CT2 final score (whole-sample run, seed 14) | **primary** |
| CT2 raw model score | required sensitivity |
| CT2 depth perturbation (5 seeds; per-sample ρ averaged over seeds) | required sensitivity; two named cases, below |
| SCENT-CCAT 1.0.3 (net13Jun12) | secondary, independent algorithm; runs only if the DS-010 technical pilot is accepted. If it is not, recorded as technically non-evaluable, with no substitute algorithm |
| Detected genes; expression Shannon | technical diagnostics only |

**Depth perturbation cases** (output labels):
- (a) **`ds_both`:** programme scores are recomputed on the same downsampled counts, used when every P1 set has ≥70% coverage in the exported CT2 feature counts.
- (b) **`ds_ct2_fixed_programme`:** CT2 comes from downsampled counts and the programme scores are the original ones on the retained cells. This is described as "CT2-depth perturbation with fixed original programme scores", never as both measures being depth-matched.

## 4. Statistics

**Primary estimand.** Within each eligible sample, the unadjusted Spearman ρ between a programme score and CT2 final.

**Mandatory robustness estimand.**
- Within-sample partial Spearman ρ, computed on rank residuals.
- Covariates: log UMI, log detected genes, mito %, S score and G2M score.
- This set is fixed; it is not extended to ribosomal or stress terms.

**Aggregation** (both estimands):
1. sample ρ → Fisher z;
2. mean within patient (samples weighted equally);
3. per-study mean with t-CI;
4. random-effects pooling (REML + Hartung–Knapp; 95% PI with k−2 df; I²);
5. LOSO.

Results are back-transformed to ρ.

**Testing families** (BH-FDR within each):

| Family | Tests |
|---|---|
| Primary | 5 P1 core sets × CT2 final, unadjusted ρ |
| Secondary | 5 P1 core sets × CCAT, unadjusted ρ (only if CCAT runs) |

Everything else is estimate + CI only: adjusted ρ, raw score, depth perturbation, sensitivity cell sets, secondary sets, ECOS-38 and the Khaliq-excluded runs.

**Programme contrasts** (descriptive):
- Per patient, take Fisher z(revCSC) − z(proCSC), z(Extended CIOC) − z(proCSC) and z(YAP core) − z(proCSC).
- Pool as above. Report CI only, with no test.

**Effect modifiers** (descriptive):
- MSI/MMR status (unknown kept separate);
- platform.

**Co-activation readout** (Extended Data, descriptive):
- Within each sample, proCSC-high and revCSC-high are scores at or above that sample's 75th percentile. The threshold is fixed and used in every study.
- Report per sample:
  - the share of co-high cells, compared with the 6.25% expected under independence;
  - median CT2 in each of the four groups: co-high, proCSC-only, revCSC-only and neither.
- Pool across studies descriptively.
- This is relative co-expression. It is not an absolute state, not comparable in absolute terms across patients, and not evidence of state transition.

## 5. Interpretation rules (written before results)

| Outcome | Allowed statement |
|---|---|
| Pooled unadjusted ρ > 0, CI excludes 0, same sign in ≥2/3 eligible studies, **and** adjusted ρ, raw score and depth perturbation keep the sign with CI excluding 0 | "robustly associated with higher predicted developmental potential" |
| Unadjusted ρ > 0 with CI excluding 0, but adjusted ρ or depth perturbation CI includes 0 | "positively associated; the association was substantially attenuated after adjustment for transcriptomic complexity and cell-cycle covariates" (not "explained by depth") |
| Unadjusted CI includes 0 | "no detectable association with predicted developmental potential" |
| Unadjusted ρ < 0, CI excludes 0 | "associated with lower predicted developmental potential" |
| CT2 and CCAT pooled signs differ, or one CI excludes 0 and the other excludes 0 in the opposite direction | "proxy-dependent"; no direction claimed |

Language rules:
- Never say "plasticity" as a measured quantity. Say "predicted developmental potential" (CT2), "CCAT-estimated differentiation potency" (CCAT) and "co-activation" (the co-activation readout).
- An association never implies causation or cell-state transition.

## 6. P2 and P3 (same freeze)

**P2 (TWEAKR).**
- Predictor: TNFRSF12A log-normalised expression (log1p CPM).
- Outcome: CT2 final.
- Estimand and aggregation as in §4.
- Descriptive only: TNFRSF12A detection, and TNFRSF12A × each P1 set.
- Gate: TNFRSF12A detected in ≥5% of epithelial cells in ≥3 studies; otherwise P2 stops.

**P3 (macrophage TWEAK)**, at sample level.
- Predictor: macrophage TNFSF12 pseudobulk log1p CPM, from L2 Macrophage cells, requiring ≥30 cells per sample.
- Outcome: the sample median of the epithelial Extended CIOC UCell score.
- Analysis: within-study Spearman, pooled by REML+HK.
- Descriptive only: epithelial CT2, proCSC and revCSC, and adjustment for macrophage fraction and depth.
- Gate: TNFSF12 detected in ≥5% of macrophages in ≥3 studies.
- Statements are limited to co-occurrence.

## 7. Stopping rules

A module stops and is reported as exploratory, with no data re-selection, when any of the following holds:
- fewer than 3 eligible studies;
- signature coverage below 70%;
- the CCAT pilot fails, or its network coverage is below 5,000 genes (CCAT branch only);
- the P2/P3 detection gate fails.

## 8. Data handling

- Per-cell scores and patient-level correlations stay on Argos under `analysis/fig1_ct2_A3_20261011/`. Only study-level and pooled aggregates go to the public repo.
- Extended CIOC/ECOS-38 membership is restricted. It is copied to a private Argos path (mode 600) and never committed; only SHA256s are public.
- Software:
  - UCell and CT2 1.1.0 (r4p3 environment);
  - SCENT 1.0.3 (CSCPOT installation).
  - Versions are recorded per run.

## 9. Pre-freeze checklist

- [x] Gene-set versions, unique human counts and SHA256s verified (2026-10-11).
- [x] Source registered as REF-012: Qin et al., Cell 2023, 186:5554 (doi 10.1016/j.cell.2023.11.004) defines proCSC/revCSC. That this exact gene file derives from the paper's markers is **not verified** (file name points to a Qin mouse organoid re-analysis, Jan 2025); this is stated as a limitation.
- [ ] Final check of v0.2 by the reviewer → freeze as `A3a_contract.md` with a FROZEN note.
