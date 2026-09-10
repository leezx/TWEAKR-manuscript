# TWEAKR-manuscript

Working repository for the TWEAKR (TNFRSF12A) oncofetal–oncoplacental
ADC-target manuscript. All prose is written in **Markdown**, but the
**structure, tone, and figure conventions follow *Cell* / *Nature* /
*Science*** research-article norms.

The analysis this manuscript reports lives in the sibling project
`../TWEAKR-OncoPlacental/` (raw results, scripts, step design docs). This
repo holds **only the manuscript and its figures/tables** — no large data.

## Layout

| Path | What it holds |
|---|---|
| `manuscript.md` | Main text: Title, Abstract, Introduction, Results, Discussion, front/back matter. |
| `method.md` | Methods, STAR Methods / Online Methods style. |
| `supplementary.md` | Supplementary text: supplementary methods, extended discussion, notes. |
| `references.bib` | BibTeX reference database, cited from `manuscript.md` / `method.md` with `[@key]`. |
| `Figures/` | One `FigureN.md` (title + legend + panel links) and one `FigureN/` folder (panel images) per main figure. |
| `Tables/` | One `TableN.md` per main table; `TableSN.md` per supplementary table. |
| `Worklog.md` | Chronological what/why/how log of all work on this repo. |

## Figure conventions

- **One Markdown file per figure**: `Figures/Figure1.md` carries the figure
  **title** and the full **panel-by-panel legend**, and links each panel
  image with a relative Markdown image link.
- **One folder per figure**: `Figures/Figure1/` holds the main panel images,
  named `Fig1a.png`, `Fig1b.png`, … (lowercase panel letters).
- **Supplementary figures** are numbered **globally** (`S1`, `S2`, `S3`, …)
  but filed **under the main figure they relate to**:
  - `Figures/Figure1/FigS1.md` — supp figure legend, headed
    "Figure S1. … Related to Figure 1."
  - `Figures/Figure1/FigS1/` — its panels, `FigS1a.png`, `FigS1b.png`, …
  - Supplementary panels are kept in their own subfolder so that the many
    sub-panels never clutter the main figure folder.
- A main figure may have several related supplementary figures
  (`Figure1/FigS1`, `Figure1/FigS2`, …); Figure 2's first supplementary
  figure continues the global count (`Figure2/FigS3`, …).

## Table conventions

- `Tables/Table1.md`, `Tables/Table2.md`, … — main tables.
- `Tables/TableS1.md`, … — supplementary tables, globally numbered.
- Large tabular data files (`.csv`, `.xlsx`) for a table go in a
  `Tables/TableN/` folder alongside the `.md`.

## Status

Scaffold stage. `Figure1` is built out as the canonical template; other
figures are added once the manuscript outline is fixed. See `Worklog.md`
for history.
