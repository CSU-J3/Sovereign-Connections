"""OGE 278 candidate emitter (Handoff #20 — OGE 278 candidate record schema).

Reads the parsed OGE Form 278e part files produced by
``collectors/oge_278/parser.py`` and emits pre-promotion candidate records into
``data/candidates.json``.

A *candidate* is a parsed financial-disclosure row that **might** describe a
sovereign-source connection, before any human research has confirmed scope.
Candidates sit between raw parser output and promoted ``SC-###`` records in
``web/data/records.json``. Promotion (``CAND-###`` -> ``SC-###``) is a separate
human step; this module does not filter to actual scope and does not research.

Design decisions (Handoff #20):
  1. Sequential IDs ``CAND-001``, ``CAND-002`` ... in parse order; no semantics.
  2. Conservative over-emission: any row that *could* describe a foreign-source
     payment, position, or asset is eligible. Scope filtering happens at
     promotion, not here.
  3. ``business_id`` is a nullable slot for a future
     ``data/connected_businesses.json`` registry; it stays ``null`` here.

Every verbatim field (``filer``, ``business_name``, ``raw_value``) is COPIED from
the parsed row, never retyped, so it cannot drift from the parse. The only
hand-authored field is ``scope_hypothesis`` — and it must stay a hedged research
prompt, never a finding.

Run: ``.venv/Scripts/python -m collectors.oge_278.candidates`` (Windows) /
``.venv/bin/python -m collectors.oge_278.candidates`` (macOS/Linux).
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SAMPLES = REPO_ROOT / "data" / "samples"
OUTPUT = REPO_ROOT / "data" / "candidates.json"

# The parsed OGE 278e part files, in parse order (Parts 2, 5, 6). disclosure_type
# is drawn from the part — NOT inferred from the row. The handoff's example set
# (position/asset/income/agreement/gift) does not map: the parser covers only the
# three asset-&-income sections, so the taxonomy is keyed to the parsed parts.
PART_FILES = {
    "2": ("witkoff-oge278-2025-08-13-part2.json", "filer_employment_asset"),
    "5": ("witkoff-oge278-2025-08-13-part5.json", "spouse_employment_asset"),
    "6": ("witkoff-oge278-2025-08-13-part6.json", "other_asset_income"),
}

# Curated selection for the Witkoff worked pass. Each tuple is
# (part_key, entry_number, scope_hypothesis). entry_number addresses a specific
# parsed row (top-level or dotted child); the row's verbatim fields are lifted by
# the emitter. Selection over-emits per decision 2: these are rows that *could*
# touch a foreign source, not confirmed ones. Order here is parse order and sets
# the CAND-### sequence.
SELECTION = [
    (
        "2",
        "1",
        "Filer reports $120,000,000 in proceeds from the sale of an interest "
        "in The Witkoff Group as part of divestiture planning. OGE Form 278e "
        "Part 2 prints the amount but no acquirer/counterparty (those would "
        "live in a separate OGE ethics agreement). Research whether the "
        "divested interest was acquired by a sovereign-linked entity — "
        "unverified; no buyer is named in the parsed filing.",
    ),
    (
        "6",
        "1",
        "Holding entity carries a 'Ltd' suffix (a non-US corporate form) and "
        "its only sub-asset is motorized water vehicles (a yacht-holding "
        "pattern). Research the entity's domicile and whether any "
        "foreign/sovereign counterparty is involved in its financing or "
        "ownership — unverified; the parsed row shows only a US-range value.",
    ),
    (
        "6",
        "2",
        "Same 'Ltd' yacht-holding pattern as M&A Management Company Ltd, at a "
        "$1M-$5M value range. Research domicile and whether any "
        "foreign/sovereign counterparty is involved — unverified; nothing in "
        "the parsed row asserts a foreign source.",
    ),
    (
        "6",
        "7",
        "Private-equity fund interest whose parsed sub-entries include "
        "foreign-located assets — 'Mixed use real estate, Marseille, France' "
        "(7.2) and 'Land development, Mumbai, India' (7.3). Research the fund's "
        "limited-partner base and co-investors for any sovereign participation "
        "— unverified; the fund holding alone does not establish a sovereign "
        "source.",
    ),
    (
        "6",
        "9.1",
        "Pooled-investment-fund holding with an offshore-style share-class "
        "designation, held inside a brokerage account. Research the fund's "
        "domicile and sponsor and whether any sovereign limited partner is "
        "present — unverified; the parsed row identifies only a fund name and "
        "US-range values.",
    ),
]


def load_part(part_key):
    filename, disclosure_type = PART_FILES[part_key]
    doc = json.loads((SAMPLES / filename).read_text(encoding="utf-8"))
    return doc, filename, disclosure_type


def find_entry(entries, entry_number):
    """Depth-first search for the row whose entry_number matches, exactly."""
    for entry in entries:
        if entry["entry_number"] == entry_number:
            return entry
        hit = find_entry(entry.get("children", []), entry_number)
        if hit is not None:
            return hit
    return None


def build():
    candidates = []
    for index, (part_key, entry_number, scope_hypothesis) in enumerate(SELECTION, start=1):
        doc, filename, disclosure_type = load_part(part_key)
        entry = find_entry(doc["entries"], entry_number)
        if entry is None:
            raise SystemExit(
                f"entry {entry_number} not found in {filename}; selection is stale"
            )
        candidates.append(
            {
                "id": f"CAND-{index:03d}",
                "source_filing": {
                    "source_pdf": doc["source_pdf"],
                    "parsed_file": f"data/samples/{filename}",
                    "part": doc["part"],
                    # No certification_status / filing_type is emitted by the
                    # parser; report_type + form are the closest provenance the
                    # parsed filing carries. See the handoff flag-back.
                    "report_type": doc["report_type"],
                    "form": doc["form"],
                    "entry_number": entry["entry_number"],
                },
                "filer": doc["filer"],
                "business_name": entry["entity_name"],
                "business_id": None,
                "disclosure_type": disclosure_type,
                # raw_value is the verbatim parsed value cluster for this row — a
                # structured copy rather than a single string, so no parsed field
                # is dropped or paraphrased. Divergence from the handoff's
                # "string" phrasing is intentional; see the handoff doc.
                "raw_value": {
                    "value_range": entry["value_range"],
                    "income_type": entry["income_type"],
                    "income_range": entry["income_range"],
                },
                "scope_hypothesis": scope_hypothesis,
                "promotion_status": "unreviewed",
            }
        )
    return candidates


def main():
    candidates = build()
    OUTPUT.write_text(
        json.dumps(candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(candidates)} candidates -> {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
