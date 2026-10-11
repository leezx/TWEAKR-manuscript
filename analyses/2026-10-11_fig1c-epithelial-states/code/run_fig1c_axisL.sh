#!/bin/bash
# Fig. 1c Stage 1 Axis L. Usage: run_fig1c_axisL.sh ref | fit (SGE_TASK_ID 1-6 -> fold 0-5) | predict (1-361)
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1c_epi_states_20261011
A3A=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
G=/home/zz950/DATA/scRNAseq/geo_datasets/GSE178341/suppl
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
export OMP_NUM_THREADS=${NSLOTS:-2} OPENBLAS_NUM_THREADS=${NSLOTS:-2} MKL_NUM_THREADS=${NSLOTS:-2}
case "$1" in
  ref)
    $PY $R/code/fig1c_pelka_ref.py --h5 $G/GSE178341_crc10x_full_c295v4_submit.h5 \
      --cluster $G/GSE178341_crc10x_full_c295v4_submit_cluster.csv.gz \
      --meta $G/GSE178341_crc10x_full_c295v4_submit_metatables.csv.gz \
      --atlas_main_h5 $(ls $A3A/export/counts/*.main.h5 | head -1) --out_dir $R/axisL/ref ;;
  fit)
    $PY $R/code/fig1c_axisL_fit.py --ref_dir $R/axisL/ref --holdout $R/private/holdout_H.private.txt \
      --fold $((SGE_TASK_ID - 1)) --out_dir $R/axisL/models ;;
  predict)
    $PY $R/code/fig1c_axisL_predict.py --counts_dir $A3A/export/counts --model_dir $R/axisL/models \
      --folds $R/axisL/ref/pelka_outer_folds.tsv --task $SGE_TASK_ID --out_dir $R/axisL/pred ;;
esac
