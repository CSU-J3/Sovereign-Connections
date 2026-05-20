# OGE Form 278 Collector — Discovery Report (Handoff #17)

Phase 5 opener. Discovery only — no collector code written. Goal: document how OGE
Form 278e disclosures are published, retrieve a pilot, map the form schema as it
bears on the tracker, and surface blockers before a parser is designed.

Pilot file: `data/samples/witkoff-oge278-2025-08-13.pdf` — Steven C. Witkoff, New
Entrant Report, electronically signed 08/13/2025. 10-page text-based PDF, 60,492
bytes, retrieved from the White House counsel surface (see below).

## 1. Where OGE 278e disclosures live

There is no single publication surface. Three distinct ones, holding different
covered persons:

**A. White House Counsel surface — `whitehouse.gov`.** Senior White House / Executive
Office of the President officials (Assistants to the President, deputy chiefs of
staff, special envoys, press staff). This is where Witkoff's filing lives.

- PDF URL pattern: `https://www.whitehouse.gov/wp-content/uploads/<YYYY>/<MM>/<Lastname>-<Firstname>.pdf`
  — e.g. `2025/09/Witkoff-Steven.pdf`, `2025/06/Wiles-Susie.pdf`, `2025/06/Miller-Stephen.pdf`.
- The `<YYYY>/<MM>` segment is the **upload date**, not the filing date, and varies
  per filer: most January-20 appointees sit under `2025/06`; Witkoff (June 30
  appointment) under `2025/09`. There is no deterministic way to construct a
  filer's URL from their name alone.
- Index page: `https://www.whitehouse.gov/disclosures/financial-disclosures/`.
  This page is indexed by search engines but returns **HTTP 404 to non-browser
  clients** (curl with a browser UA still gets the SPA 404 shell). It is
  client-side rendered or bot-served. The individual PDFs, by contrast, are
  served reliably with `Content-Type: application/pdf` and a `200`.
- First-term (2017–2021) White House filings are preserved at
  `https://trumpwhitehouse.archives.gov/disclosures/` — relevant for the
  comparative-set entries.

**B. OGE search collection — `oge.gov`.** "Officials' Individual Disclosures Search
Collection" at `oge.gov/web/oge.nsf/Officials%20Individual%20Disclosures%20Search%20Collection?OpenForm`.
A Lotus Domino (`.nsf`) application. Result table columns: Date, Type, Name,
Title, Agency, Level. Holds nominee disclosures, ethics agreements, and
certifications. Documents not online can be requested via OGE Form 201.

**C. Agency ethics offices.** Cabinet secretaries and agency-level appointees
generally file with, and are released by, their own agency's ethics office
(DOJ, Energy, Interior, etc.), not `oge.gov` directly.

**Retention limit:** OGE is required by law to destroy most public 278e reports
and associated documents **6–7 years after creation** unless they are in an
ongoing investigation. Coverage on `oge.gov` does not extend indefinitely; the
archived White House surface is the more durable record for older filings.

## 2. File format

PDF only. No JSON, no structured data behind the PDFs, no public download API.
The White House PDFs are **text-based** (not scanned images) — `pdftotext -layout`
extracts clean text, which is how the schema below was read. OGE Form 201 is the
fallback request path for documents not posted online.

## 3. Form schema as it bears on the tracker

OGE Form 278e (revision "Updated 08/2024", OMB 3209-0001, 5 C.F.R. part 2634).

**Header block:** Report Type (`New Entrant Report` here; other values: Annual,
Termination, etc.), Year (Annual only), Date of Appointment, Date of Termination,
Appointment Type (`Non-Career` here).

**Filer information + certification blocks:** filer name, position, agency,
electronic signature line (signed via `Integrity.gov`, with any filing-extension
note), an **Agency Ethics Official's Opinion** block, and an **OGE Certification**
block. In Witkoff's filing the two review blocks appear as **unsigned template
text** — no reviewing official's name or date — consistent with the
certification-pending status documented in the Warren/Murphy letter of November
2025. The production collector should capture certification status as a distinct
field: a filed-but-uncertified 278e still establishes filer-disclosed interests.

**Nine numbered parts.** Which are populated depends on report type — for a New
Entrant Report, Parts 7 (Transactions) and 9 (Gifts) are marked
`(N/A) - Not required for this type of report`.

