# Worklog — TWEAKR-manuscript

Chronological log of everything done on this project: **what** was done,
**why**, and **how**. Updated continuously during work, not just at the end.

Convention (fixed on day 1, do not switch): **newest entry at the bottom.**
Past entries are not edited except to fix a factual error — this is a log,
not a living doc. The current-state summary lives in `docs/PROJECT_SUMMARY.md`
(once created); this file is the history.

## Progress tracker

| Step | Status | Notes |
|---|---|---|
| 0. Repo scaffold | done | directory architecture created 2026-09-10 |
| 0b. git init + GitHub repo | done | private repo leezx/TWEAKR-manuscript, pushed 2026-09-10 |
| 0c. Article framework from GPT/ drafts | done | manuscript.md + Figure1-5.md + 6 supp, framework/placeholder only |
| 1. Fill panel images (user, one at a time) | in progress | user-driven |
| 2. Write Results/Intro/Discussion prose from real analysis output | not started | |
| 3. Methods (STAR) from ../TWEAKR-OncoPlacental scripts/results | not started | |
| 4. Figure finalization (print specs, final legends) | not started | |
| 5. References + submission package | not started | |

Overall: framework in place; all scientific claims still placeholders.

---

## 2026-09-10 — Session 1: initial exploration & project setup

**What**: Read the `TWEAKR-manuscript/` working directory and surveyed the
related analysis project `../TWEAKR-OncoPlacental/`. Started a brainstorming
pass to scope "assemble the figures into a submittable paper." Created this
Worklog at the user's request.

**Why**: The manuscript project has no content yet — only `_TEMPLATE`
scaffolding files were copied in. Need to understand where the figures and
scientific results live before designing the repo structure or drafting.

**How**:
- `ls` / `find` on `TWEAKR-manuscript/` — contains only templates:
  `PROJECT_CHARTER_TEMPLATE.md`, `PROJECT_SUMMARY_TEMPLATE.md`,
  `README_TEMPLATE.md`, `STEP_DESIGN_TEMPLATE.md`, `WORKLOG_TEMPLATE.md`,
  `gitignore_template`. No `.git`, no figures, no manuscript.
- Surveyed siblings under `../` (`TWEAKR-OncoPlacental`, `RA-Figure-Skeleton`,
  `CRC-Atlas`, `ArticleBlueprintOS`, etc.).
- `TWEAKR-OncoPlacental` is the analysis project: TNFRSF12A / TWEAKR as an
  oncofetal–oncoplacental ADC target. 9 analysis steps under `results/`
  (01_inventory → 02_gene_id_mapping → 03_pseudobulk_prep → 04_dfp_signature
  → 04a_dfp_gut → 05_tier2_validation → 06_crc_projection → 06a_normal_context
  → 07_clim_external_data → 08_clim_scrna_scoring → 09_developmental_ternary),
  plus matching `scripts/` and `docs/STEP*` design/results docs.
- Figure-asset scan of `TWEAKR-OncoPlacental`: only **3 rendered figure files**
  exist —
  `results/09_developmental_ternary/ternary_track_{A_gut_specific,B_pantissue,C_hcl}.png`.
  Everything else in `results/` is tables, gene lists, and audit `.md` docs.
  `notebooks/` is empty (`.gitkeep` only).

**Real findings**:
- The figures to be "assembled" largely **do not exist as files yet** in the
  analysis repo. Open question put to the user: are they to be generated from
  the results tables/scripts, or do they live somewhere else (local folder,
  slide deck, cloud)?
- No git repo initialized in `TWEAKR-manuscript/` yet.

**Review**: n/a (setup only).

**Next**: await user answer on figure source; then classify repo scaffold vs.
full manuscript-pipeline scope and present a design before creating anything.

## 2026-09-10 — Session 1: directory architecture scaffolded

**What**: Created the manuscript repo's directory architecture per the user's
spec. Markdown throughout; Cell/Nature/Science structure and figure conventions.

**Why**: User instruction — "先把目录架构建起来" (build the directory
architecture first), before sourcing figures or drafting.

**How** — structure decided with the user via 3 questions:
- Supplementary figure legends: **separate `FigSN.md` per supp figure**, filed
  in the related main figure's folder.
- Scope now: **`Figure1` built fully as the canonical template**; other figures
  copied from it once the outline is fixed.
- Extra top-level files: **all four** — `README.md`, `references.bib`,
  `supplementary.md`, `Tables/`.

Files created:
- `README.md` — layout table + figure/table naming conventions.
- `manuscript.md` — main-text skeleton: Title, Short title, Authors, Abstract,
  Introduction, Results (4 placeholder subsections), Discussion + "Limitations
  of the study", Resource availability, Acknowledgments, Author contributions,
  Declaration of interests, Figure legends index, References.
- `method.md` — STAR Methods skeleton: key resources table, resource
  availability (lead contact / materials / data & code), experimental model,
  method details (4 analysis-step placeholders keyed to `../TWEAKR-OncoPlacental`
  scripts/results), quantification & statistical analysis, additional resources.
- `supplementary.md` — supplementary text skeleton + indices of supp figures
  and supp tables.
- `references.bib` — BibTeX stub, `[@key]` citation convention noted.
- `Figures/Figure1.md` — canonical figure template: number+title, key point,
  per-panel legend with image links (`Figure1/Fig1a.png` …), full submission-form
  legend, source pointer, related-supp list.
