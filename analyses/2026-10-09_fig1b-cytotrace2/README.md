# Fig. 1B — CytoTRACE2 across CRC cellular compartments

- **Question:** How is predicted developmental potential (CytoTRACE2) distributed across epithelial,
  immune and stromal compartments of treatment-naive primary CRC, across patients and studies?
- **Figure mapping:** Figure 1B (main); Extended Data heatmap (study × compartment).
- **Date / executor / status:** 2026-10-09 / Claude Code.
  - Stage 1, contract and input validation: complete, **pending review**.
  - Validation passed: integer raw counts; 90–98% model-feature coverage per study.
  - Validation also showed large within-study depth differences between compartments, which led to
    amendment A1 (depth-matched sensitivity analysis).
  - Pilot (Joanito, Lee, Qin): not started; needs approval of the contract.
  - Full run: not started.
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

## Tables (`tables/input_validation/`)

| File | Content |
|---|---|
| `validate_inputs_summary.json` | integer check, zero-library cells, genes detected per study |
| `cytotrace2_model_gene_coverage_by_study.csv` | model features (14,271) covered by detected genes, per study |
| `cytotrace2_atlas_gene_mapping.tsv.gz` | Atlas gene → CytoTRACE2 model gene mapping |
| `depth_by_study_compartment.csv` | depth by study × compartment |

Per-cell QC (`cohort_cell_qc.tsv.gz`, 13 MB) and per-study gene detection stay on Argos.

Argos run directory: `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/`
(per-cell outputs stay there).
