#!/usr/bin/env python3
"""Discriminate between the three competing models, and bound what the
negative results are allowed to mean.

Reads only the frozen tables written by script 01, so nothing here can drift
from the numbers the figures and the text quote.

  Q2A  Model A / B / C decision: is the oncofetal association larger than the
       inflammatory one, paired within patient?
  Q2B  REC vs iREC with a POSITIVE CONTROL. If the IFN contrast that defines
       the two states cannot itself be recovered, the test has no power and the
       receptor result is uninterpretable rather than negative.
  Q2C  the ligand stop rule, evaluated explicitly against its two criteria.
  Q2D  therapy exposure (P2-7), exploratory only.

Usage: python3 02_model_discrimination.py <tables-dir>
"""
import sys, os, json
import numpy as np
import pandas as pd
from scipy import stats

TAB = sys.argv[1]
ONF_MAIN, INFL_MAIN = "onf_revCSC", "infl_IFNG"


def rd(f):
    return pd.read_csv(os.path.join(TAB, f), sep="\t")


def wtsv(df, name):
    df.to_csv(os.path.join(TAB, name), sep="\t", index=False)
    print(f"  wrote {name}  ({len(df)} rows)")


# ----------------------------------------------- Q2A: which model?
b = rd("Q1B_patient_partial_correlations.tsv")
b = b[b["eligible"]]
piv = b.pivot(index="patient", columns="dimension", values="rho_partial")
diff = piv[ONF_MAIN] - piv[INFL_MAIN]
w = stats.wilcoxon(piv[ONF_MAIN], piv[INFL_MAIN])

# Each dimension on its own, against zero.
rows = []
for dim in [ONF_MAIN, INFL_MAIN]:
    v = piv[dim].dropna()
    rows.append(dict(
        test=f"{dim} partial rho vs 0 (other dimension controlled)",
        n_patients=len(v), median=float(v.median()),
        n_positive=int((v > 0).sum()),
        wilcoxon_p=float(stats.wilcoxon(v).pvalue),
        note="p is at the n=12 signed-rank floor (0.000488) when all signs agree"))
rows.append(dict(
    test="oncofetal partial rho > inflammatory partial rho (paired)",
    n_patients=len(diff), median=float(diff.median()),
    n_positive=int((diff > 0).sum()),
    wilcoxon_p=float(w.pvalue),
    note="the quantity that separates Model A-dominant from Model B-dominant"))
q2a = pd.DataFrame(rows)
wtsv(q2a, "Q2A_model_discrimination.tsv")

# The explicit model call, with its own justification recorded.
d = rd("Q1D_control_gene_calibration.tsv")
r = d[d["is_receptor"]].iloc[0]
c = d[~d["is_receptor"]]
call = dict(
    model_A_oncofetal_only=bool(piv[ONF_MAIN].median() > 0 and
                                stats.wilcoxon(piv[INFL_MAIN]).pvalue > 0.05),
    model_B_inflammation_only=bool(piv[INFL_MAIN].median() > 0 and
                                   stats.wilcoxon(piv[ONF_MAIN]).pvalue > 0.05),
    model_C_dual=bool(stats.wilcoxon(piv[ONF_MAIN]).pvalue < 0.05 and
                      stats.wilcoxon(piv[INFL_MAIN]).pvalue < 0.05),
    oncofetal_median_partial_rho=float(piv[ONF_MAIN].median()),
    inflammatory_median_partial_rho=float(piv[INFL_MAIN].median()),
    oncofetal_dominant=bool(w.pvalue < 0.05 and diff.median() > 0),
    n_patients_oncofetal_greater=int((diff > 0).sum()),
    controls_above_receptor_oncofetal=int((c["median_rho_onf"] > r["median_rho_onf"]).sum()),
    controls_above_receptor_inflammatory=int((c["median_rho_infl"] > r["median_rho_infl"]).sum()),
    n_controls=int(len(c)))
json.dump(call, open(os.path.join(TAB, "Q2A_model_call.json"), "w"), indent=2)
print("  wrote Q2A_model_call.json")
print(f"    Model C (dual): {call['model_C_dual']};  "
      f"oncofetal-dominant: {call['oncofetal_dominant']}")

