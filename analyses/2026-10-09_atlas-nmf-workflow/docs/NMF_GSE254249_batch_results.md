# GSE254249 batch results

Date: 2026-10-10. DS-010; WL-20261010-001.

| Bucket | Samples | Completed NMF tasks | Validation failures |
| --- | ---: | ---: | ---: |
| 1 | 5 | 30 | 0 |
| 2 | 5 | 30 | 0 |
| 3 | 4 | 24 | 0 |
| 4 | 4 | 24 | 0 |
| 5 | 4 | 24 | 0 |
| 6 | 4 | 24 | 0 |
| Total | 26 | 156 | 0 |

K=4-9 produces an expected 1014 raw GEPs (26 x 39). Reviewed robust filtering retained 170 GEPs. Reviewed complete-link MP discovery produced 23 MPs. Both downstream commands exited successfully. Six BUCKET_COMPLETE flags and per-bucket validation tables were checked. Task output completeness is not an independent convergence proof.

Source IDs were local row indices within each bucket. The aggregation wrapper namespaces them by bucket, checks sample identity against the corresponding private plan row, and writes a private cohort mapping before invoking the unchanged 06/07 algorithms. Patient linkage, robust program membership and MP JSON remain on Argos, mode600.

Run root: /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_GSE254249_26_20261009

Outputs: bucket_1..6/validation.tsv, bucket_summary.tsv, tasks.all.tsv, cohort.private.tsv, robust.tsv, MPs.json. Initial job3654661 failed before NMF because of wrapper field mismatch; corrected job3654663 completed. Original scheduler error logs retained.

Aggregation command:
```bash
/home/zz950/softwares/miniforge3/envs/argos-codex/bin/python /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_GSE254249_26_20261009/aggregate.py
```

This is one-dataset MP discovery, not full Atlas analysis. No mapping to historical M01-M21, biological annotation or cross-dataset recurrence is established. GSE236581's 23 pending and four Normal samples were not included. Next: sanitized MP support/consensus summaries and results review, without reopening the algorithm gate.

## Independent summary export check

All 156 repeated top50 output tables were read; each contained exactly K unique factors. Observed raw factor count is therefore 1014, not just the expected count. All 23 MPs have 50 consensus genes (1150 rows). Exported summary contains only aggregate support counts, similarity and fractions; it contains no patient identifiers, sample memberships or program identity keys. Complete consensus genes remain local/Argos and are not included in the public PR update.

M01 supports 23 of 26 samples (88.46%), with mean Jaccard 0.4941. This ID is local to this batch, not the historical Atlas M01. Patient support uses source-local confirmed identities; no cross-study independence claim is made.
