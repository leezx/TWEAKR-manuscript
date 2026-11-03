"""Fig. TR2 structure renders for TWEAKR / Fn14 (TNFRSF12A, UniProt Q9NP84).

Run from code/ with open-source PyMOL (headless; the licensed PyMOL.app 2.5.7 on this Mac
has an expired licence and watermarks every ray-traced PNG, so it must NOT be used):
    $BIOWORKSPACE_ROOT/SOFTWARES/tools/pymol-open-source/.venv/bin/python render_fig_TR2_structures.py
    (pymol-open-source-whl 3.2.0.2, numpy<2 pinned; see requirements.lock.txt there)

Inputs  (env FN14_STRUCT_DIR, default = HotData external/structures_fn14):
    AF-Q9NP84-F1-model_v6.pdb   AlphaFold DB full-length model (v6)
    2kmz.pdb                    NMR ensemble of hFn14 ECD (UniProt 28-80, file numbering 1-53)
Outputs (../figures/TR2_parts/):
    af_membrane.png             mature chain 28-129, TM-axis vertical, transparent bg
    nmr_2kmz.png                2KMZ model 1 renumbered to UniProt, same ECD orientation
    projection.json             pixel <-> Angstrom mapping + anchor residue pixel coords
    per_residue.tsv             residue, domain, pLDDT, oriented x/y/z of CA

Coordinates of every domain are the frozen B32 coordinates (README §6).
No stochastic step; output is deterministic given the two input files.
"""
import json
import os
import sys

import numpy as np
from pymol import cmd

HERE = os.environ.get("FN14_CODE_DIR", os.getcwd())  # run from code/; PyMOL rewrites __file__
STRUCT = os.environ.get(
    "FN14_STRUCT_DIR",
    "/Volumes/Stelligen_SSD/Stelligen/DATA/HotData/TWEAKR-oncoFetal/external/structures_fn14",
)
OUT = os.path.join(HERE, "..", "figures", "TR2_parts")
os.makedirs(OUT, exist_ok=True)

# ---- frozen B32 domain map (UniProt Q9NP84) --------------------------------
DOMAINS = [  # name, start, end, hex
    ("Extracellular N-segment", 28, 35, "#A6CEE3"),
    ("CRD (TNFR-Cys, atypical)", 36, 67, "#1F78B4"),
    ("Extracellular stalk", 68, 80, "#7BA7C7"),
    ("Transmembrane helix", 81, 101, "#E6550D"),
    ("Juxtamembrane basic cluster", 102, 109, "#6A51A3"),
    ("Cytoplasmic tail (TRAF region)", 110, 129, "#31A354"),
]
DISULFIDES = [(36, 49), (52, 67), (55, 64)]
BINDING = {45: "ASP", 48: "LYS", 50: "MET", 62: "ASP"}
SS_COL = "#F2C300"
BIND_COL = "#D7301F"
HALF_CORE = 15.0  # Å, half hydrophobic thickness used to draw the bilayer

W, H = 2400, 3200  # render size (px) for the AF panel
W2, H2 = 1600, 1600  # render size for the NMR panel


def hex2rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def domain_of(r):
    for n, s, e, _ in DOMAINS:
        if s <= r <= e:
            return n
    return "Signal peptide (cleaved)"


def ca_coords(obj, sel=""):
    m = cmd.get_model(f"{obj} and name CA {sel}")
    return {int(a.resi): np.array(a.coord) for a in m.atom}, {int(a.resi): a.b for a in m.atom}


def apply_transform(obj, R, t):
    """x' = R (x - t) for every atom of obj (all states)."""
    for st in range(1, cmd.count_states(obj) + 1):
        xyz = cmd.get_coords(obj, state=st)
        cmd.load_coords((xyz - t) @ R.T, obj, state=st)


def style_common():
    cmd.bg_color("white")
    cmd.set("ray_opaque_background", 0)
    cmd.set("orthoscopic", 1)
    cmd.set("field_of_view", 20)
    cmd.set("ray_trace_mode", 1)
    cmd.set("ray_trace_color", "black")
    cmd.set("ray_trace_gain", 0.12)
    cmd.set("antialias", 2)
    cmd.set("ambient", 0.35)
    cmd.set("specular", 0.15)
    cmd.set("cartoon_fancy_helices", 1)
    cmd.set("cartoon_highlight_color", -1)
    cmd.set("cartoon_loop_radius", 0.35)
    cmd.set("cartoon_tube_radius", 0.35)
    cmd.set("stick_radius", 0.28)
    cmd.set("sphere_scale", 0.6)
    cmd.set("depth_cue", 0)
    cmd.set("ray_shadows", 0)
    for n, s, e, hx in DOMAINS:
        cname = "c_" + str(s)
        cmd.set_color(cname, hex2rgb(hx))
    cmd.set_color("c_ss", hex2rgb(SS_COL))
    cmd.set_color("c_bind", hex2rgb(BIND_COL))


