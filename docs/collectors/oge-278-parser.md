# OGE Form 278e Parser — Behavior and Known Limits (Handoff #18)

Pilot parser for OGE Form 278e financial disclosure PDFs. Scope: **Part 6 only**
("Other Assets and Income"), the section that feeds the most financial-interest
records into the tracker and carries the form's worst layout problem.

- Module: `collectors/oge_278/parser.py`
- Input (pilot): `data/samples/witkoff-oge278-2025-08-13.pdf`
- Output (pilot): `data/samples/witkoff-oge278-2025-08-13-part6.json`
- Run: `.venv/Scripts/python -m collectors.oge_278.parser` (Windows) /
  `.venv/bin/python -m collectors.oge_278.parser` (macOS/Linux). An alternate
  PDF path may be passed as `argv[1]`.

## Result on the pilot

271 Part 6 entries extracted: 62 contiguous top-level entries (1–62), nested up
to 8 levels deep. No empty entity names, no orphaned entries. The three entries
the methodology depends on come out correctly:

| Entry | Entity | Parent | EIF | Value / Income |
|---|---|---|---|---|
| `41` | Witkoff Holdings LLC | (root) | No | Over $50,000,000 / Distributions $34,363,535 |
| `41.8.1` | World Liberty Financial (cryptocurrency) | `41.8` | N/A | — |
| `41.9.1` | SC Financial Technologies LLC (stablecoin) | `41.9` | N/A | — |

The 15 `has_endnote` flags match the form's Endnotes table exactly.

## pdfplumber strategy

