# Schema proposal: typed `primary_sources` and `convergent_interest_flag` (v2)

**Date:** 2026-05-21
**Supersedes (in effect):** `schema-proposal-evidence-refs.md` (v1, Handoff #19)
**Status:** Revised against the actually deployed schema. Ready for Handoff #21.

## Why v2

v1 was drafted against a stale read of the record schema. Its motivating premise — "the shape has no way to point from a record at parser output or any other underlying primary record" — was already false when the proposal was written. `web/lib/types.ts` already carried:

```ts
primary_sources?: PrimarySource[];   // { label, url?, category }
```

SC-007 and SC-008 already used it. The UI already rendered it (`ExpandedPanel.tsx`, `record/[id]/page.tsx`). Applying v1 literally would have created a parallel `evidence_refs` field alongside `primary_sources`, producing two evidence systems — directly against v1's own single-structure intent.

v2 keeps v1's contribution (typed sub-schemas for OGE 278e, court filings, press disclosures, etc., plus the samples-pointer model and the `convergent_interest_flag` concept) and folds it into the existing `PrimarySource` type as a discriminated union. One evidence system. UI unchanged. SC-007 and SC-008 stay valid.

## Proposal

### 1. `PrimarySource` becomes a discriminated union keyed on `category`

The base shape (`label`, `url?`) carries across every variant. The `category` field becomes the discriminant. Variants for the six active sub-schemas from v1 are admitted; four future categories are reserved as accepted enum values with no required extra fields.

```ts
type PrimarySourceBase = {
  label: string;
  url?: string;
  retrieved_at?: string;  // ISO 8601, optional
};

type PrimarySource =
  // Active variants — extra fields permitted per category
  | (PrimarySourceBase & {
      category: 'oge_278e';
      filing_type: OgeFilingType;          // enum, per Handoff #17
      certification_status: OgeCertStatus; // enum, per Handoff #17
      parsed_paths?: string[];             // pointers into parser output
      entry_paths?: string[];              // pointers into specific entries
    })
  | (PrimarySourceBase & { category: 'ethics_agreement' })
  | (PrimarySourceBase & { category: 'press_disclosure' })
  | (PrimarySourceBase & { category: 'court_filing' })
  | (PrimarySourceBase & { category: 'congressional_letter' })
  | (PrimarySourceBase & { category: 'sec_filing' })
  // Reserved variants — accepted as enum values, shape deferred
  | (PrimarySourceBase & { category: 'sanctions_designation' })
  | (PrimarySourceBase & { category: 'corporate_registration' })
  | (PrimarySourceBase & { category: 'foia_release' })
  | (PrimarySourceBase & { category: 'advocacy_report' });
```

### 2. Only `oge_278e` gets its full v1 shape in this pass

v1 specified extra fields for all six active sub-schemas. v2 narrows the formal commitment to `oge_278e` because that's the only category with discovered, load-bearing fields (`filing_type`, `certification_status`, the parser-pointer pair). The other five active categories accept the base shape only. Per-category extras can be added in subsequent handoffs as real records force them — same discipline as the reserved variants.

Rationale: over-specifying variant shapes before a real case has exercised them tends to produce fields that the first actual record contradicts. The Handoff #17 OGE certification discovery is the cautionary case — the field wasn't visible until a real filing exposed it.

### 3. `convergent_interest_flag` as top-level optional boolean on `Record`

Methodology page Section 5 names the concept. The schema now supports it.

```ts
type Record = {
  // ... existing fields ...
  convergent_interest_flag?: boolean;
};
```

Opt-in per record. Default behavior on records without the field set is unchanged. Methodology page revision (the "Category-3 direction" note flagged in Handoff #19's decision 5) can land separately once the field is in.

### 4. Samples-pointer model still applies — through `url` and `parsed_paths`

v1's samples-pointer idea (actual content in `samples/`, records point at it via structured pointers rather than bulk-importing parsed output) survives. `PrimarySource.url` carries the external/canonical reference; the `oge_278e` variant's `parsed_paths` and `entry_paths` carry the in-repo pointers into parsed output. Same decoupling property — parser version drift doesn't force records migrations.

## What v2 does not do

- **No backfill of SC-001 through SC-006.** Those records carry evidence as inline prose in `summary` ("SEC filings", "NYT and FT reporting", "CREW reporting"). Converting that to typed `PrimarySource` entries needs dockets, publication dates, URLs — facts the records don't contain. That's research and curation, not type-system work. Handled separately as Handoff #22.
- **No UI changes.** `PrimarySource` is already rendered by `ExpandedPanel.tsx` and `record/[id]/page.tsx`. Adding variants doesn't change what the existing render needs to do for the cases it already handles. A future handoff can add category-specific rendering (e.g., showing the OGE filing type as a badge) once it matters.
- **No new collector work.** Phase 5 stays paused.

## Housekeeping

Root `data/records.json` is a stale 6-record copy from the v0 scaffold. The live deployed dataset is `web/data/records.json` (8 records). The root copy is a footgun — easy to edit by mistake. Handoff #21 deletes it as a one-line cleanup.

## Decisions preserved from v1

- Discriminated union with `category` as discriminant — Yes, just attached to `PrimarySource` rather than a new field.
- `oge_278e` carries `filing_type`, `certification_status`, `parsed_paths`, `entry_paths` — Yes, per Handoff #17.
- Four reserved category names registered without required extra shape — Yes.
- `convergent_interest_flag` at top level on `Record` — Yes, optional boolean.
- SC-007 and SC-008 entry timing — N/A under v2. Both already exist and already use `primary_sources` correctly; no migration needed.

## Outstanding

- Per-category extra fields for `ethics_agreement`, `press_disclosure`, `court_filing`, `congressional_letter`, `sec_filing`. Defer until a real case forces each one.
- Reserved variants' internal shapes (`sanctions_designation`, `corporate_registration`, `foia_release`, `advocacy_report`). Same — defer per case.
- SC-001 through SC-006 evidence curation (Handoff #22, research-driven, per-record sign-off as it goes).
- Methodology page Section 5 note on Category-3 direction. Drafts after Handoff #21 verifies.
