#!/bin/bash
#SBATCH -J m3_msa
#SBATCH -p short
#SBATCH -t 0-08:00
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -o /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M3/logs/%x_%j.out
#SBATCH -e /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M3/logs/%x_%j.err
# M3 stage 1 (CPU). Template cutoff 2007-12-31 for both, as pre-registered: excludes every Fn14
# structure and any antibody-Fn14 structure.
set -euo pipefail
R=/n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M3
module load alphafold/3.0.1
date "+%FT%T"
for N in m3_fn14_fab_f1_pdl192 m3_fn14_fab_f2_hup4a8; do
  run_alphafold.py --json_path=$R/inputs/$N.json --output_dir=$R/out --norun_inference --max_template_date=2007-12-31
done
date "+%FT%T"
