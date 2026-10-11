#!/bin/bash
# A3b Stage I steps 2b-5 (frozen contract A3b v0.3). Usage: run_a3b_stage1.sh tasks | tcalls | N (SGE array over studies) | identity | qa
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
A=$R/A3b
F=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
C=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1c_epi_states_20261011
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
export OMP_NUM_THREADS=${NSLOTS:-2} OPENBLAS_NUM_THREADS=${NSLOTS:-2} MKL_NUM_THREADS=${NSLOTS:-2}
S=(Chen_2024_Cancer_Cell Joanito_2022_Nat_Genet Khaliq_2022_Genome_Biol Lee_2020_Nat_Genet Li_2023_Cancer_Cell MUI_Innsbruck Pelka_2021_Cell Qian_2020_Cell_Res Qin_2023_Cell_Rep_Med Uhlitz_2021_EMBO_Mol_Med)
case "$1" in
  tasks)
    cat $A/export/cnv_inputs/*.patients.tsv | awk -F'\t' '$6=="True"{print $7}' | sort > $A/export/cnv_inputs/tasks.txt
    wc -l $A/export/cnv_inputs/tasks.txt ;;
  tcalls)
    $PY $R/code/a3b_cnv_calls.py --root $A --annotation $F/l2_annotation/final/annotation_v1.tsv.gz \
      --fig1b-patients $F/l2_annotation/light/malignancy_by_patient.csv --public $A/public ;;
  N)
    $PY $R/code/a3b_evidenceN.py --root $A --study ${S[$((SGE_TASK_ID-1))]} \
      --exclude $R/private/genesets_A3a.private.tsv $C/private/holdout_H.private.txt \
                $C/stage0/cc_genes_seurat_2019.tsv $C/resources/stress_genes.txt ;;
  identity)
    $PY $R/code/a3b_identity.py --root $A --fig1c-code $C/code --axisl-models $C/axisL/models ;;
  qa)
    $PY $R/code/a3b_identity_qa.py --root $A --samples $A/inputs/a3b_samples.tsv \
      --manifest $A/inputs/a3b_clinical_manifest.tsv --meta $A/inputs/sample_metadata.tsv \
      --commit $(cat $R/code/COMMIT_a3b) --public $A/public ;;
esac
echo STEP_DONE a3b_stage1 $1
