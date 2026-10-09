# Fig. 1B L2 annotation — implementation notes (parameters fixed before any result)

Written on 2026-10-09, after the pilot GO and **before any L2 computation was run**. This document turns
`Harmonized_annotation_plan.md` (design, APPROVED) into fixed operating parameters. Every number here is
set before labels, clusters, CNV scores or CytoTRACE2 scores are seen. Numeric parameters live in
`code/l2_config.yaml`, which is the machine-readable copy of this document.

Rules that carry over unchanged:
- No CytoTRACE2 output is read by any step of the annotation.
- Atlas and study labels are kept as new columns and never overwritten.
- After a result is seen, parameters are not re-tuned. Any change goes in as a dated amendment with its
  reason, and the original output is kept.

## 0. Pre-run facts that shape the implementation

| Fact (checked 2026-10-09) | Consequence |
|---|---|
| `r4p3` env: `import scvi` fails (pyro asserts torch 1.x; env has torch 2.0.0) | scVI runs in `scvi-env` (scvi-tools 1.4.1, torch 2.6.0, Python 3.13). All other steps stay in `r4p3` (scanpy 1.9.8, leidenalg, harmonypy, scikit-learn 0.24.2; R infercnv 1.14.0). Neither env is modified. This replaces "scVI in `r4p3`" in the plan. |
| `scvi-env` has no `scikit-misc` | HVG selection uses scanpy `flavor="seurat"` on log-normalized data, not `seurat_v3`. |
| Argos has no GPU; all.q nodes: 8 × 32 cores, 2 × 80 cores | scVI trains on CPU; all jobs go through SGE `all.q`. |
| Cohort lineage (`broad`): Epithelial 285,703; Immune 619,337; Stromal 95,886; Other 2,323 (all Atlas "Schwann cell") | Three lineage objects. Other is outside L1 and is counted, not annotated (the plan excludes Schwann/glial from L2). |
| Atlas fine labels of cohort epithelial cells: `Cancer *` for all except Enteroendocrine (484) and Tuft (1,313) | Under the approved malignancy rule, "High-confidence non-malignant" needs an Atlas normal epithelial type, so it can only arise from these 1,797 cells. CNV-low cells with a `Cancer *` label become Uncertain. The rule is **not** changed here; see Open question Q1. |
| Platforms: 10x 3′ (486,789), 10x 5′ (317,714), DNBelab C4 (150,699), BD Rhapsody (48,047) | All are UMI-based. infercnv uses `cutoff = 0.1` for all of them. |

## 1. Inputs

- Counts: Atlas `layers/counts` from `final_crc_atlas-adata.count.only.h5ad`, cohort v1 cells only.
- Cohort: `fig1b_cohort_cells_v1.tsv.gz` (`cell_id, study_id, patient_id, sample_id, platform, broad, ...`).
- Atlas labels, read from H5AD `obs`: `atlas_cell_type_fine`, `atlas_cell_type_middle`, `cell_type_study`.
- Independent marker lineage: `atlas_major_lineage_20261009/<study>_lineage.tsv.gz` (`Lineage_cell`, `Lineage_margin`).
- Gene positions: H5AD `var` columns `Chromosome`, `Start`, `End`.
- Normalization for all marker scores: counts per 10,000, then `log1p`.

## 2. L1 QC flags (flag, never reassign)

**F1, marker contradiction (per cell).** A cell is flagged when it carries a foreign lineage panel,
defined as ≥2 genes of a foreign panel each with ≥2 UMI. Panels:

| Panel | Genes | Foreign to |
|---|---|---|
| Epithelial | EPCAM, KRT8, KRT18, KRT19, CDH1 | Immune, Stromal |
| T/NK | CD3D, CD3E, CD2, TRAC, NKG7 | Epithelial, Stromal |
| Myeloid | LYZ, C1QA, C1QB, CD68, CD14 | Epithelial, Stromal |
| B/Plasma | MS4A1, CD79A, JCHAIN, MZB1 | Epithelial, Stromal |
| Fibroblast | COL1A1, COL1A2, DCN, LUM | Epithelial, Immune |
| Endothelial | PECAM1, VWF, CDH5, EMCN | Epithelial, Immune |
| Mural | RGS5, NOTCH3, PDGFRB, MYH11 | Epithelial, Immune |

Panels within the same lineage are not foreign to each other. For example, a T-cell panel in an Immune
cell is not a conflict.

**F2, cluster dominated by another lineage.** After integration and Leiden at resolution 1.0 (section 4),
all cells of a cluster are flagged when >50% of its cells have an independent `Lineage_cell` that is a
different one of the three lineages.

- Flagged cells (F1 or F2) get `celltype_L2 = "L1_flagged"` and are excluded from L2 labelling and from
  LOSO. They are counted per study × lineage in the QC report.
