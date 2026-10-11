#!/bin/bash
# A3a CCAT secondary family: completeness check, then statistics (public aggregates to $R/public_ccat).
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
n=$(ls $R/export/counts | grep -c '\.main\.h5$'); c=$(ls $R/ccat | grep -c '\.ccat\.tsv\.gz$')
[ "$n" -eq "$c" ] || { echo "CCAT incomplete: $c of $n"; exit 1; }
for f in $R/ccat/*.gz; do gzip -t "$f" || { echo "bad gzip $f"; exit 1; }; done
/home/zz950/softwares/miniconda3/envs/r4p3/bin/python $R/code/a3a_ccat_stats.py --a3-root $R --out $R/public_ccat
echo STEP_DONE ccat_stats
