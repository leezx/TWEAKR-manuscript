#!/usr/bin/env python3
"""Step 4 (r4p3): clustering, F2 flags, marker scores, calls (a)(b)(c), marker-consensus, checks.

Per lineage. Input: lineage H5AD (step 1) and scVI latent (step 2). No CytoTRACE2 input.
For Epithelial the consensus uses the normal-type panels; malignancy is applied in step 5.
"""
import argparse
import json

import anndata as ad
import harmonypy
import numpy as np
import pandas as pd
import scanpy as sc
from pynndescent import NNDescent
from scipy import sparse
from sklearn.metrics import adjusted_rand_score

from l2_common import (LINEAGES, call_top, consensus, load_cfg, panel_dict, read_gmt,
                       run_paths)


def scores_within_study(adata, gene_sets, cfg):
    """score_genes for every gene set, computed separately within each study."""
    lab = cfg["labelling"]["score_genes"]
    out = pd.DataFrame(np.nan, index=adata.obs_names, columns=list(gene_sets))
    for s in adata.obs.study_id.unique():
        m = (adata.obs.study_id == s).to_numpy()
        sub = adata[m].copy()
        for name, genes in gene_sets.items():
            g = [x for x in genes if x in sub.var_names]
            if not g:
                continue
            sc.tl.score_genes(sub, g, ctrl_size=lab["ctrl_size"], n_bins=lab["n_bins"],
                              random_state=lab["seed"], score_name="_s", use_raw=False)
            out.loc[sub.obs_names, name] = sub.obs["_s"].to_numpy()
        print("scored", s, flush=True)
    return out


