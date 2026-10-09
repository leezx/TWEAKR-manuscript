# Final eligibility proposal

This is an intake proposal, not an execution authorization. All enabled=0,
EXECUTE_NMF=0. No QC/NMF/CNV/readability reruns, no algorithm changes.

| Dataset/category | Samples | Proposal | Reason |
|---|---:|---|---|
| GSE254249 | 26 | approved, pending final review | Author Cancer label, tumor-origin metadata, reasonable identity check |
| GSE236581 Tumor | 23 | pending | Exact c91_Epi_Tumor definition still unverified |
| GSE236581 Normal | 4 | not_approved | Normal tissue is outside current malignant main-analysis intake |

FINAL_eligibility_decision.tsv includes53 rows so excluded4 remain auditable;
49 are the remaining candidates. eligibility_proposal is a proposed outcome;
review_status remains pending_final_review for26+23. No sample is enabled.

## Three conditions

GSE254249 annotation source: original downloaded scRNA metadata distinguishes
group=Cancer from Epi. This is accepted provisionally as the author label,
not independently verified CNV ground truth. The methodological limitation
must remain in subsequent results. Original Tissue is Rectum_T in all26.

Identity review now covers ALL92 GSE254249 source sample IDs, not only the26
candidates. Each candidate has one PatientID/Tissue/SampleTimePoint tuple.
No other source sample ID shares that tuple. This is reasonable evidence of
no duplicate source input in this metadata, not proof of no unrecorded technical
replication. Cross-study identities remain unresolved and cannot be used to
claim globally independent patients. Private patient keys are not exported.

GSE236581 source Tissue confirms23 Tumor and4 Normal. Selected sample identity
tuples have no collisions, but that identity check only covers the27 candidates.
Its original c91 annotation definition is not verified, so23 remain pending.
No extra CNV or weakening of selectors is proposed.

## Commands and evidence

```bash
ROOT=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_full_inventory_20261009
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
SOURCE=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/external/oncofetal_dataset_inventory_v2_2026-10-07
"$ENV/bin/python" "$ROOT/build_eligibility_review.py" "$ROOT" "$SOURCE"
```

Inputs: existing final QC identity table, source-record audit status, original
GSE254249_scRNA_metadata.tsv.gz. Output: PUBLIC_eligibility_review.tsv on Argos,
public copy FINAL_eligibility_decision.tsv. Exit0; assertions92 source samples,
53 candidate rows, enabled0. No patient associations or source timepoints
appear in the public output. Previous21/32 reuse decisions remain frozen.

Requested review: accept26 source-annotation-qualified inputs as a separate
intake batch, leave23 pending and4 not approved. This does not authorize NMF,
execution-manifest enabling, or remote Git history changes.
