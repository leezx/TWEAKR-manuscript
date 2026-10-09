"""Deterministic overlap filtering and complete-link MP discovery.

This is a declared project algorithm, not the original Gavish clustering.
Patient and biological sample IDs must be globally harmonized in the input.
"""
from collections import Counter


def overlap(a, b):
    return len(set(a['genes']) & set(b['genes']))


def validate(programs):
    seen = set()
    for p in programs:
        for key in ('program_id', 'dataset_id', 'sample_id', 'patient_id', 'rank'):
            if not p.get(key):
                raise ValueError('Missing identity: ' + key)
        if p['program_id'] in seen:
            raise ValueError('Duplicate program ID')
        seen.add(p['program_id'])
        if len(set(p['genes'])) != 50:
            raise ValueError('Require exactly 50 distinct genes')
    sample_patients = {}
    for p in programs:
        key = p['sample_id']
        if key in sample_patients and sample_patients[key] != p['patient_id']:
            raise ValueError('One biological sample maps to multiple patients')
        sample_patients[key] = p['patient_id']


def robust(programs, within=35, across=10, redundancy=10):
    validate(programs)
    stable = []
    for p in programs:
        score = max((overlap(p, q) for q in programs
                     if p['sample_id'] == q['sample_id'] and p['rank'] != q['rank']), default=0)
        if score >= within:
            stable.append(dict(p, within_rank_overlap=score))
    for p in stable:
        p['across_sample_overlap'] = max((overlap(p, q) for q in stable
                                         if p['sample_id'] != q['sample_id']), default=0)
    selected = []
    for sample in sorted({p['sample_id'] for p in stable}):
        candidates = sorted((p for p in stable if p['sample_id'] == sample
                             and p['across_sample_overlap'] >= across),
                            key=lambda p: (-p['across_sample_overlap'], p['program_id']))
        kept = []
        for p in candidates:
            if all(overlap(p, q) <= redundancy for q in kept):
                kept.append(p)
        selected.extend(kept)
    return selected


def discover(programs, min_overlap=10, min_samples=2):
    """Complete-link agglomeration: every pair shares >= min_overlap genes."""
    clusters = [[p] for p in sorted(programs, key=lambda p: p['program_id'])]
    while True:
        candidates = []
        for i, a in enumerate(clusters):
            for j in range(i + 1, len(clusters)):
                b = clusters[j]
                score = min(overlap(p, q) for p in a for q in b)
                if score >= min_overlap:
                    candidates.append((-score, i, j))
        if not candidates:
            break
        _, i, j = min(candidates)
        clusters[i] += clusters.pop(j)
    return [c for c in clusters if len({p['sample_id'] for p in c}) >= min_samples]


def summarize(cluster, cohort):
    """Consensus votes once per sample; report denominators from full cohort."""
    sample_genes = {}
    for p in cluster:
        sample_genes.setdefault(p['sample_id'], set()).update(p['genes'])
    votes = Counter(g for genes in sample_genes.values() for g in genes)
    consensus = sorted(votes, key=lambda g: (-votes[g], g))[:50]
    patients = {p['patient_id'] for p in cluster}
    datasets = {p['dataset_id'] for p in cluster}
    pairs = [overlap(p, q) / len(set(p['genes']) | set(q['genes']))
             for i, p in enumerate(cluster) for q in cluster[i + 1:]]
    support = []
    for dataset in sorted({r['dataset_id'] for r in cohort}):
        eligible = {r['sample_id'] for r in cohort if r['dataset_id'] == dataset}
        supported = {p['sample_id'] for p in cluster if p['dataset_id'] == dataset}
        support.append(dict(dataset_id=dataset, supporting_samples=len(supported),
                            eligible_samples=len(eligible), proportion=len(supported) / len(eligible)))
    return dict(n_samples=len(sample_genes), n_patients=len(patients),
                n_datasets=len(datasets), mean_jaccard=sum(pairs)/len(pairs) if pairs else 0,
                mean_rank_overlap=sum(p['within_rank_overlap'] for p in cluster)/len(cluster),
                consensus=consensus, dataset_support=support)
