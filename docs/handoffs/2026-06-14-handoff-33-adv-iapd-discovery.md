# Handoff #33 — Form ADV / IAPD collector discovery

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-14-handoff-33-adv-iapd-discovery.md`
**Lineage:** ADV/IAPD (a tier tag, not the number). Handoff numbers are global-sequential; latest on disk is #32, so this is #33.
**Type:** discovery, not implementation. No collector code, no schema changes.

## What this resolves

Form ADV is the second load-bearing primary record for the tracker, after OGE 278. OGE 278 covers the disclosed-interest side: what an officeholder or covered person reports holding. Form ADV covers the other side of the same transaction, the investment adviser receiving the capital and where that capital comes from. For sovereign-source detection that second side is often where the money is actually visible.

The worked case is already in the catalog. SC-009 (A Fin Management LLC, brand name Affinity Partners, sole owner Jared Kushner) was built by hand off Affinity's Form ADV and Part 2A brochure. Affinity reports several billion dollars in discretionary AUM, and reporting on its filings has tied UAE sovereign-wealth and Qatari capital to the firm at over $200 million each, with Saudi PIF described as the dominant funder. Whether those investor identities and amounts sit in the ADV itself or only in the reporting around it is one of the things discovery has to settle. That record is the tracker's first ADV-sourced entry and its only one, and it was transcribed by hand. A collector makes it reproducible and lets the same surface be checked for other advisers tied to covered persons.

ADV is also the only source tier with a live record and no scaffold at all. The flat `*_collector.py` files cover FARA, SEC EDGAR, PACER, CFIUS, and foreign registries as `NotImplementedError` stubs; there is no ADV stub. This handoff is discovery: map how the SEC publishes Form ADV, pull Affinity as the pilot, document which fields carry the sovereign signal, and resolve the ingestion-path question before any parser is written.

## What Code needs to do

### Step 1: Map the publication surfaces

Form ADV is filed to IARD (operated by FINRA) and published by the SEC through several surfaces. Confirm each is reachable and note what it serves:

- IAPD firm/individual search at `https://adviserinfo.sec.gov`. The front door; search by firm or individual, returns the most recent filing.
- Per-firm full ADV as PDF at `https://reports.adviserinfo.sec.gov/reports/ADV/{CRD}/PDF/{CRD}.pdf` (verified pattern: CRD 158935 resolves to that path). Keyed on the firm's CRD number.
- Bulk Form ADV data sets. Filings from January 1, 2025 to present are on IAPD (`https://adviserinfo.sec.gov/adv`); historical Part 1A with all Schedules and DRPs, back to 2001, is in CSV at `https://www.sec.gov/foia-services/frequently-requested-documents/form-adv-data`. These are multi-table sets that link on identifiers.
- Compilation download (all SEC-registered advisers plus exempt reporting advisers) in XML at `https://adviserinfo.sec.gov/compilation`.
- Part 2A firm brochures as PDF (the narrative disclosure), available through IAPD per firm.

Record which surface is authoritative for which content, and whether any require authentication, have rate limits, or carry robots/terms constraints that would shape a scheduled collector.

### Step 2: Resolve and pilot-retrieve Affinity

The filing entity is **A Fin Management LLC** (brand name Affinity Partners), a Delaware LLC, offices in Florida, sole owner Jared Kushner. It files a full Part 1A plus a Part 2A brochure, so it is a registered adviser, not an exempt reporting adviser (ERAs do not file Part 2).

- Search IAPD for "A Fin Management" and "Affinity Partners" and resolve the firm's CRD number and SEC file number (the 801- number). Document both; do not guess them.
- Pull the full ADV PDF (the `reports.adviserinfo.sec.gov` path above) and the most recent Part 2A brochure. Save to `data/samples/affinity-adv-{filing-date}.pdf` and `data/samples/affinity-adv-part2a-{filing-date}.pdf`.
- Pull Affinity's rows from the bulk CSV data set for the same period and save the extract to `data/samples/affinity-adv-{filing-date}-part1.csv` (or a small set of linked extracts if the schema spans tables). This is the input for the ingestion-path question in Step 4.

