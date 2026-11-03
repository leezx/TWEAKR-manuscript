# Review response A4: input-matrix rank recurrence

HOLD_FOR_REVIEW remains in force. No real-data pilot or full analysis.

Within-input cross-rank recurrence now requires exact equality of
(dataset_id, source_id, sample_id), the identity of one prepared NMF matrix.
Different technical inputs cannot supply each other's 35-gene recurrence
evidence. This supersedes the biological-sample matching described in A3.

Only after this test passes are GEPs deduplicated by biological_sample_id.
Cross-sample recurrence still excludes the same biological_sample_id, and support
statistics still count independent biological samples and confirmed patients.
Technical libraries are currently decomposed separately, not silently pooled.
Any future counts pooling requires a separately reviewed preprocessing design.

The regression test has three assertions: internally unstable technical inputs
fail despite cross-source matching; a stable input survives without rescuing its
unstable technical replicate; different sample labels in one source cannot
cross-support ranks. Full Argos synthetic execution is recorded in A4_Argos_tests.log
with source SHA256 hashes. Invocation uses tests/run_argos_synthetic.sh and the
absolute argos-codex environment, as in A3.

Real cohort identity review, multi-seed stability and the cell-threshold
sensitivity driver remain pending; this patch does not claim to resolve them.
