#!/usr/bin/env python3
"""Run reviewed project MP algorithm on a harmonized program TSV."""
import argparse
import csv
import json
from pathlib import Path
from program_algorithms import robust, discover, summarize

ap = argparse.ArgumentParser()
ap.add_argument('--programs', type=Path, required=True)
ap.add_argument('--cohort', type=Path, required=True)
ap.add_argument('--output', type=Path, required=True)
args = ap.parse_args()
with args.programs.open() as f:
    programs = list(csv.DictReader(f, delimiter='\t'))
for p in programs:
    p['genes'] = p['genes'].split('|')
with args.cohort.open() as f:
    cohort = list(csv.DictReader(f, delimiter='\t'))
mapping = {(r['dataset_id'], r['sample_id'], r['patient_id']) for r in cohort}
if any((p['dataset_id'], p['sample_id'], p['patient_id']) not in mapping for p in programs):
    raise ValueError('Program identity absent from approved cohort')
selected = robust(programs)
clusters = discover(selected)
result = []
for i, cluster in enumerate(clusters, 1):
    result.append(dict(mp_id=f'M{i:02d}', programs=[p['program_id'] for p in cluster],
                       **summarize(cluster, cohort)))
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, indent=2) + '\n')
