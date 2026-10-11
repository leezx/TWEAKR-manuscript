#!/usr/bin/env python3
"""A3b Stage I step 4: three-class identity, Axis-L projection, identity_v1 + SHA256 (contract A3b v0.3 §6).
No CT2, no programme score.

Per cell:
  normal_like     = N assessable for the study & d <= tau_p & cnv_state != CNV-high
  tumour_evidence = T_positive (CNV-high, clear-CNV patient, T evaluable, calibrated study)
                    & (d > tau_p, or N not assessable for the study)
  ambiguous       = everything else
Axis-L: frozen Fig. 1c final model (fold 0), predict() unchanged; assignment = Fig. 1c v0.3a rule
(aggregated max-p >= 0.70 and margin >= 0.20; OOD percentile stored, not used as a veto). Pelka cells are
labelled but flagged 'pelka_training_excluded' (contract: Pelka excluded from E1-L).
Outputs (private, Argos): <root>/identity_v1.private.tsv.gz (+ .sha256).
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

import h5py
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix

MAXP, MARGIN = 0.70, 0.20


def safe(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--fig1c-code", required=True)
    ap.add_argument("--axisl-models", required=True)
    a = ap.parse_args()
    sys.path.insert(0, a.fig1c_code)
    from fig1c_axisL_fit import Model, predict  # noqa: F401,E402
    from fig1c_axisL_predict import to_model_space  # noqa: E402
    R = Path(a.root)
    final = joblib.load(Path(a.axisl_models) / "axisL_model_fold0.joblib")
    T = pd.read_csv(R / "identity_T.private.tsv.gz", sep="\t")
    out = []
    for f in sorted((R / "export/cells").glob("*.epi_cells.tsv.gz")):
        study = f.name.replace(".epi_cells.tsv.gz", "")
        cells = pd.read_csv(f, sep="\t")
        N = pd.read_csv(R / "evidenceN" / f"{study}.N.private.tsv.gz", sep="\t")
        d = cells.merge(N, on="cell_id", how="left").merge(
            T[["cell_id", "cnv_state", "clear_cnv", "T_evaluable", "T_status", "T_positive"]], on="cell_id", how="left")
        d["T_positive"] = d.T_positive.fillna(False).astype(bool)
        n_ok = d.N_status.eq("assessable")
        d["identity"] = "ambiguous"
        d.loc[n_ok & (d.N_dist <= d.N_tau) & d.cnv_state.ne("CNV-high"), "identity"] = "normal_like"
        d.loc[d.T_positive & (~n_ok | (d.N_dist > d.N_tau)), "identity"] = "tumour_evidence"
        ax = []
        for s in sorted(d.sample_id.unique()):
            with h5py.File(R / "export/counts" / f"{safe(s)}.epi.h5", "r") as h:
                x = csc_matrix((h["data"][:], h["indices"][:], h["indptr"][:]), shape=tuple(h["shape"][:])).T.tocsr()
                genes = np.array([g.decode() for g in h["genes"][:]])
                cid = np.array([c.decode() for c in h["cells"][:]])
            xm, cov = to_model_space(x.astype(np.float32), genes, final.genes)
            pr = predict(final, xm)
            pr.insert(0, "cell_id", cid)
            pr["axisL_gene_coverage"] = cov
            ax.append(pr)
        ax = pd.concat(ax)
        ax["axisL_v03a"] = np.where((ax.maxp_agg >= MAXP) & (ax.margin_agg >= MARGIN), ax.pred_agg, "lineage-unresolved")
        d = d.merge(ax[["cell_id", "pred_agg", "maxp_agg", "margin_agg", "ood_pct", "axisL_v03a",
                        "axisL_gene_coverage"]], on="cell_id", how="left")
        d["axisL_flag"] = np.where(d.study_id.eq("Pelka_2021_Cell"), "pelka_training_excluded", "")
        out.append(d)
        print(study, len(d), d.identity.value_counts().to_dict(), flush=True)
    idt = pd.concat(out)
    cols = ["cell_id", "study_id", "patient_id", "sample_id", "side", "stage", "atlas_cell_type_fine", "umi", "genes",
            "mito_frac", "S_score", "G2M_score", "phase", "cnv_state", "clear_cnv", "T_evaluable", "T_status",
            "T_positive", "N_dist", "N_tau", "N_status", "N_reference_pool", "identity", "pred_agg", "maxp_agg",
            "margin_agg", "ood_pct", "axisL_v03a", "axisL_gene_coverage", "axisL_flag"]
    p = R / "identity_v1.private.tsv.gz"
    idt[cols].sort_values("cell_id").to_csv(p, sep="\t", index=False)
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    (R / "identity_v1.private.tsv.gz.sha256").write_text(f"{h}  identity_v1.private.tsv.gz\n")
    print("identity_v1", len(idt), h, flush=True)


if __name__ == "__main__":
    main()
