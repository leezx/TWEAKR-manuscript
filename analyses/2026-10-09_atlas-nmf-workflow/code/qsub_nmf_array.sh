#!/bin/bash
source /etc/profile
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -N atlas_fastnmf
#$ -pe pvm 2

set -euo pipefail

: "${WORKFLOW_DIR:?WORKFLOW_DIR is required}"
: "${NMF_TASKS:?NMF_TASKS is required}"
: "${CONDA_ENV:?CONDA_ENV is required}"
: "${SEED:?SEED is required}"

source /home/zz950/softwares/miniforge3/etc/profile.d/conda.sh
conda activate "${CONDA_ENV}"

task_line=$(awk -F '\t' -v row="$((SGE_TASK_ID + 1))" 'NR == row {print; exit}' "${NMF_TASKS}")
if [[ -z "${task_line}" ]]; then
  echo "No task row for SGE_TASK_ID=${SGE_TASK_ID}" >&2
  exit 2
fi

IFS=$'\t' read -r task_id dataset_id source_id sample_id matrix_path rank output_dir <<< "${task_line}"
mkdir -p "${output_dir}"
Rscript "${WORKFLOW_DIR}/code/03_run_fastnmf.R" \
  "${matrix_path}" "${rank}" "${output_dir}" "${SEED}" </dev/null
