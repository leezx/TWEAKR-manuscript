#!/bin/bash
#SBATCH -J m2_msa
#SBATCH -p short
#SBATCH -t 0-08:00
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -o /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M2/logs/%x_%j.out
#SBATCH -e /n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M2/logs/%x_%j.err
# M2 stage 1 (CPU). c = template cutoff 2007-12-31 (deciding), d = AF3 default (control).
set -euo pipefail
R=/n/scratch/users/z/zhl595/projects/TWEAKR-oncoFetal/af3_M2
module load alphafold/3.0.1
date "+%FT%T"
run_alphafold.py --json_path=$R/inputs/m2_tweak3_fn14x3_tmplc.json --output_dir=$R/out --norun_inference --max_template_date=2007-12-31
run_alphafold.py --json_path=$R/inputs/m2_tweak3_fn14x3_tmpld.json --output_dir=$R/out --norun_inference
date "+%FT%T"
