# Handoff #20 — Apply `evidence_refs` schema, backfill SC-001 through SC-006

**Date:** 2026-05-21
**Depends on:** Handoff #19 (schema proposal, signed off this session)
**Status:** Mechanical. No schema design decisions remain.

## Context

Handoff #19 proposed an `evidence_refs` structure on records using the samples-pointer model: actual filing content lives in `samples/`, records reference it via typed pointers rather than bulk-importing parsed output. Six active sub-schemas defined (`oge_278e`, `ethics_agreement`, `press_disclosure`, `court_filing`, `congressional_letter`, `sec_filing`). Four reserved sub-schema names (`sanctions_designation`, `corporate_registration`, `foia_release`, `advocacy_report`) registered without internal shape.

Signed off this session. All five parked decisions resolved:

1. **Structure** — sign-off as proposed.
2. **`convergent_interest_flag` placement** — top-level on the record type. It's a record-wide analytic judgment, not evidence-specific.
3. **SC-007/SC-008 entry timing** — separate handoff. Out of scope here.
4. **Backfill scope** — all six existing records (SC-001 through SC-006) in this handoff.
5. **Category-3 methodology note** — deferred until #20 ships and is verified, then drafted as a methodology page revision.

## Tasks

### 1. Apply the schema to the record type

Update the record type definition to add `evidence_refs` as an array of typed evidence pointers, per the #19 proposal. The six active sub-schemas get full definitions. The four reserved sub-schemas are registered as accepted `type` enum values with no required internal fields beyond the shared envelope (whatever the proposal specified as the minimum across all sub-types — at least `type`, `source_id`, `retrieved_at` per prior convention; defer to the proposal if it differs).

`oge_278e` is load-bearing. Carry its `filing_type` and `certification_status` enums per the Handoff #17 discovery, plus `parsed_paths` (array of pointers into parser output) and `entry_paths` (array of pointers into specific entries within parsed output).

Add `convergent_interest_flag` as an optional top-level field on the record type. Boolean. The methodology page Section 5 already names the concept; the schema now supports it.

### 2. Backfill SC-001 through SC-006

Rewrite each existing record's evidence references against the new `evidence_refs` structure. Records to touch:

- SC-001 (Affinity Partners, pre-2025 comparative)
- SC-002 through SC-006 (whatever currently sits in the records array — verify against the deployed dataset)

For each: convert any existing inline evidence into the appropriate typed pointer. Where the existing record has evidence that doesn't fit a defined sub-schema, use the closest reserved type and leave a code comment noting the type's shape isn't formalized yet. Do not invent fields on reserved sub-schemas.

For `convergent_interest_flag`: omit on all six unless an existing record already had logic that maps to it. The flag is opt-in per record. Don't backfill a value where the prior record didn't carry the concept.

### 3. Verification

- Typecheck passes.
- Build green (matches the standard for all prior handoffs).
- All six records still render on the deployed `sovereign-connections.vercel.app` route.
- No `convergent_interest_flag` value displayed on records that don't set it.
- The methodology page is untouched in this handoff.

## Out of scope

- SC-007 / SC-008 entry — separate handoff once #20 is in.
- Category-3 direction methodology note — drafted after #20 verifies.
- Reserved sub-schema internal shapes — each waits for a case that forces it.
- Any new collector work — Phase 5 stays paused until evidence_refs is live.

## Commit guidance

Two commits, possibly three:

1. `feat(schema): add evidence_refs structure and convergent_interest_flag field`
2. `feat(records): backfill SC-001 through SC-006 against evidence_refs`
3. (optional) `docs(handoffs): add 2026-05-21 handoff #20 session log` — if you log the session as part of the same push.

If any backfill records had to use a reserved sub-schema with un-formalized fields, call that out in the commit body so it surfaces in the next handoff review.

## Flag back to Corey if

- Any existing record's evidence shape doesn't fit a defined or reserved sub-schema. Don't invent a new sub-schema mid-handoff; surface it.
- The proposal in #19 has any internal contradictions that only become visible on application. If so, stop, note where, and don't push.
- The methodology page Section 5 reference to `convergent_interest_flag` turns out to use phrasing that conflicts with the boolean shape (e.g., implies an enum or scored field). Surface before assuming.
