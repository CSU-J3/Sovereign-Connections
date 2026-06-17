# Handoff #47 — Retype SC-007 / SC-008 primary_sources to the typed union

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-47-retype-sc007-sc008-sources.md`
**Depends on:** #45 (on main; it set the three SC-007 and one SC-008 congressional categories to 2). Branch off `main`.
**Type:** data (`web/data/records.json`).

## What this does

Adds `type` discriminators and the variant-specific fields to the SC-007 and SC-008 primary_sources that map to a union variant, bringing them in line with SC-002/006/009. Sources with no matching variant stay untyped, which is the schema's generic shape and explicitly valid (the `PrimarySource` comment names SC-007 and SC-008 as the untyped shape). Both records stay intentionally mixed: typed where a variant fits, untyped otherwise. That is the expected end state, not an incomplete one.

## Hard constraints

- ADD `type` and the typed fields only. Do not change any existing `label`, `url`, `category`, or `retrieved_at`. The categories were set by #45; preserve them exactly.
- Match each source by its exact `label`. Leave every source listed as "untyped (unchanged)" exactly as-is.
- After editing, validate JSON and the union: each typed source must carry its required fields (`oge_278e` needs `filing_type` + `certification_status`; `congressional_document` needs `document_type`; `advocacy_report` needs `organization`).

## Verified field value (the one non-mechanical call)

The Witkoff OGE Form 278e (cited in both records) is filer-signed only. Witkoff e-signed it 08/13/2025; no agency ethics official and no OGE certification followed, and it remained uncertified as of April 2026. So `certification_status` = `filer_signed_only`. Source: the public 278e on whitehouse.gov, corroborated by the Warren-Murphy letter and the Democracy Defenders Fund disclosure.

## SC-007 (16 sources)

**Type these:**

- `Witkoff OGE Form 278e (New Entrant Report, August 13, 2025)` → `oge_278e`; `filing_type`: `new_entrant`, `certification_status`: `filer_signed_only`.
- `House Select Committee on the CCP, letter to Zach Witkoff, February 4, 2026` → `congressional_document`; `document_type`: `letter`, `chamber_or_committee`: `House Select Committee on the CCP`, `document_date`: `2026-02-04`.
- `Warren-Murphy letter on Witkoff OGE form ethics-officer signoff, November 2025` → `congressional_document`; `document_type`: `letter`, `chamber_or_committee`: `U.S. Senate`. (No exact day in the label; omit `document_date`, or pin it from the letter PDF.)
- `NYT, 'Where Mideast Envoy Pitched Peace, His Son Pitched Investors' ...` → `press_disclosure`.
- `WSJ, 'Spy Sheikh Secret Stake Trump Crypto Tahnoon' series, January 31, 2026` → `press_disclosure`.
- `Public Citizen analysis of WSJ-reported documents, January 2026` → `advocacy_report`; `organization`: `Public Citizen`. (Month-only date; omit `published_at`.)
- `Dawn (Pakistan), 'Pakistan signs MoU with Donald Trump-linked World Liberty Finance', January 14, 2026` → `press_disclosure`.
- `CoinDesk, 'Pakistan regulator inks MoU with WLFI-linked crypto business ...', January 14, 2026` → `press_disclosure`.
- `Warren-Merkley letter to the MGX and Binance CEOs (Senate Banking Committee, June 11, 2025) ...` → `congressional_document`; `document_type`: `letter`, `chamber_or_committee`: `Senate Banking Committee`, `document_date`: `2025-06-11`.

**Leave untyped (unchanged):**

- `WLF corporate documentation (capital structure, founders, profit-distribution terms)` — internal corporate docs, no variant.
- `PVARA official statement on SC Financial Technologies MOU, January 14, 2026` — foreign-regulator statement, no variant.
- `Binance announcement of $2B MGX investment ..., X, March 12, 2025` — company's own announcement, not press coverage.
- `Zach Witkoff statement that MGX's Binance investment settled in WLF's USD1 ..., Token2049 Dubai ...` — individual public statement, no variant.
- `USD1 stablecoin reserve documentation identifying World Liberty Financial, Inc. and SC Financial Technologies, LLC ...` — issuer documentation, no variant.
- `BitGo USD1 Reserve Reports (monthly attestation packages ...)` — attestation packages, no variant.
- `Mubadala official announcement co-announcing the creation of MGX ...` — company's own announcement, not press coverage.

## SC-008 (6 sources)

**Type these:**

- `Witkoff OGE Form 278e (New Entrant Report, August 13, 2025)` → `oge_278e`; `filing_type`: `new_entrant`, `certification_status`: `filer_signed_only`. (Same filing as SC-007.)
- `Warren-Murphy letter on Witkoff OGE form ethics-officer signoff, November 2025` → `congressional_document`; `document_type`: `letter`, `chamber_or_committee`: `U.S. Senate`. (Same letter as SC-007; type it identically.)
- `Reuters reporting on the Roosevelt Hotel MOU and Pakistan IMF context, February 2026` → `press_disclosure`.
- `Commercial Observer, 'Trump Envoy Steve Witkoff, Pakistani Government Plan Roosevelt Hotel Redevelopment', February 26, 2026` → `press_disclosure`.
- `Bisnow New York, 'Steve Witkoff Strikes U.S.-Pakistan Deal To Redevelop Manhattan Hotel', February 20, 2026` → `press_disclosure`.

**Leave untyped (unchanged):**

- `Pakistan Finance Division statement on Roosevelt Hotel MOU, February 19, 2026` — foreign-government statement, no variant.

## Optional, recommended (separate from the typing)

Both `oge_278e` sources currently have no `url`. The public filing is at `https://www.whitehouse.gov/wp-content/uploads/2025/09/Witkoff-Steven.pdf` (verified). Adding it links a category-1 anchor that's currently unlinked. Include it on both `oge_278e` sources if you want, or skip to keep this PR typing-only.

## Verify

- Every "type these" source carries its `type` and required fields; categories unchanged.
- Every "untyped (unchanged)" source is identical to before.
- No `label`/`url`/`category`/`retrieved_at` changed anywhere, except the optional 278e `url` add if taken.
- JSON valid; union satisfied.
- Net: SC-007 gains 9 typed sources (7 stay untyped); SC-008 gains 5 typed sources (1 stays untyped).

## Commit

Single commit, `records.json` plus this handoff. Suggested:

```
data: type SC-007/SC-008 primary_sources against the union (#47)
```

Do not push unless asked.

## Flag back, do not decide

- Any source where the type assignment looks wrong against the full label text on disk. You have the complete labels; I worked from them, but surface anything I compressed.
- If the project convention is full-date-only for `document_date`/`published_at`, the month-only ones are already omitted; pin them from the source docs if you want them populated.

## Out of scope

- The untyped sources (deliberately left; the schema blesses the generic shape).
- Categories, labels, any other record.
- Sovereign-entity sources (also untyped; a separate pass if ever wanted).

---

read docs/handoffs/2026-06-16-handoff-47-retype-sc007-sc008-sources.md and follow
