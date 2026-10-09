# Fig. 1B dataset screen — which CRC Atlas studies contain epithelial, immune and stromal cells

- **Question:** Which studies in the DS-001 CRC Atlas contain all three major compartments
  (epithelial, immune, stromal) in enough patients to support a patient-level pan-cellular
  CytoTRACE2 analysis? Incomplete studies are excluded (user rule, 2026-10-09).
- **Figure mapping:** Figure 1B (cohort selection; precedes any CytoTRACE2 run).
- **Date / executor / status:** 2026-10-09 / Claude Code. v1 screen reviewed and approved as a
  **candidate pool** with required checks. The checks were added in v2 (this document), which is
  pending review. No CytoTRACE2 and no expression values were used: obs metadata only.

## Inputs

| Input | Path (Argos) |
|---|---|
| Atlas backbone H5AD (obs only) | `/home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/data/final_crc_atlas-adata.count.only.h5ad` |
| Manuscript patient scope (691 patients, 42 studies) | `/home/zz950/DATA/scRNAseq/meta_study/CRC_metadata_extraction/patient_characteristics/crc_patient_metadata.tsv` |
| Heuristic lineage for supplemental objects (WL-20261009-003) | `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/atlas_major_lineage_20261009/` |

Argos run directory: `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_dataset_screen_20261009/`.

## Method (definitions fixed before counting)

- **Lineages,** from the harmonized `atlas_cell_type_middle`:
  - Epithelial = Epithelial progenitor, Epithelial cell, Goblet, Tuft, Enteroendocrine, Cancer cell, CRLM
  - Myeloid = Monocyte, Macrophage, Dendritic cell, Neutrophil, Eosinophil, Mast cell
  - T/NK = T cell CD4, T cell regulatory, T cell CD8, NK cell, ILC, T cell γδ, NKT
  - B/Plasma = B cell, Plasma cell
  - Fibroblast; Endothelial; Pericyte
  - Not counted: Platelet, Cancer cell circulating, Hepatocyte, Schwann cell
- **Broad compartments:** Immune = Myeloid + T/NK + B/Plasma; Stromal = Fibroblast + Endothelial + Pericyte.
- **Tissue scope:** only `primary tumor` samples, filtered **before** aggregating to the patient, so
  no patient is completed with lymph node, normal or blood cells.
- **Treatment** is coded per sample as naive / treated / unknown. Unknown is never merged into either.
  - Primary scope = naive primary tumour samples.
  - Sensitivity scopes = naive + unknown, and any treatment.
  - Chen 2024, Qin 2023 and Li 2023 have pre- and post-treatment samples from the same patients.
    Their naive samples are pre-treatment tissue.
- **Sorting class** per sample: unsorted / immune-enriched / non-immune-enriched / mixed / unknown,
  from `enrichment_cell_types`. The Atlas value `naive` is read as unsorted; this has not been
  checked against each paper.
- **Completeness:**
  - A patient is complete when each of Epithelial, Immune and Stromal has ≥ N cells.
  - A study passes when it has ≥ M complete patients.
  - Three threshold sets: permissive 20/5, **primary 30/5**, stringent 50/10.
  - Also reported:
    - sample-level completeness: one primary tumour sample complete on its own;
    - unsorted-only completeness;
    - fibroblast-specific completeness (Epithelial, Immune, Fibroblast);
    - 7-lineage coverage.
  - The fibroblast and lineage tables are descriptive. They are **not** inclusion criteria.

Code: `code/screen_compartments.py` (v2) and `code/check_htapp_pelka_overlap.py`. Python 3.8 (`r4p3`
conda env on Argos), h5py, pandas.

```bash
python code/screen_compartments.py --h5ad <Atlas H5AD> --scope-tsv <crc_patient_metadata.tsv> \
  --lineage-dir <atlas_major_lineage_20261009> --out-dir tables/v2
python code/check_htapp_pelka_overlap.py --h5ad <Atlas H5AD> --scope-tsv <crc_patient_metadata.tsv> --out-dir tables/v2
```

## Study inclusion flow (`tables/v2/study_inclusion_flow.csv`)

Every study in the H5AD or the scope table (54 in total) has a recorded fate:

