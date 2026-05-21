# Handoff #19 — OGE 278 parser: Parts 2 and 5

## What this resolves

Part 6 parser landed in Handoff #18 with the WLF interest chain correctly extracted. Per Code's #18 report, Parts 2 and 5 reuse the same six-column layout, so the column-detection and nesting logic carries over. Both are load-bearing for tracker records.

- **Part 2** (Employment Agreements and Arrangements) contains the $120M Witkoff Group LLC divestiture that Handoff #17's discovery report tied to entry #41. The Witkoff working reference treats the divestiture's terms as load-bearing for the SC-008 worked case.
- **Part 5** (Spouse's Employment Assets and Income) is where 18 USC 208(a)(2) imputed spousal interests surface. The tracker's financial-interest definition explicitly counts these; without Part 5, the parser can't tell whether a covered person's spouse holds an interest in a sovereign-receiving entity.

Part 1 stays deferred per Code's #18 recommendation. It's a larger separate job and doesn't reuse Part 6's column logic.

After this lands, the parser will have read every Part of OGE 278e that maps to the tracker's financial-interest definition. Schema design becomes the natural next handoff.

## What Code needs to do

### Step 1: Extend parser to Parts 2 and 5

Add Part 2 and Part 5 extraction to `collectors/oge_278/parser.py`, reusing column-detection and nesting logic from Part 6. Document any layout divergence from Part 6 (different column count, different header structure, different value-format conventions) inline as you find it.

Conventions established in #18 carry forward unambiguously:

- **Immediate-parent nesting.** Parent of "41.8.1" is "41.8", not "41". The full ancestor chain is recoverable by walking the structure.
- **Faithful-to-print transcription.** Form typos preserved as-is. No silent cleaning.
- **Endnote flags** carry through where the form marks them.

### Step 2: Correctness tests

**Part 2 correctness test:** The Witkoff Group LLC entry containing the $120M divestiture must come through with the divestiture amount, recipient (if printed), and any conditional terms ("to be completed within 90 days of confirmation," "upon Senate confirmation," etc.). If the entry has multiple sub-parts (separate divestiture arrangements, retention bonuses, deferred compensation), all sub-parts must come through with their nesting.

**Part 5 correctness test:** Any spousal entries in Witkoff's filing must come through with the same structural fidelity as Part 6 — entity name, valuation range, income type and range, nesting preserved if multi-level.

If Witkoff's Part 5 is empty (which would itself be a finding), the parser output must distinguish "section parsed, no entries reported" from "section not parsed." Use an explicit empty marker (e.g., `"entries": []` plus a `"parsed": true` flag), not a missing key.

### Step 3: Output

Two new files alongside the Part 6 output:
- `data/samples/witkoff-oge278-2025-08-13-part2.json`
- `data/samples/witkoff-oge278-2025-08-13-part5.json`

Same JSON conventions as Part 6. Human-readable, nested structure preserved, immediate-parent nesting consistent.

### Step 4: Update parser doc

Update `docs/collectors/oge-278-parser.md` to cover:

- Part 2 and Part 5 column layouts, with divergence from Part 6 called out where it exists.
- Any new heuristics needed (divestiture-amount parsing, conditional-term capture, spousal-flag detection).
- What's still not parsed (Parts 1, 3, 4, 7-12) and which of those will eventually matter for the tracker. As of now, Parts 3, 4, and 7-12 don't map to the tracker's financial-interest definition; Part 1 stays deferred.

### Step 5: Commit

Two commits:
1. `feat(collectors): extend OGE 278 parser to Parts 2 and 5`
2. `docs(collectors): update parser doc; track Handoff #19`

The Handoff #19 doc rides with commit 2.

## What this doesn't do

- Doesn't parse Part 1. Deferred per Code's #18 recommendation.
- Doesn't parse Parts 3, 4, 7-12. These don't currently map to the tracker's financial-interest definition. Revisit if methodology adds new evidence categories.
- Doesn't design the canonical record schema. That's #20.
- Doesn't map parsed entries into tracker records. Mapping waits for schema.

## After this lands

**Handoff #20 candidate: canonical record schema design.** Substantive design step. Wants Corey-level decisions, not Code-only execution. Open inputs to the design conversation:

- What's the canonical shape of an SC-### record once it's sourced from an OGE 278e filing?
- How does the 5 CFR 2640.103(a) category get assigned? Discovery flagged this as inferential; the inference logic needs to be specified.
- How does `certification_status` get represented? (Flagged by Handoff #17 discovery, parked for Corey.)
- How does immediate-parent nesting from the parser flatten into queryable records, and where does the original nested structure get preserved for traceability?
- How are spousal interests represented in the record schema, and how does the record's covered-person field distinguish filer-as-principal from spouse-as-imputed?
- Dirty entity names (form typos preserved per the faithful-to-print convention) — does normalization happen in the schema layer, at query time, or never?

The two methodology-track items from #17 / #18 (category-3 direction, certification_status field) get adjudicated as inputs to #20's design conversation, not as blockers to it. #20 is partly methodology, partly schema; it likely gets drafted in conversation with Corey before any Code-executable handoff fires.
