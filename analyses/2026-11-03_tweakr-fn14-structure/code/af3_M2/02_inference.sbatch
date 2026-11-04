#!/bin/bash
#SBATCH -J m2_inf
#SBATCH -p gpu
#SBATCH --gres=gpu:l40s:1
#SBATCH -t 0-03:00
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -o /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M2/logs/%x_%j.out
#SBATCH -e /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M2/logs/%x_%j.err
# M2 stage 2 (GPU). Names are already lower-case (AF3 lower-cases output names).
set -euo pipefail
R=/n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M2
L=/n/data1/dfci/medonc/sethi/lab/zhixin/TWEAKR-oncoFetal/af3_M2
module load alphafold/3.0.1
nvidia-smi --query-gpu=name,memory.total --format=csv
date "+%FT%T"
for c in c d; do
  N=m2_tweak3_fn14x3_tmpl$c
  run_alphafold.py --json_path=$R/out/$N/${N}_data.json --output_dir=$R/out_inf --norun_data_pipeline
done
date "+%FT%T"
mkdir -p $L
echo "slurm_job_inference=$SLURM_JOB_ID" > $L/run_metadata.txt
for c in c d; do
  N=m2_tweak3_fn14x3_tmpl$c
  D=$(ls -d $R/out_inf/${N}* | head -1)
  mkdir -p $L/$N
  cp $R/out/$N/${N}_data.json $L/$N/
  (cd $D && find . \( -name "*.cif" -o -name "*summary_confidences.json" -o -name "ranking_scores.csv" -o -name "*confidences.json" \) -print0 | cpio -0pdm $L/$N/ 2>/dev/null)
done
(cd $L && find . -type f ! -name manifest_sha256.txt -exec sha256sum {} \; | sort -k2 > manifest_sha256.txt)
