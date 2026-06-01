# Catalog anchor — Lunate governance (sovereign-adjacent, NOT state-owned)

**Date:** 2026-05-30
**Status:** ready for a small handoff — add Lunate to `sovereign_entities.json` as sovereign-adjacent
**Owner:** CJ
**Retires:** the owed "Lunate governance verification" (from SC-009 / W-002 Affinity)
**Source type:** ownership/governance research (reputable secondary + Chimera's own site)

## The verification question, answered

The open question from SC-009 was whether Lunate is **state-owned** or **state-adjacent**, kept distinct from MGX. Answer: **sovereign-adjacent, not state-owned.**

## Ownership chain

- **Lunate is majority-owned by Chimera Investment LLC**, with the rest held by Lunate's three managing partners (Khalifa Al Suwaidi, Murtaza Hussain, Seif Fikry). It is a **privately-owned** alternative asset manager (~$115B AUM, 2026), not a government-owned fund. (Reuters, AGBI; Chimera's own site confirms Lunate Holding RSC LTD as a Chimera subsidiary.)
- **Chimera is part of Sheikh Tahnoun bin Zayed Al Nahyan's private investment empire** — specifically his private firm **Royal Group**, which majority-owns International Holding Company (IHC). Tahnoun is the UAE national security adviser and brother of the president. So Lunate's control runs to the **ruling family through a private vehicle (Royal Group → Chimera)**, not through the Abu Dhabi government's balance sheet.
- **The sovereign tie is at the LP level, not the ownership level.** ADQ (a sovereign wealth fund) and Chimera served as **anchor limited partners** from launch. ADQ invests in Lunate; it does not own Lunate.

## Classification: sovereign-adjacent

Lunate qualifies under the "foreign sovereign and sovereign-adjacent money" category via **two routes** — ruling-family control (Tahnoon/Royal Group/Chimera) and sovereign-LP anchoring (ADQ). It is **NOT state-owned** the way Mubadala (wholly owned by the Government of Abu Dhabi) or ADQ (a sovereign wealth fund) are.

Calling Lunate "state-owned" or "an Abu Dhabi sovereign fund" would overstate the state's ownership and is the SWF-vs-government conflation in miniature. The accurate catalog wording:

> Lunate — a privately-owned Abu Dhabi alternative asset manager (majority owner Chimera Investment LLC + management), controlled through Sheikh Tahnoun bin Zayed's private Royal Group empire, with sovereign capital (ADQ) as an anchor limited partner. Sovereign-**adjacent** (ruling-family-controlled + sovereign-LP-anchored), not state-owned.

## Distinct from MGX — required, and now sharper

Both Lunate and MGX run to **Tahnoon bin Zayed**, which is the conflation trap. They are **structurally different** and the catalog must show both the common thread and the difference:

| | Ownership | State element |
|---|-----------|---------------|
| **MGX** | Mubadala (state SWF) + G42 (ruling-family-chaired) | Has a **state-owned shareholder** (Mubadala) |
| **Lunate** | Chimera (private, Royal Group) + management | State tie only at **LP level** (ADQ anchor); no state-owned shareholder |

Same overseer (Tahnoon), different ownership structure. MGX has sovereign ownership; Lunate has sovereign anchoring. Do not collapse them into "Tahnoon's money" — catalog each on its own structure. (Also distinct from Royal Group, ADQ, IHC themselves, which are separate entities in the chain.)

## Source grades

| Fact | Source | Grade |
|------|--------|-------|
| Lunate majority-owned by Chimera + management | Reuters, AGBI launch coverage | secondary, uncontested |
| Lunate Holding is a Chimera subsidiary | chimerainvestment.com (Chimera's own site) | **primary-adjacent (owner's site)** |
| Chimera part of Tahnoon's Royal Group; Royal Group majority-owns IHC | Reuters, Bloomberg/InvestmentNews | secondary, uncontested |
| ADQ + Chimera anchor LPs | Medium/Global Times profile; launch coverage | secondary |
| ~$115B AUM (2026) | AGBI | secondary |

The Chimera-site confirmation of the Lunate Holding structure is the closest primary anchor; sufficient for a governance line. (A registry-grade anchor — ADGM filing for Lunate Holding RSC LTD — is an optional future pull, not required.)

## Drift-guard note

- The sovereign-adjacency is real but **specific**: ruling-family control + sovereign LP. Do not upgrade to "state-owned."
- ADQ being an LP does **not** make ADQ an owner, and does not make Lunate a sovereign fund. Keep the LP relationship and the ownership structure distinct.
- No causal claim. Classifying Lunate documents what it is; it asserts nothing about any official act tied to the Affinity (SC-009) investment.

## Handoff task (small)

1. Add **Lunate** to `web/data/sovereign_entities.json`, classified **sovereign-adjacent**, with a `governance_note` carrying: majority owner Chimera Investment LLC + management; controlled via Tahnoon bin Zayed's private Royal Group; ADQ sovereign-LP anchor; explicitly **not state-owned**; kept distinct from MGX (and from ADQ/Royal Group/IHC).
2. Link to SC-009 (the Affinity record, where Lunate is one of the three sovereign/sovereign-adjacent LPs).
3. Verify: distinct catalog entry from MGX; classification reads sovereign-adjacent not state-owned; `tsc --noEmit` + `next build` green; regression guard green.
4. Commit (small PR or docs+data); report the catalog count.

## After this — the three anchors are all retired

- ✅ MGX ownership (primary: Mubadala announcement) — applied PR #9.
- ✅ USD1 co-ownership (primary: BitGo attestations, stored in repo) — applied PR #9.
- ✅ Lunate governance (this note) — sovereign-adjacent, ready to add.

Remaining owed (non-anchor): methodology one-line note on retained/off-filing holdings; optional USPTO trademark pull; Node-24 action bump before 2026-06-16; filing-discovery handoff when a source type earns automation.
