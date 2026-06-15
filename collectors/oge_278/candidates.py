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

  ``disposition_rule`` (Handoff #30, nullable string) names the bucket rule a
  ``killed_out_of_scope`` row matched (``B1``..``B6``; ``PRE`` for the four kills
  carried forward from #27), so a reader can audit why the row was killed. It is
  required on every kill and null on ``promoted``/``hold_pending_research``/
  ``unreviewed``. The bucket rules and the frozen ``(part, entry_number)`` -> bucket
  map live in ``BUCKETS`` / ``_BUCKET_KILLS`` below; a row matching no rule is left
  ``unreviewed`` and flagged, never default-killed.

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

from collectors.common import candidate_writer

REPO_ROOT = Path(__file__).resolve().parents[2]
SAMPLES = REPO_ROOT / "data" / "samples"
OUTPUT = REPO_ROOT / "web" / "data" / "candidates.json"

# This collector's source tag in the shared candidates.json. Every OGE row
# carries it in source_filing.source so the shared writer (Handoff #36) can scope
# a regeneration to the OGE slice and leave sibling rows (ADV/IAPD) untouched.
SOURCE = "oge_278"


def source_entity_key(candidate):
    """Stable identity of an OGE candidate's source entity (Handoff #36).

    The parsed filing plus the dotted entry number — the same ``(part,
    entry_number)`` row identity dispositions key on (#27), expressed via the
    fields present on the candidate. The shared writer uses this to preserve a
    row's ``CAND-###`` across re-runs; it must not depend on parse order or id.
    """
    sf = candidate["source_filing"]
    return (sf.get("parsed_file"), sf.get("entry_number"))

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

# Bucket kill scheme (Handoff #30). The 2026-05-29 review dispositioned every
# remaining `unreviewed` candidate as `killed_out_of_scope` by bucket. Each
# killed row carries `disposition_reason` (the bucket reason) AND
# `disposition_rule` (the rule that matched) so a reader can audit why the row
# landed in its bucket. The rules, applied to the reviewed set in this precedence
# (first match wins):
#   B6  sub-entry of a killed holding -- (6,1)/(6,2)/(6,7) -- inherits the kill
#   B4  foreign-listed public equity   -- foreign corporate suffix + ticker/ADR
#   B5  US fund LP interest            -- LP form, no sovereign LP identified
#   B3  domestic bank cash             -- descriptor == "cash"
#   B2  domestic US-listed security    -- US-listed ticker or money-market fund
#   B1  domestic operating / RE        -- residual; no foreign/sovereign signal
# A row matching no rule is NOT killed -- it stays `unreviewed` and is flagged for
# human review (a fall-through is a review gap, never a default kill, Handoff #30).
BUCKETS = {
    "B1": (
        "Domestic Witkoff operating business or US real-estate/holding "
        "structure; no foreign or sovereign counterparty.",
        "B1 domestic operating / RE structure",
    ),
    "B2": (
        "Domestic US-listed security or money-market fund; no sovereign "
        "counterparty.",
        "B2 domestic public securities",
    ),
    "B3": (
        "Domestic bank cash; no sovereign counterparty.",
        "B3 domestic cash",
    ),
    "B4": (
        "Publicly-traded foreign-listed equity held as an ordinary position; "
        "foreign listing is not a sovereign tie.",
        "B4 foreign-listed public equity",
    ),
    "B5": (
        "US-managed fund LP interest; no sovereign limited partner identified "
        "and the interest size gives no LP-roster visibility.",
        "B5 US fund LP, no sovereign LP",
    ),
    "B6": (
        "Sub-entry of an out-of-scope parent (see parent disposition); "
        "property/asset inside a killed holding, not a counterparty.",
        "B6 leaf under killed parent",
    ),
}

# Bucketed kills from the 2026-05-29 review (Handoff #30), keyed on stable row
# identity (part_key, entry_number). Derived by applying the bucket rules above to
# the Handoff #29 review worksheet, then frozen here as data -- the #27
# decisions-as-keyed-data philosophy: a re-run re-associates each decision to
# whatever CAND-### the row lands on and never silently re-buckets; a row the
# parse no longer emits orphan-raises rather than vanishing.
_BUCKET_KILLS = {
    # B1 (115)
    ("2", "1.1"): "B1", ("2", "1.2.1"): "B1", ("2", "1.3.1"): "B1", ("6", "5"): "B1",
    ("6", "5.1"): "B1", ("6", "6"): "B1", ("6", "6.1"): "B1", ("6", "8"): "B1",
    ("6", "8.1"): "B1", ("6", "11.1"): "B1", ("6", "12.1"): "B1", ("6", "14"): "B1",
    ("6", "14.1"): "B1", ("6", "15"): "B1", ("6", "15.1"): "B1", ("6", "15.2"): "B1",
    ("6", "16"): "B1", ("6", "16.1"): "B1", ("6", "17"): "B1", ("6", "18"): "B1",
    ("6", "19"): "B1", ("6", "20"): "B1", ("6", "21"): "B1", ("6", "22"): "B1",
    ("6", "22.1"): "B1", ("6", "22.2.1.1.1"): "B1", ("6", "23"): "B1", ("6", "24"): "B1",
    ("6", "24.1.1.1.1.1"): "B1", ("6", "25"): "B1", ("6", "25.1.1.1.1.1.1.1"): "B1",
    ("6", "26"): "B1", ("6", "26.1.1.1.1.1"): "B1", ("6", "27"): "B1", ("6", "27.1.1"): "B1",
    ("6", "27.2.1"): "B1", ("6", "27.3"): "B1", ("6", "28"): "B1", ("6", "28.1.1.1.1.1"): "B1",
    ("6", "29"): "B1", ("6", "29.1.1.1.1.1.1.1"): "B1", ("6", "30"): "B1", ("6", "31"): "B1",
    ("6", "31.1.1.1.1.1"): "B1", ("6", "32"): "B1", ("6", "32.1.1.1.1"): "B1",
    ("6", "32.1.2.1.1"): "B1", ("6", "32.1.3.1"): "B1", ("6", "33"): "B1", ("6", "33.1.1"): "B1",
    ("6", "33.1.2"): "B1", ("6", "33.1.3"): "B1", ("6", "34"): "B1",
    ("6", "34.1.1.1.1.1.1"): "B1", ("6", "34.2.1.1"): "B1", ("6", "34.3.1.1"): "B1",
    ("6", "35"): "B1", ("6", "36"): "B1", ("6", "36.1.1.1.1.1.1"): "B1", ("6", "37"): "B1",
    ("6", "37.1.1"): "B1", ("6", "38"): "B1", ("6", "38.1.1.1.1"): "B1",
    ("6", "38.1.1.1.2.1.1"): "B1", ("6", "39"): "B1", ("6", "39.1.1.1.1"): "B1",
    ("6", "40"): "B1", ("6", "40.1.1.1.1"): "B1", ("6", "41"): "B1",
    ("6", "41.1.1.1.1.1.1.1"): "B1", ("6", "41.1.1.1.1.1.2.1"): "B1",
    ("6", "41.1.1.1.1.1.3"): "B1", ("6", "41.2.1.1.1.1.1"): "B1", ("6", "41.2.1.1.1.2.1"): "B1",
    ("6", "41.2.1.1.1.3.1"): "B1", ("6", "41.2.1.1.1.4.1"): "B1", ("6", "41.2.1.1.1.5.1"): "B1",
    ("6", "41.2.1.1.1.6.1"): "B1", ("6", "41.3.1.1"): "B1", ("6", "41.4.1"): "B1",
    ("6", "41.5"): "B1", ("6", "41.6"): "B1", ("6", "41.7"): "B1", ("6", "42"): "B1",
    ("6", "42.1.1.1.1"): "B1", ("6", "43"): "B1", ("6", "43.1.1"): "B1", ("6", "44"): "B1",
    ("6", "44.1.1.1.1.1.1.1.1"): "B1", ("6", "44.1.1.1.2.1.1.1.1"): "B1",
    ("6", "44.1.1.1.3.1.1.1.1"): "B1", ("6", "45"): "B1", ("6", "46"): "B1", ("6", "47"): "B1",
    ("6", "47.1"): "B1", ("6", "48"): "B1", ("6", "49"): "B1", ("6", "50"): "B1",
    ("6", "51"): "B1", ("6", "52"): "B1", ("6", "52.1"): "B1", ("6", "53"): "B1",
    ("6", "53.1"): "B1", ("6", "54"): "B1", ("6", "54.1"): "B1", ("6", "58"): "B1",
    ("6", "58.1.1"): "B1", ("6", "59"): "B1", ("6", "59.1"): "B1", ("6", "60"): "B1",
    ("6", "60.1"): "B1", ("6", "61"): "B1", ("6", "61.1"): "B1", ("6", "62"): "B1",
    ("6", "62.1.1"): "B1",
    # B2 (25)
    ("5", "1.1"): "B2", ("5", "1.2"): "B2", ("5", "1.3"): "B2", ("5", "1.4"): "B2",
    ("5", "1.5"): "B2", ("5", "1.6"): "B2", ("5", "1.8"): "B2", ("6", "10.1"): "B2",
    ("6", "11.2"): "B2", ("6", "12.2"): "B2", ("6", "12.3"): "B2", ("6", "12.4"): "B2",
    ("6", "12.5"): "B2", ("6", "13.1"): "B2", ("6", "13.2"): "B2", ("6", "13.3"): "B2",
    ("6", "13.4"): "B2", ("6", "13.6"): "B2", ("6", "13.7"): "B2", ("6", "13.9"): "B2",
    ("6", "19.1"): "B2", ("6", "20.1"): "B2", ("6", "21.1"): "B2", ("6", "46.1.1"): "B2",
    ("6", "50.1"): "B2",
    # B3 (7)
    ("5", "1.7"): "B3", ("6", "11.3"): "B3", ("6", "12.9"): "B3", ("6", "13.8"): "B3",
    ("6", "55"): "B3", ("6", "56"): "B3", ("6", "57"): "B3",
    # B4 (2)
    ("6", "12.6"): "B4", ("6", "13.5"): "B4",
    # B5 (7)
    ("6", "3"): "B5", ("6", "4"): "B5", ("6", "12.7"): "B5", ("6", "12.7.1"): "B5",
    ("6", "12.7.2"): "B5", ("6", "12.7.3"): "B5", ("6", "12.8"): "B5",
    # B6 (5)
    ("6", "1.1"): "B6", ("6", "2.1"): "B6", ("6", "7.1"): "B6", ("6", "7.2"): "B6",
    ("6", "7.3"): "B6",
}

# Point review-decisions that are not bucket kills, keyed on (part_key,
# entry_number): the two USD1-stack promotes, Optima's hold, and the four
# pre-existing kills carried forward from #27. The pre-existing kills keep their
# original detailed reasons (their substance predates the bucket scheme) and are
# marked with rule "PRE" so every killed row still carries a disposition_rule.
_SPECIAL = {
    ("2", "1"): {
        "status": "killed_out_of_scope",
        "reviewed_at": "2026-05-29",
        "rule": "PRE pre-bucket disposition (Handoff #27)",
        "reason": (
            "Divested clean asset; reporting confirms real-estate holdings were "
            "divested while the WLF crypto was retained. No sovereign "
            "counterparty named in the filing. Not the target."
        ),
    },
    ("6", "1"): {
        "status": "killed_out_of_scope",
        "reviewed_at": "2026-05-29",
        "rule": "PRE pre-bucket disposition (Handoff #27)",
        "reason": (
            "Cayman yacht-holding entity (Part 1 entries 76-77, George Town, "
            "Grand Cayman; sub-asset is motorized water vehicles). Foreign "
            "domicile on a boat-holding vehicle is not a sovereign tie."
        ),
    },
    ("6", "2"): {
        "status": "killed_out_of_scope",
        "reviewed_at": "2026-05-29",
        "rule": "PRE pre-bucket disposition (Handoff #27)",
        "reason": (
            "Yacht holder (motorized water vehicle). Same pattern as M&A "
            "Management Company Ltd."
        ),
    },
    ("6", "7"): {
        "status": "killed_out_of_scope",
        "reviewed_at": "2026-05-29",
        "rule": "PRE pre-bucket disposition (Handoff #27)",
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
    ("6", "41.9.1"): {
        "status": "promoted",
        "reviewed_at": "2026-05-29",
        "promoted_to": "SC-007",
        "reason": (
            "Promoted into the existing World Liberty Financial record SC-007 as "
            "the second retained-holding leg of the USD1 stack: SC Financial "
            "Technologies LLC (stablecoin), held at 41.9.1 under WC Digital SC "
            "LLC, co-owns the USD1 stablecoin brand alongside WLF (41.8.1) and is "
            "the SC Financial Technologies signatory of the exploratory Pakistan "
            "PVARA MOU. Documented financial relationship only; the MGX/UAE and "
            "Pakistan legs stay distinct and no causal claim is asserted. See "
            "docs/references/wlf-research-target.md."
        ),
    },
}


def _build_dispositions():
    """Merge the point-decisions with the expanded bucket kills into one registry.

    Keyed on (part_key, entry_number). Bucket kills expand to the shared bucket
    reason + rule; a bucket-kill key that collides with a point-decision is a
    construction error (the same row can't be both).
    """
    registry = dict(_SPECIAL)
    for key, bucket_id in _BUCKET_KILLS.items():
        if key in registry:
            raise SystemExit(f"bucket kill collides with a point-decision: {key}")
        reason, rule = BUCKETS[bucket_id]
        registry[key] = {
            "status": "killed_out_of_scope",
            "reviewed_at": "2026-05-29",
            "reason": reason,
            "rule": rule,
        }
    return registry


# The disposition registry: point-decisions + bucketed kills, keyed on
# (part_key, entry_number). apply_disposition() enforces the required slots.
DISPOSITIONS = _build_dispositions()

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
    rule = disp.get("rule")
    promoted_to = disp.get("promoted_to")
    if status == "killed_out_of_scope" and not reason:
        raise SystemExit(f"killed_out_of_scope requires a reason: ({part_key}, {entry_number})")
    if status == "killed_out_of_scope" and not rule:
        raise SystemExit(f"killed_out_of_scope requires a disposition_rule: ({part_key}, {entry_number})")
    if status == "promoted" and not promoted_to:
        raise SystemExit(f"promoted requires promoted_to: ({part_key}, {entry_number})")

    candidate["promotion_status"] = status
    candidate["disposition_reason"] = reason
    # disposition_rule (Handoff #30) names the bucket rule that matched, for
    # killed rows; null for promoted/hold/unreviewed.
    candidate["disposition_rule"] = rule
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
            # Source tag for the shared writer's slice scoping (Handoff #36).
            "source": SOURCE,
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
        "disposition_rule": None,
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

    # ids are assigned by the shared writer (Handoff #36), not here: it preserves
    # each row's existing CAND-### by source_entity_key and only mints new ids for
    # genuinely new rows, so a re-run keeps OGE 1-168 stable. build() returns the
    # emitted rows with ``id`` unset (None).
    return candidates


def write_candidates(candidates):
    """Write the OGE rows through the shared, source-scoped writer; return the path.

    Since Handoff #36 the OGE collector no longer overwrites the whole file. It
    hands its freshly emitted rows to ``collectors.common.candidate_writer``
    scoped to ``oge_278``: the writer regenerates only the OGE slice, preserves
    the ADV/IAPD sibling rows, reuses each OGE row's existing ``CAND-###`` by
    ``source_entity_key``, and writes back in stable global id order with the same
    serialization as before (byte-identical on an unchanged run).
    """
    path, _ = candidate_writer.write_source_rows(SOURCE, candidates, source_entity_key)
    return path


def main():
    candidates = build()
    write_candidates(candidates)
    print(f"wrote {len(candidates)} OGE candidates -> {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
