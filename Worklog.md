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
| 0c. Reconcile GPT/ figure drafts with Figures/ scaffold | not started | user added GPT/Figure1-5.md |
| 1. Figure inventory & audit | not started | figures source still TBD |
| 2. Manuscript outline / target journal | not started | |
| 3. Draft sections (Intro/Methods/Results/Discussion) | not started | |
| 4. Figure finalization (print specs, legends) | not started | |
| 5. References + submission package | not started | |

Overall: scaffolding phase, no analysis/writing content yet.

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
