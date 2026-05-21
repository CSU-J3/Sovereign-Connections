"""OGE Form 278e parser — Part 6 (Other Assets and Income) pilot.

Coordinate-aware extraction via pdfplumber. Handoff #18.

Part 6 is the section that feeds the most financial-interest records into the
tracker, and it carries the form's worst layout problem: deeply nested entries
whose entity name, valuation range, and income fields each wrap across multiple
physical lines, with entry numbers themselves wrapping inside a narrow column.

This module extracts Part 6 only, as a faithfully nested structure. Other parts
and the mapping to the tracker's canonical record schema are later handoffs.

See docs/collectors/oge-278-parser.md for strategy and known limits.

Run:  .venv/Scripts/python -m collectors.oge_278.parser
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber

# --- Layout constants -------------------------------------------------------
#
# Column x0 boundaries, calibrated against the OGE Form 278e "Updated 08/2024"
# revision (A4 landscape, 842 pt wide). Header anchors observed in the pilot:
#   #@35  DESCRIPTION@78  EIF@383  VALUE@469  INCOME TYPE@556  INCOME AMOUNT@643
# Boundaries are set in the gaps between anchors so a word's x0 maps cleanly.
COL_NUM_MAX = 70      # x0 < 70           -> "#" (entry number)
COL_DESC_MAX = 378    # 70  <= x0 < 378   -> Description / entity name
COL_EIF_MAX = 462     # 378 <= x0 < 462   -> EIF flag (+ "See Endnote" marker)
COL_VALUE_MAX = 550   # 462 <= x0 < 550   -> Value range
COL_ITYPE_MAX = 637   # 550 <= x0 < 637   -> Income type
#                       x0 >= 637         -> Income amount

ROW_Y_TOLERANCE = 5   # pt; words whose `top` differ by <= this share a row

# An entry-number token: dotted integers, optionally left incomplete with a
# trailing dot when the number wrapped onto the next line (e.g. "41.3.1.").
ENTRY_NUM_RE = re.compile(r"^\d+(?:\.\d+)*\.?$")

# Rows that are page furniture, not data.
HEADER_WORDS = {"#", "DESCRIPTION", "EIF", "VALUE", "INCOME", "TYPE", "AMOUNT"}
EIF_VALUES = {"Yes", "No", "N/A"}

PILOT_PDF = Path("data/samples/witkoff-oge278-2025-08-13.pdf")
PILOT_OUT = Path("data/samples/witkoff-oge278-2025-08-13-part6.json")


# --- Data model -------------------------------------------------------------

@dataclass
class Entry:
    """One Part 6 line item, before tree assembly."""

    entry_number: str
    parent_entry_number: str | None = None
    entity_name: str = ""
    eif: str | None = None
    value_range: str | None = None
    income_type: str | None = None
    income_range: str | None = None
    has_endnote: bool = False
    # Part 6 prints no per-entry reporting-period dates (those live in Part 1).
    # The field is kept for schema parity across parts; always None here.
    reporting_period: str | None = None

    # Working accumulators (not serialized).
    _desc: list[str] = field(default_factory=list, repr=False)
    _value: list[str] = field(default_factory=list, repr=False)
    _itype: list[str] = field(default_factory=list, repr=False)
    _iamount: list[str] = field(default_factory=list, repr=False)


# --- Row extraction ---------------------------------------------------------

def _column(x0: float) -> str:
    if x0 < COL_NUM_MAX:
        return "num"
    if x0 < COL_DESC_MAX:
        return "desc"
    if x0 < COL_EIF_MAX:
        return "eif"
    if x0 < COL_VALUE_MAX:
        return "value"
    if x0 < COL_ITYPE_MAX:
        return "itype"
    return "iamount"


def _rows(page) -> list[list[dict]]:
    """Group a page's words into rows by vertical position."""
    words = sorted(page.extract_words(), key=lambda w: (w["top"], w["x0"]))
    rows: list[list[dict]] = []
    anchor: float | None = None
    for w in words:
        if anchor is None or w["top"] - anchor > ROW_Y_TOLERANCE:
            rows.append([])
            anchor = w["top"]
        rows[-1].append(w)
    for r in rows:
        r.sort(key=lambda w: w["x0"])
    return rows


def _columns(row: list[dict]) -> dict[str, list[str]]:
    cols: dict[str, list[str]] = {
        "num": [], "desc": [], "eif": [], "value": [], "itype": [], "iamount": []
    }
    for w in row:
        cols[_column(w["x0"])].append(w["text"])
    return cols


def _is_header(cols: dict[str, list[str]]) -> bool:
    texts = [t for c in cols.values() for t in c]
    if not texts:
        return True
    # Repeated column-header rows ("# DESCRIPTION EIF VALUE INCOME TYPE" / "AMOUNT").
    return all(t in HEADER_WORDS for t in texts)


def _is_footer(cols: dict[str, list[str]]) -> bool:
    texts = [t for c in cols.values() for t in c]
    return "Page" in texts and any(t.startswith("Witkoff") for t in texts)


# --- Part 6 parse -----------------------------------------------------------

