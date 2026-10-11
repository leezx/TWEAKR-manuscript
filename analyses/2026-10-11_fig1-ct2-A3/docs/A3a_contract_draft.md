# A3a contract (DRAFT v0.1, for review): developmental programmes × potency proxies in CRC epithelium

- **Date:** 2026-10-11.
- **Status:** draft, not frozen. **No computation has been run.** Freeze only after review; any later change is a dated amendment.
- **Parent:** Fig. 1b CytoTRACE2 (contract A2.1, results approved 2026-10-10). Consultation: `../2026-10-09_fig1b-cytotrace2/docs/A3_next_questions_consultation_20261010.md`.
- **Working Result:** `manuscript/Figures/Figure1/Figure1.CT2-CSCprograms.result.md`.

## 0. Question and stated prior

**Question.** Within CRC tumour-derived epithelial cells, are developmental programmes (proCSC, revCSC, Lgr5CSC, oncofetal, YAP) associated with higher predicted developmental potential, and does the answer depend on the potency proxy?

**Stated prior (recorded before any A3a computation).**
- The PI expects developmental/oncofetal programmes to mark more plastic cells. The PI also expects CytoTRACE2 (CT2) to under-detect this because of known defects:
  - CT2 is depth- and complexity-sensitive: depth matching cut the Fig. 1b compartment contrasts by 43–55%;
  - the final score depends on the other cells in the sample (smoothing);
  - the training reference may not represent oncofetal/regenerative states.
- Prior single-cohort evidence (DS-010, GSE254249; 21 patients, 28,645 author-annotated Cancer cells; mean of patient-level Spearman ρ):

  | Programme | Proxy | Unadjusted ρ | Adjusted ρ |
  |---|---|---|---|
  | proCSC | CT2 | +0.59 | +0.32 |
  | proCSC | CCAT | +0.69 | +0.37 |
  | revCSC | CT2 | +0.18 | −0.05 |
  | revCSC | CCAT | +0.47 | −0.06 |

  Adjusted ρ is a rank-residual adjustment for depth, detected genes, mito and ribosomal fractions, cycling and stress.
- The direction is therefore **not** unknown. A3a is a replication and extension across 13 independent studies, not a hypothesis-free discovery. GSE254249 is not part of the 13-study cohort.

**Consequence for design.**
- Every proxy and every adjustment is fixed below, before any A3a output exists.
- No proxy, adjustment or signature may be added, dropped or re-weighted after results are seen.
- A null or negative result for a programme is reported as such. It is not explained away by CT2 defects unless the pre-specified complementary proxies (§4) also disagree with CT2.

## 1. Cohort and cells

- **Patients and samples:** cohort v1 (13 studies, 222 patients, 361 treatment-naive primary tumour samples), unchanged.
- **Primary cell set:** L1 Epithelial cells (285,703).
  - Tumour-derived epithelium, not proven malignant.
  - These are cells that already carry CT2 scores from the Fig. 1b main run (no new CT2).
- **Sensitivity cell sets** (fixed):
  1. F1-clean epithelium (L1 epithelial cells without an F1 cross-lineage marker conflict);
  2. the high-confidence malignant subset (`annotation_v1`; 76 patients / 8 studies, MSS-enriched);
  3. non-cycling epithelium (CT2 run unchanged; cells with G2M/S-high calls dropped).
- **Eligibility:** a sample enters when it has ≥100 primary-set epithelial cells. A patient enters with ≥1 eligible sample. A study is pooled when it has ≥5 eligible patients. A pooled estimate needs ≥3 eligible studies; otherwise it is reported per study as exploratory.

## 2. Programme scores (frozen gene sets; scored independently of CT2)

| Role | Set | Genes | Source |
|---|---|---:|---|
| P1 core | proCSC | 33 | `genesets/genesets/CSC_subtype_signatures.csv` (human column) |
| P1 core | revCSC | 42 | same file; also `revCSC.human.gmt` |
| P1 core | Lgr5CSC (canonical stem) | 30 | same file |
| P1 core | Extended CIOC v2.0 (oncofetal, epithelial-resolved) | 222 | oncofetal_signature `core_oncofetal` (frozen; membership restricted, see §8) |
| P1 core | YAP core | per GMT | `genesets/YAP_targets_gmt/YAP_core_heatmap.human.gmt` |
| Secondary | ECOS-38 | 38 | oncofetal_signature (frozen) |
| Secondary | YAP fetal/oncofetal effectors | per GMT | `YAP_fetal_oncofetal_effectors.human.gmt` (YAP-overlapping regeneration set, not pure YAP activity) |
| Secondary | Placenta trophoblast (filtered) | 41 | `placenta_trophoblast.filtered.gmt` (Fig. 4 link) |
| P2 | TNFRSF12A | 1 | per-cell detection (UMI > 0) and log-normalised expression |

Scoring rules:
- **Method:** UCell, rank-based, computed per sample on raw counts of the primary epithelial cells.
- **Genes:** only genes present in the Atlas GENCODE v44 space are kept. Coverage per set is reported. A set with <70% coverage is reported but not interpreted.
- **Overlap reporting:** the pairwise overlap between sets is reported, and so is the overlap of each set with the CT2 model feature space.
- **Provenance:**
  - The CSC_subtype_signatures source is to be registered in `reference.md` before freeze. The file name suggests mouse organoid CSC markers (Qin) mapped to human symbols.
  - Signature membership is not changed using any CT2/CCAT output.

## 3. Potency proxies (endpoints)

