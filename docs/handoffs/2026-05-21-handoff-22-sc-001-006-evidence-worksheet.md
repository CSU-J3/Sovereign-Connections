# Handoff #22 — SC-001 through SC-006 evidence discovery worksheet

**Date:** 2026-05-21
**Depends on:** Handoff #21 (PrimarySource discriminated union, applied and deployed)
**Status:** Discovery only. No record content changes. No schema changes. Output is a single research worksheet.

## Context

Handoff #21 extended `PrimarySource` as a discriminated union keyed on `type`, with six active variants (`oge_278e`, `ethics_agreement`, `press_disclosure`, `court_filing`, `congressional_letter`, `sec_filing`), four reserved variants, and a generic no-`type` variant for entries that don't fit a typed shape.

SC-001 through SC-006 predate `primary_sources` adoption. Their evidence currently lives as inline prose inside the `summary` field ("SEC filings", "NYT and FT reporting", "CREW reporting", etc.). To bring them onto the new schema requires sourcing specific facts (court dockets, publication dates, URLs, filing identifiers) that the records don't contain.

That sourcing is research work, not type-system work. It belongs with Corey, not with Code. This handoff's job is to surface what each record currently says, what typed variants its evidence implies, and what's missing — so the research can be done against a structured worksheet rather than from scratch.

SC-007 and SC-008 are out of scope (they already use the new schema correctly).

## Task

Generate a single markdown worksheet at `docs/references/sc-001-006-evidence-worksheet.md`. Format below. Commit it. Make no other changes.

### Worksheet format

One top-level section per record (SC-001, SC-002, SC-003, SC-004, SC-005, SC-006). For each:

1. **Record header**: ID, title, current scope category (LIVE/COMP/LITIG/OOS), current `primary_sources` array contents (if any — likely empty or sparse).

2. **Evidence prose extracted from `summary`**: verbatim quote of any phrase in the `summary` field that names a source, document, filing, or piece of reporting. One bullet per identified phrase. Keep the surrounding context (5-10 words on either side) so the phrase is readable.

3. **Per-phrase mapping**: for each extracted phrase, propose:
   - The most likely typed variant under the new schema (`oge_278e` | `ethics_agreement` | `press_disclosure` | `court_filing` | `congressional_letter` | `sec_filing` | generic no-`type`), or one of the four reserved variants if it clearly applies (`sanctions_designation`, `corporate_registration`, `foia_release`, `advocacy_report`).
   - The fields the chosen variant requires that the record doesn't currently provide. For typed variants that don't yet have a per-category extras shape in code (everything except `oge_278e`), list the natural fields someone curating that variant would want — publication and date for press, court and docket for filings, form number and filer for SEC, etc. These are research targets, not schema commitments.
   - What's already present in the record that supports the mapping (any URL, any date already in the record, any name).

4. **Open questions**: anything ambiguous. Examples: "CREW reporting" could be `press_disclosure` (treating CREW as a publication) or `advocacy_report` (treating it as the reserved category for advocacy-organization material) — surface the ambiguity, don't pick.

5. **Coverage estimate**: rough fraction of the record's evidence claims that the worksheet has surfaced as discrete phrases. If the prose is impressionistic ("various reporting"), say so and don't invent phrases.

Do not invent dockets, dates, URLs, filing numbers, publication names, or anything else not present in the record's current text. The worksheet is a transcription-and-classification exercise, not a research exercise.

If a record has zero identifiable evidence phrases in its current text, the section says so explicitly and stops at the header.

## Verification

- Worksheet exists at `docs/references/sc-001-006-evidence-worksheet.md`.
- All six records have a section, in order.
- No record content has been changed.
- No schema has been changed.
- `tsc --noEmit` and `next build` unchanged from #21 state (since nothing else moved).
- Worksheet is committed.

## Out of scope

- Any record content edits.
- Any schema or type changes.
- Any research, lookup, or verification of dockets, URLs, dates, or filing details. Worksheet is transcription only.
- SC-007, SC-008 (already on the new schema).
- UI changes.

## Commit guidance

Single commit: `docs(references): add SC-001-006 evidence discovery worksheet`. Body notes the worksheet is input to Corey's research pass, with application of findings deferred to a follow-up handoff.

## Flag back to Corey if

- Any of SC-001 through SC-006 doesn't exist in `web/data/records.json` (renumbered, dropped, or merged). Don't invent a section; surface which IDs are present.
- A record's `summary` field is absent, empty, or carries content that doesn't read as evidence-bearing prose at all. Note it and continue.
- The schema's typed-variant enum doesn't carry one of the names assumed above (`oge_278e`, `ethics_agreement`, `press_disclosure`, `court_filing`, `congressional_letter`, `sec_filing`, `sanctions_designation`, `corporate_registration`, `foia_release`, `advocacy_report`). Surface the mismatch — #21 should have set these but worth verifying against the deployed types.
- Any record already has `primary_sources` populated beyond an empty array. The worksheet should surface what's there, not overwrite it.
