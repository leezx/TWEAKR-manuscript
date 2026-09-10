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
| 0b. git init + GitHub repo | not started | needs repo name / visibility / account |
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
