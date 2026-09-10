<!--
FRAMEWORK ONLY. Panel titles + intended claims from GPT/Figure4.md.
Pathway hierarchy to establish: TWEAK → TWEAKR → YAP/TEAD → oncofetal/revival state.
Keep sufficiency (TWEAK induces), receptor dependence (KO blocks TWEAK response),
receptor requirement (KO collapses endogenous state), and YAP epistasis
(inhibitor/KO phenocopy + active-YAP rescue) as SEPARATE claims.
Public perturbation data = triangulation only, not the main causal evidence.
Do NOT let this become a "perturbation encyclopedia".
-->

# Figure 4. TWEAK–TWEAKR activates a YAP-dependent oncofetal transcriptional program in CRC

**Key point:** Isogenic organoid perturbation shows TWEAK induces the
oncofetal/revival state in a TWEAKR-dependent manner, patient-derived oncofetal
genes track this axis, and YAP/TEAD sits downstream of TWEAKR — corroborated by
independent public perturbation datasets.

**Status:** framework only — panel images and finalized legend text pending.

## Panels

### Figure 4A. Independent perturbation datasets converge on TWEAKR/YAP regulation of the oncofetal state

![Figure 4A](Figure4/Fig4a.png)
> _Image pending: `Figure4/Fig4a.png`_

**Legend (draft):** <Perturbation × program matrix. Perturbations: TWEAK,
TNFRSF12A OE, TNFRSF12A KO/KD, YAP1 KO/KD, TEAD perturbation, TGFβ, other
regeneration-inducing perturbations. Readouts: CRC-atlas oncofetal MP, published
revCSC, fetal intestine, YAP/TEAD, proCSC, cell cycle. Claim: direction
consistency (TWEAK/TWEAKR-OE/TGFβ → OnF↑; TNFRSF12A/YAP/TEAD loss → OnF↓), not
effect-size ordering across studies.>

### Figure 4B. Isogenic TWEAK–TWEAKR perturbation design in CRC organoids

![Figure 4B](Figure4/Fig4b.png)
> _Image pending: `Figure4/Fig4b.png`_

**Legend (draft):** <Design schematic: Control, TWEAK, TWEAKR KO, TWEAKR KO +
TWEAK, YAP inhibition/KO, TWEAK + YAP inhibition, (if feasible) active-YAP rescue
in TWEAKR KO. ≥2 models — e.g. one mouse Apc/Kras/p53 organoid + one human CRC
model. Core 4 arms → RNA-seq; YAP epistasis → focused readout.>

### Figure 4C. TWEAK induces a receptor-dependent global transcriptional transition

![Figure 4C](Figure4/Fig4c.png)
> _Image pending: `Figure4/Fig4c.png`_

**Legend (draft):** <PCA, sample correlation, DE-gene counts, centroid/trajectory
shift. Target result: Control→TWEAK moves one way, TWEAKR KO the opposite,
TWEAKR KO + TWEAK cannot reach the TWEAK position. "State reprogramming", not a
few markers.>

### Figure 4D. TWEAK and TWEAKR loss reciprocally regulate oncofetal/revival versus proliferative CSC programs

![Figure 4D](Figure4/Fig4d.png)
> _Image pending: `Figure4/Fig4d.png`_

**Legend (draft):** <Signature-level causal panel: oncofetal MP, revCSC,
fetal/regenerative, YAP/TEAD, proCSC, differentiation/cell cycle. Target: TWEAK →
OnF↑/revCSC↑/YAP↑/proCSC↓; TWEAKR KO → opposite; KO + TWEAK → no rescue. Supports
"TWEAK induces an oncofetal/revival-like state in a TWEAKR-dependent manner.">

### Figure 4E. Patient-derived oncofetal MP genes are induced by TWEAK and depleted after TWEAKR loss

![Figure 4E](Figure4/Fig4e.png)
> _Image pending: `Figure4/Fig4e.png`_

**Legend (draft):** <Use the Figure 1 patient-derived oncofetal MP directly:
patient OnF-MP loading vs TWEAK-treatment logFC, and vs TWEAKR-KO logFC. Define
the TWEAK-induced ∩ TWEAKR-dependent core and test its overlap with the
patient-derived MP. Closes human discovery → experimental perturbation → same
state. Most important computational panel of the figure.>

### Figure 4F. YAP/TEAD inhibition and rescue establish pathway hierarchy downstream of TWEAKR

![Figure 4F](Figure4/Fig4f.png)
> _Image pending: `Figure4/Fig4f.png`_

**Legend (draft):** <Layer 1: TWEAK → YAP nuclear localization↑, p-YAP↓, TEAD
reporter↑. Layer 2: TWEAK + YAP inhibitor → OnF induction lost. If available:
TWEAKR KO + constitutively active YAP → OnF rescued (locks TWEAKR upstream of
YAP). Determines "YAP-associated" vs "YAP-dependent".>

### Figure 4G. (optional) TWEAK converges with established fetal-regenerative perturbations such as TGFβ

![Figure 4G](Figure4/Fig4g.png)
> _Image pending: `Figure4/Fig4g.png` — optional; Supplement if space is tight._

**Legend (draft):** <TWEAK perturbation signature vs TGFβ-induced fetal
reprogramming signature (or public TGFβ RNA-seq concordance). Claim: "TWEAK
engages a program convergent with established fetal-regenerative signaling" —
not "TWEAK acts through TGFβ".>

## Full legend (submission form)

**Figure 4. TWEAK–TWEAKR activates a YAP-dependent oncofetal transcriptional program in CRC.**
**(A)** <…> **(B)** <…> **(C)** <…> **(D)** <…> **(E)** <…> **(F)** <…>
<Global notes: organoid models and genotypes; perturbation reagents and doses;
RNA-seq design and n; signature definitions (→ `method.md`); statistics. Define
OE, KO, KD, MP, OnF, YAP/TEAD.>

## Source

- Data / results: <organoid RNA-seq — `../TWEAKR-OncoPlacental/results/<step>/…`; public perturbation atlas>
- Plotting code: `../TWEAKR-OncoPlacental/scripts/<step>/…`

## Related supplementary figures

- Figure S5 — Immune-modulatory transcriptional phenotype of the oncofetal state — `Figure4/FigS5.md`
- Figure S6 — Placental/trophoblast transcriptional convergence — `Figure4/FigS6.md`

## Planning notes

Rationale: [`../GPT/Figure4.md`](../GPT/Figure4.md).
