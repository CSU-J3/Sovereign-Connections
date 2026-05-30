# Handoff #31 — Cron regression guard: scheduled pipeline re-run with drift detection

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-30-handoff-31-cron-regression-guard.md`
**Branch:** new branch off main, e.g. `feat/cron-regression-guard`
**Type:** CI/automation + a small discovery-interface stub. No parser logic, no schema, no record changes.

## Why

The collector runs one-command end-to-end (`collector.py`, #28) and every Witkoff candidate is dispositioned (#30). What's missing is anything that runs on a schedule. This handoff wires the first scheduled job: a **regression guard** that re-runs the existing pipeline against the committed Witkoff filing and fails loudly if the output drifts from what's in `web/data/candidates.json`. That gives a green/red signal on every schedule tick and on every PR, catching the case where a future code change silently changes collector output.

This is deliberately **not** filing discovery (hunting for new filings to pull). Discovery needs a data source that isn't chosen yet (OGE disclosure polling, or a filer watchlist) and is its own handoff. To keep that follow-up clean, this handoff defines the **discovery interface as a stub** — a typed seam the discovery handoff fills — without implementing it. The regression guard runs against the stub's current fixed return (the known Witkoff filing) today.

## Scope

**In scope:**
- A scheduled GitHub Actions workflow that runs the pipeline and asserts no drift against committed `candidates.json`.
- The same check runnable on PRs (not just the schedule) so drift is caught before merge.
- A stubbed `discover_filings()` interface that currently returns the one known Witkoff filing, with a clear contract for the discovery handoff to implement later.

**Explicitly NOT in scope:**
- Actual filing discovery / polling / watchlist. The stub returns a fixed list; do not implement real discovery.
- Pulling or processing any new filing. The guard runs the existing one.
- Auto-committing regenerated data. The guard *compares*; it does not write back. A drift is a failure to surface to CJ, not an auto-fix.
- Notifications beyond the workflow's own pass/fail status (no email/Slack wiring this pass; note as a future option).

## Tasks

### 1. Make the pipeline output deterministic and comparable

Confirm `collector.py` output is already byte-stable (idempotency was verified in #28/#30 — same input, byte-identical `candidates.json`). The guard depends on this. If any nondeterminism exists (map ordering, timestamps), the guard must normalize it before comparing, or the run must be made deterministic. Document which.

### 2. Stub the discovery interface

Add `discover_filings()` (in `collectors/oge_278/`, location Code's call — likely alongside `collector.py`) with a typed signature and docstring describing the contract:
- Returns a list of filing descriptors (at minimum: source PDF path/URL + filing identifier). 
- **Current stub behavior:** returns exactly the one known Witkoff filing (`data/samples/witkoff-oge278-2025-08-13.pdf`), hard-coded, with a `# STUB:` comment and a pointer to the discovery handoff (#32, TBD).
- The contract should make clear what the discovery handoff will replace: the body, not the signature. Downstream code (the guard, eventually a real scheduled collect) calls `discover_filings()` and iterates; it shouldn't care whether the list came from a stub or a real source.

The regression guard calls `discover_filings()`, runs the pipeline over what it returns, and compares — so the seam is exercised today even though it returns a fixed list.

### 3. The regression-guard workflow

Add `.github/workflows/` entry (e.g. `cron-regression.yml`):
- **Triggers:** `schedule` (a cron expression — daily is fine, e.g. `0 6 * * *`; pick a low-traffic hour and document the timezone is UTC) AND `pull_request` (so drift is caught pre-merge) AND `workflow_dispatch` (manual run).
- **Steps:** check out, set up Python + the project's deps (mirror however the repo installs — `.venv` / requirements), run the pipeline over `discover_filings()` into a *scratch* output (not the committed path), diff the scratch output against the committed `web/data/candidates.json`.
- **Pass:** scratch == committed (no drift). **Fail:** any diff — print the diff in the job log so CJ can see exactly what changed, and exit non-zero.
- The job must not modify committed data. Run into a temp dir / compare / discard.

### 4. Also assert the disposition invariants

Beyond byte-equality, the guard should assert the state tally hasn't drifted: 0 unreviewed / 2 promoted / 1 hold / 165 killed = 168, and that the DISPOSITIONS orphan-raise still fires (a stale registry key fails the run). Byte-equality already implies this, but an explicit tally assertion gives a clearer failure message than a raw diff when something moves. Keep it cheap.

### 5. Document it

Short section in `docs/collectors/oge-278-collector.md` (the #28 doc): what the guard does, its triggers, that it compares-not-writes, that discovery is stubbed and tracked to the discovery handoff, and how to read a drift failure.

## Verify

- Workflow runs green on the current committed state (no drift) — confirm via a manual `workflow_dispatch` run or local equivalent.
- Introduce a deliberate, temporary perturbation (e.g. change one candidate's emitted field in a scratch run) and confirm the guard goes red with a readable diff; then revert. Report that the red path works.
- `discover_filings()` exists, returns the one Witkoff filing, is marked `# STUB:`, and the guard calls it (the seam is exercised, not bypassed).
- The guard writes nothing to `web/data/` — confirm `git status` is clean after a run.
- The PR trigger fires the guard (this PR itself should run it).
- Tally assertion (162→ 0/2/1/165, total 168) present and passing.
- `tsc --noEmit` + `next build` still green (should be untouched).

## Commit / PR

Workflow + stub + docs. Open as a PR (the PR trigger will exercise the guard on itself — a good live test). Report: the workflow's green run, the red-path confirmation (perturb/revert), and confirmation it writes nothing to committed data.

## Downstream (not this handoff)

- **Handoff #32 — filing discovery:** implement `discover_filings()` against a real source (OGE disclosure polling or a filer watchlist — source TBD, that decision is the first half of #32). Once discovery returns more than the stub, the scheduled job shifts from pure regression guard to actual backfilling collector. That's the first real cron *validation* event the roadmap has been pointing at.
- Notifications (email/Slack on red) — optional future add.
- Still owed, unrelated to cron: MGX + USD1 co-ownership primary anchors (catalog hygiene); methodology-page one-line note on retained/off-filing holdings.
