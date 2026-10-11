#!/bin/bash
# Fig. 1c Stage 1: UCell on the frozen Stage 0 sets, main counts only (SGE array 1-361). No CT2 input.
set -eo pipefail
source /home/zz950/softwares/miniforge3/etc/profile.d/conda.sh
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
conda activate "$ENV"
set -u
export R_LIBS="$ENV/lib/R/library:$ENV/lib/R/user-library:/home/zz950/softwares/R_lib_4:/home/zz950/softwares/miniconda3/envs/r4p3/lib/R/library"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1c_epi_states_20261011
A3A=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
mkdir -p $R/ucell
tag=$(ls $A3A/export/counts | grep '\.main\.h5$' | sort | sed 's/\.main\.h5$//' | sed -n "${SGE_TASK_ID}p")
[ -z "$tag" ] && { echo "no sample for task $SGE_TASK_ID"; exit 0; }
"$ENV/bin/Rscript" $R/code/a3a_ucell.R $A3A/export/counts "$tag" $R/private/genesets_fig1c.private.tsv $R/ucell/$tag.ucell.tsv.gz 2 main
