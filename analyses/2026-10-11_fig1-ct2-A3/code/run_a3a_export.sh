#!/bin/bash
# A3a step 1: per-study export (SGE array 1-13). Frozen contract A3a v0.2.
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
F=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
S=(Chen_2024_Cancer_Cell Guo_2022_JCI_Insight Joanito_2022_Nat_Genet Khaliq_2022_Genome_Biol Lee_2020_Nat_Genet Li_2023_Cancer_Cell Liu_2024_Cancer_Res MUI_Innsbruck Pelka_2021_Cell Qi_2022_Nat_Commun Qian_2020_Cell_Res Qin_2023_Cell_Rep_Med Uhlitz_2021_EMBO_Mol_Med)
study=${S[$((SGE_TASK_ID-1))]}
$PY $R/code/a3a_export.py \
  --h5ad /home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/data/final_crc_atlas-adata.count.only.h5ad \
  --cohort-cells /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_dataset_screen_20261009/cohort/fig1b_cohort_cells_v1.tsv.gz \
  --annotation $F/l2_annotation/final/annotation_v1.tsv.gz \
  --mapping $F/input_validation/cytotrace2_atlas_gene_mapping.tsv.gz \
  --depth-targets $F/input_validation/depth_targets.csv \
  --fig1b-ds-dir $F/full/counts_ds --study $study --out-dir $R/export
echo STEP_DONE export $study