def cluster_call(scores, clusters, lab):
    means = scores.groupby(clusters.to_numpy()).mean()
    calls = call_top(means, lab["min_score"], lab["min_margin"])
    return clusters.map(calls).to_numpy(dtype=object), means.assign(call=calls)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--lineage", required=True, choices=LINEAGES)
    ap.add_argument("--revcsc-gmt", required=True)
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    P = run_paths(a.run_root)
    L, lab, cl = a.lineage, cfg["labelling"], cfg["clustering"]

    adata = sc.read_h5ad(P["objects"] / f"{L}.h5ad")
    cells = pd.read_csv(P["scvi"] / f"{L}_cells.txt", header=None)[0].astype(str)
    adata = adata[cells.to_numpy()].copy()
    adata.obsm["X_scVI"] = np.load(P["scvi"] / f"{L}_latent.npy")
    l1 = pd.read_csv(P["cells"] / "l1_cells.tsv.gz", sep="\t", usecols=["cell_id", "marker_lineage_L1"])
    adata.obs["marker_lineage_L1"] = l1.set_index("cell_id").marker_lineage_L1.reindex(adata.obs_names).to_numpy()

    # panel-gene detection (for marker specificity in step 5), before normalization
    panels = panel_dict(cfg, L)
    pg = sorted({g for pos, neg in panels.values() for g in pos} & set(adata.var_names))
    det = sparse.csr_matrix(adata[:, pg].X > 0)
    sparse.save_npz(P["labels"] / f"{L}_panel_detection.npz", det)
    pd.Series(pg).to_csv(P["labels"] / f"{L}_panel_detection_genes.txt", index=False, header=False)

    sc.pp.normalize_total(adata, target_sum=cfg["normalization"]["target_sum"])
    sc.pp.log1p(adata)

    # clustering
    sc.pp.neighbors(adata, n_neighbors=cl["n_neighbors"], use_rep="X_scVI", random_state=cl["seed"])
    for r in cl["resolutions"]:
        sc.tl.leiden(adata, resolution=r, key_added=f"leiden_r{r}", random_state=cl["seed"])
        print("leiden", r, adata.obs[f"leiden_r{r}"].nunique(), flush=True)
    key = f"leiden_r{cl['labelling_resolution']}"

    # F2: cluster where > f2_foreign_fraction of cells have a different independent lineage
    ml = adata.obs.marker_lineage_L1
    foreign = (ml.notna() & (ml != L)).to_numpy()
    fr = pd.Series(foreign, index=adata.obs_names).groupby(adata.obs[key].to_numpy()).mean()
    f2_clusters = set(fr.index[fr > cfg["l1_flags"]["f2_foreign_fraction"]])
    adata.obs["F2"] = adata.obs[key].isin(f2_clusters).to_numpy()
    fr.rename("foreign_fraction").to_csv(P["labels"] / f"{L}_F2_cluster_foreign_fraction.csv")

    # per-cell panel scores (within study), negative genes subtracted; L3 programme scores
    sets = {}
    for name, (pos, neg) in panels.items():
        sets[f"pos|{name}"] = pos
        if neg:
            sets[f"neg|{name}"] = neg
    progs = dict(cfg["l3"]["programmes"])
    if L == "Epithelial":
        progs.update(read_gmt(a.revcsc_gmt))
    for name, genes in progs.items():
        sets[f"L3_{name}"] = genes
    R = scores_within_study(adata, sets, cfg)
    S = pd.DataFrame(index=adata.obs_names)
    for name, (pos, neg) in panels.items():
        S[name] = R[f"pos|{name}"] - (R[f"neg|{name}"] if neg else 0)
    L3 = R[[c for c in R.columns if c.startswith("L3_")]]

    ok = ~adata.obs.F2.to_numpy()
    call_c = call_top(S, lab["min_score"], lab["min_margin"]).to_numpy(dtype=object)
    calls_a = {}
    for r in cl["resolutions"]:
        calls_a[r], means = cluster_call(S, adata.obs[f"leiden_r{r}"], lab)
        if r == cl["labelling_resolution"]:
            means.to_csv(P["labels"] / f"{L}_cluster_panel_means_r{r}.csv")
    call_a = calls_a[cl["labelling_resolution"]]

    # (b) kNN vote of crosswalked Atlas fine labels (self excluded, non-null neighbours only)
    xw = cfg["atlas_fine_to_L2"]
    mapped = adata.obs.atlas_cell_type_fine.astype(str).map(lambda x: xw.get(x)).to_numpy(dtype=object)
    k = lab["transfer_k"]
    idx = NNDescent(adata.obsm["X_scVI"], n_neighbors=k + 1, random_state=0).neighbor_graph[0][:, 1:]
    nb = mapped[idx]
    call_b = np.full(adata.n_obs, None, dtype=object)
    share_b = np.zeros(adata.n_obs)
    for i in range(adata.n_obs):
        v = [x for x in nb[i] if x is not None]
        if v:
            u, c = np.unique(np.array(v, dtype=object), return_counts=True)
            j = c.argmax()
            share_b[i] = c[j] / len(v)
            if share_b[i] >= lab["transfer_min_share"]:
                call_b[i] = u[j]

    label, conf, method = consensus(call_a, call_b, call_c)
    label[~ok], conf[~ok], method[~ok] = None, "flagged", "F2"

    # stability: consensus with (a) from other resolutions
    stab = {}
    for r in cl["resolutions"]:
        if r == cl["labelling_resolution"]:
            continue
        lr, _, _ = consensus(calls_a[r], call_b, call_c)
        same = (pd.Series(lr[ok]).fillna("NA").to_numpy() == pd.Series(label[ok]).fillna("NA").to_numpy())
        stab[f"consensus_unchanged_r{r}"] = float(same.mean())

    # Harmony check (comparison only)
    genes = pd.read_csv(P["scvi"] / f"{L}_genes.txt", header=None)[0].tolist()
    h = cfg["harmony"]
    hv = adata[:, genes].copy()
    sc.pp.scale(hv, max_value=10)
    sc.tl.pca(hv, n_comps=h["n_pcs"], random_state=h["seed"])
    ho = harmonypy.run_harmony(hv.obsm["X_pca"], hv.obs, [h["key"]], theta=h["theta"],
                               random_state=h["seed"], verbose=False)
    Z = np.asarray(ho.Z_corr)
    hv.obsm["X_harmony"] = Z.T if Z.shape[0] != hv.n_obs else Z
    sc.pp.neighbors(hv, n_neighbors=cl["n_neighbors"], use_rep="X_harmony", random_state=cl["seed"])
    sc.tl.leiden(hv, resolution=cl["labelling_resolution"], key_added="leiden_h", random_state=cl["seed"])
    stab["ARI_scvi_vs_harmony_leiden"] = float(adjusted_rand_score(adata.obs[key], hv.obs.leiden_h))
    stab["n_clusters"] = {str(r): int(adata.obs[f"leiden_r{r}"].nunique()) for r in cl["resolutions"]}
    stab["n_clusters_harmony"] = int(hv.obs.leiden_h.nunique())
    stab["n_F2_clusters"] = len(f2_clusters)
    stab["n_F2_cells"] = int((~ok).sum())
    json.dump(stab, open(P["labels"] / f"{L}_checks.json", "w"), indent=1)

    out = pd.DataFrame({"cell_id": adata.obs_names, "F2": ~ok,
                        "call_a": call_a, "call_b": call_b, "share_b": share_b.round(3),
                        "call_c": call_c, "consensus": label, "confidence": conf, "method": method})
    for r in cl["resolutions"]:
        out[f"leiden_r{r}"] = adata.obs[f"leiden_r{r}"].to_numpy()
    out = pd.concat([out.reset_index(drop=True), S.add_prefix("score_").reset_index(drop=True).round(4),
                     L3.reset_index(drop=True).round(4)], axis=1)
    out.to_csv(P["labels"] / f"{L}_labels.tsv.gz", sep="\t", index=False)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
