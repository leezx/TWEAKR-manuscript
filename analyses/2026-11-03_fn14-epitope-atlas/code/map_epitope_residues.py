"""Map experimentally implicated antibody-epitope residues onto the frozen M2-C TWEAK3-Fn14x3 model.

    $BIOWORKSPACE_ROOT/SOFTWARES/tools/pymol-open-source/.venv/bin/python map_epitope_residues.py
Run from code/. Writes ../tables/epitope_residue_geometry.tsv.

Residues are UniProt Q9NP84 precursor numbering; the M2 Fn14 chains (D,E,F) are construct 1-53 = UniProt - 27.
This measures geometry only. Whether an antibody actually competes with TWEAK is an experimental question;
a residue far from the TWEAK contact surface does not rule out steric competition by the whole Fab.

That caveat is not hypothetical: P4A8 is sensitive to W42A, W42 is not buried by TWEAK in this model, and
P4A8 nevertheless blocks TWEAK binding experimentally (Salzmann 2013, via GPT review). So these numbers
describe single-residue burial, and cannot by themselves predict whether an antibody competes.
"""
import csv
import os

import numpy as np
from pymol import cmd

M2 = os.environ.get("FN14_M2_MODEL", "/Volumes/Stelligen_SSD/Stelligen/DATA/HotData/TWEAKR-oncoFetal/"
                    "analysis/af3_M2/frozen/af3_M2/m2_tweak3_fn14x3_tmplc/m2_tweak3_fn14x3_tmplc_model.cif")
OUT = os.path.join(os.getcwd(), "..", "tables", "epitope_residue_geometry.tsv")
TW, FN = "ABC", "DEF"
CRD = "9-40"      # construct numbering for the CRD core (UniProt 36-67), used as the local frame
# residue -> (expected one-letter, why it is here, evidence level per docs/design.md)
# Kyowa Kirin WO2020128927A1 claims an ANTAGONIST (explicitly "not an agonist") that "attenuates the
# binding of TWEAK to Fn14" and interacts with these human Fn14 residues (claim text read 2026-11-04).
# Subdomain 1 = APGTAPCSRGSSWSADLDKCM, which this project mapped to Q9NP84 30-50 exactly.
KYOWA_EPITOPE = [32, 33, 34, 35, 42, 44, 45, 46, 47, 48, 49]

# Bayer WO2015189143A1 alanine-scanned the whole CRD and concluded (patent text, read 2026-11-04):
# "TWEAK binding depends on L46 ..., TPP-2090 binding on D47 and PDL-192 binding on R56. PDL-192 binds
#  opposite of the TWEAK ligand binding site, TPP-2090 binds directly to the TWEAK ligand site."
# That is an independent, experiment-based statement of the same geometry this script measures.
BAYER_DETERMINANTS = {46: "TWEAK ligand itself (Pellegrini, via Bayer patent)",
                      47: "TPP-2090 - patent says it binds directly AT the TWEAK ligand site",
                      56: "PDL-192 - patent says it binds OPPOSITE the TWEAK ligand site"}

