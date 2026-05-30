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
    """Build the candidate list and serialize it exactly as the collector does.

    Mirrors ``candidates.write_candidates`` byte-for-byte (2-space indent,
    ``ensure_ascii=False``, trailing newline) but returns the text instead of
    writing it. ``candidates.build()`` raises ``SystemExit`` on an orphaned
    disposition; we let that propagate — a stale registry is a guard failure.
    """
    emitted = candidates.build()
    text = json.dumps(emitted, indent=2, ensure_ascii=False) + "\n"
    return text


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

    # 1. Byte-equality against the committed snapshot.
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
