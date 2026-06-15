"""Source-scoped, merge-aware writer for ``web/data/candidates.json`` (Handoff #36).

``web/data/candidates.json`` is shared: the OGE 278 collector emits rows
``CAND-001..168`` and the ADV/IAPD collector emits ``CAND-169..171``, and the
covered-adviser inventory will grow the ADV slice. Before #36 each collector had
its own writer — OGE overwrote the whole file (so a standalone OGE run dropped the
ADV rows) while ADV hand-rolled an append. This module replaces both with one
writer, parameterized by the calling collector's ``source``, so each collector
regenerates **only its own source's rows** and leaves every sibling row untouched.

Contract (Handoff #36 Step 1)
-----------------------------
:func:`write_source_rows` reads the current file, then for the caller's ``source``:

  - drops only the rows whose ``source_filing.source`` equals ``source`` (the
    caller's prior output) and keeps every other row verbatim (the siblings);
  - re-assigns ids to the freshly emitted rows via :func:`merge_rows`: a fresh row
    whose **entity key** matches one of the dropped rows keeps that row's existing
    ``CAND-###``; a genuinely new row gets the next free **global** id (max id over
    every row + 1, so ids never collide across sources and never go backwards);
  - writes back the siblings plus the re-keyed own-rows in stable **global id
    order**, using the same serialization the collectors used before
    (2-space indent, ``ensure_ascii=False``, trailing newline) so an unchanged
    run is byte-identical.

The **entity key** is supplied by the caller as ``key_fn`` because "same source
entity" differs per collector (OGE: the parsed filing + dotted entry number; ADV:
the firm CRD + Schedule D 7.B fund id). The key must be deterministic and stable
across runs — a wrong key either renumbers existing candidates or duplicates them
(Handoff #36 Step 1). It is keyed on the *entity*, not the filing instance, so a
re-filing of the same fund/entry keeps its ``CAND-###``.

:func:`merge_rows` is the pure core (no IO) so a regression guard can compute the
exact bytes that *would* be written without touching disk, mirroring the OGE
guard's write-nothing contract.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable, Hashable

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = REPO_ROOT / "web" / "data" / "candidates.json"


def _row_source(candidate: dict) -> str | None:
    """The ``source_filing.source`` of a candidate, or None for a sourceless row."""
    return (candidate.get("source_filing") or {}).get("source")


def _id_num(candidate: dict) -> int | None:
    """The integer in a ``CAND-###`` id, or None if the row has no id yet."""
    match = re.search(r"\d+", candidate.get("id") or "")
    return int(match.group()) if match else None


def merge_rows(
    source: str,
    fresh_rows: list[dict],
    key_fn: Callable[[dict], Hashable],
    existing: list[dict],
) -> list[dict]:
    """Merge freshly emitted ``source`` rows into ``existing``; pure, writes nothing.

    ``fresh_rows`` are the caller's just-emitted candidates with ``id`` unset
    (None). ``existing`` is the full current candidate list. Returns the new full
    list — every sibling row (a different source) untouched, plus ``fresh_rows``
    with ids assigned: an existing ``CAND-###`` reused when the row's ``key_fn``
    matches a prior same-source row, otherwise the next free global id. The result
    is sorted by numeric id, which is the stable global order the file is kept in.

    ``fresh_rows`` are mutated in place (their ``id`` is filled) and also returned
    inside the merged list.
    """
    siblings = [c for c in existing if _row_source(c) != source]

    # The prior ids of this source's rows, keyed on entity identity. setdefault
    # keeps the first (lowest-id) row if a key somehow repeats, so reuse is
    # deterministic rather than order-of-iteration dependent.
    prior_ids: dict[Hashable, str] = {}
    for c in existing:
        if _row_source(c) == source and c.get("id"):
            prior_ids.setdefault(key_fn(c), c["id"])

    # Next free global id is one past the max over EVERY existing row (siblings
    # included), so a new row never reuses a sibling's id and ids only grow.
    used = [n for n in (_id_num(c) for c in existing) if n is not None]
    next_num = (max(used) + 1) if used else 1

    for row in fresh_rows:
        reused = prior_ids.get(key_fn(row))
        if reused is not None:
            row["id"] = reused
        else:
            row["id"] = f"CAND-{next_num:03d}"
            next_num += 1

    merged = siblings + list(fresh_rows)
    merged.sort(key=lambda c: _id_num(c) or 0)
    return merged


def serialize(candidates: list[dict]) -> str:
    """Serialize the candidate list exactly as the collectors have since #28."""
    return json.dumps(candidates, indent=2, ensure_ascii=False) + "\n"


def read_existing(output_path: Path = OUTPUT) -> list[dict]:
    """The current candidate list, or an empty list if the file does not exist."""
    if not output_path.exists():
        return []
    return json.loads(output_path.read_text(encoding="utf-8"))


def write_source_rows(
    source: str,
    fresh_rows: list[dict],
    key_fn: Callable[[dict], Hashable],
    output_path: Path = OUTPUT,
) -> tuple[Path, list[dict]]:
    """Read, merge the caller's ``source`` rows, and write back. Returns (path, merged).

    The merge-aware replacement for each collector's old whole-file writer: the
    caller passes its just-emitted rows (ids unset) and its entity ``key_fn``;
    this preserves every sibling collector's rows and the caller's own stable ids.
    """
    merged = merge_rows(source, fresh_rows, key_fn, read_existing(output_path))
    output_path.write_text(serialize(merged), encoding="utf-8")
    return output_path, merged
