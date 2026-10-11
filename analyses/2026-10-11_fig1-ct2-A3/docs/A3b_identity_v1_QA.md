# A3b identity_v1 — QA report (Stage I steps 1–4; contract v0.3 §8 step 5 hold point)

- **Date:** 2026-10-11.
- **No CT2, no UCell, no programme score** has been computed or read for A3b.
- **identity_v1:**
  - Argos path: `analysis/fig1_ct2_A3_20261011/A3b/identity_v1.private.tsv.gz`
  - 425,183 L1 epithelial cells, 447 samples, 165 patients, 10 studies
  - SHA256: `2098d172dd36431fc745c4ca0a4b793d812214206396dc437ee91d4512d57819`
- **Code:**
  - `a3b_export.py`, `a3b_infercnv.R`, `a3b_cnv_calls.py`, `a3b_evidenceN.py`, `a3b_identity.py`, `a3b_identity_qa.py`
  - Run commits 7b84824 → c062dfa. The second commit only registered the pickled Axis-L class; no logic changed.
- **SGE jobs:** export 3655276/7; inferCNV 3655279 (165/165); T calls 3655280; N 3655281 (10/10); identity 3655319; QA 3655320.
- **Public tables:** `tables/a3b_identity/`.

## 1. Execution and gate outcomes

| Gate | Result |
|---|---|
| F1 exact match with Fig. 1b `annotation_v1` | **0 mismatches in all 10 studies** (535k+ cohort-v1 cells checked) |
| Joint inferCNV | 165/165 patients run. CNV assessable: 153 (12 have <100 reference cells or no epithelium) |
| Concordance with Fig. 1b calls | 165 patients; 29 have no overlapping v1 cells. **30 patients fail:** 14 with κ < 0.40, 23 clear-CNV flips (overlapping). Flips are symmetric (12 F→T, 11 T→F) with median primary-side CNV-high fraction 0.20, i.e. at the 20% boundary. Qin accounts for 15 failures (κ median 0.50) |
| Normal-side CNV-high gate (median > 2% → T void) | **Void in 5/10 studies:** Uhlitz 14.8%, Chen 7.9%, Khaliq 7.2%, MUI 4.3%, Qin 3.2% (4 post-treatment normals). **Calibrated:** Joanito 1.1%, Lee 1.0%, Pelka 1.3%, Qian 0.2%, Li 0.1% |
| Evidence N calibration (median own-normal normal-like ≥ 0.75; ≥5 reference patients) | **Passes in 10/10** (0.91–0.96). Li and Qin use post-treatment normal references (flagged) |

**Observation on the normal-side CNV-high gate (descriptive, not a rule change):**
- Normal-side CNV-high rates are *not* higher in clear-CNV patients. Within-study medians, clear-CNV vs not:

  | Study | Clear-CNV | Not clear-CNV |
  |---|---|---|
  | Joanito | 0.010 | 0.255 |
  | Uhlitz | 0.092 | 0.256 |
  | Pelka | 0.004 | 0.014 |
  | Chen | 0.105 | 0.064 |

- Tumour contamination of the adjacent normal would predict the opposite pattern.
- The more likely source is the immune/stromal reference: it leaves epithelium-specific regional expression, which is called as CNV in normal epithelium.
- This failure mode was invisible in Fig. 1b, which scored tumour-sample epithelium only.

## 2. Identity composition

- **Overall:**
  - normal-like 306,753 (72.1%);
  - ambiguous 115,363 (27.1%);
  - tumour-evidence 3,067 (0.7%): Joanito 1,261, Lee 918, Pelka 882, Qian 6.
- Source: `composition_by_study.tsv` (median sample fractions).

| Branch / study | Normal side: normal-like | Tumour side: normal-like / tumour-evidence / ambiguous |
|---|---|---|
| N–P Chen | 0.85 | 0.74 / 0 / 0.26 |
| N–P Joanito | 0.90 | 0.25 / 0.15 / 0.48 |
| N–P Khaliq | 0.86 | 0.81 / 0 / 0.19 |
| N–P Lee | 0.90 | 0.55 / 0 (median) / 0.37 |
| N–P MUI | 0.89 | 0.40 / 0 / 0.60 |
| N–P Pelka | 0.89 | 0.56 / 0 (median) / 0.41 |
| N–P Qian | 0.91 | 0.81 / 0 / 0.20 |
| N–P Uhlitz | 0.80 | 0.48 / 0 / 0.52 |
| Qin Pre → Post (tumour) | — | normal-like 0.62 → 0.80 |
| Chen Pre → On → Post (tumour) | — | normal-like 0.77 → 0.86 → 0.80 |
| Li Pre → Post (tumour bed) | — | normal-like 0.83 → 0.87 |

