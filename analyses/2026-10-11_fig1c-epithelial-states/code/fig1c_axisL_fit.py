#!/usr/bin/env python3
"""Fig. 1c Stage 1, Axis L (contract v0.3 §3.1): nested patient-grouped lineage classifier on Pelka.

--fold k (1-5): train on all outer folds except k; predict the held-out fold (OOF), plus the
  tumour-only-training sensitivity and leave-one-aggregated-class-out (LOCO) unknown-rejection test.
--fold 0: final model on all Pelka patients (same procedure), used for the 12 non-Pelka studies.

Procedure inside a training set (all steps use only training patients):
  calibration patients = 20% of training patients (seeded); inner = the remaining 80%;
  inner cells capped at 8,000 per original label (seed 14);
  features = Pelka∩Atlas genes minus holdout H; log1p(CP10k) with CP10k over all genes;
  top 2,000 HVGs by variance on the capped inner cells; z-scale with inner mean/SD, clip ±10;
  C ∈ {0.01, 0.1, 1} by 3-fold patient-grouped CV (macro-F1) on the capped inner cells;
  L2 multinomial logistic regression, class_weight=balanced, refit on the capped inner cells;
  temperature scaling fitted (NLL) on calibration cells (capped 8,000 per label);
  OOD: 50 PCs on scaled inner cells; mean distance to 15 nearest inner cells; percentile against the
  calibration-cell distribution.
Assignment (fixed a priori): aggregated max-p ≥ 0.70, margin ≥ 0.20, OOD percentile ≤ 99,
otherwise "lineage-unresolved".
No CytoTRACE2 input.
"""
import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.sparse import load_npz
from scipy.special import log_softmax, softmax
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.neighbors import NearestNeighbors

LABELS = [f"cE{i:02d}" for i in range(1, 12)]
AGG = {"cE01": "Stem/TA-like", "cE02": "Transitional stem/secretory", "cE03": "Cycling Stem/TA",
       "cE04": "Absorptive differentiated-like", "cE05": "Absorptive differentiated-like",
       "cE06": "Secretory differentiated-like", "cE08": "Secretory differentiated-like",
       "cE07": "Transitional secretory/absorptive",
       "cE09": "Rare lineages", "cE10": "Rare lineages", "cE11": "Rare lineages"}
AGG_CLASSES = list(dict.fromkeys(AGG.values()))
CAP, N_HVG, CS, SEED = 8000, 2000, [0.01, 0.1, 1.0], 14
MAXP, MARGIN, OODP = 0.70, 0.20, 99.0


def lognorm(x_counts, lib):
    x = x_counts.multiply((1e4 / np.maximum(lib, 1)).reshape(-1, 1)).tocsr()
    x.data = np.log1p(x.data)
    return x


def cap_idx(idx, labels, rng):
    keep = []
    for lab in np.unique(labels[idx]):
        i = idx[labels[idx] == lab]
        keep.append(rng.choice(i, CAP, replace=False) if len(i) > CAP else i)
    return np.sort(np.concatenate(keep))


class Model:
    pass


def transform(mdl, xlog):
    z = (xlog[:, mdl.hvg].toarray() - mdl.mu) / mdl.sd
    return np.clip(z, -10, 10).astype(np.float32)


def fit(xlog, labels, pids, train_idx, seed, fixed_C=None, exclude_labels=()):
    rng = np.random.default_rng(seed)
    train_idx = train_idx[~np.isin(labels[train_idx], list(exclude_labels))]
    up = np.unique(pids[train_idx])
    calib_p = set(rng.choice(up, max(1, int(round(0.2 * len(up)))), replace=False))
    is_cal = np.isin(pids[train_idx], list(calib_p))
    inner = cap_idx(train_idx[~is_cal], labels, rng)
    calib = cap_idx(train_idx[is_cal], labels, rng)
    m = Model()
    xi = xlog[inner]
    mean = np.asarray(xi.mean(axis=0)).ravel()
    var = np.asarray(xi.multiply(xi).mean(axis=0)).ravel() - mean ** 2
    m.hvg = np.sort(np.argsort(-var)[:N_HVG])
    sub = xi[:, m.hvg].toarray()
    m.mu, m.sd = sub.mean(axis=0), sub.std(axis=0) + 1e-6
    zi = transform(m, xi)
    yi = labels[inner]
    if fixed_C is None:
        scores = {}
        for C in CS:
            f1s = []
            for tr, te in GroupKFold(3).split(zi, yi, pids[inner]):
                clf = LogisticRegression(C=C, max_iter=500, class_weight="balanced", n_jobs=-1)
                clf.fit(zi[tr], yi[tr])
                f1s.append(f1_score(yi[te], clf.predict(zi[te]), average="macro"))
            scores[C] = float(np.mean(f1s))
        m.C, m.cv_scores = max(scores, key=scores.get), scores
    else:
        m.C, m.cv_scores = fixed_C, None
    m.clf = LogisticRegression(C=m.C, max_iter=1000, class_weight="balanced", n_jobs=-1).fit(zi, yi)
    zc = transform(m, xlog[calib])
    lc = m.clf.decision_function(zc)
    yc = np.searchsorted(m.clf.classes_, labels[calib])
    ok = np.isin(labels[calib], m.clf.classes_)

    def nll(logt):
        lp = log_softmax(lc[ok] / np.exp(logt), axis=1)
        return -lp[np.arange(ok.sum()), yc[ok]].mean()
    m.T = float(np.exp(minimize_scalar(nll, bounds=(-3, 3), method="bounded").x))
    m.pca = PCA(50, random_state=SEED).fit(zi)
    pi = m.pca.transform(zi)
    m.nn = NearestNeighbors(n_neighbors=15).fit(pi)
    m.cal_dist = np.sort(m.nn.kneighbors(m.pca.transform(zc))[0].mean(axis=1))
    m.n_inner, m.n_calib, m.n_calib_patients = len(inner), len(calib), len(calib_p)
    return m