- The rates are reported as they come out. The thresholds are not re-tuned.
- SOLO doublet probability is reported per study × L2 as QC only. It is not an exclusion rule, because the
  approved plan did not include one.
- Cross-check: an agreement table of `broad` vs `Lineage_cell` per study.

## 3. Integration (one object per lineage; used only for clustering and label transfer)

- Cells: non-F1 cells of the lineage. F2 is applied after clustering.
- HVG: 3,000 genes, scanpy `highly_variable_genes(flavor="seurat", batch_key="study_id")` on log1p CP10k.
  Before selection, remove MT-, RPL/RPS, HBA/HBB genes, and (Immune only) TR[ABDG][VJ] and IG[HKL][VJ]
  genes. All L2 and L1 panel genes are then forced in.
- scVI (`scvi-env`) on raw counts of these genes:
  - `batch_key = sample_id`, `categorical_covariate_keys = [study_id]`;
  - `n_latent = 30`, `n_layers = 2`, `n_hidden = 128`, `gene_likelihood = "nb"`;
  - `max_epochs = min(400, round(20000 / n_cells × 400))` (scvi default rule), with early stopping on;
  - seed 0, `torch.set_num_threads(NSLOTS)`.
- Harmony check (`r4p3`): 50 PCs of scaled log1p CP10k on the same HVGs, harmonypy with
  `key = sample_id`, `theta = 2`, seed 0. Used only for the comparison in section 7. Not used for labels.

## 4. Clustering

- kNN graph on the scVI latent space, `n_neighbors = 15`.
- Leiden at resolutions 0.5, 1.0, 1.5 and 2.0, seed 0.
- **Resolution 1.0 is the labelling resolution.** The others are used only for the stability report.

## 5. L2 labelling (three evidence sources)

Panels are those in `Harmonized_annotation_plan.md`. The combination rules become negative genes:

| L2 | Negative genes (score subtracted) |
|---|---|
| CD4 T | CD8A, CD8B |
| NK | CD3D, CD3E |
| Pericyte | MYH11 |

**(c) Per-cell marker score.**
- For each panel, score = scanpy `score_genes` (`ctrl_size = 50`, `n_bins = 25`, seed 0), computed
  **within each study** on the lineage object, minus the score of its negative genes when it has any.
- The call is the top panel when its score is >0.10 and exceeds the second panel by ≥0.10. Otherwise there
  is no call.

**(a) Cluster marker score.**
- For each Leiden 1.0 cluster, take the mean per-cell score of every panel.
- The call uses the same rule (top >0.10, margin ≥0.10). All cells of the cluster carry the call.

**(b) Label transfer from the Atlas.**
- Atlas fine labels are mapped to L2 by the fixed crosswalk in `code/l2_config.yaml` (section
  `atlas_fine_to_L2`). Labels with no L2 counterpart map to `null` and cast no vote: Eosinophil, NKT,
  T cell γδ, myeloid and granulocyte progenitors.
- For each cell, a kNN vote (k = 30, scVI latent, the cell itself excluded) over neighbours with a non-null
  mapped label.
- The call is the majority label when its share is ≥0.60. Otherwise there is no call.

**Consensus (as approved):**
- high: (a) and (c) agree;
- medium: any two of (a), (b), (c) agree;
- low: otherwise. Low cells get `celltype_L2 = Unclassified <lineage>`.

`annotation_method` records which sources agreed, for example `a+c`, `a+b`, `b+c`, `a+b+c`.

**Epithelial order.**
1. Malignancy is called first (section 6).
2. High-confidence malignant cells get `celltype_L2 = Malignant epithelial`.
3. High-confidence non-malignant cells are labelled with the normal epithelial panels by the consensus rule
   above.
4. Uncertain cells get `celltype_L2 = Epithelial, malignancy uncertain` and are excluded from all L2
   estimates.

## 6. Malignancy calls (epithelial)

**infercnv** (R, `r4p3`, infercnv 1.14.0), one run per patient:
- Observations: all non-flagged epithelial cells of the patient.
- Reference: the patient's non-flagged immune and stromal cells, randomly subsampled (seed 0) to at most
  1,500, split half immune and half stromal where possible.
  - A patient with <100 reference cells is "CNV not assessable", and all its epithelial cells are
    Uncertain.
- Genes: chromosomes 1–22 only, ordered by Atlas `var` positions.
- Run settings: `cutoff = 0.1`, `cluster_by_groups = TRUE`, `denoise = TRUE`, `HMM = FALSE`,
  `window_length = 101`, `analysis_mode = "samples"`, `num_threads = 8`.

