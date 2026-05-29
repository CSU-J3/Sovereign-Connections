# Handoff #27 — Candidate lifecycle: four states, row-identity keying, kills + WLF promotion

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-29-handoff-27-candidate-lifecycle.md`
**Branch:** new branch off main (post-PR-#2 merge), e.g. `feat/candidate-lifecycle`
**Type:** schema + data. Adds a lifecycle state to candidates, logs four kills, promotes one candidate (WLF) to an SC record. Touches `web/data/candidates.json`, the candidate schema doc, and `web/data/records.json`.

## Why

Post-#26 there are 168 candidates, all `unreviewed`. Review produces dispositions, and those dispositions need to be recorded — a killed candidate with a logged reason is the audit trail that the scope bar was applied symmetrically. A silently dropped candidate looks like nobody looked. This handoff builds the disposition mechanism and applies the first five decisions.

## Critical: key dispositions on row identity, not CAND-###

The #26 re-run regenerated all `CAND-###` IDs from scratch (WLF went from absent to CAND-130). Any future re-run will shift them again. **Dispositions must therefore key on stable row identity — `(part, entry_number)` — not on the regenerated `CAND-###`.** The `CAND-###` is a display/reference convenience; `(part, entry_number)` is the identity that survives re-runs. Build the lifecycle so a disposition attaches to the row, and a re-run re-associates dispositions to the regenerated candidates by `(part, entry_number)` rather than orphaning them.

## Tasks

### 1. Add the four-state lifecycle field

Replace the current free `promotion_status: "unreviewed"` with a constrained lifecycle. Four states:

- `unreviewed` — default, mechanical emission, no decision yet.
- `hold_pending_research` — flagged as worth checking; awaiting off-session primary-source work.
- `killed_out_of_scope` — reviewed, does not meet the sovereign-adjacent bar; **requires a `disposition_reason` string**.
- `promoted` — became an SC record; **requires a `promoted_to` field** carrying the SC-### it became.

Add two sibling fields: `disposition_reason` (nullable string; required when `killed_out_of_scope`) and `promoted_to` (nullable SC-### ref; required when `promoted`). A `reviewed_at` date is worth carrying too. Update the candidate schema doc (#23 lineage) with the state set and the conditional-required rules. Keep enum/shape consistent with how records.json validates.

### 2. Apply the five dispositions, keyed on row identity

| (part, entry) | Entity | State | Reason / target |
|---------------|--------|-------|-----------------|
| Part 2, entry 1 | The Witkoff Group LLC ($120M divestiture) | `killed_out_of_scope` | Divested clean asset; reporting confirms real-estate holdings were divested while WLF crypto retained. No sovereign counterparty. Not the target. |
| Part 6, entry 1 | M&A Management Company Ltd | `killed_out_of_scope` | Cayman yacht-holding entity (Part 1 entries 76-77, George Town, Grand Cayman; sub-asset motorized water vehicles). Foreign domicile on a boat vehicle is not a sovereign tie. |
| Part 6, entry 2 | Sweet Tuna Boat Ltd | `killed_out_of_scope` | Yacht holder (motorized water vehicle). Same pattern. |
| Part 6, entry 7 | Silverpeak Legacy Partners III, L.P. | `killed_out_of_scope` | Fund in liquidation (endnote 6.7); Marseille/Mumbai are underlying properties, not counterparties; $15K-$50K interest gives no LP visibility. |
| Part 6, entry 9.1 | Optima STAR Fund - Long-Only - Class B | `hold_pending_research` | Offshore-style share class, no named sovereign LP; weakest signal. Hold, low priority. |

Each kill carries the reason verbatim-ish from the table. Source: `docs/references/collector-gap-finding-oge278.md`.

Note: the four kills' original hand-authored `scope_hypothesis` strings are now moot — mark them superseded-by-kill (don't delete the text; the kill reason explains why the hypothesis didn't hold, which is itself the audit trail).

### 3. Promote WLF to an SC record

WLF (Part 6, entry 41.8.1, currently CAND-130) is verified and promotion-ready per `docs/references/wlf-research-target.md`. Create the SC record in `web/data/records.json`:

- Assign the next free `SC-###`. Set the candidate's state to `promoted`, `promoted_to: SC-###`.
- The record documents **a financial relationship**, not a causal claim. Evidence base, all in the reference doc:
  - Abu Dhabi state-owned MGX → $2B into Binance (Binance announcement 2025-03-12, primary).
  - Settled in WLF's USD1 (Zach Witkoff, Token2049, ~2025-05-01, primary party statement).
  - WLF confirmed the deal would likely have used foreign fiat absent USD1 (WLF response via Warren-Merkley letter, Senate Banking 2025-06-11, primary correspondence).
  - WLF held in Witkoff's 278e at 41.8.1; co-founded by Zach Witkoff (filer's son).
- **Drift guards, load-bearing — the record must NOT assert:** that the MGX deal caused the Nov 2025 UAE AI-chip decision, or the CZ pardon. Both are contested (Binance's CEO denied preferential treatment). The record notes these allegations exist and are explicitly unverified; it stops at the documented financial relationship.
- Populate `primary_sources` with the typed evidence (the transaction facts above). MGX state-ownership currently rests on uncontested secondary reporting — flag it in the record as needing a primary ownership anchor for the SovereignEntity catalog entry, but it does not block the relationship record.
- This is the first SC record from a **retained** holding and the first where the sovereign tie is established entirely off-filing. Worth a one-line methodology note (separate, not in this handoff).

## Verify

- Candidate schema doc updated; four states defined with conditional-required rules.
- All 168 candidates carry the lifecycle field; 162 `unreviewed`, 4 `killed_out_of_scope` (each with a reason), 1 `hold_pending_research`, 1 `promoted`.
- Dispositions attach by `(part, entry_number)` and survive a hypothetical re-run (document the re-association logic even if not re-running now).
- New SC-### record exists in records.json, validates against the schema, `promoted_to` on the candidate matches, primary_sources populated, no causal claim asserted.
- `tsc --noEmit` + `next build` green from `web/`.

## Commit

Reasonable to split into two commits or keep as one — your call: (a) schema + lifecycle field + the five dispositions; (b) the WLF SC record. Open as a PR. Report the new SC-### and the final state tally.
