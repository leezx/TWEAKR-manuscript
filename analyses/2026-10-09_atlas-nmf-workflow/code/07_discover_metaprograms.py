#!/usr/bin/env python3
"""Run reviewed project MP algorithm on a harmonized program TSV."""
import argparse
import csv
import json
from pathlib import Path
from program_algorithms import IDENTITY, validate, validate_cohort, discover, summarize

ap = argparse.ArgumentParser()
ap.add_argument('--programs', type=Path, required=True)
ap.add_argument('--cohort', type=Path, required=True)
ap.add_argument('--output', type=Path, required=True)
ap.add_argument('--min-overlap', type=int, default=10)
ap.add_argument('--min-samples', type=int, default=2)
args = ap.parse_args()
with args.programs.open() as f:
    programs = list(csv.DictReader(f, delimiter='\t'))
for p in programs:
    if p.get('program_stage') != 'robust':
        raise ValueError('07 requires final robust GEPs from 06')
    p['genes'] = p['genes'].split('|')
    p['rank'] = int(p['rank'])
    p['within_rank_overlap'] = int(p['within_rank_overlap'])
with args.cohort.open() as f:
    cohort = list(csv.DictReader(f, delimiter='\t'))
mapping = validate_cohort(cohort)
validate(programs)
for p in programs:
    key = tuple(p[k] for k in ('dataset_id', 'source_id', 'sample_id'))
    if key not in mapping or any(p[k] != mapping[key][k] for k in IDENTITY):
        raise ValueError('Program identity absent from reviewed cohort')
clusters = discover(programs, args.min_overlap, args.min_samples)
result = []
for i, cluster in enumerate(clusters, 1):
    result.append(dict(mp_id=f'M{i:02d}', programs=[p['program_id'] for p in cluster],
                       **summarize(cluster, cohort)))
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, indent=2) + '\n')
