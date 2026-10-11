#!/usr/bin/env python3
"""A3b Stage S prep (contract A3b v0.3 §4; identity_v1 QA limited GO). No CT2 is run here.

Verifies the identity_v1 SHA256, then writes inputs for the Fig. 1b CytoTRACE2 export
(export_sample_counts.py, unchanged):
  ct2/cells_all.tsv          every cell of every A3b sample (whole-sample CT2 unit), with lineage/broad
  ct2/cells_np.tsv, cells_pp.tsv   the same restricted to the normal-primary / pre-post branch samples
  ct2/targets_np.csv, targets_pp.csv   T_s per study for that branch (from qa_summary.json; format of
                                       Fig. 1b depth_targets.csv: target,study,umi)
Chen naive samples belong to both branches and are downsampled at both branch targets (separate dirs).
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

EXPECTED_SHA = "2098d172dd36431fc745c4ca0a4b793d812214206396dc437ee91d4512d57819"


def dec(x):
    return x.decode() if isinstance(x, bytes) else str(x)


def read_col(obs, key):
    g = obs[key]
    if isinstance(g, h5py.Group):
        cats = np.array([dec(c) for c in g["categories"][:]], dtype=object)
        codes = g["codes"][:]
        out = np.full(codes.shape, "NA", dtype=object)
        out[codes >= 0] = cats[codes[codes >= 0]]
        return out
    return np.array([dec(x) for x in g[:]], dtype=object)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--screen-code", required=True)
    a = ap.parse_args()
    sys.path.insert(0, a.screen_code)
    from screen_compartments import BROAD_OF, MIDDLE_TO_LINEAGE  # noqa: E402
    R = Path(a.root)
    sha = hashlib.sha256((R / "identity_v1.private.tsv.gz").read_bytes()).hexdigest()
    if sha != EXPECTED_SHA:
        raise ValueError(f"identity_v1 SHA256 mismatch: {sha}")
    print("identity_v1 SHA256 verified", sha, flush=True)
    out = R / "ct2"
    out.mkdir(exist_ok=True)
    sl = pd.read_csv(R / "inputs/a3b_samples.tsv", sep="\t")
    with h5py.File(a.h5ad, "r") as f:
        obs = f["obs"]
        sid = read_col(obs, "sample_id")
        sel = np.flatnonzero(np.isin(sid, sl.sample_id.unique()))
        idx = np.array([dec(x) for x in obs[obs.attrs["_index"]][:]], dtype=object)
        cells = pd.DataFrame({"cell_id": idx[sel], "sample_id": sid[sel],
                              "study_id": read_col(obs, "study_id")[sel],
                              "patient_id": read_col(obs, "patient_id")[sel],
                              "atlas_cell_type_middle": read_col(obs, "atlas_cell_type_middle")[sel]})
    cells["lineage"] = cells.atlas_cell_type_middle.map(MIDDLE_TO_LINEAGE).fillna("Other")
    cells["broad"] = cells.lineage.map(BROAD_OF).fillna("Other")
    cells = cells.drop(columns="atlas_cell_type_middle")
    # Atlas study_id may differ in spelling from the A3b study labels; use the A3b labels
    lab = sl.drop_duplicates("sample_id").set_index("sample_id")
    cells["study_id"] = cells.sample_id.map(lab.study_id)
    cells.to_csv(out / "cells_all.tsv", sep="\t", index=False)
    qa = json.loads((R / "public/qa_summary.json").read_text())
    for br, tag in [("normal_primary", "np"), ("pre_post", "pp")]:
        smp = set(sl.loc[sl.branch == br, "sample_id"])
        cells[cells.sample_id.isin(smp)].to_csv(out / f"cells_{tag}.tsv", sep="\t", index=False)
        t = pd.DataFrame([{"target": "T_s", "study": k.split("|")[1], "umi": int(round(v))}
                          for k, v in qa["T_s"].items() if k.startswith(br + "|")])
        t.to_csv(out / f"targets_{tag}.csv", index=False)
        print(br, len(smp), "samples", t.to_dict("records"), flush=True)
    print("cells", len(cells), "samples", cells.sample_id.nunique(), flush=True)


if __name__ == "__main__":
    main()
