# Actual-code review response A3

Status: HOLD_FOR_REVIEW. No real-data pilot or full NMF has run.

## P0 repairs

- 06 is now the sole robust-filtering entry point; 07 accepts only stage=robust
  and does not apply recurrence filtering again. A subprocess end-to-end test
  proves the two retained, rank-deduplicated GEPs survive into one MP.
- A reviewed cohort TSV is mandatory for both steps. Identity fields are
  dataset_id, source_id, sample_id, biological_sample_id, patient_id,
  patient_id_status. No identity is inferred from filenames. Biological sample
  IDs and confirmed patient IDs must be globally canonical, including reviewed
  cross-study duplicates. Technical libraries share a biological sample ID.
- Within-rank recurrence uses (dataset_id, biological_sample_id); cross-sample
  recurrence excludes the same biological sample, including technical repeats.
  Max-overlap matching is intentionally many-to-one, NOT reciprocal matching.
  Greedy within-sample redundancy removal follows; this behavior is tested.
- Unknown patients have blank or literal unknown IDs, status=unknown. They are
  excluded from n_patients and counted as n_unknown_patient_samples, never as
  one shared patient. Confirmed patient support uses distinct canonical IDs.

## P1 repairs and limitations

- Counts and normalization parameters are checked for finite/valid values.
  The 200-cell gate is checked after zero-library removal; manifest separates
  input and retained cell counts. At least 50 effective genes are required.
- __all__ is rejected without single_biological_sample_verified=1 in the
  reviewed plan. This assertion still requires upstream human verification.
- Consensus uses one representative GEP per biological sample rather than
  a union. Representative maximizes total overlap to other samples, with
  program_id as deterministic tie break. Each sample votes once for each gene.
- Threshold and leave-one-dataset-out behavior are covered by synthetic tests;
  single-dataset MPs are explicitly flagged cross_dataset_recurrent=false.
  These tests are NOT a completed real-data stability analysis.
- 100/200/500 cohort sensitivity driver and multi-seed NMF stability are still
  pending implementation. Mitochondrial/ribosomal exclusion and harmonized gene
  namespace need an approved method decision. No claim of Gavish equivalence.

## Commands and inputs

```bash
python code/06_filter_robust_programs.py --tasks tasks.tsv --cohort cohort.tsv --output robust.tsv
python code/07_discover_metaprograms.py --programs robust.tsv --cohort cohort.tsv --output MPs.json
bash tests/run_argos_synthetic.sh /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_algorithm_gate_a_20261009/A3_tests.log
```

Only synthetic fixtures enter these tests. Raw Argos execution output and source
SHA256 hashes accompany this revision in docs/A3_Argos_tests.log. Passing software
tests is not authorization to analyze real samples or approval of their metadata.
