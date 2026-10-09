#!/usr/bin/env python3
"""Filter repeated top50 programs; all inputs must use harmonized gene IDs."""
import argparse
import csv
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tasks', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    with args.tasks.open() as f:
        tasks = list(csv.DictReader(f, delimiter='\t'))
    programs = []
    for task in tasks:
        groups = {}
        with (Path(task['output_dir']) / 'deliver.nmf_top50.repeated.csv').open() as f:
            for row in csv.DictReader(f):
                groups.setdefault(row['factor'], set()).add(row['gene'])
        for factor, genes in groups.items():
            if len(genes) != 50:
                raise ValueError('Every program must contain exactly 50 distinct genes')
            programs.append(dict(task, factor=factor, genes=genes))
    # Sample identity must be explicitly harmonized across source RDS files.
    def sample(p):
        return (p['dataset_id'], p['sample_id'])
    def overlap(a, b):
        return len(a['genes'] & b['genes'])
    stable = []
    for p in programs:
        score = max((overlap(p, q) for q in programs
                     if sample(p) == sample(q) and p['rank'] != q['rank']), default=0)
        p['within_rank_overlap'] = score
        if score >= 35:
            stable.append(p)
    for p in stable:
        peers = [q for q in stable if sample(p) != sample(q)]
        p['across_sample_overlap'] = max((overlap(p, q) for q in peers), default=0)
        p['supporting_datasets'] = len({q['dataset_id'] for q in peers
                                        if overlap(p, q) >= 10})
    chosen = []
    for key in sorted({sample(p) for p in stable}):
        candidates = sorted((p for p in stable if sample(p) == key
                             and p['across_sample_overlap'] >= 10),
                            key=lambda p: (-p['across_sample_overlap'], int(p['rank']), p['factor']))
        retained = []
        for p in candidates:
            if all(overlap(p, q) <= 10 for q in retained):
                retained.append(p)
        chosen.extend(retained)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = ['dataset_id', 'sample_id', 'source_id', 'rank', 'factor',
              'within_rank_overlap', 'across_sample_overlap', 'supporting_datasets', 'genes']
    with args.output.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        for p in chosen:
            writer.writerow({k: '|'.join(sorted(p[k])) if k == 'genes' else p[k] for k in fields})


if __name__ == '__main__':
    main()
