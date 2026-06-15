# Handoff #38 — Records schema: PrimarySource variants (three sign-offs + form_adv)

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-14-handoff-38-primarysource-variants.md`
**Lineage:** records layer. Global-sequential numbering; #37 was the covered-person field, so this is #38.
**Depends on:** nothing in flight. Branch off `main` (8232e0b plus #37 at be82810).
**Type:** schema. Changes `web/lib/types.ts` (the `PrimarySource` discriminated union). No collector or candidate changes; no records re-sourced here (that's downstream).

## Source the live types first

This is the rule from the two earlier schema flag-backs: do not implement against a summary of the deployed types. Step 1 is to read and quote the actual current `PrimarySource` union and reconcile the four changes below against it. The variant intents and field lists in this handoff are derived from the #35 inventory, not the live file, so where they conflict with what's deployed, the deployed file governs and you flag the conflict before writing.

## What this builds

Four changes to the `PrimarySource` union. Three are sign-offs that have been pending since May 21, now approved as drafted. The fourth adds the ADV provenance variant so ADV candidates can promote with typed sourcing.

- Activate `advocacy_report` (reserved): formal reports from advocacy and watchdog organizations, kept distinct from `press_disclosure`. CREW reports are the driving case.
- Replace `congressional_letter` (active, too narrow) with `congressional_document` carrying a `document_type` enum, so the variant covers letters, reports, hearing material, and referrals rather than letters alone.
- Activate `corporate_registration` (reserved) with a `registration_type` enum, so company-registry filings and trademark filings are one variant distinguished by type rather than separate variants.
- Add `form_adv`: ADV provenance for records promoted from ADV candidates, aligned to the ADV candidate `source_filing` shape.

These three sign-offs are approved decisions. Don't re-flag the decision itself; flag only where the live types don't match the shapes assumed here.

## Scope guardrails (apply, don't re-litigate)

- The integer category field stays the evidence-tier marker, not the union discriminant. Keep the existing discriminant.
- Adding variants is additive. Existing records on the generic/untyped shape (SC-007, SC-008, the sovereign-entity sources) must keep validating unchanged.
- This handoff defines variants. It does not re-source any record onto them. The SC-001-006 backfill and ADV promotion are separate, downstream.

## What Code needs to do

### Step 1: Quote the live union and reconcile

Read `web/lib/types.ts` and quote the current `PrimarySource` union: the discriminant, the active variants and their extra fields, and the reserved variants' current state. Find every current usage of `congressional_letter` across `web/data/` and the codebase. Reconcile the four changes below against what's deployed, and flag any conflict (a field naming convention, a discriminant detail, an existing usage) before writing.

### Step 2: Activate `advocacy_report`

Give the reserved variant its shape: at minimum the organization, a title, a publication date, and a URL. Follow the field conventions the active variants already use. Distinct from `press_disclosure`, which stays for press coverage.

### Step 3: Replace `congressional_letter` with `congressional_document`

Introduce `congressional_document` with a `document_type` enum. Starter values, extend to fit the records that will use it: `letter`, `report`, `hearing_transcript`, `testimony`, `referral`. Carry the document title, date, chamber or committee, and a URL. Migrate every `congressional_letter` usage Step 1 found to `congressional_document` with the appropriate `document_type`. If nothing currently uses `congressional_letter`, note that and just replace the definition.

### Step 4: Activate `corporate_registration`

Give the reserved variant its shape with a `registration_type` enum. Starter values, extend as needed: `company_registry`, `trademark`, `beneficial_ownership`. Carry the registry or authority, the jurisdiction, an identifier (registration or filing number), a date, and a URL.

### Step 5: Add `form_adv`

Add the variant for ADV-sourced records, aligned to the ADV candidate `source_filing` shape so a promoted record's provenance matches the candidate it came from: CRD, SEC file number, filing date, the schedule or table (e.g. `7B1`), and the fund or entry pointer. Model the typed-extras pattern on `oge_278e`.

### Step 6: Verify

- `web/lib/types.ts` compiles; `tsc` (or the repo's typecheck) is clean.
- The Next.js build passes; existing records still validate, especially the generic/untyped sources on SC-007, SC-008, and the sovereign entities.
- Any `congressional_letter` usage is migrated, with no dangling reference to the old variant name.
- The reserved variants `sanctions_designation` and `foia_release` are left as they were; only the two named here get activated.

### Step 7: Commit

Single commit: the `web/lib/types.ts` changes, any `congressional_letter` to `congressional_document` data migration, and this handoff doc. Match the commit-message convention. Don't push unless asked.

## Flag back, don't decide

- Any conflict between the shapes assumed here and the live types, per Step 1. This is the main risk.
- The enum starter values, if the records that will use them need a different set.
- Whether `congressional_document` should keep `congressional_letter` as an alias for a transition, or replace it outright (the intent is replace).
- Whether `form_adv` should carry more of the ADV candidate `source_filing` fields than listed.

## What this doesn't do

- Doesn't re-source any record. The SC-001-006 evidence backfill (applying `advocacy_report`, `congressional_document`, `corporate_registration` to those records) and ADV promotion (applying `form_adv`) are separate, downstream work.
- Doesn't activate `sanctions_designation` or `foia_release`.
- Doesn't touch collectors, candidates, or `web/data/candidates.json`.

## After this lands

- The SC-001-006 evidence backfill (Handoff #22's worksheet), now unblocked on the schema side, applying the three activated variants to those records' sources. Still research-bound to fill the worksheet.
- ADV promotion: an analyst pass turning ADV candidates (CAND-169 and on) into SC-### records with `form_adv` provenance plus the secondary-source identity work.

---

read docs/handoffs/2026-06-14-handoff-38-primarysource-variants.md and follow
