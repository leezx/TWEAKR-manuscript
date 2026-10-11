#!/usr/bin/env python3
"""A3b metadata gate, step 2: within-patient pair feasibility (metadata only; no CytoTRACE2).

Input: tables/metadata_gate/sample_metadata.tsv (one row per Atlas sample, from sample_metadata.py).
Pair designs (same patient, both sides required):
  normal_primary   adjacent normal  vs primary tumour
  pre_post         primary tumour treatment-naive vs primary tumour treated
  primary_met      primary tumour vs metastasis
  healthy_normal   healthy-donor normal (not paired; listed for completeness)
Gate rules (fixed before looking at any score):
  - side epithelial cells = harmonized epithelial `atlas_cell_type_middle` summed over the patient's samples of that side;
  - a side is usable when it has >= 30 epithelial cells (also reported at >= 100);
  - immune-enriched samples (CD45+/CD3+/... sorts) are excluded before summing;
  - a pair needs both sides usable; a study qualifies when it has >= 5 usable pairs.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parents[1]
T = HERE / "tables" / "metadata_gate"
UNSORTED = {"naive", "AnnexinV-"}
NON_IMMUNE = {"mixCD45+CD45-", "CD45+/CD45-", "CD45-", "EPCAM+", "EPCAM-/CD45-/CD31-", "epithelial"}
THRESH = (30, 100)


def sort_class(v):
    if v in UNSORTED:
        return "unsorted"
    if v in NON_IMMUNE:
        return "non_immune_or_mixed"
    return "immune_enriched" if isinstance(v, str) and v not in ("NA", "nan") else "unknown"


def side(d, mask, name):
    s = d[mask & (d.sort_class != "immune_enriched")]
    g = s.groupby(["study_id", "patient_id"])
    out = g.agg(**{f"{name}_samples": ("sample_id", "nunique"), f"{name}_epi": ("epi_total", "sum"),
                   f"{name}_cancer_cell": ("epi_Cancer_cell", "sum"), f"{name}_epi_cell": ("epi_Epithelial_cell", "sum"),
                   f"{name}_epi_umi_median": ("epi_median_umi", "median"),
                   f"{name}_platform": ("platform", lambda x: "|".join(sorted(set(map(str, x))))),
                   f"{name}_sort": ("sort_class", lambda x: "|".join(sorted(set(map(str, x))))),
                   f"{name}_tumor_source": ("tumor_source", lambda x: "|".join(sorted(set(map(str, x))))),
                   f"{name}_tissue": ("tissue", lambda x: "|".join(sorted(set(map(str, x))))),
                   f"{name}_treatment": ("treatment_status_before_resection", lambda x: "|".join(sorted(set(map(str, x))))),
                   f"{name}_drug": ("treatment_drug", lambda x: "|".join(sorted(set(map(str, x))))),
                   f"{name}_response": ("treatment_response", lambda x: "|".join(sorted(set(map(str, x))))),
                   f"{name}_RECIST": ("RECIST", lambda x: "|".join(sorted(set(map(str, x)))))})
    return out


def pairs(d, a_mask, a, b_mask, b, design):
    p = side(d, a_mask, a).join(side(d, b_mask, b), how="inner").reset_index()
    p.insert(0, "design", design)
    for t in THRESH:
        p[f"usable_{t}"] = (p[f"{a}_epi"] >= t) & (p[f"{b}_epi"] >= t)
    p["same_platform"] = p[f"{a}_platform"] == p[f"{b}_platform"]
    return p


def study_summary(p):
    rows = []
    for (des, st), g in p.groupby(["design", "study_id"]):
        r = {"design": des, "study_id": st, "pairs_metadata": len(g),
             "usable_30": int(g.usable_30.sum()), "usable_100": int(g.usable_100.sum()),
             "same_platform": int(g.same_platform.sum())}
        for c in g.columns:
            if c != "same_platform" and c.endswith(("_drug", "_response", "_RECIST", "_tissue", "_treatment", "_sort", "_platform")):
                r[c] = "; ".join(sorted(set(g.loc[g.usable_30, c].dropna().astype(str)))) if g.usable_30.any() else ""
        rows.append(r)
    s = pd.DataFrame(rows)
    s["study_qualifies_30"] = s.usable_30 >= 5
    s["study_qualifies_100"] = s.usable_100 >= 5
    return s


def main():
    d = pd.read_csv(T / "sample_metadata.tsv", sep="\t")
    d["sort_class"] = d.enrichment_cell_types.map(sort_class)
    prim = d.sample_type == "primary tumor"
    norm = d.sample_type == "adjacent normal"
    met = d.sample_type == "metastasis"
    naive = d.treatment_status_before_resection == "naive"
    treated = d.treatment_status_before_resection == "treated"
    P = [
        pairs(d, norm & naive, "normal", prim & naive, "tumour", "normal_primary_naive"),
        pairs(d, norm, "normal", prim, "tumour", "normal_primary_any_treatment"),
        pairs(d, prim & naive, "pre", prim & treated, "post", "pre_post_primary"),
        pairs(d, prim, "primary", met, "met", "primary_met_any_treatment"),
    ]
    allp = pd.concat(P, ignore_index=True)
    allp.to_csv(T / "pair_gate_patients.tsv", sep="\t", index=False)
    s = study_summary(allp)
    s.to_csv(T / "pair_gate_studies.tsv", sep="\t", index=False)
    tot = s.groupby("design").agg(studies_with_pairs=("study_id", "size"), pairs_metadata=("pairs_metadata", "sum"),
                                  usable_30=("usable_30", "sum"), usable_100=("usable_100", "sum"),
                                  studies_qualify_30=("study_qualifies_30", "sum"),
                                  pairs_in_qualifying_studies_30=("usable_30", lambda x: int(x[x >= 5].sum())))
    tot.to_csv(T / "pair_gate_overview.tsv", sep="\t")
    print(tot.to_string())
    # healthy-donor normal and polyp: not pairable, described only
    h = d[d.sample_type.isin(["healthy normal", "polyp"])].groupby(["sample_type", "study_id"]).agg(
        samples=("sample_id", "nunique"), patients=("patient_id", "nunique"), epi=("epi_total", "sum"),
        platform=("platform", lambda x: "|".join(sorted(set(map(str, x))))))
    h.to_csv(T / "unpaired_normal_polyp.tsv", sep="\t")
    print(h.to_string())


if __name__ == "__main__":
    main()
