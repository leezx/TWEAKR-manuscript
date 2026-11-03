# Final sample preparation review

DATA PREPARATION ONLY. EXECUTE_NMF=0. No NMF, CNV, normalization or scheduler
tasks launched. Core algorithms unchanged.

| Dataset | Actual RDS inputs | Retained target cells | Zero libraries | QC |
|---|---:|---:|---:|---|
| GSE236581 | 27 | 20,412 | 0 | 27/27 PASS |
| GSE254249 | 26 | 28,645 | 0 | 26/26 PASS |
| Total | 53 | 49,057 | 0 | 53/53 PASS |

Each RNA counts layer was actually read: finite/nonnegative/integer counts,
post-zero-library >=200 cells, source counts and sample Ident/sample_id match.
Only c91_Epi_Tumor and group=Cancer were selected. All inputs had one nonempty
study-provided Patient/PatientID among retained cells; this establishes only
source-local identity, not independent cross-study patient uniqueness.

Complete mapping stays on Argos in final_sample_inventory.DRAFT.tsv. Public
FINAL_sample_QC.tsv excludes patient identifiers, cell IDs and internal paths.
All53 remain pending/enabled0; automated QC is not intake authorization.
Technical-library equivalence and cross-study duplicates remain review items.

## Historical coverage correction

Legacy fastnmf_rds_manifest.tsv has only one data row; it cannot establish
complete coverage. Previous zero-match evidence is superseded. Audit now uses
fastnmf_tasks/bucket_master.tsv and actual fastnmf_batch directories.

21/53 have candidate task-name matches and all required files present:
W.matrix.rds, H.matrix.rds, fastNMF_result_object.rds, deliver.nmf_markers.csv.
These GSE236581/Chen_2024 matches use hyphen-to-underscore correspondence;
biological identity still needs source crosswalk. K5 files do not establish
completion of the current K4-9 workflow. File existence does not establish
readability, nonempty markers, equivalent cells or output reusability.

32/53 are unmatched/unverified, not proven absent historically. All53 reuse
decisions remain unresolved. FINAL_historical_sample_coverage.tsv keeps name
matching, file status, biological identity and reuse separate.

## Commands and outputs

Executed on Argos:

```bash
ROOT=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_full_inventory_20261009
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
RDS=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/external/oncofetal_dataset_inventory_v2_2026-10-07/seurat_counts_rds
R_LIBS_USER="$ENV/lib/R/user-library" "$ENV/bin/Rscript" "$ROOT/qc_candidate_rds.R" "$ROOT/eligible_samples.DRAFT.tsv" "$RDS" "$ROOT" > "$ROOT/QC_53.log" 2>&1
"$ENV/bin/python" "$ROOT/export_preparation_review.py" "$ROOT"
"$ENV/bin/python" "$ROOT/audit_legacy_samples.py" "$ROOT" /home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/NMF
```

Historical audit code: code/audit_legacy_samples.py. Source inputs: candidate
TSV, legacy task master and batch filesystem. QC log ended with
`QC_COMPLETE; all execution enabled=0`, exit0. Export asserts53 QC rows,
53 coverage rows and all QC flags0. Full log/mapping remain remote.

Next review concerns source identity and sample eligibility, not algorithms.
Other cohorts still require original annotation recovery; absence in current
downloads does not prove author annotations unavailable elsewhere.