- `Figures/Figure1/FigS1.md` — canonical supp-figure template ("Figure S1 …
  Related to Figure 1"), panels link to `FigS1/FigS1a.png` …
- `Figures/Figure1/FigS1/.gitkeep` — panel image subfolder.
- `Tables/Table1.md`, `Tables/TableS1.md` — canonical main / supp table templates.

Naming conventions locked in: main panels `Fig<N><letter>.png`; supp panels
`FigS<N><letter>.png`; supp figures numbered **globally** but filed under the
related main figure; large table data → `Tables/Table<N>/` folder.

**Real findings**:
- Leftover `_TEMPLATE` files still present at repo root
  (`PROJECT_CHARTER_TEMPLATE.md`, `PROJECT_SUMMARY_TEMPLATE.md`,
  `README_TEMPLATE.md`, `STEP_DESIGN_TEMPLATE.md`, `WORKLOG_TEMPLATE.md`,
  `gitignore_template`) — not yet removed; asked user whether to delete or keep.
- No `.git` yet; GitHub repo not created — blocked on name/visibility/account.

**Review**: n/a.

**Next**: (1) user decision on leftover template files; (2) `git init` +
`.gitignore` + create GitHub repo once repo name/visibility/account given;
(3) resume figure-source question to start Step 1.

## 2026-09-10 — Session 1: git init + private GitHub repo

**What**: Initialized git, made the first commit, created a **private** GitHub
repo `leezx/TWEAKR-manuscript` and pushed `main`.

**Why**: User instruction — "新建这个Github仓库" then "把这个Github改为私有".

**How**:
- `gh auth` active account: **leezx** (scopes: repo, workflow, read:org, gist).
- Wrote `.gitignore` adapted from `gitignore_template`: keeps figure panels
  (`.png/.pdf/.svg/.eps`) tracked — this is a manuscript repo — and ignores
  only large raw-data/binary formats, OS/editor cruft, and LaTeX build artefacts.
- `git init -b main`; `git add -A`; one commit
  (`1da4ba6`, Co-Authored-By Claude Sonnet 5).
- `gh repo create leezx/TWEAKR-manuscript --private --source=. --remote=origin --push`.
- Verified: `visibility = PRIVATE`, url https://github.com/leezx/TWEAKR-manuscript.

**Real findings**:
- Between the scaffold step and this commit, the **user added new files** to the
  working tree; they were picked up by `git add -A` and are now in the first
  commit:
  - `GPT/Figure1.md … Figure5.md` + `GPT/note.md` — draft figure plans and the
    paper's 5-figure narrative arc:
    F1 "What is the state?" (unbiased discovery + external validation + disease
    evolution); F2 "Why does the state matter?" (poor outcome + chemo/ICI
    persistence); F3 "What maintains it?" (TWEAKR + TAM-derived TWEAK + spatial
    niche); F4 "Is the axis causal?" (public perturbation + TNFSF12 stim +
    TNFRSF12A KO/RNA-seq); F5 "Does it operate in vivo?" (xenograft scRNA /
    state remodeling).
  - `Figures/Figure1/Note.md` — a note addressed to "Codex" about extracting
    meta from scRNA-seq datasets on the Argos cluster
    (`DATA/scRNAseq/…`, `projects/TWEAKR/{chemotherapy,Immune}`) into
    `DATA/scRNAseq/meta_study/` and plotting a cohort-overview figure. This is a
    data task for a different agent/environment, not the manuscript repo itself.
  - Example images: `Figures/Figure1/{Example.F1.large.jpg, example.MP.png}`,
    `Figures/Figure1/FigS1/FigS1a.jpg`.
- Now TWO figure structures exist in the repo: my `Figures/FigureN.md` +
  `FigureN/` scaffold, and the user's `GPT/FigureN.md` drafts. These need to be
  reconciled (Step 0c) — likely fold the GPT/ content into `Figures/FigureN.md`
  and keep one structure.
- Leftover `_TEMPLATE` files still at repo root and now committed; still pending
  user decision on deletion.

**Review**: n/a.

**Next**: (1) read `GPT/Figure1-5.md`, reconcile with `Figures/` scaffold —
one canonical structure; (2) user decision on leftover `_TEMPLATE` files;
(3) figure-source question / Step 1 figure inventory.

## 2026-09-10 — Session 1: article framework built from GPT/ drafts

**What**: Read `GPT/Figure1.md`–`Figure5.md` (+ `GPT/note.md`) and built the
manuscript framework — text + image placeholders only, no fabricated results.

**Why**: User instruction — read the GPT figure frameworks/panels and stand up
the article skeleton; user will fill panel images one at a time; do text +
image placeholders first.

**How**:
- `GPT/*.md` are ChatGPT advisory transcripts; each ends with a locked panel
  list and a conditional title. Extracted those into the repo's figure files.
- 5-figure narrative arc (from `GPT/note.md`): F1 what is the state · F2 why it
  matters · F3 what maintains it · F4 is it causal · F5 does it work in vivo.
- Wrote `Figures/Figure1.md`–`Figure5.md`: per figure — number+title (F2/F3
  titles flagged conditional), key point, per-panel section (`### Figure NX.`)
  with a placeholder image link `![…](FigureN/FigNx.png)`, an "_Image pending_"
  line, a bracketed **Legend (draft)** carrying the intended claim from the GPT
  doc, an analysis/data-source pointer, a submission-form full-legend stub,
  related-supp list, and a link back to `../GPT/FigureN.md`.
  Panel counts: F1 A–H (H optional), F2 A–G, F3 A–G, F4 A–G (G optional),
  F5 A–F.
- Wrote 6 supplementary figure files (framework only):
  `Figure1/FigS1.md` Atlas construction & metadata; `FigS2.md` Robustness of the
  oncofetal MP; `FigS3.md` Cross-validation & negative controls; `FigS4.md`
  Pan-cancer extension (optional); `Figure4/FigS5.md` Immune-modulatory
  transcriptional phenotype (claim ceiling: phenotype, NOT immune evasion);
  `Figure4/FigS6.md` Placental/trophoblast convergence (exploratory; has an
  explicit delete stop-rule).
- Created panel folders `Figures/Figure2..5/`, `Figure1/FigS2..S4/`,
  `Figure4/FigS5..S6/` (each with `.gitkeep`).
- Rewrote `manuscript.md`: title options (to be fixed once F2G/F3 land), abstract
  skeleton keyed to the 5 figures, 4-paragraph Introduction skeleton, Results
  with 5 declarative-sentence subsections (one per figure, each a bracketed
  paragraph with panel callouts), Discussion + "Limitations of the study",
  front/back matter, a figure-legends index table, references pointer.
- Rewrote `supplementary.md`: supplementary-note stubs + provisional index tables
  for the 6 supp figures and supp tables.

**Real findings**:
- User is adding direction notes into the tree as we go:
  `Figures/Figure4/note.md` now points at the perturbation RNA-seq and
  TEAD/YAP1 ChIP-seq working dirs under
  `DATA/2.PROJECTS/1.TWEAKR-oncoFetal/data/external/{Perturbation,TEAD_YAP1_ChIPseq}`
  — inputs for Figure 4A / Figure S5D.
- `Figures/Figure1/Note.md` (user's) points at CRC-atlas meta extraction on the
  Argos cluster — inputs for Figure 1A / Figure S1.
- No scientific numbers written anywhere; every claim is bracketed placeholder.
- Conditional-title flags recorded in-file: F2 keeps "TWEAKR-associated" only if
  Panel 2G holds; F3 title stays at "nominate" (not "drives").

**Review**: n/a.

**Next**: user fills panel PNGs into `Figures/FigureN/`. Then, per figure, write
the Results paragraph and legend from the actual analysis output in
`../TWEAKR-OncoPlacental` / the DATA working dirs; build `references.bib`;
draft Methods. Still pending: user decision on deleting root `_TEMPLATE` files
and on whether to keep `GPT/` in-repo.

## 2026-10-08 — Wang 2026 MFI Checkpoint 1A: TNFSF12/TNFRSF12A expression feasibility

**What**: First analysis folder under the new policy:
`analyses/2026-10-08_wang2026-mfi-checkpoint1a/` on branch
`analysis/20261008-wang2026-mfi-checkpoint1a`.

**Why**: User split Checkpoint 1 into 1A (expression feasibility, unblocked) and
1B (genotype origin, blocked pending author request).

**How**: QC showed the public X = log1p(raw counts) without normalisation, so
CP10k was reconstructed. Author cell-type-level origin came from Supp Table 13
(FB and pvSMC mixed; GC and Ery ambiguous). The analysis produced cell-type,
donor and trimester summaries, within-donor Wilcoxon contrasts and two Nature-style DotPlots.

**Validation**: Independent anndata re-extraction matched. Coverage assertion
covers 36 types and 193,202 nuclei. Fonts are editable and embedded; TIFF is 600 dpi.

Added library-size QC, a depth-matched detection sensitivity analysis, a sign test
and trimester-split direction counts. Renamed the level metric to `mean_log1p_cp10k`
and added `pseudobulk_cp10k`.

**Decision**: Human review — CP1A EXPLORATORY / PASS WITH LIMITATIONS. CP1B BLOCKED
(author request drafted to the corresponding authors, not sent). CP1C spatial assay
feasibility next. CP2 HOLD.

**Next**: CP1C metadata/gene-detection check; send the author email after the user
verifies it; merge to main is not authorised.

## 2026-10-08 — Wang 2026 MFI Checkpoint 1C: Stereo-seq assay feasibility

**What**: Metadata and gene-detection feasibility check of the public COSMOS
Stereo-seq explorer (no matrix download, no spatial statistics). Script
`analyses/2026-10-08_wang2026-mfi-checkpoint1a/code/cp1c_spatial_feasibility.py`.

**Result**: Explorer values are transformed, not counts (about 1% integer; 14.9% of
cells consistent with log-normalised counts; CD163 31% and PECAM1 68% nonzero),
so they cannot give detection rates. `STOMICS.h5ad` returns 404, and the Box link
holds only CODEX. Immune cells are pooled with no macrophage label. EVT subtypes,
mVEC/fVEC and stromal types are resolved. Coordinates, annotation and sample ID are
complete for 1,077,690 cells in 16 sections (GW18–24 only).

**Decision**: Proposed NOT EVALUABLE WITH PUBLIC DATA (pending review); CP2 HOLD.

## 2026-10-08 — Wang 2026 MFI (DS-013) closed

**Decision**: CP1A PASS (exploratory expression evidence); CP1C PASS — not
evaluable for spatial interaction with accessible public data; CP1B and CP2 not
pursued. DS-013 CLOSED as an exploratory developmental reference. The author
request is archived and was not sent. The branch is kept without a PR.

**Retained observation**: TNFRSF12A is reproducibly expressed in fetal-derived
extravillous trophoblast populations (iEVT), with origin based on the authors'
cell-type-level classification. Not a standalone Figure 4 panel.

## 2026-10-08 — Wang 2026 MFI Checkpoint 1D: TWEAK-associated macrophage state (scoped reopening)

**What**: snRNA-only analysis, pre-registered in `docs/Checkpoint_1D_contract.md`. Scored the
AOM/DSS Tnfsf12+ TAM core/extended programs plus control modules in maternal decidual
macrophages, with TNFSF12 as an independent readout.

**Result**: CORE meets all pre-specified PASS criteria: MH OR 1.43, 12/14 donors, OR/SD 1.29,
beats the matched-random null (p = 0.002), survives lysosomal adjustment and the CD14_M-only
check. The effect is modest (2.7% vs 1.9% detection). A C1Q complement control module is
equally associated, so the state is not TWEAK-specific. HB shows no association.

**Decision**: Proposed PASS with a specificity caveat. Level 3 is not started; Stereo-seq untouched.

## 2026-10-08 — Wang 2026 MFI CP1D review and CP1E (CORE vs C1Q)

**Decision**: CP1D PASS WITH SPECIFICITY LIMITATIONS; Level 3 HOLD. CORE is the primary
signature and C1Q the comparator; they are not merged.

**CP1E** (assembled from already-fitted models; no rerun): in M3, CORE 1.21 (1.04–1.41) and
C1Q 1.38 (1.22–1.57). In CD14_M only, CORE 1.18 (0.99–1.40) and C1Q 1.36. Score correlation is
r = 0.22 (VIF 1.05). CORE adds modest information beyond C1Q that is not robust in CD14_M.
CORE is an exploratory state score, not a TWEAK+ classifier.

## 2026-10-08 — Wang 2026 MFI (DS-013) final closure

**Decision**: CP1E PASS — C1Q association stronger. DS-013 CLOSED — developmental context
established; interaction hypothesis unvalidated. Level 3 (donor co-occurrence) and CP2
(Stereo-seq) NOT PURSUED. No PR, no author contact; branch and results kept as the archive.

**Retained** (two separate observations, not an interaction claim): TNFRSF12A in fetal-derived
trophoblast, particularly iEVT (16.3%, 13/13 donors; author cell-type-level origin); TNFSF12
detection in maternal macrophages is modestly associated with the SPP1/TREM2/GPNMB/APOE program
and more strongly with a C1Q complement program. A stronger C1Q association does not make C1Q
upstream of TNFSF12. Not a Figure 4 panel. Record: `analyses/2026-10-08_wang2026-mfi-checkpoint1a/docs/DS-013_final_closure.md`.
## 2026-10-09 — Atlas NMF workflow packaged for review; analysis held

**What**: Added `analyses/2026-10-09_atlas-nmf-workflow/` as a lightweight,
reviewable implementation of the CRC Atlas per-sample NMF workflow. No new
Atlas object was analysed and no SGE job was submitted.

**Why**: The updated counts-only Seurat RDS inventory on Argos contains
candidate datasets that may not be represented in the historical NMF run. The
user requested that the workflow be committed and reviewed before any new NMF
analysis, with every approved dataset required to have its own result.

**How**:

- recorded the new RDS root, legacy NMF root, proposed heavy output root and
  absolute `argos-codex` environment in a path manifest;
- audited the historical Atlas scripts and the upstream
  `navinlabcode/tnbc-chemo` workflow at commit
  `8b8e816a49881bd6a2cd6790a574fd331aa65ab4`;
- implemented read-only Seurat inventory and legacy-coverage comparison;
- implemented sparse raw-count preprocessing: library-size normalization,
  `log1p`, gene-wise centring and negative truncation;
- implemented deterministic `RcppML` NMF with strict/tolerant marker sets and
  repeated plus non-redundant top 50/100/200 gene lists;
- added guarded SGE array wrappers that require `EXECUTE_NMF=1` after review;
- added hard validation requiring every approved dataset at every approved rank
  to have at least one complete NMF result; and
- documented method assumptions, provenance, review decisions and claim ceiling.

**Validation**: Python unit tests, Python compilation, Bash syntax checks, R
parse checks and a synthetic 40-gene by 24-cell rank-3 NMF smoke test passed.
The synthetic test is software QA only and is not biological analysis.

**Limitations**: Dataset aliases, malignant/epithelial metadata values, final
rank range, minimum cells and disk estimate remain intentionally unresolved.
The workflow is `HOLD_FOR_REVIEW`; the new RDS directory has not been inventoried
by this task. Recomputing or updating the existing 21 metaprograms is outside
this PR and requires a separate review.

## 2026-10-09 — NMF review revision A1

Primary ranks changed to 4:9 and minimum cells to 200, with 100/200/500
sensitivity thresholds. Added an explicit robust-program filtering variant
using repeated top50 genes (35 within-rank, 10 across-sample, <=10 redundancy)
and cross-dataset support. Documented RcppML versus author NMF/snMF nrun=10
differences and that MP clustering remains unimplemented. Analysis stays HOLD.

## 2026-10-09 — Argos synthetic Gate A tests

Added cohort-aware program algorithms, deterministic complete-link MP clustering,
sample-vote consensus and dataset/patient/sample support summaries. Six tests
passed in argos-codex on Argos. See GATE_A_ALGORITHM.md and GATE_A_TEST_REPORT.md.
Real-data execution remains HOLD pending independent review; no pilot launched.

## 2026-10-09 — Actual-code review response A3

Repaired the 06-to-07 interface and removed duplicate robust filtering. Added
explicit cohort identity validation, canonical biological sample keys, confirmed
patient counts and separately reported unknown patient samples. Consensus now
selects one representative GEP per biological sample. Preprocessing checks finite
counts/parameters and applies the cell threshold after zero-library removal;
__all__ requires a reviewed single-sample assertion. Argos ran 12 Python tests
plus the R synthetic preprocessing test successfully; raw output and code hashes
are in docs/A3_Argos_tests.log. Multi-seed and cell-threshold sensitivity drivers
remain pending. Real Atlas analysis remains HOLD_FOR_REVIEW.

## 2026-10-09 — Review response A4

Restricted cross-rank recurrence to the exact input identity
(dataset_id, source_id, sample_id). Biological sample IDs are used only for
subsequent deduplication and independent support, not to let technical libraries
rescue each other's instability. Added a regression test for cross-source and
cross-sample-label evidence leakage. Argos raw validation is preserved in
docs/A4_Argos_tests.log. No real cohort mapping or Atlas analysis was run.

## 2026-10-09 — Gate A approved by human reviewer

Human review of 5babfed concludes Gate A PASS and closes core algorithm review.
Proceed to Gate B preparation only: pilot dataset annotations and identity
mapping must first be checked. EXECUTE_NMF remains 0; no real-data execution or
PR merge was performed. Multi-seed, cell-threshold sensitivity and real-data
leave-one-dataset-out are deferred validation, not Gate A blockers.

## 2026-10-09 — Gate B read-only pilot inventory

Inspected actual GSE254249 RDS candidates CRC23_tissue and CRC13_tissue: RNA
counts valid, source group=Cancer yields 506 and 514 nonzero-library cells.
Sample/PatientID/Tissue/TimePoint agree with source metadata. Added candidate
inventory and identity mapping for review only; original Cancer-calling evidence
and cross-study duplicate review remain pending. No preprocessing or NMF run.

## 2026-10-09 — Malignant annotation provenance access check

Human review accepts pilot inventory and identity mapping. Attempted primary
paper methods verification; publisher access returned 403 and search indexing
did not establish the Cancer definition. Recorded unresolved status in
MALIGNANT_PROVENANCE_CHECK.md. No claim of CNV-confirmed malignancy, no algorithm
change, no dataset expansion, EXECUTE_NMF remains 0.

## 2026-10-09 — Human-authorized two-sample pilot submitted

User authorized startup; scoped runner uses original group=Cancer only, two
approved samples, K4:9 and seed42. Submitted SGE job3654435 with pvm2 standard
resources. Root and commands are in PILOT_EXECUTION.md. General execution guard
remains 0; no full Atlas run is authorized. Completion/QC remain pending.

## 2026-10-09 — Pilot first failure and retry

Job3654435 prepared both inputs but failed on first NMF: sparse multiplication
lost dimnames. Restored dimnames explicitly and added regression assertions.
Shell task reader now strips trailing CR from output paths. Original failure log
preserved as logs/pilot.first_failed.log. Retried identical scope as job3654441;
completion still pending. No changes to algorithm parameters or sample selection.

## 2026-10-09 — Pilot completed, results submitted for review

Job3654441 completed all12 runs with zero output validation failures. 78 raw
GEPs yielded11 robust GEPs and5 pilot MPs, all from one dataset. Runtime98s,
maximum recorded processRSS470620KiB. Added PILOT_RESULTS_REVIEW.md, validation
table and raw run log. Full gene tables remain on Argos; no biological claims
or full Atlas execution approval inferred. Original annotation limits retained.

## 2026-10-09 — Full preparation first inventory checkpoint

Recorded human pilot PASS. Read-only audit of updated RDS manifests found7
datasets/333 objects/2171819 cells. Four sources lack cell-level annotations
in the build; two have Epi labels needing malignant adjudication; GSE254249
separates Cancer/Epi. Dataset-level summaries committed; disabled identity draft
stays remote. Complete legacy Atlas reconciliation and mapping review pending.
No full execution or algorithm optimization.

## 2026-10-09 — Sample preparation checkpoint

Source metadata identifies26 GSE254249 Cancer and27 GSE236581 c91_Epi_Tumor
candidate inputs with >=200 annotated cells. Source PatientID/Patient retained
remotely; no guessed or approved identities. BioProject evidence links two
datasets to legacy names, with exact sample matching and W-file checks kept
separate from full QC/biological identity review. Existing downloaded annotations
are missing in four cohorts; no CNV or NMF was launched. Final gate remains open.

## 2026-10-09 — Actual53-input QC and historical correction

All53 actual RDS passed counts/source/sample/post-zero-library QC:27
GSE236581 with20412 target cells and26 GSE254249 with28645; zero libraries0.
Public QC excludes patient identifiers/paths; full mapping remains Argos.
Truncated historical manifest superseded by real task master:21 name-candidate
matches with K5 required files;32 unmatched/unverified. Biological crosswalk
and reuse unresolved. All53 pending/enabled0; no NMF/CNV or algorithm changes.

## 2026-10-09 — Identity and historical artifact review

Accepted human53-sample QC PASS; no rerun. Source identity crosswalk yields39
study-local patient groups as aggregate only; full crosswalk stays private. Four N samples
have explicit Tissue=Normal, held for annotation review. Read21 historical K5
artifacts: all readable/finite/nonnegative/dimensions consistent; CRC02-T-I
has absent gene/cell names and empty markers. Historical cell counts differ
from current in21/21; regex vs exact selectors not established equivalent.
No reuse approval or new NMF. Publisher annotation definition still unverified.

## 2026-10-09 — Public/private separation approved

Human decision prohibits public anonymous patient linkage. Removed the unpushed
crosswalk commit from the publication branch and replaced it with a status-only
53-sample table. Four Normal samples not approved;49 require final review;
21 old K5 outputs not approved for direct reuse. All enabled0/EXECUTE_NMF0.
No patient IDs, grouping aliases, per-patient sample counts or biological identity
keys in the new public table. Full crosswalk stays on Argos; no QC rerun.

## 2026-10-09 — Source SOFT and limited privacy assessment

Read original SOFT: all53 have unique source-record candidate matches. Private
join retained mode600, public status contains no linkage. Unique records do not
prove technical independence. Original c91 method still inaccessible403. Old
pilot study codes came from author-public metadata; published history remains
OPEN pending governance assessment, no rewrite. Freeze21 old K5 direct reuse
not approved/32 coverage unresolved. No repeated QC or analysis, execution0.

## 2026-10-09 — Final eligibility proposal

Metadata-only check of all92 GSE254249 source IDs:26 candidates have one
patient/tissue/timepoint tuple and no other source sample shares it. Reasonable
duplication check, not proof of absent unrecorded replication. Propose26 approved
with original Cancer annotation limitation,23 c91 pending,4 Normal not approved.
Public evidence excludes patient linkage; final review pending, all execution0.

## 2026-11-03 — B32 立项：Fn14 结构坐标冻结与 Fig. TR1（WL-20261103-FN14-001）

**做了什么。** 用户决定把 `UDE/TWEAKR-AF3.md`（GPT 的 TWEAKR 结构/信号转导方案）立为 UDE
分支 **B32**（新主干 T8）。立项前先把方案依赖的结构事实逐条核实，再据此建图。

**为什么。** 该方案的数字和文献引用没经过核对就要被用作建模与制图依据。核实发现两处错误
（见下），说明这一步不能跳。

**核实（向权威库取回，非转述）。**
- UniProt Q9NP84：SIGNAL 1–27 · CHAIN 28–129（102 aa）· 胞外 28–80（53）·
  TRANSMEM 81–101（21，helical）· 胞内 102–129（28）· REPEAT 36–67「TNFR-Cys; atypical」·
  DISULFID 36–49/52–67/55–64 · 无 CARBOHYD。小鼠 Q9CR75 边界相同。
- 脚本硬编码的 129 aa 与 UniProt FASTA **逐字符一致**。这步必做：脚本自检是拿序列验位点，
  序列若抄错，自检会在错序列上全部通过。
- D45/K48/M50/D62 身份正确且全在 CRD 内；CRD 内六个 Cys 位置为 36/49/52/55/64/67。

**更正两处既有记录错误（已在 `UDE/TWEAKR-AF3.md` 内标注）。**
1. **2KN1 不是 Fn14。** PDBe 条目标题为 "Solution NMR Structure of BCMA"。只用 2KMZ（hFn14）
   和 2KN0（xFn14）。
2. **TM = 21 aa 来自 UniProt，不是 Winkles 2008。** 该综述给 129/102/53/28，未给 TM 长度；
   其讨论的 N-glycosylation 是 TWEAK 的。引用补全为 Nat Rev Drug Discov 2008;7(5):411–425。

**新发现。** isoform 2（Q9NP84-2）缺失 33–67，即整个 CRD 与三对二硫键，但保留 TM 和完整
胞内尾 —— 天然的「无配体结合域但可跨膜并保留 TRAF 区」变体，对应方案中
ligand-independent clustering 的问题。原方案未提。

**产出。** `analyses/2026-11-03_tweakr-fn14-structure/`：README、
`code/make_fig_TR1_topology.R`（R 4.5.2，11 项 stopifnot 自检）、Fig. TR1（PDF/SVG/PNG 600 dpi）、
图注、source data、`manifests/outputs.tsv`（sha256）。渲染后目视检查两轮，修掉标签重叠、
D45 骑在域边界上（代入椭圆方程 ≈ 0.994）、以及 36/67 标注位置与链的进出方向相反。

**claim ceiling。** 拓扑示意图，非结构渲染；膜平面是人工参考；二硫键连线与四个点是示意位置，
故不逐点标注；TRAF motif 精确坐标未核实，只标区段；不得用 AF 全长模型（pLDDT 73.19）定义几何。
本目录不含任何 CRC 数据，不支持任何关于 TWEAKR 在 CRC 中功能的主张。

**UDE。** `root-branch-history.md` 升至 v1.1：新增 T8/B32，思维导图与登记表已校验一致（32=32）；
核实记录存于 `UDE/design/history/2026-11-03_fn14-structure-verification.md`；
`CURRENT.yaml`/`CURRENT.md`/`design`/`execution` 已同步；§7 待决事项增至 11 项。

**O2。** 按用户指示写入 `~/AGENTS.md`（72 行）：DUO 硬限制、文件系统分区、计算规则、AF3、
可追溯性。写前 `ssh -O check o2` 返回 `Master running (pid=52408)`，全程复用该通道，
**未触发 DUO**；写前确认 home 无同名文件，未覆盖任何内容。第 4 节的 AF3 可用性
（`hpc_alphafold3_users` 组、`alphafold/3.0.1` wrapper、权重可读、数据库清单）当场核实。

**状态：** 未 commit、未 push、无 PR、未审核。AF3 建模（M1–M4）未授权、未执行。

## 2026-11-03 — Fig. TR2：Fn14 三维结构在膜参考系中的位置与功能域（WL-20261103-FN14-002）

**What.** 用户要一张「TWEAKR 与细胞膜的参考图」：显示真实蛋白结构，不同 domain 用不同颜色。
TR1 是手画的拓扑示意，TR2 改用真实坐标：a 为 AF-Q9NP84-F1 v6 成熟链 28–129，嵌在按 TM 螺旋轴
放置的双分子层中；b 为实验 ECD 结构 2KMZ（NMR model 1），以 CRD 叠合到 AF 模型后同向显示；
c 为线性 domain 图 + pLDDT。配色沿用 TR1。产出在
`analyses/2026-11-03_tweakr-fn14-structure/figures/Fig_TR2_*`（README §12）。

**Why this design.** 只有 AF 模型覆盖全长，但 TR1 已经限定不能用它定义域间几何。
所以 TR2 只取两样可信的东西：AF 的域内折叠（CRD 与 2KMZ 的 Cα RMSD：对 model 1 为 1.74 Å，对 20 个 model 为 1.30–2.14 Å；
首版误写为 1.25 Å，原因及更正见 README §12），
以及 TM 螺旋轴（pLDDT 87.5，域内 PAE 2.8 Å），用后者放膜。
CRD↔TM 的 PAE 为 22–24 Å，图上直接注明「CRD 相对膜的位置未确定」。

**How.** 用开源 PyMOL 3.2 做无头渲染：先 PCA 求 TM 轴并刚体对齐，再正交投影，同时导出像素↔Å 映射；
R 负责画膜、标注和拼版。输入是 AF 模型与 PAE、2KMZ、UniProt FASTA，
存放于 `DATA/HotData/TWEAKR-oncoFetal/external/structures_fn14/`，sha256 记在 `manifests/inputs.tsv`。

**负结果。** PyMOL.app 2.5.7 的许可证已于 2024-07-01 过期，每张图都带 "License expired" 水印，已弃用。
改装开源 PyMOL 到 `SOFTWARES/tools/pymol-open-source/.venv`，并登记 TOOL_INDEX；
必须固定 numpy 1.26.4，因为 numpy 2.x 下 `get_coords` 报 ABI 错误。
AF 把 124–129 放进了疏水核心，属低置信伪影，图中以星号标出。

**claim ceiling.** 参考/示意用途。域内折叠可引用；域间几何（CRD 高度、倾角、结合面「朝外」）不可引用，
不得据此讨论 TWEAK 接近方向或抗体可及性。TRAF motif 坐标仍未核实。不含 CRC 数据。

**状态：** 未 commit、未 push、无 PR、未审核。

## 2026-11-03 — M1b：AF3 不用 Fn14 模板也能恢复 CRD 折叠（WL-20261103-FN14-003）

**What.** 用 AF3 3.0.1（O2）预测 Fn14 胞外区 28–80，与实验结构 2KMZ 比较。共三个模板条件，各 5 seed × 5 sample。
**判定条件 C**（模板截止 2007-12-31）：排名第一的模型 CRD Cα RMSD 为 1.31 Å（对最接近的 NMR 模型）、
1.62 Å（对 20 个模型的中位数），三对二硫键全部形成，25/25 达标 → **PASS**。A、B 结果与 C 几乎相同。

**Why it matters.** 这是 M2（TWEAK₃–Fn14₃）的前置校验：AF3 能正确给出 Fn14 CRD 的折叠，M2 的界面才值得解读。

**How / 过程中的修正（均在看到结构结果之前）。**
- 发现 A 的模板里有 **2EQP**（人 Fn14 TNFR 结构域，NMR，2008），原定判定条件 B 排除不了它。
  为此新增 C 作为判定条件（事先注册的修订 1，有时间戳的 commit）。
- 第一次推理作业失败：AF3 会把输出名转成小写，脚本按原大小写找文件。修复后重新提交。
- 写评估脚本时，用独立的 numpy Kabsch 交叉核对，发现 TR2 首版的 RMSD（1.25 Å）是多 state 对象造成的错误值，
  已更正为 1.74 Å。

**负结果 / 限制。** AF3 训练集包含 2KMZ/2EQP，不能排除"记住"了这个结构。M1b 证明的是"不输入 Fn14 模板也能重现"，
不是从头预测。另外，冻结目录里的 `run_metadata.txt` 是在 manifest 生成之后才写入的，所以 checksum 对不上，其余 165 个文件一致。

**O2 / DUO.** 本轮在约 1 小时内触发了约 5–6 次 DUO。原因有两层：复用请求失败时 ssh 会悄悄重新登录；
而且 O2 对每个新会话都会发 DUO 推送，复用连接也不例外。为此建了两个工具：`o2-agent` 别名和 `o2-run`
（永远不会新登录），以及 `o2-sh`（只开一个常驻会话，所有命令都从这里发）。
此后取回 M1b 结果、写入 O2 文件都走同一个会话，只在建立时触发 1 次 DUO。

**状态：** PR #2 未审核。下一步 M2 需要用户确认。


## 2026-11-03 — M2：AF3 的 TWEAK₃–Fn14₃ 界面包含全部四个已知结合位点（WL-20261103-FN14-004）

**What.** AF3 3.0.1（O2）预测 3 条 TWEAK 94–249 加 3 条 Fn14 28–80 的复合物，5 seed × 5 sample，两个模板条件。
**判定条件 M2-C**（模板截止 2007-12-31，没有 Fn14 和 TWEAK 模板）：排名第一的模型中，TWEAK 三聚体 iptm ≥ 0.87；
每条 Fn14 与 TWEAK 的 iptm 为 0.71–0.72；3 个拷贝的 D45/K48/M50/D62 全部 ≤ 4 Å；CRD RMSD 1.59–1.60 Å → **PASS**。
25/25 个 sample 达标；对照 M2-D 结果相同（两者第一名模型相差 1.01 Å）。

**Why it matters.** 有了一个与已知突变数据相符的 TWEAK–Fn14 界面工作模型，可以作为后续表位解读和突变设计的结构底图。

**How / 修正.** 评估脚本第一次运行时，CRD RMSD 全为 0.0：PyMOL `rms` 按链名配对，复合物的 D/E/F 链配不上 2KMZ 的 A 链。
改为显式 Cα Kabsch，并与改链名后的 PyMOL `rms` 交叉核对；判定标准没有变。RCSB 检索确认 PDB 中没有 TWEAK–Fn14 复合物
（Fn14 只有 2EQP/2KMZ/2RPJ，TWEAK 只有 4HT1 Fab 复合物）。

**限制.** 这是预测；四个位点是事先选定的阳性对照，不是盲测；AF3 可能从 TNF/TNFR 同源复合物学到结合几何。
Fn14 链 iptm 中等；3:3 是输入设定。不涉及 CRC 生物学。

**O2 / DUO.** 提交、轮询（每 15 分钟一次）、取回结果（30 MB，分 3 段，sha256 逐段核对，manifest 161/161）都走同一个
`o2-sh` 会话，本轮没有新增 DUO。

**状态：** 已推送到 PR #2，未审核。

## 2026-11-03 — PR #2 GPT 审核第 1 轮：REQUEST_CHANGES，6 项全部修改（WL-20261103-FN14-005）

**What.** 在 ChatGPT 项目 TWEAKR-oncoFetal 的「深入分析TWEAKR蛋白结构」会话提交 PR #2（HEAD `167a401`）。判定 REQUEST_CHANGES：
P0 0、P1 3、P2 3；不要求重跑 AF3。B32、TR1、TR2、M1b 结论保留，M2 PASS 保留但证据解释要重新校准。

**修改.**
- P1-1：新增 TWEAK 侧事后核对。Dhruv 2013 证明 Y176 必需、W231 非必需；模型中 Y176 75/75 在界面（2.7–3.0 Å），
  W231 也在（3.2–3.7 Å）——模型恢复了已知的重要接触区，但接触距离区分不了热点。注明已有对接模型（Lammens 2013、Dhruv 2013），
  不能声称首次发现界面。
- P1-2：超几何数字改为描述性几何参照，不再暗示显著性；25/25 称为采样稳定性。
- P1-3：`m2_checks.py` + `test_m2_checks.py`（4 项通过）；空选择/错配一律报错；模板按 Fn14/TWEAK/复合物三类核对。
  重跑后结果表除 summary 新增两列外逐字节不变。
- P2：Fig. TR2 标出 PIEET 113–117（TRAF2 consensus）并加"Illustrative orientation only"；README 状态更新；
  第 2 轮审核包附 M1b-C、M2 全部模型和 2KMZ。

**文献.** 补登 REF-032 至 REF-038。发现首版缺了四个结合残基的一手出处（Brown 2006，REF-034，小鼠 Fn14），已补。

**未核实（如实标注）.** 审核称 Brown 2003 用 alanine scanning 定位 PIEET（全文未取得）；审核称 2013 年有 Fn14-ΔEC 研究（未给 PMID）。

**状态：** 推送后提交第 2 轮审核；未合并。

## 2026-11-03 — PR #2 GPT 审核第 2 轮：APPROVE；B32 结构支线完成（WL-20261103-FN14-006）

**What.** 第 2 轮审核 `ff9b7ca`：**APPROVE**（P0 0、P1 0、P2 4）。审核方独立重算了全部原始结构：M2 50/50 个模型、M1b-C 25/25 个模型通过各自判定，
并实际运行了单元测试。允许合并，定位为 Fn14 structural reference and hypothesis-generation resource，不是 manuscript 的结构机制证据。

**P2 清理.** PIEET 的 alanine scanning 出处改为 Han 2003（REF-039；第 1 轮审核误归于 Brown 2003，已更正）；`chance_P` 列改名为
`geometric_reference_fraction_*`（数值不变）；写清两种 75/75 的分母（Fn14 拷贝 vs TWEAK 链观测，都不是独立实验）；
`outputs.tsv` 改为当前快照（无重复路径）。登记 REF-040（Brown 2013，Fn14-ΔEC），为 isoform 2 后续支线备用。

**Why it matters.** B32 交付物（坐标冻结、TR1、TR2、M1b、M2）均通过两轮外部审核；M2-C 第一名模型冻结为后续结构参考。

**状态：** 等待用户批准合并 PR #2（Agent 不自行合并）。下一条分支建议为 Fn14 therapeutic epitope atlas，需用户决定。

## 2026-11-03 — PR #2 合并；开启 Fn14 表位清单支线（WL-20261103-FN14-007）

**What.** PR #2 经 GPT 两轮审核 + final-head 核对（APPROVE）后合并（merge `762efb1`），B32 结构支线关闭。
按审核建议开启新支线 `analysis/20261103-fn14-epitope-atlas`：先建经核实的 Fn14 抗体/ADC 表位清单，再决定是否建模。

**How.** 证据分级 E1–E5 与纳入标准先写定并 commit（`afd15b4`），之后才开始检索（PubMed、ClinicalTrials.gov）。
共收录 11 条直接结合 Fn14 的药物，另把靶向 TWEAK 配体的药物单列。

**主要发现.**
- **E1 = 0**：公开文献中没有任何 Fn14–抗体复合物的实验结构。残基级表位约束只有一组：Trebing 2014
  报告 PDL192（enavatuzumab）与 P4A8 不能有效结合 W42A、R56P 突变体。
- 把这两个残基映射到 B32 冻结的 M2-C 模型：**都不在 TWEAK 接触面上（6.3–6.9 Å），且 TWEAK 结合后其 SASA 被遮掩 0 Å²**
  （对照：D45/K48/M50/D62 被埋 9–111 Å²）。据此提出可检验假说——该表位与 TWEAK 足迹相邻但不重叠，可能是非竞争性的，
  与"单独不激动、交联后强激动"（Salzmann 2013）相容。18D1/4G5 则能阻断 TWEAK 却不受这两个突变影响，是另一个位点。
- **ITEM-4 是唯一有明确内吞证据的抗体**（2 h 内特异内吞），对 ADC 方向最有参考价值。
- **VH/VL 序列在本轮文献中均未公开**，因此暂不具备做 Fn14–Fab 结构预测的输入条件；下一步是检索专利。

**限制.** 继承 B32 全部限制；两个点突变不等于一个表位，Fab 足迹仍可能与 TWEAK 空间冲突；突变失活不等于直接接触；
证据多为摘要级（Trebing 2014 全文非开放获取）；专利未检索。不含 CRC 数据。

**状态：** 清单 v1 完成，未审核，PR 待建。

**补记（2026-11-04 00:38 UTC）：** PR #3 经用户明确授权合并（merge `cb4ba95`）。**合并时 GPT 审核尚未返回**——
审核请求已提交到指定审核会话，回复后以后续 commit 处理。与 PR #2（审核通过后才合并）不同，本目录目前是
"已合并但未经外部审核"，按 AGENTS.md §5 在审核完成前不作为 canonical evidence。

## 2026-11-04 — PR #3 审核第 1 轮：REQUEST_CHANGES，v1 有三处实质错误（WL-20261104-FN14-008）

**What.** PR #3 已按用户授权合并（`cb4ba95`）**之后**，GPT 审核返回 REQUEST_CHANGES（P0 0 / P1 4 / P2 2）。
审核方用 Biopython 独立复算了 SASA 与距离，**几何计算 PASS、数值完全一致**；需改的是证据清单与生物学解释。

**v1 的三处实质错误（都已在 PR #4 改正）.**
1. **残基归属错了。** W42 与 R56 分属两个不同抗体：PDL192（enavatuzumab）对 R56P 敏感、仍结合 W42A；P4A8 相反。
   v1 把两者当作同一个 Fab 足迹的两个锚点。
2. **"没有竞争实验"是错的。** 直接竞争数据已存在：PDL192 几乎不阻断 TWEAK，P4A8 有效阻断，BIIB036 剂量依赖阻断。
3. **漏掉了真实存在的 Fn14 ADC。** Bayer 的 TWEAKR-KSPi-ADC1/ADC2 在 CT26 结肠癌模型中有效。
   **根因是检索方法**：靶点有四个名字，v1 只用了 Fn14/TNFRSF12A，没覆盖 **TWEAKR**。已补做同义词完整检索。

**最重要的修正：v1 的核心推论被一个实证反例推翻。** v1 说"W42/R56 都没被 TWEAK 埋藏 → 这类抗体可能非竞争性"。
但 W42 没被埋，而对 W42A 敏感的 P4A8 **确实阻断** TWEAK。所以单个残基不被埋藏，不能推出抗体不竞争——
完整 Fab 足迹约 800 Å²，可以从未被埋藏的残基出发仍压住配体面。这一点 v1 写在"限制"里，现在升级为已证伪。

**换来一个更好的问题.** 两个敏感残基都未被埋、距离相近（6.3 vs 6.9 Å），却对应相反的竞争表型。
"为什么？"适合用 Fn14–Fab 建模检验，而且检验的是**已有实验标准答案的现象**，比 v1 的用法可靠。

**诚实标注.** 审核的关键证据来自三篇原文的图（Salzmann 2013、Michaelson 2011、Trebing 2014）。
本项目复核发现三篇在 Europe PMC 均标非开放获取，PMC efetch 只返回题录与摘要，**无法独立核实图级结果**。
因此表中标为 `verified(abstract) + review(figure)`，并在 results_v2 第 6 节写明。取得原文是下一步最高优先级。

**流程教训.** 本轮是先合并后审核（用户授权），结果带错误的 v1 进入了 main。PR #2 是审核通过后才合并，没有这个问题。

**状态：** 修订在 PR #4，未合并。

**补记（2026-11-04，第 3 轮提交后）：** 自行核实了两条待办中的一条，并得到第三条独立证据。
Kyowa Kirin WO2020128927A1 的权利要求原文已读：该抗体是 **antagonist 且明示不是 agonist**，
"attenuates the binding of TWEAK to Fn14"，表位为 subdomain 1（`APGTAPCSRGSSWSADLDKCM`，本项目按 Q9NP84
核对正好是 30–50）中的 Gly32/Thr33/Ala34/Pro35/**Trp42**/Ala44/**Asp45**/Leu46/Asp47/**Lys48**/Cys49。
映射到 M2 模型：11 个残基方位角 9–84°（均值 44°），整片在 TWEAK 结合面上，6/11 与 TWEAK ≤ 5 Å；
而不阻断的 enavatuzumab 所依赖的 R56 在 139°，在区间外。**至此三个相互独立的抗体都符合方位规律**
（P4A8 47° 阻断、Kyowa 9–84° 阻断、enavatuzumab 139° 不阻断）。

## 2026-11-04 — PR #4 审核第 3 轮：Bayer 专利用实验独立证实了方位结论（WL-20261104-FN14-010）

**判定 REQUEST_CHANGES**（P0 0 / P1 4 / P2 3）。审核方用同一个 CIF 复算，方位角与本项目一致
（W42 47.3°、R56 138.9°），并补做了原点敏感性分析（本项目已自行复算，数值相同）：角度随原点变化
（W42 47/46/30°、R56 139/145/108°），但**方向分离不变**；到参考区域质心的距离（6.0 vs 17.9 Å）不依赖原点。

**最重要的新证据：Bayer WO2015189143A1。** 该专利对 CRD 做了完整丙氨酸扫描，正文写明
"TWEAK binding depends on L46 …, TPP-2090 binding on D47 and PDL-192 binding on R56.
**PDL-192 binds opposite of the TWEAK ligand binding site**, TPP-2090 binds directly to the TWEAK ligand site."
这是**用实验方法、独立于本项目**得到的同一结论。本模型的距离与之吻合：L46 3.5 Å、D47 6.9 Å（结合面上）
vs R56 17.9 Å（另一侧）。至此四条独立证据（TWEAK 本身、TPP-2090、P4A8、Kyowa 拮抗抗体 vs enavatuzumab）
指向同一几何。

**决定性检验现在可做.** 审核找到 PDL192 的 VH/VL（WO2009020933A2，Facet Biotech）与 P4A8 的 VH/VL
（WO2009140177A2，Biogen）——正是方位分析中的两个抗体。建两个 Fab 模型即可直接检验它们是否落在两个面上。

**其他修改.** BIIB036 由 E4 改为 E3（它自己有双向竞争实验，Michaelson 2011 Fig 2B，WiDr 结肠癌细胞）；
专利表补到 10 个族；术语按审核改为 "four-residue TWEAK-binding reference patch"，并说明方位角是径向夹角、
不是抗体接近角；补各偶联物的内吞记录并标明哪些尚未核实。

**状态：** PR #4 未合并，待第 4 轮审核。

## 2026-11-04 — PR #4 审核第 4 轮：发现一个被转述省略的关键限定（WL-20261104-FN14-011）

**判定 REQUEST_CHANGES**（P0 0 / P1 4 组 / P2 4 组），审核称"接近最终验收"，核心结构结论通过。

**我自己的一个疏漏：** BIIB036 在主表已改 E3，但 results_v2 的汇总计数没同步，仍写 E3 = 3。
已按主表重新计数并统一：E1 0 / E2 2 / E3 4 / E4 7，共 13 条。

**最重要的发现，以及一次有价值的"不轻信转述"：** 审核指出 Biogen 专利 WO2009140177A2 的 Example 21
报告了 P4A8 Fab 与人 Fn14 胞外区的晶体（3.5 Å）。本项目读原文后发现**转述省略了决定性限定**：
电子密度只能解释 Fn14 的 **50–67**；**R-factor 46%**（未精修水平）；H3 CDR 与 Fn14 N 端在密度中缺失；
界面表是叠合 NMR 结构 + ROSETTA 建 H3 + 约束优化得到的混合模型。
**尤其关键：P4A8 依赖的 W42 落在未解析的 50–67 之外**，所以这块密度既不能证实也不能推翻 W42 表位归属。
因此不计为 E1，单列并写明限定。若照搬转述，就会把它记成一个已解析的复合物结构。

**SEQ ID 争议解决：** 审核确认 PDL192 VH=3/VL=4、P4A8 VH=2/VL=5；本项目先前看到的 SEQ ID NO: 25 是
PDL192 的重链 CDR3 而非完整 VH——这与本项目在 Biogen 专利中看到的 "P4A8 101 YGNLYYAMDYWGQGTSVTVSS 121
(SEQ ID NO: 2" 一致（框架 4 结尾，确为 VH 片段）。

**数据字典：** 新增 `internalization_verification_status` 字段级状态，避免某条记录其他字段已核实就让
未核实的内吞结论看起来也是 verified。

**状态：** PR #4 未合并，待第 5 轮。

**第 4 轮收尾（2026-11-04）：** 审核称这是最后一次要求修改。除上述两处错误外，还有一处**预注册越界**
需要记录：`design.md` 原文规定专利只用于确认序列是否公开、不作生物学证据，但 results_v2 已把 Kyowa、Bayer
专利的生物学主张当作外部支持。按事先注册的纪律，**不悄悄放宽原规则**，而是立 `design.md` 修订 1，
把证据分成 A（同行评议实验）/ B（专利报告实验）/ C（专利权利要求）三层，冻结的 E1–E5 只统计 A。
另按审核建议写定 `docs/freeze_criteria.md`：把范围定义为"截至 2026-11-04 公开文献与专利中可追溯的 binder"，
冻结条件是连续两轮定向查询无新增**独立** lineage，而不是追求穷尽。
