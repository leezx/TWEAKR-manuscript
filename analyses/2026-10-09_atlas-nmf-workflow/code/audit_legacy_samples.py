#!/usr/bin/env python3
"""Use actual historical task table, not truncated preparation manifest."""
import csv
import sys
from pathlib import Path
root, legacy = map(Path, sys.argv[1:3])
with (root/'eligible_samples.DRAFT.tsv').open() as f:
    new=[r for r in csv.DictReader(f, delimiter='\t') if int(r['n_source_label_cells'])>=200]
with (legacy/'fastnmf_tasks/bucket_master.tsv').open() as f:
    old=[r for r in csv.DictReader(f, delimiter='\t') if r['group']=='malignant']
rows=[]
required=['W.matrix.rds','H.matrix.rds','fastNMF_result_object.rds',
          'deliver.nmf_markers.csv']
for r in new:
    name='Chen_2024.'+r['sample_id'].replace('-','_') if r['dataset_id']=='GSE236581' else ''
    hits=[x for x in old if name and x['sample_id']==name]
    dirs=list((legacy/'fastnmf_batch').glob('rank*/bucket*/malignant/'+name+'/K*')) if hits else []
    missing=[]; ranks=[]
    for d in dirs:
        ranks.append(d.name)
        missing.extend(str(d/name) for name in required if not (d/name).is_file())
    rows.append(dict(dataset_id=r['dataset_id'], sample_id=r['sample_id'],
        legacy_sample_candidate=name if hits else '', match_basis='BioProject plus hyphen_underscore_only' if hits else 'no_verified_mapping',
        identity_status='unresolved_requires_source_crosswalk', n_task_matches=len(hits),
        output_ranks='|'.join(sorted(set(ranks))), n_output_dirs=len(dirs),
        missing_required_files='|'.join(missing),
        file_status='required_files_exist' if dirs and not missing else 'missing_or_unmatched',
        reuse_decision='unresolved', execution_enabled=0))
with (root/'historical_sample_coverage.tsv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n')
    w.writeheader();w.writerows(rows)
print('Candidate sample rows',len(rows),'task-name matches',sum(r['n_task_matches']>0 for r in rows),
      'required files present',sum(r['file_status']=='required_files_exist' for r in rows))
print('Reuse remains unresolved; no NMF')
