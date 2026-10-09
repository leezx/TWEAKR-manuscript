# Pre-execution review checklist

- [ ] Confirm whether the target population is malignant epithelial cells only
      or all epithelial cells for each dataset.
- [ ] Review the exact metadata column and accepted values for every RDS.
- [ ] Approve dataset aliases used to compare the v2 inventory with legacy NMF.
- [ ] Decide whether ranks 5-10 are required or whether the historical K=5 run
      should remain the primary analysis with other ranks as sensitivity.
- [ ] Confirm the minimum cell threshold and the handling of datasets whose
      samples all fall below it.
- [ ] Confirm whether each RDS is one sample or may contain multiple samples.
- [ ] Review assay/layer selection and counts integrity results.
- [ ] Review expected disk use before materializing preprocessed matrices.
- [ ] Confirm that metaprograms will be recomputed separately rather than
      silently projecting new factors onto the old 21 MPs.
- [ ] Keep `EXECUTE_NMF=0` until all items above are resolved.
