#!/bin/bash
#SBATCH -J fn14_M1b_inf
#SBATCH -p gpu
#SBATCH --gres=gpu:l40s:1
#SBATCH -t 0-02:00
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -o /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b/logs/%x_%j.out
#SBATCH -e /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b/logs/%x_%j.err
# M1b stage 2 (GPU): inference from the stage-1 *_data.json; 5 seeds x 5 diffusion samples.
set -euo pipefail
R=/n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b
L=/n/data1/dfci/medonc/sethi/lab/zhixin/TWEAKR-oncoFetal/af3_M1b
module load alphafold/3.0.1
nvidia-smi --query-gpu=name,memory.total --format=csv
date -Is
for C in A B; do
  N=fn14_ecd_28_80_tmpl$C
  run_alphafold.py --json_path=$R/out/$N/${N}_data.json --output_dir=$R/out_inf \
    --norun_data_pipeline
done
date -Is
# freeze lightweight products in the lab dir (O2 AGENTS.md §2/§4)
mkdir -p $L
for C in A B; do
  N=fn14_ecd_28_80_tmpl$C
  D=$(ls -d $R/out_inf/${N}* | head -1)
  mkdir -p $L/$N
  cp $R/out/$N/${N}_data.json $L/$N/
  (cd $D && find . \( -name "*.cif" -o -name "*summary_confidences.json" -o -name "ranking_scores.csv" -o -name "*_confidences.json" \) -print0 | cpio -0pdm $L/$N/ 2>/dev/null)
done
(cd $L && find . -type f -exec sha256sum {} \; > manifest_sha256.txt)
echo "slurm_job=$SLURM_JOB_ID" > $L/run_metadata.txt