def color_domains(obj):
    for n, s, e, _ in DOMAINS:
        cmd.color("c_" + str(s), f"{obj} and resi {s}-{e}")


def show_sites(obj):
    sel_ss = " or ".join(f"resi {a}+{b}" for a, b in DISULFIDES)
    cmd.show("sticks", f"{obj} and ({sel_ss}) and (name CA+CB+SG)")
    cmd.color("c_ss", f"{obj} and ({sel_ss}) and name SG+CB")
    bind = "+".join(str(k) for k in BINDING)
    cmd.show("sticks", f"{obj} and resi {bind} and not name N+C+O")
    cmd.color("c_bind", f"{obj} and resi {bind} and not name N+C+O+CA")
    cmd.set("cartoon_side_chain_helper", 1)


def set_ortho_view(center, half_height, w, h):
    """Identity rotation, looking down -z; orthoscopic visible half-height = half_height."""
    fov = cmd.get_setting_float("field_of_view")
    dist = half_height / np.tan(np.radians(fov / 2.0))
    view = [1, 0, 0, 0, 1, 0, 0, 0, 1,
            0, 0, -dist,
            float(center[0]), float(center[1]), float(center[2]),
            dist - 200, dist + 200, 1]
    cmd.set_view(view)
    return dist


def to_px(xy, center, half_height, w, h):
    s = (h / 2.0) / half_height  # px per Å
    return [w / 2.0 + (xy[0] - center[0]) * s, h / 2.0 - (xy[1] - center[1]) * s]


def ss_mid_px(obj, center, hh, w, h):
    out = {}
    for a, b in DISULFIDES:
        pa = np.array(cmd.get_model(f"{obj} and resi {a} and name SG").atom[0].coord)
        pb = np.array(cmd.get_model(f"{obj} and resi {b} and name SG").atom[0].coord)
        out[f"{a}-{b}"] = to_px((pa + pb) / 2, center, hh, w, h)
    return out


# ============================================================================
# 1. AlphaFold full-length model -> mature chain in membrane frame
# ============================================================================
cmd.load(os.path.join(STRUCT, "AF-Q9NP84-F1-model_v6.pdb"), "af")
seq = "".join(
    {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
     "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
     "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}[a.resn]
    for a in cmd.get_model("af and name CA").atom)
fasta = "".join(l.strip() for l in open(os.path.join(STRUCT, "Q9NP84.fasta")) if not l.startswith(">"))
assert seq == fasta and len(seq) == 129, "AF model sequence != UniProt Q9NP84"
for r, rn in BINDING.items():
    assert cmd.count_atoms(f"af and resi {r} and resn {rn} and name CA") == 1, r
for a, b in DISULFIDES:
    assert cmd.count_atoms(f"af and resi {a}+{b} and resn CYS and name CA") == 2

ca, plddt = ca_coords("af")

# TM axis by PCA of CA 81-101, oriented 101 -> 81 (cytoplasm -> outside) = +y
tm = np.array([ca[r] for r in range(81, 102)])
tm_c = tm.mean(axis=0)
u, s_, vt = np.linalg.svd(tm - tm_c)
ax = vt[0]
if np.dot(ca[81] - ca[101], ax) < 0:
    ax = -ax
# second axis: put CRD centroid in the image plane (its z = 0), on +x side
crd = np.array([ca[r] for r in range(36, 68)]).mean(axis=0) - tm_c
perp = crd - np.dot(crd, ax) * ax
xa = perp / np.linalg.norm(perp)
za = np.cross(xa, ax)
R = np.vstack([xa, ax, za])  # rows = new x, y, z
assert abs(np.linalg.det(R) - 1) < 1e-6
apply_transform("af", R, tm_c)

ca, plddt = ca_coords("af")
rows = []
for r in sorted(ca):
    rows.append((r, seq[r - 1], domain_of(r), plddt[r], *ca[r]))
with open(os.path.join(OUT, "per_residue.tsv"), "w") as f:
    f.write("resi\taa\tdomain\tplddt\tx\ty\tz\n")
    for r in rows:
        f.write("%d\t%s\t%s\t%.2f\t%.2f\t%.2f\t%.2f\n" % r)

# residues outside TM whose CA sits inside the hydrophobic core: a geometry QC
in_core = [r for r in range(28, 130) if not (81 <= r <= 101) and abs(ca[r][1]) < HALF_CORE]
tm_rise = (ca[81][1] - ca[101][1])

cmd.remove("af and resi 1-27")
style_common()
cmd.hide("everything", "af")
cmd.show("cartoon", "af")
color_domains("af")
show_sites("af")

# frame: fit the whole mature chain with margin
xyz = cmd.get_coords("af")
lo, hi = xyz.min(axis=0), xyz.max(axis=0)
center = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0.0])
half_h = max((hi[1] - lo[1]) / 2, (hi[0] - lo[0]) / 2 * H / W) + 6.0
set_ortho_view(center, half_h, W, H)
cmd.png(os.path.join(OUT, "af_membrane.png"), width=W, height=H, dpi=600, ray=1)

