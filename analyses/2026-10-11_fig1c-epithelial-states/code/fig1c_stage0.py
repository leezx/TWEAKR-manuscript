#!/usr/bin/env python3
"""Fig. 1c Stage 0 (frozen contract v0.3 §2): build every gene set used in Stage 1 and the manifest.

Outputs (private dir, umask 077; restricted A3a sets are carried through):
  genesets_fig1c.private.tsv  two columns set, gene (input to a3a_ucell.R)
  stage0_manifest.json        gene counts per set, Atlas coverage, overlaps, input/output SHA256
No CytoTRACE2 file is read.
"""
import argparse
import hashlib
import json
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix

N_SPLITS = 200
SPLIT_SEED = 14


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_main(p):
    with h5py.File(p, "r") as h:
        shape = tuple(h["shape"][:])
        m = csc_matrix((h["data"][:], h["indices"][:], h["indptr"][:]), shape=shape)
        genes = np.array([g.decode() if isinstance(g, bytes) else g for g in h["genes"][:]])
    return m, genes  # genes x cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a3a_genesets", required=True)
    ap.add_argument("--mzoughi", required=True)
    ap.add_argument("--holdout_extra", required=True)
    ap.add_argument("--stress", required=True)
    ap.add_argument("--ccgenes", required=True, help="two columns phase, gene (Seurat cc.genes.updated.2019)")
    ap.add_argument("--counts_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    a3a = pd.read_csv(a.a3a_genesets, sep="\t")
    a3a_sets = {s: list(dict.fromkeys(g.gene)) for s, g in a3a.groupby("set")}
    mz = pd.read_csv(a.mzoughi, sep="\t")
    mz_sets = {s: list(dict.fromkeys(g.gene)) for s, g in mz.groupby("set")}
    extra = [l.strip() for l in open(a.holdout_extra) if l.strip()]
    stress = {l.strip() for l in open(a.stress) if l.strip()}
    cc = set(pd.read_csv(a.ccgenes, sep="\t").gene)

    H = set(a3a_sets["YAPcore"]) | set(extra)
    pro, rev = a3a_sets["proCSC"], a3a_sets["revCSC"]

    # Atlas gene space and mean expression (deterministic subset: first 3 main.h5 per study, sorted)
    files = sorted(Path(a.counts_dir).glob("*.main.h5"))
    by_study = {}
    for f in files:
        by_study.setdefault(f.name.split(".")[0], []).append(f)
    used = [f for s in sorted(by_study) for f in by_study[s][:3]]
    tot, n_cells, genes0 = None, 0, None
    for f in used:
        m, genes = read_main(f)
        if genes0 is None:
            genes0 = genes
        assert (genes == genes0).all(), f"gene order differs in {f}"
        lib = np.asarray(m.sum(axis=0)).ravel()
        x = m.multiply(1e4 / np.maximum(lib, 1)).tocsc()
        s = np.asarray(x.sum(axis=1)).ravel()
        tot = s if tot is None else tot + s
        n_cells += m.shape[1]
    mean_expr = pd.Series(tot / n_cells, index=genes0)
    atlas = set(genes0)

    sets = {
        "proCSC": pro,
        "revCSC": rev,
        "proCSC_mb": [g for g in pro if g not in H],
        "revCSC_mb": [g for g in rev if g not in H],
        "proCSC_noCC": [g for g in pro if g not in cc],
        "proCSC_noStress": [g for g in pro if g not in stress],
        "revCSC_noStress": [g for g in rev if g not in stress],
        "hOnF": mz_sets["hOnF"],
        "hStem": mz_sets["hStem"],
        "hOnF_no": [g for g in mz_sets["hOnF"] if g not in set(pro) | set(rev)],
        "hStem_no": [g for g in mz_sets["hStem"] if g not in set(pro) | set(rev)],
    }
    # gene-splits: definition half = ceil(n/2) of Atlas-present genes, stratified by mean-expression tertile
    rng = np.random.default_rng(SPLIT_SEED)
    split_def = {}
    for name, gs in [("proCSC", pro), ("revCSC", rev)]:
        present = [g for g in gs if g in atlas]
        tert = pd.qcut(mean_expr[present].rank(method="first"), 3, labels=False)
        for i in range(1, N_SPLITS + 1):
            r = dict(zip(present, rng.random(len(present))))
            order = sorted(present, key=lambda g: (tert[g], r[g]))
            d = order[0::2]
            sets[f"{name}_split{i:03d}"] = d
            split_def[f"{name}_split{i:03d}"] = len(d)
        for g in present:
            sets[f"{name}_minus_{g}"] = [x for x in present if x != g]

    h_path = out / "holdout_H.private.txt"
    h_path.write_text("\n".join(sorted(H)) + "\n")
    h_path.chmod(0o600)
    rows = [(s, g) for s, gs in sets.items() for g in gs]
    gs_path = out / "genesets_fig1c.private.tsv"
    pd.DataFrame(rows, columns=["set", "gene"]).to_csv(gs_path, sep="\t", index=False)
    gs_path.chmod(0o600)

    def cov(gs):
        return sum(g in atlas for g in gs) / max(len(gs), 1)

    core = ["proCSC", "revCSC", "proCSC_mb", "revCSC_mb", "proCSC_noCC", "proCSC_noStress",
            "revCSC_noStress", "hOnF", "hStem", "hOnF_no", "hStem_no"]
    man = {
        "contract": "Fig1c_contract.md v0.3 (frozen 2026-10-11)",
        "holdout_H_n": len(H),
        "H_in_proCSC": sorted(set(pro) & H), "H_in_revCSC": sorted(set(rev) & H),
        "cc_in_proCSC": sorted(set(pro) & cc), "stress_in_proCSC": sorted(set(pro) & stress),
        "stress_in_revCSC": sorted(set(rev) & stress),
        "sets": {s: {"n": len(sets[s]), "n_in_atlas": sum(g in atlas for g in sets[s]),
                     "atlas_coverage": round(cov(sets[s]), 4)} for s in core},
        "hOnF_no_present_in_atlas": sum(g in atlas for g in sets["hOnF_no"]),
        "hStem_no_present_in_atlas": sum(g in atlas for g in sets["hStem_no"]),
        "n_splits": N_SPLITS, "split_seed": SPLIT_SEED,
        "split_definition_sizes": sorted(set(split_def.values())),
        "n_sets_total": len(sets),
        "mean_expr_files": [f.name for f in used], "mean_expr_cells": int(n_cells),
        "inputs_sha256": {k: sha(v) for k, v in {
            "a3a_genesets": a.a3a_genesets, "mzoughi": a.mzoughi, "holdout_extra": a.holdout_extra,
            "stress": a.stress, "ccgenes": a.ccgenes}.items()},
        "genesets_fig1c_sha256": sha(gs_path),
        "holdout_H_sha256": sha(h_path),
    }
    (out / "stage0_manifest.json").write_text(json.dumps(man, indent=1))
    print(json.dumps({k: man[k] for k in ["holdout_H_n", "H_in_proCSC", "H_in_revCSC", "cc_in_proCSC",
                                          "stress_in_proCSC", "stress_in_revCSC", "sets",
                                          "hOnF_no_present_in_atlas", "n_sets_total"]}, indent=1))


if __name__ == "__main__":
    main()
