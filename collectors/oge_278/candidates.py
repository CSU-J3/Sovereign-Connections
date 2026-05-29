"""OGE 278 candidate emitter (Handoffs #23 schema, #26 deep-leaf, #27 lifecycle).

Reads the parsed OGE Form 278e part files produced by
``collectors/oge_278/parser.py`` and emits pre-promotion candidate records into
``web/data/candidates.json`` (beside ``web/data/records.json``, the records they
promote into).

A *candidate* is a parsed financial-disclosure row that **might** describe a
sovereign-source connection, before any human research has confirmed scope.
Candidates sit between raw parser output and promoted ``SC-###`` records in
``web/data/records.json``. Promotion (``CAND-###`` -> ``SC-###``) is a separate
human step; this module does not filter to actual scope and does not research.

Design decisions (Handoff #23):
  1. Sequential IDs ``CAND-001``, ``CAND-002`` ... in parse order; no semantics.
  2. Conservative over-emission: any row that *could* describe a foreign-source
     payment, position, or asset is eligible. Scope filtering happens at
     promotion, not here.
  3. ``business_id`` is a nullable slot for a future
     ``data/connected_businesses.json`` registry; it stays ``null`` here.

Emission rule (Handoff #26 — deep-leaf flatten):
  The 278e Part 2/5/6 entries nest arbitrarily deep via dotted numbering
  (``41`` -> ``41.8`` -> ``41.8.1`` ... observed 7+ levels in the Witkoff
  filing). The collector walks the full tree and emits a candidate for every
  node that is **either a leaf entity** (a named node with no children that name
  an entity) **or carries its own value/income**. This is the fix for Gap 1 in
  ``docs/references/collector-gap-finding-oge278.md``: the most consequential
  holding in the Witkoff filing — World Liberty Financial, entry ``41.8.1``,
  value N/A because it rolls up to the parent — was invisible to an emitter that
  keyed on a row's own value range. A leaf with value N/A is still emitted; its
  parent's dollar figure is carried alongside it via ``rollup_value`` and the
  full ``ancestry_path``, never fabricated onto the leaf.

  Emitting leaves regardless of own-value is *additive* over the prior top-level
  emission (more candidates), consistent with the #23 conservative-filtering
  call: over-emit at collection, filter at review. Deep trees have many leaves,
  so the count is large by design.

Every verbatim field (``filer``, ``business_name``, ``raw_value``) is COPIED from
the parsed row, never retyped, so it cannot drift from the parse. ``descriptor``
is the parenthetical lifted verbatim from ``business_name`` (a substring, not a
retype) — a weak scope signal (``cryptocurrency``, ``stablecoin``,
foreign-domicile hints) that review uses; it is deliberately NOT filtered on at
collection (hard-coding "crypto = interesting" is exactly the brittle,
signal-keyed logic that missed WLF). ``scope_hypothesis`` is the only
hand-authored field; the mechanical walk leaves it ``null`` except on the small
set of worked rows in ``HYPOTHESES`` (the Handoff #23 pass), where the original
hedged research prompt is preserved.

Lifecycle (Handoff #27 — four states, row-identity keying):
  ``promotion_status`` is a constrained four-state lifecycle:
    - ``unreviewed`` (default) — mechanical emission, no decision yet.
    - ``hold_pending_research`` — worth checking; awaiting off-session work.
    - ``killed_out_of_scope`` — reviewed, fails the sovereign-adjacent bar;
      **requires ``disposition_reason``** (the logged reason is the audit trail
      that the bar was applied symmetrically — a silent drop looks like nobody
      looked).
    - ``promoted`` — became an SC record; **requires ``promoted_to``** (the
      ``SC-###`` it became).
  Sibling fields ``disposition_reason`` (nullable), ``promoted_to`` (nullable
  ``SC-###``), and ``reviewed_at`` (nullable ISO date) carry the disposition.

  Dispositions are keyed on **stable row identity ``(part, entry_number)``**, not
  on ``CAND-###``. The #26 re-run regenerated every ``CAND-###`` from scratch
  (WLF went from absent to ``CAND-130``); any future re-run shifts them again. By
  keying ``DISPOSITIONS`` on ``(part, entry_number)`` the emitter re-associates a
  recorded disposition to whatever ``CAND-###`` the row lands on this run — a
  re-run never orphans a review decision. The ``CAND-###`` stays a display handle
  only. When a killed row also carried a worked ``scope_hypothesis``, that text
  is kept (not deleted) and flagged ``scope_hypothesis_superseded: true`` — the
  kill reason explains why the hypothesis didn't hold, which is itself the trail.

Run: ``.venv/Scripts/python -m collectors.oge_278.candidates`` (Windows) /
``.venv/bin/python -m collectors.oge_278.candidates`` (macOS/Linux).
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SAMPLES = REPO_ROOT / "data" / "samples"
OUTPUT = REPO_ROOT / "web" / "data" / "candidates.json"

# The parsed OGE 278e part files, in parse order (Parts 2, 5, 6). disclosure_type
# is drawn from the part — NOT inferred from the row. The handoff's example set
# (position/asset/income/agreement/gift) does not map: the parser covers only the
# three asset-&-income sections, so the taxonomy is keyed to the parsed parts.
# Dict order is the parse order and sets the CAND-### sequence.
PART_FILES = {
    "2": ("witkoff-oge278-2025-08-13-part2.json", "filer_employment_asset"),
    "5": ("witkoff-oge278-2025-08-13-part5.json", "spouse_employment_asset"),
    "6": ("witkoff-oge278-2025-08-13-part6.json", "other_asset_income"),
}

# Hand-authored research prompts, keyed by (part_key, entry_number). These are
# the worked-pass hypotheses from the Handoff #23 emission; they are preserved on
# their exact rows so those candidates stay true equivalents after the #26
# deep-leaf re-run. Every other emitted candidate gets scope_hypothesis=None —
# the walk is mechanical and the hypothesis is authored at review, never inferred
# (Handoff #23: if a field can't be filled from parsed data, leave it null). Each
# prompt stays a hedged research question, never a finding.
HYPOTHESES = {
    ("2", "1"): (
        "Filer reports $120,000,000 in proceeds from the sale of an interest "
        "in The Witkoff Group as part of divestiture planning. OGE Form 278e "
        "Part 2 prints the amount but no acquirer/counterparty (those would "
        "live in a separate OGE ethics agreement). Research whether the "
        "divested interest was acquired by a sovereign-linked entity — "
        "unverified; no buyer is named in the parsed filing."
    ),
    ("6", "1"): (
        "Holding entity carries a 'Ltd' suffix (a non-US corporate form) and "
        "its only sub-asset is motorized water vehicles (a yacht-holding "
        "pattern). Research the entity's domicile and whether any "
        "foreign/sovereign counterparty is involved in its financing or "
        "ownership — unverified; the parsed row shows only a US-range value."
    ),
    ("6", "2"): (
        "Same 'Ltd' yacht-holding pattern as M&A Management Company Ltd, at a "
        "$1M-$5M value range. Research domicile and whether any "
        "foreign/sovereign counterparty is involved — unverified; nothing in "
        "the parsed row asserts a foreign source."
    ),
    ("6", "7"): (
        "Private-equity fund interest whose parsed sub-entries include "
        "foreign-located assets — 'Mixed use real estate, Marseille, France' "
        "(7.2) and 'Land development, Mumbai, India' (7.3). Research the fund's "
        "limited-partner base and co-investors for any sovereign participation "
        "— unverified; the fund holding alone does not establish a sovereign "
        "source."
    ),
    ("6", "9.1"): (
        "Pooled-investment-fund holding with an offshore-style share-class "
        "designation, held inside a brokerage account. Research the fund's "
        "domicile and sponsor and whether any sovereign limited partner is "
        "present — unverified; the parsed row identifies only a fund name and "
        "US-range values."
    ),
}

# The four lifecycle states (Handoff #27). `unreviewed` is the mechanical
# default; the other three are review dispositions recorded in DISPOSITIONS.
STATES = (
    "unreviewed",
    "hold_pending_research",
    "killed_out_of_scope",
    "promoted",
)

# Review dispositions, keyed on stable row identity (part_key, entry_number) so
# they survive the re-run that regenerates every CAND-### (Handoff #27). Each
# value is {status, reviewed_at, and the conditional-required sibling}:
#   - killed_out_of_scope -> requires "reason"
#   - promoted            -> requires "promoted_to"
#   - hold_pending_research -> "reason" optional (rationale kept for the trail)
# Reasons are lifted from docs/references/collector-gap-finding-oge278.md and the
# Handoff #27 disposition table. apply_disposition() enforces the required slots.
DISPOSITIONS = {
    ("2", "1"): {
        "status": "killed_out_of_scope",
        "reviewed_at": "2026-05-29",
        "reason": (
            "Divested clean asset; reporting confirms real-estate holdings were "
            "divested while the WLF crypto was retained. No sovereign "
            "counterparty named in the filing. Not the target."
        ),
    },
    ("6", "1"): {
        "status": "killed_out_of_scope",
        "reviewed_at": "2026-05-29",
        "reason": (
            "Cayman yacht-holding entity (Part 1 entries 76-77, George Town, "
            "Grand Cayman; sub-asset is motorized water vehicles). Foreign "
            "domicile on a boat-holding vehicle is not a sovereign tie."
        ),
    },
    ("6", "2"): {
        "status": "killed_out_of_scope",
        "reviewed_at": "2026-05-29",
        "reason": (
            "Yacht holder (motorized water vehicle). Same pattern as M&A "
            "Management Company Ltd."
        ),
    },
    ("6", "7"): {
        "status": "killed_out_of_scope",
        "reviewed_at": "2026-05-29",
        "reason": (
            "Fund in liquidation (endnote 6.7); Marseille/Mumbai entries are "
            "underlying properties, not counterparties; a $15K-$50K interest "
            "gives no limited-partner visibility."
        ),
    },
    ("6", "9.1"): {
        "status": "hold_pending_research",
        "reviewed_at": "2026-05-29",
        "reason": (
            "Offshore-style share class, no named sovereign limited partner; "
            "weakest signal. Hold, low priority."
        ),
    },
    ("6", "41.8.1"): {
        "status": "promoted",
        "reviewed_at": "2026-05-29",
        "promoted_to": "SC-007",
        "reason": (
            "Promoted as a documented financial relationship into the existing "
            "World Liberty Financial record SC-007 (not a new record): Abu "
            "Dhabi state-owned MGX -> $2B Binance investment settled in WLF's "
            "USD1 stablecoin; WLF held at 41.8.1, co-founded by the filer's "
            "son. Causal claims (UAE AI-chip decision, CZ pardon) are held as "
            "explicitly unverified and are NOT asserted by the record. See "
            "docs/references/wlf-research-target.md."
        ),
    },
}

# A trailing or embedded parenthetical descriptor, e.g. "World Liberty Financial
# (cryptocurrency)" -> "cryptocurrency". The last group wins when more than one.
DESCRIPTOR_RE = re.compile(r"\(([^()]+)\)")


def load_part(part_key):
    filename, disclosure_type = PART_FILES[part_key]
    doc = json.loads((SAMPLES / filename).read_text(encoding="utf-8"))
    return doc, filename, disclosure_type


def _descriptor(entity_name):
    """The verbatim parenthetical descriptor lifted from an entity name, or None."""
    groups = DESCRIPTOR_RE.findall(entity_name or "")
    return groups[-1].strip() if groups else None


def _is_leaf(node):
    """A node with no child that names an entity (Handoff #26 leaf definition)."""
    return not any((c.get("entity_name") or "").strip() for c in node.get("children", []))


def _carries_value(node):
    """True if the row reports its own value or income (the prior emission key)."""
    return bool(node.get("value_range")) or bool(node.get("income_range"))


def _rollup_value(ancestors):
    """Nearest ancestor carrying a value/income figure — where this leaf rolls up.

    ``ancestors`` is the root-to-parent stack; the nearest one wins so a reviewer
    can trace the dollar figure without re-opening the parse. None if no ancestor
    carries a value (e.g. the node is itself a top-level value-carrier).
    """
    for anc in reversed(ancestors):
        if _carries_value(anc):
            return {
                "entry_number": anc["entry_number"],
                "entity_name": anc["entity_name"],
                "value_range": anc.get("value_range"),
                "income_type": anc.get("income_type"),
                "income_range": anc.get("income_range"),
            }
    return None


def apply_disposition(candidate, part_key, entry_number):
    """Attach the lifecycle state for this row, keyed on (part, entry_number).

    Defaults to ``unreviewed`` with null siblings. Enforces the conditional-
    required rules: ``killed_out_of_scope`` needs a reason, ``promoted`` needs a
    ``promoted_to``. A killed row that carried a worked ``scope_hypothesis`` is
    flagged superseded (the hypothesis text is kept; the kill reason is the
    audit trail). Mutates and returns ``candidate``.
    """
    disp = DISPOSITIONS.get((part_key, entry_number), {})
    status = disp.get("status", "unreviewed")
    if status not in STATES:
        raise SystemExit(f"unknown lifecycle state {status!r} for ({part_key}, {entry_number})")
    reason = disp.get("reason")
    promoted_to = disp.get("promoted_to")
    if status == "killed_out_of_scope" and not reason:
        raise SystemExit(f"killed_out_of_scope requires a reason: ({part_key}, {entry_number})")
    if status == "promoted" and not promoted_to:
        raise SystemExit(f"promoted requires promoted_to: ({part_key}, {entry_number})")

    candidate["promotion_status"] = status
    candidate["disposition_reason"] = reason
    candidate["promoted_to"] = promoted_to
    candidate["reviewed_at"] = disp.get("reviewed_at")
    candidate["scope_hypothesis_superseded"] = bool(
        status == "killed_out_of_scope" and candidate["scope_hypothesis"]
    )
    return candidate


def _candidate(node, ancestors, doc, filename, disclosure_type, part_key):
    entry_number = node["entry_number"]
    path = " > ".join([a["entry_number"] for a in ancestors] + [entry_number])
    candidate = {
        # id is assigned after the full walk, once parse order is fixed.
        "id": None,
        "source_filing": {
            "source_pdf": doc["source_pdf"],
            "parsed_file": f"data/samples/{filename}",
            "part": doc["part"],
            # No certification_status / filing_type is emitted by the parser;
            # report_type + form are the closest provenance the parsed filing
            # carries. See the Handoff #23 flag-back.
            "report_type": doc["report_type"],
            "form": doc["form"],
            "entry_number": entry_number,
            # Full dotted ancestry, root -> this node, so review can see the
            # tree position and trace where the value rolls up (Handoff #26).
            "ancestry_path": path,
        },
        "filer": doc["filer"],
        "business_name": node["entity_name"],
        # Parenthetical descriptor lifted verbatim from business_name — a weak
        # scope signal passed through, never filtered on at collection.
        "descriptor": _descriptor(node["entity_name"]),
        "business_id": None,
        "disclosure_type": disclosure_type,
        # raw_value is the verbatim parsed value cluster for this row — a
        # structured copy rather than a single string, so no parsed field is
        # dropped or paraphrased. Divergence from the Handoff #23 "string"
        # phrasing is intentional; see the schema doc.
        "raw_value": {
            "value_range": node.get("value_range"),
            "income_type": node.get("income_type"),
            "income_range": node.get("income_range"),
        },
        # The value/income-carrying ancestor this leaf rolls up into, or null
        # when the row carries its own value. Never fabricated onto the leaf.
        "rollup_value": _rollup_value(ancestors),
        "scope_hypothesis": HYPOTHESES.get((part_key, entry_number)),
        # Lifecycle fields are filled by apply_disposition below, keyed on
        # (part, entry_number) so a re-run re-associates recorded decisions.
        "promotion_status": "unreviewed",
        "disposition_reason": None,
        "promoted_to": None,
        "reviewed_at": None,
        "scope_hypothesis_superseded": False,
    }
    return apply_disposition(candidate, part_key, entry_number)


def build():
    candidates = []
    for part_key in PART_FILES:
        doc, filename, disclosure_type = load_part(part_key)

        def walk(nodes, ancestors):
            for node in nodes:
                name = (node.get("entity_name") or "").strip()
                # Emit a leaf entity regardless of own-value (the #26 fix), and
                # keep the prior emission of any row carrying its own value.
                if name and (_is_leaf(node) or _carries_value(node)):
                    candidates.append(
                        _candidate(node, ancestors, doc, filename,
                                   disclosure_type, part_key)
                    )
                walk(node.get("children", []), ancestors + [node])

        walk(doc["entries"], [])

    # Re-association integrity: every recorded disposition must have landed on an
    # emitted row. A miss means a disposition is keyed on a (part, entry_number)
    # the current parse no longer produces — a stale decision to fix, not orphan.
    emitted_keys = {
        (k, c["source_filing"]["entry_number"])
        for c in candidates
        for k in PART_FILES
        if c["source_filing"]["parsed_file"].endswith(PART_FILES[k][0])
    }
    stale = [key for key in DISPOSITIONS if key not in emitted_keys]
    if stale:
        raise SystemExit(f"dispositions key rows that were not emitted: {stale}")

    for index, candidate in enumerate(candidates, start=1):
        candidate["id"] = f"CAND-{index:03d}"
    return candidates


def main():
    candidates = build()
    OUTPUT.write_text(
        json.dumps(candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(candidates)} candidates -> {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
