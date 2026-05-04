# Sovereign Connections — web

Next.js 15 dashboard for the Sovereign Connections tracker. The dashboard reads its data from `web/data/*.json` (this directory). The repo-root `data/` directory remains the long-term home for collector output: when Python collectors come online, they write to `../data/`, and a sync script copies updated JSON into `web/data/` before each build. For v0 the two locations hold the same hand-edited seed.

## Local development

```bash
npm install
npm run dev
```

Then open http://localhost:3000.

`npm run typecheck` and `npm run build` should both succeed before any deploy.

## Deploying to Vercel

The Vercel project for this app **must** set **Root Directory = `web`** (Settings → General → Root Directory). Without this, Vercel runs `vercel build` against the repo root, finds no Next.js project, and ships an empty `/vercel/output` — every route then returns a Vercel-level 404.

There is no `vercel.json` and no `outputFileTracingRoot` workaround. The deploy boundary equals the project boundary: Vercel builds everything inside `web/` and nothing outside it.

Stack: Next.js 15 App Router, React 19, TypeScript 5, Tailwind v4 (CSS-first config). No database for v0; static JSON only. No `/api` routes, no Vercel Cron, no watchlist.

## Routes

- `/` — records dashboard with scope, framework, source filters and inline expand
- `/swfs` — sovereign wealth fund registry with per-fund governance notes
- `/record/[id]` — individual record detail
- `/methodology` — placeholder; canonical version lives on Substack

## File layout

```
web/
├── app/
│   ├── globals.css          Tailwind v4 import + theme tokens
│   ├── layout.tsx
│   ├── page.tsx             dashboard
│   ├── swfs/page.tsx
│   ├── record/[id]/page.tsx
│   └── methodology/page.tsx
├── components/              PascalCase, mirrors cbt convention
├── data/                    seed JSON read by the dashboard at build time
├── lib/                     types, data loader, constants, format
└── ...
```
