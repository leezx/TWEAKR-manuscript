#!/bin/bash
set -euo pipefail
export R_LIBS=/home/zz950/softwares/R_lib_4
E=/home/zz950/softwares/miniconda3/envs/r4p3/bin
cd /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
$E/python code/validate_inputs.py --h5ad /home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/data/final_crc_atlas-adata.count.only.h5ad --cohort-cells /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_dataset_screen_20261009/cohort/fig1b_cohort_cells_v1.tsv.gz --out-dir input_validation
$E/Rscript code/cytotrace2_gene_coverage.R input_validation/study_gene_detection.tsv.gz input_validation
echo DONE
