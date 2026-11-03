#!/usr/bin/env python3
"""Source-backed annotation and legacy input coverage audit; no NMF."""
import csv
import gzip
import re
import shlex
import sys
from collections import Counter, defaultdict
from pathlib import Path

root, legacy, out = map(Path, sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)
def read(path, delimiter='\t'):
    with path.open(encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter=delimiter))
def write(name, rows):
    with (out/name).open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader(); w.writerows(rows)
objects=read(root/'seurat_counts_rds/validated_object_manifest.tsv')
old=read(legacy/'NMF/expr_matrix/each_sample/fastnmf_rds_manifest.tsv')
with (legacy/'metadata/datasets_integrated_in_this_paper.csv').open(encoding='utf-8-sig') as f:
    deposits=list(csv.reader(f))
projects={}
for vals in deposits:
    if len(vals)>=3 and vals[2] and vals[2].startswith('PRJNA'):
        projects[vals[2]]= '_'.join(vals[0].split('_')[:2])
aliases={}
for ds in sorted({r['accession'] for r in objects}):
    soft=root/ds/(ds+'_family.soft.gz')
    project=''
    if soft.exists():
        with gzip.open(soft,'rt') as f:
            for line in f:
                if line.startswith('!Series_relation = BioProject:'):
                    project=re.search(r'PRJNA\d+',line).group()
                    break
    aliases[ds]=(project,projects.get(project,''))
coverage=[]
for r in objects:
    ds,sample=r['accession'],r['sample']
    project,alias=aliases[ds]
    hits=[x for x in old if alias and x['group']=='malignant' and
          (x['dataset']==alias or x['dataset'].startswith(alias+'_')) and
          x['sample_id']==x['dataset']+'.'+sample]
    result_ranks=set()
    for hit in hits:
        for path in (legacy/'NMF/fastnmf_batch').glob('rank*/bucket*/malignant/'+hit['sample_id']+'/K*/W.matrix.rds'):
            if path.stat().st_size > 0:
                result_ranks.add(path.parent.name)
    coverage.append(dict(dataset_id=ds,sample_id=sample,bioproject=project,legacy_alias=alias,
        exact_legacy_inputs=len(hits),coverage_status='legacy_input_exact_match' if hits else
        ('sample_not_exactly_matched' if alias else 'dataset_alias_unresolved'),
        legacy_result_ranks='|'.join(sorted(result_ranks)),
        legacy_results_status='W_file_present_not_full_output_QC' if result_ranks else 'no_matched_W_file',
        biological_identity_review='pending'))
write('sample_legacy_coverage.tsv',coverage)
summaries=[]
for ds in sorted(aliases):
    rows=[r for r in coverage if r['dataset_id']==ds]
    summaries.append(dict(dataset_id=ds,n_rds=len(rows),bioproject=aliases[ds][0],legacy_alias=aliases[ds][1],
        exact_input_matches=sum(r['exact_legacy_inputs']>0 for r in rows),
        not_exactly_matched=sum(r['exact_legacy_inputs']==0 for r in rows),
        samples_with_W_file=sum(bool(r['legacy_result_ranks']) for r in rows),
        completion_status='full_output_QC_and_identity_review_pending'))
write('dataset_legacy_coverage_summary.tsv',summaries)
specs={'GSE254249':('GSE254249_scRNA_metadata.tsv.gz','group','Cancer','PatientID'),
       'GSE236581':('GSE236581_CRC-ICB_metadata.txt.gz','SubCellType','c91_Epi_Tumor','Patient')}
eligible=[]
for ds,(filename,label,value,patient) in specs.items():
    counts=Counter(); identities=defaultdict(set)
    with gzip.open(root/ds/'supplementary'/filename,'rt') as f:
        header=next(f)
        parse=(lambda s:next(csv.reader([s],delimiter='\t'))) if '\t' in header else shlex.split
        columns=parse(header)
        for line in f:
            vals=parse(line)
            if len(vals)==len(columns)+1: vals=vals[1:]
            if len(vals)!=len(columns): raise ValueError('Metadata width mismatch')
            row=dict(zip(columns,vals))
            if row[label]==value:
                counts[row['Ident']]+=1
                identities[row['Ident']].add(row[patient])
    for r in objects:
        if r['accession']!=ds: continue
        sample=r['sample']; pts=identities[sample]-{''}
        eligible.append(dict(dataset_id=ds,sample_id=sample,malignant_column=label,malignant_value=value,
            n_source_label_cells=counts[sample],patient_source_column=patient,
            source_patient_id='|'.join(sorted(pts)),patient_id_status='source_unique' if len(pts)==1 else 'unknown',
            source_id='',biological_sample_id='',review_status='pending' if counts[sample]>=200 else 'excluded',
            reason='source_label_ge200_needs_RDS_QC_identity_review' if counts[sample]>=200 else 'source_label_lt200',
            enabled=0))
write('eligible_samples.DRAFT.tsv',eligible)
print('Coverage:',len(coverage),'Priority annotation rows:',len(eligible))
for ds in specs:
    rows=[r for r in eligible if r['dataset_id']==ds]
    print(ds,'source malignant',sum(r['n_source_label_cells'] for r in rows),'candidate_ge200',sum(r['review_status']=='pending' for r in rows))