anchors = {str(r): to_px(ca[r], center, half_h, W, H) for r in
           [28, 36, 45, 48, 50, 62, 67, 80, 81, 101, 102, 109, 110, 129]}
proj_af = {"width": W, "height": H, "center": center.tolist(), "half_height_A": half_h,
           "px_per_A": (H / 2) / half_h,
           "membrane_y_px": {"outer": to_px([0, HALF_CORE], center, half_h, W, H)[1],
                             "inner": to_px([0, -HALF_CORE], center, half_h, W, H)[1],
                             "mid": to_px([0, 0], center, half_h, W, H)[1]},
           "anchors_px": anchors,
           "disulfide_mid_px": ss_mid_px("af", center, half_h, W, H),
           "tm_rise_A_81_to_101": tm_rise,
           "nonTM_CA_in_core": in_core}

# ============================================================================
# 2. 2KMZ NMR (model 1), renumbered to UniProt, superposed on AF ECD
# ============================================================================
cmd.load(os.path.join(STRUCT, "2kmz.pdb"), "nmr", state=1)
cmd.alter("nmr", "resi = str(int(resi) + 27)")
cmd.sort("nmr")
nmr_seq = "".join(a.resn for a in cmd.get_model("nmr and name CA").atom)
assert cmd.count_atoms("nmr and name CA") == 53
for r, rn in BINDING.items():
    assert cmd.count_atoms(f"nmr and resi {r} and resn {rn} and name CA") == 1, r
cmd.remove("hydro")
rms_crd = cmd.pair_fit("nmr and name CA and resi 36-67", "af and name CA and resi 36-67")
# all-CA (28-80) RMSD in the CRD-superposed frame, no further fitting
rms_ecd_nofit = cmd.rms_cur("nmr and name CA and resi 28-80", "af and name CA and resi 28-80")
cmd.disable("af")
cmd.hide("everything", "nmr")
cmd.show("cartoon", "nmr")
color_domains("nmr")
show_sites("nmr")
xyz = cmd.get_coords("nmr")
lo, hi = xyz.min(axis=0), xyz.max(axis=0)
c2 = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0.0])
hh2 = max(hi[1] - lo[1], hi[0] - lo[0]) / 2 + 4.0
set_ortho_view(c2, hh2, W2, H2)
cmd.png(os.path.join(OUT, "nmr_2kmz.png"), width=W2, height=H2, dpi=600, ray=1)
nca, _ = ca_coords("nmr")
proj_nmr = {"width": W2, "height": H2, "center": c2.tolist(), "half_height_A": hh2,
            "anchors_px": {str(r): to_px(nca[r], c2, hh2, W2, H2) for r in
                           [28, 36, 45, 48, 50, 62, 67, 80]},
            "sidechain_tip_px": {},
            "disulfide_mid_px": ss_mid_px("nmr", c2, hh2, W2, H2)}
for r, atom in [(45, "CG"), (48, "NZ"), (50, "SD"), (62, "CG")]:
    m = cmd.get_model(f"nmr and resi {r} and name {atom}").atom[0]
    proj_nmr["sidechain_tip_px"][str(r)] = to_px(np.array(m.coord), c2, hh2, W2, H2)

summary = {
    "af_model": "AF-Q9NP84-F1-model_v6",
    "nmr": "2KMZ model 1 of 20 (file resi + 27 = UniProt)",
    "rmsd_CA_CRD36_67_AF_vs_2KMZ_model1": rms_crd,
    "rmsd_CA_ECD28_80_after_CRD_fit": rms_ecd_nofit,
    "mean_plddt_by_domain": {
        n: float(np.mean([plddt[r] for r in range(s, e + 1)])) for n, s, e, _ in DOMAINS},
    "af": proj_af,
    "nmr2kmz": proj_nmr,
}
with open(os.path.join(OUT, "projection.json"), "w") as f:
    json.dump(summary, f, indent=1)
print(json.dumps({k: summary[k] for k in summary if k not in ("af", "nmr2kmz")}, indent=1))
print("TM rise 81->101 (A):", round(tm_rise, 2), " nonTM CA inside |y|<15:", in_core)
