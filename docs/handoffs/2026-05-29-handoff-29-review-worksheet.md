# Handoff #29 — Candidate review worksheet: surface the 162 unreviewed for human disposition

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-29-handoff-29-review-worksheet.md`
**Branch:** new branch off main (post-PR-#4 merge), e.g. `feat/review-worksheet`
**Type:** read-only scaffold. Generates a reviewable view of existing candidates. Does NOT make dispositions, does NOT modify `candidates.json`, does NOT change schema or records.

## Why

The deep-leaf re-run (#26) took the candidate set from 5 to 168. 162 sit at `unreviewed`. Until they're dispositioned, the pipeline feeds a queue nobody's working. This handoff builds the scaffold that makes Corey's review fast and durable; the dispositions themselves are human judgment (sovereign-adjacent or not is not a call Code can make) and get written back in a later handoff, keyed on `(part, entry_number)`.

This is the first review pass over the post-flatten set. The point is to see the real distribution before trusting any mechanical triage rule. So: surface everything in a reviewable order, do not pre-dispose anything.

## Scope

**In scope:** generate a human-reviewable worksheet of the 162 `unreviewed` candidates, with the fields needed to judge each, sorted so likely-interesting rows surface first.

**Explicitly NOT in scope:**
- Making, proposing, or writing any disposition. No `killed_out_of_scope`, no `hold`, no defaults. The worksheet carries an empty disposition column for Corey to fill.
- Modifying `web/data/candidates.json` or any record.
- Mechanical bucketing/triage rules that pre-dispose rows. (A later pass may add triage once the real distribution is known; not now.)
- The 6 already-dispositioned candidates (4 killed, 1 hold, 1 promoted) — exclude them from the worksheet, but note their existence in a summary line so the count reconciles to 168.

## Tasks

### 1. Generate the worksheet

Produce a worksheet at `docs/reviews/2026-05-29-oge278-witkoff-review.md` (create `docs/reviews/` if needed). One row per `unreviewed` candidate (162 rows). Markdown table, or a CSV at the same stem if 162 rows read better as CSV — Code's call on legibility, but it must be diff-friendly and human-editable.

Columns, per row:
- `CAND-###` (reference only — note in a header that dispositions will key on (part, entry_number), not this)
- `(part, entry_number)` — the stable identity
- entity name (`business_name`)
- `ancestry_path` (e.g. `41 > 41.8 > 41.8.1`)
- `rollup_value` (the nearest value-carrying ancestor, or own value if it has one)
- `descriptor` (the parenthetical — cryptocurrency, stablecoin, etc.; blank if none)
- foreign-signal flags present on the row (non-US corporate suffix like Ltd/L.P./GmbH, a foreign place-name in a sub-entry, an offshore share-class marker) — surfaced as short tags, not a judgment
- an empty `disposition` column
- an empty `reason / note` column

### 2. Sort so likely-interesting rows surface first

Order the 162 by a transparent, documented heuristic — NOT a disposition, just a sort so Corey's eye hits the candidates most likely to matter first. Suggested ordering, surface-to-bottom:
1. rows with a non-empty descriptor (crypto, stablecoin, fund-type markers)
2. rows with a foreign-signal flag (non-US suffix, foreign place-name, offshore marker)
3. rows with a high rollup_value
4. everything else (bank accounts, US index funds, plain holdings), in entry order

Document the sort key at the top of the worksheet so it's clear the order is convenience, not pre-judgment. A row low in the list is not "less likely to be killed" by Code's assertion — it's just where the eye goes last.

### 3. Summary header

Top of the worksheet, a short block:
- generated date, source filing, total candidates (168), unreviewed shown (162), already-dispositioned excluded (6: list them by (part, entry) and state)
- the sort key used
- a one-line reminder of the four states and that `killed_out_of_scope` requires a reason
- a pointer to `docs/references/collector-gap-finding-oge278.md` (the kill-disposition precedent) and `docs/references/wlf-research-target.md` (the promote precedent) so Corey reviews against the established bar

### 4. Make it regenerable

The worksheet is a snapshot. If candidates regenerate (another deep-leaf re-run, a new filing), the worksheet should be reproducible from current `candidates.json` by re-running whatever generates it. Prefer a small script (`collectors/oge_278/review_worksheet.py` or a doc-gen helper) over hand-assembly, so it's not stale the moment the data moves. Commit the generator with the worksheet.

## Verify

- Worksheet exists, 162 rows, every `unreviewed` candidate present exactly once; the 6 dispositioned ones excluded and accounted for in the header (162 + 6 = 168).
- Every row carries (part, entry_number), entity, ancestry_path, rollup_value, descriptor, foreign-signal tags, and empty disposition/reason columns.
- Sort key documented; WLF is NOT in the worksheet (it's promoted, not unreviewed) — confirm it's excluded.
- No change to `candidates.json`, records, or schema — `git diff` touches only `docs/reviews/` and the generator.
- Generator re-run reproduces the worksheet from current data.
- `tsc --noEmit` + `next build` still green from `web/` (should be untouched, but confirm nothing leaked).

## Commit

Worksheet + generator in one feature commit (docs/tooling). Open as a PR or commit to a branch for review — Code's call, but keep it off main until Corey's seen the worksheet, since the next step (writing dispositions back) depends on what the review finds. Report the row count and the top ~15 rows of the sorted worksheet in the summary so Corey can eyeball the surfacing before opening the file.

## Downstream (not this handoff)

Corey reviews the worksheet off-session, fills the disposition column. A later handoff reads the filled worksheet and writes the dispositions into `candidates.json` via the `(part, entry_number)`-keyed registry — the same mechanism #27 used, so a re-run can't orphan them. Cron wiring stays deferred until the review backlog is being worked, so the schedule isn't refilling an unworked queue.
