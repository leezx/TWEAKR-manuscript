<!--
FRAMEWORK ONLY. Panel titles + intended claims taken from GPT/Figure1.md.
Image links are placeholders — the PNGs do not exist yet; the user fills them
in one panel at a time. Do NOT write asserted results/numbers here until the
underlying analysis output is in hand; keep claims in <…> until then.
-->

# Figure 1. A recurrent oncofetal/revival-like epithelial state is present across colorectal cancer

**Key point:** An unbiased, cross-cohort CRC epithelial analysis identifies a
reproducible oncofetal/revival-like cell state that is cross-validated by
independent fetal/revival signatures and expands along disease progression.

**Status:** framework only — panel images and finalized legend text pending.

**Each panel must serve one word of the title:** *recurrent* → F; *oncofetal/revival-like* → E; *epithelial state* → B, D; *across colorectal cancer* → A, G.

## Panels

### Figure 1A. CRC atlas overview and epithelial-focused analysis schema

![Figure 1A](Figure1/Fig1a.png)
> _Image pending: `Figure1/Fig1a.png`_

**Legend (draft):** <Schematic of the integrated CRC epithelial atlas: N studies,
N patients, N samples, N epithelial cells; disease contexts covered — normal,
adenoma/FAP, primary tumour, metastasis. Keep to the minimal numbers; stage /
sex / ethnicity / study composition go to Figure S1.>
**Analysis / data source:** <CRC atlas integration — `../CRC-Atlas/…` and/or `DATA/scRNAseq/meta_study/`; see `Figures/Figure1/Note.md`.>

### Figure 1B. Epithelial landscape identifies major normal, premalignant, and malignant states

![Figure 1B](Figure1/Fig1b.png)
> _Image pending: `Figure1/Fig1b.png`_

**Legend (draft):** <Epithelial-only UMAP coloured by state (normal epithelial,
differentiated-like, proliferative CSC-like, oncofetal-like) and/or by disease
context. Sets the stage for state discovery; TWEAKR is not foregrounded here.>

### Figure 1C. Unbiased NMF / meta-program discovery identifies an oncofetal/revival-like epithelial program

![Figure 1C](Figure1/Fig1c.png)
> _Image pending: `Figure1/Fig1c.png`_

**Legend (draft):** <Meta-program loading heatmap across epithelial MPs, plus
top-weighted genes of the oncofetal-like MP (e.g. CLU, TACSTD2, ANXA1, SOX9).
Claim: this program is discovered unbiasedly, not imposed by scoring. Phrasing:
"TNFRSF12A is among the highest-weighted genes within the oncofetal-like
meta-program" — not "the top gene".>

### Figure 1D. Oncofetal MP and proliferative MP projected onto the epithelial landscape

![Figure 1D](Figure1/Fig1d.png)
> _Image pending: `Figure1/Fig1d.png`_

**Legend (draft):** <Same epithelial UMAP, continuous oncofetal-MP score beside
proliferative/proCSC-MP score. Claim: the oncofetal-like program marks a
localizable cell state, distinct from proliferative CSC and not simply
cell-cycle high/low.>

### Figure 1E. Independent fetal/revival/regenerative signatures nominate the same state

![Figure 1E](Figure1/Fig1e.png)
> _Image pending: `Figure1/Fig1e.png`_

**Legend (draft):** <Signature-by-state enrichment matrix: rows = fetal
intestine, revival stem cell, regenerative/YAP, published oncofetal/revCSC,
proliferative CSC, differentiation; columns = epithelial states or MPs. Claim:
the oncofetal-MP-high state co-enriches fetal/revival/regenerative/published
oncofetal signatures, separating from proCSC. Optional inset: cell-/sample-level
concordance of oncofetal-MP score vs published oncofetal signature.>

### Figure 1F. The oncofetal-like state recurs across patients and cohorts

![Figure 1F](Figure1/Fig1f.png)
> _Image pending: `Figure1/Fig1f.png`_

**Legend (draft):** <Patient-level recurrence: per-patient oncofetal-MP-high
fraction by study/disease category, and/or cohort recurrence heatmap, and/or
leave-one-study-out recovery. This panel carries the word "recurrent" in the
title — must be patient/cohort level, not a single pretty UMAP.>

### Figure 1G. The oncofetal-like state expands across disease progression and is enriched in metastasis

![Figure 1G](Figure1/Fig1g.png)
> _Image pending: `Figure1/Fig1g.png`_

**Legend (draft):** <Oncofetal-MP-high fraction (and published oncofetal/revival
score) across normal → adenoma/FAP → primary → metastasis, patient-level
aggregation. Claim limited to progression enrichment; survival / drug response
belong to Figure 2.>

### Figure 1H. (optional) Core marker expression distinguishing oncofetal-like and proliferative CSC states

![Figure 1H](Figure1/Fig1h.png)
> _Image pending: `Figure1/Fig1h.png` — optional; move to Figure S1 if space is tight._

**Legend (draft):** <Violin/dot/mini-heatmap of oncofetal markers (CLU, TACSTD2,
ANXA1, SOX9…), proliferative markers (MKI67, TOP2A, LGR5…), differentiation
markers.>

## Full legend (submission form)

**Figure 1. A recurrent oncofetal/revival-like epithelial state is present across colorectal cancer.**
**(A)** <…> **(B)** <…> **(C)** <…> **(D)** <…> **(E)** <…> **(F)** <…> **(G)** <…>
<Global notes: atlas composition, MP-scoring method (→ `method.md`), signature
sources, statistics — test, n and what n is, patient-level aggregation. Define
all abbreviations (MP, CSC, proCSC, revCSC, FAP).>

## Source

- Data / results: `../TWEAKR-OncoPlacental/results/<step>/…`, `../CRC-Atlas/…`
- Plotting code: `../TWEAKR-OncoPlacental/scripts/<step>/…`

## Related supplementary figures

- Figure S1 — Atlas construction and metadata — `Figure1/FigS1.md`
- Figure S2 — Robustness of the oncofetal meta-program — `Figure1/FigS2.md`
- Figure S3 — Cross-validation and negative controls — `Figure1/FigS3.md`
- Figure S4 — Pan-cancer oncofetal extension (optional) — `Figure1/FigS4.md`

## Planning notes

Rationale and panel-selection reasoning: [`../GPT/Figure1.md`](../GPT/Figure1.md).
