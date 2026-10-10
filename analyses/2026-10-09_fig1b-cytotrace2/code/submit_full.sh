#!/bin/bash
# Submit the full 13-study CytoTRACE2 run (A2.1) after the annotation_v1 freeze.
# main: 361 whole-sample tasks; ds: 361 x 5 seeds (sized 1-1805; surplus tasks exit 0).
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
cd $R; mkdir -p full/logs
Q="-terse -q all.q -S /bin/bash -cwd -V -j y -o full/logs"
e1=$(qsub $Q -N ct2f_exp_main -pe smp 4 -l m_mem_free=16G code/run_export_full.sh main)
e2=$(qsub $Q -N ct2f_exp_ds   -pe smp 4 -l m_mem_free=16G code/run_export_full.sh ds)
s1=$(qsub $Q -N ct2f_main -hold_jid $e1 -t 1-361  -pe smp 4 -l m_mem_free=6G code/run_full_task.sh full/counts full/scores | cut -d. -f1)
s2=$(qsub $Q -N ct2f_ds   -hold_jid $e2 -t 1-1805 -pe smp 4 -l m_mem_free=6G code/run_full_task.sh full/counts_ds full/scores_ds | cut -d. -f1)
echo "$(date -Is) export_main=$e1 export_ds=$e2 score_main=$s1 score_ds=$s2" | tee -a full/logs/submitted.txt
