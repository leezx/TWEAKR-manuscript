# `p4a8_crystal_interface.tsv` — provenance and the 2026-11-04 correction

**Source:** Example 21, TABLE 2 ("Amino Acid Interactions at the P4A8/Fn14 Interface") of the Biogen
anti-Fn14 patent family. Evidence tier **B** (patent-reported experiment, not peer reviewed), per
`docs/design.md` amendment 1.

**Which document was read.** The WO member (WO2009140177A2) is a 180-page scan with no text layer, and
this project originally transcribed Table 2 from its page images. The US family member
**US20090324602A1** ("Anti-fn14 antibodies and uses thereof") carries the **same Example 21 and TABLE 2
as machine-readable text**, and that is the source now used. Reading it resolved the error below and
allowed every pairing to be verified first-hand.

**Correction, 2026-11-04 (raised by the PR #5 review).** The first version of this table had **6 rows** —
the heavy-chain-CDR half of Table 2 — and this project treated them as the complete epitope. They are not.
Table 2 has a light-chain block as well, and the patent's description independently states the antibody

> "interacts with one or more of residues C49, W42, K48, D51, R58, A57, H60, R56, L46, and M50 of human Fnl4"

— **10 residues**, which is exactly the set of distinct Fn14 residues in Table 2. The table now has all 10.
The 6 heavy-chain pairings transcribed earlier were themselves **correct**; the omission was the
light-chain block, not an error within it.

**Verification status.** Every row's CDR and antibody residue is now read directly from the TABLE 2 text in
US20090324602A1 — nothing in this table is second-hand. `*` in the source marks H-bonds and is recorded in
`h_bond`. The geometric columns (`min_dist_to_TWEAK_A_in_M2C`, `angle_*`, `dist_to_patch_centroid_A`) are
computed by this project on the frozen M2-C rank-1 model, Fn14 chain D, and inherit B32's claim ceiling —
they describe a *predicted* TWEAK interface, not an experimental one.

**Consequence for the atlas claim.** "5 of the 6 contact residues lie within 5 Å of TWEAK" becomes
**6 of 10** (L46, K48, M50, A57, R58, H60), identical in Fn14 chains D, E and F. The overlap is therefore
**a smaller fraction than previously written (60% vs 83%)**, though it now includes **K48**, itself one of
the four known TWEAK-binding determinants. Angular span over the full set: **9.4–138.9°**.

**Bonus cross-check of the Fab sequences.** Table 2 prints the six P4A8 CDR strings:
L1 `RASKSVSTSSYSYMH`, L2 `YASNLES`, L3 `SRELPFT`, H1 `GYTFTDYGMH`, H2 `VISTYNGYTNYNQKFKG`,
H3 `AYYGNLYYAMDY`. **All six occur exactly** in the huP4A8 VH/VL recorded in
`../2026-11-04_fn14-fab-modelling/tables/fab_sequences.tsv`, which this project had read from scanned page
images and checked by translating the nucleotide sequence on the same page. US20090324602A1 and
WO2009140177A2 are **the same patent family**, so this is **a third cross-check within that family**, not a
third independent source. It still rules out a misreading of the sequence used for M3.
