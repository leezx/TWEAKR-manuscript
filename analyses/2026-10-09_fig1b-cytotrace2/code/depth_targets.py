#!/usr/bin/env python3
"""Study-specific UMI targets for the depth-matched sensitivity analysis (amendment A2).

Rule (fixed before any CytoTRACE2 score): for each study, the target T_s is the smallest of the
three compartments' 25th-percentile library sizes, so that every compartment keeps >= 75% of its
cells. There is no global floor.

Reported for T_s and for a grid of alternatives: cell retention per compartment, and the patients
still complete (>= 30 cells in each of Epithelial, Immune, Stromal) after dropping cells below T.
A study with fewer than 5 complete patients at T_s is excluded from this sensitivity analysis only.

Usage: python depth_targets.py <cohort_cell_qc.tsv.gz> <out_dir>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BROAD = ["Epithelial", "Immune", "Stromal"]
GRID = [500, 750, 1000, 1500, 2000, 3000]

d = pd.read_csv(sys.argv[1], sep="\t", usecols=["study_id", "patient_id", "broad", "library_size"])
d = d[d.broad.isin(BROAD)]
out = Path(sys.argv[2])
rows = []
for study, g in d.groupby("study_id"):
    q25 = g.groupby("broad").library_size.quantile(0.25)
    t_s = int(np.floor(q25.min()))
    for label, t in [("T_s", t_s)] + [(f"grid_{x}", x) for x in GRID]:
        kept = g[g.library_size >= t]
        pc = kept.groupby(["patient_id", "broad"]).size().unstack(fill_value=0).reindex(columns=BROAD, fill_value=0)
        r = {"study": study, "target": label, "umi": t,
             "complete_patients": int((pc >= 30).all(axis=1).sum()),
             "complete_patients_before": int(
                 (g.groupby(["patient_id", "broad"]).size().unstack(fill_value=0)
                  .reindex(columns=BROAD, fill_value=0) >= 30).all(axis=1).sum())}
        for b in BROAD:
            n = (g.broad == b).sum()
            r[f"{b}_retained_pct"] = round(100 * (kept.broad == b).sum() / n, 1)
            r[f"{b}_q25_umi"] = int(q25[b])
        r["included"] = r["complete_patients"] >= 5
        rows.append(r)
pd.DataFrame(rows).to_csv(out / "depth_targets.csv", index=False)
t = pd.DataFrame(rows)
print(t[t.target == "T_s"][["study", "umi", "Epithelial_retained_pct", "Immune_retained_pct",
                            "Stromal_retained_pct", "complete_patients_before", "complete_patients",
                            "included"]].to_string(index=False))
