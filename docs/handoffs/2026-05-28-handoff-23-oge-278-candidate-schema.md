# Handoff #23 — OGE 278 Candidate Record Schema

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-28-handoff-23-oge-278-candidate-schema.md`
**Lineage:** OGE-278 (a body tag, not the number). Handoff numbers are global-sequential across all lineages, not per-lineage. This work was originally filed as "#20," colliding with the evidence_refs #20; renumbered to **#23** by Handoff #24 (path-align). "OGE-278" stays a tag only — never the number.
**Depends on:** OGE 278 parser (`collectors/oge_278_collector.py`, parse stage done in prior handoff)
**Blocks:** `web/data/candidates.json` population, OGE 278 collector wrapper

> **Path note (Handoff #24, 2026-05-28):** candidate records now live at
> `web/data/candidates.json` (beside `web/data/records.json`) and records at
> `web/data/records.json`. Operational path references below were updated to
> match. The one exception is the "Divergences" note, which deliberately records
> the pre-move state as it was found.

## Goal

Define the candidate record schema that sits between raw OGE 278 parser output and promoted `SC-###` records in `web/data/records.json`, then validate it by emitting the first 4-6 candidates from Witkoff's already-parsed OGE 278 filing into `web/data/candidates.json`. Candidates are pre-promotion: parsed financial-disclosure rows that *might* describe a sovereign-source connection, before any human research has confirmed scope.

Schema design plus one worked pass. No research. No invented dockets, dates, URLs, or sponsor identities. Every field on every emitted candidate traces to a row that exists in the parsed Witkoff output. If a field can't be filled from parsed data, leave it null — do not infer it.

This is a Python/JSON repo (no TypeScript). The schema is a JSON shape, documented in this handoff and enforced by the collector that writes it — not a TS interface. Match the JSON conventions already used in `data/sovereign_entities.json` and `web/data/records.json` (field naming, ID style, how primary sources are referenced). Read those two files first and align to them; don't invent a parallel style.

## Three decisions already made (apply, don't re-litigate)

1. **Sequential candidate IDs.** `CAND-001`, `CAND-002`, ... zero-padded to three digits, assigned in parse order. No semantics in the ID. Provenance lives in a `source_filing` field; the ID is just a stable handle.

2. **Conservative collector-level filtering.** The collector over-emits. Any disclosure row that *could* describe a foreign-source payment, position, or asset gets a candidate — err toward emitting. Filtering to actual scope happens at promotion (`CAND-###` → `SC-###`), a separate human step, not here. Do not drop rows at collection because they look out-of-scope; that judgment isn't the collector's to make.

3. **`connected_businesses.json` registry deferred.** Candidates carry the connected-business name as a freeform string, not a foreign key into a registry that doesn't exist yet (`data/connected_businesses.json` is listed in the planned architecture but not built). **One refinement:** include a nullable `business_id` slot alongside `business_name`. It stays null on every candidate this handoff emits. It exists so that when the registry is designed later — once promotion patterns reveal the real deduplication shape (spelling variants, parent/subsidiary collisions, the Affinity/Witkoff entity overlap) — backfilling IDs doesn't require touching every record. Add the slot; leave it null.

## Schema to define

`web/data/candidates.json` is an array of candidate objects. Document the shape in this handoff and align field-naming to the existing `data/` JSON files. At minimum each candidate carries:

- `id` — `CAND-###`, sequential, parse order
- `source_filing` — provenance pointer back to the parser output for this filing. Use whatever the parser already writes as its output identifier/path; if the parser doesn't currently emit a stable pointer, that's a flag-back, not an invention (see below).
- `filer` — the OGE 278 filer name exactly as it appears in the parsed output
- `business_name` — freeform string, the connected business / entity / sponsor as it appears in the disclosure row
- `business_id` — nullable, always null this pass (decision 3)
- `disclosure_type` — which kind of 278 line this is (position, asset, income, agreement, gift, etc.), drawn from the parsed row's section, not inferred
- `raw_value` — the value/amount/description string exactly as parsed
- `scope_hypothesis` — short freeform note on *why this row could be sovereign-source*, phrased as a hypothesis to research, never a finding. E.g. "filer reports consulting income from entity with possible Gulf SWF parent — unverified," not "SWF-connected."
- `promotion_status` — string enum, defaults to `unreviewed`. Reserved values: `promoted`, `excluded`, `needs_research`. This pass emits everything as `unreviewed`.

