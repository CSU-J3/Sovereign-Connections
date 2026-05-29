# OGE Form 278e Parser — Behavior and Known Limits

Parser for OGE Form 278e financial disclosure PDFs. Scope: **Parts 2, 5, and 6**
— the three sections whose six-column asset layout maps to the tracker's
financial-interest definition.

- Module: `collectors/oge_278/parser.py`
- Input (pilot): `data/samples/witkoff-oge278-2025-08-13.pdf`
- Output (pilot): `data/samples/witkoff-oge278-2025-08-13-part2.json`,
  `-part5.json`, `-part6.json`
- Run: `.venv/Scripts/python -m collectors.oge_278.parser` (Windows) /
  `.venv/bin/python -m collectors.oge_278.parser` (macOS/Linux). An alternate
  PDF path may be passed as `argv[1]`.
- History: Handoff #18 built the Part 6 pilot; Handoff #19 generalized it to
  Parts 2 and 5.

## The three sections

Parts 2, 5, and 6 share an **identical six-column layout** — `#`, Description,
EIF, Value, Income type, Income amount — with the same column x-anchors. The
parser is therefore a single `parse_section(pdf_path, start_marker, end_marker)`
function; only the bounding part-title markers differ (the `SECTIONS` table in
the module).

| Part | Form title | Holds | Pilot result |
|---|---|---|---|
| 2 | Filer's Employment Assets & Income and Retirement Accounts | filer's business/employment assets — incl. the $120M Witkoff Group divestiture | 6 entries |
| 5 | Spouse's Employment Assets & Income and Retirement Accounts | 18 USC 208(a)(2) imputed spousal interests | 9 entries |
| 6 | Other Assets and Income | the bulk of the holdings | 271 entries |

**No layout divergence between the three.** Same column anchors, same header
structure, same wrapping behavior. The only Part 2/5-specific observation is
content, not layout: Part 2 entry #1's income type is an unusually long phrase
("Proceeds from the sale of an interest in the company as part of divestiture
planning") that wraps across six lines within the income-type column — handled
by the existing field-accumulation logic with no new heuristic.

### A note on the Part 2 vs Part 3 title

Handoff #19 refers to Part 2 as "Employment Agreements and Arrangements". That
is actually the title of **Part 3**. The numbered Part 2 is "Filer's Employment
Assets & Income and Retirement Accounts", and that is where the $120M Witkoff
Group divestiture is reported (entry #1's income line). The parser targets the
numbered Part 2, per the handoff's unambiguous correctness test. Part 3 — the
real "Employment Agreements and Arrangements" — contains only a lifetime
health-insurance arrangement in this filing and is not parsed (see below).

## Result on the pilot

**Part 2 — 6 entries.** Entry #1 "The Witkoff Group LLC (real estate management
company)": value "Over $50,000,000", income type "Proceeds from the sale of an
interest in the company as part of divestiture planning", income amount
**$120,000,000**. Sub-entries 1.1 (WG Development LLC), 1.2 / 1.2.1 (WG Aviation
V LLC / Aircraft), 1.3 / 1.3.1 (WG Aviation Heli I LLC / Aircraft) all nest
correctly.

The $120M divestiture comes through with its **amount** and the divestiture
descriptor. It has **no recipient and no conditional terms** — not because the
parser drops them, but because OGE Form 278e Part 2 has no fields for them. A
divestiture's recipient and conditional terms ("upon Senate confirmation", a
90-day completion window, etc.) live in a separate OGE *ethics agreement*
document, not on the 278e. Handoff #19's correctness test allows for this with
its "recipient (if printed)" hedge: here, they are not printed.

**Part 5 — 9 entries.** Entry #1 is the account ("IRA"); 1.1–1.8 are its
holdings (Macerich, Net Lease Office Properties, Regency Centers, Sabra Health
Care REIT, Ventas, W.P. Carey, a U.S. bank cash position, and the UBS Select
Treasury fund). Valuation ranges, income types, income ranges, and EIF flags all
extract correctly; the single-level nesting is preserved.

**Part 6 — 271 entries**, unchanged from the Handoff #18 result (62 contiguous
top-level entries, nesting up to 8 levels, the WLF interest chain at 41 / 41.8.1
/ 41.9.1). Its output file was regenerated only to add the `parsed` flag.

### Empty-section handling

Every section document carries `"parsed": true`. A section that parsed cleanly
but reported no entries is represented as `"parsed": true` with `"entries": []`
and `"entry_count": 0` — distinct from a section that was never run (no file).
Witkoff's Part 5 is not empty, but the flag is emitted uniformly so a future
empty section is unambiguous.

## pdfplumber strategy

`pdftotext -layout` (used in the Handoff #17 discovery) misaligns this form: it
floats wrapped fields and splits entry numbers. The parser instead works from
**word coordinates**, which are stable on this form revision.

1. **Per-page words.** `page.extract_words()` yields every word with `x0` / `top`
   coordinates. The form is A4 landscape (842 pt wide).
2. **Row grouping.** Words are sorted by `(top, x0)` and grouped into rows: a new
   row begins when a word's `top` exceeds the current row's anchor by more than
   5 pt. Wrapped lines fall into separate rows; words on one visual line cluster.
3. **Column assignment by `x0`.** The six columns have stable header anchors —
   `#`@35, `DESCRIPTION`@78, `EIF`@383, `VALUE`@469, `INCOME TYPE`@556,
   `INCOME AMOUNT`@643 — and each word is routed to a column by `x0` against
   boundaries set in the gaps (`COL_*` constants in the module).
4. **Section bounding.** Each section is bounded by its part-title rows. A
   part-title row matches `^\d+\.\s` and carries the section name; parsing
   begins after the start title and stops at the end title. Because the data
   sections precede the "Summary of Contents" restatement, matching the first
   start title and first end title isolates the data section.
5. **Page furniture** — repeated column-header rows and the
   "Witkoff, Steven C - Page N" footers — is dropped by content test.

## Heuristics

- **Entry detection.** A row whose `#`-column token matches
  `^\d+(?:\.\d+)*\.?$` starts a new entry. Every other in-section row is a
  continuation of the current entry; its column words append to the matching
  field.
- **Wrapped entry numbers.** The `#` column is narrow, so deep numbers wrap
  (`41.3.1.` then `1` → `41.3.1.1`). When an assembled number ends with `.`, the
  next row's leading `#`-column fragment completes it (looping for numbers that
  wrap more than once). Trailing dots are stripped at finalization.
