# Identity crosswalk and historical reuse review

53-sample QC is CLOSED/PASS following human review of dd03455. No QC rerun,
new NMF, CNV, core algorithm edit or scheduler submission was performed.
EXECUTE_NMF=0. All sample intake/reuse authorizations remain disabled.

## Source identity

The complete crosswalk stays PRIVATE on Argos. PUBLIC_sample_review.tsv contains
only dataset/sample codes, review statuses and enabled=0. It excludes original
and anonymous patient IDs, within-patient linkage, group sizes, biological
identity keys, and per-sample tissue/timepoint values. The approved aggregate
statistic is39 source-local patient groups among53 samples. Cross-study identity
and technical replicates remain unverified; no sample-name inference is used.

## Normal tissue warning

| Sample | Tissue review conclusion | Target cells |
|---|---|---:|
| CRC02-N-II | Normal: not approved | 549 |
| CRC03-N-III | Normal: not approved | 313 |
| CRC05-N-II | Normal: not approved | 231 |
| CRC16-N-II | Normal: not approved | 269 |

These are actual metadata values, not assumptions from the letter N. Their
cells retain the author-provided c91_Epi_Tumor label. This does not establish
malignant cells in adjacent normal tissue; no CNV-based explanation is claimed.
These4 inputs are not approved for the main malignant analysis. Remaining49
require final eligibility review; they are not automatically approved.

[Original GEO design](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE236581)
includes tumor, adjacent normal and blood samples across longitudinal treatment.
The exact c91 annotation definition could not be independently verified from
the original article methods in this run (publisher access failed).

## Historical artifacts:21 actual reads

All21 W/H/model RDS and marker CSV artifacts were read. W/H dimensions match,
values finite and nonnegative in21/21. Twenty have gene/cell names and nonempty
marker tables. CRC02-T-I K5 has no W gene names, no H cell names and0 marker
rows (170 cells); it cannot supply an identity-verifiable gene program.

Historical H cell counts differ from current target counts in ALL21 candidates.
Thus current inputs cannot be considered identical to those historical matrices.
The old preparation script selects cell_type_study via regex
`(Tumor|Cancer|Malignant)|^Tu\\d|tumor_epithelial`; the current GSE236581 selector
is exact `SubCellType=c91_Epi_Tumor`. Cell-barcode equivalence has NOT been
established. Study/name correspondence alone is insufficient.

The old results may be archived as historical reference, with these limitations,
but are NOT approved as substitute outputs for the current samples. They only
cover K5, not K4-9. Current-input K4-9 tasks remain uncomputed/unapproved; this
report does not request or launch them. The other32 samples remain unresolved
for historical coverage, not proven missing.

## Reproducible read-only commands

```bash
ROOT=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_full_inventory_20261009
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
LEGACY=/home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/NMF
"$ENV/bin/python" "$ROOT/review_identity_reuse.py" "$ROOT" "$LEGACY"
R_LIBS_USER="$ENV/lib/R/user-library" "$ENV/bin/Rscript" "$ROOT/review_legacy_readability.R" "$ROOT/legacy_readability_inputs.tsv" "$ROOT/PUBLIC_legacy_readability.tsv"
```

Both commands completed exit0; R ended READABILITY_COMPLETE. Source input:
existing final_sample_inventory.DRAFT.tsv and historical_sample_coverage.tsv.
Public outputs: PUBLIC_sample_review.tsv and LEGACY_readability_review.tsv.
Full mapping and artifact paths remain remote. Open items: author annotation
definition, technical-replicate crosswalk and independent cross-study identities.

## Publication privacy audit

The unpushed23c7de6 crosswalk commit is not an ancestor of this replacement
publication commit. Earlier already-published cohort_identity_mapping.tsv
contained two original study PatientIDs; the current file is now status-only.
Prior published versions remain in Git history. Complete historical removal
requires separately authorized coordinated history rewrite/force-push; none
was performed. Current redaction cannot remove existing clones/hosting caches.
