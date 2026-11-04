"""Evaluate AF3 M1b (Fn14 ECD 28-80) against PDB 2KMZ, per docs/M1b_preregistration.md.

Run with the open-source PyMOL venv:
    $BIOWORKSPACE_ROOT/SOFTWARES/tools/pymol-open-source/.venv/bin/python evaluate_M1b.py <af3_frozen_dir>
<af3_frozen_dir> holds fn14_ecd_28_80_tmpl{A,B,C}/ copied from the O2 lab dir.
Writes ../../tables/M1b_per_sample.tsv, ../../tables/M1b_summary.tsv, ../../tables/M1b_templates.tsv.

AF3 numbers the 53-residue construct 1-53; 2KMZ file numbering is also 1-53 (= UniProt 28-80),
so residues are compared directly; CRD 36-67 = construct 9-40. Criteria are fixed in the
pre-registration and are NOT tuned here.
"""
import csv
import glob
import json
import os
import sys

import numpy as np
from pymol import cmd

SRC = sys.argv[1]
STRUCT = os.environ.get(
    "FN14_STRUCT_DIR",
    "/Volumes/Stelligen_SSD/Stelligen/DATA/HotData/TWEAKR-oncoFetal/external/structures_fn14")
TAB = os.path.join(os.getcwd(), "..", "..", "tables")
os.makedirs(TAB, exist_ok=True)
CRD = "9-40"
SS = [(9, 22), (25, 40), (28, 37)]  # construct numbering = UniProt 36-49, 52-67, 55-64
CRIT_MIN, CRIT_MED, CRIT_SS = 2.0, 2.6, 2.5
SEQ = "EQAPGTAPCSRGSSWSADLDKCMDCASCRARPHSDFCLGCAAAPPAPFRLLWP"
EXCLUDE = {"2kmz", "2kn0", "2eqp"}  # amendment 1: 2EQP = human Fn14 TNFR domain (NMR, 2008)
DECIDING = "C"  # amendment 1: C (cutoff 2007-12-31) replaces B

cmd.load(os.path.join(STRUCT, "2kmz.pdb"), "nmr")
cmd.remove("hydro")
nstates = cmd.count_states("nmr")
assert nstates == 20


def seq_of(obj):
    three = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
             "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
             "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}
    return "".join(three[a.resn] for a in cmd.get_model(f"{obj} and name CA").atom)


assert seq_of("nmr") == SEQ


def rmsd_to_nmr(obj, sel):
    out = []
    for st in range(1, nstates + 1):
        out.append(cmd.rms(f"{obj} and name CA and resi {sel}",
                           f"nmr and name CA and resi {sel}", mobile_state=1, target_state=st,
                           cycles=0, matchmaker=-1))
    return np.array(out)


def ss_dist(obj):
    return [cmd.get_distance(f"{obj} and resi {a} and name SG", f"{obj} and resi {b} and name SG")
            for a, b in SS]


rows, tmpl_rows, summary = [], [], []
for cond in ("A", "B", "C"):
    name = f"fn14_ecd_28_80_tmpl{cond}"
    base = os.path.join(SRC, name)
    # ---- template audit from the stage-1 data json
    dj = json.load(open(glob.glob(os.path.join(base, "**", f"{name.lower()}_data.json"), recursive=True)[0]))  # AF3 lower-cases names
    tids = []
    for s in dj["sequences"]:
        for t in (s.get("protein", {}).get("templates") or []):
            mm = t.get("mmcif", "")
            pid = mm.split("\n", 1)[0].replace("data_", "").strip().lower()[:4]
            tids.append(pid)
    for pid in tids:
        tmpl_rows.append({"condition": cond, "template_pdb": pid})
    leaked = sorted(set(tids) & EXCLUDE)
    # ---- ranking scores
    rk = {}
    rk_path = glob.glob(os.path.join(base, "**", "ranking_scores.csv"), recursive=True)
    if rk_path:
        for r in csv.DictReader(open(rk_path[0])):
            rk[(int(r["seed"]), int(r["sample"]))] = float(r["ranking_score"])
    cifs = sorted(glob.glob(os.path.join(base, "**", "seed-*_sample-*", "*model.cif"), recursive=True))
    assert len(cifs) == 25, (cond, len(cifs))
    for c in cifs:
        d = os.path.basename(os.path.dirname(c))  # seed-1_sample-0
        seed, sample = int(d.split("_")[0].split("-")[1]), int(d.split("_")[1].split("-")[1])
        obj = f"{cond}_{seed}_{sample}"
        cmd.load(c, obj)
        assert seq_of(obj) == SEQ
        r_crd = rmsd_to_nmr(obj, CRD)
        r_ecd = rmsd_to_nmr(obj, "1-53")
        ssd = ss_dist(obj)
        plddt = np.mean([a.b for a in cmd.get_model(f"{obj} and name CA and resi {CRD}").atom])
        ok = (r_crd.min() <= CRIT_MIN) and (np.median(r_crd) <= CRIT_MED) and all(x <= CRIT_SS for x in ssd)
        rows.append({"condition": cond, "seed": seed, "sample": sample,
                     "ranking_score": rk.get((seed, sample), float("nan")),
                     "crd_rmsd_min": round(r_crd.min(), 3), "crd_rmsd_median": round(float(np.median(r_crd)), 3),
                     "crd_rmsd_model1": round(r_crd[0], 3),
                     "ecd_rmsd_min": round(r_ecd.min(), 3), "ecd_rmsd_median": round(float(np.median(r_ecd)), 3),
                     "ss_36_49": round(ssd[0], 2), "ss_52_67": round(ssd[1], 2), "ss_55_64": round(ssd[2], 2),
                     "crd_mean_plddt": round(plddt, 1), "meets_criteria": ok})
        cmd.delete(obj)
    cr = [r for r in rows if r["condition"] == cond]
    top = max(cr, key=lambda r: r["ranking_score"])
    verdict = ("BLOCKED (excluded template present: %s)" % ",".join(leaked)) if (cond == DECIDING and leaked) \
        else ("PASS" if top["meets_criteria"] else "FAIL")
    summary.append({"condition": cond, "n_samples": len(cr), "n_templates": len(tids),
                    "excluded_templates_present": ",".join(leaked) or "none",
                    "top_seed_sample": f'{top["seed"]}/{top["sample"]}', "top_ranking_score": top["ranking_score"],
                    "top_crd_rmsd_min": top["crd_rmsd_min"], "top_crd_rmsd_median": top["crd_rmsd_median"],
                    "top_ss_ok": all(top[k] <= CRIT_SS for k in ("ss_36_49", "ss_52_67", "ss_55_64")),
                    "frac_samples_meeting": f'{sum(r["meets_criteria"] for r in cr)}/{len(cr)}',
                    "verdict": verdict if cond == DECIDING else f"control ({verdict} on same criteria)"})


def write(path, recs):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(recs)


write(os.path.join(TAB, "M1b_per_sample.tsv"), rows)
write(os.path.join(TAB, "M1b_summary.tsv"), summary)
write(os.path.join(TAB, "M1b_templates.tsv"), tmpl_rows or [{"condition": "-", "template_pdb": "none"}])
for s in summary:
    print(s)
