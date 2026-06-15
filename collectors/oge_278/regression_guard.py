"""Regression guard for the OGE 278 collector.

Regenerates the candidate output for every filing :func:`discover_filings`
returns and fails loudly if it drifts from the committed
``web/data/candidates.json``. This is the check the scheduled GitHub Actions
workflow runs on every tick and on every PR.

How it stays write-safe
-----------------------
The collector's normal path (``collector.run`` -> ``parser.parse_all`` ->
``candidates.write_candidates``) writes to *committed* paths: the per-part
sample JSONs under ``data/samples/`` and ``web/data/candidates.json``. The
guard must not modify committed data, so it does **not** call that path.

Instead it calls ``candidates.build()`` — which reads the committed parsed
sample JSONs and *returns a list*, writing nothing — and serializes that list
**in memory** with the exact same call ``candidates.write_candidates`` uses.
That regenerated text is what would be written to ``candidates.json``, so a
byte-comparison against the committed file is a true drift check while touching
nothing on disk.

This deliberately exercises the emit + disposition stage (``candidates.py``),
which is where collector output actually drifts when code changes — and where
the orphan-raise lives: ``build()`` raises ``SystemExit`` if any recorded
disposition no longer lands on an emitted row, so a stale ``DISPOSITIONS`` key
fails the guard before any comparison. The PDF parse stage is not re-run here
because it writes to committed sample paths (and its idempotency was verified
in #28/#30); re-running it would violate the write-nothing contract for no
extra drift signal, since the drift surfaces in ``candidates.json``.

Run it:

    python -m collectors.oge_278.regression_guard
"""
from __future__ import annotations

import difflib
import json
import sys
from collections import Counter

from collectors.common import candidate_writer

from . import candidates
from .discover import FilingRef, discover_filings

# The disposition state the committed snapshot must hold, keyed on the real
# promotion_status values. Post-#30 the review left nothing unreviewed. Total =
# 168. Drift here is a regression even if byte-equality somehow passes.
EXPECTED_TALLY: dict[str, int] = {
    "unreviewed": 0,
    "hold_pending_research": 1,
    "killed_out_of_scope": 165,
    "promoted": 2,
}


def _regenerate() -> str:
    """Regenerate the OGE slice exactly as the collector would write it, in memory.

    Since Handoff #36 ``candidates.build()`` returns id-less rows and the shared
    writer assigns ids. The guard reproduces the real write path's id assignment
    by running the writer's pure ``merge_rows`` against the committed file — so an
    OGE row keeps its ``CAND-###`` by ``source_entity_key`` — then slices to the
    OGE rows and serializes them the same way the writer does. It writes nothing,
    honoring the write-nothing contract. ``candidates.build()`` raises
    ``SystemExit`` on an orphaned disposition; we let that propagate.
    """
    emitted = candidates.build()
    existing = candidate_writer.read_existing(candidates.OUTPUT)
    merged = candidate_writer.merge_rows(
        candidates.SOURCE, emitted, candidates.source_entity_key, existing
    )
    oge_rows = [c for c in merged if c["source_filing"].get("source") == candidates.SOURCE]
    return candidate_writer.serialize(oge_rows)


def _check_seam(text: str, ref: FilingRef) -> str | None:
    """Confirm the regenerated candidates trace to the discovered filing.

    Ties ``discover_filings()`` into the comparison: every emitted candidate's
    ``source_pdf`` must be the filing discovery handed us. Returns an error
    string on mismatch, else None.
    """
    expected = ref.source.relative_to(candidates.REPO_ROOT).as_posix()
    emitted = json.loads(text)
    sources = {c["source_filing"]["source_pdf"] for c in emitted}
    if sources != {expected}:
        return (
            f"discovered filing {expected!r} does not match emitted "
            f"source_pdf(s) {sorted(sources)!r} — the discovery seam and the "
            f"committed snapshot have diverged"
        )
    return None


def _check_tally(text: str) -> str | None:
    """Confirm the disposition tally matches EXPECTED_TALLY. Error string or None."""
    counts = Counter(c["promotion_status"] for c in json.loads(text))
    drift = {
        status: (EXPECTED_TALLY.get(status, 0), counts.get(status, 0))
        for status in set(EXPECTED_TALLY) | set(counts)
        if EXPECTED_TALLY.get(status, 0) != counts.get(status, 0)
    }
    if drift:
        lines = "\n".join(
            f"  {status}: {exp} -> {act}" for status, (exp, act) in sorted(drift.items())
        )
        return f"disposition tally drifted (expected -> actual):\n{lines}"
    return None


def main(argv: list[str] | None = None) -> int:
    filings = discover_filings()

    if len(filings) != 1:
        # The committed candidates.json is a single-filing snapshot. Until
        # Handoff #32 teaches the guard to aggregate, more than one discovered
        # filing means the contract changed out from under it — fail loudly
        # rather than silently compare the wrong thing.
        print(
            f"error: regression guard expects exactly 1 discovered filing "
            f"(the committed snapshot), got {len(filings)}. Aggregation across "
            f"filings is Handoff #32's job — update the guard there.",
            file=sys.stderr,
        )
        return 2

    [ref] = filings
    print(f"regression guard: regenerating {ref.filing_id}", file=sys.stderr)

    try:
        produced = _regenerate()
    except SystemExit as exc:  # build() orphan-raise (stale DISPOSITIONS key)
        print(
            f"FAIL: collector emit raised — {exc}\n"
            f"(a recorded disposition no longer lands on an emitted row; the "
            f"DISPOSITIONS registry is stale relative to the parse)"
        )
        return 1

    committed_path = candidates.OUTPUT
    if not committed_path.exists():
        print(f"error: committed file missing: {committed_path}", file=sys.stderr)
        return 1
    committed = committed_path.read_text(encoding="utf-8")

    # candidates.json is shared: since Handoff #35 it also holds ADV/IAPD rows,
    # and since #36 every row is source-tagged. This OGE guard governs only the
    # OGE slice; compare against that slice so a sibling collector's rows don't
    # read as OGE drift. The ADV/IAPD pipeline has its own regression guard (#36).
    committed_oge = [
        c for c in json.loads(committed)
        if (c.get("source_filing") or {}).get("source") == candidates.SOURCE
    ]
    committed = candidate_writer.serialize(committed_oge)

    # 1. Byte-equality against the committed snapshot (OGE slice).
    if produced != committed:
        print("FAIL: collector output drifted from committed candidates.json")
        diff = difflib.unified_diff(
            committed.splitlines(keepends=True),
            produced.splitlines(keepends=True),
            fromfile="committed/web/data/candidates.json",
            tofile="regenerated/candidates.json",
        )
        sys.stdout.writelines(diff)
        print(
            "\nThe pipeline now emits something different from what is "
            "committed. Inspect the diff above; if the change is intended, "
            "regenerate and commit candidates.json yourself "
            "(python -m collectors.oge_278.collector) — the guard never "
            "writes it for you."
        )
        return 1

    # 2. Discovery-seam tie and disposition-tally invariant. Byte-equality
    #    already implies these on a green run; checked explicitly so a failure
    #    reads clearly instead of as a raw diff.
    for check in (_check_seam(produced, ref), _check_tally(produced)):
        if check is not None:
            print(f"FAIL: {check}")
            return 1

    total = sum(EXPECTED_TALLY.values())
    print(
        f"PASS: output byte-identical to committed candidates.json; "
        f"filing {ref.filing_id}; tally {EXPECTED_TALLY} (total {total})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
