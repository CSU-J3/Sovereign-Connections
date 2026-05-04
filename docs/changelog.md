# Changelog

## 2026-05-04

Dashboard scaffold landed under `web/`. Stack matches cbt: Next.js 15 App Router, React 19, TypeScript 5, Tailwind v4 (CSS-first), no database. Routes shipped: `/` records dashboard with scope, framework, and source filters and inline expand; `/swfs` registry with seven SWF governance notes (PIF, Mubadala, ADIA, QIA, KIA, NBIM, GIC); `/record/[id]` detail pages prerendered for the six seed records; `/methodology` placeholder linking to Substack. Seed data populated in `data/records.json` (6 records: Affinity Partners, Trump Organization bookings, Ivanka Trump China trademarks, DC and Maryland v. Trump, Blumenthal v. Trump, Burisma) and `data/sovereign_entities.json` (7 SWFs). Walk-the-definition button shipped on Affinity, Trump Organization, Burisma; copies a prompt and opens claude.ai. Static JSON only for v0; Turso, /api routes, Cron, and watchlist deferred until the first collector ships a real record. Defined terms unchanged.

## 2026-05-03

Repo created. README.md and PROJECT.md drafted, defining scope, the named-family-member list, the financial-interest categories, and the foreign-sovereign-and-sovereign-adjacent-money definition. Defined terms fixed at v1. No data collected yet; collectors are stubs only.

TODO: add CC-BY-4.0 LICENSE at repo root. Deferred from this scaffold pass; to be added manually via the GitHub web UI after the initial push.