def parse_part6(pdf_path: Path) -> list[Entry]:
    """Extract Part 6 entries from an OGE 278e PDF, in document order."""
    entries: list[Entry] = []
    current: Entry | None = None
    in_part6 = False
    expect_number_continuation = False

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for row in _rows(page):
                cols = _columns(row)
                joined = " ".join(t for c in cols.values() for t in c)

                # Section boundaries. The data-side Part 6 title appears once,
                # before any entry; the Part 7 title ends the section.
                if not in_part6:
                    if "Other Assets and Income" in joined:
                        in_part6 = True
                    continue
                if joined.lstrip().startswith("7.") and "Transactions" in joined:
                    return entries

                if _is_header(cols) or _is_footer(cols):
                    continue

                num_tokens = cols["num"]

                # Continuation of a wrapped entry number: the leading "#"-column
                # fragment completes the previous entry's number.
                if expect_number_continuation and current is not None and num_tokens:
                    current.entry_number += num_tokens[0]
                    expect_number_continuation = current.entry_number.endswith(".")
                    _append_continuation(current, cols, skip_num=True)
                    continue

                # A fresh entry-number token in the "#" column starts an entry.
                if num_tokens and ENTRY_NUM_RE.match(num_tokens[0]):
                    current = Entry(entry_number=num_tokens[0])
                    entries.append(current)
                    expect_number_continuation = num_tokens[0].endswith(".")
                    _append_continuation(current, cols, skip_num=True)
                    continue

                # Otherwise: a wrapped description / value / income line.
                if current is not None:
                    _append_continuation(current, cols, skip_num=True)

    return entries


def _append_continuation(entry: Entry, cols: dict[str, list[str]], skip_num: bool) -> None:
    for tok in cols["desc"]:
        if tok in ("See", "Endnote"):
            entry.has_endnote = True
        else:
            entry._desc.append(tok)
    for tok in cols["eif"]:
        if tok in EIF_VALUES:
            entry.eif = tok
        elif tok in ("See", "Endnote"):
            entry.has_endnote = True
    entry._value.extend(cols["value"])
    entry._itype.extend(cols["itype"])
    entry._iamount.extend(cols["iamount"])


def _finalize(entries: list[Entry]) -> list[Entry]:
    """Resolve accumulators into final fields and assign parents."""
    numbers = set()
    for e in entries:
        e.entry_number = e.entry_number.rstrip(".")
        numbers.add(e.entry_number)
    for e in entries:
        e.entity_name = " ".join(e._desc).strip()
        e.value_range = " ".join(e._value).strip() or None
        e.income_type = " ".join(e._itype).strip() or None
        e.income_range = " ".join(e._iamount).strip() or None
        # Parent = the entry number with its last ".N" segment removed. If that
        # exact ancestor is missing, walk up until one exists (defends against
        # any gap in the numbering).
        parent = e.entry_number
        while "." in parent:
            parent = parent.rsplit(".", 1)[0]
            if parent in numbers:
                e.parent_entry_number = parent
                break
    return entries


# --- Tree assembly ----------------------------------------------------------

def build_tree(entries: list[Entry]) -> list[dict]:
    """Assemble flat entries into a nested parent-child structure."""
    nodes: dict[str, dict] = {}
    for e in entries:
        nodes[e.entry_number] = {
            "entry_number": e.entry_number,
            "parent_entry_number": e.parent_entry_number,
            "entity_name": e.entity_name,
            "eif": e.eif,
            "value_range": e.value_range,
            "income_type": e.income_type,
            "income_range": e.income_range,
            "has_endnote": e.has_endnote,
            "reporting_period": e.reporting_period,
            "children": [],
        }
    roots: list[dict] = []
    for e in entries:
        node = nodes[e.entry_number]
        parent = e.parent_entry_number
        if parent and parent in nodes:
            nodes[parent]["children"].append(node)
        else:
            roots.append(node)
    return roots


# --- Entry point ------------------------------------------------------------

def main() -> None:
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else PILOT_PDF
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    entries = _finalize(parse_part6(pdf_path))
    tree = build_tree(entries)

    document = {
        "source_pdf": str(pdf_path).replace("\\", "/"),
        "form": "OGE Form 278e (Updated 08/2024)",
        "filer": "Witkoff, Steven C",
        "report_type": "New Entrant Report",
        "part": "6. Other Assets and Income",
        "parser": "collectors/oge_278/parser.py (Handoff #18 Part 6 pilot)",
        "entry_count": len(entries),
        "entries": tree,
    }

    out = PILOT_OUT if pdf_path == PILOT_PDF else pdf_path.with_name(
        pdf_path.stem + "-part6.json"
    )
    out.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"Parsed {len(entries)} Part 6 entries -> {out}")

    # Correctness check: the WLF interest chain the methodology cites.
    by_num = {e.entry_number: e for e in entries}
    print("\nCorrectness check (WLF interest chain):")
    for num in ("41", "41.8", "41.8.1", "41.9", "41.9.1"):
        e = by_num.get(num)
        if e is None:
            print(f"  MISSING {num}")
            continue
        print(
            f"  {num:<8} {e.entity_name!r}"
            f"  eif={e.eif} value={e.value_range!r}"
            f" income={e.income_type!r}/{e.income_range!r}"
            f" parent={e.parent_entry_number}"
        )


if __name__ == "__main__":
    main()
