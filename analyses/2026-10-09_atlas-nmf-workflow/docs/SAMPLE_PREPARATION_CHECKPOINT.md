# Sample-level preparation checkpoint

DATA PREPARATION APPROVED; FULL NMF HOLD. No algorithm changes or new NMF.

## Priority annotation inventory

- GSE254249: original group=Cancer, 28984 source-labelled cells;26 sample inputs
  have >=200 such cells. Original PatientID is retained, not guessed from names.
- GSE236581: original SubCellType=c91_Epi_Tumor,26252 source-labelled cells;27
  inputs have >=200 such cells. Original Patient field is retained. No c90_Epi_MKI67
  or all-Epi expansion. Tumor-label provenance remains review pending.
- Both combined:261 input rows,53 annotation-count candidates. These are NOT
  final post-zero-library eligible counts. Rows below200 are provisionally
  excluded; others pending. No new row is automatically approved.

Remote eligible_samples.DRAFT.tsv contains original patient source IDs,
annotation counts, conservative labels and reasons. All enabled=0, final source
and biological IDs unfrozen/blank. One unique original patient value is labelled
source_unique, not globally confirmed. The draft is not execution-ready.

## Legacy coverage

GEO family SOFT BioProject relations are joined to the deposited-data table,
not inferred from study names. GSE205506 -> PRJNA846169 -> Li_2023;
GSE236581 -> PRJNA991601 -> Chen_2024. Exact sample suffixes are then matched to
malignant inputs only. Unmatched names are NOT automatically declared new.
Dataset summary is DATA_PREP_coverage_summary.tsv. Full sample-level list remains
remote as sample_legacy_coverage.tsv. W-file existence is checked separately and
is not a complete output QC or approved biological-sample identity match.
Remaining unmatched aliases and sample naming require provenance review.

## Other five datasets

GSE155953 has original Epi annotation, not a verified malignant selector; pending.
GSE178318 supplementary contains matrix/genes/barcodes only. GSE205506,
GSE222300 and GSE285873 downloaded RAW archives contain no filenames matching
metadata/annotation/celltype/label. This is an audit of existing downloads, NOT
proof that the authors have no annotations elsewhere. Continue source recovery,
retain in inventory, do not run CNV or drop permanently.

## Reproduce and next work

```bash
/home/zz950/softwares/miniforge3/envs/argos-codex/bin/python prepare_sample_review.py \
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/external/oncofetal_dataset_inventory_v2_2026-10-07 \
/home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025 \
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_full_inventory_20261009
```

Next required items: resolve historical sample aliases/biological identity,
validate retained RDS cell counts, freeze source/sample mapping with original
patient evidence, recover external author annotation resources, and produce
one final approved/pending/excluded inventory for human review. This checkpoint
does not claim completion of the whole data-preparation gate. EXECUTE_NMF=0.
