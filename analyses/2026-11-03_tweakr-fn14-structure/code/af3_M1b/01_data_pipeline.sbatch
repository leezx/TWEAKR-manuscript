#!/bin/bash
#SBATCH -J fn14_M1b_msa
#SBATCH -p short
#SBATCH -t 0-06:00
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -o /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b/logs/%x_%j.out
#SBATCH -e /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b/logs/%x_%j.err
# M1b stage 1 (CPU): MSA + template search for Fn14 ECD 28-80.
#   A = AF3 default template cutoff (2021-09-30) -> 2KMZ (released 2011-06-29) MAY be used as template
#   B = --max_template_date=2011-06-01        -> 2KMZ / 2KN0 excluded; this is the pre-registered test
set -euo pipefail
R=/n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M1b
module load alphafold/3.0.1
date -Is
run_alphafold.py --json_path=$R/inputs/fn14_ecd_28_80_tmplA.json --output_dir=$R/out \
  --norun_inference
run_alphafold.py --json_path=$R/inputs/fn14_ecd_28_80_tmplB.json --output_dir=$R/out \
  --norun_inference --max_template_date=2011-06-01
date -Is
