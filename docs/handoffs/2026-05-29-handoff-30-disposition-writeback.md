# Handoff #30 — Disposition write-back: 2 promotes, ~160 bucketed kills, SC-007 enrichment

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-29-handoff-30-disposition-writeback.md`
**Branch:** new branch off main (post-PR-#5 merge — see note), e.g. `feat/disposition-writeback`
**Type:** data + record. Writes review dispositions into `candidates.json` via the `(part, entry_number)`-keyed registry, enriches SC-007. No parser changes, no schema changes.

## Prerequisite: merge PR #5 first

PR #5 (the review worksheet + generator) is still open and off main. The worksheet is the input artifact this handoff acts on. Merge PR #5 to main first (standard gate: no conflict, `tsc --noEmit` + `next build` green from `web/`, `--no-ff`, push, re-verify on merged main). Then branch this work off clean main.

## Why

The full 162-candidate review (2026-05-29, against the #29 worksheet) is complete. Every row is dispositioned. This handoff writes those decisions into the data through the same `(part, entry_number)`-keyed DISPOSITIONS registry that #27 used, so a future re-run re-associates them instead of orphaning. The scope calls are Corey's, already made; Code is **applying** decisions, not judging candidates. To keep that line auditable, every kill records both its bucket reason and the matching rule.

## The dispositions

### Two promotes — both legs of the USD1 stack → SC-007

| (part, entry) | Entity | State | Target |
|---------------|--------|-------|--------|
| (6, 41.8.1) | World Liberty Financial | `promoted` | SC-007 (already set as CAND-130; confirm intact) |
| (6, 41.9.1) | SC Financial Technologies LLC | `promoted` | SC-007 (new this handoff) |

Both are retained Witkoff holdings and the two ownership legs of USD1. Evidence base and drift guards: `docs/references/wlf-research-target.md` (retitled to cover both legs). See SC-007 enrichment below.

### One hold — unchanged

| (part, entry) | Entity | State | Note |
|---------------|--------|-------|------|
| (6, 9.1) | Optima STAR Fund – Long-Only – Class B | `hold_pending_research` | already set in #27; leave as-is, do not re-key or overwrite |

### Kills — by bucket

Every remaining `unreviewed` candidate is `killed_out_of_scope`. Apply by bucket rule. Each killed row gets `disposition_reason` = the bucket reason string, plus a `disposition_rule` field naming the rule that matched (so the kill is auditable: a reader can see why this row landed in this bucket). If a row matches no bucket rule, **do not kill it — flag it for Corey.** A row that falls through is a review gap, not a default kill.

| Bucket | Rule (what matches) | `disposition_reason` |
|--------|---------------------|----------------------|
| B1 domestic operating / RE structure | WG-prefixed entities, named US real-estate developments, holding LLCs with no reportable assets, aircraft, the Walgreens net-lease portfolio | "Domestic Witkoff operating business or US real-estate/holding structure; no foreign or sovereign counterparty." |
| B2 domestic public securities | rows whose descriptor is a US-listed ticker (REITs, single stocks) or a US money-market/treasury fund (FTIXX, SETXX, etc.) | "Domestic US-listed security or money-market fund; no sovereign counterparty." |
| B3 domestic cash | rows whose descriptor is `cash` (the US bank entries) | "Domestic bank cash; no sovereign counterparty." |
| B4 foreign-listed public equity | Flex Ltd [FLEX], Shell PLC Spon ADR [SHEL] | "Publicly-traded foreign-listed equity held as ordinary position; foreign listing is not a sovereign tie." |
| B5 US fund LP, no sovereign LP | Atreides Foundation Fund LP, Addition Three LP, Coatue Fintech Fund I LP (+ its Class A tranches), Highbridge Convertible Dislocation Fund LP | "US-managed fund LP interest; no sovereign limited partner identified and interest size gives no LP-roster visibility." |
| B6 leaf under killed parent | leaves whose parent entry is itself killed — the motorized water vehicle (6, 2.1) under Sweet Tuna Boat (6, 2); Marseille (6, 7.2) and Mumbai (6, 7.3) under Silverpeak (6, 7) | "Sub-entry of an out-of-scope parent (see parent disposition); property/asset inside a killed holding, not a counterparty." |

The four original kills already set in #27 (Witkoff Group divestiture at (2,1), M&A Management at (6,1), Sweet Tuna Boat at (6,2), Silverpeak at (6,7)) stay killed — do not overwrite their existing reasons; if their reasons predate the bucket scheme, you may align them to B1/B6 wording for consistency, but preserve the substance.

## Tasks

1. **Merge PR #5** (prerequisite above), branch off clean main.
2. **Add `disposition_rule`** to the candidate schema as a nullable string sibling to `disposition_reason` (required when `killed_out_of_scope` under this handoff's bucket scheme; null otherwise). Update the schema doc (#23 lineage).
3. **Write the dispositions** into the DISPOSITIONS registry keyed on `(part, entry_number)`: the 2 promotes, the bucketed kills, leaving Optima's hold untouched. Re-run the emitter (`collector.py` or `candidates.py build()`) so the states land in `web/data/candidates.json` and the orphan-raise validates.
4. **Fall-through check:** any `unreviewed` row that matches no bucket rule is NOT killed — collect these and list them in the report for Corey. Expected count: 0, but the point is to prove it rather than assume it.
5. **Enrich SC-007** (`web/data/records.json`) for the SC Financial Technologies leg, per `docs/references/wlf-research-target.md`:
   - Establish SC Financial Technologies (41.9.1) as the second retained-holding leg of the USD1 stack alongside WLF (41.8.1).
   - Add sources: USD1 co-ownership (July 2025 reserve documentation) and the Pakistan PVARA MOU **with signatory attributed to SC Financial Technologies**. **Precision fix:** if SC-007's existing PVARA source attributes the MOU to WLF, correct it to SC Financial Technologies — that's a factual correction, not just an addition.
   - **Drift guards, load-bearing:** Pakistan MOU is *exploratory* (no consummated transaction, terms undisclosed) — do not inflate it. Keep the MGX/UAE leg and the Pakistan leg as two distinct documented relationships through USD1, not one fused narrative. No causal claim about any Witkoff official act.
6. **Commit the reference doc** `docs/references/wlf-research-target.md` (the retitled USD1-stack version) in this branch — it's the evidence base for the SC-007 enrichment and should land with it, not separately.

## Verify

- Final candidate tally: 162 → 0 `unreviewed`. Expect 2 `promoted`, 1 `hold_pending_research` (Optima), 165 `killed_out_of_scope` (160 from this pass + the prior... — **report the exact tally**, don't assume my arithmetic; the count of pre-existing kills vs new kills should reconcile to 168 total candidates).
- Every kill has both `disposition_reason` and `disposition_rule`; no kill has a null reason.
- Zero fall-through rows (or, if any, listed for Corey — not killed).
- (6, 41.8.1) and (6, 41.9.1) both `promoted_to: SC-007`; Optima (6, 9.1) still `hold_pending_research` with its original note.
- SC-007 validates; SC Financial Technologies leg present; PVARA signatory reads SC Financial Technologies; no causal claim; MGX and Pakistan legs distinct.
- DISPOSITIONS orphan-raise still fires (the registry must reject a `(part,entry)` that doesn't match an emitted row).
- `tsc --noEmit` + `next build` green from `web/`. End-to-end `collector.py` run reproduces the final state idempotently.

## Commit / PR

Reasonable split: (a) schema `disposition_rule` + the registry dispositions + re-emitted candidates.json; (b) SC-007 enrichment + the reference doc. Open as a PR. Report the exact final state tally, the fall-through list (expected empty), and confirm SC-007's PVARA signatory fix.

## Downstream (not this handoff)

With the backlog cleared, Cron wiring becomes the live next front — the schedule now refills a queue that's actually being worked. Also still owed: the methodology-page one-line note on retained/off-filing holdings, and the MGX + USD1 co-ownership primary anchors for catalog hygiene.
