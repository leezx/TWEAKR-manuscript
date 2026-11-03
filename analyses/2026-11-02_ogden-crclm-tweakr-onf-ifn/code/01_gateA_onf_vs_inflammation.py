#!/usr/bin/env python3
"""Gate A: is TNFRSF12A an oncofetal-identity receptor, an inflammation-response
receptor, or both, in human CRC liver metastasis?

Ogden, Metic et al., Cell Genomics 5(7):100881 (2025). 15 patients, paired
snRNA/snATAC multiome; this script uses the RNA modality only.

THE QUESTION, stated as three competing models (from the review):
  Model A  oncofetal-associated   -- the TNFRSF12A/revCSC link survives control
                                     for interferon response
  Model B  inflammation-associated -- the link disappears once IFN/NF-kB is
                                     controlled; the receptor tracks inflammation
  Model C  dual-context            -- independent associations with both

DESIGN DECISIONS THAT KEEP THIS HONEST.
  * The authors' REC/iREC/Stem-NOTUM labels are NOT used to define the grouping.
    Scoring uses the project's frozen signatures, so the test does not inherit
    the authors' state definitions. Their labels are retained for post-hoc
    correspondence only.
  * TNFRSF12A is a member of revCSC, of Noncanonical_NFkB_TNFR2 and of
    STAT3_response. It is stripped from every set in common.R, otherwise the
    receptor would be correlated with itself in BOTH dimensions.
  * The unit of inference is the PATIENT, not the cell. Per-cell correlations
    are computed within each patient and then aggregated across patients with a
    test that treats patients as the replicates.
  * Every effect is benchmarked against detection-matched control genes, so the
    comparison holds n and sparsity fixed.

Usage:
  python3 01_gateA_onf_vs_inflammation.py <path-to-h5ad> <outdir-for-tables>
"""
import sys, os, json
import numpy as np
import pandas as pd
import scanpy as sc

SEED = 20261102
RECEPTOR, LIGAND = "TNFRSF12A", "TNFSF12"
MIN_CELLS = 100          # per-patient epithelial cells needed for a correlation
MIN_DET = 0.05           # per-patient receptor detection needed for a correlation

H5AD = sys.argv[1]
TAB = sys.argv[2]
os.makedirs(TAB, exist_ok=True)
np.random.seed(SEED)


def wtsv(df, name):
    df.to_csv(os.path.join(TAB, name), sep="\t", index=False)
    print(f"  wrote {name}  ({len(df)} rows)")


# ---------------------------------------------------------------- signatures
# The sets are assembled once by code/00_freeze_signatures.R (which owns the
# orthologue mapping and the MSigDB pull) and frozen to a GMT, so this script
# has no network dependency and the exact gene lists are auditable on disk.
def load_signatures_from_cache(cache_gmt):
    sets = {}
    for ln in open(cache_gmt):
        x = ln.rstrip("\n").split("\t")
        if len(x) > 2:
            sets[x[0]] = [g for g in x[2:] if g]
    drop = {RECEPTOR, LIGAND}
    for k in list(sets):
        hit = drop & set(sets[k])
        if hit:
            sets[k] = [g for g in sets[k] if g not in drop]
            print(f"  CIRCULARITY GUARD: removed {'/'.join(sorted(hit))} from {k}")
    return sets


