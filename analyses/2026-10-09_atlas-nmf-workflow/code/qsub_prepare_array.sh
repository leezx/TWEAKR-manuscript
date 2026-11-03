#!/bin/bash
source /etc/profile
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -N atlas_nmf_prepare
#$ -pe pvm 2

set -euo pipefail

: "${WORKFLOW_DIR:?WORKFLOW_DIR is required}"
: "${DATASET_PLAN:?DATASET_PLAN is required}"
: "${RUN_ROOT:?RUN_ROOT is required}"
: "${CONDA_ENV:?CONDA_ENV is required}"

source /home/zz950/softwares/miniforge3/etc/profile.d/conda.sh
conda activate "${CONDA_ENV}"

plan_row=$(awk -F '\t' -v task="${SGE_TASK_ID}" \
  'NR > 1 && $7 == 1 && $8 == "approved" {n++; if (n == task) {print NR - 1; exit}}' \
  "${DATASET_PLAN}")
if [[ -z "${plan_row}" ]]; then
  echo "No approved plan row for SGE_TASK_ID=${SGE_TASK_ID}" >&2
  exit 2
fi

Rscript "${WORKFLOW_DIR}/code/02_prepare_seurat_nmf.R" \
  "${DATASET_PLAN}" "${plan_row}" "${RUN_ROOT}"
