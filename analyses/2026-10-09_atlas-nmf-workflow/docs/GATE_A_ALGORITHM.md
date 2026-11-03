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

Current interface is defined in REVIEW_REVISION_A3.md. Both 06 and 07 require
the same reviewed cohort mapping. 06 creates final robust GEPs with unique IDs;
07 performs clustering only. The A1 interface is superseded. Consensus uses one
representative GEP per biological sample, not the former sample gene union.

Sensitivity thresholds 100/200/500 mean separate reruns of cohort-level robust
filtering and MP discovery after changing eligible samples. Per-sample NMF can be
reused when its cells and preprocessing are unchanged. Cell subsampling and
repeating NMF is a separate stability experiment, not implied by cohort filtering.

Tests use synthetic gene sets only. Passing tests establish these coded rules,
not biological validity, backend equivalence, scalability or approval for pilot.
