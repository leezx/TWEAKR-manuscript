#!/bin/bash
#SBATCH -J fn14_M1b_msaC
#SBATCH -p short
#SBATCH -t 0-06:00
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -o /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b/logs/%x_%j.out
#SBATCH -e /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b/logs/%x_%j.err
# M1b amendment 1, condition C: template cutoff 2007-12-31 excludes every Fn14 experimental
# structure found so far (2EQP 2008-04-01, 2KMZ/2KN0 2011-06-29). Deciding condition.
set -euo pipefail
R=/n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b
module load alphafold/3.0.1
date -Is
run_alphafold.py --json_path=$R/inputs/fn14_ecd_28_80_tmplC.json --output_dir=$R/out \
  --norun_inference --max_template_date=2007-12-31
date -Is
