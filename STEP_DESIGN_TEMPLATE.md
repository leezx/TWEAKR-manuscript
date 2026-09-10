# Step <N>: <name> — design

> Write and review this BEFORE any compute or data acquisition happens.
> Everything here should be locked precisely enough that a different
> agent could implement it without asking follow-up questions about
> scope or method. Submit this doc for ChatGPT review (same persistent
> conversation, `docs/PROJECT_CHARTER.md` §2.2) and reach APPROVE before
> writing the implementation.

## Scope

<What this step covers and, as importantly, what it explicitly does
not — cite the charter's non-goals if relevant. If a prior step or an
external blocker narrowed scope (e.g. an access-gated dataset dropped
after asking the user), say so and why here.>

## Inputs

<Exact datasets/prior-step outputs this step consumes, with paths.>

## Method / contract

<The precise, locked design: data schemas, population/sample
definitions, statistical parameters (seeds, permutation counts,
thresholds), gene-axis or ID-canonicalization rules, anything with more
than one plausible interpretation. Lock the order of operations
explicitly when order matters (e.g. "canonicalize each reference to
bare IDs FIRST, assert no duplicate collisions, THEN intersect across
references — not the reverse").>

## Coverage / validity checks

<What gets checked before/alongside compute to catch a silent data
problem — e.g. a coverage-check gate with a relative-deviation rule, not
a flat floor; what happens when a check flags something (investigate
empirically, don't wave it through, don't block indefinitely either —
see charter §2.6).>

## Expected outputs

<What files this step will produce, where, in what format — so the
results doc can be written against a known target.>

## Open questions for review

<Anything you're genuinely unsure about and want the reviewer to weigh
in on, rather than silently picking an interpretation.>

---

# Step <N>: <name> — results

> Write this AFTER real compute has run. Report what actually happened,
> including anything that didn't match this design doc's pre-compute
> estimates. Do not edit the design section above to match results after
> the fact — a mismatch between estimate and reality is itself a finding
> worth keeping visible, not something to retroactively smooth over.

## Compute record

<Where it ran (cluster/job ID), wallclock, exit status, any real bugs
hit and how they were fixed — per charter §2.4's smoke-test-first
discipline, note what the smoke test caught before the full run, if
anything.>

## Real findings

<The actual numbers/outcomes. Compare against the design doc's
estimates where it made any. Report negative/unresolved findings with
the same weight as clean ones — see charter §2.6.>

## File manifest

<Every output file, with a one-line description. If any of these were
transferred to/from a cluster, note that they were md5-verified
byte-exact.>

## Review history

<Round-by-round: what the reviewer flagged, what was independently
verified and how, what was fixed vs. pushed back on with evidence, final
verdict + head commit at APPROVE.>
