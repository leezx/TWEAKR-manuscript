# Wang 2026 MFI — Checkpoint 1A: TNFSF12 / TNFRSF12A expression feasibility

- **Question:** In the normal human maternal–fetal interface, are TNFSF12 (TWEAK) and
  TNFRSF12A (Fn14/TWEAKR) expressed in maternal macrophages and fetal trophoblasts,
  respectively? Are they cell-type specific and donor-reproducible?
- **Figure mapping:** Figure 4 developmental benchmark (primary); Figure 2 normal-tissue
  ligand–receptor reference (supporting). Checkpoint evidence, not a manuscript panel.
- **Date / executor / status:** 2026-10-08 / Claude Code / complete. Human review decision:
  **EXPLORATORY / PASS WITH LIMITATIONS** (`docs/Checkpoint_1A_decision_memo.md`).
- **DS-013: CLOSED (final, 2026-10-08) — developmental context established; interaction
  hypothesis unvalidated.** Final status table, retained observations and wording guardrails:
  `docs/DS-013_final_closure.md`.
- **Checkpoint state:** CP0 PASS · CP1A PASS — Exploratory · CP1B NOT PURSUED (author request
  archived, not sent) · CP1C NOT EVALUABLE WITH PUBLIC DATA · CP1D PASS WITH SPECIFICITY
  LIMITATIONS (`docs/Checkpoint_1D_contract.md`, `docs/Checkpoint_1D_results.md`) · CP1E PASS —
  C1Q association stronger (`docs/Checkpoint_1E_core_vs_c1q.md`) · Level 3 NOT PURSUED ·
  CP2 NOT PURSUED.

## Inputs

See `manifests/input_manifest.tsv`. DS-013 `scPlacenta_host.h5ad` (SHA256 verified at run
time). REF-008 Supplementary Table 13a/b (author cell-type-level origin).

## Method

1. **Matrix QC.** X is CSR float32 with no layers and no `.raw`. Its values are
   log1p(raw integer UMI): minimum nonzero = ln 2, maximum deviation of expm1 from an integer
   = 3e-4, no negative values. 15/15 sampled rows equal log1p of the COSMOS
   `snRNA_raw_counts.h5ad`, which has an identical `newBC` order (read remotely, not stored).
   X is **not** library-size normalised.
2. **Expression.** Counts = round(expm1(X)). Library size = per-nucleus UMI total. Detection
   = UMI > 0. `mean_log1p_cp10k` = per-nucleus log1p(CP10k) averaged over nuclei; this is not
   pseudobulk. `pseudobulk_cp10k` (sum UMI / sum library × 1e4) and `mean_cp10k_per_nucleus`
   are reported separately. Library-size QC is given by cell type, donor and trimester, plus
   a depth-matched detection sensitivity analysis restricted to nuclei within the atlas
   library-size IQR.
3. **Origin.** `code/build_author_celltype_origin_map.py` derives `author_cell_type_origin`
   using explicit rules: exact or name-equivalent match → parent `minor_class` → otherwise
   ambiguous. A label is mixed if it is listed in both tables, or if its shortname and
   minor_class match opposite tables. Results: FB mixed; pvSMC mixed (S13a fetal "PV" vs S13b
   maternal "pvSMC"); GC and Ery ambiguous. This is never a genotype assignment.
4. **Summaries.** `code/checkpoint1a_expression.py` computes, per gene × cell type: n_cells,
   n_donors, n_expr, pct_expr, mean_expr_all, mean_expr_positive, mean CP10k, UMI share,
   fold vs rest, and donor statistics. Donor statistics count donors with ≥20 nuclei: number
   evaluable, number detected, detection rate, and median/IQR of pct_expr. The same metrics
   are given per donor and per trimester.
5. **Within-donor contrasts.** Pre-specified groups are compared with all other nuclei from
   the same donor (≥20 nuclei on each side). Donor is the unit. Two-sided Wilcoxon
   signed-rank test, BH correction across the 9 contrasts per metric. An exact sign test on
   direction and trimester-split direction counts are also reported. Trimester is not adjusted.
6. **Figures.** `code/plot_checkpoint1a_dotplots.py`, Python/matplotlib only, project
   Nature figure rules.
7. **CP1C (spatial feasibility).** `code/cp1c_spatial_feasibility.py` reads the COSMOS
   Stereo-seq explorer by HTTP byte range: schema, obs, spatial embedding and 12 gene
   vectors. It checks gene presence, value type, annotation granularity and coordinate
   completeness, and writes aggregate tables only. No spatial statistics.

Software: Python 3.12 (`SOFTWARES/envs/python-main/.venv`), anndata 0.12.16, h5py 3.16.0,
matplotlib 3.10.9. The analysis is deterministic; no random seed is needed.

