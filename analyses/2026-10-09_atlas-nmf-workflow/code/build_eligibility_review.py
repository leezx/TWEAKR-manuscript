"""Metadata-only final intake proposal; never enables execution."""
import collections
import csv
import gzip
import pathlib
import sys

root, source = map(pathlib.Path, sys.argv[1:3])
def read(name):
    with (root/name).open() as f:
        return list(csv.DictReader(f,delimiter='\t'))
rows = read('final_sample_inventory.DRAFT.tsv')
source_status = {(r['dataset_id'],r['sample_id']):r for r in read('PUBLIC_source_identity_status.tsv')}
sample_keys = collections.defaultdict(set)
with gzip.open(source/'GSE254249/supplementary/GSE254249_scRNA_metadata.tsv.gz','rt') as f:
    for r in csv.DictReader(f,delimiter='\t'):
        sample_keys[r['Ident']].add((r['PatientID'],r['Tissue'],r['SampleTimePoint']))
key_samples = collections.defaultdict(set)
for sample, keys in sample_keys.items():
    for key in keys:
        key_samples[key].add(sample)
selected_key_counts = collections.Counter((r['dataset_id'],r['patient_id'],r['tissue'],r['timepoint']) for r in rows)
output = []
for r in rows:
    normal = r['tissue']=='Normal'
    gao = r['dataset_id']=='GSE254249'
    keys = sample_keys.get(r['sample_id'],set()) if gao else set()
    identity_ok = (len(keys)==1 and all(len(key_samples[k])==1 for k in keys)) if gao else (
        selected_key_counts[(r['dataset_id'],r['patient_id'],r['tissue'],r['timepoint'])]==1)
    unique = source_status[(r['dataset_id'],r['sample_id'])]['source_record_matches']=='1'
    proposal = 'not_approved' if normal else 'approved' if gao and identity_ok and unique else 'pending'
    output.append(dict(dataset_id=r['dataset_id'],sample_id=r['sample_id'],
        annotation_evidence='author_group_Cancer_provisional_accepted' if gao else 'c91_definition_unverified',
        tissue_evidence='source_metadata_Normal' if normal else 'source_metadata_tumor_origin',
        identity_evidence='source_metadata_no_collision_detected' if identity_ok else 'identity_ambiguity',
        scope_of_identity_check='all_92_source_samples' if gao else 'selected_27_source_samples',
        source_record_status='unique_candidate' if unique else 'unresolved',
        cross_study_identity='unresolved',eligibility_proposal=proposal,
        review_status='not_approved' if normal else 'pending_final_review',enabled=0))
with (root/'PUBLIC_eligibility_review.tsv').open('w') as f:
    w=csv.DictWriter(f,list(output[0]),delimiter='\t',lineterminator='\n')
    w.writeheader();w.writerows(output)
print('GSE254249 complete source sample count:',len(sample_keys))
print('Proposal summary:',dict(collections.Counter(r['eligibility_proposal'] for r in output)))
assert len(sample_keys)==92
assert len(output)==53
assert all(r['enabled']==0 for r in output)
print('No patient relationships exported; all execution flags0')
