# Draft — request for cell-level origin metadata (Checkpoint 1B)

**Status:** draft, approved in principle. **Not sent.**
**To:** Jingjing Li <Jingjing.Li@ucsf.edu>
**Cc:** Susan J. Fisher <susan.fisher@ucsf.edu>
Recipients are the two corresponding authors whose addresses appear in the author
affiliations of PubMed 41951740 and in the PMC13149032 full-text XML (checked 2026-10-08).
**From:** Zhixin Li

---

**Subject:** Maternal/fetal origin labels for the public snPlacenta object (Wang et al., Nature 2026)

Dear Dr. Li and Dr. Fisher,

Thank you for making the maternal–fetal interface atlas and the COSMOS explorer publicly
available. We are using the annotated snRNA-seq object `scPlacenta_host.h5ad`
(cell.ucsf.edu/snPlacenta; 193,202 nuclei, 23 samples) as a developmental reference.

The paper assigns maternal versus fetal origin to each nucleus with Souporcell (Fig. 1d;
Extended Data Fig. 2d,e), and the Figure 1 notebook reads `adata.obs["origin"]`. This field
does not appear in the public H5AD objects or in the explorer metadata. Would you be willing
to share the following minimal metadata? We do not need any sequencing data.

1. Cell barcode → maternal/fetal origin for the public cell IDs (`newBC`, e.g.
   `ZY011_AAACAGCCAAGTTATC-1`), ideally as
   `cell_id, sample_id, souporcell_cluster, genotype_origin`.
2. The rule linking `sample_id` and the barcode prefix in `newBC` to the original
   Cell Ranger ARC barcodes used for Souporcell.
3. The per-sample correspondence between Souporcell cluster and maternal/fetal origin.
4. If available, an assignment-confidence value or a flag for ambiguous/unassigned nuclei.

If sharing the full per-cell table is not convenient, items 2 and 3 alone would let us
reconstruct the labels consistently with your analysis.

We would cite the paper and the COSMOS resource and use these labels only for expression
analyses of the annotated cell types.

With many thanks,

Zhixin Li
Broad Institute
