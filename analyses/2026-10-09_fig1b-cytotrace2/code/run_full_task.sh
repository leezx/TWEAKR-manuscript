#!/bin/bash
# Full-run SGE array task: run_full_task.sh <counts_dir> <scores_dir>
# Task n = line n+1 of <counts_dir>/export_manifest.tsv; modes whole,intrinsic; seed 14 (A2.1).
# Tasks beyond the manifest exit 0 (the array is sized before the export finishes).
set -euo pipefail
export R_LIBS=/home/zz950/softwares/R_lib_4
cd /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
cdir=$1; sdir=$2
mkdir -p $sdir
f=$(awk -F'\t' -v n=$((SGE_TASK_ID+1)) 'NR==n{print $5}' $cdir/export_manifest.tsv)
[ -z "$f" ] && { echo "no task $SGE_TASK_ID"; exit 0; }
out=$sdir/${f%.h5}.scores.tsv.gz
[ -s "$out" ] && { echo "exists $out"; exit 0; }
/usr/bin/time -v /home/zz950/softwares/miniconda3/envs/r4p3/bin/Rscript code/run_cytotrace2_sample.R $cdir/$f $cdir/cell_labels.tsv $out.tmp.gz 4 whole,intrinsic
mv $out.tmp.gz $out
echo STEP_DONE score $f
