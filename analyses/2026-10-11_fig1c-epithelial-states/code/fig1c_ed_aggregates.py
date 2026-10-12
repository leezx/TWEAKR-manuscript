#!/usr/bin/env python3
"""Fig. 1c Extended Data (ED-B) source data from the frozen v0.3a labels. Aggregate only; no cell or patient rows.
1) ed_b_raw_density.tsv: patient-equal-weighted 2D histogram of raw UCell proCSC x revCSC (50 x 50 bins over
   [0, max] rounded up to 0.05), split by the frozen sample-specific p75 stratum (no global cutoffs exist on the
   raw scale). Each patient's cells sum to weight 1 (split equally across that patient's samples).
2) ed_b_stratum_sizes.tsv: cell and patient counts per stratum at p70/p75/p80, plus the discordant75 count.
3) ed_b_raw_by_stratum.tsv: per-stratum quantiles (5, 25, 50, 75, 95) of raw proCSC and revCSC (cell level)."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

L, outdir = Path(sys.argv[1]), Path(sys.argv[2])
cols = ["patient_id", "sample_id", "proCSC", "revCSC", "stratum70", "stratum75", "stratum80", "discordant75"]
d = pd.concat([pd.read_csv(f, sep="\t", usecols=cols) for f in sorted(L.glob("*.cell_labels.tsv.gz"))],
              ignore_index=True)
npat = d.patient_id.nunique()
hi = np.ceil(max(d.proCSC.max(), d.revCSC.max()) / 0.05) * 0.05
nb = 50
ns = d.groupby("patient_id").sample_id.nunique()
d["w"] = 1.0 / d.groupby("sample_id").sample_id.transform("size") / d.patient_id.map(ns) / npat
d["bx"] = np.clip((d.proCSC / hi * nb).astype(int), 0, nb - 1)
d["by"] = np.clip((d.revCSC / hi * nb).astype(int), 0, nb - 1)
g = d.groupby(["bx", "by", "stratum75"]).w.sum().reset_index()
g["pro_lo"] = g.bx * hi / nb
g["rev_lo"] = g.by * hi / nb
g["bin_width"] = hi / nb
g.rename(columns={"stratum75": "stratum", "w": "patient_weight"})[
    ["pro_lo", "rev_lo", "bin_width", "stratum", "patient_weight"]].to_csv(outdir / "ed_b_raw_density.tsv",
                                                                            sep="\t", index=False)
rows = []
for t in ["stratum70", "stratum75", "stratum80"]:
    for s, x in d.groupby(t):
        rows.append((t.replace("stratum", "p"), s, len(x), x.patient_id.nunique()))
rows.append(("p75", "discordant_in_reference", int(d.discordant75.sum()), d[d.discordant75].patient_id.nunique()))
pd.DataFrame(rows, columns=["threshold", "stratum", "n_cells", "n_patients"]).to_csv(
    outdir / "ed_b_stratum_sizes.tsv", sep="\t", index=False)
q = d.groupby("stratum75")[["proCSC", "revCSC"]].quantile([0.05, 0.25, 0.5, 0.75, 0.95]).reset_index()
q.rename(columns={"stratum75": "stratum", "level_1": "quantile"}).to_csv(outdir / "ed_b_raw_by_stratum.tsv",
                                                                          sep="\t", index=False)
print(len(d), npat, hi, g.w.sum())
