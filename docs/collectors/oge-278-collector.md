# OGE 278 Collector — End-to-End Pipeline

The collector wires the existing parser and candidate emitter into one runnable
command, so a filing goes from PDF to disposition-carrying candidates in a
single call. It adds **no** parsing or schema logic; it orchestrates the two
modules that already own that logic.

- Module: `collectors/oge_278/collector.py`
- Input (pilot): `data/samples/witkoff-oge278-2025-08-13.pdf`
- Output: `web/data/candidates.json` (the emitter's output, beside
  `web/data/records.json`)
- Run: `.venv/Scripts/python -m collectors.oge_278.collector data/samples/witkoff-oge278-2025-08-13.pdf`
  (Windows) / `.venv/bin/python -m collectors.oge_278.collector …`
  (macOS/Linux). With no argument it defaults to the pilot PDF. Like the parser
  and emitter, it assumes the **repo root** as the working directory.
- History: Handoff #28. The end-to-end wiring was the deferral logged since
  PR #1 ("`oge_278_collector.py` end-to-end wiring — its own handoff").

## Stage order

1. **Parse** — `parser.parse_all(pdf_path)` extracts the filing's Parts 2/5/6 to
   the per-part JSON (`data/samples/…-partN.json`) and returns the parsed docs.
   For the pilot PDF those are the fixed sample filenames the emitter reads; any
   other PDF writes `<stem>-<key>.json` beside the input.
2. **Emit** — `candidates.build()` flattens the holding tree, emits a candidate
   per leaf / value-carrying row, and re-associates the review dispositions
   keyed on `(part, entry_number)`. `candidates.write_candidates()` then writes
   `web/data/candidates.json`.
3. **Summary** — the wrapper prints the filer, total candidate count, the
   lifecycle-state tally (`unreviewed` / `hold_pending_research` /
   `killed_out_of_scope` / `promoted`), any promoted rows
   (`entry_number → SC-###`), and the output path.

Pilot run summary: **168 candidates — 162 unreviewed / 1 hold / 4 killed / 1
promoted**, with entry `41.8.1` (World Liberty Financial, `CAND-130`) promoted
to `SC-007`.

## What the wrapper validates — and what it does not

The **one integrity check** the wrapper preserves is the orphaned-disposition
raise inside `build()`: every recorded disposition must land on a row the
current parse still emits. If a parse drops or renumbers a row such that a
disposition has no matching candidate, `build()` raises and the command exits
non-zero — it does **not** silently emit. This fires through the wrapper exactly
as it does when `candidates.py` is run directly.

The wrapper deliberately does **not** add general candidate-schema validation.
That is a separate concern (a future pass), kept out of the wiring step. The
orphaned-disposition check is the validation that protects the data integrity
that matters here.

`web/data/candidates.json` is deterministic: the parse carries no timestamps and
the `reviewed_at` dates are recorded constants in the disposition registry, so a
second run against the same PDF produces a **byte-identical** file.

## Regression guard

`regression_guard.py` re-generates the candidate output and fails if it drifts
from the committed `web/data/candidates.json`. It catches the case where a
future code change silently changes collector output (Handoff #31).

    python -m collectors.oge_278.regression_guard

It **compares, it never writes**. Rather than re-run the PDF parse (which writes
to committed `data/samples/*.json` paths), the guard calls `candidates.build()`
— which reads the committed parsed samples and *returns a list*, writing nothing
— then serializes that list in memory with the exact same call
`write_candidates()` uses and byte-compares it to the committed file. That
exercises the emit + disposition stage, which is where output actually drifts,
and where the orphan-raise lives: a stale `DISPOSITIONS` key makes `build()`
raise and the guard fails before any comparison. The guard also asserts the
disposition tally hasn't moved (0 unreviewed / 1 hold / 165 killed / 2 promoted
= 168) for a clearer message than a raw diff when a bucket shifts.

The GitHub Actions workflow `.github/workflows/cron-regression.yml` runs the
guard on three triggers: a daily `schedule` (06:00 **UTC**), every
`pull_request` (so drift is caught before merge), and manual `workflow_dispatch`.
A final step asserts `data/samples/` and `web/data/` are clean after the run,
proving nothing was written back.

**Reading a drift failure:** the unified diff shows committed (`---`) vs
regenerated (`+++`). If the change is *unintended*, a code change broke output
stability — fix the code. If it is *intended*, regenerate and commit
`candidates.json` yourself (`python -m collectors.oge_278.collector`); the guard
will never write it for you.

### Discovery is stubbed

The guard runs over whatever `discover.py`'s `discover_filings()` returns — the
seam between *finding* filings and *collecting* them. Today it is a **stub**
returning the one known Witkoff filing, so the guard validates that single
snapshot. Handoff #32 replaces the stub body with a real source (OGE disclosure
polling or a filer watchlist) without changing its signature; once it returns
more than the stub, the scheduled job shifts from pure regression guard to a
backfilling collector.

## Deferred (downstream of this handoff)

- **Cron wiring** — *done (Handoff #31):* see [Regression guard](#regression-guard)
  above. The scheduled job is a drift guard today; it becomes the first real
  cron validation event (a backfilling collect) once filing discovery is real
  (Handoff #32).
- **Multi-filing batch** — one filing per run is the current contract. The
  emitter's `PART_FILES` and the parser's pilot-path handling are keyed to the
  single Witkoff sample; batch handling is a future extension.
- **Turso / `/api` routes** — the collector is a local/manual command for now.
