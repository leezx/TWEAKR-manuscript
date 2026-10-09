"""Export minimal public QC evidence; keep raw identity mapping on Argos."""
import csv
import collections
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
with (root / 'final_sample_inventory.DRAFT.tsv').open() as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
fields = ['dataset_id', 'source_id', 'sample_id', 'assay', 'malignant_column',
          'malignant_value', 'n_source_cells', 'n_RDS_label_cells',
          'n_retained_cells', 'n_zero_library', 'counts_valid',
          'source_count_matches', 'sample_identity_consistent',
          'patient_id_status', 'review_status', 'reason', 'enabled']
with (root / 'PUBLIC_sample_QC.tsv').open('w') as f:
    w = csv.DictWriter(f, fields, delimiter='\t', extrasaction='ignore')
    w.writeheader()
    w.writerows(rows)
for dataset in sorted({r['dataset_id'] for r in rows}):
    group = [r for r in rows if r['dataset_id'] == dataset]
    print(dataset, 'n=', len(group), 'retained=', sum(int(r['n_retained_cells']) for r in group),
          'zero=', sum(int(r['n_zero_library']) for r in group),
          'counts=', collections.Counter(r['counts_valid'] for r in group),
          'sample_identity=', collections.Counter(r['sample_identity_consistent'] for r in group),
          'patient=', collections.Counter(r['patient_id_status'] for r in group),
          'review=', collections.Counter(r['review_status'] for r in group),
          'source_match=', collections.Counter(r['source_count_matches'] for r in group))
with (root / 'historical_sample_coverage.tsv').open() as f:
    coverage = list(csv.DictReader(f, delimiter='\t'))
with (root / 'PUBLIC_historical_coverage.tsv').open('w') as f:
    fields = list(coverage[0])
    w = csv.DictWriter(f, fields, delimiter='\t')
    w.writeheader()
    w.writerows(coverage)
print('Historical task matches:', sum(int(r['n_task_matches']) > 0 for r in coverage))
print('Historical statuses:', collections.Counter(r['file_status'] for r in coverage))
assert len(rows) == len(coverage) == 53
assert all(r['enabled'] == '0' for r in rows)
