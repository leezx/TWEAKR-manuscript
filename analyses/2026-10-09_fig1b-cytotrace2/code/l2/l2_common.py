"""Shared helpers for the Fig. 1B L2 annotation (parameters: ../l2_config.yaml).

No function here reads any CytoTRACE2 output.
"""
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import yaml

LINEAGES = ["Epithelial", "Immune", "Stromal"]
# independent marker lineage (atlas_major_lineage_20261009) -> L1 lineage; Unknown is never foreign
MARKER_LINEAGE_TO_L1 = {"Epithelial": "Epithelial", "Immune": "Immune",
                        "Stromal": "Stromal", "Endothelial": "Stromal"}


def load_cfg(path):
    with open(path) as fh:
        return yaml.safe_load(fh)


def dec(x):
    return x.decode() if isinstance(x, bytes) else str(x)


def read_h5_col(group, key, rows=None):
    """Read one obs/var column from an AnnData H5AD (new and old categorical encodings)."""
    node = group[key]
    if isinstance(node, h5py.Group):  # anndata >= 0.8 categorical
        cats = np.array([dec(x) for x in node["categories"][:]], dtype=object)
        codes = node["codes"][:]
        vals = np.where(codes >= 0, cats[np.clip(codes, 0, None)], None)
    else:
        vals = node[:]
        if "categories" in node.attrs:  # anndata < 0.8 categorical
            cats = np.array([dec(x) for x in group.file[node.attrs["categories"]][:]], dtype=object)
            vals = np.where(vals >= 0, cats[np.clip(vals, 0, None)], None)
        elif vals.dtype.kind in "SO":
            vals = np.array([dec(x) for x in vals], dtype=object)
    return vals if rows is None else vals[rows]


def run_paths(run_root):
    root = Path(run_root)
    p = {k: root / k for k in ["objects", "cells", "scvi", "labels", "cnv", "final", "light", "logs"]}
    for d in p.values():
        d.mkdir(parents=True, exist_ok=True)
    p["root"] = root
    return p


def panel_dict(cfg, lineage):
    """L2 panels of a lineage as {name: (pos, neg)}."""
    out = {}
    for name, spec in cfg["panels_L2"][lineage].items():
        if isinstance(spec, dict):
            out[name] = (list(spec["pos"]), list(spec.get("neg", [])))
        else:
            out[name] = (list(spec), [])
    return out


def read_gmt(path):
    sets = {}
    with open(path) as fh:
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) > 2:
                sets[f[0]] = [g for g in f[2:] if g]
    return sets


def call_top(scores, min_score, min_margin):
    """Top-column call per row: top > min_score and top - second >= min_margin, else None."""
    s = scores.to_numpy(dtype=float)
    order = np.argsort(-s, axis=1)
    top = s[np.arange(len(s)), order[:, 0]]
    second = s[np.arange(len(s)), order[:, 1]] if s.shape[1] > 1 else np.full(len(s), -np.inf)
    ok = (top > min_score) & ((top - second) >= min_margin)
    names = np.array(scores.columns, dtype=object)[order[:, 0]]
    return pd.Series(np.where(ok, names, None), index=scores.index, dtype=object)


def consensus(a, b, c):
    """Marker-consensus rule: high = a==c; medium = any two of a, b, c agree; else low."""
    a, b, c = (pd.Series(x, dtype=object) for x in (a, b, c))
    label = pd.Series([None] * len(a), dtype=object)
    conf = pd.Series(["low"] * len(a), dtype=object)
    method = pd.Series([""] * len(a), dtype=object)
    for i in range(len(a)):
        ai, bi, ci = a.iat[i], b.iat[i], c.iat[i]
        if ai is not None and ai == ci:
            label.iat[i], conf.iat[i] = ai, "high"
            method.iat[i] = "a+b+c" if bi == ai else "a+c"
        elif ai is not None and ai == bi:
            label.iat[i], conf.iat[i], method.iat[i] = ai, "medium", "a+b"
        elif bi is not None and bi == ci:
            label.iat[i], conf.iat[i], method.iat[i] = bi, "medium", "b+c"
    return label.to_numpy(), conf.to_numpy(), method.to_numpy()
