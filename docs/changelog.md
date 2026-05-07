# Changelog

## 2026-05-07 (later +1)

`SovereignEntity` schema extended with optional `primary_sources` field, mirroring the `SovereignRecord` pattern. Schema change is structural and reversible; existing entries without primary_sources continue to parse.

Three sovereign-entities entries revised with primary-source verification: ADQ, MGX, PIA. ADQ governance_note now reflects the January 15, 2026 launch of L'imad Holding Company as a successor sovereign vehicle absorbing ADQ; pre-2026 ADQ-attributed transactions in SC-007 remain accurate as documented under ADQ's pre-L'imad governance structure. MGX governance_note refined with verified founding-partner, leadership, and partnership detail; Tahnoon's chairmanship continues post-transition. PIA governance_note corrected on two points: PIA itself was privatized December 23, 2025 with Pakistani government retaining a 25% stake, and the Roosevelt Hotel ownership chain runs through PIA Investment Limited (PIAIL) and Roosevelt Hotel Corporation as PIAIL's subsidiary, not directly through PIA; the Roosevelt and other overseas assets were ring-fenced from the airline privatization for separate joint-venture-model handling.

One new sovereign-entities entry: L'imad Holding Company (LIMAD), with governance_note covering the January 15, 2026 launch and consolidation of ADQ, Modon, and CYVN under the Abu Dhabi crown prince's chairmanship.

Seven seed entries (PIF, MUBADALA, ADIA, QIA, KIA, NBIM, GIC) queued for primary-source verification in a future session; their existing prose-only governance_notes remain in place pending that pass.

Defined terms unchanged.

## 2026-05-07 (later)

SC-008 lands as the second LIVE record and the worked v2.0 covered-intermediary case the methodology page references. The record covers the Pakistan-US Roosevelt Hotel redevelopment MOU signed February 19, 2026 between the Pakistani Finance Ministry and the US General Services Administration, negotiated by Special Envoy Steve Witkoff. The convergent interest sits at the role-and-portfolio level rather than at a documented direct flow: Witkoff (envoy with Pakistan-policy portfolio), Witkoff Group (Manhattan real estate firm with portfolio overlap on the redevelopment sector), and PIA (Pakistani airline, post-December-2025 privatization with government minority stake, owner of the Roosevelt Hotel). No PIA-source flow to Witkoff Group is documented as of this entry; the record's value is in capturing v2.0 portfolio-overlap convergence honestly, with disclosed-gap discipline on the flow status.

SC-007 updated to add a third documented sovereign-adjacent transaction: the January 14, 2026 PVARA/Pakistan Ministry of Finance MOU with SC Financial Technologies (a Delaware-registered WLF affiliate that co-owns the USD1 stablecoin brand), signed by Pakistani Finance Minister Aurangzeb and WLF/SC CEO Zach Witkoff at a ceremony attended by Prime Minister Sharif and Field Marshal Munir. Three new primary_sources entries added to SC-007 covering the PVARA statement, Dawn reporting, and CoinDesk reporting.

One new sovereign_entities registry entry: PIA (Pakistan International Airlines), with governance note covering the December 2025 privatization status and continued government minority stake.

Convergent-interest flag for SC-008 expressed in summary prose. types.ts unchanged; v2.0 schema extension remains queued.

Defined terms unchanged.

## 2026-05-07

First LIVE record landed in the tracker. SC-007 covers World Liberty Financial and the Trump-family beneficial interest in WLF token-sale proceeds and stablecoin profits. The January 16, 2025 Tahnoon-Aryam transaction (a $500M acquisition of 49% of WLF by a Tahnoon-lieutenant vehicle, with $187M flowing to Trump-family entities and $31M to Witkoff-associated entities at signing) is the worked v1.x case carrying the v2.0 convergent-interest flag for Witkoff Group and WLF portfolio overlap. The May 1, 2025 MGX-USD1-Binance transaction is a separate v1.x record reference inside the same SC-007 entry without the flag.

Two new entries added to the sovereign-entities registry: ADQ (Abu Dhabi Developmental Holding Company) and MGX, both Tahnoon-chaired Abu Dhabi state vehicles surfacing in the SC-007 record.

Convergent-interest flag is expressed in the SC-007 summary prose. `web/lib/types.ts` is unchanged in this commit; v2.0 schema extension (a structured `flags` or `covered_intermediary` field) remains queued.

Defined terms unchanged.

## 2026-05-05

Covered-persons rule v2.0 adopted. The Witkoff fact pattern surfaced a structural gap in v1.x: senior administration appointees and designated envoys can hold retained financial interests in connected businesses receiving foreign sovereign or sovereign-adjacent money from governments whose policy portfolios overlap with the appointee's official duties, without any named family member on the cap table. v2.0 adds covered intermediaries bounded by a portfolio-overlap requirement. A record-level convergent-interest flag attaches where the same transaction sends documented value to both the intermediary and a named family member; the WLF Tahnoon-Aryam transaction is the worked v1.x case carrying the flag, and the Pakistan Roosevelt sequence is the worked v2.0 case. The Apollo-channel flows (Brook, and the Belgrove $100 million loan covered by the NYT's October 5, 2025 correction) are excluded by the controlling-interest-chain test under both versions. The Witkoff working reference is at `docs/references/witkoff-methodology-reference.md`; Burisma remains the symmetry-defining exclusion at `docs/references/burisma-methodology-reference.md`. Every v2.0 inclusion is checked against the symmetry test before logging. The change is forward-looking; pre-v2.0 records are not re-examined. Defined terms unchanged.

## 2026-05-04 (later)

Vercel production deploy returned 404 on every route. Build log showed `Build Completed in /vercel/output [56ms]` with no install or Next.js compile, meaning the project's Root Directory was not set and `vercel build` ran against the repo root, where no Next.js project lives. Fixed by moving the seed JSON into `web/data/` and dropping the parent-directory import; the deploy boundary now equals the project boundary, so `outputFileTracingRoot` is no longer needed and was removed from `next.config.ts`. The repo-root `data/` directory remains the long-term home for collector output; a sync step will copy into `web/data/` once collectors come online. Vercel project Root Directory still must be set to `web` for the deploy to find Next.js.

## 2026-05-04

Dashboard scaffold landed under `web/`. Stack matches cbt: Next.js 15 App Router, React 19, TypeScript 5, Tailwind v4 (CSS-first), no database. Routes shipped: `/` records dashboard with scope, framework, and source filters and inline expand; `/swfs` registry with seven SWF governance notes (PIF, Mubadala, ADIA, QIA, KIA, NBIM, GIC); `/record/[id]` detail pages prerendered for the six seed records; `/methodology` placeholder linking to Substack. Seed data populated in `data/records.json` (6 records: Affinity Partners, Trump Organization bookings, Ivanka Trump China trademarks, DC and Maryland v. Trump, Blumenthal v. Trump, Burisma) and `data/sovereign_entities.json` (7 SWFs). Walk-the-definition button shipped on Affinity, Trump Organization, Burisma; copies a prompt and opens claude.ai. Static JSON only for v0; Turso, /api routes, Cron, and watchlist deferred until the first collector ships a real record. Defined terms unchanged.

## 2026-05-03

Repo created. README.md and PROJECT.md drafted, defining scope, the named-family-member list, the financial-interest categories, and the foreign-sovereign-and-sovereign-adjacent-money definition. Defined terms fixed at v1. No data collected yet; collectors are stubs only.

TODO: add CC-BY-4.0 LICENSE at repo root. Deferred from this scaffold pass; to be added manually via the GitHub web UI after the initial push.
