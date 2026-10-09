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
