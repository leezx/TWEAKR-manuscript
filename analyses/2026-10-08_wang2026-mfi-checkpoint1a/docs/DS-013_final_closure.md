# DS-013 final closure — Wang 2026 maternal–fetal interface atlas

**Decision (user, 2026-10-08): DS-013 CLOSED — developmental context established; interaction
hypothesis unvalidated.** No further analysis, PR or contact with the authors. The analysis branch
`analysis/20261008-wang2026-mfi-checkpoint1a` and all of its results are kept as the archive.

## Final checkpoint status

| Checkpoint | Final status | Record |
|---|---|---|
| CP0 — Data provenance | PASS | `README.md`, `manifests/` |
| CP1A — Expression feasibility | PASS — Exploratory | `Checkpoint_1A_decision_memo.md` |
| CP1B — Genotype origin verification | NOT PURSUED | `author_request_email_draft.md` (archived, not sent) |
| CP1C — Spatial feasibility | NOT EVALUABLE WITH PUBLIC DATA | `Checkpoint_1C_spatial_feasibility.md` |
| CP1D — Macrophage signature validation | PASS WITH SPECIFICITY LIMITATIONS | `Checkpoint_1D_contract.md`, `Checkpoint_1D_results.md` |
| CP1E — CORE versus C1Q | PASS — C1Q association stronger | `Checkpoint_1E_core_vs_c1q.md` |
| Level 3 — Donor co-occurrence | NOT PURSUED | — |
| CP2 — Spatial colocalisation (Stereo-seq) | NOT PURSUED | — |

Level 3 was not run because donor-level co-occurrence would be non-spatial and was not expected
to raise the evidence level for a TWEAK–TWEAKR mechanism.

## Retained observations (developmental context only)

**Observation 1 — fetal trophoblast TNFRSF12A expression.** TNFRSF12A is reproducibly detected
in fetal-derived trophoblast populations at the human maternal–fetal interface, particularly
iEVTs (16.3% detection; 13/13 donors). Fetal origin rests on the authors' cell-type-level
annotation (Supp Table 13), not on per-cell genotype.

**Observation 2 — maternal macrophage TNFSF12-associated transcriptional state.** TNFSF12
detection in maternal macrophages is modestly associated with an independently derived
SPP1/TREM2/GPNMB/APOE transcriptional program, but a C1Q complement-related program shows a
stronger and more consistent association.

The two observations are kept **separate**. They must not be combined into a
macrophage–trophoblast interaction claim. There is no evidence that these macrophages colocalise
with TWEAKR+ EVT, and no evidence that TWEAK signalling mediates maternal–fetal immune tolerance.

## Wording guardrails

- *TNFSF12 detection is more strongly associated with a C1Q complement-related macrophage program
  than with the independently derived SPP1/TREM2/GPNMB/APOE-associated signature.*
- A stronger C1Q association does **not** show that C1Q is upstream of, or drives, TNFSF12
  expression. It may reflect macrophage differentiation, tissue adaptation or other shared
  regulation.
- CORE is an exploratory macrophage-state score, not a TWEAK-specific macrophage classifier.
- TNFRSF12A in fetal trophoblast does not show that TWEAKR is an oncofetal-specific receptor.
- The AOM/DSS Tnfsf12-associated signature transfers only partially and non-specifically to the
  human maternal–fetal interface.

## Manuscript use

- Not a stand-alone Figure 4 panel.
- Filed as a developmental reference analysis. Either observation may be cited if the manuscript
  later discusses TWEAKR in normal development alongside CRC plasticity.
- Resources return to direct mechanistic evidence for the TWEAKR–YAP–oncofetal state in CRC.
