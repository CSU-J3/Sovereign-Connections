# Form ADV / IAPD Collector — Discovery Report (Handoff #33)

Discovery only — no collector code, no schema changes. Goal: document how SEC Form
ADV / IAPD data is published, retrieve Affinity as the pilot, map where the
sovereign-source signal lives in the form, and resolve the ingestion-path question
(structured bulk CSV vs per-firm PDF) before a parser/ingest is designed.

Pilot entity: **A Fin Management LLC** (brand name *Affinity Partners*), the firm
behind SC-009. Delaware LLC, offices in Sunny Isles Beach FL, sole owner Jared
Kushner. It is a **registered investment adviser** (RIA) — it files a full Part 1A
plus a Part 2A brochure — not an exempt reporting adviser (ERAs do not file Part 2).

Pilot files retrieved to `data/samples/`:

- `affinity-adv-2026-03-22.pdf` — full Form ADV Part 1A + all Schedules, 50-page
  text-based PDF, 2,386,439 bytes, pulled from the SEC reports surface (§1.B).
- `affinity-adv-part2a-2026-03-22.pdf` — Part 2A firm brochure, 8 pages, 479,228
  bytes, dated March 22 2026.
- `affinity-adv-iapd-bulk-IA_ADV_Base-extract.csv` — Affinity's six Part 1A Item-5
  rows (2021–2024) extracted from the SEC bulk Form ADV data set (§1.C). This is the
  structured-vs-PDF comparison input for §4.

## 1. Where Form ADV / IAPD data lives

