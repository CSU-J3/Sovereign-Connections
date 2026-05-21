# Collectors

Python collectors for the Sovereign Connections Tracker (Phase 5). Each collector
pulls a class of public primary record — SEC filings, FARA registrations, OGE 278
financial disclosures, PACER dockets, CFIUS notices, foreign corporate registries —
and (eventually) emits structured records for the tracker.

Most files here are still `NotImplementedError` stubs. The first collector under
active construction is **OGE 278** (`oge_278/`), per Handoff #17 (discovery) and
Handoff #18 (Part 6 parser pilot).

## Environment

Collectors use a **repo-local virtual environment** at `./.venv` with plain `pip`
(no poetry / uv / pip-tools — the dependency surface is small enough that a single
pinned `requirements.txt` is sufficient). The `.venv/` directory is git-ignored.

Setup:

```sh
python -m venv .venv
# Windows
.venv/Scripts/pip install -r collectors/requirements.txt
# macOS / Linux
.venv/bin/pip install -r collectors/requirements.txt
```

Run a module with the venv interpreter, e.g.:

```sh
.venv/Scripts/python -m collectors.oge_278.parser   # Windows
.venv/bin/python -m collectors.oge_278.parser       # macOS / Linux
```

## Layout

- `*_collector.py` — flat stub modules, one per source (entry points, TBD).
- `oge_278/` — the OGE 278 collector package: `parser.py` extracts structured
  data from OGE Form 278e PDFs. See `docs/collectors/oge-278-discovery.md` and
  `docs/collectors/oge-278-parser.md`.
