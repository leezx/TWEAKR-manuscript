#!/bin/bash
# SGE wrapper: technical pilot summary (summarise_pilot.py) plus per-task resources from qacct.
#$ -N fig1b_sum
#$ -pe smp 2
#$ -l m_mem_free=24G
#$ -cwd
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
P=$R/pilot
OUT=$R/pilot/summary
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
mkdir -p "$OUT"

$PY "$R/code/summarise_pilot.py" \
  --counts-dir "$P/counts" --scores-dir "$P/scores" \
  --ds-counts-dir "$P/counts_ds" --ds-scores-dir "$P/scores_ds" \
  --sel-counts-dir "$P/counts_sel" --sel-scores-dir "$P/scores_sel" \
  --pool-counts-dir "$P/counts_pool" --pool-scores-dir "$P/scores_pool" \
  --rep-scores-dir "$P/scores_rep" --out-dir "$OUT"

cp "$P/invariance/invariance_summary.csv" "$OUT/pilot_invariance_summary.csv"

# resources per finished task (wall clock, SGE maxvmem = virtual memory, not RSS)
export SGE_ROOT=/opt/sge
{
  echo "job,variant,task,failed,exit_status,wallclock_s,maxvmem"
  for jv in 3654321:main 3654335:depth_matched 3654338:invariance 3654340:selection_only \
            3654341:patient_pooled 3654342:seed_repeat 3654343:seed_repeat 3654344:seed_repeat; do
    j=${jv%%:*}; v=${jv#*:}
    /opt/sge/bin/lx-amd64/qacct -j "$j" | awk -v j="$j" -v v="$v" '
      /^taskid/{t=$2} /^failed/{f=$2} /^exit_status/{e=$2}
      /^ru_wallclock/{w=$2; sub(/s$/,"",w)}
      /^maxvmem/{print j","v","t","f","e","w","$2}'
  done
} > "$OUT/pilot_resources_by_task.csv"
echo DONE