```text
54 study labels (49 in the H5AD + 5 supplemental objects)
├── 12 excluded before screening: in the H5AD but not in the 42-study manuscript scope
│      (non-CRC/reference: Burclaff, Conde, Elmentaite, Garrido-Trigo, He 2020, James 2020,
│       Kong 2023, Mazzurana, Parikh, Scheid, Smillie, Thomas 2024)
├── 5 not screened: supplemental objects with no harmonized cell types
│      (Moorman 2024, GSE178318, GSE205506: heuristic lineage at study level only;
│       CSE0000154, GSE236581: heuristic lineage not complete)
└── 37 screened (all 586 backbone patients found in the H5AD; 3,812,174 cells)
       ├── 13 PASS (primary 30/5, primary tumour, treatment-naive)
       └── 24 FAIL
```

37 screened + 5 supplemental = the 42 studies of Supplementary Table 1. Matching the cell total
(5,794,398) alone does not prove that patients are assigned correctly, so identifiers were checked
separately (next section).

## Identifier checks (`tables/v2/run_summary.json`)

| Check | Result | Consequence |
|---|---|---|
| Cell index unique | yes (4,264,929) | — |
| Scope patients missing from H5AD | 0 / 586 | — |
| Patient ID in >1 study | 2 (Joanito SC040, SC044 also in Borras 2023) | Borras fails, so no double counting among passing studies. Same harmonized ID, so the Atlas already treats them as one patient |
| Sample ID shared by >1 patient | 14 (all Zhang 2018: pooled sort-population labels) | Zhang 2018 fails; the screen keys on patient + sample |
| Sample with >1 sample type | 0 | — |
| Patient with >1 treatment value | 57 (Chen 2024, Qin 2023, Li 2023, Bian 2018, Yang 2023) | pre/post-treatment sampling; handled by per-sample treatment coding |

## Results

### Threshold sensitivity (primary tumour, treatment-naive)

| Study | Patients | Complete 20/5 | **Complete 30/5** | Complete 50/10 | Sample-level 30 | Unsorted-only 30 | Fibroblast 30 | Sorting |
|---|---|---|---|---|---|---|---|---|
| Pelka 2021 | 62 | 55 | **50** | 42 | 45 | 45 | 21 | mixed by sample (CD45+ and unsorted) |
| Joanito 2022 | 31 | 31 | **30** | 30 | 30 | 30 | 30 | unsorted |
| Lee 2020 | 34 | 30 | **28** | 25 | 28 | 28 | 23 | unsorted |
| Qin 2023 | 27 | 27 | **27** | 27 | 27 | 27 | 26 | unsorted |
| Chen 2024 | 20 | 19 | **19** | 18 | 19 | 19 | 12 | unsorted |
| MUI Innsbruck | 12 | 12 | **12** | 10 | 12 | 12 | 5 | unsorted |
| Liu 2024 | 15 | 12 | **12** | 9 ✗ | 12 | **0** | 10 | mixed CD45+/CD45− |
| Uhlitz 2021 | 12 | 11 | **10** | 10 | 10 | 10 | 8 | unsorted |
| Li 2023 | 10 | 10 | **9** | 9 ✗ | 9 | 9 | 6 | unsorted |
| Khaliq 2022 | 16 | 8 | **7** | 4 ✗ | 7 | 7 | **3** | unsorted |
| Qian 2020 | 7 | 7 | **7** | 7 ✗ | 7 | 7 | 7 | unsorted |
| Guo 2022 | 6 | 6 | **6** | 6 ✗ | 6 | 6 | 6 | unsorted |
| Qi 2022 | 5 | 5 | **5** | 5 ✗ | 5 | 5 | 5 | unsorted |

✗ = study fails the 50/10 set (fewer than 10 complete patients).

- **Pass counts:**
  - Permissive 20/5: 13 studies, the same set as primary.
  - Primary 30/5: 13 studies, 222 complete patients (sum over studies). There is no cross-study
    patient overlap among them; see the HTAPP check below.
  - Stringent 50/10: 7 studies (Pelka, Joanito, Lee, Qin, Chen 2024, MUI, Uhlitz).
- **Sample level:** only Pelka changes (50 → 45). Five Pelka patients are complete only when their
  CD45+ sorted and unsorted samples from the same tumour are pooled.
- **Unsorted only:** Liu 2024 has no unsorted samples (0). Pelka keeps 45 patients.
- **Fibroblast-specific:**
  - Khaliq 2022 (3) would not support fibroblast-level analysis.
  - MUI (5) is at the threshold.
  - In Pelka, fibroblasts are only 29% of stromal cells (21 patients).

### 7-lineage coverage (patients with ≥30 cells; `lineage_coverage_primary_tumor_naive.csv`)

- Epithelial, T/NK and Myeloid are covered in almost every patient.
- B/Plasma is nearly complete.
- Fibroblast, Endothelial and Pericyte are the sparse lineages. For example, pericytes: Pelka 16/62,
  Lee 14/34, Chen 2024 7/20, Khaliq 2/16.