def predict(m, xlog):
    z = transform(m, xlog)
    p = softmax(m.clf.decision_function(z) / m.T, axis=1)
    p11 = pd.DataFrame(p, columns=m.clf.classes_)
    agg = pd.DataFrame({c: p11[[k for k in p11.columns if AGG[k] == c]].sum(axis=1) if
                        any(AGG[k] == c for k in p11.columns) else 0.0 for c in AGG_CLASSES})
    srt = np.sort(agg.values, axis=1)
    d = m.nn.kneighbors(m.pca.transform(z))[0].mean(axis=1)
    oodp = 100.0 * np.searchsorted(m.cal_dist, d, side="right") / len(m.cal_dist)
    out = pd.DataFrame({"pred11": p11.idxmax(axis=1).values, "pred_agg": agg.idxmax(axis=1).values,
                        "maxp_agg": srt[:, -1], "margin_agg": srt[:, -1] - srt[:, -2],
                        "maxp11": p11.max(axis=1).values, "ood_pct": oodp})
    out["assigned"] = (out.maxp_agg >= MAXP) & (out.margin_agg >= MARGIN) & (out.ood_pct <= OODP)
    out["lineage"] = np.where(out.assigned, out.pred_agg, "lineage-unresolved")
    for c in AGG_CLASSES:
        out[f"p_{c}"] = agg[c].values
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref_dir", required=True)
    ap.add_argument("--holdout", required=True, help="file with one holdout gene per line (H)")
    ap.add_argument("--fold", type=int, required=True)
    ap.add_argument("--out_dir", required=True)
    a = ap.parse_args()
    ref, out = Path(a.ref_dir), Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    x = load_npz(ref / "ref_counts.npz").tocsr()
    genes = np.array(ref.joinpath("ref_genes.txt").read_text().split())
    meta = pd.read_csv(ref / "ref_meta.tsv", sep="\t")
    folds = pd.read_csv(ref / "pelka_outer_folds.tsv", sep="\t")
    meta = meta.merge(folds, on="PID", how="left")
    H = {l.strip() for l in open(a.holdout) if l.strip()}
    gkeep = ~np.isin(genes, list(H))
    xlog = lognorm(x, meta.lib_all_genes.values)[:, gkeep].tocsr()
    genes = genes[gkeep]
    labels, pids = meta.label.values, meta.PID.values
    k = a.fold
    train = np.where(meta.fold.values != k)[0] if k > 0 else np.arange(len(meta))
    m = fit(xlog, labels, pids, train, SEED + k)
    m.genes = genes
    joblib.dump(m, out / f"axisL_model_fold{k}.joblib", compress=3)
    info = {"fold": k, "C": m.C, "cv_scores": m.cv_scores, "T": m.T, "n_inner": int(m.n_inner),
            "n_calib": int(m.n_calib), "n_calib_patients": int(m.n_calib_patients), "n_features": int(len(genes))}
    if k > 0:
        test = np.where(meta.fold.values == k)[0]
        pr = predict(m, xlog[test])
        pr.insert(0, "cell", meta.cell.values[test])
        pr["true11"], pr["true_agg"] = labels[test], [AGG[l] for l in labels[test]]
        pr["tissue"], pr["PID"], pr["fold"] = meta.tissue.values[test], pids[test], k
        pr.to_csv(out / f"oof_fold{k}.tsv.gz", sep="\t", index=False)
        # tumour-only training sensitivity (same outer split; C fixed to the main fold choice)
        tt = train[meta.tissue.values[train] == "T"]
        mt = fit(xlog, labels, pids, tt, SEED + 100 + k, fixed_C=m.C)
        te = test[meta.tissue.values[test] == "T"]
        pt = predict(mt, xlog[te])
        pt.insert(0, "cell", meta.cell.values[te])
        pt["true_agg"] = [AGG[l] for l in labels[te]]
        pt.to_csv(out / f"tumouronly_fold{k}.tsv.gz", sep="\t", index=False)
        # leave-one-aggregated-class-out unknown rejection
        loco = []
        for c in AGG_CLASSES:
            excl = [l for l in LABELS if AGG[l] == c]
            ml = fit(xlog, labels, pids, train, SEED + 200 + k, fixed_C=m.C, exclude_labels=excl)
            pl = predict(ml, xlog[test])
            y = np.isin(labels[test], excl).astype(int)
            if 0 < y.sum() < len(y):
                loco.append({"fold": k, "held_out_class": c, "n_unknown": int(y.sum()),
                             "auroc_1_minus_maxp": roc_auc_score(y, 1 - pl.maxp_agg),
                             "auroc_ood_pct": roc_auc_score(y, pl.ood_pct),
                             "unknown_rejected_frac": float((~pl.assigned[y == 1]).mean()),
                             "known_rejected_frac": float((~pl.assigned[y == 0]).mean())})
        pd.DataFrame(loco).to_csv(out / f"loco_fold{k}.tsv", sep="\t", index=False)
    (out / f"axisL_fold{k}.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


if __name__ == "__main__":
    main()
