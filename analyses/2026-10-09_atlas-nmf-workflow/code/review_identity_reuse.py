"""Public status export: no patient identifiers or sample linkage fields."""
import csv
import pathlib
import sys
import collections

root, legacy = map(pathlib.Path, sys.argv[1:3])
def read(name):
    with (root / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))
def write(name, rows):
    with (root / name).open('w') as f:
        w = csv.DictWriter(f, list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader(); w.writerows(rows)
rows = read('final_sample_inventory.DRAFT.tsv')
coverage = read('historical_sample_coverage.tsv')
matched = {r['sample_id'] for r in coverage if int(r['n_task_matches'])}
groups = collections.Counter(r['patient_id'] for r in rows if r['patient_id_status']=='confirmed')
public = []
for r in rows:
    normal = r['tissue'] == 'Normal'
    public.append(dict(dataset_id=r['dataset_id'], sample_id=r['sample_id'],
        annotation_status='original_label_provenance_pending',
        tissue_review_status='Normal_not_approved' if normal else 'no_Normal_conflict_detected',
        qc_status='PASS', historical_reuse_status='direct_reuse_not_approved' if r['sample_id'] in matched else 'coverage_unresolved',
        review_status='not_approved_Normal' if normal else 'final_eligibility_pending',
        enabled=0))
write('PUBLIC_sample_review.tsv', public)
tasks = []
for r in coverage:
    if int(r['n_task_matches']):
        for d in (legacy/'fastnmf_batch').glob('rank*/bucket*/malignant/'+r['legacy_sample_candidate']+'/K*'):
            tasks.append(dict(dataset_id=r['dataset_id'], sample_id=r['sample_id'], output_dir=str(d)))
write('legacy_readability_inputs.tsv', tasks)
print('Normal_tissue candidates:', [(r['sample_id'],r['n_retained_cells'],r['timepoint']) for r in rows if r['tissue']=='Normal'])
print('Independent source-local patient groups:', len(groups))
print('Readability targets:', len(tasks))
