# Cancer annotation provenance: unresolved

Dataset inventory and study-level patient mapping were accepted by the human
reviewer. Only malignant annotation provenance remains a pilot blocking check.
No code changes or real-data NMF execution were performed.

Verified: group=Cancer is an original GSE254249 metadata label, separate from Epi.
Not yet verified: whether the original classification explicitly uses CNV or
another malignancy criterion, versus tumor-associated expression markers alone.

Primary paper: Gao et al., Cancer Cell, DOI 10.1016/j.ccell.2025.10.008,
PMID 41202810. Public publisher search indexing describes 19 major cell types
and 85 subpopulations based on gene profiles; this general statement does NOT
establish the definition of Cancer or exclude additional CNV analysis.

Access attempts: Cell full text and ScienceDirect returned 403. Public search
results did not expose the required classification method. Local filename
search found bibliographic Markdown records, not the paper or supplementary
methods PDF. No inference from an unrelated paper was used.

Required next source: readable STAR Methods or supplementary methods defining
malignant/cancer epithelial classification, with subsection/page citation.
Until then, retain annotation_provenance=PENDING and EXECUTE_NMF=0.

Sources:
- https://www.sciencedirect.com/science/article/pii/S1535610825004490
- https://www.cell.com/cancer-cell/fulltext/S1535-6108(25)00449-0
- https://pubmed.ncbi.nlm.nih.gov/41202810/
