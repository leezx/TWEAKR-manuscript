#!/usr/bin/env python3
"""Step 2 (scvi-env): HVG selection and scVI per lineage, with the C3 convergence check.

Convergence is judged from the loss curves only (never from labels or CytoTRACE2):
no NaN/inf, and either early stopping fired or the mean validation ELBO of the last `window`
epochs is within `max_rel_change` of the mean of the `window` epochs before. If not converged,
retrain from scratch with max_epochs x2, then x4 (cap 400), same seed.
"""
import argparse
import json
import os
import re

import numpy as np
import pandas as pd
import scanpy as sc
import scvi
import torch

from l2_common import LINEAGES, load_cfg, panel_dict, run_paths


def select_genes(adata, cfg, lineage):
    h = cfg["hvg"]
    pats = list(h["exclude_regex"]) + (list(h["exclude_regex_immune"]) if lineage == "Immune" else [])
    rx = re.compile("|".join(pats))
    keep = ~adata.var_names.to_series().str.match(rx).to_numpy()
    tmp = adata[:, keep].copy()
    sc.pp.normalize_total(tmp, target_sum=cfg["normalization"]["target_sum"])
    sc.pp.log1p(tmp)
    sc.pp.highly_variable_genes(tmp, n_top_genes=h["n_top_genes"], flavor=h["flavor"],
                                batch_key=h["batch_key"])
    hvg = list(tmp.var_names[tmp.var.highly_variable])
    forced = set()
    for spec in cfg["l1_flags"]["panels"].values():
        forced |= set(spec["genes"])
    for lin in LINEAGES:
        for pos, neg in panel_dict(cfg, lin).values():
            forced |= set(pos) | set(neg)
    forced = [g for g in sorted(forced) if g in adata.var_names and g not in hvg]
    return hvg + forced, len(hvg), len(forced)


def converged(hist, max_epochs, conv):
    v = hist["elbo_validation"].to_numpy(dtype=float)
    t = hist["elbo_train"].to_numpy(dtype=float)
    finite = bool(np.isfinite(v).all() and np.isfinite(t).all())
    early = len(v) < max_epochs
    w = conv["window"]
    rel = np.nan
    if len(v) >= 2 * w:
        last, prev = v[-w:].mean(), v[-2 * w:-w].mean()
        rel = abs(last - prev) / abs(prev)
    ok = finite and (early or (np.isfinite(rel) and rel <= conv["max_rel_change"]))
    return ok, {"finite": finite, "early_stopped": early, "epochs_run": int(len(v)),
                "rel_change_last_window": None if not np.isfinite(rel) else float(rel)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--lineage", required=True, choices=LINEAGES)
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    P = run_paths(a.run_root)
    s = cfg["scvi"]
    nthreads = int(os.environ.get("NSLOTS", "8"))
    torch.set_num_threads(nthreads)
    scvi.settings.seed = s["seed"]
    scvi.settings.num_threads = nthreads

    adata = sc.read_h5ad(P["objects"] / f"{a.lineage}.h5ad")
    adata = adata[adata.obs.F1.astype(str) != "True"].copy()
    genes, n_hvg, n_forced = select_genes(adata, cfg, a.lineage)
    pd.Series(genes).to_csv(P["scvi"] / f"{a.lineage}_genes.txt", index=False, header=False)
    sub = adata[:, genes].copy()
    del adata
    scvi.model.SCVI.setup_anndata(sub, batch_key=s["batch_key"],
                                  categorical_covariate_keys=s["categorical_covariate_keys"])
    n = sub.n_obs
    base = int(min(400, round(20000 / n * 400)))
    conv = s["convergence"]
    attempts = [base] + [min(conv["max_epochs_cap"], base * m) for m in conv["repair_multipliers"]]
    log = []
    model = None
    for k, E in enumerate(attempts):
        scvi.settings.seed = s["seed"]
        model = scvi.model.SCVI(sub, n_latent=s["n_latent"], n_layers=s["n_layers"],
                                n_hidden=s["n_hidden"], gene_likelihood=s["gene_likelihood"])
        model.train(max_epochs=E, accelerator="cpu", devices=1,
                    train_size=s["train_size"], validation_size=s["validation_size"],
                    early_stopping=s["early_stopping"],
                    early_stopping_monitor=s["early_stopping_monitor"],
                    early_stopping_patience=s["early_stopping_patience"])
        hist = pd.concat([model.history["elbo_train"], model.history["elbo_validation"]], axis=1)
        hist.columns = ["elbo_train", "elbo_validation"]
        hist.to_csv(P["scvi"] / f"{a.lineage}_history_attempt{k}.csv")
        ok, info = converged(hist, E, conv)
        log.append({"attempt": k, "max_epochs": E, "converged": ok, **info})
        print(log[-1], flush=True)
        if ok or E >= conv["max_epochs_cap"]:
            break

    np.save(P["scvi"] / f"{a.lineage}_latent.npy", model.get_latent_representation().astype(np.float32))
    pd.Series(sub.obs_names).to_csv(P["scvi"] / f"{a.lineage}_cells.txt", index=False, header=False)
    model.save(str(P["scvi"] / f"{a.lineage}_model"), overwrite=True)
    json.dump({"lineage": a.lineage, "n_cells": int(n), "n_genes": len(genes), "n_hvg": n_hvg,
               "n_forced": n_forced, "attempts": log, "converged": bool(log[-1]["converged"]),
               "scvi_version": scvi.__version__, "torch_version": torch.__version__,
               "threads": nthreads}, open(P["scvi"] / f"{a.lineage}_convergence.json", "w"), indent=1)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
