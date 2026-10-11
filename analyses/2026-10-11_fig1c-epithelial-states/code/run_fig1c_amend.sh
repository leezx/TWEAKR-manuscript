#!/bin/bash
# Fig. 1c amendment v0.3a (CT2-blinded). Usage: audit (SGE 1-13) | merge | phase1 (SGE 1-13) | gates
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1c_epi_states_20261011
A3A=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
O=$R/stage1_v03a
mkdir -p $O/audit $O/public
case "$1" in
  audit)  $PY $R/code/fig1c_lineage_audit.py study --task $SGE_TASK_ID --cells_dir $A3A/export/cells \
            --counts_dir $A3A/export/counts --axisl_dir $R/axisL/pred --out_dir $O/audit ;;
  merge)  $PY $R/code/fig1c_lineage_audit.py merge --model_dir $R/axisL/models --out_dir $O/audit --public_out $O/public ;;
  phase1) $PY $R/code/fig1c_stage1_sample.py --task $SGE_TASK_ID --cells_dir $A3A/export/cells --ucell_dir $R/ucell \
            --axisl_dir $R/axisL/pred --out_dir $O/phase1 --rule v03a --verdict $O/public/A_lineage_audit_verdict.tsv ;;
  gates)  $PY $R/code/fig1c_stage1_gates.py --root $R --phase1 stage1_v03a/phase1 \
            --summary_name stage1_v03a/stage1_gate_summary.json \
            --patient_meta /home/zz950/DATA/scRNAseq/meta_study/CRC_metadata_extraction/patient_characteristics/crc_patient_metadata.tsv \
            --public_out $O/public ;;
esac
