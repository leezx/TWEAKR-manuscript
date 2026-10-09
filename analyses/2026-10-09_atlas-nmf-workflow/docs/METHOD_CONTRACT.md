# Method contract

## Analysis unit

The historical workflow factorized malignant cells separately within each
sample and then merged recurrent factors across samples. The refresh preserves
that analysis unit. Dataset identity is retained as provenance and as a hard
coverage requirement; cells from different datasets are not pooled into one
NMF matrix.

## Input contract

Each approved row in `dataset_plan.tsv` must identify:

- one Seurat RDS path under the approved counts-only root;
- one stable dataset ID;
- a sample column or the explicit sentinel `__all__`;
- an assay containing raw counts;
- a reviewed cell-state column and exact values defining eligible cells; and
- `review_status=approved` and `enabled=1`.

The workflow stops on duplicated cell names, duplicated feature names, missing
counts, negative counts, non-integer counts, missing metadata fields or empty
subsets. It does not infer malignancy from filenames or gene expression.

## Preprocessing contract

For a raw counts matrix `C` with genes in rows and cells in columns:

1. remove zero-library cells and report them;
2. compute `L = log1p(t(t(C) / colSums(C)) * 10000)`;
3. remove genes detected in fewer than `MIN_DETECTED_CELLS` cells;
4. compute each gene mean across all retained cells, including zeros;
5. compute `A[g,c] = max(L[g,c] - mean(L[g,]), 0)`; and
6. save `A` as a sparse, named gene-by-cell RDS matrix.

This is normalized, centred and non-negative data. It is neither raw counts nor
Seurat `scale.data`. The transformation matches the logic reconstructed from
the historical Atlas run and the TNBC workflow's centred non-negative input.

## NMF contract

- Backend: `RcppML::nmf`.
- Seed: 42 unless changed before approval.
- Tolerance: `1e-5`.
- L1 penalty: `c(0.01, 0.01)`.
- Proposed ranks: 5-10; final ranks remain a review decision.
- A rank is invalid when `rank > number of cells`.
- Each sample/rank writes W, H, factor assignments, reconstruction error,
  strict marker sets, tolerance-1/2 marker sets and top 50/100/200 lists.

Repeated top lists rank genes independently within every factor. Unique top
lists first assign each gene to the factor with its maximum loading and then
rank genes within that factor; a gene therefore cannot occur in two factors.

## Dataset coverage contract

Validation is performed against all approved dataset IDs, not only completed
output directories. Final validation fails if any approved dataset has:

- no prepared sample matrix;
- no successful NMF result;
- a missing approved rank without an explicit reviewed exception; or
- only skipped samples because the cell count is too small.

This prevents the historical failure mode in which very small samples or
missing annotations could silently reduce dataset representation.

## Metaprogram boundary

This PR prepares compatible per-sample factors and records the historical
metaprogram interface, but it does not automatically merge new factors into the
existing 21 MPs. Recomputing the metaprograms can change MP numbering and must
be a separate, explicitly reviewed analysis after per-dataset coverage passes.
