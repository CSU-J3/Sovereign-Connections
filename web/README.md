# Sovereign Connections — web

Next.js 15 dashboard for the Sovereign Connections tracker. Records and sovereign-entity data live at the repo root in `../data/*.json`; this app reads them directly via static imports. The Python collectors (also at the repo root) write that JSON; for v0 the seed data is hand-edited.

## Local development

```bash
npm install
npm run dev
```

Then open http://localhost:3000.

`npm run typecheck` and `npm run build` should both succeed before any deploy.

## Deploying to Vercel

The Vercel project for this app should set **Root Directory = `web`**. Because the app imports JSON from `../data/`, two things need to be true:

1. `outputFileTracingRoot` is set to the repo root in `next.config.ts` (already done). This tells Next.js to include parent files in the trace.
2. In the Vercel project settings, leave **Include source files outside of the Root Directory in the Build Step** enabled (default for monorepos when `outputFileTracingRoot` points outside the root).

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
├── lib/                     types, data loader, constants, format
└── ...
```
