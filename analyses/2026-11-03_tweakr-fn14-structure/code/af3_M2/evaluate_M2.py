"""Evaluate AF3 M2 (TWEAK3 + Fn14x3 ECD) per docs/M2_preregistration.md. Criteria are NOT tuned here.

    $BIOWORKSPACE_ROOT/SOFTWARES/tools/pymol-open-source/.venv/bin/python evaluate_M2.py <frozen_dir>
<frozen_dir> holds m2_tweak3_fn14x3_tmpl{c,d}/. Run from code/af3_M2/.
Writes ../../tables/M2_{summary,per_sample,interface,templates,c_vs_d}.tsv.

Chains: A,B,C = TWEAK 94-249 (construct 1-156; UniProt = construct + 93);
        D,E,F = Fn14 28-80 (construct 1-53; UniProt = construct + 27).
"""
import csv
import glob
import itertools
import json
import math
import os
import sys

import numpy as np
from pymol import cmd

from m2_checks import (EvalError, check_pairing, classify_templates, kabsch_rmsd, min_distance,
                       template_id)

SRC = sys.argv[1]
STRUCT = os.environ.get(
    "FN14_STRUCT_DIR",
    "/Volumes/Stelligen_SSD/Stelligen/DATA/HotData/TWEAKR-oncoFetal/external/structures_fn14")
TAB = os.path.join(os.getcwd(), "..", "..", "tables")
os.makedirs(TAB, exist_ok=True)
TW, FN = ["A", "B", "C"], ["D", "E", "F"]
SITES = {18: ("ASP", "D45"), 21: ("LYS", "K48"), 23: ("MET", "M50"), 35: ("ASP", "D62")}  # construct: (resn, UniProt)
CRD = "9-40"
DECIDING = "c"
# Template exclusion lists (Fn14, TWEAK, TWEAK–Fn14 complex) live in m2_checks.py.

cmd.load(os.path.join(STRUCT, "2kmz.pdb"), "nmr")
cmd.remove("hydro")
assert cmd.count_states("nmr") == 20


def heavy(obj, chain):
    m = cmd.get_model(f"{obj} and chain {chain} and not hydro")
    if not m.atom:
        raise EvalError(f"no atoms in {obj} chain {chain}")
    xyz = np.array([a.coord for a in m.atom])
    res = np.array([int(a.resi) for a in m.atom])
    return xyz, res, m


def min_dist_per_residue(obj, ch, partners):
    """min heavy-atom distance from each residue of chain ch to any atom of the partner chains."""
    x, r, _ = heavy(obj, ch)
    px = np.vstack([heavy(obj, p)[0] for p in partners])
    out = {}
    for rr in np.unique(r):
        out[int(rr)] = min_distance(x[r == rr], px)
    return out


def _ca(sel, state):
    m = cmd.get_model(f"{sel} and name CA and resi {CRD}", state=state)
    return [(int(a.resi), a.resn) for a in m.atom], np.array([a.coord for a in m.atom])


def crd_rmsd_median(obj, ch):
    """Cα RMSD (Kabsch, no outlier rejection) of CRD vs each of the 20 2KMZ models; median.
    Fix 2026-11-03: cmd.rms pairs atoms by identifier incl. chain, so chains D/E/F matched nothing in
    2KMZ chain A and returned 0.0 ("No atoms selected"). Same criterion, explicit residue pairing."""
    ids_m, xm = _ca(f"{obj} and chain {ch}", 1)
    v = []
    for st in range(1, 21):
        ids_t, xt = _ca("nmr", st)
        check_pairing(ids_m, ids_t, 32)   # fail closed: 32 Cα, same residue numbers and names
        v.append(kabsch_rmsd(xm, xt))
    return float(np.median(v))


def hyper_ge(N, K, n, k):
    """P(X >= k), X ~ Hypergeometric(N population, K successes, n draws)."""
    return sum(math.comb(K, i) * math.comb(N - K, n - i) for i in range(k, min(K, n) + 1)) / math.comb(N, n)


