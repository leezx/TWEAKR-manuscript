#!/usr/bin/env python3
"""A3b Stage I step 3: Evidence N, normal-mucosa similarity (contract A3b v0.3 §2). One SGE task per study.
No CT2, no programme score; programme genes are excluded from the feature space.

Reference pool R: normal-side L1 epithelium of the study, stage naive/Pre; studies without any such normal
sample (Li, Qin) use their post-treatment normals (flagged). Reference patient: >= 30 normal-side cells; each
contributes <= 300 cells (per-patient RNG, seed 0).
For a model fitted on a reference patient set S: log1p(CP10k, library over all genes) -> exclude genes ->
2,000 HVGs (scanpy flavor 'seurat') on S -> z-scale with S mean/SD, clip +-10 -> 30-PC PCA on S -> kNN (k=15).
d(cell) = mean Euclidean distance to the 15 nearest S cells.
Query patient p: S = R \\ {p}; all of p's cells are scored. Null for p: for every q in R \\ {p}, the full
preprocessing is refitted on R \\ {p, q} and q's capped cells are scored against it (fully model-held-out);
tau_p = 90th percentile of the pooled null with each q weighted equally. normal_like_N = d <= tau_p.
Study gate: >= 5 reference patients, and median over reference patients of the share of their own normal-side
cells with d <= tau_p >= 0.75; otherwise N not assessable for the study.
Outputs: <root>/evidenceN/<study>.N.private.tsv.gz (per cell), <root>/evidenceN/<study>.N_calibration.tsv.
"""
import argparse
import re
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad
from scipy import sparse as sp
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

N_HVG, N_PC, K, CAP, MIN_REF_CELLS, MIN_REF_PAT, Q, GATE = 2000, 30, 15, 300, 30, 5, 0.90, 0.75


