# Handoff #26 — OGE 278 parser: flatten and emit deep-leaf holdings

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-29-handoff-26-parser-deep-leaf.md`
**Branch:** new branch off main (post-#25 merge), e.g. `feat/oge-278-deep-leaf`
**Type:** parser change + re-run. Touches the OGE 278 collector's emission logic and `web/data/candidates.json`.

## Why

The full read of the Witkoff 278e (2026-05-29) found the single most consequential entity in the filing sitting where the collector can't see it: **World Liberty Financial, entry 41.8.1**, seven levels deep under Witkoff Holdings LLC, with value N/A and income N/A (the value rolls up to the parent). WLF is the case that clears the tracker's sovereign-adjacent bar (Abu Dhabi state-owned MGX → $2B → settled in WLF's USD1 → WLF held by Witkoff). The collector never emitted it because it keys on a row's own value range and/or foreign-signal tokens, and WLF's row has neither.

This is Gap 1 in `docs/references/collector-gap-finding-oge278.md`. A parser that misses the most important holding in a filing isn't doing its job. Fix: flatten the holding tree and emit leaf entities regardless of own-value.

(Gap 2 in that finding — sovereign ties that live outside the filing text — is NOT a parser fix. It's a documented scope boundary. Do not try to solve it here.)

## Tasks

### 1. Flatten the holding tree

The 278e Part 6 (and Part 2) entries nest arbitrarily deep via dotted numbering (`41`, `41.8`, `41.8.1`, …; observed up to 7+ levels in the Witkoff filing, e.g. `44.1.1.1.2.1.1.1.1`). The parser should walk the full tree and emit a candidate row for each **leaf** entity (a node with a named entity and no further children that name an entity), not only top-level rows or rows carrying their own value.

- Preserve the full ancestry path on each emitted leaf (e.g. `41 > 41.8 > 41.8.1`) so review can see where value rolls up and a reviewer can trace the parent that carries the dollar figure.
- A leaf with value N/A is still emitted. The parent's value/income stays associated via the ancestry path; do not fabricate a value on the leaf.
- Keep the existing top-level emission working; this is additive (more candidates), consistent with the #20 conservative-filtering call (over-emit at collection, filter at review).

### 2. Carry a parenthetical-descriptor signal

WLF is identifiable as interesting partly by its descriptor: `World Liberty Financial (cryptocurrency)`, adjacent `SC Financial Technologies LLC (stablecoin)`. The parser already captures these parentheticals on some rows. Make sure leaf emission preserves the parenthetical descriptor as a field — it's a weak scope signal (crypto, stablecoin, foreign-domicile hints) that review uses.

Do **not** hard-code a crypto/sovereign keyword filter at collection. The descriptor is captured and passed through; filtering stays at review. (Hard-coding "crypto = interesting" would re-introduce exactly the brittle, signal-keyed logic that missed WLF in the first place.)

### 3. Re-run against the Witkoff sample and verify WLF emits

- Re-run the collector against `data/samples/witkoff-oge278-2025-08-13-*.json`.
- **WLF (41.8.1) must now appear as a candidate**, with its ancestry path and `(cryptocurrency)` descriptor intact. Same for SC Financial Technologies (41.9.1, stablecoin).
- Expect the candidate count to rise substantially (deep trees have many leaves). That's expected and correct — review does the filtering. Report the new count.

## Verify

- Re-run reproduces all 5 prior candidates (CAND-001…005 equivalents) plus the newly-reachable deep leaves.
- WLF and SC Financial Technologies are present, with ancestry paths showing the rollup parent.
- No leaf carries a fabricated value; N/A leaves emit with N/A and an ancestry pointer.
- `tsc --noEmit` + `next build` green from `web/`.
- The emitter still writes to `web/data/candidates.json` (the #24 path).

## Note on candidate IDs

The deep-leaf re-run changes the candidate set. Decide before committing whether to (a) regenerate `CAND-###` IDs from scratch on the new set, or (b) preserve the existing 5 IDs and append new ones. Recommend (a) — the current 5 are unreviewed and four are kills (see collector-gap finding), so there's nothing worth preserving stable IDs for. Regenerate clean. Flag back if you'd rather append.

## Commit

Single feature commit: the flattening logic, the descriptor pass-through, the regenerated `candidates.json`. Message in the existing convention. Open as a PR (this is real logic, not cleanup). Report the new candidate count and confirm WLF emits.

## Downstream (not this handoff)

WLF's promotion to an SC record is handled separately — the relationship facts are verified and written up in `docs/references/wlf-research-target.md` (promotion-ready as a documented financial relationship, causal claims held as unverified). The four kills (CAND-001 real-estate divestiture, the two Cayman yacht holders, the in-liquidation Silverpeak) get logged with reasons once the four-state candidate lifecycle is built — that's its own handoff, after this one.
