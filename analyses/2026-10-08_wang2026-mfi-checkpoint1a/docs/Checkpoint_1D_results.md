# Checkpoint 1D results — TWEAK-associated macrophage state (DS-013, scoped reopening)

**Decision (human review, 2026-10-08): PASS WITH SPECIFICITY LIMITATIONS.** Level 3: HOLD. CP1E
(CORE vs C1Q) assembled in `Checkpoint_1E_core_vs_c1q.md`. Original proposed call: PASS on the
pre-specified criteria for CORE (and EXTENDED), with a specificity caveat. The TNFSF12 association is shared with, and partly
explained by, a C1Q-complement macrophage axis. The effect is modest.**
Level 3 is not started and needs separate approval. Stereo-seq is untouched.

Contract: `Checkpoint_1D_contract.md`, written before analysis. One method amendment was made
before any result was seen: the conditional logit was replaced by donor fixed-effects logit.
Code: `code/cp1d_macrophage_state.py`, `code/plot_cp1d.py`. Tables: `tables/cp1d/`.
Cell-level UMAP and score files are in `$LOCAL_WORK/results/DS-013_CP1D/` (not in the repo).

## Level 1 — immune landscape

- The author snRNA labels resolve maternal macrophages (CD14_M 7,261; CD16_M 2,015), fetal
  HB (3,172), dNK (9,563), T (1,130), B (362) and cDC (435). Marker patterns are consistent
  with these labels: CD163, CSF1R and C1Q in macrophages and HB; GNLY and KLRD1 in dNK;
  MS4A1 in B; CLEC9A in cDC.
- There is no separate monocyte label. CD16_M carries monocyte-like features (FCN1 10%,
  LYZ 27%), so a CD14_M-only sensitivity analysis was run.
- Mast cells are essentially absent (one TPSAB1+KIT+ nucleus in the atlas).
- snRNA detection of CD3/TRAC is low, and ambient GNLY is visible in non-NK labels.
- Re-annotation was judged unnecessary. Figure: `figures/CP1D_L1_immune_landscape/`.

## Level 2 — maternal macrophages (CD14_M + CD16_M; 9,276 nuclei; 212 TNFSF12+; 14 informative donors)

| Pre-specified criterion | CORE | EXTENDED |
|---|---|---|
| MH OR, score-high vs score-low halves within donor | 1.43 (1.08–1.89) ✓ | 1.52 (1.15–2.01) ✓ |
| Donors high > low (exact two-sided sign test; among the 14 donors with detectable TNFSF12 in macrophages) | 12/14, 2 lower (p = 0.013) ✓ | 11/14, 2 lower (p = 0.022) ✓ |
| Logit OR per SD, donor FE + log library size | 1.29 (1.11–1.50) ✓ | 1.43 (1.24–1.64) ✓ |
| Matched random-module null (500) | null median 1.01, q95 1.17; p = 0.002 ✓ | p = 0.002 ✓ |
| Adjusted for LYSO_CONTROL | 1.25 (1.06–1.47) ✓ | 1.86 (1.45–2.37) ✓ |
| CD14_M-only direction kept | OR/SD 1.23 (1.03–1.46); 10 higher, 3 lower of 14 donors ✓ | 1.34 (1.13–1.60) ✓ |
| Depth | high/low library-size ratio 1.02 ✓ | 0.99 ✓ |

Absolute effect: TNFSF12 detection is **2.7% in score-high vs 1.9% in score-low**
macrophages (pooled). The signature raises the probability of detecting TNFSF12 modestly;
it does not recover a sharply defined TNFSF12+ population.

### Controls and specificity

- **Generic lysosomal module:** weak association (1.18; 1.01–1.37), no MH effect (1.06),
  9/14 donors, null in CD14_M only. It does not explain CORE: CORE vs lysosomal ρ = 0.30.
- **Macrophage identity:** not associated (1.13; 0.97–1.32). **Monocyte-likeness:** null (1.02).
  So the association is not simply "more macrophage-like" cells or monocyte contamination.
- **C1Q complement module (planned as a generic control):** associated **as strongly or more
  strongly** than CORE (OR/SD 1.42; MH 1.87; 12/14 donors), despite low correlation with
  CORE (ρ = 0.18; top-quartile Jaccard 0.18).
- **Post hoc** joint model: CORE 1.21 (1.04–1.41) and C1Q 1.38 (1.22–1.57) are both retained.
  In CD14_M only, CORE drops to 1.18 (0.99–1.40). EXTENDED's extra strength comes mostly from
  its C1Q genes (EXTENDED + C1Q: 1.22, 1.02–1.46).
- CORE and EXTENDED overlap partly (ρ = 0.70; top-quartile Jaccard 0.44).

### Fetal macrophages (HB; 3,172 nuclei; 55 TNFSF12+; 6 informative donors)

No association for any module (CORE 1.03, 0.76–1.39). This group is underpowered.

## Interpretation (claim ceiling)

- Supported: in human decidual (maternal) macrophages, nuclei scoring high for the
  AOM/DSS-derived SPP1/TREM2/GPNMB/APOE core program are modestly but reproducibly more likely
  to have detectable TNFSF12. The association is beyond matched random modules, library size
  and generic lysosomal activity, and is consistent in direction across most informative
  donors. This is a **TWEAK-associated macrophage state** at the level of association.
- Not supported or not shown:
  - that signature-high cells express or secrete TWEAK protein;
  - that CORE is a TWEAK-specific classifier, since a C1Q-high complement axis carries at
    least as much TNFSF12 association;
  - any link to TWEAKR+ trophoblasts, spatial proximity or tolerance.
- Limitations:
  - 9 of 23 donors contribute no TNFSF12+ macrophages.
  - Gestational age was not modelled in Level 2.
  - The signature is mouse-derived and was transcribed from a figure; the mouse DE statistics
    were not re-analysed.
  - The UMAP is the authors' integrated embedding, not recomputed.
  - Score control genes are re-implemented; agreement with scanpy `score_genes` is
    Spearman 0.98 (random control-gene draws differ).

## Gate to Level 3 (decision for the user)

The pre-specified PASS criteria are met. Before any donor-level co-occurrence analysis with
TNFRSF12A+ EVT, consider whether the state should be defined as CORE alone or as CORE plus the
C1Q axis. Level 3 would require gestational-age control and would remain non-spatial.
