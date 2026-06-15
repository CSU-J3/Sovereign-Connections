# Handoff #36 — ADV/IAPD collector: writer unification + package to runnable parity

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-14-handoff-36-adv-iapd-writer-unification-parity.md`
**Lineage:** ADV/IAPD. Global-sequential numbering; #35 was the build, so this is #36.
**Depends on:** Handoff #35 (ingest + candidates), which lands via PR #12. Branch off `main` once both PR #11 and PR #12 have merged, since this touches the OGE collector on main and the ADV collector from #35. If they haven't merged, branch off `feat/adv-iapd-collector` and say so in the report.
**Type:** build. Refactors both collectors' write paths and completes the `collectors/adv_iapd/` package. Extends no candidate data (count stays 171); no `records.json` or `web/lib/types.ts` changes.

## What this builds

Two things, both flagged in #35.

The headline is the coexistence fix. The OGE `write_candidates` still overwrites all of `candidates.json`, so running `python -m collectors.oge_278.collector` standalone would drop CAND-169/170/171. The ADV writer is already merge-aware (it appends after the OGE rows idempotently), so the fix is to give both collectors a shared, source-scoped writer: each regenerates only its own source's rows and preserves every sibling row untouched.

The second is parity. The ADV package is `ingest.py` plus `candidates.py`. This adds the wrapper that runs it end to end, its own regression guard, and a seed config, so it's a runnable, guarded collector like `collectors/oge_278/`.

## Scope guardrails (apply, don't re-litigate)

- Global sequential `CAND-###` IDs, no semantics in the ID, provenance in `source_filing`. This handoff does not change the ID scheme. Existing IDs (OGE 1-168, ADV 169-171) stay put.
- Conservative over-emission and the seeded-not-universal model stand. The seed is still Affinity (CRD 315482) only.
- `connected_businesses.json` registry still deferred; `business_id: null`.
- The covered-person candidate field is out of scope here. It's #37.

## What Code needs to do

### Step 1: Shared, source-scoped writer

Extract one merge-aware writer both collectors call, parameterized by source. Its contract:

- Read the current `web/data/candidates.json`.
- Drop only the rows whose `source_filing.source` matches the calling collector.
- Regenerate that collector's rows, preserving the existing `CAND-###` for any row that still maps to the same source entity, and assigning the next free global ID only to genuinely new rows.
- Write back the regenerated own-rows plus every preserved sibling row, in stable order.

The match key that decides "same source entity, keep its ID" needs to be deterministic (source plus filing plus the entity identifier). If the right key isn't obvious for one of the collectors, flag it rather than guessing, because a wrong key either renumbers existing candidates or duplicates them.

### Step 2: OGE adopts the shared writer

Replace OGE's whole-file overwrite with a call to the shared writer scoped to `oge_278`. After this, running the OGE collector preserves the ADV rows and keeps OGE's own IDs (1-168) stable on re-run.

The OGE regression guard already slices to OGE rows (the #35 minimal fix). Leave that behavior; it's correct.

### Step 3: ADV package to parity

- `collectors/adv_iapd/collector.py`: the wrapper, runnable as `python -m collectors.adv_iapd.collector`. It reads the seed, runs `ingest` then `candidates` for each seeded CRD, and writes through the shared writer scoped to `adv_iapd`.
- `collectors/adv_iapd/seed.json` (or a module constant if that matches the OGE pattern better): the seed list of covered-person-connected adviser CRDs. One entry for now, CRD 315482. This is the ADV analog of OGE's `discover.py`; ADV is seeded, not discovered, so a separate `discover.py` isn't required unless parity surfaces a reason. Flag if it does.
- `collectors/adv_iapd/regression_guard.py`: the ADV-slice guard, mirroring the OGE-slice guard. It checks the ADV rows regenerate byte-identically from the committed Affinity sample, so CI catches drift in the ADV slice the way it does for OGE.

A review worksheet is premature at three candidates; skip it until the seed list grows.

### Step 4: Verify coexistence and idempotency

Concrete checks, all must pass:

- Run `python -m collectors.oge_278.collector`, then confirm `candidates.json` still holds CAND-169/170/171.
- Run `python -m collectors.adv_iapd.collector`, then confirm CAND-001 through 168 survive.
- Run each collector twice in a row; the second run produces a zero diff.
- 171 candidates total, IDs 1-171 with no gaps, valid JSON.
- Both regression guards pass.

### Step 5: Document rollup_value per source

Add a short note (in the discovery doc's schema section or a `docs/` schema note, wherever the candidate schema is described) stating what `rollup_value` carries per source type: the OGE meaning, and the ADV reuse for firm-level Item 5 totals as the concentration denominator. This closes the implicit-reuse flag from #35.

### Step 6: Commit

Single commit: the shared writer, the OGE writer change, the ADV `collector.py` / `seed` / `regression_guard.py`, the rollup_value note, and this handoff doc. Match the commit-message convention. Don't push unless asked.

## Flag back, don't decide

- The stable match key for the shared writer, if it isn't clean for either collector.
- Whether the shared writer lives in a new shared module and where (e.g. `collectors/common/`), versus a helper imported from one side.
- Any OGE behavior change the refactor forces beyond the write path.
- Any parity gap that argues for more than the wrapper, seed, and guard.

## What this doesn't do

- Doesn't add the covered-person field. That's #37, including how OGE populates it (its filer already is the covered person) for cross-collector consistency.
- Doesn't change the ID scheme. Global sequential stays.
- Doesn't expand the seed beyond Affinity.
- Doesn't touch `records.json` or `web/lib/types.ts`.

## After this lands

- #37: the covered-person candidate field, fed from an enriched seed (CRD plus covered person) on the ADV side and from `filer` on the OGE side, with the cross-collector consistency decision.
- Covered-adviser inventory to grow the seed list, derived from the covered-persons definition in PROJECT.md.
- The `form_adv` PrimarySource variant on the records layer, plus the three schema sign-offs pending from May 21, for when ADV candidates get promoted to SC-### records.

---

read docs/handoffs/2026-06-14-handoff-36-adv-iapd-writer-unification-parity.md and follow
