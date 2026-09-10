<!--
Main text. Markdown; Cell / Nature / Science research-article structure and tone.
Citations as [@bibkey] against references.bib. Figure calls: "Figure 1A",
"Figure S1B". Results subsection headers are short declarative sentences (Cell).
FRAMEWORK STAGE: text is a skeleton. Bracketed <…> marks content to be written
from real analysis output — do not convert to asserted results/numbers until the
underlying data is in hand. Per-figure panel plans live in Figures/FigureN.md;
design rationale in GPT/FigureN.md.
-->

# <Title>

Working options (tighten once Figure 2G / Figure 3 land):
- *A macrophage TWEAK–TWEAKR–YAP niche sustains a recurrent oncofetal state in colorectal cancer*
- *TWEAK–TWEAKR signaling maintains a clinically aggressive oncofetal cell state in colorectal cancer*

**Short title / running head:** <≤ 50 characters, e.g. "TWEAK–TWEAKR oncofetal state in CRC">

## Authors

<Author One^1^, …, Corresponding Author^1,\*^>

^1^<Affiliation>
\*Correspondence: <email>

---

## Abstract

<One paragraph, ~150–200 words. Context: therapy-resistant, plastic cell states
in CRC. Gap: what maintains the oncofetal/revival-like malignant state and
whether it is actionable. Approach: cross-cohort single-cell + spatial atlas,
frozen-signature clinical projection, isogenic organoid perturbation, in vivo
validation. Key results (fill from figures): a recurrent oncofetal state
(Fig. 1); adverse outcome and treatment persistence (Fig. 2); a TNFSF12⁺
macrophage–TNFRSF12A niche (Fig. 3); TWEAK→TWEAKR→YAP causal control (Fig. 4);
in vivo state remodeling and modulated therapy response (Fig. 5). Significance:
a TME-driven, druggable axis (TNFRSF12A is an ADC target) upstream of a
clinically aggressive state. No citations; define no new abbreviations.>

**Keywords:** TNFRSF12A; TWEAKR; TWEAK/TNFSF12; oncofetal state; revival stem cell;
YAP/TEAD; tumour-associated macrophage; colorectal cancer; therapy persistence;
antibody–drug conjugate.

---

## Introduction

<Para 1 — The problem: CRC outcome is limited by plastic, therapy-tolerant
malignant cell states; regenerative/"revival"/oncofetal programs are recurrent
across intestinal injury and cancer [@…].>

<Para 2 — What is known / the gap: fetal-regenerative reprogramming is
YAP/TEAD-linked and TNFRSF12A itself is a YAP-associated fetal gene [@…]; TWEAK
(TNFSF12)–TWEAKR (TNFRSF12A) signaling drives NF-κB/YAP responses in epithelial
injury [@…]. Whether a TME ligand sustains the oncofetal state in CRC, through
which receptor, and whether it is causal and actionable, is unresolved.>

<Para 3 — Why prior approaches fall short: signature-scoring studies risk
circularity; single-cohort "pretty examples" cannot establish recurrence;
association cannot establish causality or direction.>

<Para 4 — This study: an unbiased cross-cohort discovery of the state, a frozen
clinical test, a convergent population/spatial nomination of a macrophage
TWEAK niche, isogenic perturbation establishing TWEAK→TWEAKR→YAP causality, and
in vivo validation with a therapy readout. Headline (fill from results).>

---

## Results

### A recurrent oncofetal/revival-like epithelial state spans colorectal cancer

<Introduce the integrated CRC epithelial atlas — N studies, N patients, N
samples, N epithelial cells; normal → adenoma/FAP → primary → metastasis
(Figure 1A; Figure S1). Unbiased NMF meta-program discovery across the
epithelial compartment identifies an oncofetal/revival-like program; TNFRSF12A
is among its highest-weighted genes (Figure 1B–C). Projected onto the
single-cell landscape the program marks a localizable state distinct from
proliferative CSC (Figure 1D), and independent fetal/revival/regenerative
signatures nominate the same state (Figure 1E; Figure S3). The state recurs
across patients and cohorts (Figure 1F; Figure S2) and expands along disease
progression, peaking in metastasis (Figure 1G). It is not explained by cell
cycle, EMT, hypoxia/stress, or dissociation artifact (Figure S3).>

### The oncofetal state marks clinically aggressive, treatment-persistent CRC

<Using signatures frozen from Figure 1 — the NMF oncofetal MP, published revCSC,
and proCSC as a counter-axis — projected onto independent bulk, single-cell, and
longitudinal treatment cohorts (Figure 2A). The oncofetal score is associated
with adverse OS/RFS across cohorts (Figure 2B) and <is / is not> independent of
stage, MSI/MMR, and CMS/stromal content (Figure 2C) — adjust the claim
accordingly. In matched pre/post samples, chemotherapy shifts CSC-state balance
toward the revival-like side (selective persistence, not induction) (Figure 2D),
the shift <relates to> clinical response, with baseline oncofetal state the most
informative (Figure 2E), and an independent ICI cohort shows analogous
persistence (Figure 2F) — distinct therapeutic pressures converging on a common
persistence state. TNFRSF12A preferentially marks the adverse/treatment-persistent
oncofetal compartment (Figure 2G); if this does not hold, the state is described
without the receptor here and TWEAKR is introduced in the next section.>

### Population-scale and spatial analyses nominate a TWEAK⁺ macrophage niche

