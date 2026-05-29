"""OGE 278 collector — end-to-end PDF -> candidates pipeline (Handoff #28).

Wires the existing parser and candidate emitter into one runnable command. A
filing goes from PDF to disposition-carrying candidates in a single call:

    1. Parse   — collectors.oge_278.parser.parse_all() extracts Parts 2/5/6 to
                 the per-part JSON the emitter reads.
    2. Emit    — collectors.oge_278.candidates.build() flattens the holding
                 tree, emits a candidate per leaf/value-carrying row, and
                 re-associates dispositions keyed on (part, entry_number). It
                 raises (non-zero exit) if any recorded disposition orphans —
                 the wrapper does not weaken that check. write_candidates()
                 then writes web/data/candidates.json.
    3. Summary — counts by lifecycle state, the filer, and the output path,
                 returned for the CLI to print.

The wrapper orchestrates; all parsing and emission logic stays in the modules
it calls. It does NOT add general candidate-schema validation: build() raising
on an orphaned disposition is the integrity check that protects the data, and
broad output-schema validation is a separate pass (Handoff #28 scope). Cron
scheduling and multi-filing batch are deferred downstream — see
docs/collectors/oge-278-collector.md.

Like parser.py / candidates.py, this assumes it is run from the repo root (the
parser writes per-part JSON to paths relative to cwd; the emitter reads them
relative to the repo root).

Run: .venv/Scripts/python -m collectors.oge_278.collector \
         data/samples/witkoff-oge278-2025-08-13.pdf
"""

from __future__ import annotations

import collections
import sys
from pathlib import Path

from collectors.oge_278 import candidates, parser


def run(pdf_path) -> dict:
    """Run parse -> emit for one filing and return a run summary.

    Raises ``SystemExit`` on a missing/failed PDF parse (via the parser) or an
    orphaned disposition (via ``candidates.build()``); the CLI guard turns that
    into a non-zero exit. Returns a summary dict: filer, source PDF, total
    candidate count, the lifecycle-state tally, the promoted rows
    (entry_number -> SC-###), and the output path.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    # Stage 1 — parse the filing's sections to per-part JSON. parse_all writes
    # the files candidates.build() reads.
    docs = parser.parse_all(pdf_path)

    # Stage 2 — flatten the tree, emit candidates, re-associate dispositions.
    # build() raises if any disposition key no longer matches an emitted row;
    # that loud failure is preserved, never swallowed.
    emitted = candidates.build()
    out_path = candidates.write_candidates(emitted)

    tally = collections.Counter(c["promotion_status"] for c in emitted)
    promoted = {
        c["source_filing"]["entry_number"]: c["promoted_to"]
        for c in emitted
        if c["promotion_status"] == "promoted"
    }
    return {
        "filer": docs["part2"]["filer"],
        "source_pdf": str(pdf_path).replace("\\", "/"),
        "total": len(emitted),
        "tally": {state: tally.get(state, 0) for state in candidates.STATES},
        "promoted": promoted,
        "output": str(out_path.relative_to(candidates.REPO_ROOT)).replace("\\", "/"),
    }


def _print_summary(summary: dict) -> None:
    print(f"\nfiler:  {summary['filer']}")
    print(f"source: {summary['source_pdf']}")
    print(f"total:  {summary['total']} candidates")
    print("tally:")
    for state, count in summary["tally"].items():
        print(f"  {state:<22} {count}")
    if summary["promoted"]:
        for entry_number, sc in summary["promoted"].items():
            print(f"promoted: entry {entry_number} -> {sc}")
    print(f"output: {summary['output']}")


def main() -> None:
    pdf_arg = sys.argv[1] if len(sys.argv) > 1 else str(parser.PILOT_PDF)
    summary = run(pdf_arg)
    _print_summary(summary)


if __name__ == "__main__":
    main()
