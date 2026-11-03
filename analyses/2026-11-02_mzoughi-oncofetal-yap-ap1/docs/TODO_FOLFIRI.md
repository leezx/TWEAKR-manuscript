# To-do: the FOLFIRI arm of Mzoughi *et al.* Fig. 4

Recorded, not run — this was the explicit instruction for Fig. 4. The data is
downloaded and checksummed so the work can start without another retrieval step.

## Why the design is worth copying

Figure 4 is the only part of this paper that goes from *"a resistant cell state
exists"* to *"removing it changes the outcome of chemotherapy"*. Three features
make it unusually strong, and all three are directly transferable to the TWEAKR
manuscript:

1. **The resistant state is measured, not assumed.** A synthetic locus control
   region driving a fluorophore (the OnF reporter) reads out the oncofetal state
   live, so the same tumoroid can be scored before and after treatment. FOLFIRI
   shifts the population from OnF 9.9%/8.2% and Stem 18.7%/22.1% to Hybrid 52.1%/54.2%
   (Supplementary Table S6, Fig. 4d) — chemotherapy *enriches* the plastic state
   rather than depleting it.
2. **Genetic ablation of the state, not pharmacological inhibition of a gene.**
   `OnF-DTR` / `STAR-DTR` diphtheria-toxin receptor alleles let them delete the
   OnF compartment, the stem compartment, or both, in an established tumour, and
   compare tumour volume (Fig. 4h, 4j). That separates "the state matters" from
   "this drug has an effect".
3. **The combination is tested as a combination.** FOLFIRI alone vs FOLFIRI + DT
   (Fig. 4l), and a full drug-concentration matrix with combination indices for
   FOLFIRI × IAG933 (TEAD inhibitor) and FOLFIRI × MRTX1133 (KRAS G12D inhibitor),
   including the triple (Fig. 4m–q). The CI values distinguish additivity from
   synergy: FOLFIRI + IAG933 ≈ 1.0 (additive), the triple ≈ 0.40–0.47 (synergistic).

## The TWEAKR parallel

If TWEAKR marks and sustains the same plastic state, the matching experiment is:
does blocking TWEAK–TWEAKR before or alongside FOLFIRI prevent the shift into the
Hybrid/OnF compartment, and is the combination synergistic by the same CI
measure? Script 02 of this analysis already establishes the prerequisite —
*Tnfrsf12a* is YAP- and AP-1-dependent, i.e. it sits inside the programme this
figure ablates.

## Data already in hand

| What | Accession | Local path | Size |
|---|---|---|---|
| VAKPS tumoroids, DMSO vs FOLFIRI, 3 vs 3, bulk RNA-seq | GSE237837 | `raw/GSE237837/GSE237837_EG12_salmon_gene_counts.csv.gz` | 764 KB |
| Authors' DESeq2 for the same contrast | Suppl. Table S4c | `processed/suppl_tables/Table_S4c.tsv` | 3.7 MB |
| OnF reporter high vs negative, 3 vs 3 | GSE235205 | `raw/GSE235205/` | 795 KB |
| Reporter GFP-high vs GFP-neg DE | Suppl. Table S4b | (in MOESM1) | — |
| Fig. 4 source data: population shifts, tumour volumes, viability matrices, CIs | Suppl. Table S6 | `raw/supplementary/41588_2024_2058_MOESM6_ESM.xlsx` | 54 KB |
| TFBS of the OnF synthetic locus control region | Suppl. Table S4a | (in MOESM1) | — |

All paths are relative to
`DATA/HotData/TWEAKR-oncoFetal/geo_GSE237954_mzoughi_oncofetal/`.

## Proposed first step, when this is picked up

One contrast, already runnable with `code/02_bulk_perturbation.R`'s machinery:
*Tnfrsf12a* and the oncofetal / placenta / immune programmes in FOLFIRI vs DMSO.
Prediction from the above: if FOLFIRI enriches the plastic state, the receptor
should go **up** under chemotherapy. A negative there would be informative, and
would be the cheapest available falsification of the whole TWEAKR–resistance link.

Caveat to carry into that analysis: n = 3 vs 3, one tumoroid line, one time point.
