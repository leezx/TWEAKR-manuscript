#!/bin/bash
# Full 13-study export (A2.1): run_export_full.sh main|ds
#   main: whole-sample raw counts (model genes), primary run input -> full/counts
#   ds  : depth-matched variant at study target T_s, seeds 1-5     -> full/counts_ds
set -euo pipefail
cd /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
P=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
S=Chen_2024_Cancer_Cell,Guo_2022_JCI_Insight,Joanito_2022_Nat_Genet,Khaliq_2022_Genome_Biol,Lee_2020_Nat_Genet,Li_2023_Cancer_Cell,Liu_2024_Cancer_Res,MUI_Innsbruck,Pelka_2021_Cell,Qi_2022_Nat_Commun,Qian_2020_Cell_Res,Qin_2023_Cell_Rep_Med,Uhlitz_2021_EMBO_Mol_Med
A="--h5ad /home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/data/final_crc_atlas-adata.count.only.h5ad --cohort-cells /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_dataset_screen_20261009/cohort/fig1b_cohort_cells_v1.tsv.gz --mapping input_validation/cytotrace2_atlas_gene_mapping.tsv.gz --studies $S"
case $1 in
  main) $P code/export_sample_counts.py $A --out-dir full/counts ;;
  ds)   $P code/export_sample_counts.py $A --out-dir full/counts_ds --depth-targets input_validation/depth_targets.csv --seeds 1,2,3,4,5 ;;
esac
echo STEP_DONE export $1
