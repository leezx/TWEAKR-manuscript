#!/usr/bin/env python3
"""Checkpoint 1C: Stereo-seq assay feasibility for TNFSF12 / TNFRSF12A (DS-013).

Reads the public COSMOS Stereo-seq explorer (Cirrocumulus jsonl) by HTTP byte range:
schema, obs categories, spatial embedding and a few gene vectors only. Writes
aggregate tables; no cell-level coordinates or expression are saved. No spatial
statistics, neighbourhood or colocalisation analysis.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

TARGETS = ("TNFSF12", "TNFRSF12A")
MARKERS = ("PTPRC", "CD68", "CD163", "LYVE1", "PECAM1", "HLA-G")
HOUSEKEEPING = ("ACTB", "GAPDH", "MALAT1", "KRT7")
REF_SNRNA = {"TNFSF12": 0.94, "TNFRSF12A": 8.36}


def fetch(url: str, rng=None) -> bytes:
    headers = {"Range": f"bytes={rng[0]}-{rng[1]}"} if rng else {}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=600) as r:
        return r.read()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="https://cell.ucsf.edu/snPlacenta/build5/stereo_host/stereo_host")
    p.add_argument("--out-dir", required=True, type=Path)
    a = p.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)

    idx_bytes = fetch(a.base + ".jsonl.idx.json")
    index = json.loads(idx_bytes)["index"]

    def get(key):
        t = fetch(a.base + ".jsonl", index[key]).decode()
        return json.loads(t[t.index("{"):])

    schema = get("schema")
    schema = schema.get("schema", schema)
    n = int(schema["shape"][0])
    var_names = {v["id"] if isinstance(v, dict) else v for v in schema["var"]}

    obs = {}
    for field in schema.get("obsCat", []):
        d = get(field)[field]
        obs[field] = np.asarray(d["categories"], dtype=object)[np.asarray(d["values"])]
    obs = pd.DataFrame(obs)
    if len(obs) != n:
        raise AssertionError("obs length does not match schema shape")

    sp = get("spatial")["spatial"]
    xy = np.column_stack([np.asarray(sp["spatial_1"], float), np.asarray(sp["spatial_2"], float)])
    coord_qc = pd.DataFrame({"sample_id": obs.sample_id, "x": xy[:, 0], "y": xy[:, 1]}).groupby("sample_id").agg(
        n_cells=("x", "size"), n_missing_xy=("x", lambda v: int(np.isnan(v).sum())),
        x_min=("x", "min"), x_max=("x", "max"), y_min=("y", "min"), y_max=("y", "max")).reset_index()
    dup = pd.DataFrame(xy).assign(s=obs.sample_id.values).duplicated().sum()

    genes = [g for g in TARGETS + MARKERS + HOUSEKEEPING if g in index]
    value_qc, rows, srows = [], [], []
    M = np.zeros((n, len(genes)), dtype=np.float32)
    for g in genes:
        d = get(g)[g]
        vec = np.zeros(n)
        ind, val = np.asarray(d.get("index", d.get("indices")), int), np.asarray(d.get("value", d.get("values")), float)
        vec[ind] = val
        M[:, genes.index(g)] = vec
        nz = val[val != 0]
        value_qc.append({"gene": g, "n_nonzero": int(nz.size), "min_nonzero": float(nz.min()) if nz.size else np.nan,
                         "max": float(nz.max()) if nz.size else np.nan,
                         "fraction_integer_nonzero": float(np.mean(np.isclose(nz, np.round(nz)))) if nz.size else np.nan})
        df = obs.assign(v=vec, pos=vec > 0)
        for keys, out in (("celltype", rows), ("sample_id", srows)):
            t = df.groupby(keys, observed=True).agg(n_cells=("v", "size"), n_nonzero_explorer=("pos", "sum"),
                                                    mean_explorer_value=("v", "mean")).reset_index()
            t["pct_nonzero_explorer"] = 100 * t.n_nonzero_explorer / t.n_cells
            t.insert(0, "gene", g)
            out.append(t)
        if g in TARGETS:
            ds = df.groupby(["celltype", "sample_id"], observed=True).agg(n=("v", "size"), ne=("pos", "sum")).reset_index()
            ds = ds[ds.n >= 20]
            rep = ds.groupby("celltype").agg(n_samples_evaluable=("n", "size"),
                                              n_samples_nonzero=("ne", lambda x: int((x > 0).sum()))).reset_index()
            rep.insert(0, "gene", g)
            rows[-1] = rows[-1].merge(rep.drop(columns="gene"), on="celltype", how="left")

    ct = pd.concat(rows, ignore_index=True)
    ct.to_csv(a.out_dir / "cp1c_explorer_nonzero_by_celltype.csv", index=False)
    pd.concat(srows, ignore_index=True).to_csv(a.out_dir / "cp1c_explorer_nonzero_by_sample.csv", index=False)

    # Log-normalised counts imply expm1(values) within a nucleus are integer multiples of one unit.
    nnz = (M > 0).sum(1)
    test_cells = np.where(nnz >= 4)[0][:20000]
    consistent = 0
    for i in test_cells:
        v = M[i][M[i] > 0].astype(float)
        e = np.expm1(v)
        r = e / e.min()
        tol = np.maximum((np.expm1(v + 0.005) - np.expm1(v - 0.005)) / e.min(), 0.05)
        consistent += bool(np.all(np.abs(r - np.round(r)) <= tol))
    integer_multiple_test = {"genes": genes, "n_cells_tested": int(len(test_cells)),
                             "fraction_consistent_with_lognormalised_counts":
                                 float(consistent / len(test_cells)) if len(test_cells) else None}
    coord_qc.to_csv(a.out_dir / "cp1c_coordinates_qc_by_sample.csv", index=False)
    comp = obs.groupby(["sample_id", "celltype"], observed=True).size().unstack(fill_value=0)
    comp.to_csv(a.out_dir / "cp1c_celltype_counts_by_sample.csv")

    overall = {g: float(100 * ct[ct.gene == g].n_nonzero_explorer.sum() / n) for g in genes}
    (a.out_dir / "cp1c_run_summary.json").write_text(json.dumps({
        "source": a.base + ".jsonl", "index_sha256": hashlib.sha256(idx_bytes).hexdigest(),
        "shape": schema["shape"], "obs_fields": list(obs.columns), "embeddings": schema.get("embeddings"),
        "layers": schema.get("layers"), "category_levels": schema.get("categoryOrder"),
        "genes_present": {g: g in var_names for g in TARGETS + MARKERS},
        "value_qc": value_qc, "integer_multiple_test": integer_multiple_test,
        "overall_pct_nonzero_explorer": overall, "snRNA_reference_pct_expr": REF_SNRNA,
        "n_duplicate_xy_within_sample": int(dup),
        "notes": "Explorer values are transformed (non-integer, not consistent with log-normalised counts). "
                 "pct_nonzero_explorer is NOT a detection rate. No cell-level data saved.",
    }, indent=2, default=str) + "\n")


if __name__ == "__main__":
    main()