<A patient-level epithelial receptor screen against the frozen oncofetal
signature ranks TNFRSF12A among the most consistently associated receptors
(Figure 3A). Ligand–target inference over a unified evidence ranking nominates
TNFSF12–TNFRSF12A among the most recurrent candidate axes, alongside other
regenerative ligands shown transparently (Figure 3B). Across human CRC, AOM/DSS,
and Cdx2/APC/KRAS models, macrophages are the predominant transcriptional source
of TNFSF12 (Figure 3C), concentrated in an SPP1⁺/LAM-like TAM state (Figure 3D).
TNFSF12-high TAM abundance covaries with epithelial TNFRSF12A/oncofetal state
across patients (Figure 3E), and spatially, TNFSF12⁺ macrophages localize
preferentially near TNFRSF12A-high/oncofetal tumour regions (Figure 3F),
reproducibly across sections and patients (Figure 3G). These orthogonal analyses
nominate — but do not prove — a TNFSF12⁺ macrophage–TNFRSF12A-high epithelial
niche.>

### TWEAK–TWEAKR drives a YAP-dependent oncofetal program

<Independent public perturbation datasets show directionally consistent control
of the oncofetal program by the TWEAKR/YAP axis (Figure 4A). In isogenic CRC
organoids (≥2 models; Figure 4B), TWEAK induces a receptor-dependent global
transcriptional transition that TWEAKR KO blocks and TWEAKR KO + TWEAK cannot
rescue (Figure 4C). TWEAK and TWEAKR loss reciprocally regulate
oncofetal/revival versus proliferative CSC programs (Figure 4D). Patient-derived
oncofetal MP genes (Figure 1) are preferentially induced by TWEAK and depleted
after TWEAKR loss, defining a TWEAK-induced ∩ TWEAKR-dependent core (Figure 4E).
YAP/TEAD inhibition abolishes TWEAK-induced reprogramming and constitutively
active YAP rescues it in TWEAKR KO, placing YAP downstream of TWEAKR
(Figure 4F). The program converges with established fetal-regenerative signaling
such as TGFβ without acting through it (Figure 4G). The oncofetal state also
carries an immune-modulatory transcriptional phenotype (Figure S5); a
trophoblast-specific component is examined in Figure S6.>

### TWEAKR–YAP signaling maintains the oncofetal state in vivo

<In vivo (Figure 5A), TWEAK expands and TWEAKR loss contracts the oncofetal
state, with YAP perturbation phenocopying TWEAKR loss, by mouse-level state
proportions (Figure 5B) and per-mouse pseudobulk scoring (Figure 5C). In vitro
and in vivo perturbations, and the patient-derived MP, converge on the same
program (Figure 5D). Against the strongest clinical exit from Figure 2, TWEAKR
loss <alters tumour response / remodels residual oncofetal fraction>
(Figure 5E) — claim scaled to whether drug response itself changes. A working
model summarizes solid (TWEAK→TWEAKR→YAP→state) versus proposed (macrophage
source; persistence; immune phenotype; placental convergence) links
(Figure 5F).>

---

## Discussion

<Para 1 — Principal finding: a TME ligand (macrophage TWEAK) acting through
TNFRSF12A and YAP/TEAD sustains a recurrent, clinically aggressive oncofetal
state in CRC; what this resolves.>

<Para 2 — Relation to prior work: fetal-regenerative reprogramming, YAP/TEAD,
revival stem cells, SPP1⁺/LAM TAMs; TNFRSF12A as a YAP-associated fetal gene.>

<Para 3 — Translational implication: TNFRSF12A is an ADC target; an axis
upstream of therapy persistence. Link to `../TWEAKR-OncoPlacental` target-window
analyses (normal-tissue safety, oncofetal specificity).>

<Para 4 — Alternative interpretations / open mechanism: ligand sufficiency vs
in vivo requirement; macrophage-derived vs macrophage-associated; immune
phenotype vs immune evasion; placental convergence vs generic developmental
reactivation.>

### Limitations of the study

<Reanalysis-heavy discovery; cohort composition and platform heterogeneity;
patient n for longitudinal ICI; "nominate" not "prove" for the macrophage
source without the conditioned-medium/blockade experiment; xenograft vs
syngeneic constraints on ICI; spatial cohort size.>

---

## STAR Methods / Methods

See [`method.md`](method.md).

## Resource availability

Lead contact, materials availability, and data and code availability statements
are in [`method.md`](method.md). Analysis code: `../TWEAKR-OncoPlacental`.

---

## Acknowledgments

<Funding (grant numbers), cores, non-author contributors.>

## Author contributions

<CRediT roles.>

## Declaration of interests

<TNFRSF12A / ADC-related interests must be disclosed here if applicable.>

---

## Figure legends

Maintained per figure and concatenated here for submission:

| Figure | Title | Legend file |
|---|---|---|
| Figure 1 | A recurrent oncofetal/revival-like epithelial state is present across colorectal cancer | [`Figures/Figure1.md`](Figures/Figure1.md) |
| Figure 2 | The TWEAKR-associated oncofetal state marks clinically aggressive and treatment-persistent CRC | [`Figures/Figure2.md`](Figures/Figure2.md) |
| Figure 3 | Population-scale and spatial analyses nominate a TWEAK⁺ macrophage niche for TNFRSF12A-high oncofetal tumour cells | [`Figures/Figure3.md`](Figures/Figure3.md) |
| Figure 4 | TWEAK–TWEAKR activates a YAP-dependent oncofetal transcriptional program in CRC | [`Figures/Figure4.md`](Figures/Figure4.md) |
| Figure 5 | TWEAKR–YAP signaling maintains the oncofetal state in vivo and modulates therapeutic response | [`Figures/Figure5.md`](Figures/Figure5.md) |

Supplementary figures and text: [`supplementary.md`](supplementary.md).

---

## References

Managed in [`references.bib`](references.bib); cited inline as `[@key]`.
