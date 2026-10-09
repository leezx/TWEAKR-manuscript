# Fig. 1B — CytoTRACE2 across CRC cellular compartments

- **Question:** How is predicted developmental potential (CytoTRACE2) distributed across epithelial,
  immune and stromal compartments of treatment-naive primary CRC, across patients and studies?
- **Figure mapping:** Figure 1B (main); Extended Data heatmap (study × compartment).
- **Date / executor / status:** 2026-10-09 / Claude Code.
  - Stage 1, contract and input validation: complete. Dataset screening and input validation are
    CLOSED; contract A2.1 and the annotation design were APPROVED (2026-10-09).
  - Validation passed: integer raw counts; 90–98% model-feature coverage per study.
  - Validation also showed large within-study depth differences between compartments, which led to
    amendment A1 (depth-matched sensitivity analysis).
  - Pilot (Joanito, Lee, Qin): COMPLETE on Argos SGE (`all.q`): 1,200 tasks, 0 failed.
    - The six-item technical report is `docs/Pilot_report.md`.
    - The final technical review on 2026-10-09 gave **GO**; all six items PASS. No A2.2 is needed.
  - Stage order after the GO:
    1. L2 harmonized annotation (started; input inventory done);
    2. annotation QC and freeze of `annotation_v1`;
    3. full 13-study CytoTRACE2 run under A2.1. It is approved but is submitted only after the L2
       freeze.
  - Interpretation constraints from the review:
    - any epithelial–stromal conclusion must be read together with the depth-matched and raw-score
      results;
    - no plasticity hierarchy may be claimed from the final-score ordering in immune cells alone.
  - L2 parameters were fixed before any computation in `docs/L2_implementation_notes.md` and
    `code/l2_config.yaml` (2026-10-09). They are under review; no L2 job has been submitted.
- **Cohort:** frozen v1 from `../2026-10-09_fig1b-dataset-screen/cohort/` (13 studies, 222 patients,
  1,003,249 cells).

## Documents

| File | Content |
|---|---|
| `docs/CytoTRACE2_contract.md` | question, claim ceiling, input, run unit, metrics, statistics, sensitivity analyses, pilot gate |

## Code

| Script | Purpose | Where it runs |
|---|---|---|
| `code/validate_inputs.py` | integer-count check, per-cell library size and detected genes, per-study gene detection for cohort cells | Argos SGE (`r4p3` Python) |
| `code/cytotrace2_gene_coverage.R` | CytoTRACE2 1.1.0 human→model gene mapping; per-study model-feature coverage | Argos (`r4p3` R, `R_LIBS=/home/zz950/softwares/R_lib_4`) |
| `code/summarise_depth.py` | median UMI, detected genes and % cells with <500 genes per study × compartment | Argos |
| `code/run_validate.sh` | SGE wrapper (`qsub -l m_mem_free=48G`, job 3654250) | Argos |
| `code/depth_targets.py` | study-specific depth target T_s (A2 rule) with cell and patient retention | Argos |
| `code/export_sample_counts.py` | per-sample raw counts (model genes) as HDF5; optional depth-matched variants (exact downsampling to T_s, seeds 1–5) | Argos SGE (`run_export.sh`) |
| `code/run_cytotrace2_sample.R` | CytoTRACE2 1.1.0 per sample: whole-sample (primary), cell-intrinsic (`preprocessData` + `predictData`), compartment-split (diagnostic) | Argos SGE array (`run_pilot_task.sh`, `-pe smp 4`) |
| `code/summarise_pilot.py` | technical pilot diagnostics (no biological contrasts) | Argos |

## Documents (A2)

| File | Content |
|---|---|
| `docs/Harmonized_annotation_plan.md` | L1/L2/L3 taxonomy, human marker panels, malignancy calls, integration/labelling/validation procedure, L2 eligibility |
| `docs/L2_implementation_notes.md` | fixed operating parameters for L2 (envs, L1 flags, scVI, Leiden, three-source consensus, infercnv thresholds, LOSO, compute plan) and open questions Q1–Q2 |
| `code/l2_config.yaml` | machine-readable copy of the L2 parameters, panels and Atlas fine → L2 crosswalk |

## Tables (`tables/input_validation/`)

| File | Content |
|---|---|
| `validate_inputs_summary.json` | integer check, zero-library cells, genes detected per study |
| `cytotrace2_model_gene_coverage_by_study.csv` | model features (14,271) covered by detected genes, per study |
| `cytotrace2_atlas_gene_mapping.tsv.gz` | Atlas gene → CytoTRACE2 model gene mapping |
| `depth_by_study_compartment.csv` | depth by study × compartment |

## Pilot tables (`tables/pilot/`)

These are the light outputs of `code/summarise_pilot.py` and `code/run_summarise.sh`, SGE job
3654471. The report that explains them is `docs/Pilot_report.md`.

Per-cell QC (`cohort_cell_qc.tsv.gz`, 13 MB) and per-study gene detection stay on Argos.

Argos run directory: `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/`
(per-cell outputs stay there).
