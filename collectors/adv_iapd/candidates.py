"""ADV/IAPD candidate emitter (Handoff #35 build; #36 writer unification).

Emits pre-promotion ``CAND-###`` candidates from the structured ADV ingest
(``collectors.adv_iapd.ingest``) into ``web/data/candidates.json``, the same file
the OGE 278 emitter writes. This module is now pure emission: :func:`build_rows`
turns one assembled firm object into ADV candidate rows; the orchestration (which
firms to fetch) lives in ``collectors.adv_iapd.collector`` and the merge-and-write
(coexisting with the OGE rows, preserving ids) lives in the shared
``collectors.common.candidate_writer`` (Handoff #36). The OGE rows are never
touched, and a re-run keeps each ADV fund's ``CAND-###`` stable by
:func:`source_entity_key`.

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
    carried alongside the fund as the concentration denominator, never fabricated
    onto the fund. See ``docs/collectors/candidate-schema-notes.md``.
  - ``filer``            = the adviser legal name, ``business_name`` = the fund
    name, both verbatim from the structured filing (uppercase as the SEC serves
    them).
  - ``descriptor``       = null: ADV fund names carry no parenthetical, so the OGE
    descriptor slot has no ADV analog; the fund type lives in ``raw_value``.

Emission rule (Step 4): over the seeded adviser(s), emit one candidate per private
fund that reports non-US ownership (``%Owned Non-US`` > 0). Funds reporting no
non-US ownership are not emitted. Filtering to actual sovereign scope is a
promotion-time judgment, not the collector's. Emitted rows are ordered by gross
asset value descending (then fund id) so emission is deterministic.

Lifecycle: every ADV candidate emits ``promotion_status: "unreviewed"`` with null
disposition siblings. The proxy limit (#33/#34) holds — the ADV gives ownership
*shape*, never owner *identity* — so ``scope_hypothesis`` stays a hedged research
prompt that names the proxy signal and states plainly that the owners are not in
the ADV and the sovereign source is unverified. It never asserts a sovereign
connection.
"""

from __future__ import annotations

# This collector's source tag in the shared candidates.json. Every ADV row
# carries it in source_filing.source so the shared writer (Handoff #36) can scope
# a regeneration to the ADV slice and leave the OGE rows untouched.
SOURCE = "adv_iapd"

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


def source_entity_key(candidate: dict):
    """Stable identity of an ADV candidate's source entity (Handoff #36).

    The firm CRD plus the Schedule D 7.B Fund ID — the *fund*, not the filing
    instance, so a re-filing of the same fund keeps its ``CAND-###``. The shared
    writer uses this to preserve ids across re-runs; it must not depend on
    emission order or id.
    """
    sf = candidate["source_filing"]
    return (sf.get("crd"), (candidate.get("raw_value") or {}).get("fund_id"))


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
    """One candidate for a private fund reporting non-US ownership. id set by the writer."""
    return {
        "id": None,
        "source_filing": {
            "source": SOURCE,
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


def build_rows(firm: dict) -> list[dict]:
    """The ADV candidates for one assembled firm object (ids left unset).

    One candidate per private fund reporting non-US ownership; funds with none are
    not emitted. Ordered by gross asset value descending, then fund id, so emission
    is deterministic. The shared writer assigns ids, preserving a fund's
    ``CAND-###`` by :func:`source_entity_key`.
    """
    funds = [f for f in firm["private_funds"] if (f.get("percent_non_us_owners") or 0) > 0]
    funds.sort(key=lambda f: (-(f.get("gross_asset_value") or 0), f.get("fund_id") or ""))
    return [_candidate(firm, f) for f in funds]
