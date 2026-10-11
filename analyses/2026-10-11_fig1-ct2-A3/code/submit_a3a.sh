#!/bin/bash
# Submit A3a (frozen v0.2): export (13 studies) -> UCell (361) -> stats/pool.
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
cd $R; mkdir -p logs
Q="-terse -q all.q -S /bin/bash -cwd -V -j y -o logs"
e=$(qsub $Q -N a3a_exp -t 1-13 -pe smp 2 -l m_mem_free=24G code/run_a3a_export.sh | cut -d. -f1)
u=$(qsub $Q -N a3a_uc -hold_jid $e -t 1-361 -tc 60 -pe smp 2 -l m_mem_free=8G code/run_a3a_ucell.sh | cut -d. -f1)
s=$(qsub $Q -N a3a_st -hold_jid $u -pe smp 2 -l m_mem_free=48G code/run_a3a_stats.sh | cut -d. -f1)
echo "export=$e ucell=$u stats=$s"
