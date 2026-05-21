# Schema design proposal: records.json + evidence_refs

Status: Discussion draft. Not a Code handoff yet. Goal is for Corey to react, adjust, sign off, then a follow-up Code handoff applies the schema change.

## What the current schema does

`data/records.json` holds an array of records keyed by SC-### id. Each record carries:
- `id`, `business`, `family_member` — identifying fields, all strings
- `scope` — COMP, LITIG, OOS (no LIVE scope used yet)
- `source` — keyed to a `sovereign_entities.json` id, or special values (MULTI, CHN, NA, NONE)
- `period` — date range string
- `frameworks` — array of adjacent-framework tags (EMOL, FIRRMA, OGE, 208, FARA, LDA)
- `evidence_category` — integer array (1/2/3 per PROJECT.md's evidence hierarchy)
- `summary` — prose paragraph carrying the analytical content
- `documented_amount` — optional free-text dollar amount or descriptor

`sovereign_entities.json` is a curated table of seven SWFs with per-entity governance notes. `candidates.json` and `connected_businesses.json` exist as reserved structure but are empty.

The shape works for the six comparative/litigation/excluded records it currently holds.

## What it doesn't do

The shape has no way to point from a record at parser output (or any other underlying primary record). When SC-008 gets entered for the Witkoff / WLF case, it'll need to reference Witkoff's August 13, 2025 OGE 278e and the specific Part 6 entry paths (41, 41.8.1, 41.9.1) where the WLF interest sits. The current schema has no field for that.

Two related needs the design has to handle:
- Records with multiple primary sources (the Tahnoon-WLF case alone draws on the OGE 278e, the WSJ January 31, 2026 reporting, the House Select Committee February 4, 2026 letter, and Public Citizen's analysis). A single record needs to point at all of them.
- Records with multi-record primary sources for a single event (the $120M Witkoff divestiture is in OGE 278e Part 2 as an income line; the divestiture's terms — recipient, timing, conditions — would be in a separate OGE ethics agreement document. Two primary records, one event).

## Proposed change

Add one new optional field to records: `evidence_refs`. Array of structured evidence pointers. Each pointer has a `type` and type-specific fields. Records without `evidence_refs` work as before (the existing SC-001 through SC-006 stay untouched).

### Type: `oge_278e`

```json
{
  "type": "oge_278e",
  "filer": "Witkoff, Steven",
  "filing_date": "2025-08-13",
  "filing_type": "new_entrant",
  "certification_status": "filer_signed_only",
  "sample_path": "data/samples/witkoff-oge278-2025-08-13.pdf",
  "parsed_paths": [
    "data/samples/witkoff-oge278-2025-08-13-part2.json",
    "data/samples/witkoff-oge278-2025-08-13-part6.json"
  ],
  "entry_paths": ["41", "41.8.1", "41.9.1"],
  "notes": "Witkoff Holdings parent (#41) + WLF (41.8.1) + SC Financial Technologies (41.9.1) + $120M Witkoff Group divestiture (Part 2 #1)"
}
```

`filing_type` enum: `new_entrant`, `annual`, `amendment`, `termination`.
`certification_status` enum: `filer_signed_only`, `ethics_certified`, `oge_certified`, `amended_post_certification`.

### Type: `ethics_agreement`

```json
{
  "type": "ethics_agreement",
  "filer": "Witkoff, Steven",
  "filing_date": "TK",
  "url_or_sample_path": "TK"
}
```

Placeholder structure. Lets a record cite the ethics agreement as a separate evidence record from the 278e, even when the agreement document itself isn't yet retrieved.

### Type: `press_disclosure`

```json
{
  "type": "press_disclosure",
  "publisher": "Wall Street Journal",
  "date": "2026-01-31",
  "url": "https://www.wsj.com/politics/policy/spy-sheikh-secret-stake-trump-crypto-tahnoon-ea4d97e8",
  "title": "'Spy Sheikh' Bought Secret Stake in Trump Company",
  "byline": "Sam Kessler, Rebecca Ballhaus, Eliot Brown, Angus Berwick",
  "establishes": "$500M Tahnoon vehicle transaction; $187M to Trump family entities; $31M to Witkoff entities"
}
```

### Type: `court_filing`

```json
{
  "type": "court_filing",
  "case": "District of Columbia and Maryland v. Trump",
  "docket": "8:17-cv-01596-PJM",
  "court": "D. Md.",
  "filing_date": "2017-06-12",
  "url": "https://www.citizensforethics.org/legal-action/lawsuits/dc-md-trump-emoluments/"
}
```

### Type: `congressional_letter`

```json
{
  "type": "congressional_letter",
  "committee": "House Select Committee on the Strategic Competition Between the United States and the Chinese Communist Party",
  "signers": ["Ro Khanna"],
  "date": "2026-02-04",
  "addressee": "Zach Witkoff (World Liberty Financial)",
  "url": "https://democrats-selectcommitteeontheccp.house.gov/sites/evo-subsites/.../2-4-26-scc-letter-to-wlf.pdf"
}
```

### Type: `sec_filing`

```json
{
  "type": "sec_filing",
  "filer": "Apollo Commercial Real Estate Finance Inc.",
  "form": "10-K",
  "filing_date": "TK",
  "url": "TK",
  "establishes": "QIA position in ARI (common + preferred)"
}
```

### Other types — reserved

`sanctions_designation`, `corporate_registration`, `foia_release`, `advocacy_report` (e.g., Public Citizen, CREW). Add when first needed.

## Worked example: SC-008 under the proposed schema

```json
{
  "id": "SC-008",
  "business": "World Liberty Financial Inc.",
  "family_member": "Donald Trump Jr., Eric Trump, Barron Trump (co-founders); Steve Witkoff (covered intermediary per v2.0)",
  "scope": "LIVE",
  "source": "MULTI",
  "period": "2024-PRES",
  "frameworks": ["EMOL", "OGE", "208"],
  "evidence_category": [1, 2],
  "documented_amount": "$500M Tahnoon vehicle (49% stake, Jan 16 2025); $187M to Trump family entities at signing; $31M to Witkoff entities; $2B MGX-Binance settlement via USD1 (May 1 2025)",
  "summary": "v2.0 worked case. Tahnoon bin Zayed Al Nahyan's controlling-interest chain to UAE sovereign vehicles satisfies the sovereign-source test through his official roles (UAE National Security Advisor) plus chairmanship of ADQ, IHC, G42, MGX. Trump family co-founder status documented in corporate filings; Witkoff family interests documented in OGE 278e. Convergent-interest flag attaches: same transaction sends documented value to both a covered intermediary (Witkoff) and named family members of the principal.",
  "convergent_interest_flag": true,
  "evidence_refs": [
    { "type": "oge_278e", "filer": "Witkoff, Steven", "filing_date": "2025-08-13", "filing_type": "new_entrant", "certification_status": "filer_signed_only", "sample_path": "data/samples/witkoff-oge278-2025-08-13.pdf", "parsed_paths": ["data/samples/witkoff-oge278-2025-08-13-part6.json"], "entry_paths": ["41", "41.8.1", "41.9.1"], "notes": "WLF and SC Financial Technologies nested under Witkoff Holdings" },
    { "type": "press_disclosure", "publisher": "Wall Street Journal", "date": "2026-01-31", "url": "https://www.wsj.com/politics/policy/spy-sheikh-secret-stake-trump-crypto-tahnoon-ea4d97e8", "title": "'Spy Sheikh' Bought Secret Stake in Trump Company", "byline": "Sam Kessler, Rebecca Ballhaus, Eliot Brown, Angus Berwick", "establishes": "$500M Tahnoon vehicle transaction; allocations to Trump family and Witkoff entities" },
    { "type": "congressional_letter", "committee": "House Select Committee on the Strategic Competition Between the United States and the Chinese Communist Party", "signers": ["Ro Khanna"], "date": "2026-02-04", "addressee": "Zach Witkoff (World Liberty Financial)", "url": "https://democrats-selectcommitteeontheccp.house.gov/sites/evo-subsites/.../2-4-26-scc-letter-to-wlf.pdf" },
    { "type": "advocacy_report", "publisher": "Public Citizen", "title": "Conflict Coin", "url": "https://www.citizen.org/article/trump-crypto-world-liberty-financial-binance-iran-sanctions/" }
  ]
}
```

Note the new `convergent_interest_flag` field. Methodology page Section 5 already names this as a record-level field for v2.0; the schema needs to support it. Defaults to `false` or absent on records where it doesn't apply.

## Backward compatibility

`evidence_refs` and `convergent_interest_flag` are optional. SC-001 through SC-006 keep working without either field. Backfill is a separate hand-curation decision per existing record.

## What's NOT in scope for this proposal

- Splitting records into separate evidence and records tables. Single-layer architecture preserved.
- Populating `connected_businesses.json` as a normalized entity table. Worth doing eventually, but currently records carry the business name inline as a string and that works.
- Dirty-entity-name handling (form typos like "WHO II Mezz LLC"). Punt until cross-record entity-matching becomes necessary.
- 5 CFR 2640.103(a) category inference. Methodology says this is inferential; inference is a query-time concern, not a record-storage concern.

## Methodology items that don't translate to schema changes

- **Category-3 direction.** Versioned PROJECT.md note clarifying filer-as-creditor vs filer-as-debtor. No schema impact.
- **Certification status semantics.** Schema captures the enum values; the methodology page may want a brief note on what the four certification states mean for the evidence hierarchy.

## Decisions for Corey

1. **Sign off or override** on the `evidence_refs` structure as drafted above. Adjust the type-specific shapes if anything looks wrong for how you want to use them.
2. **`convergent_interest_flag` placement.** Currently proposed as a top-level record field. Alternative: nest it inside a `v2_metadata` object. Top-level is simpler; nested keeps record root cleaner if more v2.0-specific fields accumulate.
3. **SC-007 / SC-008 entry.** Records.json currently stops at SC-006. Do SC-007 (probably Tahnoon-WLF as a Tahnoon-source distinct record?) and SC-008 (Witkoff worked case) get entered as part of this schema rollout, or as separate handoffs after the schema lands?
4. **Backfill scope.** Any of SC-001 through SC-006 that should get `evidence_refs` added retroactively? SC-001 (Affinity Partners) and SC-006 (Burisma) both have meaningful primary-source records that could be cited. SC-002, SC-003 are diffuse and might not justify backfill. SC-004, SC-005 are litigation records with one obvious court_filing each.
5. **Methodology adjudications.** Ready to write up the category-3 direction note for PROJECT.md as part of this rollout, or punt to a separate methodology handoff?

Once these are settled, the follow-up Code handoff is straightforward: extend the schema, add an optional `evidence_refs` validator, optionally backfill the records you want backfilled. No structural rework.