If the parsed 278 carries a certification field (`filing_type` / `certification_status` from #17's discovery), attach it under `source_filing` rather than duplicating it on the candidate.

## Worked pass: Witkoff

Run the schema over the parsed Witkoff OGE 278 output the parser already produced. Emit 4-6 candidates into `web/data/candidates.json`. Constraints:

- Every emitted candidate's `raw_value`, `business_name`, `filer`, and `disclosure_type` is a verbatim or near-verbatim lift from a row that exists in the parsed file. If you're typing a value that isn't in the parse, stop — that's the invented-data failure this tracker exists to prevent.
- `scope_hypothesis` is the only freeform field. Keep each one hedged, pointing at what research would confirm. Never assert a sovereign connection.
- All emit at `promotion_status: "unreviewed"`, `business_id: null`.
- If conservative filtering yields fewer than 4 candidate-worthy rows, emit what's there and note the count — do not pad to hit 4.

If you can't locate the parsed Witkoff output in the repo, stop and flag it rather than re-running or reconstructing the parse — the parse stage was a prior handoff and its output location should be known, not guessed.

## Verify before reporting back

- `web/data/candidates.json` is valid JSON and every object carries the required fields.
- Every candidate ID is sequential from `CAND-001`, no gaps.
- Every `business_id` is null. Every `promotion_status` is `"unreviewed"`.
- Spot-check 2 candidates back to their source rows in the parsed Witkoff output — confirm `raw_value` and `business_name` match the parse, not a paraphrase that drifted.
- No candidate `scope_hypothesis` states a sovereign connection as fact. Flag any that read as findings.

## Flag back, don't decide

- If the 278 sections don't map cleanly to a `disclosure_type` set, surface the mismatch and propose the taxonomy — don't force rows into ill-fitting types.
- If the parser doesn't emit a stable `source_filing` pointer, say so and propose the smallest addition that gives candidates traceable provenance; don't fabricate a path.
- If the existing `data/` JSON files use a field-naming or ID convention that conflicts with anything above, follow the repo and note the divergence.

## Commit

Single commit: the schema documentation (this handoff in `docs/handoffs/`) + `web/data/candidates.json` with the Witkoff worked pass + any collector changes needed to emit it. Match the existing commit-message convention. Don't push unless asked.

---

# Schema as built (2026-05-28)

`web/data/candidates.json` is a JSON array of candidate objects. Each is emitted by
`collectors/oge_278/candidates.py`, which reads the parsed part files
(`data/samples/witkoff-oge278-2025-08-13-part{2,5,6}.json`) and copies the
verbatim fields directly from the parse — they are never retyped, so they cannot
drift. The single hand-authored field is `scope_hypothesis`.

```jsonc
{
  "id": "CAND-001",                       // sequential, parse order, zero-padded
  "source_filing": {                      // provenance pointer back to the parse
    "source_pdf":   "data/samples/witkoff-oge278-2025-08-13.pdf",
    "parsed_file":  "data/samples/witkoff-oge278-2025-08-13-part2.json",
    "part":         "2. Filer's Employment Assets & Income and Retirement Accounts",
    "report_type":  "New Entrant Report", // closest thing to a certification field (see flag-back)
    "form":         "OGE Form 278e (Updated 08/2024)",
    "entry_number": "1"                   // addresses the exact parsed row (dotted children allowed)
  },
  "filer":          "Witkoff, Steven C",  // verbatim from the parsed part doc
  "business_name":  "The Witkoff Group LLC (real estate management company)", // verbatim entity_name
  "business_id":    null,                 // reserved registry slot; null this pass (decision 3)
  "disclosure_type":"filer_employment_asset", // from the part, not inferred (taxonomy below)
  "raw_value": {                          // verbatim parsed value cluster (divergence below)
    "value_range":  "Over $50,000,000",
    "income_type":  "Proceeds from the sale of an interest in the company as part of divestiture planning",
    "income_range": "$120,000,000"
  },
  "scope_hypothesis": "...hedged research prompt, never a finding...",
  "promotion_status": "unreviewed"        // enum; reserved: promoted | excluded | needs_research
}
```

## `disclosure_type` taxonomy (flag-back resolved)

The handoff's example set (`position` / `asset` / `income` / `agreement` /
`gift`) does **not** map cleanly: the parser only covers OGE 278e Parts 2, 5, and
6, which are **all asset-&-income sections** (see `docs/collectors/oge-278-parser.md`).
Forcing them into that set would collapse the filer/spouse/other distinction and
invent `position`/`agreement`/`gift` types for which no parsed rows exist.
Adopted taxonomy, keyed to the parsed part (not inferred from the row):

| `disclosure_type`         | OGE 278e Part                                                  |
|---------------------------|----------------------------------------------------------------|
| `filer_employment_asset`  | Part 2 — Filer's Employment Assets & Income and Retirement Accounts |
| `spouse_employment_asset` | Part 5 — Spouse's Employment Assets & Income and Retirement Accounts |
| `other_asset_income`      | Part 6 — Other Assets and Income                               |

When Part 1 (positions), Part 3 (agreements), Part 4 (compensation sources), or
Part 9 (gifts) get parsed, extend this set — don't retrofit the asset rows.

## Worked pass: Witkoff — 5 candidates

Conservative over-emission (decision 2) over the parsed Witkoff filing yielded
**5** candidate-worthy rows (within the 4–6 target; not padded):

