# Handoff #21 — Extend `PrimarySource` as a discriminated union, add `convergent_interest_flag`

**Date:** 2026-05-21
**Depends on:** `docs/drafts/schema-proposal-evidence-refs-v2.md` (drafted this session)
**Replaces:** Handoff #20 (superseded — kept in the log as a dead artifact)
**Status:** Mechanical. Schema changes only. No record content changes. No UI changes.

## Context

Handoff #20 was drafted against a stale read of the deployed schema. It treated `evidence_refs` as a new parallel field, unaware that `primary_sources` already existed on `Record` and was already rendered by the UI. Code caught it before pushing — exactly the failure mode the "Flag back to Corey if" clause was designed to surface.

v2 of the proposal (`schema-proposal-evidence-refs-v2.md`) corrects the premise: extend `PrimarySource` as a discriminated union keyed on `category` rather than add a parallel `evidence_refs` field. Single evidence system. UI unchanged. SC-007 and SC-008 stay valid without migration.

This handoff applies v2.

## Tasks

### 1. Extend `PrimarySource` in `web/lib/types.ts`

Convert the existing `PrimarySource` from a flat shape to a discriminated union, per v2 §1.

- Base shape carries `label`, `url?`, `retrieved_at?`.
- Active variants admitted: `oge_278e`, `ethics_agreement`, `press_disclosure`, `court_filing`, `congressional_letter`, `sec_filing`.
- Reserved variants admitted: `sanctions_designation`, `corporate_registration`, `foia_release`, `advocacy_report`.
- Only the `oge_278e` variant carries extra required fields in this pass: `filing_type` (enum, per Handoff #17), `certification_status` (enum, per Handoff #17). Plus optional `parsed_paths?: string[]` and `entry_paths?: string[]`.
- All other variants carry only the base shape. Per-category extras can be added in future handoffs as real records force them.

If the existing `OgeFilingType` and `OgeCertStatus` enums already exist somewhere in the codebase (Handoff #17 should have introduced them), reuse those. If they don't yet exist as exported types, introduce them in `web/lib/types.ts` alongside the union. The discriminated union assumes their existence.

### 2. Add `convergent_interest_flag` to the `Record` type

Optional top-level boolean. Per v2 §3.

```ts
convergent_interest_flag?: boolean;
```

Do not set the flag on any existing record. Opt-in per record. Future handoffs that add or revise records can set it where the methodology supports it.

### 3. Delete the stale root `data/records.json`

The root `data/records.json` is a 6-record artifact from the v0 scaffold. The live dataset is `web/data/records.json` (8 records). The root copy is a footgun for accidental edits.

`git rm data/records.json`. Note in commit body.

Check first that no script, build step, or import path references the root copy. If any does, surface that and pause on the deletion — the root copy might be wired up somewhere v2 didn't account for. The expected answer is "nothing references it" (it's stale scaffold), but verify before deleting.

## Verification

- `tsc --noEmit` (or equivalent typecheck) passes.
- Production build succeeds.
- All eight records (SC-001 through SC-008) still render on `sovereign-connections.vercel.app` after deploy.
- `ExpandedPanel.tsx` and `record/[id]/page.tsx` still display existing `primary_sources` entries with no visual regression.
- Records without `convergent_interest_flag` set show no UI artifact related to the new field. The flag is dormant until a record opts in and a future handoff adds rendering.
- Root `data/records.json` no longer exists in the working tree.

## Out of scope

- Backfilling SC-001 through SC-006 evidence as typed `PrimarySource` entries. Their current evidence is inline prose in `summary` ("SEC filings", "NYT and FT reporting", "CREW reporting"). Converting that to typed entries needs dockets, dates, URLs the records don't contain. Handled as Handoff #22, research-driven, per-record sign-off.
- Per-category UI rendering (e.g., showing OGE filing type as a badge, formatting court filing dockets). Future handoff once it matters.
- Per-category extras for the five non-OGE active variants. Defer per case.
- Reserved-variant internal shapes. Defer per case.
- Methodology page Section 5 revision on Category-3 direction. Drafts after this handoff verifies.

## Commit guidance

Two or three commits:

1. `feat(schema): extend PrimarySource as discriminated union, add convergent_interest_flag`
   — types.ts changes only. Note in the commit body that variants beyond oge_278e carry base shape only and per-category extras defer to future handoffs.

2. `chore(data): remove stale root data/records.json`
   — single deletion. Body notes the live dataset is at `web/data/records.json`.

3. (optional) `docs(handoffs): add 2026-05-21 handoff #21 session log`
   — if session-log convention applies.

## Flag back to Corey if

- Anything in `web/data/records.json` (the live dataset) has a `primary_sources` entry with a category value not listed in v2. v2 was drafted from the chat record of what SC-007 and SC-008 carry; if a real category appears that v2 missed, surface it before adding it silently.
- The `OgeFilingType` or `OgeCertStatus` enums from Handoff #17 conflict with what v2 implies they should be. Surface the conflict before redefining.
- Any code path references the root `data/records.json`. Stop, note where, don't delete.
- `convergent_interest_flag`'s boolean shape conflicts with what the methodology page Section 5 actually says (e.g., methodology implies an enum or a scored field). Surface before assuming the boolean is correct.