- **Parent inference.** Nesting is derived purely from the dotted number:
  immediate parent of `41.8.1` is `41.8`, of `41.8` is `41`. If an exact parent
  is absent, the parser walks up until an existing ancestor is found. The output
  JSON is a genuine tree (`children` arrays), not a flat list.
- **Wrapped descriptions / values / income.** Entity names, value ranges, and
  income fields routinely wrap; continuation rows append to the relevant column
  accumulator, joined with single spaces at finalization. This reconstructs
  ranges like `$1,000,001 - $5,000,000`, `None (or less than $1,001)`, and the
  six-line Part 2 divestiture income-type string correctly.
- **Endnote markers.** "See Endnote" is detected by text and recorded as a
  boolean `has_endnote` rather than polluting the entity name or EIF value. The
  endnote *text* is not yet pulled in.

No new heuristics were needed for Parts 2 and 5 — the Part 6 logic carried over
exactly, as expected.

## Conventions (carried from Handoff #18)

- **Immediate-parent nesting.** Parent of `41.8.1` is `41.8`, not `41`; the full
  ancestor chain is recoverable by walking the dotted number.
- **Faithful-to-print transcription.** Entity names are copied exactly as
  printed, including the form's own typos (the pilot prints "WHO II Mezz LLC"
  for "WEHO II Mezz LLC"). Downstream consumers must not assume clean names.

## Known cases where the parser would break

- **Different form revisions.** Column `x0` anchors are calibrated to the
  "Updated 08/2024" revision. A revision with shifted columns needs the `COL_*`
  constants re-calibrated; the parser does not auto-detect column positions.
- **Scanned (image) PDFs.** This pilot is text-based. A scanned filing yields no
  words from `extract_words()` and needs an OCR pre-pass.
- **Hand-written annotations / amendments** are not on the column grid and would
  be mis-routed or dropped.
- **Faithful-to-print transcription** means form typos pass straight through.
- **Row-grouping tolerance.** The 5 pt tolerance suits this form's spacing; a
  filing with tighter line spacing could merge two lines into one row.
- **A column-spanning field** (a value or income string overrunning its column
  band) would split across two fields.

## Not yet parsed

- **Part 1** (Filer's Positions Held Outside US Government) — deferred. It uses a
  *different* column set (Organization Name / City-State / Position Type-Held /
  From / To) with its own date-wrapping problem, and does not reuse the
  six-column logic. It still matters to the tracker: Part 1 establishes the
  *connected-business* link and the filer's officer/managing-member position.
  Its own handoff.
- **Parts 3, 4, 7–12** — not parsed, and as of now they do **not** map to the
  tracker's financial-interest definition:
  - Part 3 (Employment Agreements and Arrangements), Part 4 (Sources of
    Compensation over $5,000) — relationship context, not a financial interest.
  - Part 7 (Transactions), Part 9 (Gifts) — `N/A` on a New Entrant Report.
  - Part 8 (Liabilities) — filer-as-debtor, which does not map to the tracker's
    category-3 (family-member-as-creditor); see the Handoff #17 discovery.
  Revisit if the methodology adds new evidence categories.
- **Endnote resolution** — `has_endnote` is a boolean; the linked endnote text
  is not extracted.
- **Reporting-period dates** — Parts 2/5/6 print none at the entry level;
  `reporting_period` is always `null`.
- **Cover-page certification block** — the parser reads only the Part 2/5/6
  asset tables, not the 278e cover page, so it emits **no**
  `certification_status` / `filing_type`. The part docs carry `report_type`
  ("New Entrant Report") and `form` as the closest available provenance, and the
  OGE-278 candidate records (Handoff #23) attach those under `source_filing`.
  Extracting the cover-page ethics-officer signoff is **deferred until a
  promotion decision (`CAND-###` → `SC-###`) actually needs it** — see PR #1
  deferral #1 (https://github.com/CSU-J3/Sovereign-Connections/pull/1).
- **Canonical record schema mapping** and **5 CFR 2640.103(a) category
  inference** — separate design work (Handoff #23).
- **Range normalization** — ranges are emitted as printed strings, not numeric
  bounds.

## Recommended Handoff #23

Canonical record schema design — landed as Handoff #23
(`docs/handoffs/2026-05-28-handoff-23-oge-278-candidate-schema.md`; numbering is
global-sequential across lineages). The parser now reads every Part of OGE 278e
that maps to the tracker's financial-interest definition (2, 5, 6); the open
design questions — how a parsed entry becomes an SC-### record, how the 5 CFR
2640.103(a) category is inferred, how `certification_status` and imputed spousal
interests are represented, where the nested structure is preserved versus
flattened — are substantive and want Corey-level input, not Code-only execution.
