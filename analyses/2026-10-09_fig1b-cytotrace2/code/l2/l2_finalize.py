#!/usr/bin/env python3
"""Step 5 (r4p3): malignancy calls, final L2, LOSO, light tables, annotation table + SHA256.

Malignancy (approved rule, unchanged) and the C1 sensitivity class `putative non-malignant
epithelial`. LOSO = cross-study label reproducibility on the jointly trained scVI latent.
No CytoTRACE2 input.
"""
import argparse
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from pynndescent import NNDescent  # noqa: E402
from scipy import sparse  # noqa: E402

from l2_common import LINEAGES, load_cfg, run_paths  # noqa: E402

UNC = "Epithelial, malignancy uncertain"
MAL = "Malignant epithelial"


def malignancy(epi, cnv, pats, cfg):
    """Return per-cell malignancy columns for epithelial cells and per-patient/study summaries."""
    c = cfg["infercnv"]
    e = epi.merge(cnv[cnv.group == "obs"][["cell_id", "cnv_score", "cnv_cor"]], on="cell_id", how="left")
    ref = cnv[cnv.group != "obs"]
    q = ref.groupby("patient_id").agg(
        s_hi=("cnv_score", lambda x: x.quantile(c["high_quantile"])),
        r_hi=("cnv_cor", lambda x: x.quantile(c["high_quantile"])),
        s_lo=("cnv_score", lambda x: x.quantile(c["low_quantile"])),
        r_lo=("cnv_cor", lambda x: x.quantile(c["low_quantile"])))
    e = e.join(q, on="patient_id")
    e["cnv_state"] = np.where(e.cnv_score.isna(), "not_assessable",
                     np.where((e.cnv_score > e.s_hi) & (e.cnv_cor > e.r_hi), "CNV-high",
                     np.where((e.cnv_score <= e.s_lo) & (e.cnv_cor <= e.r_lo), "CNV-low", "intermediate")))
    e["atlas_cancer"] = e.atlas_cell_type_fine.astype(str).str.startswith("Cancer")
    pt = e[e.atlas_cancer & (e.cnv_state != "not_assessable")].groupby("patient_id").cnv_state.apply(
        lambda s: (s == "CNV-high").mean()).rename("frac_cancer_cnv_high")
    pats = pats.join(pt, on="patient_id")
    pats["clear_cnv"] = pats.assessable & (pats.frac_cancer_cnv_high >= c["patient_clear_min_high_fraction"])
    st = pats[pats.assessable].groupby("study_id").clear_cnv.mean().rename("frac_patients_clear")
    poor = set(st.index[st < c["study_poor_max_clear_fraction"]])
    e = e.join(pats.set_index("patient_id").clear_cnv, on="patient_id")
    e["clear_cnv"] = e.clear_cnv.fillna(False).astype(bool)
    e["study_poor"] = e.study_id.isin(poor)
    normal = e.call_c.notna()
    usable = e.clear_cnv & ~e.study_poor
    hcm = e.atlas_cancer & (e.cnv_state == "CNV-high") & usable
    hcn = ~e.atlas_cancer & (e.cnv_state == "CNV-low") & normal & usable
    e["malignancy_confidence"] = np.where(hcm, "High-confidence malignant",
                                 np.where(hcn, "High-confidence non-malignant", "Uncertain"))
    put = e.atlas_cancer & (e.cnv_state == "CNV-low") & normal & e.clear_cnv & ~e.study_poor
    e["malignancy_sensitivity"] = np.where(put, "putative non-malignant epithelial", e.malignancy_confidence)
    st = st.to_frame().assign(poor_sensitivity=lambda d: d.index.isin(poor))
    return e, pats, st


