#!/bin/bash
# SGE array task: one exported sample file per task (line SGE_TASK_ID+1 of export_manifest.tsv).
set -euo pipefail
export R_LIBS=/home/zz950/softwares/R_lib_4
cd /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
f=$(awk -F'\t' -v n=$((SGE_TASK_ID+1)) 'NR==n{print $5}' pilot/counts/export_manifest.tsv)
out=pilot/scores/${f%.h5}.scores.tsv.gz
[ -s "$out" ] && { echo "exists $out"; exit 0; }
/usr/bin/time -v /home/zz950/softwares/miniconda3/envs/r4p3/bin/Rscript code/run_cytotrace2_sample.R pilot/counts/$f pilot/counts/cell_labels.tsv $out.tmp.gz 4
mv $out.tmp.gz $out
