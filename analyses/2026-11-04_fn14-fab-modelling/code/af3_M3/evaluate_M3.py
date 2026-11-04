"""Evaluate AF3 M3 (Fn14 ECD + Fab VH/VL) against docs/preregistration.md.

The criteria in that file were frozen before submission and are NOT tuned here. This script
only computes the quantities the pre-registration names and prints the verdict its rules imply.

    $BIOWORKSPACE_ROOT/SOFTWARES/tools/pymol-open-source/.venv/bin/python evaluate_M3.py <frozen_dir>

<frozen_dir> holds m3_fn14_fab_f1_pdl192/ and m3_fn14_fab_f2_hup4a8/ as fetched from O2.
Run from code/af3_M3/. Writes ../../tables/M3_{summary,epitope,per_sample}.tsv.

Chains: A = Fn14 28-80 (construct 1-53; UniProt = construct + 27); H = VH; L = VL.
"""
import csv
import glob
import json
import os
import sys

import numpy as np
from pymol import cmd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..",
                                "2026-11-03_tweakr-fn14-structure", "code", "af3_M2"))
from m2_checks import EvalError, check_pairing, kabsch_rmsd, min_distance  # noqa: E402

SRC = sys.argv[1]
STRUCT = os.environ.get(
    "FN14_STRUCT_DIR",
    "/Volumes/Stelligen_SSD/Stelligen/DATA/HotData/TWEAKR-oncoFetal/external/structures_fn14")
TAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tables"))

CONDS = {"f1_pdl192": "m3_fn14_fab_f1_pdl192", "f2_hup4a8": "m3_fn14_fab_f2_hup4a8"}
FN, FAB = "A", ["H", "L"]
CRD = "9-40"           # construct numbering, = UniProt 36-67; same window as M1b/M2
OFF = 27               # UniProt = construct + OFF
CUT = 5.0              # the pre-registered contact cutoff, heavy-atom minimum distance

# --- frozen inputs, copied from the pre-registration (do not edit after results) -------------
# TWEAK contact set: M2-C rank-1 model (seed 2 / sample 0), chain D, <= 5 A.
# Source: 2026-11-03_tweakr-fn14-structure/tables/M2_interface.tsv and docs/M2_results.md L79-84.
TWEAK_SET = {32, 43, 44, 45, 46, 47, 48, 50, 54, 57, 58, 60, 61, 62, 63}
RMSD_MAX = 2.6         # CRD Ca RMSD median vs 2KMZ
IPTM_MIN = 0.50        # chain_pair_iptm, Fab chain vs Fn14
SUPPORT_RATIO = 2.0    # P4A8 overlap >= 2x PDL192 overlap
SUPPORT_P4A8_MIN = 4   # and P4A8 >= 4
SUPPORT_PDL_MAX = 3    # and PDL192 <= 3
# Report-only: WO2009140177A2 (patent-reported, tier B).
# TABLE2 is the set named in the pre-registration and is NOT changed after the fact: it is the
# heavy-chain-CDR-associated subset that this project transcribed from Example 21 Table 2.
TABLE2_HEAVY_SUBSET = [46, 50, 56, 57, 58, 60]
# Correction 2026-11-04 (PR #5 review): that transcription was incomplete. The patent's own
# description text states the antibody "interacts with one or more of residues C49, W42, K48, D51,
# R58, A57, H60, R56, L46, and M50 of human Fnl4" -- 10 residues, verified by this project directly
# in the Google Patents text of WO2009140177A2. The four missed ones pair with light-chain CDRs.
# Reported in addition to, not in place of, the pre-registered subset.
TABLE2_FULL = [42, 46, 48, 49, 50, 51, 56, 57, 58, 60]
# Same source, antibody side: CDR-L1 residues the patent names as Fn14-interacting.
PATENT_CDR_L1 = [32, 34, 36]

cmd.load(os.path.join(STRUCT, "2kmz.pdb"), "nmr")
cmd.remove("hydro")
if cmd.count_states("nmr") != 20:
    raise EvalError(f"2kmz has {cmd.count_states('nmr')} states, expected 20")


def heavy(obj, chain):
    m = cmd.get_model(f"{obj} and chain {chain} and not hydro")
    if not m.atom:
        raise EvalError(f"no atoms in {obj} chain {chain}")
    return (np.array([a.coord for a in m.atom]),
            np.array([int(a.resi) for a in m.atom]))


