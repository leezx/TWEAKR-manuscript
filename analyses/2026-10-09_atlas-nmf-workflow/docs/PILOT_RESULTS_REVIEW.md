# Two-sample NMF pilot: results for review

## Core result

The complete real-data pipeline ran successfully on both approved inputs,
including preprocessing, multi-rank NMF, output validation, robust GEP filtering
and MP clustering. This establishes feasibility, not biological validation or
authorization for full Atlas execution.

| Metric | Result |
|---|---|
| Dataset | GSE254249 |
| Samples | CRC23_tissue, CRC13_tissue |
| Original group=Cancer cells | 506, 514 |
| Ranks / seed | K4:9 / 42 |
| Raw GEPs | 39 per sample, 78 total |
| Completed NMF runs | 12/12 |
| Output validation failures | 0 |
| Robust GEPs | 11 total; CRC23=5, CRC13=6 |
| Pilot MPs | 5 |
| Supporting datasets | 1 only |

## MP QC summary

| Pilot ID | Member GEPs | Mean intra-MP Jaccard | Mean within-input cross-rank overlap (genes/50) |
|---|---:|---:|---:|
| M01 | 2 | 0.315789 | 44.00 |
| M02 | 3 | 0.128044 | 46.33 |
| M03 | 2 | 0.408451 | 45.50 |
| M04 | 2 | 0.694915 | 43.00 |
| M05 | 2 | 0.333333 | 45.50 |

All five MPs have support from two samples/two study-confirmed patients, but
only one dataset; cross_dataset_recurrent=false. These pilot M01-M05 labels
are local IDs, not the original Atlas M01-M21. No functional annotation or
oncofetal/CSC conclusion is asserted. M02 has substantially lower intra-MP
similarity and should not be interpreted as an established biological state.

## Execution and resources

Successful job3654441 ran on argos2, SGE pvm2, absolute argos-codex environment.
Log timestamps: 2026-10-09 21:17:06 to 21:18:44 UTC (98 seconds, excluding queue
and startup). Individual NMF processes took 4.67-10.14 seconds. Highest recorded
process RSS was 470620 KiB (~460 MiB); this is not aggregate scheduler memory.

Initial job3654435 failed before the first NMF completed because normalization
lost matrix dimnames. The fix explicitly restores dimnames; shell output paths
also strip CR. Both are in commit2620fba; no methodological parameter changed.
The first failure log remains on Argos as logs/pilot.first_failed.log.

Evidence committed here: PILOT_validation.tsv (12 tasks) and PILOT_run.log
(commands, timestamps, solver output and per-process time-v reports).
Exact input/commands and outputs are documented in PILOT_EXECUTION.md and the
scoped runner. Full GEP/gene consensus exports remain on Argos and are omitted
from this public review packet pending explicit approval of that payload.

Remote output root:
`/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_pilot_GSE254249_20261009/`

## Limits and decision requested

Malignant-cell selection was based on the original study-provided Cancer
annotation. The underlying malignancy classification procedure could not be
independently verified. Epi cells were excluded; no new CNV inference was run.
Multi-seed stability, 100/200/500 sensitivity, real leave-one-dataset-out and
full-cohort malignancy harmonization are not completed. RcppML is not claimed
equivalent to original Gavish NMF/snMF; successful exit/output validation alone
does not independently prove optimizer convergence or biological reproducibility.

Request review of pilot feasibility and output/QC evidence. Full Atlas execution
remains NOT AUTHORIZED; do not expand automatically from this successful pilot.