# ----------------------------------------------- Q2B: REC vs iREC + power
f = rd("Q1F_REC_vs_iREC_paired.tsv")
pair = f[f["subtype"].isin(["REC", "iREC"])]
rows = []
for val, label in [("detection", "receptor detection"),
                   ("mean_expr", "receptor expression"),
                   ("mean_ifng", "IFNG score  [POSITIVE CONTROL]"),
                   ("mean_revcsc", "revCSC score")]:
    p = pair.pivot(index="patient", columns="subtype", values=val).dropna()
    if len(p) < 3:
        continue
    w2 = stats.wilcoxon(p["REC"], p["iREC"])
    rows.append(dict(quantity=label, n_patients_with_both=len(p),
                     median_REC=float(p["REC"].median()),
                     median_iREC=float(p["iREC"].median()),
                     median_paired_diff_iREC_minus_REC=float((p["iREC"] - p["REC"]).median()),
                     wilcoxon_p=float(w2.pvalue)))
q2b = pd.DataFrame(rows)
wtsv(q2b, "Q2B_REC_vs_iREC_with_positive_control.tsv")

ctrl_row = q2b[q2b["quantity"].str.contains("POSITIVE CONTROL")]
powered = bool(len(ctrl_row) and ctrl_row["wilcoxon_p"].iloc[0] < 0.05
               and ctrl_row["median_paired_diff_iREC_minus_REC"].iloc[0] > 0)
print(f"    REC/iREC positive control recovered: {powered}")
json.dump(dict(positive_control_recovered=powered,
               n_patients_with_both_states=int(q2b["n_patients_with_both"].max()),
               interpretation=("the paired REC/iREC comparison is UNDERPOWERED and "
                               "uninterpretable; the IFN difference that defines the "
                               "two states cannot itself be recovered in these patients")
               if not powered else "powered"),
          open(os.path.join(TAB, "Q2B_power_verdict.json"), "w"), indent=2)
print("  wrote Q2B_power_verdict.json")

# ----------------------------------------------- Q2C: the ligand stop rule
g = rd("Q1G_ligand_by_cell_type.tsv")
rep = rd("Q1G_ligand_patient_reproducibility.tsv")
usable = rep[rep["n_ligand_pos"] >= 10]
top_counts = usable["top_source"].value_counts()
rows = [dict(criterion="detection adequate",
             threshold="any cell type with >10% of cells detected",
             observed=f"max detection {g['ligand_detection'].max():.1%} "
                      f"({g.loc[g['ligand_detection'].idxmax(), 'cell_type']})",
             met=bool(g["ligand_detection"].max() > 0.10)),
        dict(criterion="source consistent across patients",
             threshold="one cell type is the top source in >=70% of usable patients",
             observed="; ".join(f"{k} {v}/{len(usable)}" for k, v in top_counts.items()),
             met=bool(len(top_counts) and top_counts.iloc[0] / len(usable) >= 0.70))]
q2c = pd.DataFrame(rows)
q2c["stop_rule_triggered"] = not q2c["met"].any()
wtsv(q2c, "Q2C_ligand_stop_rule.tsv")
print(f"    ligand stop rule triggered: {not q2c['met'].any()}")

# ----------------------------------------------- Q2D: therapy, exploratory
pc = pd.read_csv(os.path.join(TAB, "Q1_percell_scores.tsv.gz"), sep="\t",
                 index_col=0, compression="gzip")
ep = pc["Cell_type"] == "Epithelial"
rows = []
for p, dd in pc[ep].groupby("Patient"):
    rows.append(dict(patient=p, therapy=dd["Therapy"].iloc[0], n_cells=len(dd),
                     receptor_detection=float((dd["receptor"] > 0).mean()),
                     revcsc=float(dd[ONF_MAIN].mean()),
                     ifng=float(dd[INFL_MAIN].mean())))
t = pd.DataFrame(rows)
wtsv(t, "Q2D_therapy_per_patient.tsv")
rows = []
for q in ["receptor_detection", "revcsc", "ifng"]:
    a = t.loc[t["therapy"] == "Treated", q]
    b2 = t.loc[t["therapy"] == "Naive", q]
    rows.append(dict(quantity=q, n_treated=len(a), n_naive=len(b2),
                     median_treated=float(a.median()), median_naive=float(b2.median()),
                     mannwhitney_p=float(stats.mannwhitneyu(a, b2).pvalue)))
q2d = pd.DataFrame(rows)
q2d["caveat"] = ("not paired pre/post; confounded by patient selection, tumour "
                 "genotype and sampling time. Exploratory only.")
wtsv(q2d, "Q2D_therapy_exploratory.tsv")
print("done")
