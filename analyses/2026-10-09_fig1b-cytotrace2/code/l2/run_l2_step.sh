#!/bin/bash
# SGE task for one L2 step. Usage: run_l2_step.sh <step> <run_root> [extra args]
# Lineage steps map SGE_TASK_ID 1..3 to Epithelial, Immune, Stromal.
# infercnv: SGE_TASK_ID = row of cnv/patients.tsv; non-assessable patients exit 0.
set -euo pipefail
step=$1; R=$2; shift 2
C=$R/code
export R_LIBS=/home/zz950/softwares/R_lib_4
export PYTHONPATH=$C/l2
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
SCVI=/home/zz950/softwares/miniconda3/envs/scvi-env/bin/python
RS=/home/zz950/softwares/miniconda3/envs/r4p3/bin/Rscript
LIN=(Epithelial Immune Stromal)
cd $R
case $step in
  build)    /usr/bin/time -v $PY $C/l2/l2_build.py --config $C/l2_config.yaml --run-root $R "$@" ;;
  scvi)     /usr/bin/time -v $SCVI $C/l2/l2_scvi.py --config $C/l2_config.yaml --run-root $R --lineage ${LIN[$((SGE_TASK_ID-1))]} ;;
  label)    /usr/bin/time -v $PY $C/l2/l2_label.py --config $C/l2_config.yaml --run-root $R --lineage ${LIN[$((SGE_TASK_ID-1))]} --revcsc-gmt $C/revCSC.human.gmt ;;
  cnvprep)  /usr/bin/time -v $PY $C/l2/l2_cnv_prep.py --config $C/l2_config.yaml --run-root $R ;;
  infercnv)
    line=$(awk -F'\t' -v n=$((SGE_TASK_ID+1)) 'NR==1{for(i=1;i<=NF;i++)h[$i]=i} NR==n{print $h["assessable"]"\t"$h["dir"]}' cnv/patients.tsv)
    [ -z "$line" ] && { echo "no patient row $SGE_TASK_ID"; exit 0; }
    ok=$(cut -f1 <<<"$line"); dir=$(cut -f2 <<<"$line")
    [ "$ok" != "True" ] && { echo "not assessable $dir"; exit 0; }
    out=cnv/out/$dir
    [ -s $out/cnv_metrics.tsv.gz ] && { echo "exists $out"; exit 0; }
    /usr/bin/time -v $RS $C/l2/l2_infercnv.R cnv/inputs/$dir cnv/gene_order.tsv cnv/genes.txt $out ${NSLOTS:-8} ;;
  finalize) /usr/bin/time -v $PY $C/l2/l2_finalize.py --config $C/l2_config.yaml --run-root $R ;;
  *) echo "unknown step $step"; exit 2 ;;
esac
echo "STEP_DONE $step ${SGE_TASK_ID:-}"
