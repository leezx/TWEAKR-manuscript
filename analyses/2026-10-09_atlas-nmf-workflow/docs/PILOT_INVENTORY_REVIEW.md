# Gate B pilot candidate packet

Gate A remains PASS. Only read-only inventory was performed; NMF NOT STARTED.

The two review materials are pilot_dataset_inventory.tsv and
cohort_identity_mapping.tsv. Candidate dataset: GSE254249 (project DS-010,
REF-007), original source metadata, baseline rectal tumor samples:

| Sample | All cells | group=Cancer | After zero-library check | Source PatientID |
|---|---:|---:|---:|---|
| CRC23_tissue | 3635 | 506 | 506 | RC23 |
| CRC13_tissue | 4385 | 514 | 514 | RC13 |

Both actual RDS objects contain RNA counts, sample_id matching Ident and the
source filename, Tissue=Rectum_T and SampleTimePoint=BL. Counts are finite,
nonnegative and integer-like. Cancer and Epi are separate source annotations;
only group=Cancer is proposed. This is not a new marker-based malignancy call.

Patient IDs are study-prefixed and confirmed against original PatientID within
this study. Cross-study duplicate review remains pending. These two different
patients and samples have no technical duplicates in the proposed pilot subset;
this does not establish absence of duplication across the complete Atlas.
Source IDs are reserved for plan rows 1 and 2 in this order; reordering a future
plan must regenerate the mapping. Biological sample IDs are explicit, not
automatically derived at NMF execution time.

## Evidence and limits

Source metadata: Argos external/oncofetal_dataset_inventory_v2_2026-10-07/
GSE254249/supplementary/GSE254249_scRNA_metadata.tsv.gz.
Source GEO record: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE254249.
The downloaded family SOFT identifies PMID 41202810 and DOI
10.1016/j.ccell.2025.10.008. The web page was blocked by CAPTCHA; the local source
record and actual RDS were inspected. The precise original method for calling
Cancer (e.g. CNV evidence) has not been rechecked here and remains a review item.
All table review_status fields are pending, not approved.

## Reproduction

```bash
R_LIBS_USER=/home/zz950/softwares/miniforge3/envs/argos-codex/lib/R/user-library \
/home/zz950/softwares/miniforge3/envs/argos-codex/bin/Rscript \
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_gate_b_inventory_20261009/inventory_pilot_annotations.R \
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/external/oncofetal_dataset_inventory_v2_2026-10-07/seurat_counts_rds \
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_gate_b_inventory_20261009
```

Initial inventory used defunct GetAssayData(slot=) and stopped before completing;
the read-only helper was corrected to LayerData(layer=counts) and reran successfully.
No core NMF algorithm changed. No matrix normalization or factorization occurred.
Execution protection remains HOLD_FOR_REVIEW / EXECUTE_NMF=0.
