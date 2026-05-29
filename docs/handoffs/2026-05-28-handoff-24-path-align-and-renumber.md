# Handoff #24 — Path alignment, README sync, candidate-schema renumber

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-28-handoff-24-path-align-and-renumber.md`
**Numbering note:** filed as #23, but #23 was already occupied by this handoff itself, so the candidate-schema doc took #23 (older work sorts first, per this handoff's own tie-break rule) and this cleanup became **#24**.
**Branch:** continue on `feat/oge-278-candidate-schema` (do not open the PR until this lands)
**Type:** mechanical cleanup. No schema changes, no new candidates, no parser work.

## Why

The candidate-schema branch is correct but sits on three stale assumptions that should be fixed before the PR opens, so the first PR reflects the repo as it actually is:

1. `records.json` moved from root `data/` to `web/data/` (commit c374bcb). `data/candidates.json` is now split across two trees from the records it promotes into.
2. The README architecture block still describes the pre-`web/` layout.
3. This candidate-schema handoff was filed as "#20," colliding with the live evidence_refs #20 (`2026-05-21-handoff-20-apply-evidence-refs.md`). Two lineages, one number.

None of this touches the schema, the 5 Witkoff candidates, the taxonomy, or `raw_value` structure — all of that stands. This is moves and renames only.

## Tasks

### 1. Move candidates beside records

Move `data/candidates.json` → `web/data/candidates.json`, sitting next to `web/data/records.json`. Candidates and records are the same pipeline (pre- and post-promotion); they live in one tree. Update `collectors/oge_278/candidates.py` so its output path writes to `web/data/candidates.json`. Update any other reference to the old `data/candidates.json` path (grep the repo for it).

Use `git mv` so history follows the file. Confirm the moved JSON is byte-identical to the pre-move file — this is a move, not an edit.

### 2. Sync the README architecture block

The README's "Architecture (planned, not yet built)" tree still shows root `data/` and a `docs/`-based dashboard. Update it to match what's actually on disk now: the `web/` tree, `web/data/records.json`, `web/data/candidates.json`, and wherever the parser/collector files actually live. Describe the real layout, not the aspirational one. Don't invent paths — grep/`ls` first, then document what's there.

Leave the rest of the README alone (scope, defined terms, evidence hierarchy, etc. are all current).

### 3. Renumber the candidate-schema handoff out of the #20 collision

The handoff log is sequential-by-date across all lineages, not per-lineage. #20 is taken by evidence_refs. Renumber the OGE-278 candidate-schema handoff (the one currently at the OGE `#20` slot, `docs/handoffs/oge-278-record-schema.md`) to the next free integer in the global sequence: **#21-pre is taken, #22 is the SC-001-006 worksheet, so this becomes the OGE-278 candidate schema as a dated entry — file it as the next sequential handoff after #22.**

Concretely:
- `git mv docs/handoffs/oge-278-record-schema.md docs/handoffs/2026-05-28-handoff-23-oge-278-candidate-schema.md` (adjust the integer if a #23 already exists on disk — grep `docs/handoffs/` first and take the next free one; flag back if the sequence isn't what's assumed).
- Inside the renamed doc, change the title/number to match, and add a one-line note: lineage is OGE-278, numbering is global-sequential. Keep "OGE-278" as a tag in the body, never as the number.
- This handoff (#23-path-align) and the renamed candidate-schema doc are two separate files. If both want the same integer, this cleanup handoff takes the higher number — the candidate-schema work is older and should sort first by date/number.

If the on-disk handoff sequence doesn't match the assumption above (#20 evidence_refs, #22 worksheet, #23 free), **stop and report the actual sequence** rather than renumbering into another collision.

## Verify

- `web/data/candidates.json` exists, byte-identical to the old `data/candidates.json`; old path gone; no dangling references (grep clean).
- `candidates.py` writes to the new path; re-running the emitter reproduces the same 5 candidates at the new location.
- README architecture block matches `ls`-able reality.
- No two files in `docs/handoffs/` share a handoff number.
- `git log --follow` shows continuous history for both moved files.

## Commit

Single commit, mechanical: the two `git mv`s, the `candidates.py` path edit, the README block. Message in the existing convention, scoped as a path/numbering cleanup — make clear it changes no schema and no data content. Don't push, don't open the PR; report back so the three flag-back deferrals (certification field, collector stub wiring, the global renumber confirmation) can be logged before the branch goes up.