summary, per_sample, iface_rows, tmpl_rows = [], [], [], []
for cond in ("c", "d"):
    name = f"m2_tweak3_fn14x3_tmpl{cond}"
    base = os.path.join(SRC, name)
    dj = json.load(open(glob.glob(os.path.join(base, "**", f"{name}_data.json"), recursive=True)[0]))
    tids = []
    for s in dj["sequences"]:
        p = s.get("protein", {})
        for t in (p.get("templates") or []):
            pid = template_id(t.get("mmcif", ""))
            tids.append(pid)
            tmpl_rows.append({"condition": cond, "chain_ids": ",".join(p["id"]) if isinstance(p["id"], list) else p["id"],
                              "template_pdb": pid})
    cls = classify_templates(tids)
    # BLOCKED if any Fn14, TWEAK or TWEAK–Fn14 complex template was used (stricter than the
    # preregistered "Fn14 or complex"; added after review round 1, does not change either verdict)
    leaked = cls["fn14"] + cls["tweak"] + cls["complex"]
    rk = {}
    for r in csv.DictReader(open(glob.glob(os.path.join(base, "**", "ranking_scores.csv"), recursive=True)[0])):
        rk[(int(r["seed"]), int(r["sample"]))] = float(r["ranking_score"])
    dirs = sorted(glob.glob(os.path.join(base, "**", "seed-*_sample-*"), recursive=True))
    dirs = [d for d in dirs if os.path.isdir(d)]
    assert len(dirs) == 25, (cond, len(dirs))
    for d in dirs:
        tag = os.path.basename(d)
        seed, sample = int(tag.split("_")[0].split("-")[1]), int(tag.split("_")[1].split("-")[1])
        sc = json.load(open(os.path.join(d, "summary_confidences.json")))
        cpi = np.array(sc["chain_pair_iptm"])  # order follows chain ids A..F
        obj = f"{cond}_{seed}_{sample}"
        cmd.load(os.path.join(d, "model.cif"), obj)
        for k, (rn, _) in SITES.items():
            for ch in FN:
                assert cmd.count_atoms(f"{obj} and chain {ch} and resi {k} and resn {rn} and name CA") == 1
        idx = {c: i for i, c in enumerate(TW + FN)}
        tw_pairs = [(cpi[idx[a], idx[b]] + cpi[idx[b], idx[a]]) / 2 for a, b in itertools.combinations(TW, 2)]
        c1 = all(v >= 0.70 for v in tw_pairs)
        c2_list, c3_list, c4_list, groove, frac_if = [], [], [], [], []
        for ch in FN:
            dmin = min_dist_per_residue(obj, ch, TW)
            n_contact = sum(1 for v in dmin.values() if v <= 4.5)
            best_ip = max(cpi[idx[ch], idx[t]] for t in TW)
            c2_list.append(best_ip >= 0.50 and n_contact >= 5)
            sites_at = [SITES[k][1] for k in SITES if dmin[k] <= 5.0]
            c3_list.append(len(sites_at) >= 3)
            crd = crd_rmsd_median(obj, ch)
            c4_list.append(crd <= 2.6)
            per_tw = [sum(1 for v in min_dist_per_residue(obj, ch, [t]).values() if v <= 4.5) for t in TW]
            groove.append(sum(1 for v in per_tw if v >= 3))
            frac_if.append(sum(1 for v in dmin.values() if v <= 5.0) / len(dmin))
            tw_side = []
            for t in TW:
                dt = min_dist_per_residue(obj, t, [ch])
                hits = [str(r + 93) for r, v in sorted(dt.items()) if v <= 5.0]
                if hits:
                    tw_side.append(f"{t}:" + ",".join(hits))
            iface_rows.append({"condition": cond, "seed": seed, "sample": sample, "fn14_chain": ch,
                               "best_chain_iptm_to_tweak": round(best_ip, 3), "n_contact_res_4p5A": n_contact,
                               "sites_within_5A": ",".join(sites_at),
                               **{f"dmin_{SITES[k][1]}": round(dmin[k], 2) for k in SITES},
                               "crd_rmsd_median_2kmz": round(crd, 3), "tweak_chains_contacted": groove[-1],
                               "interface_residues_uniprot": ",".join(str(r + 27) for r, v in sorted(dmin.items()) if v <= 5.0),
                               "tweak_interface_uniprot": ";".join(tw_side)})
        c3 = sum(c3_list) >= 2
        ok = c1 and all(c2_list) and c3 and all(c4_list)
        K = round(np.mean(frac_if) * 53)
        per_sample.append({"condition": cond, "seed": seed, "sample": sample, "ranking_score": rk[(seed, sample)],
                           "iptm": sc.get("iptm"), "ptm": sc.get("ptm"),
                           "tweak_pair_iptm_min": round(min(tw_pairs), 3), "c1_trimer": c1,
                           "c2_all_fn14_bound": all(c2_list), "c3_copies_with_>=3_sites": sum(c3_list),
                           "c4_crd_intact": all(c4_list), "meets_all": ok,
                           "mean_interface_fraction": round(float(np.mean(frac_if)), 3),
                           "geometric_reference_fraction_ge3of4": round(hyper_ge(53, K, 4, 3), 4),  # descriptive, NOT a P value
                           "copies_in_groove(2 TWEAK chains)": sum(1 for g in groove if g >= 2)})
        if (seed, sample) == max(rk, key=rk.get):
            cmd.create(f"top_{cond}", obj)
        cmd.delete(obj)
    cs = [r for r in per_sample if r["condition"] == cond]
    top = max(cs, key=lambda r: r["ranking_score"])
    if cond == DECIDING and leaked:
        verdict = "BLOCKED (Fn14/TWEAK/complex template present: %s)" % ",".join(leaked)
    else:
        verdict = "PASS" if top["meets_all"] else "FAIL"
    summary.append({"condition": cond, "templates": ",".join(sorted(set(tids))) or "none",
                    "fn14_templates_present": ",".join(cls["fn14"]) or "none",
                    "tweak_templates_present": ",".join(cls["tweak"]) or "none",
                    "complex_templates_present": ",".join(cls["complex"]) or "none",
                    "top_seed_sample": f'{top["seed"]}/{top["sample"]}', "top_ranking_score": round(top["ranking_score"], 3),
                    "top_iptm": top["iptm"], "c1": top["c1_trimer"], "c2": top["c2_all_fn14_bound"],
                    "c3_copies": top["c3_copies_with_>=3_sites"], "c4": top["c4_crd_intact"],
                    "top_geometric_reference_fraction": top["geometric_reference_fraction_ge3of4"], "top_groove_copies": top["copies_in_groove(2 TWEAK chains)"],
                    "frac_samples_meeting_all": f'{sum(r["meets_all"] for r in cs)}/{len(cs)}',
                    "verdict": verdict if cond == DECIDING else f"control ({verdict} on same criteria)"})


