# Fig. 1c contract v0.1 — GPT technical audit (2026-10-11)

- Conversation: https://chatgpt.com/c/6acbaf02-1bc8-83ea-a533-5d9a9c06e138 (same conversation as the design consultation). The full text is in the conversation; this file is a structured record. Section names and verdicts are copied exactly.
- Submitted: `Fig1c_contract_v0.1_draft.md`, plus 4 facts:
  - no human pro/rev reference;
  - the anchors sit inside the Qin sets;
  - DS-010 is not in cohort v1;
  - Mzoughi 2025 is verified.

## Overall: REVISE

- Scientific framework: **FREEZE**.
- Operational contract: **REVISE**.

| Section | Verdict | Reason |
|---|---|---|
| §0 Scope / H1a / H1b | FREEZE | — |
| §1 CT2 inputs | FREEZE | reuse of Fig. 1b |
| §2.1 Axis L / Pelka | REVISE | label hierarchy, calibration, domain shift |
| §2.2 Axis S / S1 | REVISE | gene-split does not resolve definition–validation circularity |
| §2.3 Final assignment | REVISE | S overriding L conflates lineage, programme and state |
| §2.4 Gates | REVISE | mix validity, feasibility and biology; missing OOD, stability, specificity |
| §3 Statistics | REVISE | conditional estimand, depth rule, baseline selection |
| §4 Scope | FREEZE | — |
| §5 Order | REVISE | add an S-axis decision stage |

## A. Axis S

**Decision:** S3 (full Qin signatures, continuous pro × rev) is the primary representation. S1 (repeated gene-split) becomes an ED robustness check. S2 (Mzoughi huOnF) becomes ED external validation.

- **Two kinds of circularity:**
  - Type I (annotation–outcome) is already handled by CT2-blinding.
  - Type II (definition–validation) is only partly mitigated by a gene-split. Both halves share the mouse prior, the ortholog mapping and the co-expression structure. A high split-AUC shows signature coherence, not separable states; a single continuous gradient would also give it.
- **Mzoughi human OnF:** GPT reports that Mzoughi gives a human OnF signature (huOnF) in **Supplementary Table 1f**, built from mouse OnF orthologues and filtered with independent human fetal vs adult intestine data. *(Not verified by us.)*
  - Use it as convergent-validity evidence for the rev axis, not as its definition.
  - Check its gene overlap with revCSC, and test concordance on non-overlapping genes.
  - Check whether its source cohorts overlap cohort v1.
- **Operational strata for the CT2 contrasts:**
  - Groups: pro-dominant, rev-dominant, hybrid-high and neither-high, using the sample-specific 75th percentile (consistent with the A3a co-activation definition).
  - Report threshold sensitivity at the 70th and 80th percentiles.
  - Call them "programme-defined strata", not cell types.
  - Do not use their prevalence as evidence of enrichment, because the threshold fixes the marginal high fractions.
- **H1a revised wording:** "reproducibly identifiable stem-associated transcriptional configurations, which may present as a continuum with hybrid activation".

## B. Axis L (Pelka)

**Accepted, with revisions:**

- **Training labels:** train on all 11 original cE labels and aggregate to classes afterwards with a pre-set hierarchy. Do not collapse before training.
  - cE02 (Stem/TA/Immature Goblet) and cE07 (Goblet/Enterocyte) are transitional.
  - Classes with poor held-out performance go to rare/uncertain.
- **Patient-grouped folds:** all samples from one patient, normal and tumour, stay in one fold. Feature selection, tuning and calibration happen inside the training folds (nested CV, or separate train, calibration and evaluation patients).
- **Overlap check:** verify the Pelka patient IDs that overlap cohort v1 by actual ID, not by study name.
- **Normal + tumour training:** accepted. Sensitivities:
  - tumour-only training;
  - tumour-only held-out performance;
  - a tissue-source confounding check.
- **New, OOD handling:**
  - an expression-space OOD or reference-neighbourhood distance score;
  - a leave-one-class-out unknown-rejection test;
  - unassigned/OOD fractions by study;
  - unmatched cells are labelled "lineage-unresolved".
- Pelka lineage transfer does **not** validate Axis S.

## C. Gates v0.2 (replacing G1–G6)

