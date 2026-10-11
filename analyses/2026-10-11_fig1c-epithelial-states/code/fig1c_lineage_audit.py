#!/usr/bin/env python3
"""Fig. 1c amendment v0.3a: CT2-blinded lineage plausibility audit (contract amendment section).

phase 'study' (SGE task = study index): per study x v0.3a predicted class x old-OOD status, pseudobulk
marker counts and library sizes; per sample Spearman of OOD percentile with log UMI / log genes.
phase 'merge': module scores, pre-specified pass rule, classifier-HVG overlap, OOD-driver summary.
"""
import argparse
import sys
from pathlib import Path

import h5py
import joblib
import numpy as np
import pandas as pd
from scipy import stats
from scipy.sparse import csc_matrix

sys.path.insert(0, str(Path(__file__).parent))
from fig1c_axisL_fit import Model  # noqa: E402,F401

MOD = {"absorptive": ["KRT20", "FABP1", "ALPI", "CA1", "CA2", "SLC26A3", "CEACAM7", "AQP8"],
       "secretory": ["MUC2", "TFF3", "SPINK4", "CLCA1", "FCGBP", "ZG16"],
       "stem": ["LGR5", "ASCL2", "SMOC2", "OLFM4", "RGMB"],
       "cycling": ["MKI67", "TOP2A", "CENPF", "UBE2C"]}
RULES = {"Absorptive differentiated-like": ("absorptive", ["Stem/TA-like", "Cycling Stem/TA"]),
         "Secretory differentiated-like": ("secretory", ["Absorptive differentiated-like", "Stem/TA-like"]),
         "Stem/TA-like": ("stem", ["Absorptive differentiated-like"]),
         "Cycling Stem/TA": ("cycling", ["Stem/TA-like"])}
GENES = sorted({g for v in MOD.values() for g in v})


def study_phase(a):
    files = sorted(Path(a.cells_dir).glob("*.cells.tsv.gz"))
    if a.task > len(files):
        return
    cf = files[a.task - 1]
    study = cf.name[:-len(".cells.tsv.gz")]
    cells = pd.read_csv(cf, sep="\t", usecols=["cell_id", "sample_id", "variant"])
    cells = cells[cells.variant == "main"]
    agg, ood = [], []
    for tag in sorted(cells.sample_id.unique()):
        h5p, pp = Path(a.counts_dir) / f"{tag}.main.h5", Path(a.axisl_dir) / f"{tag}.axisL.tsv.gz"
        if not h5p.exists() or not pp.exists():
            continue
        with h5py.File(h5p, "r") as h:
            m = csc_matrix((h["data"][:], h["indices"][:], h["indptr"][:]), shape=tuple(h["shape"][:]))
            genes = np.array([g.decode() if isinstance(g, bytes) else g for g in h["genes"][:]])
            cid = np.array([c.decode() if isinstance(c, bytes) else c for c in h["cells"][:]])
        lib = np.asarray(m.sum(axis=0)).ravel()
        ngen = np.asarray((m > 0).sum(axis=0)).ravel()
        gi = pd.Series(np.arange(len(genes)), index=genes)
        gi = gi[~gi.index.duplicated()].reindex(GENES)
        sub = pd.DataFrame(0.0, index=cid, columns=GENES)
        have = gi.dropna().astype(int)
        sub[have.index] = m[have.values].T.toarray()
        p = pd.read_csv(pp, sep="\t", usecols=["cell_id", "pred_agg", "maxp_agg", "margin_agg", "ood_pct"]).set_index("cell_id")
        p = p.reindex(cid)
        cls = np.where((p.maxp_agg >= 0.70) & (p.margin_agg >= 0.20), p.pred_agg, "lineage-unresolved")
        df = sub.assign(lib=lib, cls=cls, ood_pass=(p.ood_pct <= 99.0).values)
        g = df.groupby(["cls", "ood_pass"]).agg({**{x: "sum" for x in GENES}, "lib": ["sum", "size"]})
        g.columns = GENES + ["lib_sum", "n_cells"]
        g = g.reset_index().assign(study_id=study, sample_id=tag)
        agg.append(g)
        ok = np.isfinite(p.ood_pct.values)
        if ok.sum() >= 30:
            ood.append({"study_id": study, "sample_id": tag, "n": int(ok.sum()),
                        "median_ood_pct": float(np.nanmedian(p.ood_pct)),
                        "frac_ood_fail": float((p.ood_pct > 99).mean()),
                        "rho_ood_logumi": stats.spearmanr(p.ood_pct[ok], np.log10(np.maximum(lib[ok], 1))).correlation,
                        "rho_ood_loggenes": stats.spearmanr(p.ood_pct[ok], np.log10(np.maximum(ngen[ok], 1))).correlation,
                        "median_umi": float(np.median(lib))})
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if agg:
        pd.concat(agg).to_csv(out / f"{study}.audit_pseudobulk.tsv.gz", sep="\t", index=False)
    pd.DataFrame(ood).to_csv(out / f"{study}.audit_ood.tsv", sep="\t", index=False)
    print(study, len(agg))