def epitope(obj):
    """Fn14 residues (UniProt) whose nearest heavy atom to any Fab chain is <= CUT."""
    x, r = heavy(obj, FN)
    px = np.vstack([heavy(obj, c)[0] for c in FAB])
    out = {}
    for rr in np.unique(r):
        out[int(rr) + OFF] = min_distance(x[r == rr], px)
    return out


def _ca(sel, state):
    m = cmd.get_model(f"{sel} and name CA and resi {CRD}", state=state)
    return [(int(a.resi), a.resn) for a in m.atom], np.array([a.coord for a in m.atom])


def crd_rmsd_median(obj):
    """Ca RMSD of the CRD vs each of the 20 2KMZ models; median. Same criterion as M1b/M2.
    Explicit residue pairing, because cmd.rms pairs atoms by identifier including chain."""
    ids_m, xm = _ca(f"{obj} and chain {FN}", 1)
    vals = []
    for st in range(1, 21):
        ids_t, xt = _ca("nmr", st)
        check_pairing(ids_m, ids_t, 32)
        vals.append(kabsch_rmsd(xm, xt))
    return float(np.median(vals))


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else float("nan")


summary, epi_rows, per_sample = [], [], []
res = {}

for tag, sub in CONDS.items():
    d = os.path.join(SRC, sub)
    obj = f"m3_{tag}"
    cmd.load(os.path.join(d, f"{sub}_model.cif"), obj)
    cmd.remove(f"{obj} and hydro")
    chains = sorted(cmd.get_chains(obj))
    if chains != ["A", "H", "L"]:
        raise EvalError(f"{tag}: chains {chains}, expected A/H/L")

    sc = json.load(open(os.path.join(d, f"{sub}_summary_confidences.json")))
    cp = sc["chain_pair_iptm"]
    i_ah, i_al = cp[0][1], cp[0][2]      # A-H, A-L
    rmsd = crd_rmsd_median(obj)

    dmin = epitope(obj)
    ep = {k for k, v in dmin.items() if v <= CUT}
    ov = ep & TWEAK_SET

    usable = (rmsd <= RMSD_MAX) and (i_ah >= IPTM_MIN) and (i_al >= IPTM_MIN)
    res[tag] = dict(rmsd=rmsd, i_ah=i_ah, i_al=i_al, ep=ep, ov=ov, usable=usable,
                    ranking=sc["ranking_score"], iptm=sc["iptm"], ptm=sc["ptm"])

    for u in sorted(dmin):
        epi_rows.append({"condition": tag, "residue_uniprot": u,
                         "dmin_to_fab_A": round(dmin[u], 2),
                         "in_epitope_5A": int(u in ep),
                         "in_M2_tweak_contact_set": int(u in TWEAK_SET)})

    # spread across all 25 samples, for the distribution column only
    for s in sorted(glob.glob(os.path.join(d, "seed-*_sample-*", "summary_confidences.json"))):
        j = json.load(open(s))
        c = j["chain_pair_iptm"]
        per_sample.append({"condition": tag, "model": os.path.basename(os.path.dirname(s)),
                           "ranking_score": j["ranking_score"], "iptm": j["iptm"],
                           "chain_pair_iptm_A_H": c[0][1], "chain_pair_iptm_A_L": c[0][2]})

    summary.append({
        "condition": tag, "ranking_score": sc["ranking_score"], "iptm": sc["iptm"],
        "ptm": sc["ptm"], "chain_pair_iptm_A_H": i_ah, "chain_pair_iptm_A_L": i_al,
        "crd_rmsd_median_2kmz": round(rmsd, 3),
        "model_usable_per_prereg": "yes" if usable else "NO -> INCONCLUSIVE",
        "n_epitope_res_5A": len(ep),
        "epitope_residues_uniprot": ",".join(str(x) for x in sorted(ep)),
        "n_overlap_with_tweak_set": len(ov),
        "overlap_residues": ",".join(str(x) for x in sorted(ov)),
        "jaccard_with_tweak_set": round(jaccard(ep, TWEAK_SET), 3),
    })

