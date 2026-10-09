# Gate A algorithm implementation

Real-data execution remains HOLD_FOR_REVIEW.

The new `program_algorithms.py` and `07_discover_metaprograms.py` implement a
deterministic project variant: top50 overlap robustness followed by complete-link
agglomeration with every pair sharing at least 10 genes, retaining clusters with
at least two independent biological samples. The MP count is not fixed. This
is not claimed to reproduce Gavish's custom clustering or GeneNMF cosine clustering.

Consensus genes receive one vote per biological sample, irrespective of ranks
or repeated factors. Dataset support uses eligible biological samples from the
full approved cohort as denominator. Patient support uses globally harmonized
patient IDs; repeated timepoints from one patient count once for patient support.
Technical replicates must share a biological sample ID. A cohort mapping is
required; patient IDs are never inferred from filenames.

Input programs TSV fields: program_id, dataset_id, sample_id, patient_id, rank,
genes (50 harmonized gene IDs separated by |). Cohort TSV fields: dataset_id,
sample_id, patient_id. All programs must match the approved cohort.

The old task-based `06_filter_robust_programs.py` is retained as historical A1
code. Use the new cohort-aware entry point for MP discovery. Automated conversion
from existing task manifests to this harmonized contract remains pending mapping
review; it must not invent patient/sample identity.

Sensitivity thresholds 100/200/500 mean separate reruns of cohort-level robust
filtering and MP discovery after changing eligible samples. Per-sample NMF can be
reused when its cells and preprocessing are unchanged. Cell subsampling and
repeating NMF is a separate stability experiment, not implied by cohort filtering.

Tests use synthetic gene sets only. Passing tests establish these coded rules,
not biological validity, backend equivalence, scalability or approval for pilot.
