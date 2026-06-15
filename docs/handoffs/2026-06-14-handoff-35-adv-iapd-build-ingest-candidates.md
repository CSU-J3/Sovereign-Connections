# Handoff #35 — ADV/IAPD collector build: structured ingest + candidate emission (Affinity worked pass)

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-14-handoff-35-adv-iapd-build-ingest-candidates.md`
**Lineage:** ADV/IAPD. Global-sequential numbering; #34 was the recon, so this is #35.
**Depends on:** Handoffs #33 (discovery) and #34 (recon). `docs/collectors/adv-iapd-discovery.md` (with §8) is the source spec for surfaces, tables, and fields. Branch off `main` once PR #11 has merged. If #11 hasn't merged yet, branch off `feat/adv-iapd-discovery` and say so in the report.
**Type:** build. Adds the ADV ingest and candidate-emission modules and extends `web/data/candidates.json`. No `records.json` changes, no `web/lib/types.ts` changes (candidates are the Python/JSON pipeline layer, not the TS records layer).

## What this builds

The first build slice of the ADV collector. Recon returned Verdict A, so this is a structured ingest, not a PDF parse. Build the ingest and the candidate emission, validate end to end against Affinity, and land ADV candidates in `web/data/candidates.json`. The proxy limit stands: ADV gives ownership shape, never sovereign identity, so emitted candidates carry the proxy signal and stay unreviewed until a human promotes them with secondary-source identity work.

This pass is seeded, not universal. The collector runs against a list of covered-person-connected adviser CRDs, not the whole 23,478-firm RIA universe (which would emit noise, since most large private funds have non-US LPs). For this handoff the seed is one firm: Affinity (A Fin Management LLC, CRD 315482). Growing the seed list is separate work.

## Scope guardrails (apply, don't re-litigate)

Carried over from the OGE collector so the two stay one pipeline:

- Sequential `CAND-###` IDs, continuing the existing sequence (168 candidates as last reported; confirm the current max on disk and start at the next integer, no gaps). No semantics in the ID; provenance lives in `source_filing`.
- Conservative over-emission. For a seeded adviser, emit a candidate for every private fund that reports non-US ownership. Filtering to actual sovereign scope happens at promotion, not at collection. Do not drop funds because the non-US share looks ordinary; that judgment isn't the collector's.
- `connected_businesses.json` registry still deferred. Candidates carry `business_id: null`.
- Seeded adviser list. CRD 315482 (Affinity) only, this pass.

## What Code needs to do

### Step 1: ADV ingest for a CRD

Per `docs/collectors/adv-iapd-discovery.md` §8, fetch and assemble the structured ADV record for a given CRD from the current-period surface. Read the table and column details from the discovery doc; do not reconstruct them from memory. The tables that carry the signal:

- `IA_ADV_Base` for firm-level Item 5: regulatory AUM (the `Q5F2C` field) and non-US AUM (`Q5F3`, Item 5.F(3)).
- `IA_Schedule_D_7B1` for per-fund Schedule D 7.B: fund name, gross asset value, percent non-US owners, and beneficial-owner count.
- Schedule A / Schedule B tables for direct and indirect owners.

Join on CRD and filing id into a per-firm object that holds the firm's Item 5 totals, its owner rows, and a list of its private funds with their 7.B fields. Build the ingest to fetch from the live structured surface; the Affinity samples already in `data/samples/` from #33 are the known-good reference to check it against.

### Step 2: Validate the ingest against Affinity

Run the ingest on CRD 315482, current filing 2026-03-22, and confirm it reproduces the recon figures: $6.16B regulatory AUM, $6.10B across three 100% non-US-owned funds, Parallel Fund I at $4,307,145,842 across 6 beneficial owners, with Delta and Sigma also 100% non-US. If the assembled object doesn't reproduce these, stop and flag the gap rather than adjusting numbers to fit.

### Step 3: Extend the candidate schema for ADV