If Affinity files under an umbrella registration or has affiliated advisers with their own CRDs, note them rather than collapsing them. The Part 2A names "investment advisory affiliates" collectively, and the entity graph matters for promotion later.

### Step 3: Map the sovereign-relevant fields

Read Affinity's actual filing and document where sovereign capital becomes visible, confirming the field locations against the form rather than assuming them. The places to check:

- Item 5.D client-type breakdown, which reports number of clients and AUM by client type. Confirm whether the form carries a category for sovereign wealth funds and foreign official institutions, and whether Affinity's filing populates it.
- Schedule A and Schedule B (direct and indirect owners), for ownership and control persons.
- Schedule D Section 7.B private-fund reporting, for the funds Affinity manages and their characteristics.
- The Part 2A brochure narrative, for client-concentration or funding-source language the structured items do not capture.

For each, record what Affinity's filing actually shows about the PIF / QIA / UAE capital, and which field a future collector would key on to flag a sovereign-source client. If the filing reports only aggregate client-type and AUM totals without naming individual sovereign investors, say so plainly; that is itself a finding about the limit of the source.

### Step 4: Resolve the ingestion path (the load-bearing question)

Unlike OGE 278, Form ADV is published as structured bulk data, not PDF only. The decision that shapes the whole collector: do the sovereign-relevant fields from Step 3 appear in the bulk CSV in structured form, or only in the per-firm PDF and Part 2A narrative?

Compare the Affinity bulk-CSV extract against the Affinity PDF for the Step 3 fields. Document, field by field, which surface carries each. If the bulk CSV carries Item 5.D, the owner schedules, and the private-fund rows, the collector is a structured ingest and parsing is largely a join problem. If the sovereign signal lives only in the brochure narrative, it is a PDF-parsing problem closer to the OGE 278 build. Name which it is; do not assume the cleaner answer.

### Step 5: Produce the discovery report

Create `docs/collectors/adv-iapd-discovery.md` (same shape as `docs/collectors/oge-278-discovery.md`) covering:

- The publication surfaces from Step 1, with the working URL patterns and access method for each.
- Affinity's resolved identifiers (CRD, SEC file number) and the filings retrieved.
- The sovereign-relevant field map from Step 3, with what Affinity's filing shows in each.
- The ingestion-path finding from Step 4, stated as a recommendation (structured CSV ingest, PDF parse, or hybrid).
- Blockers and unknowns for the production collector: bulk-data refresh cadence, how amendments and historical versions are tracked, whether exempt reporting advisers (which file only a subset of items) will matter for other covered advisers, and the umbrella/affiliate entity question.

### Step 6: Commit

Two commits, in order:

1. `data(samples): add Affinity (A Fin Management) Form ADV pilot` for the PDF, brochure, and CSV extract.
2. `docs(collectors): add ADV/IAPD discovery report (Handoff #33)` for the discovery doc and this handoff doc together.

Don't push unless asked.

## What this doesn't do

- Doesn't write the collector. There is no ADV stub to fill; the future package path is `collectors/adv_iapd/`, created in a later handoff once discovery names the ingestion path.
- Doesn't pull advisers beyond Affinity. Affinity is the pilot, the way Witkoff was for OGE 278. The broader covered-adviser inventory waits for the production collector.
- Doesn't add the `form_adv` PrimarySource variant. That is records-layer schema work, and it bundles with the three variant sign-offs still pending from May 21 (`advocacy_report`, `congressional_document`, `corporate_registration`), not with this discovery pass.
- Doesn't design candidate emission for ADV rows. That is informed by what Step 4 finds, and is a later handoff.

## After this lands

Natural #34 candidates, depending on the ingestion-path finding:

- ADV parser / ingest design: structured CSV if Step 4 says the fields are there, PDF parsing if they are not.
- Sovereign-detection field mapping into the candidate schema, keyed on the Step 3 fields.
- The `form_adv` PrimarySource variant plus the pending schema sign-offs, so ADV-sourced records carry typed provenance.
- Covered-adviser inventory: the RIAs whose filings the collector should sweep, derived from the covered-persons definition in PROJECT.md.

The discovery report's blockers section decides the order.

---

read docs/handoffs/2026-06-14-handoff-33-adv-iapd-discovery.md and follow
