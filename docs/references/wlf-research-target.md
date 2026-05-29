# Research target — World Liberty Financial (Witkoff retained asset)

**Status:** RECONCILED 2026-05-29 — WLF is already recorded as **SC-007** (scope LIVE), which predates this note. CAND-130 → `promoted_to: SC-007`. This doc's earlier "new record" framing was stale and is corrected below; it now serves as the evidence-enrichment record for SC-007.
**Owner:** Corey (off-session, per disclosed-gap principle)
**Source filing:** Witkoff OGE Form 278e, New Entrant, filed 2025-08-13 (`whitehouse.gov/wp-content/uploads/2025/09/Witkoff-Steven.pdf`)
**Candidate status:** in `candidates.json` as **CAND-130** (emitted by the #26 deep-leaf re-run; not present before that). State: `promoted`, `promoted_to: SC-007`.

## What the filing shows

World Liberty Financial appears at **entry 41.8.1**, nested seven levels under:

```
41   Witkoff Holdings LLC        Over $50M, $34,363,535 distributions
41.8   WC Digital Fi LLC
41.8.1   World Liberty Financial (cryptocurrency)   value N/A, income N/A
```

Adjacent: **41.9.1 SC Financial Technologies LLC (stablecoin)** under WC Digital SC LLC.

WLF carries no own value or income line — both N/A. The value rolls up to the parent (Witkoff Holdings LLC). It's a US-domiciled crypto entity with no foreign-signal field anywhere in its row.

## Why it's the live case (and CAND-001 is not)

The $120M divestiture (CAND-001) is **The Witkoff Group LLC real estate management company** (Part 2, entry 1). Reporting confirms Witkoff divested real-estate holdings while **retaining** the WLF crypto. So the divested asset (CAND-001) is the clean one with no sovereign question; the **retained** asset (WLF) is the one carrying the sovereign tie. Last session had this backwards.

## The sovereign connection — verified

The sovereign-adjacent link is **not in the filing**; it lives in the MGX-Binance-USD1 transaction. As of the 2026-05-29 verification pass, the transaction facts are primary-sourced and MGX's sovereign status is confirmed:

- **MGX is Abu Dhabi state-owned.** Confirmed in multiple reports characterizing MGX as Abu Dhabi's state-owned investment firm. This places it inside the sovereign-and-sovereign-adjacent definition without inference — it is not merely a foreign fund.
- **The $2B Binance investment is primary-anchored.** Binance's own announcement (X, 2025-03-12) states the $2B from MGX is the first institutional investment in its history. Settlement using WLF's USD1 stablecoin was announced by Zach Witkoff (Steve Witkoff's son, WLF co-founder) at Token2049 Dubai, ~2025-05-01.
- **WLF's own admission, via primary correspondence.** The Warren-Merkley letter to the MGX and Binance CEOs (Senate Banking, 2025-06-11) reports WLF confirmed MGX and Binance would likely have settled the transaction in a foreign fiat currency had USD1 not been available — i.e., USD1's selection routed value to the WLF-linked parties.

**The connection chain:** Abu Dhabi state-owned MGX → $2B into Binance → settled in WLF's USD1 → WLF accrues on the stablecoin → WLF is held in Steve Witkoff's 278e (41.8.1) and co-founded by his son. That chain clears the bar CAND-001 could not.

### Source grades

| Fact | Source | Grade |
|------|--------|-------|
| $2B MGX→Binance, first institutional investment | Binance announcement 2025-03-12 | primary (party statement) |
| USD1 used to settle | Zach Witkoff, Token2049, ~2025-05-01 | primary (party statement) |
| MGX is Abu Dhabi state-owned | multiple reports | secondary, uncontested |
| WLF would-have-used-foreign-fiat admission | WLF response via Warren-Merkley letter 2025-06-11 | primary correspondence (advocacy framing) |
| WLF held by Witkoff | OGE 278e 41.8.1 | primary (filing) |

## Remaining primary-source target

- **MGX state-ownership primary anchor** — the state-owned characterization is uncontested but currently secondary. For the SovereignEntity catalog entry, pull a primary anchor (MGX/Mubadala-ADIA ownership disclosure, or an Abu Dhabi government source) and run it against the versioned definition. This is catalog hygiene, not a blocker on the relationship facts.
- **OGE certification status** — as of Apr 2026 the 278e was still uncertified 7+ months post-filing; the ethics agreement/waiver requested by Senate offices was not public. Track whether certification names the WLF disposition. Not a blocker.

## Drift guards specific to this case — load-bearing

The record is promotable **only as a documented financial relationship.** It must NOT assert the causal claims:

- **Drift mode 1 (payment occurred → payment caused outcome).** Reporting links the MGX deal to a Nov 2025 US AI-chip decision for the UAE and to the CZ (Changpeng Zhao) pardon. Both are causal and **contested** — Binance's CEO rejected that USD1 got preferential treatment. The record notes these allegations exist and are unproven; it does not adopt them. The honest record stops at: a sovereign-adjacent fund routed $2B through an official's disclosed asset.
- **Drift mode 2 (sovereign source → sovereign government).** MGX is state-owned, which is sovereign-adjacent. The record documents MGX as the actor, not "the UAE government," unless a primary source establishes direct government direction of the transaction.
- The Senate letters are primary *correspondence* but *advocacy* in framing — usable for transaction facts (dates, parties, the WLF admission), not for the causal conclusions the senators draw.

## Disposition: enriched SC-007 (not a new record)

WLF was already recorded as **SC-007** in a prior session (scope LIVE), documenting the MGX→$2B→USD1 chain plus material this note didn't have: the Aryam/Tahnoon ~$500M stake and the Pakistan PVARA MOU. The 2026-05-29 verification pass added value not by minting a record but by **enriching SC-007's `primary_sources`** with three anchors it lacked:

- Binance announcement, 2025-03-12 (party statement)
- Zach Witkoff @ Token2049, ~2025-05-01 (party statement)
- Warren-Merkley Senate Banking letter, 2025-06-11 (primary correspondence)

SC-007 went from 10 to 13 primary sources. No restructure; the Aryam/Tahnoon and PVARA content was untouched; no causal claim was added.

The methodology points still stand and are worth a one-line note on the methodology page (not yet written):
- SC-007 is sourced in part from a **retained** (not divested) holding;
- its sovereign tie is established **entirely off-filing** (the 278e shows the holding at 41.8.1; the connection lives in the transaction record);
- the disclosure form under-captures by design, so the tracker's value is the off-filing verification, not the parse.

**Correction note:** earlier drafts of this doc called WLF "promotion-ready as a new record" and "the first SC record from a retained holding." Both were wrong — SC-007 predates this note. The retained-holding/off-filing observations are still true *about SC-007*; they were never grounds for a new record.

## Supersedes

This note supersedes `cand-001-research-target.md`. CAND-001 is reclassified: divested clean asset, no sovereign question, kill-or-downgrade. See collector-gap finding for the four-candidate kill dispositions.
