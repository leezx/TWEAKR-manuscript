#!/usr/bin/env python3
"""Map COSMOS celltype_shortname labels to the authors' cell-type-level origin
(Wang et al. Nature 2026, Supplementary Table 13a fetal / 13b maternal).

This is author_cell_type_origin, never a per-cell genotype assignment.
Unmatched labels are 'ambiguous'; labels supported by both tables are 'mixed'.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import anndata as ad
import openpyxl
import pandas as pd

# COSMOS label -> Supp Table 13 label, only where names differ but are unambiguous.
NAME_EQUIVALENT = {
    "EVT": "other EVT",
    "CD14_M": "M(CD14)",
    "CD16_M": "M(CD16)",
    "SCT_pro": "SCTpro",
    "VCT_dividing": "VCT(MKI67)",
}

ANALYSIS_ROLE_BY_SHORTNAME = {
    "CD14_M": "ligand_candidate", "CD16_M": "ligand_candidate",
    "HB": "fetal_macrophage_control",
    "fEC": "specificity_control", "aEC": "specificity_control", "vEC": "specificity_control",
}
ANALYSIS_ROLE_BY_MINOR = {
    "EVT": "receptor_candidate_EVT", "VCT": "receptor_candidate_VCT", "SCT": "receptor_candidate_SCT",
    "DSC": "alternative_receptor_maternal_stroma", "eS": "alternative_receptor_maternal_stroma",
}


def analysis_role(short: str, minor: str) -> str:
    return ANALYSIS_ROLE_BY_SHORTNAME.get(short) or ANALYSIS_ROLE_BY_MINOR.get(minor, "")


def read_s13(path: Path, sheet: str) -> list[str]:
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[sheet]
    rows = list(ws.iter_rows(values_only=True))
    return [str(r[0]).strip() for r in rows[2:] if r and r[0] is not None]


def classify(short: str, minor: str, major: str, fetal: set[str], maternal: set[str]) -> dict:
    s13 = NAME_EQUIVALENT.get(short, short)
    in_f, in_m = s13 in fetal, s13 in maternal
    if in_f and in_m:
        return dict(s13_label=s13, mapping_basis="listed_in_both_tables", origin="mixed")
    if in_f or in_m:
        # A label matched on one side is still mixed if its parent minor_class is listed on the other side.
        other = maternal if in_f else fetal
        if minor != short and minor in other:
            return dict(s13_label=f"{s13} | {minor}", mapping_basis="conflict_shortname_vs_minor_class",
                        origin="mixed")
        basis = "name_equivalent" if short in NAME_EQUIVALENT else "exact"
        return dict(s13_label=s13, mapping_basis=basis, origin="fetal" if in_f else "maternal")
    if minor in fetal and minor not in maternal:
        return dict(s13_label=minor, mapping_basis="parent_minor_class", origin="fetal")
    if minor in maternal and minor not in fetal:
        return dict(s13_label=minor, mapping_basis="parent_minor_class", origin="maternal")
    return dict(s13_label="", mapping_basis="not_listed", origin="ambiguous")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--h5ad", required=True, type=Path)
    p.add_argument("--supp-table13", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args()

    fetal, maternal = set(read_s13(a.supp_table13, "S13a")), set(read_s13(a.supp_table13, "S13b"))
    obs = ad.read_h5ad(a.h5ad, backed="r").obs
    labels = (obs.groupby(["major_class", "minor_class", "celltype_shortname", "celltype_fullname"], observed=True)
                 .agg(n_cells=("sample_id", "size"), n_donors=("sample_id", "nunique")).reset_index())
    rows = []
    for r in labels.itertuples(index=False):
        c = classify(str(r.celltype_shortname), str(r.minor_class), str(r.major_class), fetal, maternal)
        rows.append({
            "major_class": r.major_class, "minor_class": r.minor_class,
            "celltype_shortname": r.celltype_shortname, "celltype_fullname": r.celltype_fullname,
            "n_cells": r.n_cells, "n_donors": r.n_donors,
            "author_cell_type_origin": c["origin"], "supp_table13_label": c["s13_label"],
            "mapping_basis": c["mapping_basis"],
            "analysis_role": analysis_role(str(r.celltype_shortname), str(r.minor_class)),
        })
    out = pd.DataFrame(rows)
    order = {"maternal": 0, "fetal": 1, "mixed": 2, "ambiguous": 3}
    out = out.sort_values(["author_cell_type_origin", "major_class", "celltype_shortname"],
                          key=lambda s: s.map(order) if s.name == "author_cell_type_origin" else s)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(a.out, sep="\t", index=False)
    unused = (fetal | maternal) - set(out.supp_table13_label.str.split(" | ", regex=False).explode())
    print(out.to_string(index=False))
    print("Supp Table 13 labels not matched to any COSMOS label:", sorted(unused))


if __name__ == "__main__":
    main()
