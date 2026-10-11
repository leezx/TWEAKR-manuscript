#!/usr/bin/env python3
"""Fig. 1c Stage 1, Axis L prediction for cohort v1 epithelial cells (contract v0.3 §3.1).

Each A3a main.h5 (L1 epithelial cells, all Atlas genes) is log1p(CP10k)-normalised with the library
size over all Atlas genes, then mapped to the model genes (absent genes = 0).
Pelka samples use the outer-fold model of their patient (out-of-fold); all other studies use the final
model (fold 0). Pelka cells also get the final-model prediction, for an agreement report only.
No CytoTRACE2 input.
"""
import argparse
import sys
from pathlib import Path

import h5py
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix, csr_matrix

sys.path.insert(0, str(Path(__file__).parent))
from fig1c_axisL_fit import Model, predict  # noqa: E402,F401  (Model needed for unpickling)


def read_main(p):
    with h5py.File(p, "r") as h:
        shape = tuple(h["shape"][:])
        m = csc_matrix((h["data"][:], h["indices"][:], h["indptr"][:]), shape=shape)
        dec = lambda v: [x.decode() if isinstance(x, bytes) else x for x in v]  # noqa: E731
        return m.T.tocsr().astype(np.float32), np.array(dec(h["genes"][:])), np.array(dec(h["cells"][:]))


def to_model_space(x, genes, model_genes):
    lib = np.asarray(x.sum(axis=1)).ravel()
    x = x.multiply((1e4 / np.maximum(lib, 1)).reshape(-1, 1)).tocsc()
    pos = pd.Series(np.arange(len(genes)), index=genes)
    pos = pos[~pos.index.duplicated()]
    idx = pos.reindex(model_genes).values
    have = ~np.isnan(idx)
    cols = np.zeros((x.shape[0], len(model_genes)), dtype=np.float32)
    cols[:, have] = x[:, idx[have].astype(int)].toarray()
    out = csr_matrix(np.log1p(cols))
    return out, float(have.mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts_dir", required=True)
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--folds", required=True)
    ap.add_argument("--task", type=int, required=True, help="1-based index into sorted main.h5 list")
    ap.add_argument("--out_dir", required=True)
    a = ap.parse_args()
    files = sorted(Path(a.counts_dir).glob("*.main.h5"))
    if a.task > len(files):
        return
    f = files[a.task - 1]
    tag = f.name[:-len(".main.h5")]
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    x, genes, cells = read_main(f)
    final = joblib.load(Path(a.model_dir) / "axisL_model_fold0.joblib")
    is_pelka = tag.startswith("Pelka_2021")
    if is_pelka:
        pid = tag.split(".", 1)[1].split("_", 1)[0]
        folds = pd.read_csv(a.folds, sep="\t").set_index("PID").fold
        k = int(folds[pid])
        mdl = joblib.load(Path(a.model_dir) / f"axisL_model_fold{k}.joblib")
    else:
        k, mdl = 0, final
    xm, cov = to_model_space(x, genes, mdl.genes)
    pr = predict(mdl, xm)
    pr.insert(0, "cell_id", cells)
    pr.insert(1, "sample_tag", tag)
    pr["model_fold"], pr["gene_coverage"] = k, cov
    if is_pelka:
        xf, _ = to_model_space(x, genes, final.genes)
        pf = predict(final, xf)
        pr["final_model_lineage"] = pf.lineage.values
    pr.to_csv(out / f"{tag}.axisL.tsv.gz", sep="\t", index=False)
    print(tag, len(pr), k, round(cov, 4))


if __name__ == "__main__":
    main()