```bash
P=$BIO_PYTHON_MAIN/bin/python; W=$LOCAL_WORK_ROOT/external/Wang_Nature_2026_MFI
$P code/build_author_celltype_origin_map.py --h5ad $W/scPlacenta_host.h5ad \
  --supp-table13 $W/paper_supplementary_2026-10-08/supp_tables/SuppTable13.xlsx \
  --out tables/author_celltype_origin_map.tsv
$P code/checkpoint1a_expression.py --h5ad $W/scPlacenta_host.h5ad \
  --origin-map tables/author_celltype_origin_map.tsv --out-dir tables \
  --expected-sha256 3b23e56a0f778665fb60df8e2bd0085d5520d0a885eec7356e4d1e61f7e2eb58
$P code/plot_checkpoint1a_dotplots.py --tables tables --out-dir figures
$P code/cp1c_spatial_feasibility.py --out-dir tables/cp1c
$P code/cp1d_macrophage_state.py --h5ad $W/scPlacenta_host.h5ad --out-dir tables/cp1d \
  --cell-dir $LOCAL_WORK_ROOT/results/DS-013_CP1D
$P code/plot_cp1d.py --tables tables/cp1d --cell-dir $LOCAL_WORK_ROOT/results/DS-013_CP1D --out-dir figures
```

## Outputs

| File | Content |
|---|---|
| `tables/author_celltype_origin_map.tsv` | 36 labels → author origin, mapping basis, analysis role |
| `tables/expression_summary_by_celltype.csv` | full expression summary (2 genes × 36 types) |
| `tables/expression_by_donor_celltype.csv` | donor-level summary |
| `tables/expression_by_trimester_celltype.csv` | All/T1/T2/T3 summary (figure source) |
| `tables/donor_paired_contrasts.csv` | within-donor contrasts with BH q |
| `tables/run_summary.json` | input hash, matrix QC, metric definitions, overall detection |
| `tables/qc_library_size.csv` | library-size distribution by cell type / donor / trimester |
| `tables/qc_depth_matched_detection.csv` | detection restricted to the atlas library-size IQR |
| `figures/CP1A_{TNFSF12,TNFRSF12A}_dotplot/` | SVG/PDF/TIFF/PNG plus source, legend and QA |
| `docs/Checkpoint_1A_decision_memo.md` | answers, rule mapping, proposed call |
| `docs/author_request_email_draft.md` | Checkpoint 1B request (not sent) |
| `docs/Checkpoint_1C_spatial_feasibility.md` | CP1C answers and proposed call |
| `tables/cp1d/`, `figures/CP1D_*` | CP1D immune landscape, module–TNFSF12 association, matched null, adjusted models (statsmodels 0.14.6, scanpy 1.12.1; seed 0) |
| `tables/cp1c/` | Stereo-seq explorer: value QC, nonzero fractions (not detection), coordinate QC, cell-type counts |

## Main results

- **TNFSF12** is detectable in maternal macrophages but is neither highly expressed nor
  macrophage-specific. Atlas-wide detection is 0.94%; CD14_M 2.5% (rank 8/36, or 4/36 when
  depth-matched). The within-donor Wilcoxon gives q = 0.03, but the effect is small
  (+0.36 percentage points) and direction is not consistent (13/23 donors, sign test
  p = 0.17; 9 donors have zero macrophage detection). LEC, T and DSC1 remain higher after
  depth matching.
- **TNFRSF12A** is reproducibly expressed in fetal trophoblast populations, particularly
  iEVTs (16.3%; 13/13 donors; robust to depth matching), but is not exclusive to
  trophoblasts: aEC, fEC, mixed FB/pvSMC and DSC3 also express it. The EVT group as a whole is
  not enriched over all other cells within donors. The T3 rise occurs despite lower T3
  depth; composition vs within-EVT upregulation has not been resolved.

## Validation, limitations, claim ceiling

- Independent anndata re-extraction reproduced the detection counts exactly. Both genes
  were checked for unique var matches. An earlier run silently dropped 11 cell types with
  an empty `analysis_role` (NaN group keys). This was fixed, and the script now asserts full
  coverage.
- Origin is cell-type-level only. Mixed types (FB, pvSMC) support no origin-specific claim.
  snRNA-seq under-detects some ligands. T3 (5 donors) shows a global rise in TNFRSF12A.
- **Claim ceiling:** descriptive co-expression feasibility. This analysis does not show
  spatial proximity, signalling, or immune tolerance.

## Review

PR: none, by user decision. The branch `analysis/20261008-wang2026-mfi-checkpoint1a` is kept as the archive; not merged. Ledgers: project WorkLog WL-20261008-018 to -023; DS-013 (CLOSED); REF-008.