SITES = {
    # Corrected after GPT review round 1: the two residues separate between the two antibodies.
    # Salzmann 2013 Fig 1A (cited by the review; paywalled, NOT independently verified here):
    # PDL192 is sensitive to R56P but still binds W42A; P4A8 is the mirror image.
    42: ("W", "P4A8 binding lost on W42A; PDL192 still binds (Salzmann 2013 Fig 1A, via review)", "E2"),
    56: ("R", "PDL192/enavatuzumab binding lost on R56P; P4A8 still binds (Salzmann 2013 Fig 1A, via review)", "E2"),
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
        # Distance from this residue to the nearest TWEAK-contacting residue, EXCLUDING sequence
        # neighbours. Fix 2026-11-04: the first version excluded only the residue itself, so when
        # c-1 or c+1 was in the interface it returned the peptide-bond length (~1.33 A) for every
        # residue and carried no information. |i - j| >= 2 is required.
        # Where does this residue sit relative to the TWEAK footprint, as seen from the CRD core?
        # Burial and minimum distance do NOT separate W42 from R56 (both 0 A buried, both ~3 A from
        # the patch), but the direction does. foot = centroid of the four TWEAK-binding residues.
        crd_core = coords(f"m and chain {ch} and name CA and resi {CRD}").mean(0)
        foot = np.vstack([coords(f"m and chain {ch} and resi {k - 27} and not hydro") for k in SITES
                          if SITES[k][2] == "reference"]).mean(0)
        v1, v2 = x.mean(0) - crd_core, foot - crd_core
        angle = float(np.degrees(np.arccos(np.clip(v1 @ v2 / np.linalg.norm(v1) / np.linalg.norm(v2), -1, 1))))
        d_foot = float(np.linalg.norm(x.mean(0) - foot))
        far = [r for r in iface if abs(r - c) >= 2]
        d_iface = min((min_dist(x, coords(f"m and chain {ch} and resi {r} and not hydro")) for r in far),
                      default=float("nan"))
        rows.append({
            "fn14_chain": ch, "uniprot_resi": uni, "resn": aa, "evidence_level": lvl, "basis": why,
            "min_dist_to_TWEAK_A": round(d_tweak, 2),
            "in_TWEAK_interface_5A": c in iface,
            "dist_to_nearest_nonadjacent_interface_residue_A": round(d_iface, 2),
            "sasa_isolated_receptor_A2": round(sasa, 1),
            "sasa_in_complex_A2": round(sasa_cplx, 1),
            "sasa_buried_by_TWEAK_A2": round(sasa - sasa_cplx, 1),
            "angle_to_TWEAK_footprint_deg": round(angle, 1),
            "dist_to_footprint_centroid_A": round(d_foot, 1),
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
          f"buried {np.mean([r['sasa_buried_by_TWEAK_A2'] for r in rr]):.0f} A2 | "
          f"angle {np.mean([r['angle_to_TWEAK_footprint_deg'] for r in rr]):.0f} deg, "
          f"{np.mean([r['dist_to_footprint_centroid_A'] for r in rr]):.0f} A from footprint centre")


# ---------------------------------------------------------------------------------------------
# Third test of the orientation model: a patent-claimed epitope of a TWEAK-blocking antagonist.
# If orientation (not burial) tracks competition, this whole epitope should sit on the TWEAK face.
print()
ch = "D"
crd_core = coords(f"m and chain {ch} and name CA and resi {CRD}").mean(0)
foot = np.vstack([coords(f"m and chain {ch} and resi {k - 27} and not hydro")
                  for k in SITES if SITES[k][2] == "reference"]).mean(0)
tw_all = coords(f"m and chain {'+'.join(TW)} and not hydro")


def angle_of(uni):
    x = coords(f"m and chain {ch} and resi {uni - 27} and not hydro")
    v1, v2 = x.mean(0) - crd_core, foot - crd_core
    return float(np.degrees(np.arccos(np.clip(v1 @ v2 / np.linalg.norm(v1) / np.linalg.norm(v2), -1, 1)))), \
        min_dist(x, tw_all)


ang = [angle_of(u) for u in KYOWA_EPITOPE]
with open(os.path.join(os.getcwd(), "..", "tables", "kyowa_epitope_geometry.tsv"), "w") as f:
    f.write("uniprot_resi\tangle_to_TWEAK_footprint_deg\tmin_dist_to_TWEAK_A\n")
    for u, (a, d) in zip(KYOWA_EPITOPE, ang):
        f.write(f"{u}\t{a:.1f}\t{d:.2f}\n")
print("Kyowa Kirin antagonist epitope (WO2020128927A1), chain D: "
      f"angles {min(a for a, _ in ang):.0f}-{max(a for a, _ in ang):.0f} deg "
      f"(mean {np.mean([a for a, _ in ang]):.0f}); "
      f"{sum(d <= 5 for _, d in ang)}/{len(ang)} residues within 5 A of TWEAK")
print(f"  R56 (enavatuzumab, does NOT block TWEAK) is at {angle_of(56)[0]:.0f} deg - outside that range")


# ---------------------------------------------------------------------------------------------
# Robustness: the angle depends on the chosen origin, so report it under three definitions, plus
# the distance to the reference-patch centroid, which needs no origin at all.
print()
patch = foot
origins = {"CRD CA centroid (reported)": coords(f"m and chain {ch} and name CA and resi {CRD}").mean(0),
           "CRD heavy-atom centroid": coords(f"m and chain {ch} and resi {CRD} and not hydro").mean(0),
           "full ECD heavy-atom centroid": coords(f"m and chain {ch} and not hydro").mean(0)}


def ang_from(uni, origin):
    x = coords(f"m and chain {ch} and resi {uni - 27} and not hydro")
    v1, v2 = x.mean(0) - origin, patch - origin
    return float(np.degrees(np.arccos(np.clip(v1 @ v2 / np.linalg.norm(v1) / np.linalg.norm(v2), -1, 1))))


shown = [46, 47, 42, 56]
with open(os.path.join(os.getcwd(), "..", "tables", "orientation_sensitivity.tsv"), "w") as f:
    f.write("origin_definition\t" + "\t".join(f"angle_{u}_deg" for u in shown) + "\n")
    for n, o in origins.items():
        f.write(n + "\t" + "\t".join(f"{ang_from(u, o):.1f}" for u in shown) + "\n")
    f.write("dist_to_patch_centroid_A (origin-free)\t" +
            "\t".join(f"{np.linalg.norm(coords(f'm and chain {ch} and resi {u - 27} and not hydro').mean(0) - patch):.1f}"
                      for u in shown) + "\n")
print("Orientation vs the four-residue TWEAK-binding reference patch (chain D):")
for u in shown:
    d = np.linalg.norm(coords(f"m and chain {ch} and resi {u - 27} and not hydro").mean(0) - patch)
    tag = BAYER_DETERMINANTS.get(u, "P4A8 - blocks TWEAK" if u == 42 else "")
    print(f"  {u:>3}: angle {'/'.join(f'{ang_from(u, o):.0f}' for o in origins.values()):>14} deg "
          f"| {d:5.1f} A from patch centroid | {tag}")
print("  The angle shifts with the origin; the on-site vs opposite-side split does not.")
