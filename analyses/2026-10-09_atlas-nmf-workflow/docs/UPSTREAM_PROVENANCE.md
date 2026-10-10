# Upstream provenance and historical fixes

## Upstream audit

Repository: `https://github.com/navinlabcode/tnbc-chemo`

Audited commit: `8b8e816a49881bd6a2cd6790a574fd331aa65ab4`

Relevant upstream files:

- `analysis/scripts/fastnmf.R`
- `analysis/scripts/metamodule.fnmf.wrapper.snk.py`
- `analysis/scripts/metamodule_fnmf.s1.R`
- `analysis/scripts/metamodule_fnmf.s2a.R`
- `analysis/scripts/metamodule_fnmf.s2c.R`
- `analysis/scripts/metamodule_fnmf.s2e.alt.R`
- `analysis/scripts/metamodule_fnmf.s3.R`
- `analysis/scripts/metamodule_cell_frequency.R`
- `analysis/cancer_cell_metaprogram.md`

No license file was present at the audited commit, so upstream source files are
not copied into this repository.

## Historical CRC Atlas run

The Argos run used a local upstream copy under
`CRC_single_cell_atlas_2025/tnbc-chemo-main/` plus project wrappers under
`CRC_single_cell_atlas_2025/NMF/`.

Verified local fixes included:

- preserving matrix row and column names during H5AD-to-RDS conversion;
- using the supported `readr::write_csv(..., file=...)` argument;
- guarding optional heatmaps and reconstruction-error calculation;
- avoiding a hard dependency on `ggpubr` in the per-sample runner;
- skipping a symbol-specific optional expression panel for Ensembl row names;
- reading SGE bucket tasks without allowing child processes to consume loop
  input; and
- parsing sample IDs from the right because sample names may contain
  underscores.

The legacy run used K=5 for the completed CRC batch (248 successful samples;
three epithelial samples had fewer than five cells). Upstream examples also
show rank sweeps. The proposed refresh exposes ranks as a reviewed parameter
instead of treating either choice as implicit.
