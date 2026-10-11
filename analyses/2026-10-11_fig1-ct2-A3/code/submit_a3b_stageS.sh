#!/bin/bash
# Submit A3b Stage S scoring: prep (SHA check) -> exports (main, ds np, ds pp) -> CT2 arrays; UCell array.
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
cd $R; mkdir -p logs
Q="-terse -q all.q -S /bin/bash -cwd -V -j y -o logs"
p=$(qsub $Q -N a3bS_prep -pe smp 2 -l m_mem_free=24G code/run_a3b_ct2.sh prep | cut -d. -f1)
em=$(qsub $Q -N a3bS_exm -hold_jid $p -pe smp 2 -l m_mem_free=24G code/run_a3b_ct2.sh export main | cut -d. -f1)
en=$(qsub $Q -N a3bS_exn -hold_jid $p -pe smp 2 -l m_mem_free=24G code/run_a3b_ct2.sh export np | cut -d. -f1)
ep=$(qsub $Q -N a3bS_exp -hold_jid $p -pe smp 2 -l m_mem_free=24G code/run_a3b_ct2.sh export pp | cut -d. -f1)
sm=$(qsub $Q -N a3bS_ctm -hold_jid $em -t 1-450 -tc 80 -pe smp 4 -l m_mem_free=8G code/run_a3b_ct2.sh score main | cut -d. -f1)
sn=$(qsub $Q -N a3bS_ctn -hold_jid $en -t 1-1600 -tc 80 -pe smp 4 -l m_mem_free=8G code/run_a3b_ct2.sh score np | cut -d. -f1)
sp=$(qsub $Q -N a3bS_ctp -hold_jid $ep -t 1-1000 -tc 60 -pe smp 4 -l m_mem_free=8G code/run_a3b_ct2.sh score pp | cut -d. -f1)
u=$(qsub $Q -N a3bS_uc -hold_jid $p -t 1-450 -tc 60 -pe smp 2 -l m_mem_free=8G code/run_a3b_ct2.sh ucell | cut -d. -f1)
echo "prep=$p exp_main=$em exp_np=$en exp_pp=$ep ct2_main=$sm ct2_np=$sn ct2_pp=$sp ucell=$u"
