<!--
FRAMEWORK ONLY. Panel titles + intended claims from GPT/Figure5.md.
Figure 5 has ONE job: show the Figure 4 mechanism holds in vivo and connects to
one real disease phenotype. Do not open new mechanism lines (placenta, immune
origin) here. Technical constraint: immunodeficient xenograft cannot test ICI —
ICI needs an immunocompetent/syngeneic (AKP → C57BL/6) setting; pick the single
strongest clinical exit from Figure 2 (chemo OR ICI), not a full factorial of both.
-->

# Figure 5. TWEAKR–YAP signaling maintains the oncofetal state in vivo and modulates therapeutic response

**Key point:** In vivo perturbation of TWEAK/TWEAKR/YAP remodels malignant-state
composition consistent with the in vitro mechanism, in vitro and in vivo
perturbations converge on the same program, and TWEAKR loss alters response to
the strongest clinically relevant treatment.

**Status:** framework only — panel images and finalized legend text pending.

## Panels

### Figure 5A. In vivo experimental design

![Figure 5A](Figure5/Fig5a.png)
> _Image pending: `Figure5/Fig5a.png`_

**Legend (draft):** <Arms: Control, TWEAK/vehicle, TWEAKR KO, YAP perturbation;
plus one treatment arm (chemo OR ICI — whichever Figure 2 shows strongest).
Model matched to the endpoint (syngeneic AKP → C57BL/6 if ICI). No chemo+ICI
factorial in the main figure.>

### Figure 5B. In vivo malignant-state landscape

![Figure 5B](Figure5/Fig5b.png)
> _Image pending: `Figure5/Fig5b.png`_

**Legend (draft):** <scRNA across control / TWEAK / TWEAKR KO / YAP perturbation:
oncofetal/revCSC, proCSC, differentiation, YAP activity — reported as
mouse-level state proportions, not only UMAP. Target: TWEAK → OnF expansion;
TWEAKR loss → OnF contraction; YAP loss/inhibition phenocopies TWEAKR loss.>

### Figure 5C. Pseudobulk confirms transcriptional state remodeling in vivo

![Figure 5C](Figure5/Fig5c.png)
> _Image pending: `Figure5/Fig5c.png`_

**Legend (draft):** <One pseudobulk per mouse; score Figure 1 NMF-OnF MP,
published revCSC, fetal, YAP/TEAD, proCSC. Avoids pseudoreplication — arguably
more important than the UMAP.>

### Figure 5D. In vitro and in vivo perturbations converge on the same transcriptional program

![Figure 5D](Figure5/Fig5d.png)
> _Image pending: `Figure5/Fig5d.png`_

**Legend (draft):** <Figure 4 TWEAK-induced genes vs Figure 5 in vivo
TWEAK-induced genes; TWEAKR-KO in vitro vs in vivo. Three-way concordance:
Figure 1 patient OnF MP ↔ Figure 4 in vitro ↔ Figure 5 in vivo. This is the
mechanistic closure.>

### Figure 5E. Therapeutic pressure interacts with the oncofetal state

![Figure 5E](Figure5/Fig5e.png)
> _Image pending: `Figure5/Fig5e.png`_

**Legend (draft):** <Strongest clinical exit only. Chemo: Control / Chemo /
TWEAKR KO / TWEAKR KO + Chemo → tumour response, residual OnF fraction, proCSC
fraction, regrowth/persistence. (ICI analogously, syngeneic.) Claim ladder:
"TWEAKR-dependent oncofetal plasticity contributes to treatment persistence"
only if TWEAKR KO changes drug response; otherwise "therapy remodels the
abundance of the TWEAKR-associated oncofetal state".>

### Figure 5F. Working model

![Figure 5F](Figure5/Fig5f.png)
> _Image pending: `Figure5/Fig5f.png`_

**Legend (draft):** <Solid arrows: TWEAK → TWEAKR → YAP/TEAD →
oncofetal/revival cell-state remodeling. Dashed: TWEAK⁺ TAM → TWEAK (unless the
macrophage-CM experiment is done); OnF → treatment persistence; OnF →
immune-modulatory phenotype; OnF ↔ placental convergence. Evidence grade must be
visible: what was discovered vs proved vs proposed.>

## Full legend (submission form)

**Figure 5. TWEAKR–YAP signaling maintains the oncofetal state in vivo and modulates therapeutic response.**
**(A)** <…> **(B)** <…> **(C)** <…> **(D)** <…> **(E)** <…> **(F)** model.
<Global notes: mouse model, genotypes, n per arm, treatment schedule, scRNA
platform, state-scoring method (→ `method.md`), mouse-level statistics.>

## Source

- Data / results: <in vivo scRNA — `../TWEAKR-OncoPlacental/results/<step>/…`>
- Plotting code: `../TWEAKR-OncoPlacental/scripts/<step>/…`

## Related supplementary figures

- <TBD during drafting — e.g. per-mouse QC; treatment tumour-growth curves; gating.>
- See also Figure S5 (immune phenotype) and Figure S6 (placental convergence), filed under Figure 4.

## Planning notes

Rationale: [`../GPT/Figure5.md`](../GPT/Figure5.md).