def module(pb, mod):
    cp = pb[MOD[mod]].astype(float).div(pb.lib_sum.astype(float), axis=0) * 1e4
    return np.log2(1 + cp).mean(axis=1)


def merge_phase(a):
    d = Path(a.out_dir)
    pb = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(d.glob("*.audit_pseudobulk.tsv.gz"))])
    rows = []
    for subset in ["all_assigned", "old_ood_rejected"]:
        x = pb if subset == "all_assigned" else pb[~pb.ood_pass]
        s = x.groupby(["study_id", "cls"])[GENES + ["lib_sum", "n_cells"]].sum().reset_index()
        for study, ss in s.groupby("study_id"):
            ss = ss.set_index("cls")
            for cls, (mod, comp) in RULES.items():
                n_c = int(ss.n_cells.get(cls, 0))
                cc = [c for c in comp if c in ss.index]
                n_k = int(ss.loc[cc].n_cells.sum()) if cc else 0
                r = {"study_id": study, "subset": subset, "class": cls, "module": mod,
                     "n_class": n_c, "n_comparator": n_k}
                if n_c >= 50 and n_k >= 50:
                    a_ = module(ss.loc[[cls]], mod).iloc[0]
                    b_ = module(ss.loc[cc].sum().to_frame().T, mod).iloc[0]
                    r.update(module_class=a_, module_comparator=b_, diff=a_ - b_, evaluable=True, pass_=bool(a_ - b_ >= 1))
                else:
                    r.update(evaluable=False, pass_=None)
                rows.append(r)
    t = pd.DataFrame(rows)
    t.to_csv(Path(a.public_out) / "A_lineage_audit_long.tsv", sep="\t", index=False)
    vr = []
    for (study, cls), g in t.groupby(["study_id", "class"]):
        al = g[g.subset == "all_assigned"].iloc[0]
        rj = g[g.subset == "old_ood_rejected"]
        rj_ok = rj.empty or (not bool(rj.iloc[0].evaluable)) or bool(rj.iloc[0].pass_)
        if not bool(al.evaluable):
            vd = "not_evaluable"
        elif bool(al.pass_) and rj_ok:
            vd = "verified"
        else:
            vd = "lineage_transfer_unverified"
        vr.append({"study_id": study, "class": cls, "verdict": vd})
    v = pd.DataFrame(vr)
    v.to_csv(Path(a.public_out) / "A_lineage_audit_verdict.tsv", sep="\t", index=False)
    # classifier-HVG overlap of marker genes
    ov = []
    for k in range(6):
        m = joblib.load(Path(a.model_dir) / f"axisL_model_fold{k}.joblib")
        hv = set(m.genes[m.hvg])
        ov.append({"fold": k, **{mod: ",".join(sorted(set(gs) & hv)) for mod, gs in MOD.items()}})
    pd.DataFrame(ov).to_csv(Path(a.public_out) / "A_marker_hvg_overlap.tsv", sep="\t", index=False)
    oo = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(d.glob("*.audit_ood.tsv")) if f.stat().st_size > 1])
    oo.groupby("study_id")[["median_ood_pct", "frac_ood_fail", "rho_ood_logumi", "rho_ood_loggenes", "median_umi"]] \
        .median().round(3).to_csv(Path(a.public_out) / "A_ood_drivers_by_study.tsv", sep="\t")
    print(v.verdict.value_counts().to_string())
    print(v[v.verdict != "verified"].to_string())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["study", "merge"])
    ap.add_argument("--task", type=int, default=0)
    ap.add_argument("--cells_dir")
    ap.add_argument("--counts_dir")
    ap.add_argument("--axisl_dir")
    ap.add_argument("--model_dir")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--public_out")
    a = ap.parse_args()
    study_phase(a) if a.phase == "study" else merge_phase(a)


if __name__ == "__main__":
    main()
