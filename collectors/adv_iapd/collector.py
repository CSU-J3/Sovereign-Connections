"""ADV/IAPD collector — end-to-end seed -> candidates pipeline (Handoff #36).

Brings the ADV/IAPD package to parity with ``collectors/oge_278/``: a single
runnable command that goes from the seed list to candidate rows in
``web/data/candidates.json``. A run, per seeded adviser CRD:

    1. Ingest   — ``collectors.adv_iapd.ingest.fetch_firm(crd)`` assembles the
                  firm's current ADV filing (Item 5 totals + Schedule D 7.B funds)
                  from the live structured surface.
    2. Validate — ``ingest.validate(firm)`` fails loudly if a known-good firm no
                  longer reproduces its recon figures (source drift); the wrapper
                  does not weaken that check, so drifted numbers never flow into
                  candidates.
    3. Emit     — ``candidates.build_rows(firm, covered_person)`` emits one
                  candidate per private fund reporting non-US ownership (ids
                  unset), each stamped with the seed entry's covered person.
    4. Write    — the shared ``collectors.common.candidate_writer`` regenerates
                  only the ``adv_iapd`` slice, preserves the OGE rows and each
                  ADV fund's existing ``CAND-###`` by source-entity key, and writes
                  the merged file.

ADV is *seeded*, not discovered (Verdict A, #34): the covered advisers are named
inputs, not a polled feed, so the seam here is ``seed.json`` rather than a
``discover.py``. The seed loader is the analog of the OGE ``discover_filings()``
stub; the covered-adviser inventory that grows the list is a later handoff.

Network: ``ingest`` fetches from the SEC; set ``ADV_IAPD_UA`` to declare your own
contact (see ``ingest``). The offline regression guard does not hit the network —
it regenerates from a committed firm fixture.

Run: ``.venv/Scripts/python -m collectors.adv_iapd.collector`` (Windows) /
``.venv/bin/python -m collectors.adv_iapd.collector`` (macOS/Linux).
"""

from __future__ import annotations

import collections
import json
from pathlib import Path

from collectors.adv_iapd import candidates, ingest
from collectors.common import candidate_writer

PACKAGE_DIR = Path(__file__).resolve().parent
SEED_FILE = PACKAGE_DIR / "seed.json"


def load_seed() -> list[dict]:
    """The seeded covered advisers to collect (the seed seam, #36; #37 covered_person).

    The ADV analog of ``collectors.oge_278.discover.discover_filings``: callers
    iterate it without caring that it is a committed list today. Each entry is the
    seed object — ``crd`` (str) and ``covered_person`` (the administration-connected
    person the funds tie to, authored in source-faithful Schedule A form), plus an
    optional ``adviser_name`` for readability. Growing the list is a later handoff.
    """
    seed = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    return [{**entry, "crd": str(entry["crd"])} for entry in seed["advisers"]]


def run(advisers: list[dict] | None = None) -> dict:
    """Run ingest -> validate -> emit for every seeded adviser and write the ADV slice.

    Each seed entry carries its CRD and the covered person stamped on every
    candidate from that adviser (#37). Returns a summary dict: the CRDs processed,
    per-firm fund/candidate counts, the total candidate count in the file after the
    merge, the ADV-slice tally, and the output path. Raises ``SystemExit`` (via
    ``ingest``) on a missing firm or source drift; the CLI guard turns that into a
    non-zero exit.
    """
    advisers = advisers or load_seed()

    rows: list[dict] = []
    firms: list[dict] = []
    for entry in advisers:
        firm = ingest.fetch_firm(entry["crd"])
        ingest.validate(firm)  # stop on source drift; do not emit drifted numbers
        firm_rows = candidates.build_rows(firm, entry["covered_person"])
        rows.extend(firm_rows)
        firms.append(
            {
                "crd": firm["crd"],
                "legal_name": firm["legal_name"],
                "filing_date": firm["filing_date"],
                "funds": len(firm["private_funds"]),
                "candidates": len(firm_rows),
            }
        )

    out_path, merged = candidate_writer.write_source_rows(
        candidates.SOURCE, rows, candidates.source_entity_key
    )

    adv = [c for c in merged if c["source_filing"].get("source") == candidates.SOURCE]
    tally = collections.Counter(c["promotion_status"] for c in adv)
    return {
        "crds": [entry["crd"] for entry in advisers],
        "firms": firms,
        "adv_candidates": len(adv),
        "total_in_file": len(merged),
        "tally": dict(tally),
        "output": str(out_path.relative_to(candidate_writer.REPO_ROOT)).replace("\\", "/"),
    }


def _print_summary(summary: dict) -> None:
    for firm in summary["firms"]:
        print(
            f"firm:   {firm['legal_name']} (CRD {firm['crd']}, filed "
            f"{firm['filing_date']}) — {firm['candidates']} candidate(s) from "
            f"{firm['funds']} fund(s)"
        )
    print(f"adv:    {summary['adv_candidates']} ADV candidates; tally {summary['tally']}")
    print(f"total:  {summary['total_in_file']} candidates in file")
    print(f"output: {summary['output']}")


def main() -> None:
    summary = run()
    _print_summary(summary)


if __name__ == "__main__":
    main()
