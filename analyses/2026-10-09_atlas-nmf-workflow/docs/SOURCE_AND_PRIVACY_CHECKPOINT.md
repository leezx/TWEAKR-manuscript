# Source identity and historical privacy checkpoint

Scope: read existing source SOFT and identity tables, no repeated counts QC,
NMF/CNV, readability rerun or remote history rewrite. EXECUTE_NMF=0.

## Source identity evidence

All53 candidates match one original GEO sample record:27/27 GSE236581 and
26/26 GSE254249. Four Normal inputs remain not approved;49 require final intake
review. Unique source-record matching improves traceability but does not prove
absence of technical duplicates or cross-study patient independence.

GSE254249 uses exact source sample titles. GSE236581 joins source metadata
Patient with the source sample suffix to source SOFT title; Patient is never
derived from a CRC name. Matches remain candidates, not approved frozen
biological equivalence. The private join table contains source accession and
characteristics, stays on Argos with mode600. The public status table exposes
only match counts/statuses, not patient linkage or source clinical fields.

The original GSE236581 article methods remain inaccessible (publisher403).
The precise c91_Epi_Tumor definition is still unverified. Do not equate the
cluster name with independently confirmed malignancy. Source design evidence
does not resolve that annotation question. No extra CNV is requested.

## Frozen historical reuse decisions

21 historical K5 outputs: direct_reuse_not_approved; historical reference only.
32 other candidates: coverage_unresolved; no assertion of missing results.
No additional old-output readability check is needed. The decisions do not
authorize current-input K4-9 execution. All enabled flags remain0.

## Limited historical privacy risk assessment

The original published cohort_identity_mapping.tsv was introduced in e2f3200
and current fields removed in549aabb. It exposed two study-local patient
codes with sample identity linkage. These codes are present in existing
author-provided public GSE254249 metadata; they are not names, hospital record
numbers or newly obtained clinical identifiers. Their public source does NOT
authorize unrestricted linkage disclosure or establish institutional compliance.

Current public files are redacted. Old Git objects remain reachable through
published history. Clone/cache exposure and institution-specific rules have not
been assessed; historical privacy is OPEN, not PASS. No forced push, repository
visibility change or assurance of erasure is made. A human data-governance
decision is required before coordinated historical remediation.

## Commands and evidence

```bash
ROOT=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_full_inventory_20261009
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
SOURCE=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/external/oncofetal_dataset_inventory_v2_2026-10-07
"$ENV/bin/python" "$ROOT/audit_source_identity.py" "$ROOT" "$SOURCE"
```

Inputs: existing53-input identity table and two downloaded family.soft.gz files.
Outputs: PRIVATE_source_identity.tsv (Argos only,600) and
PUBLIC_source_identity_status.tsv (public copy SOURCE_identity_status.tsv).
Exit0; 169 and92 source sample records parsed, 53 unique candidates found.
Private full identity draft and prior private linkage table permissions were
also restricted to600. Git path history and pickaxe locate the two revisions;
no raw patient values are reproduced here.

Outstanding: original annotation definition and technical-replicate evidence
for final49 intake, cross-study identities unresolved, governance decision for
history risk. No sample is automatically approved by this checkpoint.
