# Handoff #34 — ADV/IAPD current-period access recon

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-14-handoff-34-adv-iapd-current-period-recon.md`
**Lineage:** ADV/IAPD. Global-sequential numbering; #33 is the discovery handoff, so this is #34.
**Depends on:** Handoff #33 (ADV/IAPD discovery). Branch off `main` once the #33 PR has merged, so the discovery report and samples are present. If #33 hasn't merged yet, branch off `feat/adv-iapd-discovery` and say so in the report.
**Type:** recon, not implementation. No collector code, no schema or record changes. Resolves one open blocker from the #33 discovery report.

## What this resolves

Discovery found that Form ADV is a structured-CSV ingest, not a PDF parse: every sovereign-relevant Part 1A field is a bulk-data column. One blocker stands in the way of treating that as the whole ingestion story. The bulk FOIA CSV lags to 2024-12-31, so Affinity's current filing (2026-03-22, $6.16B AUM) is not in it. Current-period data is reachable only through IAPD, whose surfaces #33 flagged as awkward: the firm pages are a single-page app with no HTML data, the compilation XML is JS-gated, and the clean per-firm path serves a PDF.

This recon answers one question: is there a scriptable, structured, current-period (2025 onward) Form ADV surface, or does current data come only as a per-firm PDF? The answer sets the ADV collector's real cost and decides whether the build is a clean structured ingest or a hybrid.

## What Code needs to do

### Step 1: Probe for a structured current-period surface

Three targets, in order:

- `https://adviserinfo.sec.gov/adv`. The SEC's Form ADV Data page states current filings (January 1, 2025 onward) live here, separate from the lagging FOIA CSV. Fetch it and determine whether the 2025-onward data is a direct structured download (CSV, XML, or ZIP) or only viewable behind the app. Look for a direct file URL.
- The IAPD firm-detail app. Fetch the page's JavaScript bundle and grep it for API endpoint patterns (`api.`, `.json`, fetch/XHR call sites, query URLs). A single-page app fetches its data from a backend; identify the endpoint the firm-detail view calls.
- The compilation download (`https://adviserinfo.sec.gov/compilation`). Check whether a direct zip URL exists behind the JS gate.

Apply the SEC-policy User-Agent #33 already found necessary for `www.sec.gov` where the surface requires it.

### Step 2: Test against Affinity's current filing

For any candidate structured surface, test it on CRD 315482. Confirm it returns the current 2026-03-22 filing, not a stale one, by matching the #33 figures: $6.16B AUM, $6.10B across three 100% non-US-owned funds, Parallel Fund I at $4.31B across 6 beneficial owners. Confirm the sovereign-relevant fields (Item 5.D client matrix, Schedule A/B owners, Schedule D 7.B percent non-US owners) are present and parseable in whatever format the surface returns. Record the access method: URL, required headers, format, and any rate limit.

### Step 3: Render the cost verdict

State which of two outcomes holds, with the evidence behind it:

- Verdict A: a clean, scriptable, current-period structured surface exists. The ADV collector is a light structured ingest end to end, historical and current from the same kind of source.
- Verdict B: no structured current surface; current filings come only as per-firm PDF. The ADV collector is a hybrid, structured CSV for filings through 2024 and a PDF parse for 2025 onward, closer to the OGE 278 build for the current slice.

Do not round toward A. If the only current-period structured access requires a browser session or a credential a scheduled collector can't hold, that is Verdict B.

### Step 4: Write up the recon

Append a "Current-period access" section to `docs/collectors/adv-iapd-discovery.md` covering the surfaces probed, the working endpoint and access method if one was found, the Affinity test result, and the cost verdict. Update the discovery report's blockers section to mark this blocker resolved, or to record the PDF fallback if Verdict B.

### Step 5: Commit

Single commit: `docs(collectors): resolve ADV/IAPD current-period access (Handoff #34)`, including this handoff doc. Don't push unless asked.

## What this doesn't do

- Doesn't build the collector. The future package path stays `collectors/adv_iapd/`, unwritten.
- Doesn't parse a full filing. One test fetch to confirm field presence is enough; this is recon, not ingestion.
- Doesn't rank ADV against the other tiers. That call comes after the cost verdict, not in this handoff.
- No schema or record changes.

## After this lands

- Verdict A points to the ADV collector build: structured ingest plus sovereign-detection mapping keyed on Schedule D 7.B percent non-US owners, beneficial-owner concentration, and fund scale, not percent non-US alone.
- Verdict B points to a decision rather than a build: whether the hybrid cost is worth paying now, or whether a tier that carries sovereign identity as primary source (EDGAR 13F/13D/13G, where sovereign funds name their public-equity stakes) takes the next slot first.

Either way, the pathway-ranking call is the next decision, informed by what this recon costs out.

---

read docs/handoffs/2026-06-14-handoff-34-adv-iapd-current-period-recon.md and follow