os.makedirs(TAB, exist_ok=True)
for name, rows in (("M3_summary", summary), ("M3_epitope", epi_rows), ("M3_per_sample", per_sample)):
    with open(os.path.join(TAB, f"{name}.tsv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

# ---- verdict, strictly by the frozen rules ---------------------------------------------------
p, q = res["f2_hup4a8"], res["f1_pdl192"]
print("\n=== criterion 1: model usable ===")
for tag, r in res.items():
    print(f"  {tag}: CRD RMSD {r['rmsd']:.3f} A (<= {RMSD_MAX}: {r['rmsd'] <= RMSD_MAX}), "
          f"chain_pair_iptm A-H {r['i_ah']} / A-L {r['i_al']} (>= {IPTM_MIN}: "
          f"{r['i_ah'] >= IPTM_MIN and r['i_al'] >= IPTM_MIN})  -> "
          f"{'usable' if r['usable'] else 'INCONCLUSIVE'}")

print("\n=== criterion 2: overlap with the frozen TWEAK contact set ===")
for tag, r in res.items():
    print(f"  {tag}: epitope {len(r['ep'])} res, overlap {len(r['ov'])} "
          f"({sorted(r['ov'])}), Jaccard {jaccard(r['ep'], TWEAK_SET):.3f}")

if not (p["usable"] and q["usable"]):
    bad = [t for t, r in res.items() if not r["usable"]]
    verdict = ("TEST NOT DECIDABLE: " + ", ".join(bad) + " failed criterion 1, so criterion 2 "
               "cannot be applied to it. Neither support nor contradiction for H.")
elif len(p["ov"]) >= SUPPORT_RATIO * len(q["ov"]) and \
        len(p["ov"]) >= SUPPORT_P4A8_MIN and len(q["ov"]) <= SUPPORT_PDL_MAX:
    verdict = "SUPPORTS H"
elif len(q["ov"]) >= len(p["ov"]):
    verdict = "CONTRADICTS H"
else:
    verdict = "NEITHER SUPPORTS NOR CONTRADICTS H"
print(f"\n=== verdict ===\n  {verdict}")

print("\n=== criterion 3: report-only residue checks ===")
d_pdl, d_p4a8 = epitope("m3_f1_pdl192"), epitope("m3_f2_hup4a8")
print(f"  R56 in PDL192 epitope: {56 in q['ep']} (dmin {d_pdl[56]:.2f} A)")
print(f"  W42 in P4A8 epitope:   {42 in p['ep']} (dmin {d_p4a8[42]:.2f} A)")

hit_h = [r for r in TABLE2_HEAVY_SUBSET if r in p["ep"]]
hit_f = [r for r in TABLE2_FULL if r in p["ep"]]
print(f"  pre-registered heavy-chain-CDR subset {TABLE2_HEAVY_SUBSET}: "
      f"{hit_h} ({len(hit_h)}/{len(TABLE2_HEAVY_SUBSET)})")
print(f"  full patent epitope set {TABLE2_FULL}: {hit_f} ({len(hit_f)}/{len(TABLE2_FULL)})")
for r in TABLE2_FULL:
    print(f"      {r:3d}  {d_p4a8[r]:6.2f} A  {'<=5A' if d_p4a8[r] <= CUT else ''}")


def chain_split(obj, uniprot_res):
    """Min heavy-atom distance from one Fn14 residue to VH and to VL separately, plus the Fab
    residues within CUT. The pooled per-residue distance cannot tell VH from VL."""
    x, r = heavy(obj, FN)
    xr = x[r == uniprot_res - OFF]
    out = {}
    for c in FAB:
        y, ry = heavy(obj, c)
        dm = np.sqrt(((xr[:, None, :] - y[None, :, :]) ** 2).sum(-1))
        near = sorted({int(ry[k]) for k in range(len(ry)) if dm[:, k].min() <= CUT})
        out[c] = (float(dm.min()), near)
    return out


sp = chain_split("m3_f2_hup4a8", 42)
print(f"  W42 split: VH {sp['H'][0]:.2f} A (VH res within {CUT} A: {sp['H'][1]}); "
      f"VL {sp['L'][0]:.2f} A (VL res within {CUT} A: {sp['L'][1]})")
l1 = [r for r in PATENT_CDR_L1 if r in sp["L"][1]]
print(f"  patent CDR-L1 residues {PATENT_CDR_L1} contacting W42 in the model: {l1} "
      f"({len(l1)}/{len(PATENT_CDR_L1)})")
print(f"\ntables written to {TAB}")
