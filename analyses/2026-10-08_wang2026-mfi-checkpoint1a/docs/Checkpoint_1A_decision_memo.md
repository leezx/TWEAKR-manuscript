# Checkpoint 1A decision memo — TNFSF12 / TNFRSF12A expression feasibility (DS-013)

**Decision (human review, 2026-10-08): EXPLORATORY / PASS WITH LIMITATIONS — complete.**

**DS-013: CLOSED — exploratory result; spatial hypothesis not evaluable with accessible public data.**
A no-go decision is a complete deliverable. Stereo-seq is not pursued, the author request is
not sent, and the branch is kept without a PR.

| Checkpoint | Decision | Status |
|---|---|---|
| CP0 — data provenance | PASS | complete |
| CP1A — expression feasibility | EXPLORATORY / PASS WITH LIMITATIONS | complete |
| CP1B — genotype origin verification | NOT PURSUED | author request archived, not sent |
| CP1C — spatial assay feasibility (metadata and gene detection only) | PASS — NOT EVALUABLE | complete |
| CP2 — spatial colocalisation | NOT PURSUED | closed |

## Approved summary statements

- **Primary retained observation:** TNFRSF12A is reproducibly expressed in fetal-derived
  extravillous trophoblast populations at the human maternal–fetal interface. "Fetal-derived"
  rests on the authors' cell-type-level origin classification, not on per-cell genotype
  re-verified here.
- TNFSF12 is sparsely detected across multiple maternal–fetal interface cell populations,
  without consistent macrophage-specific enrichment. The BH q = 0.03 Wilcoxon result is not
  taken as a stable enrichment claim: 13/23 donors, 9 donors with zero macrophage detection,
  median Δ +0.36 percentage points, and sensitivity to depth and gestational composition.
  This does not show that macrophages do not produce TWEAK.
- Secondary: TNFRSF12A may be gestationally regulated. It is higher in T3 despite lower T3
  depth, but gestational regulation, subtype composition and donor/batch effects were not
  separated. No further analysis is planned.
- TNFRSF12A is reproducibly expressed in fetal trophoblast populations, particularly iEVTs, but is not exclusive to trophoblasts.
- The data do not support the claim "maternal macrophage-derived TWEAK establishes a fetal
  immune-tolerant niche". They support a broader working hypothesis: TWEAK–TWEAKR
  signalling may contribute to cellular interactions at the maternal–fetal interface, with
  TNFRSF12A-expressing trophoblasts as potential recipient cells.

## Scope and definitions

- Data: COSMOS `scPlacenta_host.h5ad`, 193,202 nuclei, 23 donors (GW5–39). snRNA-seq captures nuclear transcripts only.
- Origin: `author_cell_type_origin` from Supplementary Table 13a/b, **not** per-nucleus
  genotype. FB and pvSMC are `mixed`; GC and Ery are `ambiguous`.
- Detection = raw UMI > 0 (`pct_expr`).
- `mean_log1p_cp10k` = per-nucleus log1p(UMI / library size × 1e4), averaged over nuclei. It
  is **not** pseudobulk CPM and not log1p(mean CP10k). Pseudobulk CP10k (sum of UMIs / sum of
  library sizes) and the linear per-nucleus mean CP10k are reported in separate columns.
- The public X is log1p(raw counts) without size normalisation. Counts were reconstructed
  from it and checked against `snRNA_raw_counts.h5ad`.

## Results

### TNFSF12 (ligand)

| Metric | Value |
|---|---|
| Atlas-wide detection | 0.94% (1,825 nuclei; 1,845 UMIs) |
| CD14_M / CD16_M detection | 2.49% / 1.54% |
| CD14_M rank (all nuclei / depth-matched) | 8/36 → 4/36 |
| Types at or above CD14_M after depth matching | LEC 3.5%, T 3.2%, DSC1 3.0% |
| Maternal-labelled share of all TNFSF12 UMIs | 76.6% (epithelium 20.5%, CD14_M 9.9%, DSC0/1 ~7% each) |
| Macrophage vs other nuclei, within donor | higher in 13/23 donors; 9/23 donors have zero macrophage detection |

**Statistical detail for q = 0.03** (`tables/donor_paired_contrasts.csv`):
- Test: two-sided Wilcoxon signed-rank on donor-level values, macrophages (CD14_M + CD16_M)
  vs all other nuclei of the same donor.
- Metrics: detection fraction (p = 0.0033, BH q = 0.030) and mean_log1p_cp10k (p = 0.0029,
  q = 0.026). BH corrects across the 9 pre-specified contrasts per metric.
