# Handoff #37 — Candidate schema: covered-person field

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-14-handoff-37-candidate-covered-person-field.md`
**Lineage:** ADV/IAPD (cross-collector). Global-sequential numbering; #36 was writer unification, so this is #37.
**Depends on:** Handoff #36 (the shared writer, the ADV seed, the ADV package), now on main at 8232e0b. Branch off `main`.
**Type:** build. A candidate-schema field plus its backfill across both collectors. No `records.json` or `web/lib/types.ts` changes; this is the Python/JSON candidate layer.

## What this builds

A `covered_person` field on every candidate, naming the administration-connected person whose tie to the business the candidate documents. It closes the gap flagged in #35: an ADV candidate names the adviser (filer) and the fund (business_name) but not Kushner, the reason the candidate matters.

The field is uniform across sources, populated source-appropriately:

- ADV: from the seed. The seed is the list of covered-person-connected advisers, so the connection is known at collection, not inferred. Affinity (CRD 315482) maps to Kushner.
- OGE: from `filer`. An OGE 278 is filed by the covered person, so for OGE `covered_person` equals `filer`. That duplicates `filer` for OGE, but a single field that answers "which covered person" regardless of source is worth the redundancy.

## Scope guardrails (apply, don't re-litigate)

- Global sequential `CAND-###` IDs unchanged; the field is additive, IDs stay 1-171.
- Candidate-layer values stay source-faithful, normalization deferred to records (the #35 casing call).
- Seeded-not-universal model stands; seed is still Affinity only.
- `connected_businesses.json` registry still deferred; `business_id: null`.

## What Code needs to do

### Step 1: Add `covered_person` to the candidate shape

Add it as a top-level candidate field, alongside `filer` and `business_name`, in whatever defines the candidate shape for emission. A name string. Document it in `docs/collectors/candidate-schema-notes.md` (the file #36 created): what it carries, and that OGE populates it from `filer` while ADV populates it from the seed.

### Step 2: Enrich the ADV seed

The seed gains a covered person per entry. The required pair is the CRD and the covered person; an adviser name is optional for readability. For the one current entry: CRD 315482, covered person Kushner. Author the covered-person value in the form it carries in the source where practical (the Schedule A owner name the ingest already pulls), so candidate-layer values stay as source-faithful as the OGE `filer` they sit beside. If matching the Schedule A form reads worse than a clean name, flag it.

### Step 3: Populate on emission

- ADV emission reads `covered_person` from the seed entry for the CRD being run and stamps it on every candidate from that adviser.
- OGE emission sets `covered_person` equal to the row's `filer`.

### Step 4: Regenerate and confirm, don't hand-edit

Don't surgically patch `candidates.json`. Run both collectors so the shared writer regenerates each source's slice through the new emission. The added field rides on the existing rows, which keep their IDs by entity key. Then confirm:

- `covered_person` is present and non-empty on all 171 candidates.
- OGE rows carry `covered_person` equal to their `filer`; the three ADV rows carry the seed's covered person.
- IDs are still 1-171 with no gaps; valid JSON.
- Both collectors re-run zero-diff.
- Both regression guards pass (their regenerated expected output now includes the field).

### Step 5: Commit

Single commit: the schema-note update, the seed enrichment, the emission changes in both collectors, the regenerated `candidates.json`, and this handoff doc. Match the commit-message convention. Don't push unless asked.

## Flag back, don't decide

- Field shape. This handoff sets `covered_person` as a name string. If a basis or relationship (officeholder, family member, covered intermediary, per PROJECT.md) is wanted on the candidate now rather than left to the seed and the records layer, that's a one-field addition; surface it rather than assuming.
- The ADV seed's covered-person form, if the Schedule A verbatim reads worse than a clean authored name.
- Whether OGE carrying `covered_person` as a duplicate of `filer` is acceptable, versus any change to `filer` itself (the recommendation is keep both for uniformity).

## What this doesn't do

- Doesn't add the `form_adv` PrimarySource variant or the three schema sign-offs pending from May 21. Those are the records layer and they're what open promotion; they're a separate handoff plus your sign-off.
- Doesn't expand the seed beyond Affinity.
- Doesn't add a covered-person basis or category field (deferred unless flagged in Step 1).
- Doesn't touch `records.json` or `web/lib/types.ts`.

## After this lands

- The records-layer `form_adv` PrimarySource variant plus the three May sign-offs (`advocacy_report`, `congressional_document`, `corporate_registration`), which together let ADV candidates promote to SC-### records.
- Covered-adviser inventory to grow the seed list beyond Affinity, derived from the covered-persons definition in PROJECT.md.

---

read docs/handoffs/2026-06-14-handoff-37-candidate-covered-person-field.md and follow
