# A3b Stage S final review — ChatGPT ("Fig.1b-CT2 plasticity"), 2026-10-12, on commit 23eb194

- **Verdict:** CONDITIONAL APPROVED — minor correction required.
- **What was checked:** the reviewer read `A3b_stageS_results.md`, `A3b_pooled.tsv`, `A3b_study.tsv`, `A3b_cohort_estimates.tsv`, the patient-level E1 table and `a3b_estimands.py`.
- **Format:** a condensed record. Wording recommendations are quoted.

## Decisions

| Item | Status |
|---|---|
| CT2 scoring execution / join QC | APPROVED |
| E1 primary statistical interpretation | APPROVED; Chen P02 clinical eligibility must be resolved |
| E1 mandatory sensitivities | APPROVED; interpretation tightened |
| Four normal–primary programmes | APPROVED; update after P02 decision |
| E1-L | APPROVED as secondary exploratory |
| Qin E1-pp (depth-matched) | APPROVED |
| Qin original-depth / programme readouts | **CORRECTION REQUIRED:** exclude TRG0 |
| Chen E1-pp | APPROVED as exploratory ED |
| E3 | Descriptive only; no pooled inference |
| Figure drafting | **GO** |
| Final figure lock / Stage S closure | HOLD pending the minimal correction |

## Per question

### 1. E1

- **Status:** approved; direction consistent, pooled inference uncertain.
- **Wording:**

  > "Across six independent studies, tumour-specimen epithelium consistently exhibited higher point estimates of CytoTRACE2-predicted developmental potential than paired adjacent-normal epithelium; however, the pooled random-effects estimate was imprecise and did not reach statistical significance."

- **Sensitivities:**
  - They use partly different patient sets, so we cannot claim that technical confounding is excluded.
  - Wording: "Positive point estimates were retained across the prespecified sensitivity analyses, although none provided statistically conclusive pooled evidence."
- **Model:** no MUI exclusion and no model change to rescue p=0.069.

### 2. Programmes

- **Status:** approved, at the tissue-context level only.
- **Limits:**
  - proCSC, revCSC and ExtCIOC are 7/7 same-sign and pass BH.
  - Only ExtCIOC's PI is above 0.
  - The UCell scores are original depth only; no depth-matched programme sensitivity was run.
  - This cannot be read as malignant cells upregulating these programmes, or as oncofetal reprogramming or lineage conversion.
- **Wording:**

  > "Paired tumour specimens exhibited higher epithelial proCSC, revCSC and Extended CIOC signature scores than adjacent-normal specimens, whereas YAP-core scores did not show a statistically supported pooled difference."

### 3. E1-L Cycling Stem/TA

- Secondary exploratory: Extended Data, no significance stars, and a note that Pelka is excluded because of training-set overlap.
- Absorptive differentiated-like (CI crosses 0) must be shown alongside it.

### 4. Pre/post

- **Wording:**

  > "Neither cohort showed a statistically supported change in CT2-predicted developmental potential after treatment when sequencing depth was matched."

- Do not write "no depth-robust change". The samples are small (18 and 10), so this is not an equivalence result.
- The Qin original-depth vs depth-matched difference uses different patient sets. It cannot be attributed wholly to depth, nor to biopsy-versus-resection quality.
- **Contract deviation found:**
  - Frozen §3 puts Qin TRG0 patients in composition only.
  - The original-depth sensitivity and the four programmes used `E1_prematch` eligibility, which still included TRG0 patients XFZ07 and XFZ48.
  - Correct n=22 to n=20 and re-summarise. No rescoring is needed.
  - Add a descriptive same-18-patient original-depth vs depth-matched comparison.
  - Do not report Qin original-depth p=0.004 or the proCSC decrease before the correction.

### 5. Chen P02

- Treat this as clinical-eligibility correction. The effect direction must not decide it.
- If prior treatment is confirmed: file a dated clinical-eligibility amendment, exclude P02 from all normal–primary estimands, re-pool from the existing patient statistics (expected E1 85 patients; Chen 16), and keep the frozen 86-patient Atlas-label analysis as a traceable sensitivity.
- If uncertain: keep the primary analysis and report an exploratory excluding-P02 sensitivity.
- No change to depth targets, identity or thresholds.

### 6. Figures

GO for draft Extended Data panels. Final figures must use the corrected inclusion list.

| Panel | Content | Notes |
|---|---|---|
| ED-A | E1 forest: 6 studies, REML/HK pooled estimate, CI and PI, plus sensitivities (i)–(iii) | MUI shown |
| ED-B | Forest for the 4 programmes with BH p | E1-L as an adjacent small panel, labelled secondary exploratory |
| ED-C | Qin and Chen paired pre/post plots, depth-matched primary, plus a small original-depth inset | Legend states the Qin biopsy/resection and processing confound, and that Chen Post specimens are verified only by GEO stage |

## Claim ceiling

- **Not supported:** "CRC malignant cells have significantly higher developmental potency than matched normal cells."
- **Supported:**

  > "Paired analyses revealed consistently positive but heterogeneous differences in CT2-predicted developmental potential between tumour-specimen and adjacent-normal epithelium, without conclusive evidence for a pooled effect after depth matching. In contrast, several CSC- and oncofetal-associated transcriptional programmes were elevated in tumour-specimen epithelium, while exploratory pre/post-treatment comparisons showed no statistically supported depth-matched CT2 changes."

- **Strategy:** treat A3b as supporting evidence, and do not invest heavily in a normal → tumour → post-treatment potency progression. The stronger main line is A3a: canonical proCSC couples with transcriptome-derived potency, whereas the revival/YAP programmes do not follow the same robust pattern.

## Next (reviewer)

Submit the corrected Qin pre/post summaries and the Chen P02 eligibility decision, and keep the old tables as an audit record. If the numbers and inclusion rules agree, A3b final approval and the ED figures follow.
