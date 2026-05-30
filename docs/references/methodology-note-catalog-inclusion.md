# Methodology note — sovereign-entity catalog inclusion is evaluation-gated, not state-gated

**Date:** 2026-05-30
**Status:** decided; versioned principle
**Applies to:** `sovereign_entities.json` (the SovereignEntity catalog) and any candidate that proposes a sovereign-source counterparty
**Owner:** CJ

## The principle

An entity enters `sovereign_entities.json` only after it has been **evaluated against the sovereign-and-sovereign-adjacent standard in the context of a documented fact pattern.** Entities are catalogued on evaluation, never on the existence of a state.

There is no such thing as adding a *country* to the catalog. The catalog records *vehicles* (funds, holding companies, SOEs, intermediaries) that cleared the standard because a real, documented transaction named them and forced the evaluation. Every existing entry got there that way: PIF, Mubadala, MGX, ADQ, and the Tahnoon-controlled cluster were each evaluated against a specific transaction, with their governance structure cited, not assumed.

## Why this is the discipline, not a limitation

This is the catalog-side expression of the tracker's load-bearing drift guard: **"sovereign source paid" must not slide into "sovereign government paid."** The standard turns on a specific vehicle's governance structure, not on the state behind it. Cataloguing a country pre-emptively — before any vehicle is named or evaluated — *is* the SWF-vs-government conflation the methodology exists to prevent. It would have the catalog asserting "[State] sovereign money" as a live category before a single [State] vehicle had been shown to be a sovereign-source vehicle.

It is the same discipline that:
- kept **Burisma** out (private Cyprus holding, no state equity, no sovereign-source payment — failed the standard against its actual fact pattern);
- required **MGX**'s state-ownership to be *verified* against the fact pattern rather than assumed from its UAE domicile.

A catalog gap for a given state is therefore not a definitional hole. It is the correct, honest state of the catalog when no vehicle from that state has yet been a counterparty in a documented transaction. The absence is information: it says "no fact pattern has required this evaluation," which is true and should stay visible.

## Application: Iran

Iran has no entry in `sovereign_entities.json`. Under this principle, **none is added now.**

- The only Iran-adjacent item in the project is the floated ~$300B investment-fund proposal in the `docs/triage/` video-review log — relayed by an aggregator, doubted by the source itself, with no named vehicle, no governance structure, and no primary record. Under the 5-tier evidence hierarchy it sits at tier 4–5.
- There is nothing to evaluate: no fund, no entity, no transaction. So there is no catalog entry to make.
- Iran is **not excluded as a state.** If a documented transaction later names a specific Iranian state-investment vehicle, that vehicle gets evaluated against the standard at that point — same as any other. The watch item stays in triage until then.

## What this closes

This converts the previously-open "should Iran be in the catalog" question into a settled, versioned rule that generalizes to every state:

> Vehicles enter the catalog on evaluation against a documented fact pattern. The existence of a state, a floated proposal, or press speculation is never sufficient. A catalog with no entry for a given state is correct whenever no vehicle from that state has been evaluated.

It also pre-empts the failure mode where a future session sees the Iran watch item (or any country-level prompt) and reflexively adds a state-level entry. If a future candidate proposes an Iranian (or any new-state) counterparty, the work is: name the vehicle, cite its governance, evaluate against the standard, *then* catalog — in that order, never the reverse.

## Pointer

- Triage item: `docs/triage/2026-05-29-triage-01-video-review-vulcan-iran.md` (Iran fund = pre-candidate FSF watch item; Vulcan Elements routed to Connected Procurement).
- Standard: PROJECT.md Defined Terms ("foreign sovereign and sovereign-adjacent money"); v2.0 covered-intermediary category bounded by portfolio overlap.
