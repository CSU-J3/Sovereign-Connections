# Handoff #28 — OGE 278 collector wrapper: end-to-end parse → flatten → emit

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-29-handoff-28-collector-wrapper.md`
**Branch:** new branch off main (post-PR-#3 merge), e.g. `feat/oge-278-wrapper`
**Type:** wiring. Connects the existing parser and candidate-emitter into one runnable pipeline. No new parsing logic, no new schema, no record changes.

## Why

The pieces exist but don't run as a unit. `collectors/oge_278/parser.py` extracts a filing's sections to per-part JSON (`data/samples/witkoff-oge278-2025-08-13-part*.json`). `collectors/oge_278/candidates.py` flattens the holding tree, emits leaf candidates, applies dispositions from the `(part, entry_number)`-keyed registry, and writes `web/data/candidates.json`. Today those are invoked separately. This is the deferral logged since PR #1 ("`oge_278_collector.py` end-to-end wiring — its own handoff"). Wire them into one entry point so a filing goes from PDF to disposition-carrying candidates in a single command.

## Scope — read this before building

**In scope:** parse → flatten → emit, as one command, with the existing disposition re-association preserved.

**Explicitly NOT in scope:**
- Broad schema-validation of the emitted candidates. The `build()` step already raises on orphaned disposition keys, which is the validation that protects the data integrity that matters. General output-schema validation is a separate concern and gets its own pass — do not add it here.
- Turso, `/api` routes, Cron wiring. The wrapper is a local/manual command for now. Cron comes after the wrapper exists and is trusted; it is downstream of this handoff, not part of it.
- Any change to parser extraction logic or the candidate schema.
- Multi-filing batch handling. One filing per run is fine for this pass; note batch as a future extension if the structure makes it trivial, but don't build it.

## Tasks

### 1. Create the wrapper entry point

Create `collectors/oge_278/collector.py` (the name the deferral has referenced since PR #1; if a stub already exists at that path, fill it rather than duplicate). It exposes one callable — a `run(pdf_path, ...)` function and a `__main__` CLI guard — that executes, in order:

1. **Parse:** call the existing `parser.py` entry point on the input PDF, producing the per-part JSON. Reuse what's there; do not reimplement extraction.
2. **Flatten + emit:** call the existing `candidates.py` `build()` so the tree-flatten, leaf emission, disposition re-association, and write to `web/data/candidates.json` all happen as they do today.
3. Return a small run summary object (counts by state, path written, filing identifier) for the CLI to print.

The wrapper orchestrates; the logic stays in the modules it calls. If the current `parser.py` / `candidates.py` entry points aren't cleanly importable (e.g. logic trapped under `if __name__ == "__main__"`), refactor the minimum needed to expose a callable, and note what was moved.

### 2. Preserve disposition re-association exactly

`build()` already re-associates dispositions by `(part, entry_number)` and raises if any registry key doesn't match an emitted row. The wrapper must not weaken this — a parse that drops or renumbers a row such that a disposition orphans should still fail the run loudly, not silently emit. Confirm this still fires when called through the wrapper, not just when `candidates.py` is run directly.

### 3. CLI ergonomics

`python -m collectors.oge_278.collector <pdf_path>` (or the repo's established invocation) runs the full pipeline and prints the run summary: filing identifier, total candidates, the state tally (unreviewed / hold_pending_research / killed_out_of_scope / promoted), and the output path. Exit non-zero on any orphaned-disposition raise or parse failure.

### 4. Document the pipeline

Add a short section to `docs/collectors/oge-278-parser.md` (or a new `docs/collectors/oge-278-collector.md` if cleaner) describing the end-to-end command, the stage order, what the wrapper does and does not validate, and the explicit note that Cron/batch are deferred.

## Verify

- `python -m collectors.oge_278.collector data/samples/witkoff-oge278-2025-08-13.pdf` runs clean end-to-end and reproduces the current `web/data/candidates.json` state: 168 candidates, tally 162 / 4 / 1 / 1, WLF present as CAND-130 with `promoted_to: SC-007`, the four kills and one hold intact.
- Re-running is idempotent: a second run against the same PDF produces byte-identical `candidates.json` (or a documented, justified diff — e.g. a timestamp field, which should be avoided in the committed data).
- The orphaned-disposition raise still fires through the wrapper (test by temporarily perturbing a registry key or a parsed entry number, confirm non-zero exit, then revert).
- `tsc --noEmit` + `next build` green from `web/` (the emitted JSON still validates against the app's types).
- No parser logic or schema changed; the diff is wrapper + minimal import-surface refactor + docs.

## Commit

Single feature commit (plus a separate docs commit if you prefer), opened as a PR. Report: the exact invocation command, the run summary output, and confirmation the tally and SC-007 linkage survived a full pipeline run from PDF.

## Downstream (not this handoff)

Once the wrapper is trusted, the next fronts are: Cron wiring to run it on a schedule (the first cron validation event), and review of the 162 unreviewed candidates the deep-leaf pass surfaced (now runnable against a live pipeline). Order TBD next session.