def safe(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", s)


def load_h5(path):
    with h5py.File(path, "r") as h:
        m = sp.csc_matrix((h["data"][:], h["indices"][:], h["indptr"][:]), shape=tuple(h["shape"][:]))
        genes = np.array([g.decode() for g in h["genes"][:]])
        cells = np.array([c.decode() for c in h["cells"][:]])
    return m.T.tocsr().astype(np.float32), genes, cells


def wquantile(x, w, q):
    o = np.argsort(x)
    cw = np.cumsum(w[o]) / w.sum()
    return float(x[o][np.searchsorted(cw, q)])


class Model:
    def __init__(self, X):
        a = ad.AnnData(X)
        sc.pp.highly_variable_genes(a, n_top_genes=N_HVG, flavor="seurat")
        self.hv = np.flatnonzero(a.var.highly_variable.to_numpy())
        Z = X[:, self.hv].toarray()
        self.mu = Z.mean(0)
        self.sd = Z.std(0)
        self.sd[self.sd == 0] = 1
        self.pca = PCA(n_components=N_PC, svd_solver="full").fit(self._z(Z))
        self.nn = NearestNeighbors(n_neighbors=K).fit(self.pca.transform(self._z(Z)))

    def _z(self, Z):
        return np.clip((Z - self.mu) / self.sd, -10, 10)

    def dist(self, X):
        d, _ = self.nn.kneighbors(self.pca.transform(self._z(X[:, self.hv].toarray())))
        return d.mean(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--study", required=True)
    ap.add_argument("--exclude", nargs="+", required=True, help="gene list files (one gene per line or set\\tgene)")
    a = ap.parse_args()
    R = Path(a.root)
    out = R / "evidenceN"
    out.mkdir(exist_ok=True)
    cells = pd.read_csv(R / "export/cells" / f"{safe(a.study)}.epi_cells.tsv.gz", sep="\t")

    excl = set()
    for f in a.exclude:
        t = pd.read_csv(f, sep="\t", header=None, dtype=str)
        excl |= set(t.iloc[:, -1].str.strip())
    Xs, cid = [], []
    genes = None
    for s in sorted(cells.sample_id.unique()):
        x, g, c = load_h5(R / "export/counts" / f"{safe(s)}.epi.h5")
        if genes is None:
            genes = g
        elif not np.array_equal(genes, g):
            raise ValueError("gene order differs")
        lib = np.asarray(x.sum(1)).ravel()
        lib[lib == 0] = 1
        x = sp.diags(1e4 / lib) @ x
        x.data = np.log1p(x.data)
        Xs.append(x.tocsr()); cid.append(c)
    X = sp.vstack(Xs).tocsr()
    cid = np.concatenate(cid)
    keep = ~(pd.Series(genes).isin(excl) | pd.Series(genes).str.match(r"^(MT-|RP[SL]|HB[AB])")).to_numpy()
    X = X[:, np.flatnonzero(keep)]
    print(a.study, "cells", X.shape[0], "genes kept", int(keep.sum()), "excluded", int((~keep).sum()), flush=True)
    meta = cells.set_index("cell_id").loc[cid].reset_index()

    nrm = meta.side.eq("normal")
    ref_mask = nrm & meta.stage.isin(["naive", "Pre"])
    ref_flag = "naive_or_pre_normals"
    if not ref_mask.any():
        ref_mask, ref_flag = nrm.copy(), "post_treatment_normals"
    cnt = meta[ref_mask].groupby("patient_id").size()
    refs = sorted(cnt[cnt >= MIN_REF_CELLS].index)
    cap = {}
    for p in refs:
        ii = np.flatnonzero((ref_mask & meta.patient_id.eq(p)).to_numpy())
        rng = np.random.default_rng(0)
        cap[p] = np.sort(rng.choice(ii, min(CAP, len(ii)), replace=False))
    status = "assessable" if len(refs) >= MIN_REF_PAT else "not_assessable_few_refs"
    print("reference patients", len(refs), ref_flag, status, flush=True)

    cache = {}

    def model(excluded):
        key = frozenset(excluded)
        if key not in cache:
            rows = np.concatenate([cap[q] for q in refs if q not in key])
            cache[key] = Model(X[rows])
        return cache[key]

    d = np.full(X.shape[0], np.nan)
    tau = np.full(X.shape[0], np.nan)
    calib = []
    if len(refs) >= 3:  # need >= 2 reference patients left for a null
        for p in sorted(meta.patient_id.unique()):
            pi = np.flatnonzero(meta.patient_id.eq(p).to_numpy())
            d[pi] = model({p}).dist(X[pi])
            nulls, w = [], []
            for q in refs:
                if q == p:
                    continue
                dq = model({p, q}).dist(X[cap[q]])
                nulls.append(dq); w.append(np.full(len(dq), 1.0 / len(dq)))
            tau[pi] = wquantile(np.concatenate(nulls), np.concatenate(w), Q)
            own = pi[(ref_mask.to_numpy() | nrm.to_numpy())[pi]]
            calib.append(dict(study_id=a.study, patient_id=p, is_reference=p in refs, tau=tau[pi[0]],
                              n_cells=len(pi), n_own_normal=len(own),
                              own_normal_like=float((d[own] <= tau[own]).mean()) if len(own) else np.nan))
            print(p, len(pi), round(tau[pi[0]], 3), flush=True)
    cal = pd.DataFrame(calib)
    med = cal.loc[cal.is_reference & (cal.n_own_normal >= MIN_REF_CELLS), "own_normal_like"].median() if len(cal) else np.nan
    if status == "assessable" and not (med >= GATE):
        status = "not_assessable_calibration"
    cal["study_median_own_normal_like"] = med
    cal["N_status"] = status
    cal["reference_pool"] = ref_flag
    cal["n_reference_patients"] = len(refs)
    cal.to_csv(out / f"{safe(a.study)}.N_calibration.tsv", sep="\t", index=False)
    pd.DataFrame({"cell_id": cid, "N_dist": d, "N_tau": tau, "N_normal_like": d <= tau,
                  "N_status": status, "N_reference_pool": ref_flag}).to_csv(
        out / f"{safe(a.study)}.N.private.tsv.gz", sep="\t", index=False)
    print("DONE", a.study, status, "median own-normal normal-like", med, flush=True)


if __name__ == "__main__":
    main()
