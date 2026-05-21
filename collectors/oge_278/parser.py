"""OGE Form 278e parser — Parts 2, 5, and 6.

Coordinate-aware extraction via pdfplumber. Handoffs #18 (Part 6) and #19
(Parts 2 and 5).

Parts 2, 5, and 6 of OGE Form 278e share an identical six-column asset layout
(#, Description, EIF, Value, Income type, Income amount) with the same column
x-anchors, so a single section parser handles all three — only the section
title markers differ. The form's hard problem is the same throughout: entity
names, valuation ranges, income fields, and even entry numbers wrap across
multiple physical lines.

- Part 2 — Filer's Employment Assets & Income and Retirement Accounts. Holds
  the $120M Witkoff Group LLC divestiture (entry #1's income line).
- Part 5 — Spouse's Employment Assets & Income and Retirement Accounts. Where
  18 USC 208(a)(2) imputed spousal interests surface.
- Part 6 — Other Assets and Income. The bulk of the holdings.

Part 1 (a different column set, with From/To date columns) and Parts 3, 4, and
7-12 are not parsed; see docs/collectors/oge-278-parser.md.

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
# revision (A4 landscape, 842 pt wide). Header anchors observed in the pilot,
# identical across Parts 2, 5, and 6:
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
# A part-title row: starts "N. " and carries the part's name.
PART_TITLE_RE = re.compile(r"^\s*\d+\.\s")

# Rows that are page furniture, not data.
HEADER_WORDS = {"#", "DESCRIPTION", "EIF", "VALUE", "INCOME", "TYPE", "AMOUNT"}
EIF_VALUES = {"Yes", "No", "N/A"}

PILOT_PDF = Path("data/samples/witkoff-oge278-2025-08-13.pdf")

# Section configuration. `start`/`end` are substrings of the part-title rows
# that bound each section's data. The data-side titles appear before the
# "Summary of Contents" restatement, so matching the *first* occurrence and
# stopping at the *first* end title isolates the data section.
SECTIONS = {
    "part2": {
        "label": "2. Filer's Employment Assets & Income and Retirement Accounts",
        "start": "Filer's Employment Assets",
        "end": "Employment Agreements and Arrangements",
        "out": "witkoff-oge278-2025-08-13-part2.json",
    },
    "part5": {
        "label": "5. Spouse's Employment Assets & Income and Retirement Accounts",
        "start": "Spouse's Employment Assets",
        "end": "Other Assets and Income",
        "out": "witkoff-oge278-2025-08-13-part5.json",
    },
    "part6": {
        "label": "6. Other Assets and Income",
        "start": "Other Assets and Income",
        "end": "Transactions",
        "out": "witkoff-oge278-2025-08-13-part6.json",
    },
}


# --- Data model -------------------------------------------------------------

@dataclass
class Entry:
    """One asset-section line item, before tree assembly."""

    entry_number: str
    parent_entry_number: str | None = None
    entity_name: str = ""
    eif: str | None = None
    value_range: str | None = None
    income_type: str | None = None
    income_range: str | None = None
    has_endnote: bool = False
    # Parts 2/5/6 print no per-entry reporting-period dates (those live in
    # Part 1). The field is kept for schema parity across parts; always None.
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


def _is_part_title(joined: str, marker: str) -> bool:
    """True if `joined` is a part-title row ("N. ...") carrying `marker`."""
    return marker in joined and PART_TITLE_RE.match(joined) is not None


# --- Section parse ----------------------------------------------------------

def parse_section(pdf_path: Path, start_marker: str, end_marker: str) -> list[Entry]:
    """Extract one six-column asset section's entries, in document order.

    `start_marker` / `end_marker` are substrings of the bounding part-title
    rows. Parsing begins after the start title and stops at the end title.
    """
    entries: list[Entry] = []
    current: Entry | None = None
    in_section = False
    expect_number_continuation = False

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for row in _rows(page):
                cols = _columns(row)
                joined = " ".join(t for c in cols.values() for t in c)

                if not in_section:
                    if _is_part_title(joined, start_marker):
                        in_section = True
                    continue
                if _is_part_title(joined, end_marker):
                    return entries

                if _is_header(cols) or _is_footer(cols):
                    continue

                num_tokens = cols["num"]

                # Continuation of a wrapped entry number: the leading "#"-column
                # fragment completes the previous entry's number.
                if expect_number_continuation and current is not None and num_tokens:
                    current.entry_number += num_tokens[0]
                    expect_number_continuation = current.entry_number.endswith(".")
                    _append_continuation(current, cols)
                    continue

                # A fresh entry-number token in the "#" column starts an entry.
                if num_tokens and ENTRY_NUM_RE.match(num_tokens[0]):
                    current = Entry(entry_number=num_tokens[0])
                    entries.append(current)
                    expect_number_continuation = num_tokens[0].endswith(".")
                    _append_continuation(current, cols)
                    continue

                # Otherwise: a wrapped description / value / income line.
                if current is not None:
                    _append_continuation(current, cols)

    return entries


def _append_continuation(entry: Entry, cols: dict[str, list[str]]) -> None:
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


def parse_part(pdf_path: Path, section_key: str) -> dict:
    """Parse one configured section into a serializable document dict."""
    cfg = SECTIONS[section_key]
    entries = _finalize(parse_section(pdf_path, cfg["start"], cfg["end"]))
    return {
        "source_pdf": str(pdf_path).replace("\\", "/"),
        "form": "OGE Form 278e (Updated 08/2024)",
        "filer": "Witkoff, Steven C",
        "report_type": "New Entrant Report",
        "part": cfg["label"],
        "parser": "collectors/oge_278/parser.py (Handoffs #18, #19)",
        # `parsed` distinguishes "section parsed, no entries" from a section
        # that was never run — see Handoff #19 Step 2.
        "parsed": True,
        "entry_count": len(entries),
        "entries": build_tree(entries),
    }


# --- Entry point ------------------------------------------------------------

def _flatten(nodes: list[dict]):
    for n in nodes:
        yield n
        yield from _flatten(n["children"])


def main() -> None:
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else PILOT_PDF
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    docs: dict[str, dict] = {}
    for key, cfg in SECTIONS.items():
        doc = parse_part(pdf_path, key)
        docs[key] = doc
        if pdf_path == PILOT_PDF:
            out = PILOT_PDF.with_name(cfg["out"])
        else:
            out = pdf_path.with_name(f"{pdf_path.stem}-{key}.json")
        out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        print(f"{key}: {doc['entry_count']:>3} entries -> {out}")

    # Correctness checks.
    p2 = {n["entry_number"]: n for n in _flatten(docs["part2"]["entries"])}
    print("\nPart 2 correctness check ($120M Witkoff Group divestiture):")
    for num in ("1", "1.1", "1.2", "1.2.1", "1.3", "1.3.1"):
        n = p2.get(num)
        print(f"  MISSING {num}" if n is None else
              f"  {num:<6} {n['entity_name']!r}"
              f" eif={n['eif']} value={n['value_range']!r}"
              f" income={n['income_type']!r}/{n['income_range']!r}"
              f" parent={n['parent_entry_number']}")

    print("\nPart 5 correctness check (spouse's employment assets):")
    p5 = docs["part5"]
    print(f"  parsed={p5['parsed']}  entry_count={p5['entry_count']}")
    for n in _flatten(p5["entries"]):
        print(f"  {n['entry_number']:<6} {n['entity_name']!r}"
              f" eif={n['eif']} value={n['value_range']!r}"
              f" income={n['income_type']!r}/{n['income_range']!r}"
              f" parent={n['parent_entry_number']}")


if __name__ == "__main__":
    main()
