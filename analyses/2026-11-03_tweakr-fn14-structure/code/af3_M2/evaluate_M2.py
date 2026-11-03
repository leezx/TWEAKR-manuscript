"""Evaluate AF3 M2 (TWEAK3 + Fn14x3 ECD) per docs/M2_preregistration.md. Criteria are NOT tuned here.

    $BIOWORKSPACE_ROOT/SOFTWARES/tools/pymol-open-source/.venv/bin/python evaluate_M2.py <frozen_dir>
<frozen_dir> holds m2_tweak3_fn14x3_tmpl{c,d}/. Run from code/af3_M2/.
Writes ../../tables/M2_{summary,per_sample,interface,templates}.tsv.

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
EXCLUDE_FN14 = {"2kmz", "2kn0", "2eqp"}

cmd.load(os.path.join(STRUCT, "2kmz.pdb"), "nmr")
cmd.remove("hydro")
assert cmd.count_states("nmr") == 20


def heavy(obj, chain):
    m = cmd.get_model(f"{obj} and chain {chain} and not hydro")
    xyz = np.array([a.coord for a in m.atom])
    res = np.array([int(a.resi) for a in m.atom])
    return xyz, res, m


def min_dist_per_residue(obj, ch, partners):
    """min heavy-atom distance from each residue of chain ch to any atom of the partner chains."""
    x, r, _ = heavy(obj, ch)
    px = np.vstack([heavy(obj, p)[0] for p in partners])
    out = {}
    for rr in np.unique(r):
        d = np.sqrt(((x[r == rr][:, None, :] - px[None, :, :]) ** 2).sum(-1)).min()
        out[int(rr)] = float(d)
    return out


def crd_rmsd_median(obj, ch):
    v = []
    for st in range(1, 21):
        v.append(cmd.rms(f"{obj} and chain {ch} and name CA and resi {CRD}",
                         f"nmr and name CA and resi {CRD}", mobile_state=1, target_state=st, cycles=0))
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
            pid = t.get("mmcif", "").split("\n", 1)[0].replace("data_", "").strip().lower()[:4]
            tids.append(pid)
            tmpl_rows.append({"condition": cond, "chain_ids": ",".join(p["id"]) if isinstance(p["id"], list) else p["id"],
                              "template_pdb": pid})
    leaked = sorted(set(tids) & EXCLUDE_FN14)
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
            iface_rows.append({"condition": cond, "seed": seed, "sample": sample, "fn14_chain": ch,
                               "best_chain_iptm_to_tweak": round(best_ip, 3), "n_contact_res_4p5A": n_contact,
                               "sites_within_5A": ",".join(sites_at),
                               **{f"dmin_{SITES[k][1]}": round(dmin[k], 2) for k in SITES},
                               "crd_rmsd_median_2kmz": round(crd, 3), "tweak_chains_contacted": groove[-1],
                               "interface_residues_uniprot": ",".join(str(r + 27) for r, v in sorted(dmin.items()) if v <= 5.0)})
        c3 = sum(c3_list) >= 2
        ok = c1 and all(c2_list) and c3 and all(c4_list)
        K = round(np.mean(frac_if) * 53)
        per_sample.append({"condition": cond, "seed": seed, "sample": sample, "ranking_score": rk[(seed, sample)],
                           "iptm": sc.get("iptm"), "ptm": sc.get("ptm"),
                           "tweak_pair_iptm_min": round(min(tw_pairs), 3), "c1_trimer": c1,
                           "c2_all_fn14_bound": all(c2_list), "c3_copies_with_>=3_sites": sum(c3_list),
                           "c4_crd_intact": all(c4_list), "meets_all": ok,
                           "mean_interface_fraction": round(float(np.mean(frac_if)), 3),
                           "chance_P(>=3of4)": round(hyper_ge(53, K, 4, 3), 4),
                           "copies_in_groove(2 TWEAK chains)": sum(1 for g in groove if g >= 2)})
        cmd.delete(obj)
    cs = [r for r in per_sample if r["condition"] == cond]
    top = max(cs, key=lambda r: r["ranking_score"])
    if cond == DECIDING and leaked:
        verdict = "BLOCKED (Fn14 template present: %s)" % ",".join(leaked)
    else:
        verdict = "PASS" if top["meets_all"] else "FAIL"
    summary.append({"condition": cond, "templates": ",".join(sorted(set(tids))) or "none",
                    "fn14_templates_present": ",".join(leaked) or "none",
                    "top_seed_sample": f'{top["seed"]}/{top["sample"]}', "top_ranking_score": round(top["ranking_score"], 3),
                    "top_iptm": top["iptm"], "c1": top["c1_trimer"], "c2": top["c2_all_fn14_bound"],
                    "c3_copies": top["c3_copies_with_>=3_sites"], "c4": top["c4_crd_intact"],
                    "top_chance_P": top["chance_P(>=3of4)"], "top_groove_copies": top["copies_in_groove(2 TWEAK chains)"],
                    "frac_samples_meeting_all": f'{sum(r["meets_all"] for r in cs)}/{len(cs)}',
                    "verdict": verdict if cond == DECIDING else f"control ({verdict} on same criteria)"})


def write(path, recs):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(recs)


write(os.path.join(TAB, "M2_summary.tsv"), summary)
write(os.path.join(TAB, "M2_per_sample.tsv"), per_sample)
write(os.path.join(TAB, "M2_interface.tsv"), iface_rows)
write(os.path.join(TAB, "M2_templates.tsv"), tmpl_rows or [{"condition": "-", "chain_ids": "-", "template_pdb": "none"}])
for s in summary:
    print(s)
