"""POST-HOC (not preregistered) TWEAK-side check of the M2 models; does not change the M2 verdict.

    .../pymol-open-source/.venv/bin/python posthoc_tweak_sites.py <frozen_dir>     (run from code/af3_M2/)

Dhruv et al. 2013 (REF-035, PMID 24056367): TWEAK Y176A abolishes Fn14 binding; W231 mutation does not.
Reports the min heavy-atom distance from TWEAK Y176 / W231 (UniProt; construct = UniProt - 93) of each
TWEAK chain to any Fn14 atom, for all 25 samples of both conditions. Writes ../../tables/M2_posthoc_tweak_sites.tsv.
"""
import csv, glob, os, sys
import numpy as np
from pymol import cmd

from m2_checks import min_distance

SRC = sys.argv[1]
OUT = os.path.join(os.getcwd(), "..", "..", "tables", "M2_posthoc_tweak_sites.tsv")
SITES = {176: ("TYR", "Y176"), 231: ("TRP", "W231")}
rows = []
for cond in "cd":
    dirs = sorted(d for d in glob.glob(os.path.join(SRC, f"m2_tweak3_fn14x3_tmpl{cond}", "seed-*_sample-*")) if os.path.isdir(d))
    assert len(dirs) == 25
    for d in dirs:
        cmd.load(os.path.join(d, "model.cif"), "m")
        fn = np.array(cmd.get_coords("m and chain D+E+F and not hydro"))
        for uni, (rn, lab) in SITES.items():
            for t in "ABC":
                sel = f"m and chain {t} and resi {uni - 93} and not hydro"
                assert cmd.count_atoms(f"{sel} and name CA and resn {rn}") == 1
                x = np.array(cmd.get_coords(sel))
                dmin = min_distance(x, fn)
                rows.append({"condition": cond, "sample": os.path.basename(d), "tweak_site": lab,
                             "tweak_chain_observation": t, "dmin_to_fn14_A": round(dmin, 2)})
        cmd.delete("m")
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t"); w.writeheader(); w.writerows(rows)
for cond in "cd":
    for s in ("Y176", "W231"):
        v = [r["dmin_to_fn14_A"] for r in rows if r["condition"] == cond and r["tweak_site"] == s]
        print(cond, s, f"TWEAK-chain observations n={len(v)} (25 models x 3 chains; not independent experiments) "
                       f"min={min(v)} median={np.median(v):.2f} max={max(v)} <=5A: {sum(x <= 5 for x in v)}/{len(v)}")
