# Changelog

## 2026-05-04 (later)

Vercel production deploy returned 404 on every route. Build log showed `Build Completed in /vercel/output [56ms]` with no install or Next.js compile, meaning the project's Root Directory was not set and `vercel build` ran against the repo root, where no Next.js project lives. Fixed by moving the seed JSON into `web/data/` and dropping the parent-directory import; the deploy boundary now equals the project boundary, so `outputFileTracingRoot` is no longer needed and was removed from `next.config.ts`. The repo-root `data/` directory remains the long-term home for collector output; a sync step will copy into `web/data/` once collectors come online. Vercel project Root Directory still must be set to `web` for the deploy to find Next.js.

## 2026-05-04

Dashboard scaffold landed under `web/`. Stack matches cbt: Next.js 15 App Router, React 19, TypeScript 5, Tailwind v4 (CSS-first), no database. Routes shipped: `/` records dashboard with scope, framework, and source filters and inline expand; `/swfs` registry with seven SWF governance notes (PIF, Mubadala, ADIA, QIA, KIA, NBIM, GIC); `/record/[id]` detail pages prerendered for the six seed records; `/methodology` placeholder linking to Substack. Seed data populated in `data/records.json` (6 records: Affinity Partners, Trump Organization bookings, Ivanka Trump China trademarks, DC and Maryland v. Trump, Blumenthal v. Trump, Burisma) and `data/sovereign_entities.json` (7 SWFs). Walk-the-definition button shipped on Affinity, Trump Organization, Burisma; copies a prompt and opens claude.ai. Static JSON only for v0; Turso, /api routes, Cron, and watchlist deferred until the first collector ships a real record. Defined terms unchanged.

## 2026-05-03

Repo created. README.md and PROJECT.md drafted, defining scope, the named-family-member list, the financial-interest categories, and the foreign-sovereign-and-sovereign-adjacent-money definition. Defined terms fixed at v1. No data collected yet; collectors are stubs only.

TODO: add CC-BY-4.0 LICENSE at repo root. Deferred from this scaffold pass; to be added manually via the GitHub web UI after the initial push.
