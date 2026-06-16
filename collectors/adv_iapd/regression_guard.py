"""Regression guard for the ADV/IAPD collector (Handoff #36).

The ADV-slice analog of ``collectors/oge_278/regression_guard.py``. It regenerates
the ADV candidate rows and fails loudly if they drift from the committed
``web/data/candidates.json``. This is what the scheduled GitHub Actions workflow
runs alongside the OGE guard on every tick and PR.

How it stays write-safe and offline
------------------------------------
The collector's normal path hits the SEC over the network (``ingest.fetch_firm``),
which a CI guard must not depend on, and writes the committed
``web/data/candidates.json``, which a guard must not modify. So the guard does
**neither**. For each seeded CRD it loads a committed **firm fixture** — the
assembled object ``ingest.fetch_firm`` would return, captured under
``data/samples/adv-iapd-firm-{crd}.json`` — runs ``ingest.validate`` on it (so a
fixture that no longer reproduces the recon figures fails), emits rows with
``candidates.build_rows``, and assigns ids by running the shared writer's *pure*
``merge_rows`` against the committed file. It then slices to the ADV rows and
byte-compares them to the committed ADV slice. Nothing is fetched; nothing is
written.

This deliberately exercises emission (``candidates.build_rows``) and the
source-entity keying the shared writer uses to preserve a fund's ``CAND-###``,
which is where ADV output drifts when code or the fixture changes. The OGE slice
is governed by its own guard; this one compares only the ADV slice so a sibling
collector's rows don't read as ADV drift.

Run it:

    python -m collectors.adv_iapd.regression_guard
"""

from __future__ import annotations

import difflib
import json
import sys
from collections import Counter
from pathlib import Path

from collectors.common import candidate_writer

from . import candidates, ingest
from .collector import load_seed

SAMPLES = candidate_writer.REPO_ROOT / "data" / "samples"

# The disposition tally the committed ADV slice must hold. ADV candidates emit
# `unreviewed` only (no dispositions yet). The seed is Affinity's three non-US
# funds (CRD 315482) plus 1789 Capital's fifteen non-US funds (CRD 335007,
# Handoff #42). Drift here is a regression even if byte-equality somehow passes.
EXPECTED_TALLY: dict[str, int] = {
    "unreviewed": 18,
}


def _fixture_path(crd: str) -> Path:
    """The committed firm fixture for a seeded CRD."""
    return SAMPLES / f"adv-iapd-firm-{crd}.json"


def _regenerate(advisers: list[dict]) -> str:
    """Regenerate the ADV slice exactly as the collector would write it, in memory.

    Loads each seeded CRD's committed firm fixture (offline), validates it, emits
    rows stamped with the seed entry's covered person (#37), then reproduces the
    real write path's id assignment by running the writer's pure ``merge_rows``
    against the committed file — so an ADV fund keeps its ``CAND-###`` by
    source-entity key. Returns the serialized ADV slice. Raises ``SystemExit`` (via
    ``ingest.validate``) on a drifted fixture.
    """
    rows: list[dict] = []
    for entry in advisers:
        crd = entry["crd"]
        fixture = _fixture_path(crd)
        if not fixture.exists():
            raise SystemExit(f"missing committed firm fixture for CRD {crd}: {fixture}")
        firm = json.loads(fixture.read_text(encoding="utf-8"))
        ingest.validate(firm)  # a fixture that drifted from the recon figures fails
        rows.extend(candidates.build_rows(firm, entry["covered_person"]))

    existing = candidate_writer.read_existing(candidate_writer.OUTPUT)
    merged = candidate_writer.merge_rows(
        candidates.SOURCE, rows, candidates.source_entity_key, existing
    )
    adv_rows = [c for c in merged if c["source_filing"].get("source") == candidates.SOURCE]
    return candidate_writer.serialize(adv_rows)


def _check_seed(text: str, crds: set[str]) -> str | None:
    """Confirm every emitted ADV row traces to a seeded CRD. Error string or None."""
    emitted = json.loads(text)
    sources = {c["source_filing"].get("crd") for c in emitted}
    extra = sources - crds
    if extra:
        return (
            f"emitted ADV candidates reference CRD(s) {sorted(extra)!r} not in the "
            f"seed {sorted(crds)!r} — the seed and the committed snapshot diverged"
        )
    return None


def _check_covered_person(text: str, by_crd: dict[str, str]) -> str | None:
    """Confirm every emitted ADV row carries its seed entry's covered person (#37).

    Each ADV candidate's ``covered_person`` must be non-empty and equal the seed's
    covered person for that row's CRD. Byte-equality already implies this on a green
    run; checked explicitly so a covered-person regression reads clearly.
    """
    for c in json.loads(text):
        crd = c["source_filing"].get("crd")
        actual = c.get("covered_person")
        expected = by_crd.get(crd)
        if not actual:
            return f"ADV candidate {c.get('id')} (CRD {crd}) has an empty covered_person"
        if actual != expected:
            return (
                f"ADV candidate {c.get('id')} (CRD {crd}) covered_person "
                f"{actual!r} != seed {expected!r}"
            )
    return None


def _check_tally(text: str) -> str | None:
    """Confirm the ADV disposition tally matches EXPECTED_TALLY. Error string or None."""
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
        return f"ADV disposition tally drifted (expected -> actual):\n{lines}"
    return None


def main(argv: list[str] | None = None) -> int:
    advisers = load_seed()
    crds = [entry["crd"] for entry in advisers]
    covered_by_crd = {entry["crd"]: entry["covered_person"] for entry in advisers}
    print(f"regression guard: regenerating ADV slice for CRD(s) {crds}", file=sys.stderr)

    try:
        produced = _regenerate(advisers)
    except SystemExit as exc:  # missing fixture or ingest.validate drift
        print(f"FAIL: ADV regeneration raised — {exc}")
        return 1

    committed_path = candidate_writer.OUTPUT
    if not committed_path.exists():
        print(f"error: committed file missing: {committed_path}", file=sys.stderr)
        return 1
    committed_all = json.loads(committed_path.read_text(encoding="utf-8"))
    committed_adv = [
        c for c in committed_all if (c.get("source_filing") or {}).get("source") == candidates.SOURCE
    ]
    committed = candidate_writer.serialize(committed_adv)

    # 1. Byte-equality against the committed ADV slice.
    if produced != committed:
        print("FAIL: ADV collector output drifted from committed candidates.json")
        diff = difflib.unified_diff(
            committed.splitlines(keepends=True),
            produced.splitlines(keepends=True),
            fromfile="committed/web/data/candidates.json (adv slice)",
            tofile="regenerated/adv slice",
        )
        sys.stdout.writelines(diff)
        print(
            "\nThe ADV pipeline now emits something different from what is "
            "committed. Inspect the diff above; if the change is intended, "
            "regenerate and commit candidates.json yourself "
            "(python -m collectors.adv_iapd.collector) — the guard never writes "
            "it for you."
        )
        return 1

    # 2. Seed-seam tie and disposition-tally invariant. Byte-equality already
    #    implies these on a green run; checked explicitly so a failure reads
    #    clearly instead of as a raw diff.
    for check in (
        _check_seed(produced, set(crds)),
        _check_covered_person(produced, covered_by_crd),
        _check_tally(produced),
    ):
        if check is not None:
            print(f"FAIL: {check}")
            return 1

    total = sum(EXPECTED_TALLY.values())
    print(
        f"PASS: ADV slice byte-identical to committed candidates.json; "
        f"CRD(s) {crds}; tally {EXPECTED_TALLY} (total {total})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
