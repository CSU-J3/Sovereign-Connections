# FSF Watchlist — entry criterion, source taxonomy, and evaluated entries

**Date:** 2026-05-30
**Status:** living document; v0.4 (four entries: 2 evaluated, 1 watch, 1 out)
**Scope:** the research queue for the Foreign Sovereign Funds tracker. Subjects worth pulling and evaluating for a sovereign-source nexus, across all source types — NOT a 278e-pull queue. Filing status does not gate inclusion.
**Owner:** CJ
**Related:** `docs/references/methodology-note-catalog-inclusion.md` (the catalog rule this mirrors); PROJECT.md Defined Terms.

## What the watchlist is, and is not

The watchlist is a list of **subjects to evaluate** — people or vehicles where credible reporting raises a sovereign-source financial nexus worth structuring against the tracker's standard. It is the input queue, distinct from:
- `sovereign_entities.json` — the catalog of sovereign-source **vehicles** that have cleared the standard (PIF, MGX, etc.).
- the **records** (SC-###) — the structured findings, e.g. SC-007.

A subject on the watchlist has not been adjudicated. Inclusion means "worth pulling the primary record and evaluating," not "confirmed sovereign-linked."

## Entry criterion (evaluation-gated, mirrors the catalog rule)

A subject enters the watchlist when **both** hold:

1. **A credibly-reported sovereign-source nexus** — reporting (primary or reputable secondary) describes a financial relationship between the subject's holdings/business and a sovereign or sovereign-adjacent vehicle, specific enough to name the vehicle and the relationship. Not "is politically prominent," not "is Gulf-adjacent," not "is controversial." A named sovereign-source vehicle and a described financial tie.

2. **A retrievable primary record exists** — there is a document (or document type) that would let the nexus be evaluated against the standard: a 278e, an SEC ADV, an SEC deal filing, a foreign corporate registry, a government MOU, etc. If no primary record is reachable even in principle, the subject stays a **note**, not a watchlist entry (there's nothing to evaluate).

**Symmetry guard — load-bearing.** The criterion is applied identically regardless of the subject's politics, party, or who they're associated with. The failure mode this guards against: the watchlist quietly becoming a list of politically disfavored names with a methodology wrapper. The test for every entry is "would I add a subject with the opposite political valence on this same quality of evidence?" If the honest answer is no, the entry doesn't meet the criterion. A subject is removed or downgraded if the nexus turns out to rest only on prominence or association rather than a named vehicle and a described tie.

## Source-type taxonomy

Subjects don't share a source type. The eventual discovery/retrieval mechanism must handle several; a single 278e drop-directory is insufficient (Affinity alone breaks it). Tag every entry with its primary source type:

| Tag | Source | Retrieval path | Parse status |
|-----|--------|----------------|--------------|
| `278e` | OGE Form 278e public financial disclosure | request-gated (OGE Form 201) or agency/White House PDF release; **no public bulk API** | parser built (`collectors/oge_278/`) |
| `adv` | SEC Form ADV (investment advisers) | SEC IAPD / Investment Adviser Public Disclosure; public, structured | parser built (`collectors/adv_iapd/`) |
| `sec-deal` | SEC transaction/ownership filings (13D/G, S-1, etc.) | EDGAR; public, structured | no parser yet |
| `registry` | foreign corporate registry | per-jurisdiction; varies | manual |
| `gov-doc` | government MOU, sovereign-fund disclosure, official statement | per-source; often press-released | manual |
| `other` | reporting-only, no clean primary doc | n/a | manual / note-only |

A subject can carry more than one tag (a sitting official with both a 278e and an SEC footprint). The retrieval mechanism is **deferred** until the watchlist has enough entries of a given source type to justify automating that type. (278e drop-directory was deferred for exactly this reason — only one 278e subject so far.)

## Disposition states

- `active` — nexus meets the criterion; primary record identified; ready to pull/evaluate or already in progress.
- `evaluated` — primary record pulled and structured into a record (or correctly rejected); cross-reference the SC-### or the rejection rationale.
- `watch` — nexus reported but criterion not yet fully met (no named vehicle, or no retrievable primary record); held as a note, not yet worked.
- `out` — evaluated and rejected, or failed the symmetry/criterion test; keep with the reason (the audit trail that the bar was applied).

---

## Entries

### W-001 — Steven C. Witkoff
- **Source type:** `278e` (+ `gov-doc` for the off-filing ties)
- **State:** `evaluated` → SC-007
- **Nexus:** USD1 stablecoin stack (WLF + SC Financial Technologies, both retained holdings at 41.8.1 / 41.9.1 on the 2025-08-13 New Entrant 278e). Sovereign-source ties: MGX (Abu Dhabi state-owned) settled $2B into Binance via USD1; Pakistan PVARA MOU signed with SC Financial Technologies. Sitting official (Special Envoy).
- **Primary records:** 278e (pulled); Binance announcement; PVARA statement; Senate Banking correspondence. Full evidence base in `docs/references/wlf-research-target.md`.
- **Drift guards on record:** relationship documented, no causal claim re: chip decision or CZ pardon; MGX and Pakistan legs kept distinct. Sustained in SC-007.
- **Owed:** MGX state-ownership + USD1 co-ownership primary anchors (catalog hygiene).

### W-002 — Jared Kushner / Affinity Partners (A Fin Management LLC)
- **Source type:** `adv` (+ `sec-deal` for the EA consortium)
- **State:** `evaluated` → SC-009 — primary record (SEC ADV, A Fin Management LLC, CRD 315482) pulled and structured.
- **Promoted to:** SC-009 (`promoted_to: SC-009`).
- **Nexus:** Affinity Partners (wholly owned by Kushner; SEC entity A Fin Management LLC) is sovereign-funded at scale. PIF (Saudi) anchored ~$2B in 2021. Qatar Investment Authority (sovereign) and Abu Dhabi's Lunate added ~$1.5B in 2024. AUM ~$4.8B by end-2024, ~99% non-US-person capital. Three sovereign / sovereign-adjacent funds into a single vehicle owned by a former senior official.
- **Not a 278e subject:** Kushner left government Jan 2021; Affinity was incorporated the day after. No current filing obligation. The nexus lives in **SEC ADV filings**, not OGE disclosure — this is the entry that proves the watchlist must be broader than 278e.
- **Primary records to pull:** SEC Form ADV for A Fin Management LLC (AUM, client-composition %, beneficial owners); SEC filings on the EA acquisition consortium (Affinity / PIF / Silver Lake). Congressional records (Wyden 2024, Maloney 2022 probe) are **primary correspondence but advocacy** — usable for transaction facts (the $2B, the ~$40M/yr fee figures, the PIF screening-committee objection overruled by MBS), not for their causal conclusions.
- **Drift guards (pre-loaded for when this is structured):**
  - **No payback inference.** The oversight letters frame the investment as potential payback for Kushner's official acts (his MBS relationship while in the White House). That is drift mode 1 (payment → caused outcome) and is denied. The record documents that sovereign funds placed $3.5B into a vehicle wholly owned by a former official who had a close relationship with the controlling principal while in office. It stops there.
  - **EA deal is business-development, not an official act.** Kushner reportedly introduced PIF to EA and led talks; document that as what it is. He held no government office in 2025-26, so there is no official act to causally link.
  - **Distinguish the three sovereign funds.** PIF, QIA, and Lunate are separate vehicles with separate governance — catalog and cite each on its own, don't fuse into "Gulf money."
- **Symmetry check:** passes — a former official of any party with three named sovereign funds anchoring a wholly-owned vehicle at 99% foreign capital would clear this criterion on the same evidence.

### W-003 — Charles Kushner / Ambassador to France & Monaco
- **Source type:** `278e`
- **State:** `out` — evaluated on a full read of the primary record; no sovereign-source nexus found.
- **Record read:** certified Nominee 278e (signed 2025-01-25, certified 2025-04-15). Full read across Parts 1–5/8 and endnotes.
- **What the filing shows:** a domestic real-estate and trust portfolio — Westminster Management, the Carmel and Nara Nevada trusts, and 480+ Kushner Companies property LLCs — plus commercial-bank liabilities. **No sovereign or sovereign-adjacent counterparty appears anywhere** in the disclosure.
- **Items checked and cleared:**
  - **Qiagen N.V.** — ordinary Dutch-listed stock, not a sovereign holding.
  - **Israel Discount Bank** — a commercial loan *owed*, not a sovereign investment.
  - **Temerity Fund LP** — a small US private-equity commitment, no sovereign LP on the face of the record.
- **Why not on prominence/association:** familial proximity to Jared Kushner's Affinity/PIF nexus (W-002) does **not** transfer. The criterion requires a named vehicle and a described tie in *this* subject's record; neither is present. Adding him on the family link alone is exactly the symmetry-guard failure mode the watchlist exists to prevent.
- **Reopen condition:** only if reporting surfaces a sovereign LP inside one of the entity structures (a fund or vehicle in the portfolio with a sovereign limited partner). Absent that, stays `out`.

### W-004 — Donald Trump Jr. / 1789 Capital Management, LLC
- **Source type:** `adv`
- **State:** `watch` — ADV primary record pulled and structured into candidates (CAND-172 through CAND-186, Handoff #42); non-US ownership is documented but no sovereign source is identified, so 1789 stays out of the SC catalog with a defined promotion trigger. Distinct from W-003 `out`: this entry has documented non-US ownership, not an absent nexus.
- **Subject / qualifying interest:** 1789 Capital Management, LLC (CRD 335007). Covered person Donald Trump Jr., a named family member (the President's son) and partner at the firm. The qualifying financial interest is the partner/employment role under 5 CFR 2640.103(a), **not** Schedule A ownership — he is not a Schedule A owner of the adviser; the Form ADV references him only as "DTJ" in disclosing the New York Attorney General injunction barring him from serving as an officer or director of a New York entity. See `docs/references/covered-adviser-inventory.md`.
- **Nexus:** 1789's funds report non-US beneficial ownership at scale, and the firm is reported to be open to sovereign-wealth-fund capital from countries it considers "pro-American." No public source names a sovereign limited partner in any 1789 fund.
- **What is documented:**
  - **SEC Form ADV** (CRD 335007, filing 2026-03-31): 15 of 26 private funds report non-US ownership at Schedule D 7.B. **Category 1.** Firm-level Item 5.F(3) non-US *client* AUM is $0; the per-fund 7.B beneficial-owner figure is the signal, not Item 5 — the two measure different things (see the inventory note on the distinction).
  - **Reuters**, "Trump-linked venture fund 1789 Capital tops $1 billion in assets," September 8, 2025: the firm is open to accepting foreign investors including sovereign wealth funds from countries it considers "pro-American," per people familiar with the firm. **Category 3.** Establishes a stated willingness to take sovereign capital; names no specific sovereign fund and reports no specific sovereign investment. (Byline and canonical reuters.com URL not yet pinned.)
- **Why it stays out:** the sovereign-source test requires a named foreign sovereign, sovereign wealth fund, state-owned enterprise, or controlling-interest chain, established through a category-1 source or category-3 reporting that cites underlying primary documents. Non-US ownership alone does not clear scope, because the owners may be private foreign nationals, which the definition excludes. A stated policy of accepting sovereign money is not a documented sovereign flow. No public source names a sovereign limited partner in any 1789 fund.
- **Promotion trigger** (the forward-looking analog of W-003's reopen condition): a named sovereign limited partner (foreign treasury, SWF, SOE, or controlling-interest chain) in any 1789 fund, established through a category-1 source or category-3 reporting that cites underlying primary documents. On that, the relevant candidate among CAND-172 through CAND-186 promotes through the existing pipeline.
- **Linked candidates:** CAND-172 through CAND-186 — the 15 ADV candidates emitted in #42, which stay `unreviewed`; the watchlist entry carries the disposition.
- **Symmetry note:** evaluated on the documented fact pattern, not prominence. An opposite-party analogue — a President's child as a partner in a registered adviser whose funds report non-US ownership with no named sovereign limited partner — resolves the same way: a watch, not a record. Distinct from W-003 (Charles Kushner, `out`, no nexus at all); W-004 has documented non-US ownership but an unestablished sovereign source.

---

## How the next entry gets added

1. Reporting raises a nexus → check it against the **entry criterion** (named vehicle + described tie + retrievable primary record + symmetry test).
2. If it passes: add as `W-###`, tag the **source type(s)**, set state `active` or `watch`, write the one-line nexus and the primary records to pull.
3. Pull the primary record, evaluate against the standard, structure into an SC-### or reject with reason → state `evaluated`.
4. New source types (first `adv`, first `sec-deal`) each justify their own parser/retrieval handoff once there's enough volume. Until then, retrieval is manual.

## Deferred / owed

- **Retrieval mechanism** (drop-directory or per-type fetchers): deferred until a source type has enough entries to justify automation. Currently 1 × `278e`, 2 × `adv` — not yet.
- **ADV parser:** done — built in #35/#36 (`collectors/adv_iapd/`). W-002 was worked manually (SC-009) before it existed; W-004 (1789) is now the second `adv` subject, worked through the parser.
- **Lunate governance verification:** SC-009 surfaced Lunate (Abu Dhabi) as a sovereign-vehicle catalog candidate but it was **not** added — its governance (state-owned vs. state-adjacent) is unverified. Verify governance and catalog it on its own line if it clears the standard; keep it **distinct from MGX** (separate Abu Dhabi vehicle already in catalog via SC-007). PIF and QIA were already in `sovereign_entities.json` and needed no addition.
- **Breadth pass:** a wider search for additional subjects (other principals with reported sovereign-source nexuses) runs *against this template* in a later session, so each candidate is evaluated, not just listed.
