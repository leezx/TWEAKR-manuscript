#!/bin/bash
# A3b Stage S (limited GO after identity_v1 QA). Fig. 1b CytoTRACE2 pipeline reused unchanged
# (export_sample_counts.py; run_cytotrace2_sample.R modes whole,intrinsic; seed 14).
# Usage: run_a3b_ct2.sh prep | export main|np|pp | score <variant: main|np|pp> | ucell
set -eo pipefail
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
A=$R/A3b; C=$A/ct2
F=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_cytotrace2_20261009
H5=/home/zz950/DATA/scRNAseq/meta_study/CRC_single_cell_atlas_2025/data/final_crc_atlas-adata.count.only.h5ad
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
STUDIES=Chen_2024_Cancer_Cell,Joanito_2022_Nat_Genet,Khaliq_2022_Genome_Biol,Lee_2020_Nat_Genet,Li_2023_Cancer_Cell,MUI_Innsbruck,Pelka_2021_Cell,Qian_2020_Cell_Res,Qin_2023_Cell_Rep_Med,Uhlitz_2021_EMBO_Mol_Med
umask 077
case "$1" in
  prep)
    $PY $R/code/a3b_ct2_prep.py --root $A --h5ad $H5 \
      --screen-code /home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1b_dataset_screen_20261009/code ;;
  export)
    case "$2" in
      main) $PY $F/code/export_sample_counts.py --h5ad $H5 --cohort-cells $C/cells_all.tsv \
              --mapping $F/input_validation/cytotrace2_atlas_gene_mapping.tsv.gz --studies $STUDIES --out-dir $C/counts_main ;;
      np|pp) $PY $F/code/export_sample_counts.py --h5ad $H5 --cohort-cells $C/cells_$2.tsv \
              --mapping $F/input_validation/cytotrace2_atlas_gene_mapping.tsv.gz --studies $STUDIES \
              --depth-targets $C/targets_$2.csv --seeds 1,2,3,4,5 --out-dir $C/counts_ds_$2 ;;
    esac ;;
  score)
    export R_LIBS=/home/zz950/softwares/R_lib_4
    cdir=$C/counts_$([ "$2" = main ] && echo main || echo ds_$2); sdir=$C/scores_$2
    mkdir -p $sdir
    f=$(awk -F'\t' -v n=$((SGE_TASK_ID+1)) 'NR==n{print $5}' $cdir/export_manifest.tsv)
    [ -z "$f" ] && { echo "no task $SGE_TASK_ID"; exit 0; }
    out=$sdir/${f%.h5}.scores.tsv.gz
    [ -s "$out" ] && { echo "exists $out"; exit 0; }
    cd $F
    /home/zz950/softwares/miniconda3/envs/r4p3/bin/Rscript code/run_cytotrace2_sample.R $cdir/$f $cdir/cell_labels.tsv $out.tmp.gz 4 whole,intrinsic
    mv $out.tmp.gz $out ;;
  ucell)
    source /home/zz950/softwares/miniforge3/etc/profile.d/conda.sh
    ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
    conda activate "$ENV"
    export R_LIBS="$ENV/lib/R/library:$ENV/lib/R/user-library:/home/zz950/softwares/R_lib_4:/home/zz950/softwares/miniconda3/envs/r4p3/lib/R/library"
    export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
    mkdir -p $A/ucell
    tag=$(ls $A/export/counts | grep '\.epi\.h5$' | sort | sed 's/\.epi\.h5$//' | sed -n "${SGE_TASK_ID}p")
    [ -z "$tag" ] && { echo "no sample for task $SGE_TASK_ID"; exit 0; }
    [ -s $A/ucell/$tag.ucell.tsv.gz ] && { echo exists; exit 0; }
    "$ENV/bin/Rscript" $R/code/a3a_ucell.R $A/export/counts "$tag" $R/private/genesets_A3a.private.tsv $A/ucell/$tag.ucell.tsv.gz 2 epi ;;
  check)
    $PY $R/code/a3b_ct2_check.py --root $A --fig1b-scores $F/full/scores --public $A/public ;;
  estimands)
    $PY $R/code/a3b_estimands.py --root $A --fig1b-code $F/code --public $A/public ;;
esac
echo STEP_DONE a3b_ct2 "$@"
