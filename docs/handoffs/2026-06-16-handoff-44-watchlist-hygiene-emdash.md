# Handoff #44 — Watchlist parser-status hygiene + SC-007/SC-009 em-dash cleanup

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-44-watchlist-hygiene-emdash.md`
**Depends on:** nothing blocking. Touches the watchlist and SC-007/SC-009 record text. Branch off `main`.
**Type:** docs / data. Two mechanical cleanups, no tier change, no methodology change.

## What this does

Two stale-text fixes. The watchlist still describes the ADV parser as not built and counts one ADV subject; both are now wrong. And SC-007/SC-009 carry em-dashes in record-layer text that violate the house no-em-dash rule.

## Part 1: Watchlist staleness (`docs/references/fsf-watchlist.md`)

The ADV parser was built in #35/#36, and 1789 (W-004) is now the second ADV subject alongside Affinity (SC-009). Two lines are stale.

1. Source-taxonomy table: the `adv` row reads "no parser yet" (or similar). Update it to reflect that the parser exists, built in #35/#36, matching how the table denotes parser status for the other source types.
2. "Deferred / owed" section: it states the ADV parser "is justified only when a second adv subject appears" and counts "1 × adv." The parser is built and there are now two ADV subjects (Affinity/SC-009, 1789/W-004). Mark the ADV-parser deferred item as done (built #35/#36) or remove it per the section's convention, and update the subject count to 2.

Do not change any other watchlist content. The W-001 through W-004 entries stay exactly as they are.

## Part 2: SC-007/SC-009 em-dash cleanup (`web/data/records.json`)

Scan the SC-007 and SC-009 record-layer text fields (primary_source `label` values, and any record prose such as notes or descriptions) for em-dashes and rewrite to comply with the house no-em-dash rule, preserving meaning with a comma, parentheses, or a restructure.

Record-layer only. Do not touch candidate `scope_hypotheses`; the no-em-dash rule is records and published prose only, ruled earlier in the project. Show the before and after for each rewrite.

## Verify

- Only `fsf-watchlist.md` and `records.json` changed.
- The W-001 through W-004 entries are unchanged.
- All primary_source `category` values and structure are unchanged. This pass is label text only, no tier changes.
- No `candidates.json` or `PROJECT.md` change.

## Commit

Single commit, both files plus this handoff. Suggested:

```
docs: watchlist parser-status hygiene + SC-007/009 em-dash cleanup (#44)
```

Do not push unless asked.

## Flag back, do not decide

- If the watchlist taxonomy table or deferred section uses a fixed convention that doesn't fit "mark done" (for example a fixed status enum), surface it and propose the closest fit.
- If any SC-007/SC-009 em-dash rewrite would change meaning rather than punctuation, flag it rather than guess.

## Out of scope

- Any tier or `category` change. The congressional-document hierarchy re-tier is a separate handoff.
- Candidate fields.
- `PROJECT.md`.

---

read docs/handoffs/2026-06-16-handoff-44-watchlist-hygiene-emdash.md and follow
