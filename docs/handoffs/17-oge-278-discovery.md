# Handoff #17 — Phase 5 opener: OGE 278 collector discovery

## What this resolves

First piece of Phase 5 (Python collectors). OGE Form 278e is the load-bearing primary record for the tracker's financial-interest definition (per 5 CFR 2640.103(a) / 18 USC 208(a)) and the methodology already cites Steve Witkoff's August 13, 2025 New Entrant Report directly. The collector that pulls these disclosures produces the records that connect covered persons to connected businesses. That makes OGE 278 the natural opener for collector work.

This handoff is discovery, not implementation. Goal: figure out how OGE publishes 278e disclosures, retrieve one as a pilot, document what the form actually contains as it bears on the tracker, surface blockers before any parser gets written.

## What Code needs to do

### Step 1: Locate the publication surface

OGE Form 278e disclosures are public records. Find where they're published. Candidates worth checking:

- OGE.gov search (`https://search.oge.gov/` or similar)
- The White House counsel's office (for senior White House staff, special envoys, etc.)
- Specific agency disclosure offices (Cabinet secretaries typically appear via their agency's ethics office, not OGE.gov directly)

Note which surface holds what. Different covered persons file with different offices.

### Step 2: Pilot retrieval

Retrieve Steve Witkoff's August 13, 2025 New Entrant Report. Save the file at `data/samples/witkoff-oge278-2025-08-13.<ext>` using whatever format the publication surface serves (PDF most likely; structured data if available).

If the search interface returns multiple Witkoff filings (New Entrant Report, supplemental annual report, amendments), grab all of them and label by type and date. Otherwise just the New Entrant Report.

### Step 3: Inspect the form's schema

Read through the actual document and document the structure. The bits that matter for the tracker:

- Section structure: OGE Form 278e has standard sections covering positions outside government, employment assets and income, employment agreements and arrangements, sources of compensation, spouse's employment assets and income, non-investment income (filer and spouse), assets and income, transactions, liabilities, gifts and travel reimbursements, and compensation in excess of $5,000 paid by one source. Confirm which sections are populated in Witkoff's filing.
- For each entity Witkoff reports an interest in: what fields are filled? Entity name, valuation range, type of interest, income amount range?
- How are spousal interests reported? The tracker counts these per 18 USC 208(a)(2), so the schema needs a representation for them.
- How are Witkoff Group affiliates represented? The methodology draft says Witkoff has "continuing equity exposures across multiple Witkoff Group affiliates." Document the actual entity names that show up in the filing, the interest types, and the valuation ranges.

### Step 4: Produce the discovery report

Create `docs/collectors/oge-278-discovery.md` covering:

- Where OGE 278e disclosures live (publication surface, URL pattern, access method, any authentication required)
- File format(s) served (PDF, JSON, both)
- Form schema as it bears on the tracker (the categories from Step 3, plus anything unexpected)
- Witkoff filing summary (entity names listed, types of interest, valuation ranges, spousal entries if any)
- Blockers and unknowns for the production collector

Specific questions the report should answer:

- Is the search interface filterable by name, role, agency, date?
- Are filings served as PDF only, or is there structured data behind the PDFs?
- Is there a public download API, or does collection mean HTML/PDF scraping?
- Are amendments and supplemental annual reports tracked separately from New Entrant Reports?
- How far back does coverage go? Relevant for the comparative-set entries (Affinity Partners, Trump Organization 2017-2020 foreign-government bookings).
- Are there rate limits, terms of use, or robots.txt constraints that would shape a scheduled collector?

### Step 5: Commit

Two commits, in this order:

1. `data(samples): add Witkoff OGE 278e New Entrant Report (2025-08-13)` for the pilot file (and any related Witkoff filings retrieved).
2. `docs(collectors): add OGE 278 discovery report (Handoff #17)` for the discovery doc and this handoff doc together.

## What this doesn't do

- Doesn't write the collector. `collectors/oge_278_collector.py` stays as a `NotImplementedError` stub. Implementation comes in a later handoff once the discovery report names the path.
- Doesn't pull multiple covered persons. Witkoff is the pilot. Broader coverage (the v2.0 covered-persons list in PROJECT.md) waits for the production collector.
- Doesn't design the canonical record schema. The schema is informed by what the form actually contains; designing it before discovery is backwards.
- Doesn't wire up Turso storage. The pilot file is a sample document, not a record in the database.

## After this lands

Natural Handoff #18 candidates, depending on what discovery surfaces:

- Parser design, if PDFs are the only format and parsing is non-trivial.
- Search interface mapping, if OGE.gov's interface needs care for a scheduled collector.
- Covered persons inventory: the full list of names whose filings the collector should pull, derived from PROJECT.md's covered-persons definition.
- Canonical record schema design, if the form's schema is clean enough to model directly.

The discovery report's "blockers and unknowns" section will tell us which.