- All 23 donors pass the ≥20-nuclei rule, with a minimum of 64 macrophages per donor. Trimester is **not** adjusted.
- Effect size is small: median Δ = +0.36 percentage points.
- Direction is weakly consistent: exact sign test 13/23, p = 0.17. By trimester: T1 6/9, T2 5/9, T3 2/5.
- The Wilcoxon result is therefore driven by the size of the positive differences in about
  half of the donors, not by consistent direction. At ~1–2% detection, donors with fewer than
  ~250 macrophages expect only a few positive nuclei, so zero detection is compatible with
  sampling.

### TNFRSF12A (receptor)

| Metric | Value |
|---|---|
| Atlas-wide detection | 8.4% |
| Fetal- vs maternal-labelled detection | 11.9% vs 3.3%; fetal types hold 76.6% of UMIs (SCT 54.7%) |
| iEVT | 16.3%; detected in 13/13 evaluable donors; donor median 10.6%; depth-matched 15.8% |
| Other trophoblasts | SCT_b 14.7%, pEVT 13.5% (n=170), SCT 12.9%, EVTpro 11.8%; "other EVT" 7.2%; eEVT 1.5% |
| Non-trophoblast expression | GC 20.5% (ambiguous), aEC 16.1% (n=472), FB/pvSMC ~14% (mixed), fEC 12.9%, DSC3 12.7% |
| EVT group vs other nuclei, within donor | higher in 7/17 donors, q = 0.72 (other nuclei include high-expressing SCT) |
| Maternal stroma (DSC+eS) vs other nuclei | q = 0.32; not the dominant receptor compartment |

### Library-size QC (`tables/qc_library_size.csv`, `tables/qc_depth_matched_detection.csv`)

- Median UMIs per nucleus: T1 4,381, T2 3,486, T3 3,302. Donor medians range from 2,123 to 11,405.
- Cell types with the highest TNFSF12 detection also have the deepest libraries (LEC median
  4,966; aEC 4,568; DSC1 4,836; ciliated 5,396 vs CD14_M 3,937). Restricting to nuclei
  within the atlas library-size IQR (3,040–4,528) narrows the gap but does not make
  macrophages the leading source.
- TNFRSF12A is **higher** in T3 despite **lower** T3 depth, so the T3 rise is not a depth
  artefact. Three explanations still need to be separated: (i) a global T3 increase,
  (ii) a change in EVT subtype composition, and (iii) true receptor upregulation within EVT.
  This was not resolved here.

## Rule mapping

| Rule | Met? |
|---|---|
| GO | No |
| Conditional GO | Partially (receptor arm only) |
| **Exploratory** | **Yes — adopted** |
| Hypothesis revision (receptor mainly in maternal stroma) | No |
| NO-GO | No |

## Open questions carried forward

1. What is the main TNFSF12 source? Endothelial (LEC/aEC/vEC) and stromal sources rival or
   exceed macrophages. Endothelial–trophoblast signalling may deserve equal weight.
2. Are TNFRSF12A+ trophoblasts located near ligand-producing cells? Only Stereo-seq can
   answer this. Even then, proximity would show spatial association only, not receptor
   activation, recruitment or tolerance.
3. Cellular origin is not the same as anatomical compartment: iEVT are fetal cells located in maternal decidua.

## Evidence boundary for the TWEAKR manuscript

| Question | Evidence from Wang 2026 | Value |
|---|---|---|
| Is TWEAKR present in normal fetal-derived cells? | reproducibly detected in iEVT | moderate |
| Is TWEAKR fetal-cell-specific? | also expressed in other cell types | weak |
| Are maternal macrophages the main TWEAK source? | no stable enrichment | weak |
| Do TWEAK+ macrophages colocalise with TWEAKR+ EVT? | not reliably evaluable | none |
| Does TWEAK–TWEAKR mediate maternal–fetal tolerance? | no functional evidence | none |
| Do CRC oncofetal cells recapitulate an EVT program? | not compared | none |

TWEAKR expression in EVT does **not** imply that TWEAKR-high CRC cells reactivate an EVT
program; that would need a direct transcriptional-program comparison controlled for generic
EMT, proliferation, stress and ECM programs. A large-scale EVT–CRC comparison is explicitly
**out of scope**. DS-013 can be reopened if a developmental comparison becomes necessary.

## Figure 4 implication

Not a standalone Figure 4 panel. Use as a developmental-context observation (research notes, candidate supplementary analysis, or Discussion background). A cautious statement, still to be validated against
the CRC oncofetal transcriptional state: *TWEAKR is expressed in fetal trophoblast
populations at the maternal–fetal interface, suggesting that this receptor is associated
with cellular programs operating in both developmental and malignant contexts.*

## Not done

No DEG, pathway, YAP, spatial or Stereo-seq analysis. No genotype inference.
