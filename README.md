# Sovereign Connections Tracker

![status](https://img.shields.io/badge/status-pre--launch-orange) ![data collection](https://img.shields.io/badge/data%20collection-not%20yet%20active-lightgrey) ![scope](https://img.shields.io/badge/scope-foreign%20sovereign%20%26%20sovereign--adjacent-blue)

A research tracker monitoring foreign sovereign and sovereign-adjacent money flowing to businesses in which a named family member of the current administration holds a documented financial interest. The beat is mechanism-focused: how do existing legal frameworks for foreign-influence oversight (the foreign Emoluments Clause, FARA, FIRRMA, OGE conflict-of-interest rules, CFIUS, the Lobbying Disclosure Act) engage or fail to engage with this class of transaction.

This repo currently contains only the project scope and methodology. Data collection is not yet active. Companion project to [Follow-the-Moneys](https://github.com/CSU-J3/Follow-the-Moneys) (post-conflict reconstruction) and [Connected-Procurement](https://github.com/CSU-J3/Connected-Procurement) (federal civilian procurement).

## Status

| Item                          | State                                                            |
| ----------------------------- | ---------------------------------------------------------------- |
| Scope statement               | Documented (this README)                                         |
| Defined terms                 | Documented (see below)                                           |
| Primary source list           | Documented (see below)                                           |
| Sovereign wealth fund registry| 11 entries at `/swfs` (3 with primary_sources; seven seeds queued)|
| Connected business registry   | Not built                                                        |
| Collector code                | Stubs only                                                       |
| Data file                     | 8 records (2 LIVE), 11 entities; collectors not yet wired        |
| Public dashboard              | [sovereign-connections.vercel.app](https://sovereign-connections.vercel.app) |
| Methodology page              | Live at `/methodology` (v2.0 adopted 2026-05-05)                 |
| Live records collected | SC-007 (World Liberty Financial), SC-008 (Witkoff Group · Roosevelt redevelopment) |

The repo exists at this stage to document the scope publicly before any data collection begins.

## Core analytical question

How do existing legal frameworks for foreign-influence oversight engage or fail to engage with foreign sovereign and sovereign-adjacent money flowing to businesses connected to named family members of the current administration?

The relevant frameworks include:

- The foreign Emoluments Clause (Article I, Section 9, Clause 8) and its modern case law (DC and Maryland v. Trump, Blumenthal v. Trump, the early-republic ratifying-era discussion)
- The Foreign Agents Registration Act (FARA, 22 USC 611-621) and DOJ enforcement practice
- The Foreign Investment Risk Review Modernization Act of 2018 (FIRRMA) and CFIUS jurisdiction
- OGE conflict-of-interest rules at 5 CFR Part 2635, particularly 2635.204 (gifts from foreign governments)
- The Lobbying Disclosure Act (2 USC 1601-1614) where it intersects with foreign-financial-flow disclosure
- 18 USC 208 and the conflict-of-interest framework at 5 CFR Part 2640

The frame is descriptive, not prescriptive. The tracker documents how oversight engages, or doesn't, with a defined class of transaction. It does not allege quid pro quo or intent.

## Defined terms

All three definitions are fixed. Changes are versioned with a dated changelog entry.

### Named family member

Same as Connected Procurement, for cross-tracker consistency. Exhaustive list: the President's children and their spouses; the President's siblings and their spouses; relatives by blood, marriage, or adoption who hold or held Senate-confirmed positions during this administration. Excludes friends, business associates without family tie, in-laws of in-laws, romantic partners short of marriage.

### Financial interest

Per 5 CFR 2640.103(a) and 18 USC 208(a):

- Ownership stake (any share, partnership interest, or membership interest)
- Employment by the entity (including consulting and contractor relationships)
- Debt instruments held by the named family member where the entity is the obligor
- Beneficial interest in a trust where the entity is among the trust's holdings
- Spousal interests imputed under 18 USC 208(a)(2)

### Foreign sovereign and sovereign-adjacent money

The category includes:

- Direct payments or investments by foreign governments
- Payments or investments by sovereign wealth funds (PIF, ADIA, Mubadala, QIA, KIA, NBIM, GIC, etc.; the SWF Institute's recognized list is the canonical reference)
- Payments or investments by entities majority-owned by a foreign government (state-owned enterprises)
- Payments or investments by entities where a foreign government holds a controlling interest through a chain of ownership
- Payments or investments by foreign government officials acting in their official capacity (per the foreign Emoluments Clause case law)

The category does not include private foreign nationals, private foreign companies with no documented sovereign ownership, or open-market trades in publicly traded securities by sovereign entities.

When ownership chains are ambiguous, the default is documentation: cite the regulatory filing or court record establishing the sovereign tie, and only include the record if such documentation exists.

## Primary sources

The tracker has the slowest cadence of the three companion projects; many sources publish irregularly or only when triggered by litigation.

| Source                                          | Cadence            | What it covers                          |
| ----------------------------------------------- | ------------------ | --------------------------------------- |
| OGE Form 278 filings                            | Annual             | Public financial disclosure              |
| SEC EDGAR filings                               | On filing          | Investment positions, ownership stakes   |
| Federal court filings (PACER)                   | On filing          | Emoluments and related litigation        |
| FARA registrations and supplemental filings     | On filing/biannual | Foreign agent disclosures                |
| DOJ FARA enforcement actions                    | On publication     | Investigations, prosecutions             |
| CFIUS public determinations                     | Irregular          | Foreign-investment review outcomes       |
| Foreign jurisdiction registries                 | Varies             | Companies House, GAFI, free-zone records |
| Investigative reporting (NYT, ProPublica, FT)   | On publication     | Where primary records are sealed/foreign |

Investigative reporting plays a larger role here than in the other two trackers because primary records on foreign sovereign flows are often sealed, non-U.S., or only surfaced through investigation. The methodology treats reporting as a more weighty source than in BoP or Connected Procurement, but only when the reporting cites underlying documents the tracker can also link.

## Evidence hierarchy

Strongest to weakest:

1. Primary records: OGE 278 filings, SEC filings, court filings, FARA registrations, CFIUS public determinations, congressional testimony, foreign jurisdiction registry filings
2. Tracker data with traceable primary record (federal or foreign-jurisdiction)
3. Investigative reporting from outlets with demonstrated foreign-financial-flow capacity (NYT, WaPo, ProPublica, FT, Bloomberg, Reuters, AP, OCCRP) where the reporting cites underlying documents
4. Analysis from named experts at established institutions (CREW, POGO, academic ethics scholars, Brookings, Lawfare, foreign-influence specialists)
5. Opinion writing

Claims published in the connected research portfolio cite category 1 or 2 by default. Reliance on category 3 is more common here than in the other trackers, and is disclosed.

## Out of scope

Hard exclusions, named to prevent scope drift:

- Federal civilian procurement ([Connected-Procurement](https://github.com/CSU-J3/Connected-Procurement) project)
- Post-conflict reconstruction financial governance ([Follow-the-Moneys](https://github.com/CSU-J3/Follow-the-Moneys) project)
- Routine commercial dealings between U.S. businesses and foreign private entities
- Foreign campaign finance violations (FECA, specialized beat with different evidence rules)
- Foreign lobbying generally, except where it intersects with money flowing to a connected business
- State and local foreign-investment review
- Pre-2025 cases except as comparative methodology references
- Allegations of intent, motive, or quid pro quo absent direct evidentiary support
- The underlying foreign-policy fights about the countries involved
- The political fights about the people involved

## Comparative case set

Historical cases the methodology references:

- Kushner / Affinity Partners $2 billion Saudi PIF investment (2021-present), the closest direct analogue
- Trump Organization 2017-2020 foreign-government bookings (CREW reporting, House Oversight Committee work, foreign Emoluments Clause litigation)
- DC and Maryland v. Trump (foreign Emoluments Clause)
- Blumenthal v. Trump (congressional standing)
- Hunter Biden / Burisma (Ukrainian energy company; documented for methodology completeness even though Ukrainian-private-company status places it at the edge of the sovereign-adjacent definition)
- Ivanka Trump China trademark grants (2017-2018)
- The historical foreign Emoluments Clause record (early-republic ratifying-era discussion, the Edmund Randolph framework, modern case law)

The same evidence rules apply to any case in the comparison set.

## Methodology disclosure principles

Borrowed from BoP and Connected Procurement:

- Every record traces to a primary source (federal or foreign-jurisdiction). Records sourced only to investigative reporting are flagged separately and treated as category 3.
- Every excluded scope decision is documented on the methodology page with the rationale.
- Cadence is disclosed honestly. This tracker has the slowest cadence of the three portfolio projects.
- Defined terms are fixed. Changes are versioned and dated.
- Errors get corrected publicly with a changelog entry, not silent edits.
- Sovereign wealth fund governance structures are documented per fund, not assumed.

## Architecture

```
sovereign-connections/
├── README.md                          # this file
├── PROJECT.md                         # full project instructions for Claude Projects
├── docs/
│   ├── changelog.md                   # versioned methodology changes
│   └── handoffs/                      # per-session handoff docs
├── data/                              # collector write target (Python); for v0 hand-edited seed
│   ├── records.json                   # canonical records (seeded)
│   ├── candidates.json                # pending review (empty for v0)
│   ├── sovereign_entities.json        # sovereign-adjacent entity registry (seeded)
│   └── connected_businesses.json      # entity registry with sourced ties (empty for v0)
├── collectors/                        # Python, stubs only
│   ├── oge_278_collector.py
│   ├── sec_edgar_collector.py
│   ├── pacer_collector.py
│   ├── fara_collector.py
│   ├── cfius_collector.py
│   └── foreign_registry_collector.py
├── web/                               # Next.js 15 dashboard, Vercel project root
│   ├── app/                           # /, /swfs, /record/[id], /methodology
│   ├── components/                    # PascalCase, mirrors cbt convention
│   ├── data/                          # seed JSON read by the dashboard at build time
│   ├── lib/                           # types, data loader, constants, format helpers
│   ├── package.json
│   └── README.md                      # local dev and Vercel deploy notes
└── .github/workflows/                 # collector + deploy automation (stub)
```

The Python and TypeScript halves run on separate lifecycles and on opposite sides of the deploy boundary. Vercel builds only files under `web/`, so the dashboard reads from `web/data/*.json`. The repo-root `data/` directory is the collector write target: Python writes there, and a sync step copies `data/*.json` into `web/data/*.json` before each build. For v0 both locations hold the same hand-edited seed. There is no shared `package.json` and no runtime API between the two. The data contract is the JSON shape itself, defined in `web/lib/types.ts` and mirrored in collector outputs.

## License

Public accountability project. Use it, fork it, build on it.

— CJ / [das_DEMARC:/](https://dasdemarc.substack.com/)

## Related work

- [Follow-the-Moneys](https://github.com/CSU-J3/Follow-the-Moneys): post-conflict reconstruction financial governance, anchored by the Board of Peace
- [Connected-Procurement](https://github.com/CSU-J3/Connected-Procurement): federal civilian contract awards and GSA leases to entities with named-family-member financial interests
