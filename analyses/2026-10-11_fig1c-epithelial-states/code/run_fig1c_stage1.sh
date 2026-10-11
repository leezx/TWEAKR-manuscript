#!/bin/bash
# Fig. 1c Stage 1 statistics. Usage: run_fig1c_stage1.sh phase1 (SGE 1-13, one study each) | gates
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1c_epi_states_20261011
A3A=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
case "$1" in
  phase1)
    $PY $R/code/fig1c_stage1_sample.py --task $SGE_TASK_ID --cells_dir $A3A/export/cells \
      --ucell_dir $R/ucell --axisl_dir $R/axisL/pred --out_dir $R/stage1/phase1 ;;
  gates)
    $PY $R/code/fig1c_stage1_gates.py --root $R \
      --patient_meta /home/zz950/DATA/scRNAseq/meta_study/CRC_metadata_extraction/patient_characteristics/crc_patient_metadata.tsv \
      --public_out $R/stage1/public ;;
esac
