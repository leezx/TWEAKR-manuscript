#!/usr/bin/env python3
"""Fig. 1c Stage 1, Axis L input (contract v0.3 §3.1): Pelka 2021 epithelial reference + frozen outer folds.

Keeps Pelka cells with clTopLevel == Epi and labels cE01-cE11 (tumour and normal), restricted to the
Pelka ∩ Atlas gene space. Library size (for CP10k) is taken over ALL Pelka genes before restriction.
Outer folds: unique Pelka PIDs shuffled with seed 14, fold = rank % 5 + 1 (all samples of a patient,
normal and tumour, share one fold).
Outputs: ref_counts.npz (cells x genes CSR), ref_meta.tsv, ref_genes.txt, pelka_outer_folds.tsv.
"""
import argparse
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix, save_npz

LABELS = [f"cE{i:02d}" for i in range(1, 12)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5", required=True)
    ap.add_argument("--cluster", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--atlas_main_h5", required=True, help="any A3a main.h5 (Atlas gene space)")
    ap.add_argument("--out_dir", required=True)
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    cl = pd.read_csv(a.cluster)
    cl = cl[(cl.clTopLevel == "Epi") & cl.cl295v11SubShort.isin(LABELS)]
    mt = pd.read_csv(a.meta, usecols=["cellID", "SPECIMEN_TYPE", "PID", "MMRStatus"])
    cl = cl.merge(mt, left_on="sampleID", right_on="cellID", how="left")
    assert cl.PID.notna().all()

    with h5py.File(a.atlas_main_h5, "r") as h:
        atlas = {g.decode() if isinstance(g, bytes) else g for g in h["genes"][:]}

    with h5py.File(a.h5, "r") as f:
        m = f["matrix"]
        bc = np.array([b.decode() for b in m["barcodes"][:]])
        genes = np.array([g.decode() for g in m["features/name"][:]])
        pos = pd.Series(np.arange(len(bc)), index=bc)
        cols = pos.loc[cl.sampleID.values].values
        order = np.argsort(cols)
        cols, cl = cols[order], cl.iloc[order].reset_index(drop=True)
        indptr = m["indptr"][:]
        parts = []
        block = 20000
        for b0 in range(0, len(bc), block):  # block reads; keep only epithelial columns
            b1 = min(b0 + block, len(bc))
            sel = cols[(cols >= b0) & (cols < b1)]
            if len(sel) == 0:
                continue
            lo, hi = indptr[b0], indptr[b1]
            blk = csc_matrix((m["data"][lo:hi].astype(np.float32), m["indices"][lo:hi], indptr[b0:b1 + 1] - lo),
                             shape=(len(genes), b1 - b0))
            parts.append(blk[:, sel - b0])
        from scipy.sparse import hstack
        x = hstack(parts).tocsc()
    lib = np.asarray(x.sum(axis=0)).ravel()
    # duplicate symbols in the 10x feature list: keep the first occurrence
    keep = ~pd.Series(genes).duplicated().values & np.isin(genes, list(atlas))
    x = x[keep].T.tocsr()
    save_npz(out / "ref_counts.npz", x)
    (out / "ref_genes.txt").write_text("\n".join(genes[keep]) + "\n")
    meta = pd.DataFrame({"cell": cl.sampleID, "batch": cl.batchID, "label": cl.cl295v11SubShort,
                         "label_full": cl.cl295v11SubFull, "PID": cl.PID, "tissue": cl.SPECIMEN_TYPE,
                         "MMR": cl.MMRStatus, "lib_all_genes": lib})
    meta.to_csv(out / "ref_meta.tsv", sep="\t", index=False)
    pids = np.array(sorted(meta.PID.unique()))
    rng = np.random.default_rng(14)
    pids = pids[rng.permutation(len(pids))]
    folds = pd.DataFrame({"PID": pids, "fold": np.arange(len(pids)) % 5 + 1})
    folds.to_csv(out / "pelka_outer_folds.tsv", sep="\t", index=False)
    print(f"cells={x.shape[0]} genes_kept={x.shape[1]}/{len(genes)} patients={len(pids)}")
    print(meta.groupby(["label", "tissue"]).size().unstack(fill_value=0).to_string())
    print(folds.groupby("fold").size().to_string())


if __name__ == "__main__":
    main()
