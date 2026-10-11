#!/bin/bash
# A3b Stage I step 1: per-study export (SGE array 1-10). Frozen contract A3b v0.3.
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
F=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
S=(Chen_2024_Cancer_Cell Joanito_2022_Nat_Genet Khaliq_2022_Genome_Biol Lee_2020_Nat_Genet Li_2023_Cancer_Cell MUI_Innsbruck Pelka_2021_Cell Qian_2020_Cell_Res Qin_2023_Cell_Rep_Med Uhlitz_2021_EMBO_Mol_Med)
study=${S[$((SGE_TASK_ID-1))]}
$PY $R/code/a3b_export.py \
  --h5ad /home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/data/final_crc_atlas-adata.count.only.h5ad \
  --samples $R/A3b/inputs/a3b_samples.tsv \
  --l2-config $F/l2_annotation/code/l2_config.yaml \
  --screen-code /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_dataset_screen_20261009/code \
  --annotation $F/l2_annotation/final/annotation_v1.tsv.gz \
  --study $study --out-dir $R/A3b/export
echo STEP_DONE a3b_export $study
