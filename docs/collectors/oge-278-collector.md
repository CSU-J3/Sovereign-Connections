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

## Deferred (downstream of this handoff)

- **Cron wiring** — running the collector on a schedule (the first cron
  validation event). Comes after the wrapper exists and is trusted; not part of
  this pass.
- **Multi-filing batch** — one filing per run is the current contract. The
  emitter's `PART_FILES` and the parser's pilot-path handling are keyed to the
  single Witkoff sample; batch handling is a future extension.
- **Turso / `/api` routes** — the collector is a local/manual command for now.
