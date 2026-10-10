#!/usr/bin/env python3
"""Read existing manifests and source metadata; never load expression or run NMF."""
import csv
import gzip
import json
import sys
import shlex
from collections import Counter
from pathlib import Path

root, out = map(Path, sys.argv[1:3])
out.mkdir(parents=True, exist_ok=True)
with (root/'seurat_counts_rds/validated_object_manifest.tsv').open() as f:
    objects = list(csv.DictReader(f, delimiter='\t'))
sources = {
    'GSE155953': 'GSE155953_ADC-integrated_cellinfo.txt.gz',
    'GSE236581': 'GSE236581_CRC-ICB_metadata.txt.gz',
    'GSE254249': 'GSE254249_scRNA_metadata.tsv.gz',
}
reports = []
for dataset in sorted({r['accession'] for r in objects}):
    rows = [r for r in objects if r['accession'] == dataset]
    report = dict(dataset_id=dataset, n_rds=len(rows), cells_manifest=sum(int(r['cells']) for r in rows),
                  bytes_manifest=sum(int(r['bytes']) for r in rows), annotation_status='no_cell_metadata_in_build',
                  source_metadata='', metadata_columns='', label_counts='', identity_status='needs_review',
                  execution_status='HOLD')
    if dataset in sources:
        path = root/dataset/'supplementary'/sources[dataset]
        with gzip.open(path, 'rt') as f:
            header = next(f)
            parse = (lambda line: next(csv.reader([line], delimiter='\t'))) if '\t' in header else shlex.split
            columns = parse(header)
            counters = {k: Counter() for k in columns if any(t in k.lower() for t in ('group','celltype','cell_type','malign','cluster'))}
            for line in f:
                values = parse(line)
                if len(values) == len(columns) + 1:
                    values = values[1:]  # R row.names field has no header.
                if len(values) != len(columns):
                    raise ValueError('Metadata field count mismatch: ' + str(path))
                row = dict(zip(columns, values))
                for k in counters:
                    counters[k][row[k]] += 1
            if any(len(v) > 1000 for v in counters.values()):
                raise ValueError('Unexpected high-cardinality annotation; stop export')
        report.update(source_metadata=str(path), metadata_columns='|'.join(columns),
                      label_counts=json.dumps({k:dict(v) for k,v in counters.items()}, sort_keys=True),
                      annotation_status='source_labels_present_requires_review')
    reports.append(report)
with (out/'dataset_annotation_inventory.tsv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(reports[0]), delimiter='\t', lineterminator='\n')
    writer.writeheader()
    writer.writerows(reports)
# Mapping stays remote. Do not invent confirmed biological or patient identity.
mapping = []
for i, row in enumerate(objects, 1):
    mapping.append(dict(dataset_id=row['accession'], source_id=f'source_{i:04d}', sample_id=row['sample'],
                        biological_sample_id='', patient_id='', patient_id_status='unknown',
                        identity_review_status='unresolved', rds_path=row['path'], enabled=0))
with (out/'cohort_identity_mapping.UNREVIEWED.tsv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(mapping[0]), delimiter='\t', lineterminator='\n')
    writer.writeheader()
    writer.writerows(mapping)
print('Datasets:',len(reports),'RDS:',len(objects),'cells:',sum(int(r['cells']) for r in objects))
print('No NMF executed; identity draft disabled and not valid for analysis')