def loso(lat, lab, study, cfg):
    p = cfg["loso"]
    rows = []
    for s in sorted(np.unique(study)):
        tr, te = study != s, study == s
        if te.sum() == 0 or tr.sum() == 0:
            continue
        index = NNDescent(lat[tr], n_neighbors=p["k"], random_state=0)
        nn, dist = index.query(lat[te], k=p["k"])
        ytr = lab[tr]
        w = 1.0 / np.maximum(dist, 1e-9)
        pred = []
        for i in range(len(nn)):
            v = pd.Series(w[i]).groupby(ytr[nn[i]]).sum()
            pred.append(v.idxmax())
        pred = np.array(pred, dtype=object)
        yte = lab[te]
        for t in np.unique(yte):
            m = yte == t
            rows.append({"held_out_study": s, "celltype_L2": t, "n_cells": int(m.sum()),
                         "recall": float((pred[m] == t).mean())})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--run-root", required=True)
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    P = run_paths(a.run_root)
    el = cfg["eligibility"]
    lp = cfg["loso"]

    l1 = pd.read_csv(P["cells"] / "l1_cells.tsv.gz", sep="\t")
    labs = {L: pd.read_csv(P["labels"] / f"{L}_labels.tsv.gz", sep="\t") for L in LINEAGES}
    for L in LINEAGES:
        labs[L] = labs[L].replace({np.nan: None})

    # malignancy
    pats = pd.read_csv(P["cnv"] / "patients.tsv", sep="\t")
    cnv = []
    for _, r in pats[pats.assessable].iterrows():
        f = P["cnv"] / "out" / r["dir"] / "cnv_metrics.tsv.gz"
        if not f.exists():
            raise FileNotFoundError(f)
        t = pd.read_csv(f, sep="\t")
        t["patient_id"] = r["patient_id"]
        cnv.append(t)
    cnv = pd.concat(cnv)
    epi = labs["Epithelial"].merge(l1[["cell_id", "study_id", "patient_id", "atlas_cell_type_fine"]], on="cell_id")
    epi = epi[~epi.F2.astype(bool)]
    e, pats, studies = malignancy(epi, cnv, pats, cfg)

    # final per-cell table
    base = l1.copy()
    base["celltype_L1"] = np.where(base.broad.isin(LINEAGES), base.broad, "Other")
    out = []
    for L in LINEAGES:
        t = labs[L].copy()
        if L == "Epithelial":
            t = t.merge(e[["cell_id", "cnv_score", "cnv_cor", "cnv_state", "malignancy_confidence",
                           "malignancy_sensitivity"]], on="cell_id", how="left")
            mc = t.malignancy_confidence.fillna("Uncertain")
            l2 = np.where(mc == "High-confidence malignant", MAL,
                 np.where(mc == "High-confidence non-malignant",
                          np.where(t.consensus.notna(), t.consensus, "Unclassified epithelial"), UNC))
            conf = np.where(mc == "High-confidence malignant", "high",
                   np.where(mc == "High-confidence non-malignant", t.confidence, "low"))
            meth = np.where(mc == "High-confidence malignant", "malignancy:atlas+cnv",
                   np.where(mc == "High-confidence non-malignant", "malignancy:atlas+cnv+markers;" + t.method.fillna(""),
                            "malignancy:uncertain"))
            t["malignancy_confidence"] = mc
        else:
            l2 = np.where(t.consensus.notna(), t.consensus, f"Unclassified {L.lower()}")
            conf, meth = t.confidence, t.method.fillna("")
        t["celltype_L2"] = np.where(t.F2.astype(bool), "L1_flagged", l2)
        t["annotation_confidence"] = np.where(t.F2.astype(bool), "flagged", conf)
        t["annotation_method"] = np.where(t.F2.astype(bool), "F2", meth)
        out.append(t)
    lab = pd.concat(out, ignore_index=True)
    ann = base.merge(lab, on="cell_id", how="left")
    ann.loc[ann.F1.astype(bool), ["celltype_L2", "annotation_confidence", "annotation_method"]] = \
        ["L1_flagged", "flagged", "F1"]
    ann.loc[ann.celltype_L1 == "Other", ["celltype_L2", "annotation_confidence", "annotation_method"]] = \
        ["Other (not annotated)", "none", "excluded"]
    ann["cellstate_L3"] = np.where(ann.L3_proliferation > cfg["l3"]["cycling"]["min_score"], "Cycling", "")
    ann["original_celltype"] = ann.atlas_cell_type_fine.astype(str) + " | " + ann.cell_type_study.astype(str)

    # LOSO (cross-study label reproducibility) on high/medium labels
    loso_rows = []
    for L in LINEAGES:
        cells = pd.read_csv(P["scvi"] / f"{L}_cells.txt", header=None)[0].astype(str).to_numpy()
        lat = np.load(P["scvi"] / f"{L}_latent.npy")
        a_ = ann.set_index("cell_id").loc[cells]
        m = a_.annotation_confidence.isin(["high", "medium"]).to_numpy() & \
            ~a_.celltype_L2.isin(["L1_flagged", UNC]).to_numpy()
        r = loso(lat[m], a_.celltype_L2.to_numpy(dtype=object)[m], a_.study_id.to_numpy()[m], cfg)
        r["lineage"] = L
        loso_rows.append(r)
    lo = pd.concat(loso_rows, ignore_index=True)
    lo.to_csv(P["light"] / "l2_loso_recall.csv", index=False)
    ev = lo[lo.n_cells >= lp["min_cells"]].assign(rec=lambda d: d.recall >= lp["min_recall"])
    rec = ev.groupby(["lineage", "celltype_L2"]).rec.sum().rename("n_studies_recovered").reset_index()
    rec["loso_status"] = np.where(rec.n_studies_recovered >= lp["pan_crc_min_studies"], "pan-CRC",
                         np.where(rec.n_studies_recovered == 2, "Extended Data only", "study-specific (merged)"))
    rec.to_csv(P["light"] / "l2_loso_status.csv", index=False)
    merged = set(rec.loc[rec.loso_status == "study-specific (merged)", "celltype_L2"]) - {MAL}
    for t in merged:
        m = ann.celltype_L2 == t
        lin = ann.loc[m, "celltype_L1"].iat[0].lower() if m.any() else ""
        ann.loc[m, "celltype_L2"] = f"Unclassified {lin}"
        ann.loc[m, "annotation_method"] = ann.loc[m, "annotation_method"] + ";LOSO-merged:" + t

    cols = ["cell_id", "study_id", "patient_id", "sample_id", "platform", "celltype_L1", "celltype_L2",
            "cellstate_L3", "malignancy_confidence", "malignancy_sensitivity", "annotation_confidence",
            "annotation_method", "original_celltype", "F1", "F2", "cnv_state", "cnv_score", "cnv_cor",
            "SOLO_doublet_prob"] + [c for c in ann.columns if c.startswith("L3_") or c.startswith("score_")]
    fn = P["final"] / "annotation_v1.tsv.gz"
    ann[cols].to_csv(fn, sep="\t", index=False)
    sha = hashlib.sha256(open(fn, "rb").read()).hexdigest()
    (P["final"] / "annotation_v1.tsv.gz.sha256").write_text(f"{sha}  annotation_v1.tsv.gz\n")

    # light tables
    lt = P["light"]
    real = ~ann.celltype_L2.isin(["L1_flagged", "Other (not annotated)", UNC]) & \
        ~ann.celltype_L2.str.startswith("Unclassified")
    cnt = ann.groupby(["study_id", "celltype_L1", "celltype_L2"]).agg(
        n_cells=("cell_id", "size"), n_patients=("patient_id", "nunique")).reset_index()
    cnt.to_csv(lt / "l2_counts_by_study.csv", index=False)
    pp = ann[real].groupby(["celltype_L2", "study_id", "patient_id"]).size().rename("n").reset_index()
    pp = pp[pp.n >= el["min_cells_per_patient"]]
    elig = pp.groupby("celltype_L2").agg(eligible_patients=("patient_id", "nunique"),
                                         eligible_studies=("study_id", "nunique")).reset_index()
    elig = elig.merge(rec[["celltype_L2", "loso_status"]], on="celltype_L2", how="left")
    elig["main_panel"] = (elig.eligible_patients >= el["main_min_patients"]) & \
        (elig.eligible_studies >= el["main_min_studies"]) & (elig.loso_status == "pan-CRC")
    elig.to_csv(lt / "l2_eligibility.csv", index=False)
    ann.groupby(["study_id", "celltype_L1", "annotation_confidence"]).size().rename("n_cells") \
        .reset_index().to_csv(lt / "l2_confidence_by_study.csv", index=False)
    for ref in ["atlas_cell_type_fine", "cell_type_study"]:
        pd.crosstab([ann.study_id, ann[ref].astype(str)], ann.celltype_L2).to_csv(lt / f"l2_confusion_vs_{ref}.csv")
    # malignancy (C4)
    ms = e.groupby("study_id").agg(n_epithelial=("cell_id", "size"),
                                   malignant=("malignancy_confidence", lambda s: (s == "High-confidence malignant").mean()),
                                   non_malignant=("malignancy_confidence", lambda s: (s == "High-confidence non-malignant").mean()),
                                   uncertain=("malignancy_confidence", lambda s: (s == "Uncertain").mean()),
                                   putative_non_malignant=("malignancy_sensitivity",
                                                           lambda s: (s == "putative non-malignant epithelial").mean()))
    ms = ms.join(studies).reset_index()
    ms.to_csv(lt / "malignancy_by_study.csv", index=False)
    mp = e.groupby(["study_id", "patient_id"]).agg(
        n_epithelial=("cell_id", "size"),
        n_malignant=("malignancy_confidence", lambda s: int((s == "High-confidence malignant").sum())),
        n_non_malignant=("malignancy_confidence", lambda s: int((s == "High-confidence non-malignant").sum())),
        n_uncertain=("malignancy_confidence", lambda s: int((s == "Uncertain").sum())),
        n_cnv_high=("cnv_state", lambda s: int((s == "CNV-high").sum())),
        n_cnv_low=("cnv_state", lambda s: int((s == "CNV-low").sum()))).reset_index()
    mp = mp.merge(pats[["patient_id", "assessable", "n_ref_immune", "n_ref_stromal", "frac_cancer_cnv_high",
                        "clear_cnv"]], on="patient_id", how="left")
    msi = l1.groupby("patient_id").microsatellite_status.agg(lambda s: ";".join(sorted(set(map(str, s)))))
    mp = mp.join(msi, on="patient_id")
    mp.to_csv(lt / "malignancy_by_patient.csv", index=False)
    # marker specificity: detection rate of each panel gene in the type vs rest of the lineage
    spec = []
    for L in LINEAGES:
        cells = pd.read_csv(P["scvi"] / f"{L}_cells.txt", header=None)[0].astype(str).to_numpy()
        det = sparse.load_npz(P["labels"] / f"{L}_panel_detection.npz").tocsc()
        genes = pd.read_csv(P["labels"] / f"{L}_panel_detection_genes.txt", header=None)[0].tolist()
        a_ = ann.set_index("cell_id").loc[cells]
        for s in sorted(a_.study_id.unique()):
            ms_ = (a_.study_id == s).to_numpy()
            for t in sorted(set(a_.celltype_L2[ms_])):
                if t in ("L1_flagged",) or t.startswith("Unclassified") or t == UNC:
                    continue
                it = ms_ & (a_.celltype_L2 == t).to_numpy()
                rest = ms_ & ~it
                if it.sum() < el["min_cells_per_patient"] or rest.sum() == 0:
                    continue
                dt = np.asarray(det[it].mean(axis=0)).ravel()
                dr = np.asarray(det[rest].mean(axis=0)).ravel()
                for g, x, y in zip(genes, dt, dr):
                    spec.append({"lineage": L, "study_id": s, "celltype_L2": t, "gene": g,
                                 "det_in_type": round(float(x), 4), "det_in_rest": round(float(y), 4)})
    pd.DataFrame(spec).to_csv(lt / "l2_marker_specificity.csv", index=False)
    # exclusions and convergence
    ex = ann.groupby(["study_id", "celltype_L1", "celltype_L2"]).size()
    ex = ex[ex.index.get_level_values(2).isin(["L1_flagged", "Other (not annotated)", UNC])]
    ex.rename("n_cells").reset_index().to_csv(lt / "l2_excluded_cells.csv", index=False)
    conv = {}
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.2))
    for ax, L in zip(axes, LINEAGES):
        cj = json.load(open(P["scvi"] / f"{L}_convergence.json"))
        conv[L] = cj
        k = cj["attempts"][-1]["attempt"]
        h = pd.read_csv(P["scvi"] / f"{L}_history_attempt{k}.csv", index_col=0)
        ax.plot(h.index, h.elbo_train, label="train", lw=1)
        ax.plot(h.index, h.elbo_validation, label="validation", lw=1)
        ax.set_title(f"{L} (converged={cj['converged']})", fontsize=7)
        ax.set_xlabel("Epoch", fontsize=6)
        ax.set_ylabel("ELBO", fontsize=6)
        ax.tick_params(labelsize=5)
    axes[0].legend(fontsize=5, frameon=False)
    fig.tight_layout()
    fig.savefig(lt / "scvi_convergence.png", dpi=200)
    checks = {L: json.load(open(P["labels"] / f"{L}_checks.json")) for L in LINEAGES}
    json.dump({"annotation_sha256": sha, "n_cells": int(len(ann)), "scvi": conv, "label_checks": checks},
              open(lt / "l2_summary.json", "w"), indent=1)
    print("DONE", sha, flush=True)


if __name__ == "__main__":
    main()