## 3. Key limitation: Evidence N has low sensitivity for overt tumour cells

Validation table `N_space_cnv_high.tsv`: the share of CNV-high cells in clear-CNV patients that lie beyond τ_p.

| Study | Share beyond τ_p |
|---|---|
| Khaliq | 0.04 |
| Qian | 0.05 |
| Qin | 0.16 |
| Chen | 0.21 |
| Joanito | 0.24 |
| Pelka | 0.29 |
| Uhlitz | 0.32 |
| Lee | 0.32 |
| MUI | 0.45 |

**Consequences:**
- About 55–96% of overt (CNV-high) tumour cells fall inside the normal-reference distance threshold.
- Per contract, such cells are **ambiguous**; the cutoff was not moved. The tumour-evidence class therefore requires d > τ_p, which removes most CNV-high cells and leaves only 3,067 tumour-evidence cells.
- More important: **CNV-negative tumour cells cannot be distinguished from normal mucosa by N.** The tumour-side "normal-like" fraction (0.25–0.81) is therefore *not* an estimate of residual normal epithelium. It is an upper bound that includes normal-similar tumour cells.
- This undermines the interpretation of:
  - E2 composition ("normal-like share");
  - E4 (normal-like tumour side vs normal side);
  - the pre/post composition shifts (E2-pp).
- E1 (tissue context, all epithelium) does not depend on identity.

## 4. Axis-L coverage

- Lineage-unresolved under the v0.3a rule: 6–19% of normal-side cells and 12–27% of tumour-side cells (`axisL_coverage.tsv`).
- Pelka is flagged and excluded from E1-L.

## 5. Final eligibility (replaces the metadata-screen counts)

Source: `eligibility_studies.tsv`. E1 counts are after depth matching. T_s per branch × study is in `qa_summary.json`.

| Contrast | E1 (post-match) | E1 pre-match | E2 | E3 | E4 |
|---|---|---|---|---|---|
| N–P Pelka | 30 | 30 | 31 | 6 | 30 |
| N–P Chen | 17 | 18 | 19 | 0 (T void) | 18 |
| N–P Lee | 12 | 17 | 18 | 5 | 18 |
| N–P MUI | 12 | 12 | 12 | 0 (T void) | 12 |
| N–P Uhlitz | 10 | 11 | 11 | 0 (T void) | 10 |
| N–P Qian | 5 | 5 | 6 | 0 | 6 |
| N–P Joanito | 3 | 5 | 11 | 4 | 9 |
| N–P Khaliq | 3 | 3 | 7 | 0 (T void) | 6 |
| Qin Pre vs surgical Post (TRG0 excluded) | 18 | 22 | 25 | 0 (T void) | 25 |
| Chen Pre vs GEO-annotated Post | 10 | 11 | 14 | 0 (T void) | 13 |
| Li Pre vs Post | — (composition only) | 8 | 8 | NO-GO | 8 |

**Implications under the frozen rules:**
- **Primary E1 normal–primary:** **6 qualifying studies, 86 patients** (Pelka 30, Chen 17, Lee 12, MUI 12, Uhlitz 10, Qian 5). Estimable.
- **E3:** only Pelka (6) and Lee (5) qualify (Joanito 4), fewer than 3 studies → **descriptive only**. It is also MSS/CNV-selected.
- **E3-pp:** 0 in all cohorts (Qin and Chen T void) → not estimable.
- **E1-pp:** Qin 18, Chen 10 → per-cohort exploratory.
- **E1-L:** pending a per-class count at the CT2 step (Pelka excluded).

## 6. Questions for review

1. Accept identity_v1 as frozen (SHA above) and authorise Stage S (CT2 + UCell) for the estimands that remain estimable?
2. Given the low N sensitivity (§3), should E2 and E4 (and E2-pp) be:
   - (a) kept, but worded strictly as "similarity to normal mucosa" (an upper bound on residual normal epithelium); or
   - (b) demoted to descriptive QA only?
   We recommend (b) for E4 and (a)-descriptive for E2.
3. Should E3 stay as a descriptive two-study (Pelka, Lee) secondary, given its MSS/CNV selection and only 11 patients?
4. Should the T-void outcome in 5 studies and the reference-artefact observation be reported in Methods/ED as a limitation of immune/stromal-referenced inferCNV for distinguishing normal from tumour epithelium? This bears on how the Fig. 1b CNV-supported subset is described, although Fig. 1b only used tumour samples.