| Gate | Content | Hard? |
|---|---|---|
| G1 Lineage transfer | patient-held-out collapsed macro-F1 ≥ 0.70; per-class precision/recall; tumour-only performance; calibration | hard |
| G2 Programme integrity | gene coverage; full vs split stability within patients; no single-gene driver | hard |
| G3 External concordance | rev vs huOnF agree in direction in most patients, including on non-overlapping genes; pro supported by independent stem/proliferation anchors | wording |
| G4 Distinguishability | pro/rev correlation, joint occupancy, hybrid fraction, conditional specificity, cross-patient stability; within-patient r ≳ 0.9 triggers a redundancy review | wording |
| G5 Coverage | ≥30 cells per stratum, ≥20 patients, ≥3 studies per contrast, plus a **patient eligibility / reference-availability audit** | hard |
| G6 Co-existence | pro-dominant and rev-dominant each ≥30 cells in one sample, in ≥20 patients across ≥3 studies | wording |
| G7 Technical dependence | depth, genes, cell cycle and mito association audit, including continuous scores; reported, not used as a gate trigger | report |
| G8 OOD | unknown-rejection validation; unassigned/OOD by study; cutoff set from the OOD performance | — |
| G9 Study robustness | >40% from one study is a warning, plus LOSO | warning |
| G10 Provenance | features, partitions, holdouts, thresholds and hashes all locked | hard |

- The v0.1 G5 rule ("AUC > 0.75 triggers co-primary") is rejected.
  - Depth-matched CT2 is a **mandatory robustness endpoint for every primary contrast**.
  - A strong potency claim must pass it.
  - If it disagrees with the primary result, the finding is reported as "depth-sensitive".

## D. Other required changes

1. **H1b estimand.**
   - Primary question: the lineage-conditioned joint organisation of the pro and rev programmes.
   - Secondary question: within-patient CT2 contrasts among pro-dominant, rev-dominant and differentiated-like strata.
   - These contrasts are not functional differences between cell types.
2. **Differentiated baseline.**
   - Primary reference: Axis-L Enterocyte-like cells, defined independently of Axis S.
   - Sensitivities: Enterocyte-like with S-low; other differentiated lineages.
   - Overlapping cells (L-Enterocyte that are also pro/rev-high) are labelled "lineage–program discordant", excluded from the strict reference, and their fraction is reported.
3. **Mechanistic holdouts.**
   - Keep two versions: Qin-full scores (identical to A3a) and mechanism-blinded scores, which drop TNFRSF12A, the YAP core and TWEAK-response genes. Report any divergence between them.
   - Exclude the same holdout list from the Axis-L classifier features.
   - Freeze gene IDs, the ortholog version and the retained genes per set.
4. **Adjustment level.**
   - Unadjusted: sample-level medians, then paired differences.
   - Adjusted: a within-sample conditional model, with a pre-set fallback if it cannot be estimated.
   - Depth-matched: ds1–5 on identical cells, groups and patients. Each replicate gives patient-level effects; the replicates are not treated as independent patients.
   - No pooled cell-level regression.
5. **Eligibility selectivity.**
   - Report which patients have pro, rev and a reference group, and which lack a reference.
   - Report the characteristics of excluded patients: study, MSI, depth and composition.
   - If many high-oncofetal tumours lack a reference, add a secondary continuous model over all evaluable patients.

Additional points:

- **Population wording:** "epithelial cells isolated from treatment-naive primary CRC tumor specimens (tumor-specimen-derived epithelium), without assuming universal malignancy".
- **Relation to A3a:** S3 uses the same Qin signatures, so it is **not** an independent validation of A3a. The increment of Fig. 1c is lineage-conditioned joint organisation, co-activation architecture and patient-level strata contrasts.
- **Stage 1 can run before A3a finishes,** provided every Axis S threshold change is made before any contact with CT2.

## G. Decision matrix after Stage 1

| Stage 1 outcome | Allowed | Fig. 1c interpretation |
|---|---|---|
| L reliable; pro/rev stable; external concordance | continuous landscape + operational contrasts | distinct transcriptional configurations, possible hybrid continuum |
| L reliable; pro ≈ rev | continuous only | shared stem-associated programme architecture |
| L reliable; rev–OnF concordant; pro mostly proliferation | keep both axes, weaker pro interpretation | proliferation- vs oncofetal-associated programmes |
| L unreliable; Qin axes reproducible | lineage-independent description only | epithelial programmes, lineage unresolved |
| Qin axes unstable or concordance fails | stop the two-configuration claim | unable to resolve two configurations |

The A–F CT2 branches then apply after Stages 3–4.
