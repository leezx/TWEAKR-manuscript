#!/bin/bash
set -euo pipefail
cd /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
/home/zz950/softwares/miniconda3/envs/r4p3/bin/python code/export_sample_counts.py --h5ad /home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/data/final_crc_atlas-adata.count.only.h5ad --cohort-cells /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_dataset_screen_20261009/cohort/fig1b_cohort_cells_v1.tsv.gz --mapping input_validation/cytotrace2_atlas_gene_mapping.tsv.gz --studies Joanito_2022_Nat_Genet,Lee_2020_Nat_Genet,Qin_2023_Cell_Rep_Med --out-dir pilot/counts_ds --depth-targets input_validation/depth_targets.csv --seeds 1,2,3,4,5
echo DONE
