#!/bin/bash
# Fig. 1c Stage 3: CT2 joined to frozen v0.3a labels. Usage: sample (SGE 1-13) | pool
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1c_epi_states_20261011
A3A=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
F=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
L=$R/stage1_v03a/phase1
O=$R/stage3
mkdir -p $O/sample $O/public
case "$1" in
  sample) $PY $R/code/fig1c_stage3.py sample --task $SGE_TASK_ID --labels_dir $L --cells_dir $A3A/export/cells \
            --fig1b_root $F --out_dir $O/sample ;;
  pool)   $PY $R/code/fig1c_stage3.py pool --labels_dir $L --out_dir $O/sample --public_out $O/public \
            --stage1_summary $R/stage1_v03a/stage1_gate_summary.json ;;
esac
