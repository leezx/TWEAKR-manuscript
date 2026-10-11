#!/bin/bash
# A3b Stage I step 2: joint inferCNV, one patient per task (task list: A3b/export/cnv_inputs/tasks.txt).
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
export R_LIBS=/home/zz950/softwares/R_lib_4
RS=/home/zz950/softwares/miniconda3/envs/r4p3/bin/Rscript
C=$R/A3b/export/cnv_inputs
d=$(sed -n "${SGE_TASK_ID}p" $C/tasks.txt)
[ -f $R/A3b/cnv_out/$d/cnv_metrics.tsv.gz ] && { echo SKIP $d; exit 0; }
$RS $R/code/a3b_infercnv.R $C/$d $C/gene_order.tsv $C/genes.txt $R/A3b/cnv_out/$d ${NSLOTS:-4}
echo STEP_DONE a3b_infercnv $d
