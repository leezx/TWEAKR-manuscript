#!/bin/bash

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: submit_reviewed_workflow.sh {prepare|nmf} WORKFLOW_ENV" >&2
  exit 2
fi

stage=$1
env_file=$2
workflow_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

set -a
source "${env_file}"
set +a

if [[ "${DATASET_PLAN}" != /* ]]; then
  DATASET_PLAN="${workflow_dir}/${DATASET_PLAN}"
fi

if [[ "${EXECUTE_NMF:-0}" != "1" ]]; then
  echo "Execution is locked. Set EXECUTE_NMF=1 only after review." >&2
  exit 3
fi

source /home/zz950/softwares/miniforge3/etc/profile.d/conda.sh
conda activate "${CONDA_ENV}"
mkdir -p "${RUN_ROOT}/logs" "${RUN_ROOT}/manifests"

if [[ "${stage}" == "prepare" ]]; then
  [[ -f "${DATASET_PLAN}" ]] || { echo "Missing dataset plan" >&2; exit 4; }
  n_tasks=$(awk -F '\t' 'NR > 1 && $7 == 1 && $8 == "approved" {n++} END {print n+0}' "${DATASET_PLAN}")
  [[ "${n_tasks}" -gt 0 ]] || { echo "No approved preparation tasks" >&2; exit 5; }
  "${QSUB_BIN}" -t "1-${n_tasks}" -tc "${MAX_CONCURRENT}" \
    -pe pvm "${PREPARE_SLOTS}" \
    -l "m_mem_free=${PREPARE_MEMORY}" \
    -o "${RUN_ROOT}/logs" -e "${RUN_ROOT}/logs" \
    -v "WORKFLOW_DIR=${workflow_dir},DATASET_PLAN=${DATASET_PLAN},RUN_ROOT=${RUN_ROOT},CONDA_ENV=${CONDA_ENV},MIN_CELLS=${MIN_CELLS},MIN_DETECTED_CELLS=${MIN_DETECTED_CELLS},SCALE_FACTOR=${SCALE_FACTOR}" \
    "${workflow_dir}/code/qsub_prepare_array.sh"
elif [[ "${stage}" == "nmf" ]]; then
  python "${workflow_dir}/code/04_build_nmf_tasks.py" \
    --prepared-root "${RUN_ROOT}/prepared" \
    --ranks "${RANKS}" \
    --output-root "${RUN_ROOT}" \
    --prepared-manifest "${PREPARED_MANIFEST}" \
    --tasks "${NMF_TASKS}"
  n_tasks=$(awk 'END {print NR-1}' "${NMF_TASKS}")
  "${QSUB_BIN}" -t "1-${n_tasks}" -tc "${MAX_CONCURRENT}" \
    -pe pvm "${NMF_SLOTS}" \
    -l "m_mem_free=${NMF_MEMORY}" \
    -o "${RUN_ROOT}/logs" -e "${RUN_ROOT}/logs" \
    -v "WORKFLOW_DIR=${workflow_dir},NMF_TASKS=${NMF_TASKS},CONDA_ENV=${CONDA_ENV},SEED=${SEED}" \
    "${workflow_dir}/code/qsub_nmf_array.sh"
else
  echo "Unknown stage: ${stage}" >&2
  exit 2
fi
