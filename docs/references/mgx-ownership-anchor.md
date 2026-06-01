# Catalog anchor — MGX ownership (primary), and SC-007 precision fix

**Date:** 2026-05-30
**Status:** ready for a small handoff — catalog enrichment + SC-007 wording fix
**Owner:** CJ
**Retires:** the long-owed "MGX state-ownership primary anchor" (catalog hygiene from SC-007)

## The find

MGX's ownership is anchorable to a **primary source**: the founding shareholder's own announcement, not journalist characterization. For a privately-held vehicle that files no public ownership disclosure, a founding partner's official statement is as primary as the record gets.

**Primary anchor:** Mubadala's official press release announcing MGX's creation —
`mubadala.com/en/news/abu-dhabi-launches-comprehensive-global-investment-strategy-on-artificial-intelligence`

It states: the Artificial Intelligence and Advanced Technology Council (AIATC), established 2024-01-22 by Sheikh Mohamed bin Zayed Al Nahyan (President of the UAE), announced the creation of MGX, with **Mubadala and G42 as founding partners.**

## Ownership chain — both founding shareholders are Abu Dhabi state / ruling-family entities

- **Mubadala Investment Company** — a sovereign wealth fund **wholly owned by the Government of Abu Dhabi** (Private Joint Stock Company, government-owned; ~$330B AUM). Unambiguous SWF; no inference needed.
- **G42 (Group 42 Holding Ltd)** — Emirati AI holding company **chaired by Sheikh Tahnoun bin Zayed Al Nahyan**, of the UAE ruling family (national security advisor; brother of the president). State-adjacent through ruling-family control.
- **Oversight:** MGX is overseen by Tahnoun bin Zayed — the figure atop the broader Abu Dhabi AI/SWF structure. (Bloomberg, 2025-01.)
- **Persistence:** Mubadala and G42 **remain core shareholders** even as MGX explores raising outside capital toward a larger fund (Reuters/reporting, 2025-08). So the sovereign ownership is structural, not a launch artifact.

## The precision fix — "state-owned" is slightly imprecise

SC-007 currently characterizes MGX as "Abu Dhabi state-owned" (uncontested secondary). The accurate, more defensible wording names the two shareholders and their nature:

> MGX is an Abu Dhabi technology-investment vehicle (founded 2024) whose two founding and core shareholders are **Mubadala** (a sovereign wealth fund wholly owned by the Government of Abu Dhabi) and **G42** (an Emirati AI holding company chaired by Sheikh Tahnoun bin Zayed Al Nahyan of the ruling family). It is overseen by Tahnoun bin Zayed, UAE national security advisor and brother of the president.

This is **sovereign and sovereign-adjacent at the shareholder level** — squarely within the defined "foreign sovereign and sovereign-adjacent money" category — and it's the difference between a flat claim a critic could nitpick ("MGX isn't literally a government ministry") and a precise one they can't. It does not weaken the SC-007 finding; it strengthens it by sourcing the ownership to Mubadala's own statement.

## Drift-guard note

- The settlement chain in SC-007 (MGX → $2B into Binance → USD1) is unchanged. This only firms up *what MGX is*.
- Keep MGX distinct from **Lunate** (the separate Abu Dhabi vehicle surfaced in SC-009, still pending governance verification). Two different Abu Dhabi vehicles; do not conflate. This note covers MGX only.
- No causal claim is added or implied. Naming the shareholders documents the vehicle's nature, nothing more.

## Source grades

| Fact | Source | Grade |
|------|--------|-------|
| MGX founded 2024; Mubadala + G42 founding partners | Mubadala official announcement | **primary (founding shareholder statement)** |
| Mubadala wholly owned by Govt of Abu Dhabi; SWF | Mubadala corporate profile / reporting | primary-adjacent, uncontested |
| G42 chaired by Tahnoun bin Zayed (ruling family) | G42 corporate profile / reporting | secondary, uncontested |
| MGX overseen by Tahnoun bin Zayed | Bloomberg 2025-01 | secondary |
| Mubadala + G42 remain core shareholders | Reuters 2025-08 | secondary |

## Handoff tasks (small)

1. **Catalog:** enrich the existing MGX entry in `web/data/sovereign_entities.json` with the founding-shareholder governance (Mubadala SWF + G42 ruling-family chair; Tahnoun bin Zayed oversight) and the Mubadala announcement as the primary source. Do not change MGX's catalog ID or its links to SC-007.
2. **SC-007 fix:** replace the flat "Abu Dhabi state-owned" characterization with the two-shareholder wording above; add the Mubadala announcement to `primary_sources` (it moves the ownership fact from secondary to primary). No other SC-007 content changes; preserve the USD1 / Pakistan legs and the existing drift guards.
3. **Verify:** MGX still distinct from Lunate and MGX (no conflation); `tsc --noEmit` + `next build` green; regression guard green (this touches catalog/records, not the candidate pipeline).
4. **Commit** as a small PR or docs+data commit per the repo's pattern; report the SC-007 source count (should increment by 1).

## Still owed after this

- **USD1 co-ownership** primary anchor (the July 2025 reserve documentation itself).
- **Lunate** governance verification (state-owned vs state-adjacent; distinct from MGX) before any catalog entry.
- Methodology one-line note on retained/off-filing holdings.
