#!/bin/bash
# Fig. 1c Stage 0: cell-cycle list from Seurat, then gene sets + manifest. No CT2 input.
set -euo pipefail
umask 077
R=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1c_epi_states_20261011
A3A=/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1_ct2_A3_20261011
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
export R_LIBS="$ENV/lib/R/library:$ENV/lib/R/user-library:/home/zz950/softwares/R_lib_4:/home/zz950/softwares/miniconda3/envs/r4p3/lib/R/library"
PY=/home/zz950/softwares/miniconda3/envs/r4p3/bin/python
mkdir -p $R/private $R/stage0
"$ENV/bin/Rscript" -e 'suppressMessages(library(Seurat)); x <- Seurat::cc.genes.updated.2019;
  write.table(rbind(data.frame(phase="S", gene=x$s.genes), data.frame(phase="G2M", gene=x$g2m.genes)),
  commandArgs(TRUE)[1], sep="\t", quote=FALSE, row.names=FALSE)' $R/stage0/cc_genes_seurat_2019.tsv
$PY $R/code/fig1c_stage0.py \
  --a3a_genesets $A3A/private/genesets_A3a.private.tsv \
  --mzoughi $R/resources/mzoughi2025_tableS1f_hOnF_hStem.tsv \
  --holdout_extra $R/resources/holdout_tweak_fn14.txt \
  --stress $R/resources/stress_genes.txt \
  --ccgenes $R/stage0/cc_genes_seurat_2019.tsv \
  --counts_dir $A3A/export/counts \
  --out_dir $R/private
mv $R/private/stage0_manifest.json $R/stage0/stage0_manifest.json
