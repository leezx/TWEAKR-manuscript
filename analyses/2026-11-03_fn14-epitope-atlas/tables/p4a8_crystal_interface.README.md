# `p4a8_crystal_interface.tsv` — provenance and the 2026-11-04 correction

**Source:** WO2009140177A2 (Biogen). Evidence tier **B** (patent-reported experiment, not peer reviewed),
per `docs/design.md` amendment 1.

**Correction, 2026-11-04 (raised by the PR #5 review):** the first version of this table had **6 rows**.
Those 6 are the heavy-chain-CDR-associated contacts this project transcribed from Example 21 Table 2.
They are **not** the complete P4A8 epitope. The patent's own description text states that the antibody

> "interacts with one or more of residues C49, W42, K48, D51, R58, A57, H60, R56, L46, and M50 of human Fnl4"

— **10 residues**. This project verified that sentence directly in the Google Patents full text of
WO2009140177A2 (it appears twice, in the summary and in the detailed description), so the 10-residue set
is first-hand. The table now has all 10 rows.

**What is and is not verified per row:**

- The 10 Fn14 residue identities: **verified** by this project from the patent text.
- The CDR pairing for the 6 heavy-chain rows: transcribed by this project from the Example 21 Table 2
  page images.
- The CDR pairing for W42 / K48 / C49 / D51: **not independently verified.** The PR #5 review reports
  them as light-chain CDR contacts in Table 2. The patent description separately names light-chain
  **S32, Y34, Y36 (CDR L1)**, Y54 (CDR L2) and R96 (CDR L3) as Fn14-interacting residues — this project
  verified that sentence — but it does not pair them with specific Fn14 residues. Re-reading the scanned
  Example 21 page would be needed to confirm the pairing.
- `min_dist_to_TWEAK_A_in_M2C`, `angle_*`, `dist_to_patch_centroid_A`: computed by this project on the
  frozen M2-C rank-1 model, Fn14 chain D. Inherits B32's claim ceiling — it is a predicted interface.

**Consequence for the atlas claim.** The earlier statement "5 of the 6 contact residues are within 5 Å of
TWEAK" becomes **6 of 10** (L46, K48, M50, A57, R58, H60), identical in Fn14 chains D, E and F.
The overlap is therefore **smaller in fraction (60% vs 83%)** than previously written, but it now
includes **K48**, which is itself one of the four known TWEAK-binding determinants.
The angular span over the full set is **9.4–138.9°**, unchanged in direction from the earlier correction.
