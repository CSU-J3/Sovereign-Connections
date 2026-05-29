# Collector-gap finding — OGE 278 parser, two blind spots (Witkoff filing)

**Status:** finding, to be logged against the `oge_278_collector.py` wiring handoff
**Source:** full read of Witkoff OGE Form 278e (`whitehouse.gov/wp-content/uploads/2025/09/Witkoff-Steven.pdf`), 2026-05-29
**Impact:** affects every future OGE 278 the collector processes, not just this filing

## The two gaps

### Gap 1 — deeply-nested zero-value holdings are invisible

The parser emits candidates on foreign-signal fields at the rows it surfaces. It did not surface **World Liberty Financial**, which sits at entry **41.8.1**, seven levels deep:

```
41 Witkoff Holdings LLC → 41.8 WC Digital Fi LLC → 41.8.1 World Liberty Financial (cryptocurrency)
```

WLF carries value N/A and income N/A — the value rolls up to the parent. A collector keying on a row's own value range or foreign-signal token never sees it. Same for 41.9.1 SC Financial Technologies LLC (stablecoin).

**Implication:** the substance of an OGE 278 lives in the leaf nodes of deep holding trees, and the most consequential holdings are often the ones with N/A own-values because they roll up. The parser needs to flatten and emit leaf entities regardless of own-value, not just rows carrying their own value/foreign token.

### Gap 2 — off-filing sovereign connections can't be reached by definition

WLF's sovereign-adjacent tie (UAE fund $500M; ~$2B MGX deal) appears **nowhere in the 278e**. It exists only in reporting and Senate oversight. No parser reading the filing's own text can surface a connection that isn't in the text.

**Implication:** the collector is a *candidate-surfacer*, not a connection-finder. It can flag "this entity exists and looks worth checking"; it cannot establish sovereign ties that live outside the filing. That's a human research step, and the methodology should state it plainly — the disclosure form under-captures by design, so the tracker's value is in the off-filing verification, not in the parse. (Worth a methodology-page line.)

## What this does NOT change

The conservative collector-level filtering call (#20) still stands — over-emit at collection, filter at review. Gap 1 is an argument to over-emit *more* (flatten deep trees), consistent with that call. Gap 2 isn't a parser bug; it's a scope boundary to document.

## Candidate kill dispositions (from the full filing)

| Candidate | Disposition | Filing evidence |
|-----------|-------------|-----------------|
| CAND-001 (Witkoff Group $120M) | kill / downgrade — divested clean asset, no sovereign question | Part 2 entry 1; reporting confirms real-estate divested, WLF retained |
| CAND-002 (M&A Management Ltd) | kill — Cayman yacht holder | Part 1 entries 76-77: M&A Boat Ltd + M&A Management Company Ltd, George Town, Grand Cayman; sub-asset is motorized water vehicles |
| CAND-003 (Sweet Tuna Boat Ltd) | kill — yacht holder | Part 6 entry 2: motorized water vehicle |
| CAND-004 (Silverpeak Legacy III) | kill / trivial — fund in liquidation | endnote 6.7 "Currently in liquidation"; Marseille/Mumbai are properties, $15K-$50K interest |
| CAND-005 (Optima STAR Fund) | hold, low priority — offshore share class, no named sovereign LP | Part 6 entry 9.1; unchanged from prior read |

Each kill should be recorded with its reason, not silently dropped — the logged kill is the audit trail that the bar was applied symmetrically. This is the argument for the four-state candidate lifecycle (`unreviewed → promoted / hold_pending_research / killed_out_of_scope`, reason on kill).

## Live target

WLF — see `wlf-research-target.md`. Not in `candidates.json`; needs manual entry or a re-run after Gap 1 is fixed.