| Part | Title | Columns | Tracker relevance |
|---|---|---|---|
| 1 | Filer's Positions Held Outside US Government | #, Organization Name, City/State, Position (Type + Held), From, To | Establishes the *connected business* link and the *position* (officer/managing member) |
| 2 | Filer's Employment Assets & Income and Retirement Accounts | #, Description, EIF, Value, Income Type, Income Amount | Ownership stakes, employment-derived income |
| 3 | Filer's Employment Agreements and Arrangements | #, Employer/Party, City/State, Status and Terms, Date | Continuing arrangements (severance, retained equity, benefits) |
| 4 | Filer's Sources of Compensation Exceeding $5,000 | #, Source Name, City/State, Brief Description of Duties | Employment/consulting relationships |
| 5 | Spouse's Employment Assets & Income | same as Part 2 | **Spousal interests imputed under 18 USC 208(a)(2)** |
| 6 | Other Assets and Income | #, Description, EIF, Value, Income Type, Income Amount | Bulk of the holdings; filer + spouse + dependent children aggregated |
| 7 | Transactions | #, ... | N/A on a New Entrant Report; populated on Annual |
| 8 | Liabilities | #, Creditor Name, Type, Amount, Year Incurred, Rate, Term | See mapping caveat below |
| 9 | Gifts and Travel Reimbursements | #, ... | N/A on a New Entrant Report |

Followed by an **Endnotes** table (keyed by part + entry number), a **Summary of
Contents** (instructions for each part), and the Privacy Act statement.

**Valuation is reported as bracketed ranges, not exact figures.** Standard value
brackets observed: `None (or less than $1,001)`, `$1,001 - $15,000`,
`$15,001 - $50,000`, `$50,001 - $100,000`, `$100,001 - $250,000`,
`$250,001 - $500,000`, `$500,001 - $1,000,000`, `$1,000,001 - $5,000,000`,
`$5,000,001 - $25,000,000`, `$25,000,001 - $50,000,000`, `Over $50,000,000`.
Income brackets are parallel. The `Income Amount` column sometimes carries an
**exact dollar figure** instead of a bracket (e.g. `$120,000,000`, `$34,363,535`,
`$1,218,905`) — the collector schema must accept both a range and an exact value.

**EIF column:** Excepted Investment Fund flag (`Yes` / `No` / `N/A`). For an EIF,
income type is not required — affects how completely a holding is described.

**Hierarchical entry numbering:** Parts 2, 5, and 6 use nested numbering
(`41`, `41.8`, `41.8.1`, `41.1.1.1` …) to express holding-company → subsidiary →
underlying-asset chains. Value and income are typically reported **at the top
parent level only**; child entries carry the entity name but blank value/income.

**Type-of-interest representation — a gap for the tracker.** Part 1 has explicit
`Type` (Limited Liability Company, Corporation, Non-Profit, Limited Company) and
`Held` (Managing Member, Member, President, CEO & Sole Stockholder, Consultant,
Trustee, Director, Sole Shareholder) fields. Parts 2/5/6 have **no explicit
"type of financial interest" field** that maps cleanly to the tracker's five
5 CFR 2640.103(a) / 18 USC 208(a) categories — interest type must be *inferred*
from the description, the part it appears in, and the nesting. The collector will
need an inference layer; this is not a direct field read.

**Liabilities caveat:** Part 8 reports liabilities the filer *owes* (filer as
debtor). The tracker's financial-interest category 3 is "debt instruments **held
by** the named family member where the entity is the obligor" (family member as
*creditor*). Part 8 therefore does **not** map to tracker category 3. It is
relevant context but not a financial-interest trigger.

**Spousal interests:** Part 5 plus spouse-labeled entries inside Part 6 (e.g.
"Spouse Brokerage Account #1"). The form labels spouse accounts explicitly, so
spousal interests under 18 USC 208(a)(2) are machine-distinguishable.

## 4. Witkoff filing summary

- **Part 1 — 77 outside positions.** Overwhelmingly Managing Member of Witkoff
  Group affiliate LLCs (the `WG …`, `SCW …`, `Witkoff …`, `150 …`, `866 …`
  numbered entities). Non-real-estate / non-domestic entries of note:
  #70 **Bally's Corporation** (Corporation, Consultant); #76 **M&A Boat Ltd.** and
  #77 **M&A Management Company Ltd.** (both George Town, Grand Cayman — Director
  and Sole Shareholder respectively).
- **Part 2 — The Witkoff Group LLC**, value `Over $50,000,000`, income type
  "Proceeds from the sale of an interest in the company as part of divestiture
  planning", income amount **`$120,000,000`**. This is the $120M divestiture the
  Witkoff working reference flags as not-otherwise-identified — the form ties it
  specifically to The Witkoff Group LLC.
- **Part 4 — Bally's Corporation**, "Consultancy services in 2023."
- **Part 5 — spouse IRA / brokerage** holding public REITs and equities (Macerich,
  Regency Centers, Ventas, W.P. Carey, etc.) in small ranges.
- **Part 6 — World Liberty Financial.** Entry **41.8.1 "World Liberty Financial
  (cryptocurrency)"** is nested under **41.8 WC Digital Fi LLC**, and **41.9.1
  "SC Financial Technologies LLC (stablecoin)"** under **41.9 WC Digital SC LLC** —
  both children of **#41 Witkoff Holdings LLC** (value `Over $50,000,000`,
  distributions `$34,363,535`). Critically, the WLF and SC Financial Technologies
  entries themselves carry **no separate value or income** — the dollar figures
  sit at the Witkoff Holdings parent level. The OGE form thus documents the
  *existence* of Witkoff's WLF interest but not its standalone valuation.