- The fibroblast share of stromal cells ranges from 22% (Li 2023) to 57% (Joanito). Broad "Stromal"
  scores would therefore mix different lineage compositions across studies.

### Treatment scopes

| Study | Naive | Naive + unknown | Any |
|---|---|---|---|
| HTAPP HTAN | 0 | 19 | 19 |
| Li 2023 | 9 | 9 | 19 |
| Qin 2023 | 27 | 27 | 29 |
| Chen 2024 | 19 | 19 | 20 |
| Wang 2023 Sci Adv | 0 | 0 | 5 |
| Che 2021 / Terekhanova 2023 / Ji 2024 Cancer Lett | 3 / 1 / 0 | 3 / 1 / 2 | 6 / 3 / 2 |

### HTAPP HTAN vs Pelka 2021 (`htapp_vs_pelka_fingerprint.csv`, `htapp_pelka_patient_demographics.csv`)

- **Identifiers:** no shared patient, sample, GEO or Synapse ID. HTAPP patients are `HTA1_xxx`
  (Synapse syn24181445) and Pelka patients are `Cxxx` (GEO). The ID systems differ, so this alone
  does not rule out the same patients.
- **Cell fingerprints** (exact total counts + genes detected):
  - 5.4% of HTAPP cells match some Pelka cell (control Lee 2020: 2.8%).
  - Only 0.25% match the best single Pelka sample (control 0.27%).
  - **No HTAPP sample is a re-release of a Pelka sample's cells.** This test cannot detect the same
    tissue re-processed with a different pipeline.
- **Clinical metadata:** HTAPP is 13 F / 7 M, with stage, MSI and treatment all unknown (19/20).
  Pelka is 31 F / 31 M, stages I–IV and MSI known.
- **Status:** no evidence of duplicated cells. Patient-level overlap and treatment status remain
  **unresolved** from the Atlas metadata. HTAPP HTAN stays **out of the primary analysis** as a
  treatment-unknown sensitivity cohort. Resolving it needs the HTAN clinical manifest for
  syn24181445 (not done).

## Proposed tiers (for review; not a final cohort)

- **Core:** Joanito 2022, Lee 2020, Qin 2023, and Pelka 2021 (flagged: mixed sorting).
- **Extended:** Chen 2024, Liu 2024 (mixed enrichment; absent from the unsorted-only analysis),
  MUI Innsbruck (BD Rhapsody), Uhlitz 2021, Li 2023, Qian 2020, Khaliq 2022 (low stromal; not usable
  for fibroblast-level analysis), Guo 2022, Qi 2022 (at the threshold).
- **Sensitivity only:** HTAPP HTAN (treatment unknown, possible Pelka overlap).

Core is a review order. It does not certify freedom from sampling bias.

## Outputs (`tables/v2/`; v1 kept in `tables/v1/`)

| File | Content |
|---|---|
| `study_inclusion_flow.csv` | all 54 study labels with H5AD/scope patient counts and fate |
| `study_screen_summary.csv` | per scope × study: compartment %, complete patients under 3 thresholds, sample-level, unsorted-only, fibroblast-specific |
| `sample_lineage_counts.csv.gz` | study × patient × sample × sample type × treatment × sorting class × platform, with 7-lineage and broad counts |
| `patient_lineage_counts_primary_tumor_naive.csv.gz` | patient-level counts in the primary scope |
| `lineage_coverage_primary_tumor_naive.csv` | per study: patients with ≥30 cells per lineage; fibroblast share of stroma |
| `study_design_flags.csv` | platform, sorting class, sample types, treatment, malignant vs normal epithelial cells |
| `supplemental_objects_study_level.csv` | (v1 only) heuristic lineage counts of supplemental objects |
| `htapp_vs_pelka_fingerprint.csv`, `htapp_pelka_patient_demographics.csv`, `overlap.log` | HTAPP–Pelka overlap check |
| `run_summary.json`, `run.log` | identifier checks, scope check, pass counts |

## Limitations

- The thresholds are operational and were fixed before any CytoTRACE2 result. They are not validated
  minimum sample sizes for CytoTRACE2.
- Low stromal fractions (Pelka, Chen 2024, MUI, Khaliq: 3–4%) may reflect dissociation or enrichment.
  These studies must not be used to infer true tissue composition.
- Chen 2024 pre-treatment samples may be biopsies rather than resections; this has not been checked.
- Biological interpretation of later CytoTRACE2 scores is limited to predicted developmental
  potential, not measured plasticity.