Follow the candidate shape already in `web/data/candidates.json` (the OGE candidates are the precedent) and extend it for ADV rows. The mapping:

- `disclosure_type`: `adv_private_fund`, keyed to Schedule D 7.B, not inferred from the row. Add it to the taxonomy alongside the existing OGE part-keyed types; don't retrofit the OGE types onto ADV rows.
- `source_filing`: provenance back to the ADV filing. At minimum `source` ("adv_iapd"), CRD, SEC file number (801-122021 for Affinity), filing date, and the table/source pointer. Mirror how the OGE candidates structure `source_filing`.
- `raw_value`: a structured object copying the fund's 7.B fields verbatim (gross asset value, percent non-US owners, beneficial-owner count, fund identifiers). Same posture as the OGE `raw_value` object; copy from the parse, never retype.
- `filer`: the adviser legal name ("A Fin Management LLC").
- `business_name`: the private fund name as it appears in `IA_Schedule_D_7B1`.
- `business_id`: null.

If an ADV row doesn't map cleanly to the existing candidate fields, propose the extension and flag it; don't force the row into an ill-fitting shape.

### Step 4: Emit candidates (Affinity worked pass)

Over the seeded adviser (CRD 315482), emit one candidate per private fund reporting non-US ownership. Continue `CAND-###` from the current max. Every candidate emits at `promotion_status: "unreviewed"`, `business_id: null`. The `scope_hypothesis` is the only hand-authored field: hedged, carrying the proxy reasoning (percent non-US, owner concentration, fund scale) and stating plainly that owner identities are not in the ADV and the sovereign source is unverified. Never assert a sovereign connection.

If the worked pass yields fewer funds than expected, emit what's there and note the count; don't pad.

### Step 5: Verify before reporting back

- `web/data/candidates.json` is valid JSON; every object carries the required fields.
- New ADV candidate IDs continue sequentially from the existing OGE candidates with no gaps.
- Every new `business_id` is null; every new `promotion_status` is `"unreviewed"`.
- Spot-check 2 ADV candidates back to their source ADV rows; confirm `raw_value` matches the ingest, not a drifted paraphrase.
- No `scope_hypothesis` states a sovereign connection as fact.
- The existing 168 OGE candidates are untouched.

### Step 6: Commit

Single commit: the ingest and candidate-emission modules under `collectors/adv_iapd/`, the extended `web/data/candidates.json`, and this handoff doc. Match the existing commit-message convention. Don't push unless asked.

## Flag back, don't decide

- The `filer` / `business_name` mapping. This handoff sets filer = adviser, business_name = fund. The covered-person interest is in the adviser (Kushner owns A Fin Management), not the fund, so an alternative is to carry the adviser as `business_name`. Confirm the mapping before it's baked into 100+ future candidates.
- The `source_filing` shape if ADV provenance doesn't fit the OGE structure.
- Whether the fund-name field needs normalization (umbrella/affiliate naming from #33).
- Any schema gap the seed-of-one worked pass surfaces.

## What this doesn't do

- Doesn't expand the seed list beyond Affinity. The covered-adviser inventory is a later handoff.
- Doesn't build the package plumbing to OGE parity (wrapper, discover stub, regression guard, CI). That's #36.
- Doesn't touch `records.json` or `web/lib/types.ts`. ADV candidates are pipeline rows, not records.
- Doesn't tune detection thresholds. Emission is conservative now; ranking on the proxy signal is a promotion-time judgment.

## After this lands

- #36: package plumbing for `collectors/adv_iapd/` (wrapper chaining ingest to candidates, discover stub, regression guard, CI) to match the OGE package.
- Covered-adviser inventory to expand the seed list beyond Affinity, derived from the covered-persons definition in PROJECT.md.
- The `form_adv` PrimarySource variant on the records layer, plus the three schema sign-offs still pending from May 21, for when ADV candidates get promoted to SC-### records.

---

read docs/handoffs/2026-06-14-handoff-35-adv-iapd-build-ingest-candidates.md and follow
