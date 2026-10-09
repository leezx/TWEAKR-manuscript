#!/bin/bash
#$ -S /bin/bash
#$ -pe pvm 2
#$ -cwd
#$ -N NMF_pilot_2samples
set -eo pipefail
source /etc/profile
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
source /home/zz950/softwares/miniforge3/etc/profile.d/conda.sh
conda activate "$ENV"
export R_LIBS_USER="$ENV/lib/R/user-library"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
ROOT=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_pilot_GSE254249_20261009
WF="$ROOT/analyses/2026-10-09_atlas-nmf-workflow"
mkdir -p "$ROOT/logs"
exec > >(tee "$ROOT/logs/pilot.log") 2>&1
set -x
date -u
hostname
export EXECUTE_NMF=1 MIN_CELLS=200 MIN_DETECTED_CELLS=1 SCALE_FACTOR=10000
for row in 1 2; do
  /usr/bin/time -v "$ENV/bin/Rscript" "$WF/code/02_prepare_seurat_nmf.R" "$WF/config/pilot_plan.tsv" "$row" "$ROOT"
done
"$ENV/bin/python" "$WF/code/04_build_nmf_tasks.py" --prepared-root "$ROOT/prepared" --ranks 4,5,6,7,8,9 --output-root "$ROOT" --prepared-manifest "$ROOT/prepared_manifest.tsv" --tasks "$ROOT/tasks.tsv"
while IFS=$'\t' read -r task dataset source sample matrix rank output; do
  output=${output%$'\r'}
  /usr/bin/time -v "$ENV/bin/Rscript" "$WF/code/03_run_fastnmf.R" "$matrix" "$rank" "$output" 42
done < <(tail -n +2 "$ROOT/tasks.tsv")
"$ENV/bin/python" "$WF/code/05_validate_nmf_outputs.py" --plan "$WF/config/pilot_plan.tsv" --tasks "$ROOT/tasks.tsv" --ranks 4,5,6,7,8,9 --output "$ROOT/validation.tsv"
"$ENV/bin/python" "$WF/code/06_filter_robust_programs.py" --tasks "$ROOT/tasks.tsv" --cohort "$WF/docs/cohort_identity_mapping.tsv" --output "$ROOT/robust.tsv"
"$ENV/bin/python" "$WF/code/07_discover_metaprograms.py" --programs "$ROOT/robust.tsv" --cohort "$WF/docs/cohort_identity_mapping.tsv" --output "$ROOT/MPs.json"
date -u
echo PILOT_COMPLETE
touch "$ROOT/PILOT_COMPLETE"
