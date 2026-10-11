#!/bin/bash
# SGE wrapper: A3b metadata gate step 1 (obs only; no expression, no CytoTRACE2).
#$ -N A3b_meta
#$ -pe smp 1
#$ -l m_mem_free=32G
#$ -cwd
set -euo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
mkdir -p "$R/metadata_gate"
$PY "$R/code/sample_metadata.py" \
  --h5ad /home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/data/final_crc_atlas-adata.count.only.h5ad \
  --scope-tsv /home/zz950/DATA/scRNAseq/meta_study/CRC_metadata_extraction/patient_characteristics/crc_patient_metadata.tsv \
  --out "$R/metadata_gate/sample_metadata.tsv" > "$R/metadata_gate/sample_metadata.summary.json"
