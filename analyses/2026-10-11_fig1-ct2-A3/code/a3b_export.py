#!/usr/bin/env python3
"""A3b Stage I step 1 (one SGE task per study; contract A3b v0.3 §1, §5). No CT2, no programme score.

For every sample of the study in tables/metadata_gate/a3b_samples.tsv:
  - broad lineage from atlas_cell_type_middle (screen_compartments.py maps);
  - F1 = frozen Fig. 1b A2.1 rule (l2_config.yaml l1_flags; l2_build.py logic): >= f1_min_genes genes of a
    panel foreign to the cell's broad lineage, each >= f1_min_umi UMI. Checked to equal annotation_v1 F1 on
    every cohort-v1 cell (mismatch -> stop);
  - L1 epithelium = broad Epithelial & not F1 -> <sample>.epi.h5 (all genes, raw counts) + per-cell table
    (umi, detected genes, mito fraction, S/G2M/phase, Atlas fine label).
Per patient (all of its A3b samples together): inferCNV inputs, Fig. 1b L2 rule with an independent per-patient
RNG (seed 0): observations = L1 epithelium grouped by sample; reference = non-F1 immune + stromal cells,
<= 1,500, half/half with spare quota passed over; < 100 reference cells -> not assessable. Autosomal genes
ordered by Atlas position.
"""
import argparse
import gzip
import re
import sys
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import yaml
from scipy import io
from scipy import sparse as sp


def dec(x):
    return x.decode() if isinstance(x, bytes) else str(x)


