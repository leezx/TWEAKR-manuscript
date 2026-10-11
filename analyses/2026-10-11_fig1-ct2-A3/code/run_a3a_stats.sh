#!/bin/bash
# A3a steps 3-4: per-sample correlations, then pooling (public aggregates to $R/public).
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
F=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
n=$(ls $R/export/counts | grep -c '\.main\.h5$'); u=$(ls $R/ucell | grep -c '\.ucell\.tsv\.gz$')
[ "$n" -eq "$u" ] || { echo "UCell incomplete: $u of $n"; exit 1; }
$PY $R/code/a3a_sample_stats.py --a3-root $R --fig1b-root $F --out $R/stats
$PY $R/code/a3a_pool.py --stats-dir $R/stats \
  --patient-meta /home/zz950/DATA/scRNAseq/meta_study/CRC_metadata_extraction/patient_characteristics/crc_patient_metadata.tsv \
  --out $R/public
echo STEP_DONE stats
