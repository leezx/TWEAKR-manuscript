#!/bin/bash
# Generic SGE array task (A2.1 diagnostics): run_variant_task.sh <counts_dir> <scores_dir> <modes> <seed>
# Task n = line n+1 of <counts_dir>/export_manifest.tsv. Seed 14 is the default CytoTRACE2 seed.
set -euo pipefail
export R_LIBS=/home/zz950/softwares/R_lib_4
cd /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
cdir=$1; sdir=$2; modes=$3; seed=$4
mkdir -p $sdir
f=$(awk -F'\t' -v n=$((SGE_TASK_ID+1)) 'NR==n{print $5}' $cdir/export_manifest.tsv)
suffix=""; [ "$seed" != "14" ] && suffix=".seed$seed"
out=$sdir/${f%.h5}$suffix.scores.tsv.gz
[ -s "$out" ] && { echo "exists $out"; exit 0; }
/usr/bin/time -v /home/zz950/softwares/miniconda3/envs/r4p3/bin/Rscript code/run_cytotrace2_sample.R $cdir/$f $cdir/cell_labels.tsv $out.tmp.gz 4 $modes $seed
mv $out.tmp.gz $out