def safe(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", s)


def read_col(obs, key):
    g = obs[key]
    if isinstance(g, h5py.Group):
        cats = np.array([dec(c) for c in g["categories"][:]], dtype=object)
        codes = g["codes"][:]
        out = np.full(codes.shape, "NA", dtype=object)
        out[codes >= 0] = cats[codes[codes >= 0]]
        return out
    v = g[:]
    return np.array([dec(x) for x in v], dtype=object) if v.dtype.kind in "SO" else v


def read_rows(mat, indptr, rows, n_genes, slab=100_000_000):
    data, ind, lens = [], [], []
    i = 0
    while i < len(rows):
        j = i
        while j + 1 < len(rows) and indptr[rows[j + 1] + 1] - indptr[rows[i]] <= slab:
            j += 1
        lo, hi = indptr[rows[i]], indptr[rows[j] + 1]
        d, x = mat["data"][lo:hi], mat["indices"][lo:hi]
        for r in rows[i:j + 1]:
            a, b = indptr[r] - lo, indptr[r + 1] - lo
            data.append(d[a:b]); ind.append(x[a:b]); lens.append(b - a)
        i = j + 1
    ptr = np.concatenate([[0], np.cumsum(lens)])
    return sp.csr_matrix((np.concatenate(data).astype(np.float32), np.concatenate(ind), ptr),
                         shape=(len(rows), n_genes))


def write_h5(path, x, genes, cells):
    y = x.T.tocsc()
    with h5py.File(path, "w") as h:
        h["data"] = y.data.astype(np.int32)
        h["indices"] = y.indices.astype(np.int32)
        h["indptr"] = y.indptr.astype(np.int64)
        h["shape"] = np.array(y.shape, dtype=np.int64)
        h["genes"] = np.array(genes, dtype="S")
        h["cells"] = np.array(cells, dtype="S")


def chrom_num(x):
    m = re.fullmatch(r"(?:chr)?(\d+)", str(x))
    return int(m.group(1)) if m and 1 <= int(m.group(1)) <= 22 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--samples", required=True)
    ap.add_argument("--l2-config", required=True)
    ap.add_argument("--screen-code", required=True, help="dir with screen_compartments.py")
    ap.add_argument("--annotation", required=True, help="Fig. 1b annotation_v1.tsv.gz (F1 check)")
    ap.add_argument("--study", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    sys.path.insert(0, a.screen_code)
    from screen_compartments import BROAD_OF, MIDDLE_TO_LINEAGE  # noqa: E402
    cfg = yaml.safe_load(open(a.l2_config))
    fl, cc = cfg["l1_flags"], cfg["infercnv"]
    out = Path(a.out_dir)
    for d in ["counts", "cells", "cnv_inputs"]:
        (out / d).mkdir(parents=True, exist_ok=True)

    sl = pd.read_csv(a.samples, sep="\t")
    sl = sl[sl.study_id == a.study]
    samples = sorted(sl.sample_id.unique())
    ann = pd.read_csv(a.annotation, sep="\t", usecols=["cell_id", "F1"])
    ann_f1 = dict(zip(ann.cell_id.astype(str), ann.F1.astype(str) == "True"))

    with h5py.File(a.h5ad, "r") as f:
        obs = f["obs"]
        idx = np.array([dec(x) for x in obs[obs.attrs["_index"]][:]], dtype=object)
        sid = read_col(obs, "sample_id")
        sel = np.flatnonzero(np.isin(sid, samples))
        meta = pd.DataFrame({"cell_id": idx[sel], "row": sel, "sample_id": sid[sel]})
        for k in ["patient_id", "atlas_cell_type_middle", "atlas_cell_type_fine"]:
            meta[k] = read_col(obs, k)[sel]
        for k in ["S_score", "G2M_score", "phase"]:
            meta[k] = read_col(obs, k)[sel]
        var = f["var"]
        genes = np.array([dec(x) for x in var["var_names"][:]], dtype=object)
        chrom = read_col(var, "Chromosome")
        start = pd.to_numeric(pd.Series(read_col(var, "Start")), errors="coerce").to_numpy()
        end = pd.to_numeric(pd.Series(read_col(var, "End")), errors="coerce").to_numpy()
        mat = f["layers/counts"]
        indptr = mat["indptr"][:]
        n_genes = int(mat.attrs["shape"][1])
        meta = meta.sort_values("row").reset_index(drop=True)
        X = read_rows(mat, indptr, meta.row.to_numpy(), n_genes)

    meta["lineage"] = pd.Series(meta.atlas_cell_type_middle).map(MIDDLE_TO_LINEAGE).fillna("Other")
    meta["broad"] = meta.lineage.map(BROAD_OF).fillna("Other")
    gpos = {g: i for i, g in enumerate(genes)}
    meta["F1"] = False
    for name, spec in fl["panels"].items():
        cols = [gpos[g] for g in spec["genes"] if g in gpos]
        hit = np.asarray((X[:, cols] >= fl["f1_min_umi"]).sum(axis=1)).ravel() >= fl["f1_min_genes"]
        foreign = (meta.broad.isin(["Epithelial", "Immune", "Stromal"]) & (meta.broad != spec["lineage"])).to_numpy()
        meta.loc[hit & foreign, "F1"] = True
    chk = meta.cell_id.map(ann_f1)
    m = chk.notna()
    mismatch = int((chk[m].astype(bool) != meta.F1[m]).sum())
    print(f"F1 check vs annotation_v1: {int(m.sum())} cohort cells, {mismatch} mismatches", flush=True)
    if mismatch:
        raise ValueError("F1 differs from Fig. 1b annotation_v1")

    mt = np.flatnonzero(pd.Series(genes).str.startswith("MT-").to_numpy())
    umi = np.asarray(X.sum(axis=1)).ravel()
    meta["umi"] = umi
    meta["genes"] = np.diff(X.indptr)
    meta["mito_frac"] = np.divide(np.asarray(X[:, mt].sum(axis=1)).ravel(), umi, out=np.zeros_like(umi), where=umi > 0)
    meta["L1_epi"] = (meta.broad == "Epithelial") & ~meta.F1
    side = sl.drop_duplicates("sample_id").set_index("sample_id")
    meta["side"] = meta.sample_id.map(side.side)
    meta["stage"] = meta.sample_id.map(side.stage)

    epi_rows = []
    for s, g in meta[meta.L1_epi].groupby("sample_id"):
        ii = g.index.to_numpy()
        write_h5(out / "counts" / f"{safe(s)}.epi.h5", X[ii], genes, g.cell_id.to_numpy())
        epi_rows.append(g)
    cells = pd.concat(epi_rows).drop(columns=["row", "lineage"])
    cells.insert(1, "study_id", a.study)
    cells.to_csv(out / "cells" / f"{safe(a.study)}.epi_cells.tsv.gz", sep="\t", index=False)
    meta.groupby(["sample_id", "broad", "F1"]).size().rename("cells").reset_index().to_csv(
        out / "cells" / f"{safe(a.study)}.lineage_counts.tsv", sep="\t", index=False)

    # inferCNV inputs per patient
    ok = np.array([chrom_num(c) is not None for c in chrom]) & ~np.isnan(start)
    order = pd.DataFrame({"gene": genes[ok], "chr": [chrom_num(c) for c in chrom[ok]], "start": start[ok],
                          "end": np.where(np.isnan(end[ok]), start[ok], end[ok]), "col": np.flatnonzero(ok)})
    order = order.sort_values(["chr", "start"])
    if order.gene.duplicated().any():
        raise ValueError("duplicate autosomal gene symbols")
    gcols = order.col.to_numpy()
    cnv_dir = out / "cnv_inputs"
    pd.DataFrame({"gene": order.gene, "chr": "chr" + order.chr.astype(int).astype(str),
                  "start": order.start.astype(int), "end": order.end.astype(int)}).to_csv(
        cnv_dir / "gene_order.tsv", sep="\t", index=False, header=False)
    order.gene.to_csv(cnv_dir / "genes.txt", index=False, header=False)
    man = []
    for pid, g in meta.groupby("patient_id"):
        rng = np.random.default_rng(cc.get("seed", 0))
        epi = g[g.L1_epi]
        ref = {L: g[(g.broad == L) & ~g.F1] for L in ["Immune", "Stromal"]}
        avail = {L: len(ref[L]) for L in ref}
        half = cc["ref_max_cells"] // 2
        take = {L: min(avail[L], half) for L in ref}
        spare = cc["ref_max_cells"] - sum(take.values())
        for L in ref:
            extra = min(spare, avail[L] - take[L])
            take[L] += extra
            spare -= extra
        n_ref = sum(take.values())
        rec = dict(study_id=a.study, patient_id=pid, n_obs=len(epi), n_ref_immune=take["Immune"],
                   n_ref_stromal=take["Stromal"], assessable=bool(n_ref >= cc["ref_min_cells"] and len(epi) > 0),
                   dir=safe(pid))
        man.append(rec)
        if not rec["assessable"]:
            continue
        rows = [epi.index.to_numpy()]
        grp = ["obs__" + safe(x) for x in epi.sample_id]
        for L, lab in [("Immune", "ref_immune"), ("Stromal", "ref_stromal")]:
            if take[L]:
                pick = np.sort(rng.choice(avail[L], take[L], replace=False))
                rows.append(ref[L].index.to_numpy()[pick])
                grp += [lab] * take[L]
        rows = np.concatenate(rows)
        d = cnv_dir / rec["dir"]
        d.mkdir(exist_ok=True)
        M = X[rows][:, gcols].T.tocsr()
        with gzip.open(d / "counts.mtx.gz", "wb") as fh:
            io.mmwrite(fh, M, field="real")
        cid = meta.cell_id.to_numpy()[rows]
        pd.Series(cid).to_csv(d / "cells.txt", index=False, header=False)
        pd.DataFrame({"cell": cid, "group": grp}).to_csv(d / "annotation.tsv", sep="\t", index=False, header=False)
        # tumour-side (pre/primary) cells define the top-5% CNV profile (contract §5)
        tum = epi[(epi.side == "tumour") & epi.stage.isin(["naive", "Pre"])].cell_id
        pd.Series(tum).to_csv(d / "profile_cells.txt", index=False, header=False)
        print(pid, len(epi), n_ref, len(tum), flush=True)
    pd.DataFrame(man).to_csv(cnv_dir / f"{safe(a.study)}.patients.tsv", sep="\t", index=False)
    (out / "cells" / f"{safe(a.study)}.DONE").write_text("ok\n")


if __name__ == "__main__":
    main()