| ID | Part | Entry | Business name | Why it *could* touch a foreign source |
|----|------|-------|---------------|----------------------------------------|
| CAND-001 | 2 | 1   | The Witkoff Group LLC | $120M divestiture proceeds; acquirer not printed on the 278e |
| CAND-002 | 6 | 1   | M&A Management Company Ltd | `Ltd` form + yacht holding — possible non-US domicile |
| CAND-003 | 6 | 2   | Sweet Tuna Boat Ltd | same `Ltd` yacht-holding pattern, $1M–$5M |
| CAND-004 | 6 | 7   | Silverpeak Legacy Partners III, L.P. | sub-assets in Marseille, France (7.2) and Mumbai, India (7.3) |
| CAND-005 | 6 | 9.1 | Optima STAR Fund - Long-Only - Class B | offshore-style fund share class held in a brokerage account |

Part 5 (spouse) yielded **no** candidate — its 9 rows are US REITs, a US bank
cash position, and a US Treasury fund, none of which read as foreign-source even
under conservative emission.

Validation run (`collectors/oge_278/candidates.py` + an assertion pass) confirms:
valid JSON; IDs sequential `CAND-001`…`CAND-005` with no gaps; every
`business_id` is `null` and every `promotion_status` is `"unreviewed"`; every
`filer` / `business_name` / `raw_value` field byte-matches the source parsed row;
no `scope_hypothesis` asserts a sovereign connection as fact.

## Divergences from the handoff (followed the repo, noting it)

1. **Root `data/records.json` no longer exists.** It was removed at root (commit
   `c374bcb`, "remove stale root data/records.json") and now lives at
   **`web/data/records.json`**. Conventions were aligned to that file:
   snake_case fields, `SC-###` IDs, `primary_sources` as an array of
   `{label, url?, category:int}`.
2. **Root `data/candidates.json` and `data/connected_businesses.json` already
   existed** as empty arrays (`[]`) when this work started, where the handoff
   treated both as not-yet built. `candidates.json` was populated and then
   **moved to `web/data/candidates.json` by Handoff #24** (it sits beside
   records); `connected_businesses.json` stays empty at root `data/` per
   decision 3.
3. **`raw_value` is a structured object, not a single string.** The handoff
   phrased it as "the value/amount/description string." A 278e row carries three
   distinct printed value fields (`value_range`, `income_type`, `income_range`);
   collapsing them into one string would either drop data or require a
   hand-built join — exactly the drift this tracker guards against. The object
   copies each field verbatim. Easy to flatten later if a string is preferred.

## Flag-backs (decide upstream)

- **No certification field in the parser output.** The parsed part docs carry
  `report_type` ("New Entrant Report") and `form`, but **no**
  `certification_status` / `filing_type` (the #17 discovery fields). The 278e
  certification/ethics-officer signoff lives on the cover page, which the parser
  does not read. `report_type` + `form` are attached under `source_filing` as
  the closest available provenance. Smallest fix: have the parser extract the
  cover-page certification block into the part-doc header, then surface it here.
- **`oge_278_collector.py` is still a stub** (`NotImplementedError`). The worked
  pass is emitted by the new `collectors/oge_278/candidates.py`, which reads the
  already-parsed part files. Wiring the stub collector to drive
  parse → candidate emission end-to-end is its own handoff.
- **Handoff-number collision — RESOLVED by Handoff #24.** This doc was
  originally labeled "Handoff #20," colliding with the `evidence_refs` #20
  (`2026-05-21-handoff-20-apply-evidence-refs.md`, since superseded by #21).
  Handoff numbering is **global-sequential across all lineages**, so this
  candidate-schema work was renumbered to **#23** and the path-align cleanup
  itself took **#24**. The parser doc (`docs/collectors/oge-278-parser.md`) still
  refers to "Handoff #20" for this work and should be updated to "#23" on its
  next edit (a stale cross-reference, not a blocker).

## Schema extension (Handoff #26 — deep-leaf flatten)

The emitter was changed from a curated selection of specific rows to a full
tree walk (Gap 1 fix, `collectors/oge_278/candidates.py`). It now emits every
node that is **either a leaf entity or carries its own value/income**, which
surfaces deep holdings whose own value is N/A because it rolls up to a parent —
the case that missed World Liberty Financial (`41.8.1`). Three fields were added
(the canonical shape is the module docstring):

- `source_filing.ancestry_path` — full dotted chain root → this node, e.g.
  `"41 > 41.8 > 41.8.1"`. Lets review trace tree position.
- `rollup_value` — nullable object pointing at the nearest value/income-carrying
  ancestor (`entry_number`, `entity_name`, the three value fields), so a leaf
  with N/A own-value shows where its dollar figure lives. Never fabricated onto
  the leaf; `raw_value` stays the row's own (possibly all-null) parse.
- `descriptor` — nullable parenthetical lifted verbatim from `business_name`
  (e.g. `"cryptocurrency"`, `"stablecoin"`). A weak scope signal passed through,
  **not** filtered on at collection (hard-coding "crypto = interesting" is the
  brittle signal-keying that missed WLF in the first place).

`scope_hypothesis` is now `null` on every mechanically-emitted candidate except
the original Handoff #23 worked rows, whose hedged prompts are preserved via a
`(part, entry_number)`-keyed override. The Witkoff re-run yields **168**
candidates (part2 4, part5 8, part6 156).