| Proxy | Role | Status |
|---|---|---|
| CT2 final score (whole-sample run, seed 14) | **primary** | exists (Fig. 1b `full/scores`) |
| CT2 raw model score (cell-intrinsic, pre-smoothing) | required sensitivity | exists |
| CT2 depth-matched (5 seeds, mean of per-sample correlations) | required sensitivity | exists (`full/scores_ds`); programme scores recomputed on the same downsampled counts. The exported ds counts hold CT2 model features only, so if set coverage there is <70%, the programme scores use original counts of the retained cells (recorded) |
| CCAT (SCENT 1.0.3, net13Jun12), signalling entropy | **co-primary complementary proxy** | new; runs only if its DS-010 technical pilot is accepted in the parallel CSCPOT workstream |
| Expression Shannon / detected genes | technical control only, never a potency readout | computed |

**Discordance rule (fixed).**
- Report CT2 and CCAT side by side.
- Concordance requires the same sign and both pooled CIs to exclude 0.
- If CT2 and CCAT disagree, the conclusion is "proxy-dependent". Neither proxy is preferred post hoc.

## 4. Statistics

**Primary metric.** Within each eligible sample, the **partial Spearman** correlation between programme score and proxy, adjusting for log UMI, log detected genes, mito %, and S and G2M scores (rank residuals). Unadjusted Spearman is reported alongside.
- *Rationale:* Fig. 1b showed strong depth sensitivity; the DS-010 prior shows that the revCSC association depends on this adjustment.

**Aggregation.**
1. sample ρ → Fisher z;
2. mean within patient;
3. patient mean per study (t-CI);
4. random-effects pooling across studies (REML + Hartung–Knapp, 95% PI with k−2 df, I²), as in A2.1;
5. LOSO over studies.

**Multiple testing.**
- Primary family: 5 P1 core sets × primary proxy (CT2 partial ρ) = 5 tests, BH-FDR.
- CCAT forms its own 5-test family.
- Secondary sets are descriptive (CIs, no FDR claim).

**Effect modifiers** (pre-specified, descriptive):
- MSI/MMR status, from the Atlas `microsatellite_status` / patient table; unknown is kept separate;
- study platform.

**Programme contrasts** (answers "distinct dimensions?"):
- For each patient, the difference in partial ρ: Extended CIOC − proCSC, revCSC − proCSC, and YAP core − proCSC.
- These differences are pooled the same way.

## 5. Interpretation rules (written before results)

| Outcome for a programme | Allowed statement |
|---|---|
| Pooled partial ρ > 0, CI excludes 0, same sign in ≥2/3 eligible studies, preserved in raw-score and depth-matched sensitivities | "associated with higher predicted developmental potential" |
| As above, but lost after adjustment or after depth matching | "association explained by transcriptional complexity/depth" |
| CI includes 0 | "no detectable association with predicted developmental potential" |
| Pooled partial ρ < 0 with CI excluding 0 | "associated with lower predicted developmental potential" |
| CT2 and CCAT disagree | "proxy-dependent"; no direction claimed |

Language rules:
- Never use "plasticity" as a measured quantity. Use "predicted developmental potential" (CT2) or "signalling entropy" (CCAT).
- A positive association does not show that the programme causes potency, or that cells transition between states.

## 6. P2 and P3 (secondary modules; same freeze)

**P2 (TWEAKR).** Per-sample partial ρ of TNFRSF12A with the proxies and with each P1 set, aggregated as in §4.
- Gate: TNFRSF12A must be detected in ≥5% of epithelial cells in ≥3 studies, otherwise P2 stops.

**P3 (macrophage TWEAK).** Sample level only.
- Predictor: macrophage TNFSF12 pseudobulk (CPM) or detection fraction, from L2 Macrophage cells with ≥30 cells per sample.
- Outcomes: the sample medians of epithelial programme scores and of the proxies.
- Model: within-study Spearman, pooled across studies; adjust for macrophage fraction and depth.
- Gate: TNFSF12 detected in ≥5% of macrophages in ≥3 studies.
- Statements are restricted to co-occurrence, never interaction or proximity.

## 7. Stopping rules

Stop a module, report it as exploratory, and do not extend it when any of these holds:
- fewer than 3 eligible studies;
- signature coverage below 70%;
- for CCAT, the parallel pilot fails or network coverage is below 5,000 genes;
- P2/P3 detection gates fail.

Data are never re-selected to rescue a module.

## 8. Data handling

- **Location:** per-cell scores and patient-level correlations stay on Argos under `analysis/fig1_ct2_A3_20261011/`. Only study-level and pooled aggregates go to the repo, and the repo is public.
- **Restricted gene sets:** Extended CIOC/ECOS-38 membership is restricted. Scripts read it from a private Argos path; gene lists are never committed.
- **Software:** UCell and CT2 1.1.0 are already in the r4p3 environment; SCENT 1.0.3 comes from the CSCPOT installation. Versions are recorded.

## 9. Questions for review

1. Is the partial ρ (adjusted for depth, genes, mito and cycle) the right primary metric, given that it may remove true biology linked to complexity? Or should unadjusted and adjusted be co-primary?
2. Should CCAT be co-primary, given that it is still at pilot stage in DS-010? Should a non-potency readout of state plasticity be added? Example: per-cell programme hybridity, i.e. co-high scores across ≥2 programmes, or entropy over the P1 programme scores.
3. Are the P1 core sets right? In particular, should the oncofetal axis be Extended CIOC (222) or the stricter ECOS-38?
4. Is a ≥100-cell sample threshold reasonable (it removes small samples), or is 50 enough?
