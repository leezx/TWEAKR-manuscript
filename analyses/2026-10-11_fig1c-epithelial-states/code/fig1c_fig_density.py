#!/usr/bin/env python3
"""Fig. 1c c-i source data: patient-equal-weighted 2D histogram of within-sample percentile ranks of
proCSC and revCSC (frozen v0.3a labels; all labelled tumour-specimen epithelial cells). Aggregate only.
Percentile rank = 100 * (rank - 0.5) / n within sample (average ties). Each patient's cells sum to weight 1
(split equally across that patient's samples). Bins: 2.5 percentile units (40 x 40)."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

L, out = Path(sys.argv[1]), Path(sys.argv[2])
H = np.zeros((40, 40))
n_cells = 0
pats = set()
for f in sorted(L.glob("*.cell_labels.tsv.gz")):
    d = pd.read_csv(f, sep="\t", usecols=["patient_id", "sample_id", "proCSC", "revCSC"])
    ns = d.groupby("patient_id").sample_id.nunique()
    for (p, s), x in d.groupby(["patient_id", "sample_id"]):
        n = len(x)
        px = 100 * (stats.rankdata(x.proCSC) - 0.5) / n
        rx = 100 * (stats.rankdata(x.revCSC) - 0.5) / n
        h, _, _ = np.histogram2d(px, rx, bins=40, range=[[0, 100], [0, 100]])
        H += h / n / ns[p]
        n_cells += n
        pats.add(p)
e = np.arange(0, 100, 2.5)
g = pd.DataFrame([(e[i], e[i] + 2.5, e[j], e[j] + 2.5, H[i, j]) for i in range(40) for j in range(40)],
                 columns=["pro_pct_lo", "pro_pct_hi", "rev_pct_lo", "rev_pct_hi", "patient_weight"])
g["patient_weight"] /= len(pats)
g.to_csv(out, sep="\t", index=False)
print(n_cells, len(pats), g.patient_weight.sum())