# M2-C vs M2-D top models: Cα RMSD over the whole complex and over each chain (report only)
def _all_ca(o, ch):
    m = cmd.get_model(f"{o} and chain {ch} and name CA")
    return [(int(a.resi), a.resn) for a in m.atom], np.array([a.coord for a in m.atom])


cd_rows = []
xc_all, xd_all = [], []
for ch in TW + FN:
    ic, xc = _all_ca("top_c", ch)
    idd, xd = _all_ca("top_d", ch)
    if len(ic) == 0:
        raise EvalError(f"no CA atoms for chain {ch}")
    check_pairing(ic, idd, len(ic))
    xc_all.append(xc); xd_all.append(xd)
    cd_rows.append({"chain": ch, "n_ca": len(xc), "rmsd_top_c_vs_top_d": round(kabsch_rmsd(xc, xd), 3)})
cd_rows.append({"chain": "complex", "n_ca": sum(len(x) for x in xc_all),
                "rmsd_top_c_vs_top_d": round(kabsch_rmsd(np.vstack(xc_all), np.vstack(xd_all)), 3)})


def write(path, recs):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(recs)


write(os.path.join(TAB, "M2_summary.tsv"), summary)
write(os.path.join(TAB, "M2_per_sample.tsv"), per_sample)
write(os.path.join(TAB, "M2_interface.tsv"), iface_rows)
write(os.path.join(TAB, "M2_c_vs_d.tsv"), cd_rows)
write(os.path.join(TAB, "M2_templates.tsv"), tmpl_rows or [{"condition": "-", "chain_ids": "-", "template_pdb": "none"}])
for s in summary:
    print(s)
