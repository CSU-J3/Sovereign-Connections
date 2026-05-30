"""Candidate review worksheet generator (Handoff #29).

Reads ``web/data/candidates.json`` and emits a human-reviewable worksheet of the
``unreviewed`` candidates to ``docs/reviews/2026-05-29-oge278-witkoff-review.md``.

This is a **read-only scaffold**: it makes no disposition, writes no default, and
never touches ``candidates.json`` or any record. The disposition / reason columns
are left empty for a human to fill; a later handoff reads the filled worksheet and
writes the decisions back into ``candidates.json`` keyed on ``(part, entry_number)``
(the #27 mechanism, so a re-run can't orphan them).

The worksheet is a snapshot — re-run this after any candidate regeneration (a new
deep-leaf pass or a new filing) to reproduce it from current data.

Run: .venv/Scripts/python -m collectors.oge_278.review_worksheet (Windows) /
     .venv/bin/python -m collectors.oge_278.review_worksheet (macOS/Linux).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = REPO_ROOT / "web" / "data" / "candidates.json"
OUTPUT = REPO_ROOT / "docs" / "reviews" / "2026-05-29-oge278-witkoff-review.md"

# OGE Form 278e value brackets, ascending. Rank is used for sorting (high value
# surfaces first) and for the "high rollup_value" sort tier. A blank/None value
# ranks 0. Income-only single amounts (no bracket string) fall back to a
# magnitude→rank lookup below.
VALUE_BRACKETS = (
    "None (or less than $1,001)",
    "$1,001 - $15,000",
    "$15,001 - $50,000",
    "$50,001 - $100,000",
    "$100,001 - $250,000",
    "$250,001 - $500,000",
    "$500,001 - $1,000,000",
    "$1,000,001 - $5,000,000",
    "$5,000,001 - $25,000,000",
    "$25,000,001 - $50,000,000",
    "Over $50,000,000",
)
_RANK = {b: i + 1 for i, b in enumerate(VALUE_BRACKETS)}  # 0 reserved for "no value"
# Upper bound of each bracket (for income-only amounts that aren't a bracket
# string), parallel to VALUE_BRACKETS; "Over $50M" has no upper bound.
_UPPER = (1_000, 15_000, 50_000, 100_000, 250_000, 500_000,
          1_000_000, 5_000_000, 25_000_000, 50_000_000, float("inf"))
# Sort tier 3 ("high rollup_value") = lower bound >= $1,000,001, i.e. the
# "$1,000,001 - $5,000,000" bracket and above.
HIGH_VALUE_RANK = _RANK["$1,000,001 - $5,000,000"]

# US location tails (USPS codes + the spelled forms that appear in the filing).
# A real-estate row reading "..., City, <tail>" whose tail is one of these is
# domestic and gets no place tag.
US_STATE_TAILS = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC", "Mass", "Wash", "Calif", "Conn", "Fla", "Tex",
}
# Corporate-form tails that are NOT locations — excluded so "..., Inc." etc.
# never reads as a foreign place.
CORP_TAILS = {"Inc.", "Inc", "LLC", "L.P.", "LP", "Ltd.", "Ltd", "Corp.",
              "Corp", "Co.", "Co", "PLC", "N.A.", "N.A"}

# Non-US corporate-form suffixes (genuinely foreign vehicles). "LP"/"L.P." is a
# standard US form too, so it is tagged separately (suffix:LP) and never asserted
# as foreign — the reviewer decides; we only name the suffix we saw.
FOREIGN_SUFFIX_RE = re.compile(
    r"\b(Ltd|Limited|GmbH|S\.A\.|S\.A|N\.V\.|N\.V|AG|PLC|Pte|S\.r\.l|Sarl|"
    r"S\.à\.r\.l|B\.V\.|B\.V|SpA|OOO|Oy|AB|SE)\b"
)
US_SUFFIX_RE = re.compile(r"\b(L\.P\.|LP)\b")
# A fund share-class designation (same weak "offshore-style share class" signal
# the 9.1 hold flagged). Not asserted as offshore; surfaced as share-class.
SHARE_CLASS_RE = re.compile(r"\bClass\s+([A-Z])\b")


def _effective_value(c: dict) -> tuple[str | None, str | None]:
    """The value string to show and the ancestor it rolls up from.

    Own value if the row carries one; otherwise the nearest value-carrying
    ancestor (``rollup_value``). Returns (value_string, ancestor_entry_or_None).
    """
    rv = c["raw_value"]
    own = rv.get("value_range") or rv.get("income_range")
    if own:
        return own, None
    roll = c.get("rollup_value")
    if roll:
        return roll.get("value_range") or roll.get("income_range"), roll.get("entry_number")
    return None, None


def _value_rank(value_str: str | None) -> int:
    if not value_str:
        return 0
    if value_str in _RANK:
        return _RANK[value_str]
    amounts = [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", value_str)]
    if not amounts:
        return 0
    biggest = max(amounts)
    for rank, upper in enumerate(_UPPER, start=1):
        if biggest <= upper:
            return rank
    return len(VALUE_BRACKETS)


def _location_tag(name: str) -> str | None:
    """A foreign place tag for a '<asset>, <city>, <tail>' row, or None.

    Domestic (US-state tail) and corporate tails ("Inc.") yield no tag; a tail
    that is a non-US place name (e.g. France, India) yields ``place:<tail>``.
    Limitation: catches a foreign tail in the row's own name; a foreign sub-entry
    is itself an emitted leaf row, so it surfaces on its own line.
    """
    parts = [p.strip() for p in name.split(",")]
    if len(parts) < 2:
        return None
    tail = parts[-1]
    # A US state may trail without its comma ("New York NY") — if the last token
    # of the tail is a state code, the row is domestic.
    last_token = tail.split()[-1] if tail.split() else tail
    if tail in US_STATE_TAILS or last_token in US_STATE_TAILS or tail in CORP_TAILS:
        return None
    # A place name is title-case alphabetic words (allow a space, e.g. "Hong Kong").
    if re.fullmatch(r"[A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)*", tail):
        return f"place:{tail}"
    return None


def signal_tags(name: str) -> list[str]:
    """Foreign / weak-scope signal tags on a row's name. Surfaced, never judged."""
    name = name or ""
    tags: list[str] = []
    for m in dict.fromkeys(FOREIGN_SUFFIX_RE.findall(name)):
        tags.append(f"suffix:{m}")
    if US_SUFFIX_RE.search(name):
        tags.append("suffix:LP")
    place = _location_tag(name)
    if place:
        tags.append(place)
    sc = SHARE_CLASS_RE.search(name)
    if sc:
        tags.append(f"share-class:{sc.group(1)}")
    return tags


