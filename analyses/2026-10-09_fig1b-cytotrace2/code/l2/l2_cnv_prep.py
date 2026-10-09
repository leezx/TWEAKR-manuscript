#!/usr/bin/env python3
"""Step 3a (r4p3): per-patient infercnv inputs.

Observations: the patient's non-flagged (F1, F2) epithelial cells. Reference: the patient's
non-flagged immune and stromal cells, subsampled (seed 0) to <= ref_max_cells, half immune and
half stromal where possible. Patients with < ref_min_cells reference cells are "not assessable".
Genes: autosomes only, ordered by Atlas position.
"""
import argparse
import gzip
import re

import numpy as np
import pandas as pd
import scanpy as sc
from scipy import io
from scipy import sparse as sp

from l2_common import LINEAGES, load_cfg, run_paths


def chrom_num(x):
    m = re.fullmatch(r"(?:chr)?(\d+)", str(x))
    return int(m.group(1)) if m and 1 <= int(m.group(1)) <= 22 else None


def safe(x):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--run-root", required=True)
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    P = run_paths(a.run_root)
    c = cfg["infercnv"]
    rng = np.random.default_rng(c["seed"])

    objs = {}
    for L in LINEAGES:
        o = sc.read_h5ad(P["objects"] / f"{L}.h5ad")
        lab = pd.read_csv(P["labels"] / f"{L}_labels.tsv.gz", sep="\t", usecols=["cell_id", "F2"])
        keep = lab.loc[lab.F2.astype(str) != "True", "cell_id"].astype(str)  # F1 cells are absent
        objs[L] = o[o.obs_names.isin(keep)]
    var = objs["Epithelial"].var.copy()
    var["chr"] = var.Chromosome.map(chrom_num)
    var["start"] = pd.to_numeric(var.Start, errors="coerce")
    var["end"] = pd.to_numeric(var.End, errors="coerce")
    var = var[var.chr.notna() & var.start.notna()].sort_values(["chr", "start"])
    genes = var.index.to_numpy()
    gorder = pd.DataFrame({"gene": genes, "chr": "chr" + var.chr.astype(int).astype(str),
                           "start": var.start.astype(int), "end": var.end.fillna(var.start).astype(int)})
    gorder.to_csv(P["cnv"] / "gene_order.tsv", sep="\t", index=False, header=False)

    rows = []
    patients = sorted(objs["Epithelial"].obs.patient_id.unique())
    for pid in patients:
        epi = objs["Epithelial"][(objs["Epithelial"].obs.patient_id == pid).to_numpy()]
        ref = {}
        for L in ["Immune", "Stromal"]:
            o = objs[L]
            ref[L] = o[(o.obs.patient_id == pid).to_numpy()]
        n_avail = {L: ref[L].n_obs for L in ref}
        half = c["ref_max_cells"] // 2
        take = {L: min(n_avail[L], half) for L in ref}
        spare = c["ref_max_cells"] - sum(take.values())
        for L in ref:  # give unused quota to the other lineage
            extra = min(spare, n_avail[L] - take[L])
            take[L] += extra
            spare -= extra
        n_ref = sum(take.values())
        rec = {"patient_id": pid, "study_id": epi.obs.study_id.iat[0] if epi.n_obs else "",
               "n_obs": int(epi.n_obs), "n_ref_immune": take["Immune"], "n_ref_stromal": take["Stromal"],
               "assessable": bool(n_ref >= c["ref_min_cells"] and epi.n_obs > 0),
               "dir": safe(pid)}
        rows.append(rec)
        if not rec["assessable"]:
            continue
        parts, groups = [epi[:, genes]], ["obs"] * epi.n_obs
        for L, grp in [("Immune", "ref_immune"), ("Stromal", "ref_stromal")]:
            if take[L] == 0:
                continue
            sel = np.sort(rng.choice(n_avail[L], take[L], replace=False))
            parts.append(ref[L][sel][:, genes])
            groups += [grp] * take[L]
        d = P["cnv"] / "inputs" / rec["dir"]
        d.mkdir(parents=True, exist_ok=True)
        cells = np.concatenate([p.obs_names.to_numpy() for p in parts])
        M = sp.vstack([p.X for p in parts]).T.tocsr()  # genes x cells
        with gzip.open(d / "counts.mtx.gz", "wb") as fh:
            io.mmwrite(fh, M.astype(np.float32), field="real")
        pd.Series(cells).to_csv(d / "cells.txt", index=False, header=False)
        pd.DataFrame({"cell": cells, "group": groups}).to_csv(d / "annotation.tsv", sep="\t",
                                                               index=False, header=False)
        print(pid, epi.n_obs, n_ref, flush=True)
    pd.Series(genes).to_csv(P["cnv"] / "genes.txt", index=False, header=False)
    man = pd.DataFrame(rows)
    man.to_csv(P["cnv"] / "patients.tsv", sep="\t", index=False)
    man[man.assessable].to_csv(P["cnv"] / "tasks.tsv", sep="\t", index=False)
    print("tasks", int(man.assessable.sum()), "of", len(man), flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
