# Handoff #18 — OGE 278 parser: Part 6 pilot

## What this resolves

Handoff #17's discovery report identified the parsing-side blocker: PDF column alignment is unstable, `pdftotext -layout` floats Part 1 dates and wraps Part 6's nested entries. The path forward is coordinate-aware extraction via pdfplumber. None of pypdf, pdfplumber, or PyPDF2 is installed in the repo. This handoff sets up the parsing toolchain and pilots it on Part 6 (Assets and Income), the section where the tracker's load-bearing financial-interest connections live.

Part 6 first because:
- It's where Witkoff's WLF interest sits (entries 41.8.1 and 41.9.1 under Witkoff Holdings LLC, nested under entry #41).
- It's where the nested-entry layout problem is sharpest. Discovery named it as the worst-case.
- It's the section that feeds the most records into the tracker. Part 2 (employment agreements) is rarer; Part 8 (liabilities) doesn't map to the tracker's category-3 anyway.

If pdfplumber handles Part 6's nesting and coordinate alignment, the other sections are comparatively easy follow-ups. If it doesn't, that's the signal to rethink before extending to anything else.

This is a parser-build handoff, not a tracker-schema handoff. Output is structured data extracted from Part 6. Mapping that data to the tracker's canonical record schema comes in a later handoff.

## What Code needs to do

### Step 1: Toolchain setup

Add pdfplumber to the collectors' Python environment. If there's no `requirements.txt` or `pyproject.toml` for collectors yet, create one. Document the environment choice (venv, poetry, uv, pip-tools) in `collectors/README.md` if it isn't already there.

Commit the dependency file as its own commit so future collectors share the same env.

### Step 2: Parser pilot on Part 6

Build a Python module at `collectors/oge_278/parser.py` (or wherever fits the existing collector layout) that takes the pilot PDF at `data/samples/witkoff-oge278-2025-08-13.pdf` and extracts Part 6 only as a structured Python dict / JSON.

For each Part 6 entry, the data model should preserve:
- Entry number (e.g., "41", "41.8.1")
- Parent entry number if nested (for "41.8.1", parent is "41")
- Entity name as printed
- EIF (Excepted Investment Fund) flag, if the form marks it
- Valuation range as printed (the standard ranges like "$1,000,001 - $5,000,000")
- Income type (Dividends, Salary, Capital gains, etc.)
- Income range
- Reporting period dates if printed at the entry level

Correctness test: the parser must correctly extract these three:
- Entry #41 Witkoff Holdings LLC, with its valuation and income
- Entry 41.8.1 World Liberty Financial (cryptocurrency) under WC Digital Fi LLC, nested correctly
- Entry 41.9.1 SC Financial Technologies LLC under WC Digital SC LLC, nested correctly

These three are the WLF-related interest chain the methodology cites. If they don't come out right, the parser doesn't work.

### Step 3: Output

Write the structured output to `data/samples/witkoff-oge278-2025-08-13-part6.json` (next to the pilot PDF). The JSON should be human-readable and represent the nested structure faithfully (parent-child relationships preserved, not flattened).

### Step 4: Document parser behavior and known limits

Create `docs/collectors/oge-278-parser.md` covering:
- pdfplumber strategy used (coordinate-based extraction, table detection, page-by-page handling, etc.)
- Heuristics that proved necessary (entry-number detection, parent-child nesting inference, valuation-range parsing)
- Known cases where the parser would break (different formatting in earlier filings, hand-written annotations, scanned-rather-than-text PDFs)
- What's not yet handled: Parts 1-5, 7-12. Part 2 (employment agreements / divestitures, where the $120M Witkoff Group divestiture lives) and Part 5 (spouse's employment assets) are the highest-priority follow-ups for tracker records.

### Step 5: Commit

Three commits, in this order:
1. `chore(collectors): set up Python environment for collectors`
2. `feat(collectors): pilot OGE 278 Part 6 parser`
3. `docs(collectors): document OGE 278 parser behavior (Handoff #18)` — the Handoff #18 doc rides with this commit.

## What this doesn't do

- Doesn't parse the other 11+ parts of the form. Part 6 first, others in subsequent handoffs.
- Doesn't map Part 6 entries to the tracker's canonical record schema. Mapping is a separate design step.
- Doesn't infer the 5 CFR 2640.103(a) category. Discovery flagged this as inferential; the inference logic is its own handoff.
- Doesn't pull additional covered-person filings. Still Witkoff-only.
- Doesn't address the two methodology-track items below.

## Flagged for Corey (methodology track, parallel to this handoff)

Two items the discovery report surfaced that aren't on Code's plate but want Corey's adjudication when convenient.

**Item 1: Category-3 direction.** The tracker's category-3 financial-interest definition reads "debt instruments held by the named family member where the entity is the obligor" — filer-as-creditor. OGE 278 Part 8 reports filer-as-debtor (the family member or appointee owes money). If category-3 is meant to capture filer-as-creditor positions, OGE 278 isn't the right primary record for that direction. Worth a versioned methodology note clarifying which way category-3 runs, and pointing to whatever primary record surfaces filer-as-creditor data (if any exists in the public-records system). PROJECT.md change + changelog entry if so.

**Item 2: Certification status as a record field.** Discovery confirmed Witkoff's filing is filer-signed but the ethics-official and OGE blocks are unsigned template text — consistent with the Warren/Murphy November 2025 letter. This is a real evidence-quality signal: an uncertified 278e is a different evidentiary artifact than a certified one. Recommend adding a `certification_status` field to the canonical record schema when it gets designed (probably Handoff #20 or thereabouts), with values like `filer_signed_only`, `ethics_certified`, `oge_certified`, or `amended_post_certification`.

## After this lands

Natural Handoff #19 candidates:
- Extend the parser to Part 2 (employment agreements and divestitures, where the $120M Witkoff Group divestiture lives) and Part 5 (spouse's employment assets, where 18 USC 208(a)(2) imputed interests would surface).
- Canonical record schema design for the tracker, now that Part 6's actual structure is known.
- 5 CFR 2640.103(a) category inference layer (the parser produces raw Part 6 entries; the tracker needs to classify each as one of the five financial-interest categories).

The parser doc's "known limits" section will shape which #19 is.
