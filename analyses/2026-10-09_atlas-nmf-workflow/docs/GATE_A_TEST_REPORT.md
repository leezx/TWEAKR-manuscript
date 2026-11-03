# Argos synthetic algorithm verification

Date: 2026-10-09. Environment: /home/zz950/softwares/miniforge3/envs/argos-codex.
Working root: /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_algorithm_gate_a_20261009.

Command: environment bin/python -m unittest discover -s analyses/2026-10-09_atlas-nmf-workflow/tests -v.

Result: 6 tests passed, 0.951 seconds. Tests cover 35/34 overlap boundary,
cross-rank requirement, within-sample redundant copies, independent patient
counts, per-dataset denominators, two-cluster recovery, singleton exclusion,
input-order invariance, legacy coverage, task expansion and missing dataset/rank
failure. Initial subprocess interpreter failure was repaired using sys.executable.

No real Atlas counts or metadata were read. This is software verification;
Gate A remains pending independent code/method review and Gate B has not started.
