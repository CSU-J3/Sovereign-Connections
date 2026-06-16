# Handoff #40 — repoint the Affinity methodology walk from retired SC-001 to SC-009

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-40-walk-repoint-sc009.md`
**Depends on:** Handoff #39 (SC-001 retired into SC-009). Branch off the #39 branch `feat/evidence-backfill-slice-1` if it has not merged yet, so the retirement and this repoint land together; otherwise branch off `main` and say so.
**Type:** UI config. Edits `web/lib/constants.ts` only. No data change, no schema change.

## What this does

Handoff #39 removed SC-001 but scoped UI out, so `web/lib/constants.ts` still lists SC-001 in two places: the `RECORDS_WITH_WALK` set and a `WALK_PROMPTS` entry. That is now a reference to a removed record ID.

The walk set is the methodology-teaching trio: SC-001 was the inclusion exemplar (a real sovereign source caught by the definition), SC-002 is the framework case, SC-006 is the exclusion case. Dropping SC-001 outright would leave the trio with no inclusion exemplar. SC-009 is the better inclusion exemplar in any case, because its sovereign-wealth-fund capital is disclosed by category in the ADV itself, and the existing prompt already reads "the Affinity Partners record," which is SC-009 now. So repoint, do not drop.

## What Code needs to do

### Step 1: Repoint the walk set

In `web/lib/constants.ts`, line 79, change the `RECORDS_WITH_WALK` set so the Affinity slot points at SC-009 instead of SC-001:

```
const RECORDS_WITH_WALK = new Set(["SC-001", "SC-002", "SC-006"]);
```

becomes

```
const RECORDS_WITH_WALK = new Set(["SC-009", "SC-002", "SC-006"]);
```

### Step 2: Rekey the walk prompt

In the same file, rekey the `WALK_PROMPTS` entry from `"SC-001"` to `"SC-009"`. Keep the prompt text exactly as it is:

```
"SC-009":
  "Walk the sovereign-adjacent definition through the Affinity Partners record using PROJECT.md categories.",
```

Leave the SC-002 and SC-006 entries unchanged.

### Step 3: Verify before reporting back

- `web/lib/constants.ts` typechecks clean.
- `hasWalkButton("SC-009")` returns true; `hasWalkButton("SC-001")` returns false.
- `WALK_PROMPTS["SC-009"]` resolves; `WALK_PROMPTS["SC-001"]` is undefined.
- Grep `web/lib/constants.ts` for `SC-001`: no hits remain.
- Repo-wide grep for `SC-001` returns only historical handoff, triage, draft, and reference docs, plus this handoff. No live source or data file references SC-001.
- `next build` clean.

### Step 4: Commit

Single commit, `web/lib/constants.ts` plus this handoff doc. Suggested message:

```
fix(ui): repoint Affinity methodology walk from retired SC-001 to SC-009 (#40)
```

Do not push unless asked.

## Flag back, do not decide

- The prompt text is kept verbatim because it already names "the Affinity Partners record," which fits SC-009. If a prompt that leans into the ADV and the sovereign-wealth-fund-by-category angle is wanted, that is a one-line content tweak, not a mechanical step. Surface it; do not rewrite the prompt without a call.

## Out of scope

- Data, schema, and records changes.
- The pre-existing em-dash cleanup in SC-007 and SC-009 labels and the SC-009 summary. Separate hygiene pass.
- SC-002, SC-003, SC-006 sourcing (slice 2).

---

read docs/handoffs/2026-06-16-handoff-40-walk-repoint-sc009.md and follow
