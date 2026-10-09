# CRC Atlas NMF workflow refresh

## Status

`HOLD_FOR_REVIEW`. This change packages and audits the workflow only. It does
not inspect the biological content of the new Seurat objects, submit SGE jobs,
or create NMF results.

## Question and objective

The updated Atlas candidate objects are stored as counts-only Seurat RDS files
on Argos. Before running any new analysis, this directory provides a reviewed,
versioned workflow that can:

1. inventory each RDS without copying it into Git;
2. compare represented datasets with the legacy CRC Atlas NMF run;
3. prepare one non-negative, gene-centred expression matrix per eligible sample;
4. run multiple NMF ranks with deterministic seeds;
5. export both non-redundant and repeated top-gene definitions; and
6. fail validation when an approved dataset lacks an NMF result.

## Scope and provenance

- Figure: Figure 1, unbiased CRC epithelial-state analysis.
- Dataset ledger: `DS-001` for the existing CRC Atlas; `DS-002`-`DS-012` for
  the v2 candidate inventory.
- New input root (read-only):
  `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/external/oncofetal_dataset_inventory_v2_2026-10-07/seurat_counts_rds/`
- Legacy analysis root (read-only):
  `/home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/NMF/`
- Proposed new heavy output root:
  `/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/atlas_nmf_refresh_20261009/`
- Argos environment:
  `/home/zz950/softwares/miniforge3/envs/argos-codex`
- Upstream method/code reference:
  `navinlabcode/tnbc-chemo`, audited at commit
  `8b8e816a49881bd6a2cd6790a574fd331aa65ab4` on 2026-10-09.

The upstream repository does not expose a license file at the audited commit.
Its source is therefore not vendored here. The code in this directory is a
clean project implementation of the documented algorithm and records the
upstream repository as methodological provenance.

## Method summary

For each approved malignant/epithelial sample:

```text
raw counts (gene x cell)
  -> library-size normalization to 10,000 counts per cell
  -> log1p
  -> gene-wise mean centring across cells
  -> truncate negative values to zero
  -> sparse gc.NonNegCenterMat.rds
  -> RcppML NMF for each approved rank
  -> W/H matrices, factor assignments, reconstruction error and markers
```

The default review configuration proposes ranks 5-10 but does not freeze them.
Ranks, cell filters, metadata columns and dataset aliases must be approved in
`config/dataset_plan.tsv` before execution.

## Directory map

- `code/00_inventory_seurat_rds.R`: read-only RDS inventory and input QA.
- `code/01_compare_legacy_coverage.py`: compare new datasets with legacy NMF.
- `code/02_prepare_seurat_nmf.R`: counts-to-NMF matrix preprocessing.
- `code/03_run_fastnmf.R`: deterministic NMF and marker export.
- `code/04_build_nmf_tasks.py`: expand prepared matrices across ranks.
- `code/05_validate_nmf_outputs.py`: sample/rank and dataset-level hard QA.
- `code/qsub_prepare_array.sh`: SGE worker for preprocessing.
- `code/qsub_nmf_array.sh`: SGE worker for NMF.
- `code/submit_reviewed_workflow.sh`: guarded submission entry point.
- `config/workflow.env.example`: paths and parameters, with execution disabled.
- `config/dataset_plan.template.tsv`: manually reviewed dataset/RDS contract.
- `docs/METHOD_CONTRACT.md`: frozen assumptions and review gates.
- `docs/REVIEW_CHECKLIST.md`: decisions required before running.
- `docs/UPSTREAM_PROVENANCE.md`: relation to the historical workflow.
- `manifests/paths.tsv`: lightweight path registry; no data objects.
- `manifests/historical_script_checksums.tsv`: checksums of audited Argos scripts.

## Proposed commands after approval

These commands are documentation only while `EXECUTE_NMF=0`.

```bash
conda activate /home/zz950/softwares/miniforge3/envs/argos-codex
cd /path/to/this/analysis/directory

Rscript code/00_inventory_seurat_rds.R \
  "$RDS_ROOT" "$RUN_ROOT/manifests/seurat_rds_inventory.tsv"

python code/01_compare_legacy_coverage.py \
  --inventory "$RUN_ROOT/manifests/seurat_rds_inventory.tsv" \
  --legacy-manifest "$LEGACY_NMF_MANIFEST" \
  --output "$RUN_ROOT/manifests/nmf_dataset_coverage.tsv"

# Review and complete config/dataset_plan.tsv before either submission.
bash code/submit_reviewed_workflow.sh prepare config/workflow.env
bash code/submit_reviewed_workflow.sh nmf config/workflow.env

python code/05_validate_nmf_outputs.py \
  --plan config/dataset_plan.tsv \
  --tasks "$NMF_TASKS" \
  --ranks "$RANKS" \
  --output "$RUN_ROOT/manifests/nmf_output_validation.tsv"
```

## Claim ceiling

This PR establishes reproducible code and an execution contract only. It does
not show that any new dataset is eligible, absent from the old run, malignant,
successfully factorized, or biologically concordant with the existing 21 MPs.
Those claims require the subsequent audited run and separate review.

## Review status

- Branch: `analysis/20261009-atlas-nmf-workflow`
- Pull request: https://github.com/leezx/TWEAKR-manuscript/pull/1
- Analysis execution: not started
- User approval required before changing `EXECUTE_NMF=1`