`pdftotext -layout` (used in the Handoff #17 discovery) misaligns this form: it
floats wrapped fields and splits entry numbers. The parser instead works from
**word coordinates**, which are stable on this form revision.

1. **Per-page words.** `page.extract_words()` yields every word with `x0` / `top`
   coordinates. The form is A4 landscape (842 pt wide).
2. **Row grouping.** Words are sorted by `(top, x0)` and grouped into rows: a new
   row begins when a word's `top` exceeds the current row's anchor by more than
   5 pt. Wrapped lines (~10–20 pt apart) fall into separate rows; words on one
   visual line cluster together.
3. **Column assignment by `x0`.** The six columns have stable header anchors —
   `#`@35, `DESCRIPTION`@78, `EIF`@383, `VALUE`@469, `INCOME TYPE`@556,
   `INCOME AMOUNT`@643 — and each word is routed to a column by `x0` against
   boundaries set in the gaps (`COL_*` constants in the module).
4. **Section bounding.** Parsing starts after the row containing
   "Other Assets and Income" and stops at the Part 7 ("Transactions") title row.
   This naturally excludes the Part 5 spouse rows that share Part 6's first
   physical page, and the "Summary of Contents" restatement of the Part 6
   heading later in the document.
5. **Page furniture** — repeated column-header rows and the
   "Witkoff, Steven C - Page N" footers — is dropped by content test.

## Heuristics that proved necessary

- **Entry detection.** A row whose `#`-column token matches
  `^\d+(?:\.\d+)*\.?$` starts a new entry. Every other in-section row is treated
  as a continuation of the current entry, and its column words are appended to
  the matching field.
- **Wrapped entry numbers.** The `#` column is narrow, so deep numbers wrap:
  the PDF renders `41.3.1.1` as `41.3.1.` on one line and `1` on the next. When
  an assembled number ends with `.`, the parser expects the next row's leading
  `#`-column fragment to complete it, and appends it (looping for numbers that
  wrap more than once). Trailing dots are stripped at finalization.
- **Parent inference.** Nesting is derived purely from the dotted number:
  parent of `41.8.1` is `41.8`, of `41.8` is `41`, of `41` is none. If an exact
  parent number is somehow absent, the parser walks up the dotted path until an
  existing ancestor is found — a guard against numbering gaps. The output JSON
  is a genuine tree (`children` arrays), not a flat list.
- **Wrapped descriptions / values / income.** Entity names, value ranges, and
  income amounts routinely wrap across lines (`Over` / `$50,000,000`;
  `Members club, marina, hotel and hotel condo` / `development, Hallandale, FL`).
  Continuation rows append to the relevant column accumulator; fields are joined
  with single spaces at finalization, which reconstructs ranges like
  `$1,000,001 - $5,000,000` and `None (or less than $1,001)` correctly.
- **Endnote markers.** "See Endnote" sits between the description and EIF
  columns. Its tokens are detected by text and recorded as a boolean
  `has_endnote` rather than polluting the entity name or EIF value. The endnote
  *text* itself (in the form's Endnotes table) is not yet pulled in.

## Note on the handoff's parent definition

Handoff #18 §Step-2 parenthetically says "for `41.8.1`, parent is `41`". The
parser instead records the **immediate** parent (`41.8`), because the same
handoff's correctness test requires `41.8.1` to nest "under WC Digital Fi LLC"
— and WC Digital Fi LLC *is* entry `41.8`. Immediate-parent nesting is the
faithful reading and is what Step 3 ("parent-child relationships preserved, not
flattened") asks for. The top-level ancestor (`41`) is always recoverable by
walking the dotted number.

## Known cases where the parser would break

- **Different form revisions.** Column `x0` anchors are calibrated to the
  "Updated 08/2024" revision. An earlier or later revision with shifted columns
  would need re-calibration of the `COL_*` constants. The parser does not yet
  auto-detect column positions from the header row.
- **Scanned (image) PDFs.** This pilot PDF is text-based. A scanned filing would
  yield no words from `extract_words()` and need an OCR pre-pass.
- **Hand-written annotations / amendments** overlaid on the PDF would not be
  positioned on the column grid and would be mis-routed or dropped.
- **Faithful-to-print transcription.** The parser copies entity names exactly as
  printed, including the form's own typos (e.g. the pilot prints "WHO II Mezz
  LLC" for what is plainly "WEHO II Mezz LLC"). Downstream consumers should not
  assume entity names are clean.
- **Row-grouping tolerance.** The 5 pt vertical tolerance suits this form's
  spacing. A filing with tighter line spacing could merge two lines into one row.
- **A column-spanning value.** The parser assumes each field stays within its
  column band. A filing where, say, a long income-type string overruns into the
  income-amount band would split that string across two fields.

## Not yet handled

- **Parts 1–5 and 7–12.** Part 6 only. Highest-priority follow-ups for tracker
  records: **Part 2** (employment assets / income, where the $120M Witkoff Group
  divestiture is reported) and **Part 5** (spouse's employment assets, where
  18 USC 208(a)(2) imputed interests surface). Part 1 (outside positions) has a
  different column set and its own date-wrapping problem.
- **Endnote resolution.** `has_endnote` is a boolean; the linked endnote text is
  not extracted or attached.
- **Reporting-period dates.** Part 6 prints none at the entry level; the
  `reporting_period` field is present for schema parity across parts and is
  always `null` for Part 6 output.
- **Canonical record schema mapping.** The parser emits raw Part 6 entries. The
  mapping to the tracker's record schema, and the 5 CFR 2640.103(a) category
  inference, are separate handoffs.
- **Value/income range normalization.** Ranges are emitted as printed strings
  (`"$1,000,001 - $5,000,000"`), not parsed into numeric bounds.

## Recommended Handoff #19

Extend the same coordinate-based approach to **Part 2** and **Part 5** — both
reuse Part 6's six-column asset layout, so the column logic should largely carry
over; the new work is the part-boundary detection and Part 2's income-type
strings (e.g. the divestiture-proceeds wording). Part 1 is a larger job (its own
column set and `From`/`To` date columns) and should be its own handoff. The
canonical record schema can be designed in parallel now that Part 6's real
structure — deep nesting, parent-level valuation, range-vs-exact amounts — is
known.