Unlike OGE 278 (PDF-only, three scattered surfaces), Form ADV has a single
regulator (SEC, filed through FINRA's IARD) and is published as **both structured
bulk data and per-firm PDF**. Five surfaces, confirmed reachable during discovery:

**A. IAPD front door — `https://adviserinfo.sec.gov`.** Firm/individual search,
returns the most recent filing. **It is an Angular single-page app**: a non-browser
client (`curl`, WebFetch) receives only the shell HTML; all firm data loads via XHR
against a JSON API. `adviserinfo.sec.gov/firm/summary/315482` therefore cannot be
scraped from its HTML — the firm page is a dead end for a scraper. Use the bulk
data (§1.C) or the per-firm PDF (§1.B) instead.

**B. Per-firm full ADV PDF — `reports.adviserinfo.sec.gov`.** Pattern
`https://reports.adviserinfo.sec.gov/reports/ADV/{CRD}/PDF/{CRD}.pdf` (verified:
`/reports/ADV/315482/PDF/315482.pdf` → 200, `application/octet-stream`, 50-page PDF).
Served from S3/CloudFront, **no robots.txt, no auth**, keyed purely on CRD. This is
the cleanest per-firm surface — it renders Part 1A plus every Schedule (A/B owners,
D 7.B private funds) into one document. It does **not** include the Part 2A brochure.

**C. Bulk Form ADV data sets (structured CSV) — `www.sec.gov/files/…`.** The
load-bearing surface. Historical Part 1A with all Schedules is published as
multi-table CSV inside large zips, linked on filing identifiers:
- `adv-filing-data-20001019-20111104.zip` (238 MB)
- `adv-filing-data-20111105-20241231-part1.zip` (669 MB) — IA + ERA base, Schedules
  A/B, 1B/1F/1I, and all ERA Schedule-D tables.
- `adv-filing-data-20111105-20241231-part2.zip` (409 MB) — the IA (registered) Schedule
  D 7.B private-fund tables and remaining IA schedules.

Tables are prefixed `IA_` (registered advisers) and `ERA_` (exempt reporting
advisers); `part1`/`part2` are size-splits, not a clean IA/ERA split. **Coverage
ends 2024-12-31** on this FOIA page; filings from 2025 to present are only on IAPD
(current/compilation). `www.sec.gov` rejects clients that do not send an SEC-policy
User-Agent (declared name + contact email) with a "Request Rate Threshold Exceeded"
/ 403 page — a compliant UA was required for every fetch here.

**D. Compilation download (all advisers, XML) — `adviserinfo.sec.gov/compilation`.**
Returns the IAPD SPA homepage to non-JS clients; the XML compilation is a
JS-triggered download. Needs a headless browser or the documented direct file URL
(not resolved in discovery — see blockers).

**E. Part 2A brochures (narrative PDF).** Per-firm at
`files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID={id}`
(Affinity's current brochure is version id **1023093**, brochure id 354475). Two
catches: a bare GET 404s — the request needs browser-like headers (User-Agent +
`Referer`) to return the PDF; **and `adviserinfo.sec.gov/robots.txt` disallows this
path** (`Disallow: /IAPD/Content/Common/crd_iapd_Brochure.aspx` and `/firm/brochure/`).
A scheduled collector should not hit the per-firm brochure path. Brochures are also
published in bulk as `adv-brochures-YYYY-month.zip` on the FOIA page (§1.C host) —
that is the compliant route to brochure text.

## 2. File formats and access summary

| Content | Surface | Format | Access notes |
|---|---|---|---|
| Part 1A + Schedules (one firm) | reports.adviserinfo.sec.gov | PDF (text-based) | open, keyed on CRD, no robots |
| Part 1A + Schedules (all firms) | www.sec.gov/files bulk zips | multi-table CSV | SEC-compliant UA required; ends 2024-12-31 |
| Part 1A current (2025→) | IAPD compilation / JSON API | XML / JSON | JS-gated; method unresolved |
| Part 2A brochure (one firm) | files.adviserinfo.sec.gov | PDF | **robots-disallowed**; needs browser headers |
| Part 2A brochures (all firms) | www.sec.gov/files brochure zips | PDF in zip | compliant bulk route |

Unlike OGE 278, the structured fields do **not** require PDF parsing — they are
published as CSV columns. The PDF is needed only for human verification and for the
current period that the lagging FOIA CSV does not yet cover.

## 3. Affinity resolved identifiers and the sovereign-relevant field map

**Resolved identifiers (not guessed — read from the filing):**
- Firm CRD **315482**; SEC file number **801-122021** (Part 1A Item 1.D).
- Sole owner / control person: **Kushner, Jared Corey** (CRD 4220900), "Founder and
  Chief Executive Officer", title acquired 06/2021, Schedule A ownership code **E
  (75% or more)**, control person **Yes**. CFO: Lauren Elise Key (ownership NA).
- Part 2A brochure version id 1023093 (dated 2026-03-22).
- Six private funds, each with an `805-` private-fund ID and its own affiliated GP
  (e.g. fund *Affinity Partners Fund I Co-Invest Delta II LP* → ID 805-2944771777,
  GP *Affinity Partners Fund I Co-Invest GP LP*). The brochure (Item 4) states an
  affiliated entity serves as GP/managing member to each fund and is covered under
  Affinity's single registration "in accordance with SEC guidance" — i.e. the GP
  affiliates are not separately registered (special-purpose-vehicle treatment); no
  umbrella relying-adviser Schedule R was needed.

The places the sovereign signal could appear, and what Affinity's filing actually
shows in each:

**Item 5.D — client-type / AUM matrix (Part 1A).** The form has an explicit line
**(l) "Sovereign wealth funds and foreign official institutions"** alongside (f)
"Pooled investment vehicles", with columns for number of clients, "fewer than 5
clients", and RAUM. In Affinity's filing the **(l) sovereign line is blank** and all
regulatory AUM is reported under **(f) Pooled investment vehicles**. This is
structural, not an omission: Part 1A instructions exclude private-fund *investors*
from being counted as 5.D clients, so a fund adviser's sovereign LPs will never
surface on the (l) line. **5.D is therefore a weak sovereign detector for fund
advisers.**

**Schedule A / B — direct and indirect owners.** Confirms Kushner as 75%+ control
owner (above). Identifies *the adviser's* owners, not its fund investors — no
sovereign signal here for this structure.

**Schedule D Section 7.B — private-fund reporting.** This is where the structured
sovereign *proxy* lives. Each of the six funds reports gross asset value, number of
beneficial owners, % owned by the adviser/related persons, and **% beneficially
owned by non-United States persons (Question 16)**:

| Private fund | Gross asset value | Benef. owners | % related | % non-US |
|---|---:|---:|---:|---:|
| Affinity Partners Parallel Fund I LP | $4,307,145,842 | 6 | 0% | **100%** |
| Affinity Partners Fund I Co-Invest Delta LP | $1,193,319,132 | 1 | 0% | **100%** |
| Affinity Partners Fund I Co-Invest Sigma LP | $596,596,930 | 1 | 0% | **100%** |
| Affinity Partners Fund I LP | $45,179,176 | 1 | 100% | 0% |
| Affinity Partners Fund I Co-Invest Delta II LP | $12,033,077 | 1 | 100% | 0% |
| Affinity Partners Fund I Co-Invest Sigma II LP | $6,023,254 | 1 | 100% | 0% |

Total GAV = **$6,160,297,411**, equal to the reported regulatory AUM. The three
largest funds — **$6,097,061,904, ≈99% of AUM — are 100% beneficially owned by
non-US persons**, and Parallel Fund I concentrates $4.31B across just **6 beneficial
owners**. This concentration-plus-foreign-ownership pattern is the strongest
sovereign-source proxy the ADV carries — but Question 16 reports only an aggregate
percentage; it **does not name the non-US owners**.

**Part 2A brochure narrative (Item 7, Types of Clients).** Lists that underlying
investors "include (or are expected to include) high net-worth individuals,
financial institutions, corporations, **sovereign wealth funds**, endowments,
charitable organizations, public and private pension funds…", minimum investment
$25–50M. This is boilerplate forward-looking client-category language — it confirms
sovereign-wealth-fund capital is *contemplated as a category*, but does not attest
which current investors are sovereign funds and **does not name PIF, QIA, or Lunate**.
(SC-009's citation of "Item 7" refers to this Part 2A brochure item, not a structured
Part 1A Item 7.) Item 5 confirms the 0.5%-quarterly / 2.0%-annualized management fee
and Item 6 the up-to-20% carried interest.

**Finding stated plainly, as the handoff required:** within the four-corners of
Affinity's ADV, sovereign capital is visible only as (a) a blank-for-this-structure
client-type line, (b) an aggregate 100%-non-US-ownership flag plus extreme
beneficial-owner concentration on the large funds, and (c) a generic "sovereign
wealth funds" category in the brochure. The **identity** of the sovereign sources
(PIF ~$2B 2021; QIA + Lunate ~$1.5B 2024) appears **nowhere in the ADV** — it lives
only in secondary reporting, on the separate evidentiary footing SC-009 already
records.

## 4. Ingestion path — the load-bearing question

**Resolved against real data, not assumed.** The Affinity bulk-CSV extract
(`affinity-adv-iapd-bulk-IA_ADV_Base-extract.csv`, six filings 2021–2024 from
`IA_ADV_Base_A`) was compared field-by-field against the Affinity PDF:

- The Item 5.D matrix is **structured columns** in the bulk Base table: `5D1a–n`
  (client counts), `5D2a–n` (fewer-than-5 flags), `5D3a–n` (AUM by client type),
  with `5D*l` = the sovereign line and `5D*f` = pooled vehicles. Affinity's rows
  show `5D3l` **blank in every filing**, RAUM carried in `5D3f` (e.g. 2024-03-28:
  `5D3f` = `5F2c` = $3,004,963,927), `5D2l` = `N`. The CSV reproduces the PDF
  exactly — and in fact **resolves a column-alignment ambiguity** that `pdftotext
  -layout` introduces on the 5.D grid (the PDF floats the AUM figure onto the wrong
  client-type row; the CSV is unambiguous). Argument for structured ingest.
- Schedule A/B owners → `IA_Schedule_A_B` (structured). Schedule D 7.B private-fund
  fields (GAV, beneficial owners, **% non-US**) → the `IA_Schedule_D_7B*` table family
  in the bulk set's part2 (same naming as the visible `ERA_Schedule_D_7B1A23/25/26…`
  tables). Structured.

**Recommendation: structured CSV / compilation ingest, not PDF parsing.** Every
sovereign-relevant Part 1A field is a bulk-CSV column joinable on filing id / CRD —
the collector is largely a join, unlike the OGE 278 build which is fundamentally a
PDF parse. The per-firm PDF is a **fallback / verification** surface, needed mainly
because the FOIA CSV lags ~15 months (current-period structured data must come from
IAPD). The Part 2A brochure (PDF) adds only weak narrative signal and is
robots-constrained per firm.

**But the cleaner answer has a hard limit:** the structured fields carry *proxies*
(7.B % non-US + beneficial-owner concentration; the existence of the 5.D(l) column),
never the sovereign *identity*. An ADV collector can surface and rank candidates;
it cannot, from the ADV alone, assert that a given fund's capital is PIF/QIA/Lunate.
Promotion to a record still requires secondary-source corroboration.

## 5. Blockers and unknowns for the production collector

1. **Bulk CSV lag.** FOIA bulk data ends 2024-12-31; Affinity's current $6.16B
   filing (2026-03-22) is absent — the CSV's latest Affinity RAUM is $3.0B
   (2024-03-28). Current-period structured data is only on IAPD
   (compilation/JSON API), whose machine-access method is unresolved (D below).
2. **IAPD is a SPA.** Firm pages serve no data in HTML; the `compilation` XML is
   JS-gated. The collector needs either the IAPD JSON API (reverse-engineered from
   XHR) or a headless-browser path for 2025→ filings.
3. **Brochure path robots-disallowed.** Per-firm Part 2A
   (`crd_iapd_Brochure.aspx`) is in `Disallow`; use the bulk `adv-brochures-*.zip`
   sets. Brochure text is not in the Part 1A CSV.
4. **SEC.gov access policy.** `www.sec.gov` requires a declared User-Agent (name +
   email) and polite rate limiting, or it serves a threshold/403 page.
5. **Sovereign identity not in the source.** The ADV never names the sovereign
   investor. Candidate emission must flag-for-research, not assert; records need the
   congressional/press corroboration already on separate footing in SC-009.
6. **Versioning / supersession.** Each annual update is a new filing row; the bulk
   Base table holds multiple rows per CRD (six for Affinity). The collector must
   pick the latest filing per CRD and track amendments.
7. **ERA vs RIA coverage.** Exempt reporting advisers file only a subset of Part 1A
   (no full Item 5.D client matrix, no Part 2A) — covered advisers that are ERAs
   will yield thinner structured signal than a full RIA like Affinity.
8. **Umbrella / affiliate entities.** Affinity's GP affiliates are covered under one
   registration (no relying-adviser Schedule R), but advisers that *do* file umbrella
   registrations will spread funds across filing/relying advisers (`IA_SCH_R_*`
   tables) — the entity graph must be preserved, not collapsed.

## 6. Specific questions from the handoff

- **Authoritative surface per content?** Structured Part 1A → bulk CSV (current via
  IAPD compilation); per-firm verification → reports.adviserinfo PDF; narrative →
  Part 2A brochure (bulk zip).
- **Structured or PDF-only?** Structured CSV *and* PDF. The sovereign-relevant Part
  1A fields are all CSV columns — structured ingest, not a parse.
- **Does the form carry a sovereign-wealth-fund category?** Yes — Item 5.D line (l).
  For a private-fund adviser it is blank by construction (LPs aren't 5.D clients);
  the usable structured proxy is Schedule D 7.B Question 16 (% non-US) + owner
  concentration.
- **Does Affinity name PIF/QIA/Lunate?** No. The ADV confirms sovereign capital only
  by category and by aggregate non-US ownership; identities are secondary-source.
- **Auth / rate limits / robots?** reports.adviserinfo: open. adviserinfo: brochure
  + viewform paths disallowed. sec.gov: compliant-UA + rate-limit policy.

## 7. Recommended next handoff (#34)

Discovery names the ingestion path as **structured ingest**, so the natural #34 is
ADV structured-ingest design, in this order (the blockers above set it):

- **IAPD current-period access** (blocker 1/2) — resolve the compilation/JSON-API
  method, since the FOIA CSV cannot see Affinity's current filing. This gates
  everything else.
- **Structured join + sovereign-detection mapping** — key candidate emission on
  Schedule D 7.B `% non-US` + beneficial-owner concentration + the 5.D(l) column,
  flagging for research; never auto-assert sovereign identity.
- **`form_adv` PrimarySource variant** plus the three pending May-21 schema sign-offs
  (`advocacy_report`, `congressional_document`/`congressional_letter`,
  `corporate_registration`), so ADV-sourced records carry typed provenance. Out of
  scope for this discovery pass.
- **Covered-adviser inventory** — the RIAs tied to covered persons whose ADVs the
  collector should sweep, derived from PROJECT.md.

Per the handoff, this pass writes no collector code, adds no `form_adv` schema
variant, designs no candidate emission, and pulls no adviser beyond the Affinity
pilot. The future package path is `collectors/adv_iapd/`, created in #34 once the
IAPD current-period access method is settled.
