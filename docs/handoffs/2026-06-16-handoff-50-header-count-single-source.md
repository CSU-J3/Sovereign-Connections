# Handoff #50 — Single source of truth for the header "N records · M live" count

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-50-header-count-single-source.md`
**Branch:** off `main`.
**Numbering:** if #50 is already on disk, take the next free integer and flag back (per the #24 tie-break rule).
**Pairs with:** #49, which sets SC-008's soft-flag; this handoff's "live" rule consumes it. Order-independent: live reads 3 until #49 lands, 2 after. Both correct.
**Type:** web (shared header / count helper). No data edits.

## Why

The header status string "{N} records · {M} live · pre-launch" renders different values on different pages of the same dataset:

- `/` and `/record/[id]`: 8 records, 3 live.
- `/methodology`: 8 records, 2 live.
- `/swfs`: 7 records, 1 live.

The counts are hardcoded or computed per page and have frozen at different times (SWFs is the most stale). For a project whose premise is internal consistency, the count disagreeing with itself page to page is the most visible defect on the site. Fix: compute both numbers once from `records.json` and render the same string everywhere.

## Task

Read disk first; do not assume the component structure from this handoff.

1. Find where the status string is produced on each of the four page types (`/`, `/record/[id]`, `/methodology`, `/swfs`). Determine why they diverge: hardcoded literals, stale props, or different data sources. Report what you find before changing it.
2. Create or designate one helper that derives the counts from `web/data/records.json`, and have every page render from it. The string must be identical on all four pages.
3. Count rules:
   - records is the total number of records in `records.json`, all scopes (LIVE, COMP, LITIG, OOS). Currently 8.
   - live is the number of records whose scope is `LIVE` and which are not soft-flagged (the #49 field). That is 3 scope-LIVE records today, 2 after #49 flags SC-008. Read the soft-flag field from `types.ts` / the record shape. If #49 has not landed and no field exists yet, live is the count of scope `LIVE` (3), and the "minus soft-flagged" clause is a no-op that activates once #49 lands. Write the rule so it is correct in both states.
   - pre-launch is a static status string, unchanged.
4. While you are in `records.json` for the denominator: report whether an `SC-001` record exists in the file. The rendered list starts at SC-002 and SC-001 is not linked anywhere. This is a confirmation check for the count's denominator, not a fix. If SC-001 exists in data but is filtered from the list, surface the discrepancy; the count must match what the list renders. If it does not exist, the denominator is simply 8 and the numbering gap is a separate decision.

## Verify

- `/`, `/record/[id]`, `/methodology`, and `/swfs` all render the identical status string.
- The numbers are derived from `records.json`, not hardcoded on any page.
- records is the total record count; live is scope-LIVE-and-not-soft-flagged.
- Report states whether SC-001 is present in `records.json`.
- No data files edited. No em-dashes or banned words in any new copy.

## Commit

One branch off `main`, single commit. Suggested message:

```
web: single source of truth for header record/live counts (#50)
```

Commit this handoff with the work. Do not push unless asked.

## Flag back, do not decide

- If the four pages diverge because they read different data sources rather than hardcoded strings, report the architecture before unifying; there may be a reason two trees exist.
- The SC-001 numbering decision (renumber, restore, or changelog note) is a separate call, not part of this handoff. Just report presence or absence.

## Out of scope

- SC-008's soft-flag value (handoff #49).
- The SC-001 numbering fix itself.
- Any record content or schema change.

---

read docs/handoffs/2026-06-16-handoff-50-header-count-single-source.md and follow
