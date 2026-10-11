#!/bin/bash
# A3a POST-HOC (review 2026-10-11): UCell for revCSC without TNFRSF12A, main variant only (array 1-361).
set -eo pipefail
source /home/zz950/softwares/miniforge3/etc/profile.d/conda.sh
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
conda activate "$ENV"
set -u
export R_LIBS="$ENV/lib/R/library:$ENV/lib/R/user-library:/home/zz950/softwares/R_lib_4:/home/zz950/softwares/miniconda3/envs/r4p3/lib/R/library"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
mkdir -p $R/posthoc/ucell
tag=$(ls $R/export/counts | grep '\.main\.h5$' | sort | sed 's/\.main\.h5$//' | sed -n "${SGE_TASK_ID}p")
[ -z "$tag" ] && exit 0
"$ENV/bin/Rscript" $R/code/a3a_ucell.R $R/export/counts "$tag" $R/private/genesets_posthoc_revCSC_noTNFRSF12A.private.tsv $R/posthoc/ucell/$tag.ucell.tsv.gz 2 main
