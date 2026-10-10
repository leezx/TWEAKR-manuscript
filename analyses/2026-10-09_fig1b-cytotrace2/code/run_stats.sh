#!/bin/bash
# SGE wrapper: Fig. 1B A2.1 statistics on the full run (held on the depth-matched array).
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
C=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_dataset_screen_20261009/cohort
export OMP_NUM_THREADS=$NSLOTS MKL_NUM_THREADS=$NSLOTS OPENBLAS_NUM_THREADS=$NSLOTS
cd $R
/home/zz950/softwares/miniconda3/envs/r4p3/bin/python code/fig1b_stats.py --root $R \
  --cohort-cells $C/fig1b_cohort_cells_v1.tsv.gz --cohort-patients $C/fig1b_cohort_patients_v1.csv --out full/stats
echo STEP_DONE stats
