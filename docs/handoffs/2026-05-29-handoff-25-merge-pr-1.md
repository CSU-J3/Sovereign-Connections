# Handoff #25 — Merge PR #1 (candidate schema) into main

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-29-handoff-25-merge-pr-1.md`
**Branch:** `feat/oge-278-candidate-schema` → `main`
**Type:** merge only. No code changes, no schema changes, no new work. Confirm green, merge, push.

## Why

PR #1 carries the candidate schema, the 5 Witkoff candidates in `web/data/candidates.json`, the path/README/renumber cleanup (#24), and the two cross-ref fixes. Everything downstream — the candidate→record promotion path, the collector wrapper wiring — branches off merged main. Merging this in isolation gives a known-good main before any new work touches it, so a problem in later work reverts one PR instead of untangling a merge plus half-built logic.

The three deferrals logged on the PR are not blockers and stay deferred:
- Certification cover-page extraction — waits on a promotion decision that needs it
- `oge_278_collector.py` end-to-end wiring — its own handoff
- Global renumber confirmed at #23 (OGE-278 candidate schema) / #24 (path-align cleanup)

## Tasks

### 1. Confirm the branch is mergeable and green

- `git checkout feat/oge-278-candidate-schema`, `git pull` if needed.
- Confirm it's still N commits ahead of main with no conflicts against current main (`git fetch origin main`, `git log --oneline origin/main..HEAD`, `git merge-base --is-ancestor origin/main HEAD` or a dry-run merge check). If main has moved since the PR opened and there's a conflict, **stop and report** rather than force-resolving.
- Run the build from `web/`: `tsc --noEmit` and `next build`. Both must pass. If either fails, **stop and report** — do not merge a red branch.

### 2. Merge to main

- Merge `feat/oge-278-candidate-schema` into `main`. Prefer a merge commit (`--no-ff`) so the PR arc stays legible in history rather than flattening it. Message in the existing convention, referencing the candidate-schema arc.
- Push `main`.

### 3. Confirm post-merge state

- Re-run the build on merged main from `web/`: `tsc --noEmit` + `next build`, both green.
- Confirm `web/data/candidates.json` is present on main with the 5 Witkoff candidates intact (byte count / candidate count check).
- Confirm `git log --follow` history is continuous for the moved files (`candidates.json`, the renamed handoff doc) — the #24 `git mv`s should carry through the merge.

## Verify

- `main` contains the full PR #1 arc: candidate schema, 5 candidates at `web/data/candidates.json`, README architecture block matching disk, no handoff-number collisions in `docs/handoffs/`.
- Build green on main, post-merge.
- The three deferrals remain logged (note them in the merge commit body or a follow-up issue so they survive the PR closing).
- Branch can be deleted or left; report which.

## Report back

- Confirm merge SHA and that main is green.
- Confirm the 5 candidates survived the merge intact.
- Restate the three live deferrals so the next handoff (candidate→record promotion path) starts from a clean ledger.

Do not start promotion-path work in this session. Merge, verify, report — that's the whole job.
