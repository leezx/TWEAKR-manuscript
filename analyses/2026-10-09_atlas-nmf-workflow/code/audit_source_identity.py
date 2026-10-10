"""Audit existing SOFT identities; keep joins and patient values private on Argos."""
import collections
import csv
import gzip
import pathlib
import sys

root, source = map(pathlib.Path, sys.argv[1:3])
with (root/'final_sample_inventory.DRAFT.tsv').open() as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
def soft(dataset):
    samples = []
    current = None
    with gzip.open(source/dataset/(dataset+'_family.soft.gz'), 'rt') as f:
        for line in f:
            if line.startswith('^SAMPLE = '):
                current = collections.defaultdict(list)
                current['accession'].append(line.strip().split(' = ',1)[1])
                samples.append(current)
            elif line.startswith('^'):
                current = None
            elif current is not None and line.startswith('!') and ' = ' in line:
                key, value = line.strip().split(' = ',1)
                current[key].append(value)
    return samples
sources = {d:soft(d) for d in {r['dataset_id'] for r in rows}}
private, public = [], []
for r in rows:
    title = r['sample_id']
    basis = 'exact_sample_title'
    if r['dataset_id']=='GSE236581':
        # Patient comes from source metadata, never inferred from the CRC name.
        title = r['original_patient_id']+'-'+r['sample_id'].split('-',1)[1]
        basis = 'source_patient_plus_source_sample_suffix'
    hits = [s for s in sources[r['dataset_id']] if title in s['!Sample_title']]
    public.append(dict(dataset_id=r['dataset_id'],sample_id=r['sample_id'],
        source_record_matches=len(hits), source_identity_status='unique_source_record_candidate' if len(hits)==1 else 'unresolved',
        technical_replicate_status='not_proven_absent',
        annotation_definition_status='unverified_original_methods',enabled=0))
    private.append(dict(dataset_id=r['dataset_id'],sample_id=r['sample_id'],
        patient_id=r['patient_id'],join_basis=basis,
        accessions='|'.join(s['accession'][0] for s in hits),
        source_characteristics='|'.join(v for s in hits for v in s['!Sample_characteristics_ch1'])))
for name, data in [('PRIVATE_source_identity.tsv',private),('PUBLIC_source_identity_status.tsv',public)]:
    with (root/name).open('w') as f:
        w=csv.DictWriter(f,list(data[0]),delimiter='\t',lineterminator='\n')
        w.writeheader();w.writerows(data)
    if name.startswith('PRIVATE'):
        (root/name).chmod(0o600)
for d in sorted(sources):
    print(d,'SOFT records=',len(sources[d]),'candidate_matches=',dict(collections.Counter(r['source_record_matches'] for r in public if r['dataset_id']==d)))
print('PRIVATE mapping retained on Argos; all enabled=0; no analysis executed')
