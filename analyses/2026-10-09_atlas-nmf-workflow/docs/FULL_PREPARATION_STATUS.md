# Full preparation: first inventory checkpoint

Gate A/B/C PASS; pilot feasibility closed. Full Atlas execution HOLD.
No core algorithm modification, new synthetic test or full NMF was performed.

Scope here is the updated counts-RDS directory, NOT the complete historical
76-dataset Atlas. Existing validated manifests contain7 datasets,333 RDS and
2,171,819 cells. Counts validation is inherited from those manifests, not newly
repeated across333 objects. Dataset-level table: FULL_dataset_annotation_inventory.tsv.

| Dataset | RDS | Cells | Annotation readiness |
|---|---:|---:|---|
| GSE155953 | 4 | 19653 | Epi label exists; not a verified malignant label |
| GSE178318 | 15 | 140281 | Build lacks cell-type annotation; source annotation needed |
| GSE205506 | 40 | 324020 | Build lacks cell-type annotation; source annotation needed |
| GSE222300 | 3 | 14852 | Build lacks cell-type annotation; source annotation needed |
| GSE236581 | 169 | 975275 | MajorCellType/SubCellType exist; malignant rule not approved |
| GSE254249 | 92 | 619635 | Cancer vs Epi explicit; full sample/QC mapping still pending |
| GSE285873 | 10 | 78103 | Build lacks cell-type annotation; source annotation needed |

GSE254249 source metadata contains28984 Cancer cells and32261 Epi cells.
GSE155953 contains16872 Epi cells; these must not be silently called malignant.
GSE236581 contains174818 MajorCellType=Epi cells; epithelial identity alone does
not approve malignancy. Exact subtypes are retained in the dataset-level table.

An UNREVIEWED identity draft for333 inputs is on Argos only. Biological sample
IDs remain blank, patient IDs unknown and enabled=0; it intentionally fails
the execution identity contract until reviewed. Source IDs are provisional
manifest-row indices and must be frozen with the final plan. No mapping is
claimed reviewed and no patient counts are inferred from sample names.

Argos preparation root:
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_full_inventory_20261009

```bash
/home/zz950/softwares/miniforge3/envs/argos-codex/bin/python audit_full_inventory.py \
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/external/oncofetal_dataset_inventory_v2_2026-10-07 \
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_full_inventory_20261009
```

Parsing was corrected for R whitespace-separated metadata and an unlabelled
row.names field; field count and category cardinality are now checked. The first
malformed temporary output was replaced before publication, not used as evidence.

Next: review existing original annotation resources for the four unlabeled
datasets, resolve epithelial vs malignant labels in the two Epi-only sources,
build source-backed sample/patient mappings, and reconcile with legacy Atlas
coverage. No dataset is dropped or automatically approved in this checkpoint.
