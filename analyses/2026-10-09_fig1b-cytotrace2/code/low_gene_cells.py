#!/usr/bin/env python3
"""A2.1: cells with < 500 detected genes, by study x compartment x sample (cohort v1), and the
minimum detected genes per study as evidence of the Atlas QC threshold actually applied.

Counts are on all Atlas genes (cohort_cell_qc). CytoTRACE2's own warning counts model-feature genes
only; that version is added from the pilot score files when available.

Usage: python low_gene_cells.py <cohort_cell_qc.tsv.gz> <out_dir>
"""
import sys
from pathlib import Path

import pandas as pd

d = pd.read_csv(sys.argv[1], sep="\t", usecols=["study_id", "patient_id", "sample_id", "broad",
                                               "library_size", "n_genes_detected"])
d = d[d.broad.isin(["Epithelial", "Immune", "Stromal"])]
d["lt500"] = d.n_genes_detected < 500
out = Path(sys.argv[2])
by_sample = (d.groupby(["study_id", "patient_id", "sample_id", "broad"])
             .agg(cells=("lt500", "size"), lt500_cells=("lt500", "sum")).reset_index())
by_sample["lt500_pct"] = (100 * by_sample.lt500_cells / by_sample.cells).round(1)
by_sample.to_csv(out / "low_gene_cells_by_sample.csv", index=False)
by_study = (d.groupby(["study_id", "broad"]).agg(cells=("lt500", "size"), lt500_pct=("lt500", "mean"))
            .reset_index())
by_study["lt500_pct"] = (100 * by_study.lt500_pct).round(1)
qc = d.groupby("study_id").agg(min_genes=("n_genes_detected", "min"), min_umi=("library_size", "min"),
                                p01_genes=("n_genes_detected", lambda s: s.quantile(0.01))).reset_index()
by_study = by_study.merge(qc, on="study_id")
by_study.to_csv(out / "low_gene_cells_by_study.csv", index=False)
print(by_study.pivot(index="study_id", columns="broad", values="lt500_pct").to_string())
print(qc.to_string(index=False))
