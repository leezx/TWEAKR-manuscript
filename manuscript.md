<!--
Main text. Markdown format; Cell / Nature / Science research-article
structure and tone. Citations as [@bibkey], resolved against references.bib.
Figure calls in text as "Figure 1A", "Figure 2C", "Figure S1B".
Keep Results subsection headers as short declarative sentences (Cell style)
or noun phrases (Nature style) — pick one and stay consistent.
-->

# <Title — one declarative sentence, ≤ ~15 words>

**Short title / running head:** <≤ 50 characters>

## Authors

<Author One^1^, Author Two^2^, …, Corresponding Author^1,\*^>

^1^<Affiliation>
^2^<Affiliation>
\*Correspondence: <email>

---

## Abstract

<150–200 words (Cell) / ≤ 150 words unstructured (Nature). One paragraph:
context → gap → what was done → key result(s) with direction/magnitude →
significance. No citations, no undefined abbreviations.>

**Keywords:** TNFRSF12A; TWEAKR; oncofetal antigen; antibody–drug conjugate;
colorectal cancer; <…>

---

## Introduction

<3–4 paragraphs. Para 1: the disease / biological problem and why the
target class matters. Para 2: what is known about TWEAKR/TNFRSF12A and the
oncofetal-antigen rationale; the specific unknown. Para 3 (optional): why
prior approaches are insufficient. Final para: what this study does and the
headline finding — 2–3 sentences, present tense.>

---

## Results

### <Result heading 1 — e.g. "A fetal-developmental programme defines the TWEAKR target window">

<Narrative tied to Figure 1. State the question, the approach in one clause,
then the result with numbers. Cite panels: (Figure 1A). Push method detail
to method.md and validation detail to Figure S1.>

### <Result heading 2>

<… Figure 2 …>

### <Result heading 3>

<… Figure 3 …>

### <Result heading 4>

<… Figure 4 …>

<!-- add/remove Results subsections as the figure set settles -->

---

## Discussion

<3–5 paragraphs. Para 1: restate the principal finding and what it resolves,
without repeating the Results blow-by-blow. Middle paras: interpretation,
relation to prior work, mechanism. Include a "Limitations of the study"
paragraph (required by Cell; good practice everywhere). Final para: outlook
/ translational implication.>

### Limitations of the study

<Direct, specific. Data/design constraints, generalisability, what would be
needed to close each gap.>

---

## STAR Methods / Methods

See [`method.md`](method.md).

---

## Resource availability

Summarised in `method.md`; lead contact, materials availability, data and
code availability statements live there.

---

## Acknowledgments

<Funding (grant numbers), facilities, people who helped but are not authors.>

## Author contributions

<CRediT roles, e.g. "Conceptualization, A.O. and B.T.; Methodology, …;
Writing – original draft, A.O.; Writing – review & editing, all authors.">

## Declaration of interests

<"The authors declare no competing interests." or itemised disclosures.>

---

## Figure legends

Legends are maintained per figure in `Figures/FigureN.md` (main) and
`Figures/FigureN/FigSN.md` (supplementary). For submission they are
concatenated here in order:

- Figure 1 — see [`Figures/Figure1.md`](Figures/Figure1.md)
- <Figure 2 …>

---

## References

Managed in [`references.bib`](references.bib); cited inline as `[@key]`.
