"""Unit tests for m2_checks.py.  Run from code/af3_M2/:  python test_m2_checks.py   (or pytest)"""
import numpy as np

from m2_checks import (EvalError, check_pairing, classify_templates, kabsch_rmsd, min_distance,
                       template_id)


def raises(fn, *a):
    try:
        fn(*a)
    except EvalError:
        return True
    return False


def test_empty_selection_never_gives_zero():
    # the bug this guards against: zero matched atoms reported as 0.0 Å
    assert raises(kabsch_rmsd, np.zeros((0, 3)), np.zeros((0, 3)))
    assert raises(min_distance, np.zeros((0, 3)), np.ones((5, 3)))


def test_unpaired_or_mismatched_atoms_raise():
    rng = np.random.default_rng(0)
    assert raises(kabsch_rmsd, rng.normal(size=(32, 3)), rng.normal(size=(31, 3)))
    assert raises(kabsch_rmsd, rng.normal(size=(2, 3)), rng.normal(size=(2, 3)))
    bad = rng.normal(size=(32, 3)); bad[0, 0] = np.nan
    assert raises(kabsch_rmsd, bad, rng.normal(size=(32, 3)))
    ids = [(i, "CYS") for i in range(9, 41)]
    assert raises(check_pairing, ids, ids[:-1], 32)          # missing atom
    assert raises(check_pairing, ids, ids, 31)               # wrong expected length
    swapped = ids[:]; swapped[3] = (12, "ALA")
    assert raises(check_pairing, ids, swapped, 32)           # residue identity differs
    check_pairing(ids, list(ids), 32)                        # correct pairing passes


def test_kabsch_values():
    rng = np.random.default_rng(1)
    P = rng.normal(size=(32, 3)) * 5
    th = 0.7
    R = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])
    assert kabsch_rmsd(P, P @ R.T + 3.0) < 1e-6              # rigid motion -> 0
    Q = P.copy(); Q[:, 0] += 1.0                             # pure translation of 1 Å in x
    assert abs(kabsch_rmsd(P, Q)) < 1e-6
    Q = P + rng.normal(scale=1.0, size=P.shape)
    assert kabsch_rmsd(P, Q) > 0.5                           # real noise -> clearly > 0


def test_templates():
    assert template_id("data_1XU1\n#") == "1xu1"
    assert raises(template_id, "")
    assert raises(template_id, "loop_\n")
    c = classify_templates(["1xu1", "2EQP", "4ht1", "1rj8"])
    assert c == {"fn14": ["2eqp"], "tweak": ["4ht1"], "complex": []}
    assert classify_templates(["1dax", "1iqa"]) == {"fn14": [], "tweak": [], "complex": []}


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f(); n += 1
    print(f"{n} tests passed")
