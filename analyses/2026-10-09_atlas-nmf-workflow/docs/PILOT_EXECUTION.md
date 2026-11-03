# Scoped pilot authorized and submitted

Human explicitly authorized startup on 2026-10-09. Gate A PASS; Gate B feasibility
PASS with original study group=Cancer accepted provisionally. Malignant-cell
selection was based on the original study-provided Cancer annotation. The
underlying malignancy classification procedure could not be independently verified.

Scope: CRC23_tissue and CRC13_tissue only, K=4:9, seed 42, minimum 200 cells
after QC. No CNV rerun, no Epi pooling, no full Atlas authorization.
EXECUTE_NMF=1 is scoped inside run_scoped_pilot.sh; the general example guard
remains 0. SGE pvm 2 matches the user's qsub.standard.sh template.

Argos work/output root:
/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/nmf_pilot_GSE254249_20261009

Submission (from that root, after source /etc/profile):
```bash
/opt/sge/bin/lx-amd64/qsub -o pilot.qsub.log -e pilot.qsub.err analyses/2026-10-09_atlas-nmf-workflow/code/run_scoped_pilot.sh
```
Job ID: 3654435. Submission succeeded; completion is not yet claimed.
The runner records exact commands with set -x, hostname, timestamps and time -v
resource reports in logs/pilot.log. Outputs are prepared_manifest.tsv, tasks.tsv,
12 sample/rank NMF directories, validation.tsv, robust.tsv and MPs.json.
PILOT_COMPLETE is written only after all commands succeed. Empty robust/MP output
is possible in a two-sample feasibility pilot and must be reported, not forced.
