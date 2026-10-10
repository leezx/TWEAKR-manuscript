#!/usr/bin/env python3
"""Produce final robust GEPs using an explicitly reviewed identity mapping."""
import argparse
import csv
import json
from pathlib import Path
from program_algorithms import IDENTITY, robust, validate_cohort


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tasks', type=Path, required=True)
    ap.add_argument('--cohort', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    with args.cohort.open() as f:
        mapping = validate_cohort(list(csv.DictReader(f, delimiter='\t')))
    with args.tasks.open() as f:
        tasks = list(csv.DictReader(f, delimiter='\t'))
    programs = []
    for task in tasks:
        key = tuple(task[k] for k in ('dataset_id', 'source_id', 'sample_id'))
        if key not in mapping:
            raise ValueError('Task absent from reviewed cohort mapping')
        groups = {}
        with (Path(task['output_dir']) / 'deliver.nmf_top50.repeated.csv').open() as f:
            for row in csv.DictReader(f):
                groups.setdefault(row['factor'], set()).add(row['gene'])
        for factor, genes in groups.items():
            programs.append(dict(mapping[key], rank=int(task['rank']), factor=factor,
                program_id=json.dumps([*key, int(task['rank']), factor], separators=(',', ':')),
                genes=sorted(genes)))
    selected = robust(programs)
    fields = ['program_id', *IDENTITY, 'rank', 'factor', 'within_rank_overlap',
              'across_sample_overlap', 'program_stage', 'genes']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        for p in selected:
            p['program_stage'] = 'robust'
            writer.writerow({k: '|'.join(p[k]) if k == 'genes' else p[k] for k in fields})


if __name__ == '__main__':
    main()
