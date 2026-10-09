# Current pre-pilot checklist

Gate A PASS for algorithm commit 5babfed, per human fourth-round review.
See GATE_B_READINESS.md; older algorithm review requests are historical.

- [x] Core algorithm, K=4:9, post-QC >=200 cells and synthetic tests reviewed.
- [ ] Name the small pilot dataset/sample selection.
- [ ] Verify malignant epithelial annotation fields, values and evidence.
- [ ] Review canonical biological sample and patient mapping, including repeats.
- [ ] Record a scoped pilot execution decision after those checks.
- [x] Keep EXECUTE_NMF=0; no full-scale execution authorization.

Deferred until after pilot: multi-seed stability, 100/200/500 sensitivity,
real-data leave-one-dataset-out. These do not reopen Gate A.
