#!/bin/bash
# Submit the L2 annotation chain on Argos (all.q). Usage: submit_l2.sh smoke|full
# Run from the Argos run root's code/ copy (synced from the repo; commit in code/COMMIT).
set -euo pipefail
mode=$1
BASE=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009/l2_annotation
if [ "$mode" = smoke ]; then
  R=$BASE/smoke; NPAT=4; EXTRA=--smoke; SEXTRA="--smoke-base-epochs 10"
  B="-pe smp 4 -l m_mem_free=8G"; S="-pe smp 4 -l m_mem_free=4G"; L="-pe smp 4 -l m_mem_free=8G"
  CP="-pe smp 4 -l m_mem_free=8G"; IC="-pe smp 4 -l m_mem_free=4G"; F="-pe smp 4 -l m_mem_free=8G"
elif [ "$mode" = full ]; then
  R=$BASE; NPAT=222; EXTRA=; SEXTRA=
  B="-pe smp 8 -l m_mem_free=16G"; S="-pe smp 16 -l m_mem_free=8G"; L="-pe smp 8 -l m_mem_free=24G"
  CP="-pe smp 4 -l m_mem_free=40G"; IC="-pe smp 8 -l m_mem_free=4G"; F="-pe smp 4 -l m_mem_free=32G"
else
  echo "usage: submit_l2.sh smoke|full"; exit 2
fi
mkdir -p $R/logs
[ "$R" != "$BASE" ] && { rm -rf $R/code; cp -r $BASE/code $R/code; }
W=$R/code/l2/run_l2_step.sh
Q="-q all.q -V -cwd -o $R/logs -e $R/logs -terse"
j1=$(qsub $Q $B -N l2b_$mode $W build $R $EXTRA)
j2=$(qsub $Q $S -N l2s_$mode -hold_jid $j1 -t 1-3 $W scvi $R $SEXTRA | cut -d. -f1)
j3=$(qsub $Q $L -N l2l_$mode -hold_jid $j2 -t 1-3 $W label $R | cut -d. -f1)
j4=$(qsub $Q $CP -N l2c_$mode -hold_jid $j3 $W cnvprep $R)
j5=$(qsub $Q $IC -N l2i_$mode -hold_jid $j4 -t 1-$NPAT $W infercnv $R | cut -d. -f1)
j6=$(qsub $Q $F -N l2f_$mode -hold_jid $j5 $W finalize $R)
echo "$mode build=$j1 scvi=$j2 label=$j3 cnvprep=$j4 infercnv=$j5 finalize=$j6" | tee -a $R/logs/submitted.txt
