#!/bin/bash
# A3a CCAT. PILOT=1: 3 fixed samples (small/median/large epithelial n) with repeat-run check.
# PILOT=0: all samples (array 1-361), only after the technical gate is accepted by review.
set -eo pipefail
source /home/zz950/softwares/miniforge3/etc/profile.d/conda.sh
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
conda activate "$ENV"
set -u
export R_LIBS="$ENV/lib/R/library:$ENV/lib/R/user-library:/home/zz950/softwares/R_lib_4:/home/zz950/softwares/miniconda3/envs/r4p3/lib/R/library"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
if [ "${PILOT:-1}" = "1" ]; then
  mkdir -p $R/ccat_pilot
  tag=$(sed -n "${SGE_TASK_ID}p" $R/ccat_pilot/pilot_samples.txt)
  "$ENV/bin/Rscript" $R/code/a3a_ccat.R $R/export/counts "$tag" $R/ccat_pilot/$tag.ccat.tsv.gz repeat
else
  mkdir -p $R/ccat
  tag=$(ls $R/export/counts | grep '\.main\.h5$' | sort | sed 's/\.main\.h5$//' | sed -n "${SGE_TASK_ID}p")
  [ -z "$tag" ] && exit 0
  "$ENV/bin/Rscript" $R/code/a3a_ccat.R $R/export/counts "$tag" $R/ccat/$tag.ccat.tsv.gz
fi