def _entry_sort_key(part_key: str, entry_number: str) -> tuple:
    """Natural order for (part, dotted entry number): part asc, then numerically."""
    nums = tuple(int(x) for x in entry_number.split("."))
    return (int(part_key), nums)


def _part_key(candidate: dict) -> str:
    """The part key ('2'/'5'/'6') from the candidate's parsed-file path."""
    parsed = candidate["source_filing"]["parsed_file"]
    m = re.search(r"-part(\d+)\.json$", parsed)
    return m.group(1) if m else "?"


def build_rows(candidates: list[dict]) -> list[dict]:
    """Shape unreviewed candidates into worksheet rows, sorted surface-to-bottom."""
    rows = []
    for c in candidates:
        if c["promotion_status"] != "unreviewed":
            continue
        name = c["business_name"] or ""
        value_str, rollup_from = _effective_value(c)
        tags = signal_tags(name)
        rank = _value_rank(value_str)
        rows.append({
            "cand": c["id"],
            "part": _part_key(c),
            "entry": c["source_filing"]["entry_number"],
            "name": name,
            "ancestry": c["source_filing"]["ancestry_path"],
            "value": value_str,
            "rollup_from": rollup_from,
            "descriptor": c["descriptor"],
            "tags": tags,
            "rank": rank,
        })

    def sort_key(r):
        has_desc = bool(r["descriptor"])
        has_flag = bool(r["tags"])
        is_high = r["rank"] >= HIGH_VALUE_RANK
        # Tier: 0 descriptor, 1 foreign flag, 2 high value, 3 everything else.
        if has_desc:
            tier = 0
        elif has_flag:
            tier = 1
        elif is_high:
            tier = 2
        else:
            tier = 3
        # Within tiers 0-2, higher value first; tier 3 stays in entry order.
        value_order = 0 if tier == 3 else -r["rank"]
        return (tier, value_order, _entry_sort_key(r["part"], r["entry"]))

    rows.sort(key=sort_key)
    return rows


def _esc(text: str | None) -> str:
    return (text or "").replace("|", "\\|")


