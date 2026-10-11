#!/usr/bin/env python3
"""A3b Stage S QC (before estimands): CT2 scoring success per variant, and equality of A3b original-depth scores
with Fig. 1b full-run scores for tumour samples present in both (same pipeline, same cells -> must match).
Outputs: <public>/A3b_ct2_qc.tsv, <public>/A3b_ct2_fig1b_equality.tsv
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--fig1b-scores", required=True)
    ap.add_argument("--public", required=True)
    a = ap.parse_args()
    R, P = Path(a.root) / "ct2", Path(a.public)
    rows = []
    for v, cd in [("main", "counts_main"), ("np", "counts_ds_np"), ("pp", "counts_ds_pp")]:
        m = pd.read_csv(R / cd / "export_manifest.tsv", sep="\t")
        done = {f.name.replace(".scores.tsv.gz", ".h5") for f in (R / f"scores_{v}").glob("*.scores.tsv.gz")}
        m["scored"] = m.file.isin(done)
        rows.append(dict(variant=v, files=len(m), scored=int(m.scored.sum()), cells=int(m.cells.sum()),
                         missing=";".join(m.loc[~m.scored, "file"].head(20))))
    pd.DataFrame(rows).to_csv(P / "A3b_ct2_qc.tsv", sep="\t", index=False)
    eq = []
    for f in sorted((R / "scores_main").glob("*.scores.tsv.gz")):
        g = Path(a.fig1b_scores) / f.name
        if not g.exists():
            continue
        x = pd.read_csv(f, sep="\t").set_index("cell_id")
        y = pd.read_csv(g, sep="\t").set_index("cell_id")
        common = x.index.intersection(y.index)
        eq.append(dict(file=f.name, cells_a3b=len(x), cells_fig1b=len(y), common=len(common),
                       max_abs_diff_whole=float(np.abs(x.loc[common, "whole_score"] - y.loc[common, "whole_score"]).max()),
                       max_abs_diff_intrinsic=float(np.abs(x.loc[common, "intrinsic_score"] - y.loc[common, "intrinsic_score"]).max())))
    e = pd.DataFrame(eq)
    e.to_csv(P / "A3b_ct2_fig1b_equality.tsv", sep="\t", index=False)
    print(pd.DataFrame(rows).to_string())
    if len(e):
        print("overlap samples", len(e), "identical cell sets", int((e.cells_a3b == e.cells_fig1b).sum()),
              "max diff whole", e.max_abs_diff_whole.max(), "intrinsic", e.max_abs_diff_intrinsic.max())


if __name__ == "__main__":
    main()
