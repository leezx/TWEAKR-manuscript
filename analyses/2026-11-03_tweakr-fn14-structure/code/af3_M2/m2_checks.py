"""Fail-closed helpers for evaluate_M2.py (no PyMOL dependency, so they can be unit-tested).

Added 2026-11-03 after GPT review round 1 (P1-3): the first evaluator run silently turned an empty
atom selection into a 0.0 Å RMSD. Every helper here raises instead of returning a number when its
input is empty, unpaired or malformed. Tested by test_m2_checks.py.
"""
import numpy as np

# All PDB entries that contain Fn14 or TWEAK (RCSB, by UniProt accession, checked 2026-11-03).
# No experimental TWEAK–Fn14 complex exists; COMPLEX_PDB is kept so a future entry is caught.
FN14_PDB = {"2kmz", "2kn0", "2eqp", "2rpj"}   # Q9NP84 (2EQP, 2KMZ, 2RPJ) + Xenopus Fn14 (2KN0)
TWEAK_PDB = {"4ht1"}                           # O43508 (TWEAK–Fab)
COMPLEX_PDB = set()                            # TWEAK–Fn14; none deposited


class EvalError(ValueError):
    """Raised when an evaluation input cannot support a number; never converted to PASS."""


def kabsch_rmsd(P, Q):
    """Cα RMSD after optimal superposition. Raises on empty, unequal or non-finite input."""
    P, Q = np.asarray(P, float), np.asarray(Q, float)
    if P.ndim != 2 or P.shape[1] != 3 or P.shape != Q.shape:
        raise EvalError(f"coordinate arrays not paired: {P.shape} vs {Q.shape}")
    if len(P) < 3:
        raise EvalError(f"need >= 3 paired atoms, got {len(P)}")
    if not (np.isfinite(P).all() and np.isfinite(Q).all()):
        raise EvalError("non-finite coordinates")
    P, Q = P - P.mean(0), Q - Q.mean(0)
    U, S, Vt = np.linalg.svd(P.T @ Q)
    S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((P ** 2).sum() + (Q ** 2).sum() - 2 * S.sum(), 0.0) / len(P)))


def check_pairing(ids_mobile, ids_target, expected_n):
    """Residue (number, name) lists must match one-to-one and have the expected length."""
    if len(ids_mobile) != expected_n or len(ids_target) != expected_n:
        raise EvalError(f"expected {expected_n} atoms, got {len(ids_mobile)} / {len(ids_target)}")
    if list(ids_mobile) != list(ids_target):
        bad = [(a, b) for a, b in zip(ids_mobile, ids_target) if a != b][:3]
        raise EvalError(f"residue identities differ, e.g. {bad}")


def min_distance(X, Y):
    """Minimum Euclidean distance between two non-empty point sets."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    if X.size == 0 or Y.size == 0:
        raise EvalError("empty atom set in distance calculation")
    return float(np.sqrt(((X[:, None, :] - Y[None, :, :]) ** 2).sum(-1)).min())


def template_id(mmcif_text):
    """4-character PDB id from a template mmCIF 'data_XXXX' header; raises if it cannot be parsed."""
    head = (mmcif_text or "").split("\n", 1)[0].strip()
    if not head.startswith("data_"):
        raise EvalError(f"template mmCIF has no data_ header: {head[:30]!r}")
    pid = head[5:].strip().lower()[:4]
    if len(pid) != 4 or not pid.isalnum():
        raise EvalError(f"cannot parse template id from {head[:30]!r}")
    return pid


def classify_templates(tids):
    """Which used templates are Fn14, TWEAK or a TWEAK–Fn14 complex."""
    s = {t.lower() for t in tids}
    return {"fn14": sorted(s & FN14_PDB), "tweak": sorted(s & TWEAK_PDB), "complex": sorted(s & COMPLEX_PDB)}