- **Part 8 — three liabilities:** two JP Morgan Chase loans (margin account /
  aircraft) and one M&T Bank loan, in the `$1M–$5M` and `$25M–$50M` ranges.
- The filing is **filer-signed but not ethics-certified** (see §3).

## 5. Blockers and unknowns for the production collector

1. **PDF-only, parsing required.** No structured data anywhere. A parser is the
   core of the production collector.
2. **PDF column alignment is unstable.** `pdftotext -layout` output shows Part 1
   `From`/`To` dates floating away from their rows, and Part 6's deeply nested
   entries wrapping `EIF`/`Value`/`Income` across lines unpredictably. A naive
   line-based parse will misalign fields. Coordinate-aware extraction
   (`pdfplumber` bounding boxes) or per-section heuristics will be needed.
   **None of `pypdf`, `pdfplumber`, or `PyPDF2` is currently installed** —
   a dependency decision for the parser handoff.
3. **No machine-readable index.** The White House `/disclosures/financial-disclosures/`
   index 404s to non-browser clients. PDFs are directly fetchable but the
   `YYYY/MM` upload-date folder cannot be derived from a filer's name. Options:
   (a) headless browser to render the index, (b) crawl `sitemap_index.xml`,
   (c) drive discovery from the OGE search collection instead.
4. **Multiple surfaces, different covered persons.** White House surface = EOP
   officials; OGE search collection = nominees + some agency; Cabinet officials
   = agency ethics offices. The collector needs a per-covered-person routing
   table keyed off the PROJECT.md covered-persons list.
5. **OGE search collection is a Lotus Domino app.** Its query/filter mechanics
   (Date/Type/Name/Title/Agency/Level columns) need separate mapping before it
   can be driven programmatically — a strong Handoff #18 candidate.
6. **Coverage horizon.** OGE destroys most 278e reports 6–7 years after creation.
   Comparative-set targets (Affinity Partners ~2022, Trump Org 2017–2020) may be
   at or past the OGE retention edge; `trumpwhitehouse.archives.gov/disclosures/`
   preserves the 2017–2021 term and should be the source for those.
7. **Report-type and supersession logic.** New Entrant, Annual, and Termination
   reports populate different parts; OGE Form 278-T (STOCK Act periodic
   transaction reports) is a separate document. The collector must record report
   type and handle a later filing superseding an earlier one.
8. **No clean interest-type field.** As noted in §3, mapping form entries to the
   tracker's five 5 CFR 2640.103(a) categories is inferential, and Part 8
   liabilities do not map to tracker category 3.
9. **robots / terms of use.** `whitehouse.gov/robots.txt` is fully permissive
   (`User-agent: *`, empty `Disallow:`, no crawl-delay). The PDFs are public
   records, no authentication. `oge.gov`'s robots.txt was not cleanly retrieved
   during discovery and should be checked directly before any scheduled
   collector hits that host. Rate-limit politely regardless.

## 6. Specific questions from the handoff

- **Filterable by name/role/agency/date?** OGE search collection exposes
  Date/Type/Name/Title/Agency/Level columns — filterable in principle, mechanics
  TBD. The White House surface has no machine-accessible index, so it is *not*
  filterable for a scraper; retrieval there means knowing the PDF URL.
- **PDF only or structured data?** PDF only. Text-based (extractable), no JSON.
- **Public download API?** No. HTML/PDF retrieval only; OGE Form 201 request
  process for offline documents.
- **Amendments / supplemental reports tracked separately?** Yes — the Report Type
  header field distinguishes New Entrant / Annual / Termination; 278-T is a
  separate form. Supersession logic is the collector's responsibility.
- **How far back does coverage go?** OGE: 6–7 years (statutory destruction).
  `trumpwhitehouse.archives.gov/disclosures/` preserves 2017–2021 filings.
- **Rate limits / ToU / robots?** `whitehouse.gov` permissive; `oge.gov` TBD.

## 7. Recommended next handoff

Two viable Handoff #18 directions, and they are complementary:

- **Parser design** — pick the PDF library (`pdfplumber` favored, for bounding-box
  access), and design the per-part extraction with the column-alignment problem
  in §5.2 as the central challenge. Witkoff's filing is a hard pilot: 77
  positions, 62 deeply nested Part 6 entries.
- **Search-surface mapping** — map the OGE Domino search collection so the
  collector can discover filings by covered person rather than depending on
  hand-collected PDF URLs.

Parser design is the higher-priority of the two: until the form can be turned
into records, surface mapping only produces more PDFs to sit on. The canonical
record schema should be designed *after* the parser proves what fields come out
cleanly — the §3 caveats (no interest-type field, parent-level valuation,
range-vs-exact amounts) are the schema's hard constraints.
