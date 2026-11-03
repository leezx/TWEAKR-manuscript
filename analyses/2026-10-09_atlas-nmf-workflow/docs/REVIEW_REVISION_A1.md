# Revision A1: rank, eligibility and robust programs

Status: HOLD_FOR_REVIEW. No real dataset analysis has started.

- Primary ranks: K=4:9, yielding 39 raw factors per sample. K is the number
  of factors in one decomposition, never the final MP count.
- Primary eligibility: at least 200 high-confidence malignant epithelial cells
  per independent biological tumor/sample. Sensitivity thresholds: 100/200/500.
  These cell thresholds are project choices, not claims about Gavish's methods.
- Normal epithelium and stroma are excluded from the malignant primary analysis.
  EPCAM alone cannot establish malignancy. Counts assay, species/gene IDs,
  sample/timepoint/technical-batch mappings must be reviewed before execution.
- Robust filtering uses repeated top50 genes: >=35 shared genes across different
  ranks within a sample, >=10 shared genes with another sample's rank-stable
  program, and greedy within-sample pruning retaining overlap <=10 genes.
  `06_filter_robust_programs.py` implements this declared variant and reports
  cross-dataset support. It has not been validated on biological data.
- Cross-rank recurrence explicitly excludes same-rank matches, a refinement
  to the upstream function's unrestricted within-sample comparison.
- Existing runner is RcppML, not multiNMF or getMetaPrograms. Author README uses
  NMF::nmf(rank=4:9, method='snmf/r', nrun=10). RcppML seed=42 is not equivalent.
- The preprocessing retains the historical TNBC-style centered nonnegative
  input; it is not yet established as Gavish's identical normalization/HVG
  selection. Gene selection and backend equivalence remain review questions.
- MP clustering is NOT implemented in this PR. Robust programs are intermediate
  outputs. Final MP count is data-driven, not fixed at 21 or chosen from K.
- Subsequent MP discovery must report supporting tumors, patients and datasets,
  rank stability, mean similarity and top50 consensus genes. Patient support
  requires a verified patient mapping; it cannot be inferred from sample names.

Primary sources inspected:
https://github.com/tiroshlab/3ca/blob/main/ITH_hallmarks/README.md
https://github.com/tiroshlab/3ca/blob/main/ITH_hallmarks/Generating_MPs/robust_nmf_programs.R

For review access, a local PR diff is exported alongside this working checkout;
GitHub private-repository access is required to view PR #1.
