"""ADV/IAPD candidate emitter (Handoff #35, build slice 1 — Affinity worked pass).

Emits pre-promotion ``CAND-###`` candidates from the structured ADV ingest
(``collectors.adv_iapd.ingest``) into ``web/data/candidates.json``, the same file
the OGE 278 emitter writes. ADV candidates are appended after the existing OGE
candidates; the OGE rows are never touched.

Shape and posture follow the OGE precedent (``collectors/oge_278/candidates.py``):
sequential ``CAND-###`` with no semantics, conservative over-emission, verbatim
copy of the parsed fields into ``raw_value`` (never retyped), ``business_id`` null
pending the ``connected_businesses.json`` registry, and ``scope_hypothesis`` as the
only hand-authored field. ADV-specific mapping (Handoff #35 Step 3):

  - ``disclosure_type``  = ``adv_private_fund`` (keyed to Schedule D 7.B, a new
    taxonomy member alongside the OGE part-keyed types — not retrofitted).
  - ``source_filing``    = ADV provenance: ``source`` ("adv_iapd"), CRD, SEC
    number, filing id + date, form, table, and source dataset.
  - ``raw_value``        = the fund's 7.B fields copied verbatim from the ingest.
  - ``rollup_value``     = the firm-level Item 5 totals the fund sits within
    (regulatory AUM, non-US AUM) — the ADV analog of the OGE parent rollup,
    carried alongside the fund for concentration context, never fabricated onto
    the fund. (Proposed reuse of the OGE slot — flagged in the handoff report.)
  - ``filer``            = the adviser legal name, ``business_name`` = the fund
    name, both verbatim from the structured filing (uppercase as the SEC serves
    them). The filer/business_name mapping is flagged back in the handoff.
  - ``descriptor``       = null: ADV fund names carry no parenthetical, so the OGE
    descriptor slot has no ADV analog; the fund type lives in ``raw_value``.

Emission rule (Step 4): over the seeded adviser(s), emit one candidate per private
fund that reports non-US ownership (``%Owned Non-US`` > 0). Funds reporting no
non-US ownership are not emitted. Filtering to actual sovereign scope is a
promotion-time judgment, not the collector's. Emitted candidates are ordered by
gross asset value descending so the ``CAND-###`` assignment is deterministic
across runs.

Lifecycle: every ADV candidate emits ``promotion_status: "unreviewed"`` with null
disposition siblings. The proxy limit (#33/#34) holds — the ADV gives ownership
*shape*, never owner *identity* — so ``scope_hypothesis`` stays a hedged research
prompt that names the proxy signal and states plainly that the owners are not in
the ADV and the sovereign source is unverified. It never asserts a sovereign
connection.

Idempotent: a re-run strips prior ``adv_iapd`` candidates, re-fetches, and
re-appends from the current max OGE id, so the OGE rows and the ADV ids stay
stable as long as the OGE count is fixed.

Run: ``.venv/Scripts/python -m collectors.adv_iapd.candidates`` (Windows) /
``.venv/bin/python -m collectors.adv_iapd.candidates`` (macOS/Linux).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from collectors.adv_iapd import ingest

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = REPO_ROOT / "web" / "data" / "candidates.json"

# Seeded adviser list (Handoff #35 scope guardrail): CRD 315482 (Affinity) only.
# The covered-adviser inventory that grows this is a later handoff.
SEED_CRDS = ["315482"]

# Hand-authored hedged research prompts, keyed by the fund's Schedule D 7.B
# ``Fund ID``. Each names the proxy signal (percent non-US, owner concentration,
# fund scale) and states plainly that the owners are not in the ADV and the
# sovereign source is unverified. A fund without an authored prompt falls back to
# the templated hedge below (still proxy-only, still asserts nothing).
HYPOTHESES = {
    # Affinity Partners Parallel Fund I LP
    "805-7516626074": (
        "Schedule D 7.B reports this fund 100% beneficially owned by non-United "
        "States persons, $4,307,145,842 gross asset value across only 6 beneficial "
        "owners — roughly 70% of the adviser's $6,160,297,411 regulatory AUM. The "
        "scale and six-owner concentration are consistent with large institutional "
        "or sovereign limited partners, but Form ADV reports only the aggregate "
        "non-US percentage and the owner count; it does not name the owners. "
        "Whether any beneficial owner is a sovereign-wealth fund is unverified and "
        "not established by the ADV — secondary-source identity work is required "
        "before promotion. No sovereign connection is asserted."
    ),
    # Affinity Partners Fund I Co-Invest Delta LP
    "805-9422731494": (
        "Schedule D 7.B reports this co-investment fund 100% beneficially owned by "
        "non-United States persons, $1,193,319,132 held by a single beneficial "
        "owner. A single foreign beneficial owner at this scale is consistent with "
        "one large institutional or sovereign limited partner, but the ADV gives "
        "only the aggregate non-US percentage and owner count, never the owner's "
        "identity. The sovereign source is unverified and not established by the "
        "ADV; secondary-source identity work is required before promotion. No "
        "sovereign connection is asserted."
    ),
    # Affinity Partners Fund I Co-Invest Sigma LP
    "805-3756709628": (
        "Schedule D 7.B reports this co-investment fund 100% beneficially owned by "
        "non-United States persons, $596,596,930 held by a single beneficial "
        "owner. As with the other Affinity co-invest vehicles, a single foreign "
        "owner at this scale points to one large institutional or sovereign "
        "limited partner, but the ADV reports only the aggregate non-US share and "
        "owner count and names no owner. The sovereign source is unverified and "
        "not established by the ADV; secondary-source identity work is required "
        "before promotion. No sovereign connection is asserted."
    ),
}


def _scope_hypothesis(fund: dict) -> str:
    authored = HYPOTHESES.get(fund.get("fund_id"))
    if authored:
        return authored
    gav = fund.get("gross_asset_value")
    return (
        f"Schedule D 7.B reports this fund {fund.get('percent_non_us_owners')}% "
        "beneficially owned by non-United States persons, "
        f"${gav:,} gross asset value across "
        f"{fund.get('beneficial_owner_count')} beneficial owner(s). Form ADV "
        "reports only the aggregate non-US percentage and owner count — it does "
        "not name the owners. Whether any beneficial owner is a sovereign-wealth "
        "fund is unverified and not established by the ADV; secondary-source "
        "identity work is required before promotion. No sovereign connection is "
        "asserted."
    )


def _candidate(firm: dict, fund: dict) -> dict:
    """One candidate for a private fund reporting non-US ownership. id set later."""
    return {
        "id": None,
        "source_filing": {
            "source": "adv_iapd",
            "crd": firm["crd"],
            "sec_number": firm["sec_number"],
            "filing_id": firm["filing_id"],
            "filing_date": firm["filing_date"],
            "form": "SEC Form ADV Part 1A, Schedule D Section 7.B",
            "table": firm["source_table"],
            "source_dataset": firm["source_dataset"],
        },
        "filer": firm["legal_name"],
        "business_name": fund["fund_name"],
        # ADV fund names carry no parenthetical; the OGE descriptor slot has no
        # ADV analog. Fund type is kept in raw_value, not retyped here.
        "descriptor": None,
        "business_id": None,
        "disclosure_type": "adv_private_fund",
        # Verbatim 7.B fields, copied from the ingest — never retyped.
        "raw_value": {
            "fund_id": fund["fund_id"],
            "fund_type": fund["fund_type"],
            "gross_asset_value": fund["gross_asset_value"],
            "percent_non_us_owners": fund["percent_non_us_owners"],
            "beneficial_owner_count": fund["beneficial_owner_count"],
        },
        # Firm-level Item 5 context the fund sits within — concentration signal,
        # carried alongside the fund, never fabricated onto it.
        "rollup_value": {
            "firm_regulatory_aum": firm["item5"]["regulatory_aum"],
            "firm_non_us_aum": firm["item5"]["non_us_aum"],
        },
        "scope_hypothesis": _scope_hypothesis(fund),
        "promotion_status": "unreviewed",
        "disposition_reason": None,
        "disposition_rule": None,
        "promoted_to": None,
        "reviewed_at": None,
        "scope_hypothesis_superseded": False,
    }


def _next_id_number(preserved: list[dict]) -> int:
    nums = [int(re.sub(r"\D", "", c["id"])) for c in preserved if c.get("id")]
    return (max(nums) + 1) if nums else 1


def build() -> list[dict]:
    """Existing non-ADV candidates, then freshly emitted ADV candidates.

    Reads the current ``candidates.json``, keeps every non-``adv_iapd`` row
    untouched (the OGE candidates), and appends one ADV candidate per seeded
    fund reporting non-US ownership, with ids continuing from the current max.
    """
    existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
    preserved = [
        c for c in existing
        if (c.get("source_filing") or {}).get("source") != "adv_iapd"
    ]

    emitted: list[dict] = []
    for crd in SEED_CRDS:
        firm = ingest.fetch_firm(crd)
        ingest.validate(firm)  # stop on source drift; do not emit drifted numbers
        funds = [f for f in firm["private_funds"] if (f.get("percent_non_us_owners") or 0) > 0]
        funds.sort(key=lambda f: -(f.get("gross_asset_value") or 0))
        emitted.extend(_candidate(firm, f) for f in funds)

    start = _next_id_number(preserved)
    for offset, cand in enumerate(emitted):
        cand["id"] = f"CAND-{start + offset:03d}"
    return preserved + emitted


def write_candidates(candidates: list[dict]) -> Path:
    """Serialize to ``candidates.json``; same format as the OGE writer (#28)."""
    OUTPUT.write_text(
        json.dumps(candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return OUTPUT


def main() -> None:
    candidates = build()
    write_candidates(candidates)
    adv = [c for c in candidates if (c.get("source_filing") or {}).get("source") == "adv_iapd"]
    print(f"wrote {len(candidates)} candidates ({len(adv)} ADV) -> {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
