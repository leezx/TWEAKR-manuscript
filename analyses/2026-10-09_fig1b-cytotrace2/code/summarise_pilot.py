#!/usr/bin/env python3
"""Technical diagnostics for the Fig. 1B CytoTRACE2 pilot (contract A2). No biological contrasts.

Inputs: per-sample score files from run_cytotrace2_sample.R, the export manifests and cell labels.
Outputs (light tables):
  pilot_run_status.csv          - samples expected / scored / failed, per study and variant
  pilot_allgenes_equivalence.csv- model-gene subset vs all-gene input on one sample
  pilot_mode_agreement.csv      - per study x compartment: Spearman whole vs intrinsic / split;
                                  potency-category agreement whole vs intrinsic
  pilot_split_compression.csv   - per sample: spread of compartment medians, whole vs split
                                  (unsigned magnitude only)
  pilot_potency_shares.csv      - potency category shares per study x compartment (whole run)
  pilot_patient_median_stability.csv - bootstrap (cells within patient) 95% CI width of patient medians
  pilot_depth_dependence.csv    - per study x compartment: Spearman of score with detected model genes,
                                  for whole and intrinsic scores, original and depth-matched data
  pilot_depth_matched_seed_spread.csv - per study x compartment: SD across seeds of patient medians
A2.1:
  pilot_matched_cell_depth.csv  - same retained cells: selection effect (sel - full) and depth effect
                                  (downsampled - sel), whole and raw model scores
  pilot_sample_vs_patient_pool.csv - per-cell and patient-median differences, sample-wise vs pooled run
  pilot_batching_repeats.csv    - per-cell SD of the final score across seeds for samples >10,000 cells
  pilot_low_gene_effect.csv     - per study x compartment: % cells < 500 detected model genes; unsigned
                                  change and rank agreement of patient medians when they are dropped
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

BROAD = ["Epithelial", "Immune", "Stromal"]
rng = np.random.default_rng(0)


def load_scores(score_dir, manifest):
    frames = []
    for _, r in manifest.iterrows():
        f = Path(score_dir) / (r.file[:-3] + ".scores.tsv.gz")
        if f.exists():
            frames.append(pd.read_csv(f, sep="\t").assign(variant=r.variant, sample_id=r.sample_id))
    return pd.concat(frames) if frames else pd.DataFrame()


def rho(a, b):
    ok = a.notna() & b.notna()
    return spearmanr(a[ok], b[ok])[0] if ok.sum() > 10 else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts-dir", required=True)
    ap.add_argument("--scores-dir", required=True)
    ap.add_argument("--ds-counts-dir", default="")
    ap.add_argument("--ds-scores-dir", default="")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--sel-counts-dir", default="")
    ap.add_argument("--sel-scores-dir", default="")
    ap.add_argument("--pool-counts-dir", default="")
    ap.add_argument("--pool-scores-dir", default="")
    ap.add_argument("--rep-scores-dir", default="")
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    man = pd.read_csv(Path(a.counts_dir) / "export_manifest.tsv", sep="\t")
    labels = pd.read_csv(Path(a.counts_dir) / "cell_labels.tsv", sep="\t")
    sc = load_scores(a.scores_dir, man)
    status = man.assign(scored=man.file.map(
        lambda f: (Path(a.scores_dir) / (f[:-3] + ".scores.tsv.gz")).exists()))
    status.groupby(["study_id", "variant"]).agg(expected=("file", "size"), scored=("scored", "sum")) \
        .reset_index().to_csv(out / "pilot_run_status.csv", index=False)

    # model-gene subset vs all genes
    eq = []
    for s in man[man.variant == "allgenes"].sample_id:
        x = sc[(sc.sample_id == s) & (sc.variant == "model")].set_index("cell_id")
        y = sc[(sc.sample_id == s) & (sc.variant == "allgenes")].set_index("cell_id").reindex(x.index)
        for c in ["whole_score", "intrinsic_score", "split_score"]:
            eq.append({"sample_id": s, "score": c, "max_abs_diff": float((x[c] - y[c]).abs().max()),
                       "spearman": rho(x[c], y[c])})
    pd.DataFrame(eq).to_csv(out / "pilot_allgenes_equivalence.csv", index=False)

    d = sc[sc.variant == "model"].merge(labels[["cell_id", "study_id", "patient_id", "broad"]], on="cell_id")
    d = d[d.broad.isin(BROAD)]

    agree = []
    for (study, b), g in d.groupby(["study_id", "broad"]):
        agree.append({"study": study, "compartment": b, "cells": len(g),
                      "rho_whole_intrinsic": rho(g.whole_score, g.intrinsic_score),
                      "rho_whole_split": rho(g.whole_score, g.split_score),
                      "potency_agreement_whole_intrinsic": float((g.whole_potency == g.intrinsic_potency).mean())})
    pd.DataFrame(agree).to_csv(out / "pilot_mode_agreement.csv", index=False)

    comp = []
    for (study, sample), g in d.groupby(["study_id", "sample_id"]):
        med = g.groupby("broad")[["whole_score", "split_score", "intrinsic_score"]].median()
        if len(med) == 3:
            comp.append({"study": study, "sample_id": sample,
                         **{f"{c}_compartment_range": float(med[c].max() - med[c].min())
                            for c in ["whole_score", "split_score", "intrinsic_score"]}})
    pd.DataFrame(comp).to_csv(out / "pilot_split_compression.csv", index=False)

    shares = (d.groupby(["study_id", "broad"]).whole_potency.value_counts(normalize=True)
              .rename("share").reset_index())
    shares.to_csv(out / "pilot_potency_shares.csv", index=False)

    stab = []
    for (study, patient, b), g in d.groupby(["study_id", "patient_id", "broad"]):
        v = g.whole_score.to_numpy()
        if len(v) < 30:
            continue
        boots = [np.median(rng.choice(v, len(v))) for _ in range(200)]
        stab.append({"study": study, "patient_id": patient, "compartment": b, "cells": len(v),
                     "ci95_width": float(np.percentile(boots, 97.5) - np.percentile(boots, 2.5))})
    pd.DataFrame(stab).to_csv(out / "pilot_patient_median_stability.csv", index=False)

    dep = []
    for (study, b), g in d.groupby(["study_id", "broad"]):
        for c in ["whole_score", "intrinsic_score"]:
            dep.append({"study": study, "compartment": b, "data": "original", "score": c,
                        "rho_with_detected_genes": rho(g[c], g.n_model_genes_detected)})
    if a.ds_counts_dir:
        dman = pd.read_csv(Path(a.ds_counts_dir) / "export_manifest.tsv", sep="\t")
        ds = load_scores(a.ds_scores_dir, dman).merge(
            labels[["cell_id", "study_id", "patient_id", "broad"]], on="cell_id")
        ds = ds[ds.broad.isin(BROAD)]
        for (study, b), g in ds.groupby(["study_id", "broad"]):
            for c in ["whole_score", "intrinsic_score"]:
                dep.append({"study": study, "compartment": b, "data": "depth_matched_all_seeds", "score": c,
                            "rho_with_detected_genes": rho(g[c], g.n_model_genes_detected)})
        pm = ds.groupby(["study_id", "patient_id", "broad", "variant"]).whole_score.median().reset_index()
        pm.groupby(["study_id", "broad"]).apply(
            lambda g: g.groupby("patient_id").whole_score.std().median()).rename("median_patient_sd_across_seeds") \
            .reset_index().to_csv(out / "pilot_depth_matched_seed_spread.csv", index=False)
    pd.DataFrame(dep).to_csv(out / "pilot_depth_dependence.csv", index=False)

    full = d.set_index("cell_id")
    if a.sel_counts_dir and a.ds_counts_dir:
        sman = pd.read_csv(Path(a.sel_counts_dir) / "export_manifest.tsv", sep="\t")
        sel = load_scores(a.sel_scores_dir, sman).set_index("cell_id")
        dsm = ds.groupby("cell_id")[["whole_score", "intrinsic_score"]].mean()
        m = full[["study_id", "broad", "whole_score", "intrinsic_score"]].join(
            sel[["whole_score"]].rename(columns={"whole_score": "sel_whole"}), how="inner").join(
            dsm.rename(columns={"whole_score": "ds_whole", "intrinsic_score": "ds_raw"}), how="inner")
        rows = []
        for (study, b), g in m.groupby(["study_id", "broad"]):
            rows.append({"study": study, "compartment": b, "cells": len(g),
                         "selection_median_shift_whole": float((g.sel_whole - g.whole_score).median()),
                         "selection_rho_whole": rho(g.sel_whole, g.whole_score),
                         "depth_median_shift_whole": float((g.ds_whole - g.sel_whole).median()),
                         "depth_rho_whole": rho(g.ds_whole, g.sel_whole),
                         "depth_median_shift_raw": float((g.ds_raw - g.intrinsic_score).median()),
                         "depth_rho_raw": rho(g.ds_raw, g.intrinsic_score)})
        pd.DataFrame(rows).to_csv(out / "pilot_matched_cell_depth.csv", index=False)

    if a.pool_counts_dir:
        pman = pd.read_csv(Path(a.pool_counts_dir) / "export_manifest.tsv", sep="\t")
        pool = load_scores(a.pool_scores_dir, pman).set_index("cell_id")
        m = full[["study_id", "patient_id", "broad", "whole_score"]].join(
            pool[["whole_score"]].rename(columns={"whole_score": "pool_whole"}), how="inner")
        rows = []
        for (study, patient), g in m.groupby(["study_id", "patient_id"]):
            pm = g.groupby("broad")[["whole_score", "pool_whole"]].median()
            rows.append({"study": study, "patient_id": patient, "cells": len(g),
                         "cell_rho": rho(g.whole_score, g.pool_whole),
                         "cell_median_abs_diff": float((g.whole_score - g.pool_whole).abs().median()),
                         **{f"{b}_patient_median_diff": float(pm.loc[b, "pool_whole"] - pm.loc[b, "whole_score"])
                            for b in pm.index}})
        pd.DataFrame(rows).to_csv(out / "pilot_sample_vs_patient_pool.csv", index=False)

    if a.rep_scores_dir:
        reps = [pd.read_csv(f, sep="\t")[["cell_id", "whole_score"]].assign(rep=f.name)
                for f in Path(a.rep_scores_dir).glob("*.scores.tsv.gz")]
        if reps:
            r = pd.concat(reps + [d[d.cell_id.isin(reps[0].cell_id)][["cell_id", "whole_score"]].assign(rep="seed14")])
            sd = r.groupby("cell_id").whole_score.std()
            pd.DataFrame({"cells": [len(sd)], "median_cell_sd": [sd.median()], "p95_cell_sd": [sd.quantile(0.95)],
                          "runs": [r.rep.nunique()]}).to_csv(out / "pilot_batching_repeats.csv", index=False)

    # low-gene cells (< 500 detected model genes, CytoTRACE2's own warning): share per study x compartment
    # and the unsigned change in patient medians when those cells are dropped after scoring
    low = []
    d["low"] = d.n_model_genes_detected < 500
    for (study, b), g in d.groupby(["study_id", "broad"]):
        allm = g.groupby("patient_id").whole_score.median()
        hi = g[~g.low]
        kept = hi.groupby("patient_id").whole_score.agg(["median", "size"])
        kept = kept[kept["size"] >= 30]["median"]
        both = pd.concat([allm.rename("all"), kept.rename("kept")], axis=1).dropna()
        low.append({"study": study, "compartment": b, "cells": len(g),
                    "lt500_model_genes_pct": round(100 * g.low.mean(), 1),
                    "patients": allm.size, "patients_still_eligible": kept.size,
                    "median_abs_change_patient_median": float((both.kept - both["all"]).abs().median())
                    if len(both) else np.nan,
                    "rho_patient_medians": rho(both["all"], both.kept) if len(both) > 10 else np.nan})
    pd.DataFrame(low).to_csv(out / "pilot_low_gene_effect.csv", index=False)
    print("scored files:", int(status.scored.sum()), "of", len(status))


if __name__ == "__main__":
    main()