# ---------------------------------------------------------------------- main
def main():
    root = os.environ.get("STELLIGEN_ROOT", "/Volumes/Stelligen_SSD/Stelligen")
    cache = os.path.join(root, "DATA/HotData/TWEAKR-oncoFetal",
                         "ogden2025_crclm_multiome/processed/signatures_human.gmt")
    SIG = load_signatures_from_cache(cache)
    ONF = [k for k in SIG if k.startswith("onf_")]
    INFL = [k for k in SIG if k.startswith("infl_")]
    print(f"  {len(ONF)} oncofetal sets, {len(INFL)} inflammatory sets")

    print("reading", H5AD)
    ad = sc.read_h5ad(H5AD)
    print(f"  {ad.n_obs} cells x {ad.n_vars} genes")
    # X is already log-normalised (non-integer, median total 3942).
    ad.var_names_make_unique()

    # ---- per-cell QC covariates ----
    ad.obs["log_counts"] = np.log1p(ad.obs["nCount_RNA"].astype(float))
    ad.obs["n_genes"] = ad.obs["nFeature_RNA"].astype(float)

    # ---- cell cycle (Tirosh via scanpy's standard lists) ----
    s_genes = ["MCM5", "PCNA", "TYMS", "FEN1", "MCM2", "MCM4", "RRM1", "UNG",
               "GINS2", "MCM6", "CDCA7", "DTL", "PRIM1", "UHRF1", "CENPU",
               "HELLS", "RFC2", "RPA2", "NASP", "RAD51AP1", "GMNN", "WDR76",
               "SLBP", "CCNE2", "UBR7", "POLD3", "MSH2", "ATAD2", "RAD51",
               "RRM2", "CDC45", "CDC6", "EXO1", "TIPIN", "DSCC1", "BLM",
               "CASP8AP2", "USP1", "CLSPN", "POLA1", "CHAF1B", "BRIP1", "E2F8"]
    g2m_genes = ["HMGB2", "CDK1", "NUSAP1", "UBE2C", "BIRC5", "TPX2", "TOP2A",
                 "NDC80", "CKS2", "NUF2", "CKS1B", "MKI67", "TMPO", "CENPF",
                 "TACC3", "SMC4", "CCNB2", "CKAP2L", "CKAP2", "AURKB",
                 "BUB1", "KIF11", "ANP32E", "TUBB4B", "GTSE1", "KIF20B",
                 "HJURP", "CDCA3", "CDC20", "TTK", "CDC25C", "KIF2C", "RANGAP1",
                 "NCAPD2", "DLGAP5", "CDCA2", "CDCA8", "ECT2", "KIF23",
                 "HMMR", "AURKA", "PSRC1", "ANLN", "LBR", "CKAP5", "CENPE",
                 "CTCF", "NEK2", "G2E3", "GAS2L3", "CBX5", "CENPA"]
    sc.tl.score_genes_cell_cycle(
        ad, s_genes=[g for g in s_genes if g in ad.var_names],
        g2m_genes=[g for g in g2m_genes if g in ad.var_names])

    # ---- signature scores ----
    for k, genes in SIG.items():
        present = [g for g in genes if g in ad.var_names]
        sc.tl.score_genes(ad, present, score_name=k, random_state=SEED)
        print(f"  scored {k:18s} {len(present):4d}/{len(genes):4d} genes present")

    # ---- receptor / ligand vectors ----
    def vec(g):
        x = ad[:, g].X
        return np.asarray(x.todense()).ravel() if hasattr(x, "todense") else np.asarray(x).ravel()

    ad.obs["receptor"] = vec(RECEPTOR)
    ad.obs["ligand"] = vec(LIGAND)
    ad.obs["receptor_det"] = ad.obs["receptor"] > 0

    ep = ad.obs["Cell_type"] == "Epithelial"
    print(f"  {ep.sum()} epithelial (malignant-compartment) cells")

    # =================================================== Q1A: where is it
    o = ad.obs
    rows = []
    for st, d in o[ep].groupby("Cell_subtype", observed=True):
        if len(d) < 50:
            continue
        rows.append(dict(subtype=st, n_cells=len(d),
                         n_patients=d["Patient"].nunique(),
                         detection=float(d["receptor_det"].mean()),
                         mean_expr=float(d["receptor"].mean()),
                         mean_expr_in_pos=float(d.loc[d["receptor_det"], "receptor"].mean()),
                         median_n_genes=float(d["n_genes"].median())))
    qa = pd.DataFrame(rows).sort_values("detection", ascending=False)
    wtsv(qa, "Q1A_receptor_by_epithelial_subtype.tsv")

    # per-patient detection, to show the heterogeneity honestly
    rows = []
    for p, d in o[ep].groupby("Patient", observed=True):
        rows.append(dict(patient=p, n_epithelial=len(d),
                         therapy=d["Therapy"].iloc[0],
                         receptor_detection=float(d["receptor_det"].mean()),
                         ligand_detection=float((d["ligand"] > 0).mean()),
                         median_n_genes=float(d["n_genes"].median())))
    qa2 = pd.DataFrame(rows).sort_values("receptor_detection", ascending=False)
    wtsv(qa2, "Q1A_receptor_by_patient.tsv")

    # =================================================== Q1B: the core test
    # Per patient: partial Spearman of the receptor with each dimension,
    # controlling for the OTHER dimension plus cell cycle and detection depth.
    def pspearman(x, y, Z):
        ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(Z).all(1)
        x, y, Z = x[ok], y[ok], Z[ok]
        if len(x) < 20 or x.std() == 0 or y.std() == 0:
            return np.nan
        rx = pd.Series(x).rank().values
        ry = pd.Series(y).rank().values
        Zr = np.apply_along_axis(lambda c: pd.Series(c).rank().values, 0, Z)
        Zr = Zr[:, Zr.std(0) > 0]
        if Zr.shape[1]:
            A = np.column_stack([np.ones(len(rx)), Zr])
            rx = rx - A @ np.linalg.lstsq(A, rx, rcond=None)[0]
            ry = ry - A @ np.linalg.lstsq(A, ry, rcond=None)[0]
        if rx.std() == 0 or ry.std() == 0:
            return np.nan
        return float(np.corrcoef(rx, ry)[0, 1])

    ONF_MAIN, INFL_MAIN = "onf_revCSC", "infl_IFNG"
    eligible = []
    rows = []
    for p, d in o[ep].groupby("Patient", observed=True):
        keep = len(d) >= MIN_CELLS and d["receptor_det"].mean() >= MIN_DET
        if keep:
            eligible.append(p)
        r = d["receptor"].values.astype(float)
        cc = d[["S_score", "G2M_score", "log_counts", "n_genes"]].values.astype(float)
        for dim, other in [(ONF_MAIN, INFL_MAIN), (INFL_MAIN, ONF_MAIN)]:
            rows.append(dict(
                patient=p, n_cells=len(d), eligible=keep,
                dimension=dim,
                rho_marginal=pspearman(r, d[dim].values.astype(float), cc),
                rho_partial=pspearman(r, d[dim].values.astype(float),
                                      np.column_stack([cc, d[other].values.astype(float)])),
                receptor_detection=float(d["receptor_det"].mean())))
    qb = pd.DataFrame(rows)
    wtsv(qb, "Q1B_patient_partial_correlations.tsv")

    # patient-level aggregation (the inference)
    from scipy import stats
    agg = []
    for dim, d in qb[qb["eligible"]].groupby("dimension"):
        for kind in ["rho_marginal", "rho_partial"]:
            v = d[kind].dropna().values
            w = stats.wilcoxon(v, alternative="two-sided") if len(v) >= 6 else None
            agg.append(dict(dimension=dim, estimate=kind, n_patients=len(v),
                            median_rho=float(np.median(v)),
                            mean_rho=float(np.mean(v)),
                            n_positive=int((v > 0).sum()),
                            wilcoxon_p=float(w.pvalue) if w else np.nan))
    qbs = pd.DataFrame(agg)
    wtsv(qbs, "Q1B_patient_level_summary.tsv")

    # ---- the same test across EVERY signature, so the choice of IFNG is not
    # ---- the thing driving the answer
    rows = []
    for k in ONF + INFL + ["imm_suppression", "imm_cytotox_res"]:
        if k not in o:
            continue
        ctrl = INFL_MAIN if k.startswith("onf_") else ONF_MAIN
        vals_m, vals_p = [], []
        for p in eligible:
            d = o[ep & (o["Patient"] == p)]
            r = d["receptor"].values.astype(float)
            cc = d[["S_score", "G2M_score", "log_counts", "n_genes"]].values.astype(float)
            vals_m.append(pspearman(r, d[k].values.astype(float), cc))
            vals_p.append(pspearman(r, d[k].values.astype(float),
                                    np.column_stack([cc, d[ctrl].values.astype(float)])))
        vm = np.array(vals_m, float); vp = np.array(vals_p, float)
        vm = vm[np.isfinite(vm)]; vp = vp[np.isfinite(vp)]
        rows.append(dict(signature=k, dimension="oncofetal" if k.startswith("onf_")
                         else ("inflammatory" if k.startswith("infl_") else "immune"),
                         controlled_for=ctrl,
                         n_patients=len(vm),
                         median_rho_marginal=float(np.median(vm)),
                         median_rho_partial=float(np.median(vp)),
                         n_positive_partial=int((vp > 0).sum()),
                         wilcoxon_p_partial=float(stats.wilcoxon(vp).pvalue) if len(vp) >= 6 else np.nan))
    qc = pd.DataFrame(rows)
    wtsv(qc, "Q1C_all_signatures_partial.tsv")

    # =================================================== Q1D: control genes
    sub = ad[ep.values].copy()
    Xb = sub.X > 0
    det_all = np.asarray(Xb.mean(0)).ravel()
    det_s = pd.Series(det_all, index=sub.var_names)
    target = det_s[RECEPTOR]
    cand = det_s[(det_s - target).abs() <= 0.02].index.difference([RECEPTOR, LIGAND])
    rng = np.random.default_rng(SEED)
    ctrl_genes = sorted(rng.choice(cand, size=min(24, len(cand)), replace=False))
    print(f"  {len(ctrl_genes)} detection-matched control genes "
          f"(receptor detection {target:.3f})")

    rows = []
    for g in [RECEPTOR] + list(ctrl_genes):
        gv_all = np.asarray(sub[:, g].X.todense()).ravel() if hasattr(sub.X, "todense") \
            else np.asarray(sub[:, g].X).ravel()
        mo, mi = [], []
        for p in eligible:
            m = (sub.obs["Patient"] == p).values
            d = sub.obs[m]
            cc = d[["S_score", "G2M_score", "log_counts", "n_genes"]].values.astype(float)
            mo.append(pspearman(gv_all[m], d[ONF_MAIN].values.astype(float),
                                np.column_stack([cc, d[INFL_MAIN].values.astype(float)])))
            mi.append(pspearman(gv_all[m], d[INFL_MAIN].values.astype(float),
                                np.column_stack([cc, d[ONF_MAIN].values.astype(float)])))
        rows.append(dict(gene=g, is_receptor=(g == RECEPTOR),
                         detection=float(det_s[g]),
                         median_rho_onf=float(np.nanmedian(mo)),
                         median_rho_infl=float(np.nanmedian(mi))))
    qd = pd.DataFrame(rows)
    qd["rank_onf"] = qd["median_rho_onf"].rank(ascending=False).astype(int)
    qd["rank_infl"] = qd["median_rho_infl"].rank(ascending=False).astype(int)
    wtsv(qd.sort_values("median_rho_onf", ascending=False),
         "Q1D_control_gene_calibration.tsv")

    # =================================================== Q1E: 2x2 stratification
    # Presented as an analysis stratification, NOT as four cell states.
    rows = []
    for p in eligible:
        d = o[ep & (o["Patient"] == p)].copy()
        oh = d[ONF_MAIN] > d[ONF_MAIN].median()
        ih = d[INFL_MAIN] > d[INFL_MAIN].median()
        for on, lo in [(True, "OnF-high"), (False, "OnF-low")]:
            for inn, li in [(True, "IFN-high"), (False, "IFN-low")]:
                m = (oh == on) & (ih == inn)
                if m.sum() >= 20:
                    rows.append(dict(patient=p, stratum=f"{lo} / {li}",
                                     onf_high=on, ifn_high=inn, n_cells=int(m.sum()),
                                     detection=float(d.loc[m, "receptor_det"].mean()),
                                     mean_expr=float(d.loc[m, "receptor"].mean())))
    qe = pd.DataFrame(rows)
    wtsv(qe, "Q1E_2x2_stratification.tsv")
    qes = qe.groupby("stratum").agg(n_patients=("patient", "nunique"),
                                    n_cells=("n_cells", "sum"),
                                    median_detection=("detection", "median"),
                                    median_mean_expr=("mean_expr", "median")).reset_index()
    wtsv(qes, "Q1E_2x2_summary.tsv")

    # =================================================== Q1F: REC vs iREC
    # The authors' own labels, used only here, for correspondence.
    rows = []
    for p in eligible:
        d = o[ep & (o["Patient"] == p)]
        for st in ["REC", "iREC", "Stem NOTUM", "Intermediate", "Stem", "Colonocyte"]:
            m = d["Cell_subtype"] == st
            if m.sum() >= 20:
                rows.append(dict(patient=p, subtype=st, n_cells=int(m.sum()),
                                 detection=float(d.loc[m, "receptor_det"].mean()),
                                 mean_expr=float(d.loc[m, "receptor"].mean()),
                                 mean_ifng=float(d.loc[m, INFL_MAIN].mean()),
                                 mean_revcsc=float(d.loc[m, ONF_MAIN].mean())))
    qf = pd.DataFrame(rows)
    wtsv(qf, "Q1F_REC_vs_iREC_paired.tsv")

    # paired REC vs iREC where both exist in the same patient
    piv = qf[qf["subtype"].isin(["REC", "iREC"])].pivot(
        index="patient", columns="subtype", values="detection").dropna()
    if len(piv) >= 3:
        w = stats.wilcoxon(piv["REC"], piv["iREC"])
        pair = pd.DataFrame([dict(comparison="REC vs iREC, receptor detection",
                                  n_patients=len(piv),
                                  median_REC=float(piv["REC"].median()),
                                  median_iREC=float(piv["iREC"].median()),
                                  median_paired_difference=float((piv["iREC"] - piv["REC"]).median()),
                                  wilcoxon_p=float(w.pvalue))])
        # and the IFN contrast that defines the two states, as a positive control
        pv2 = qf[qf["subtype"].isin(["REC", "iREC"])].pivot(
            index="patient", columns="subtype", values="mean_ifng").dropna()
        w2 = stats.wilcoxon(pv2["REC"], pv2["iREC"])
        pair = pd.concat([pair, pd.DataFrame([dict(
            comparison="REC vs iREC, IFNG score (positive control)",
            n_patients=len(pv2), median_REC=float(pv2["REC"].median()),
            median_iREC=float(pv2["iREC"].median()),
            median_paired_difference=float((pv2["iREC"] - pv2["REC"]).median()),
            wilcoxon_p=float(w2.pvalue))])], ignore_index=True)
        wtsv(pair, "Q1F_REC_vs_iREC_test.tsv")

    # =================================================== Q1G: ligand sources
    rows = []
    for ct, d in o.groupby("Cell_type", observed=True):
        rows.append(dict(cell_type=ct, n_cells=len(d),
                         n_patients=d["Patient"].nunique(),
                         ligand_detection=float((d["ligand"] > 0).mean()),
                         ligand_mean=float(d["ligand"].mean()),
                         pct_of_ligand_pos=float((d["ligand"] > 0).sum())))
    qg = pd.DataFrame(rows)
    qg["pct_of_ligand_pos"] = 100 * qg["pct_of_ligand_pos"] / qg["pct_of_ligand_pos"].sum()
    wtsv(qg.sort_values("ligand_detection", ascending=False),
         "Q1G_ligand_by_cell_type.tsv")

    # per-patient reproducibility of the top source
    rows = []
    for p, d in o.groupby("Patient", observed=True):
        sub2 = d[d["ligand"] > 0]
        if len(sub2) < 5:
            rows.append(dict(patient=p, n_ligand_pos=len(sub2), top_source=None,
                             top_fraction=np.nan))
            continue
        vc = sub2["Cell_type"].value_counts()
        rows.append(dict(patient=p, n_ligand_pos=len(sub2),
                         top_source=vc.index[0],
                         top_fraction=float(vc.iloc[0] / len(sub2))))
    wtsv(pd.DataFrame(rows), "Q1G_ligand_patient_reproducibility.tsv")

    # ---- freeze the per-cell scores used by the figures ----
    cols = ["Patient", "Therapy", "Cell_type", "Cell_subtype", "receptor",
            "receptor_det", "ligand", "S_score", "G2M_score", "log_counts",
            "n_genes"] + ONF + INFL + ["imm_suppression", "imm_cytotox_res"]
    o[cols].to_csv(os.path.join(TAB, "Q1_percell_scores.tsv.gz"),
                   sep="\t", index=True, compression="gzip")
    print("  wrote Q1_percell_scores.tsv.gz")

    meta = dict(n_cells=int(ad.n_obs), n_genes=int(ad.n_vars),
                n_epithelial=int(ep.sum()), n_patients=int(o["Patient"].nunique()),
                eligible_patients=sorted(eligible),
                n_eligible=len(eligible),
                control_genes=list(ctrl_genes),
                receptor_detection_epithelial=float(o.loc[ep, "receptor_det"].mean()),
                seed=SEED)
    json.dump(meta, open(os.path.join(TAB, "Q1_run_metadata.json"), "w"), indent=2)
    print("done")


if __name__ == "__main__":
    main()