**Per-cell metrics** from the infercnv output matrix:
- CNV score = mean of (x − 1)² over genes.
- CNV correlation = Pearson r with the mean profile of the top 5% of the patient's epithelial cells by CNV
  score.

The patient's reference cells, taken from the same output, give the null distribution:
- CNV-high: score > reference P99 **and** correlation > reference P99;
- CNV-low: score ≤ reference P95 **and** correlation ≤ reference P95;
- otherwise intermediate.

**Patient and study level:**
- Clear CNV structure: ≥20% of the patient's `Cancer *`-labelled epithelial cells are CNV-high.
- Poor study sensitivity: <50% of a study's assessable patients have clear CNV structure. All calls in such
  a study are Uncertain.

**Normal-marker coherence:** the per-cell call (c) on the normal epithelial panels is a normal type with
the margin rule met.

**`malignancy_confidence` (approved rule, unchanged):**
- High-confidence malignant: Atlas `Cancer *` label, CNV-high, and a patient with clear CNV structure.
- High-confidence non-malignant: Atlas normal epithelial label, CNV-low, coherent normal markers, and a
  patient with clear CNV structure.
- Uncertain: everything else.

Reported per study and per patient: CNV detection rate, share of Uncertain cells, and assessable or not.

## 7. Validation (light tables)

- Confusion tables of consensus L2 vs `cell_type_study` and vs `atlas_cell_type_fine`, per study.
- Marker specificity per L2 × study: detection rate of each panel gene in the type vs the rest of the
  lineage.
- Patient and study coverage per L2, with eligibility (≥30 cells per patient; main panel when ≥5 eligible
  patients in ≥3 studies).
- Confidence distribution (high / medium / low) per study × lineage.
- Stability:
  - share of cells whose consensus is unchanged when (a) uses Leiden 0.5 or 2.0 instead of 1.0;
  - ARI between Leiden 1.0 clusterings on the scVI and Harmony embeddings.

## 8. Leave-one-study-out (LOSO)

- Per lineage and per held-out study *s*: a kNN classifier (k = 15, distance-weighted, scVI latent) is
  trained on high and medium consensus cells from the other 12 studies and predicts the high and medium
  cells of *s*.
- Recovery of L2 type *t* in *s* is the recall, computed when *s* has ≥30 cells of *t*.
- *t* is stably recovered in *s* when recall ≥0.60.
- Decision per L2 type:
  - recovered in ≥3 studies: pan-CRC consensus type;
  - recovered in exactly 2 studies: kept, but Extended Data only;
  - recovered in ≤1 study: merged into `Unclassified <lineage>` and listed as study-specific.
- Limitation: the scVI latent space is trained on all studies, so LOSO tests label reproducibility, not
  embedding generalization.

## 9. L3 in `annotation_v1`

L3 does not gate Fig. 1B.
- In v1, L3 is stored as continuous programme scores (per-cell `score_genes`, within study):
  - the malignant programmes in the plan, including revCSC from `genesets/revCSC.human.gmt` (32 genes);
  - Treg, exhaustion, naive/memory, myCAF-like, iCAF-like and lymphatic panels.
- The only categorical L3 state is `Cycling`: proliferation score (MKI67, TOP2A, UBE2C, CDK1) >0.50.
- Other categorical L3 states are deferred to a later version.

## 10. Compute plan (Argos SGE `all.q`)

Run root: `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/l2_annotation/`
(single root; per-cell outputs stay there).

| Step | Env | Job shape |
|---|---|---|
| 1. Build lineage objects, F1 flags, L1 cross-check | `r4p3` | 1 job, 8 slots |
| 2. scVI per lineage | `scvi-env` | array of 3, 16–32 slots |
| 3. infercnv per patient | `r4p3` R | array of 222, 8 slots (parallel with step 2) |
| 4. Clustering, F2, labelling, Harmony check, LOSO per lineage | `r4p3` | array of 3 |
| 5. Malignancy calls, merge, `annotation_v1.tsv.gz` + SHA256, light tables | `r4p3` | 1 job |

The freeze happens after user and reviewer review of the step 5 tables, before any CytoTRACE2 result is
read by L2.

## Open questions for review (no change made)

- **Q1. Non-malignant epithelial cells are almost unreachable by design.** Every cohort epithelial cell
  except 1,797 EEC/tuft cells carries an Atlas `Cancer *` label. The approved rule therefore puts
  CNV-low, normal-marker-coherent `Cancer *` cells into Uncertain. This is accepted as the primary
  analysis.
  - Should a pre-declared sensitivity analysis be added that counts such cells as non-malignant, in
    patients with clear CNV structure?
  - Not adding it is also acceptable. The cohort is primary tumour only, and the main contrasts are by
    compartment.
- **Q2.** Is v1 with continuous L3 scores (only `Cycling` categorical) acceptable for the freeze?
