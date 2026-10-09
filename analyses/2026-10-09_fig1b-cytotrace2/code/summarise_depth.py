#!/usr/bin/env python3
"""Median library size and detected genes per study x broad compartment (cohort v1).

Usage: python summarise_depth.py <cohort_cell_qc.tsv.gz> <out.csv>
(Run inline on Argos on 2026-10-09 with identical logic; saved here for reproducibility.)
"""
import sys

import pandas as pd

d = pd.read_csv(sys.argv[1], sep="\t")
d = d[d.broad != "Other"]
g = (d.groupby(["study_id", "broad"])
     .agg(cells=("cell_id", "size"), median_umi=("library_size", "median"),
          median_genes=("n_genes_detected", "median"),
          pct_cells_lt500_genes=("n_genes_detected", lambda s: round(100 * (s < 500).mean(), 1)))
     .reset_index())
g.to_csv(sys.argv[2], index=False)
