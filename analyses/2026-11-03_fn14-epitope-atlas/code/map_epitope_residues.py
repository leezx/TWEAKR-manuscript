"""Map experimentally implicated antibody-epitope residues onto the frozen M2-C TWEAK3-Fn14x3 model.

    $BIOWORKSPACE_ROOT/SOFTWARES/tools/pymol-open-source/.venv/bin/python map_epitope_residues.py
Run from code/. Writes ../tables/epitope_residue_geometry.tsv.

Residues are UniProt Q9NP84 precursor numbering; the M2 Fn14 chains (D,E,F) are construct 1-53 = UniProt - 27.
This measures geometry only. Whether an antibody actually competes with TWEAK is an experimental question;
a residue far from the TWEAK contact surface does not rule out steric competition by the whole Fab.
"""
import csv
import os

import numpy as np
from pymol import cmd

M2 = os.environ.get("FN14_M2_MODEL", "/Volumes/Stelligen_SSD/Stelligen/DATA/HotData/TWEAKR-oncoFetal/"
                    "analysis/af3_M2/frozen/af3_M2/m2_tweak3_fn14x3_tmplc/m2_tweak3_fn14x3_tmplc_model.cif")
OUT = os.path.join(os.getcwd(), "..", "tables", "epitope_residue_geometry.tsv")
TW, FN = "ABC", "DEF"
# residue -> (expected one-letter, why it is here, evidence level per docs/design.md)
SITES = {
    42: ("W", "PDL192/P4A8 binding lost on W42A (Trebing 2014, abstract)", "E2"),
    56: ("R", "PDL192/P4A8 binding lost on R56P (Trebing 2014, abstract)", "E2"),
    45: ("D", "TWEAK binding (Brown 2006)", "reference"),
    48: ("K", "TWEAK binding (Brown 2006)", "reference"),
    50: ("M", "TWEAK binding (Brown 2006)", "reference"),
    62: ("D", "TWEAK binding (Brown 2006)", "reference"),
}
THREE2ONE = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G",
             "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S",
             "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}

cmd.load(M2, "m")
cmd.remove("hydro")


def coords(sel):
    x = cmd.get_coords(sel)
    if x is None or len(x) == 0:
        raise ValueError("empty selection: " + sel)
    return np.asarray(x, float)


def min_dist(a, b):
    return float(np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)).min())


# per-chain solvent accessibility of the isolated receptor (no ligand), for "is it reachable by an antibody"
cmd.set("dot_solvent", 1)
cmd.set("dot_density", 3)

rows = []
for ch in FN:
    partner = coords(f"m and chain {'+'.join(TW)} and not hydro")
    # interface set of this copy, recomputed here so the table is self-contained
    iface = set()
    for r in range(1, 54):
        try:
            if min_dist(coords(f"m and chain {ch} and resi {r} and not hydro"), partner) <= 5.0:
                iface.add(r)
        except ValueError:
            pass
    cmd.create("solo", f"m and chain {ch}")
    for uni, (aa, why, lvl) in sorted(SITES.items()):
        c = uni - 27
        sel = f"m and chain {ch} and resi {c}"
        resn = cmd.get_model(f"{sel} and name CA").atom[0].resn
        assert THREE2ONE[resn] == aa, (uni, resn, aa)
        x = coords(f"{sel} and not hydro")
        d_tweak = min_dist(x, partner)
        sasa = cmd.get_area(f"solo and resi {c}")          # isolated receptor
        sasa_cplx = cmd.get_area(sel)                       # within the complex
        # distance from this residue to the nearest residue that does contact TWEAK
        if iface:
            d_iface = min(min_dist(x, coords(f"m and chain {ch} and resi {r} and not hydro"))
                          for r in iface if r != c)
        else:
            d_iface = float("nan")
        rows.append({
            "fn14_chain": ch, "uniprot_resi": uni, "resn": aa, "evidence_level": lvl, "basis": why,
            "min_dist_to_TWEAK_A": round(d_tweak, 2),
            "in_TWEAK_interface_5A": c in iface,
            "dist_to_nearest_interface_residue_A": round(d_iface, 2),
            "sasa_isolated_receptor_A2": round(sasa, 1),
            "sasa_in_complex_A2": round(sasa_cplx, 1),
            "sasa_buried_by_TWEAK_A2": round(sasa - sasa_cplx, 1),
        })
    cmd.delete("solo")

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader()
    w.writerows(rows)

for uni in sorted(SITES):
    rr = [r for r in rows if r["uniprot_resi"] == uni]
    print(f"{SITES[uni][0]}{uni} [{SITES[uni][2]:>9}] "
          f"dist->TWEAK {min(r['min_dist_to_TWEAK_A'] for r in rr):.2f}-{max(r['min_dist_to_TWEAK_A'] for r in rr):.2f} A | "
          f"in interface {sum(r['in_TWEAK_interface_5A'] for r in rr)}/3 | "
          f"SASA free {np.mean([r['sasa_isolated_receptor_A2'] for r in rr]):.0f} A2 | "
          f"buried by TWEAK {np.mean([r['sasa_buried_by_TWEAK_A2'] for r in rr]):.0f} A2")
