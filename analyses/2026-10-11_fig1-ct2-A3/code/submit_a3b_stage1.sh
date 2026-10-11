#!/bin/bash
# Submit A3b Stage I (frozen v0.3) after export: tasks -> inferCNV (<=200 patients) -> T calls; N per study;
# identity -> QA. Usage: submit_a3b_stage1.sh <export_job_id>
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
cd $R; mkdir -p logs
Q="-terse -q all.q -S /bin/bash -cwd -V -j y -o logs"
t=$(qsub $Q -N a3b_tasks -hold_jid $1 -l m_mem_free=2G code/run_a3b_stage1.sh tasks | cut -d. -f1)
c=$(qsub $Q -N a3b_cnv -hold_jid $t -t 1-200 -tc 40 -pe smp 4 -l m_mem_free=8G code/run_a3b_infercnv.sh | cut -d. -f1)
k=$(qsub $Q -N a3b_tcall -hold_jid $c -pe smp 2 -l m_mem_free=48G code/run_a3b_stage1.sh tcalls | cut -d. -f1)
n=$(qsub $Q -N a3b_N -hold_jid $1 -t 1-10 -pe smp 4 -l m_mem_free=48G code/run_a3b_stage1.sh N | cut -d. -f1)
i=$(qsub $Q -N a3b_id -hold_jid $k,$n -pe smp 4 -l m_mem_free=64G code/run_a3b_stage1.sh identity | cut -d. -f1)
a=$(qsub $Q -N a3b_qa -hold_jid $i -pe smp 2 -l m_mem_free=48G code/run_a3b_stage1.sh qa | cut -d. -f1)
echo "tasks=$t cnv=$c tcalls=$k N=$n identity=$i qa=$a"