def render(rows: list[dict], dispositioned: list[dict]) -> str:
    total = len(rows) + len(dispositioned)
    out: list[str] = []
    out.append("# OGE 278 Candidate Review Worksheet — Witkoff (2026-05-13 filing)")
    out.append("")
    out.append(f"- **Generated:** 2026-05-29 (snapshot; regenerate with "
               "`collectors/oge_278/review_worksheet.py`)")
    out.append("- **Source filing:** `data/samples/witkoff-oge278-2025-08-13.pdf` "
               "(OGE Form 278e, New Entrant Report)")
    out.append(f"- **Candidates total:** {total}  ·  "
               f"**unreviewed shown:** {len(rows)}  ·  "
               f"**already dispositioned, excluded:** {len(dispositioned)} "
               f"({len(rows)} + {len(dispositioned)} = {total})")
    out.append("")
    out.append("## Already dispositioned (excluded from the table below)")
    out.append("")
    out.append("These 6 are not in the worksheet; listed so the count reconciles. "
               "World Liberty Financial is **promoted**, not unreviewed, so it is "
               "correctly absent below.")
    out.append("")
    out.append("| (part, entry) | entity | state | → |")
    out.append("|---|---|---|---|")
    for d in dispositioned:
        target = d.get("promoted_to") or ""
        out.append(f"| ({d['part']}, {d['entry']}) | {_esc(d['name'])} | "
                   f"{d['state']} | {target} |")
    out.append("")
    out.append("## How to use this worksheet")
    out.append("")
    out.append("- Fill the **disposition** column with one of the four lifecycle "
               "states: `unreviewed` (leave as-is), `hold_pending_research`, "
               "`killed_out_of_scope`, or `promoted`.")
    out.append("- `killed_out_of_scope` **requires a reason** in the reason/note "
               "column (the audit trail that the bar was applied — a silent drop "
               "looks like nobody looked). `promoted` requires the target `SC-###`.")
    out.append("- Dispositions key on **(part, entry_number)**, the stable row "
               "identity — *not* on `CAND-###`, which is a display handle that a "
               "candidate re-run reassigns. Edit the disposition/reason cells; a "
               "later handoff reads them back keyed on (part, entry).")
    out.append("- Review against the established bar: "
               "`docs/references/collector-gap-finding-oge278.md` (kill precedent) "
               "and `docs/references/wlf-research-target.md` (promote precedent).")
    out.append("")
    out.append("**Sort key (convenience, NOT a judgment):** rows are ordered "
               "surface-to-bottom by tier — (1) has a descriptor (parenthetical: "
               "crypto, stablecoin, fund/ticker markers), then (2) carries a "
               "foreign-signal tag, then (3) high rollup value (≥ $1,000,001 "
               "bracket), then (4) everything else in entry order; within tiers "
               "1–3, higher value first. A row low in the list is just where the "
               "eye lands last — it is **not** a Code assertion that it's less "
               "likely to be killed.")
    out.append("")
    out.append("**Signal tags** are surfaced, not judged: `suffix:Ltd` etc. = a "
               "non-US corporate form; `suffix:LP` = US limited-partnership form "
               "(shown for completeness, not asserted foreign); `place:France` = a "
               "non-US place name in the row; `share-class:B` = a fund share-class "
               "designation (the same weak signal the 9.1 hold flagged).")
    out.append("")
    out.append(f"## Unreviewed candidates ({len(rows)})")
    out.append("")
    out.append("| # | CAND (ref) | (part, entry) | entity | ancestry_path | "
               "value | descriptor | signals | disposition | reason / note |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, start=1):
        value = _esc(r["value"]) or "—"
        if r["rollup_from"]:
            value += f" ↥{r['rollup_from']}"
        out.append(
            f"| {i} | {r['cand']} | ({r['part']}, {r['entry']}) | "
            f"{_esc(r['name'])} | {_esc(r['ancestry'])} | {value} | "
            f"{_esc(r['descriptor']) or '—'} | "
            f"{_esc(', '.join(r['tags'])) or '—'} |  |  |"
        )
    out.append("")
    return "\n".join(out)


def dispositioned_rows(candidates: list[dict]) -> list[dict]:
    out = []
    for c in candidates:
        if c["promotion_status"] == "unreviewed":
            continue
        out.append({
            "part": _part_key(c),
            "entry": c["source_filing"]["entry_number"],
            "name": c["business_name"] or "",
            "state": c["promotion_status"],
            "promoted_to": c.get("promoted_to"),
        })
    out.sort(key=lambda d: _entry_sort_key(d["part"], d["entry"]))
    return out


def generate() -> tuple[str, int]:
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    rows = build_rows(candidates)
    disp = dispositioned_rows(candidates)
    return render(rows, disp), len(rows)


def main() -> None:
    text, n = generate()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text + "\n", encoding="utf-8")
    print(f"wrote {n} unreviewed rows -> {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
