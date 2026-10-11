#!/bin/bash
# A3a POST-HOC (review 2026-10-11): pooled self-inclusion check, P3 QC, co-activation expectation.
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
F=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
/home/zz950/softwares/miniconda3/envs/r4p3/bin/python $R/code/a3a_posthoc.py --a3-root $R --fig1b-root $F --out $R/public_posthoc
echo STEP_DONE posthoc
