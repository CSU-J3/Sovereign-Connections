# Handoff #48 — PrimarySource union validator in CI

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-48-primarysource-validator.md`
**Depends on:** nothing blocking. Branch off `main`.
**Type:** tooling / CI (a validator script plus CI wiring). No data change.

## What this does

Adds a CI check that validates every `primary_sources` entry in `web/data/records.json` and `web/data/sovereign_entities.json` against the `PrimarySource` union in `web/lib/types.ts`, failing on a malformed source. Closes the gap surfaced in #47: there is no automated assertion of the data file against the union. The TS typecheck does not assert the JSON data, and no JSON validator exists, so the #47 retype relied on a one-off manual check.

## Confirm first (decides scope)

The README's file map is stale (it calls the collectors "stubs" and `.github/workflows` "empty," neither of which matches shipped work). Read disk, not the README. Confirm whether the regression guard is a PR-gating workflow or runs another way. If there is an existing CI workflow, add this as a sibling check. If there is genuinely no PR-gating CI yet, this validator stands up the first one, which is a larger lift; flag that before building so the scope is a deliberate call, not a surprise.

## Approach

Recommended: a Python validator, matching the regression guard's language and wiring. The Python side has no `package.json` or Node toolchain (per the README), and the guard is Python, so this adds no new toolchain. Locate the regression-guard workflow and script on disk and mirror its structure: same fail mechanism, same trigger model, ideally a sibling step so records validation and the tally guard run together.

Why not a typed `tsc` assertion: importing the JSON and asserting it against the union does not compile even for valid data, because TS widens JSON string fields to `string`, which is not assignable to the literal `type` discriminants. Validate at runtime, not via `tsc`.

Single source of truth: `types.ts` defines the union; the validator encodes the same rules below. Adding or changing a variant means updating both. Put that note at the top of the validator, and add a one-line pointer to the validator in the `PrimarySource` comment in `types.ts`.

Node/zod in `web/` is an acceptable alternative if you'd rather keep the schema in the TS toolchain; the rules below are language-agnostic. Flag it if you take that path.

## Validation rules (from `web/lib/types.ts`, current)

Base fields on every source: `label` (non-empty string, required), `category` (integer 1-5, required), `url` (string, optional), `retrieved_at` (string, optional).

Discriminant: `type` (optional). If absent, the source is the generic shape and only base fields are allowed. If present, it must be one of the values below and carry that variant's required fields.

- (no `type`) → generic. Base fields only.
- `oge_278e` → requires `filing_type` in {`new_entrant`, `annual`, `amendment`, `termination`} and `certification_status` in {`filer_signed_only`, `ethics_certified`, `oge_certified`, `amended_post_certification`}. Optional: `parsed_paths` (string[]), `entry_paths` (string[]).
- `ethics_agreement` → no extra fields.
- `press_disclosure` → no extra fields.
- `court_filing` → no extra fields.
- `congressional_document` → requires `document_type` in {`letter`, `report`, `hearing_transcript`, `testimony`, `referral`}. Optional: `chamber_or_committee` (string), `document_date` (string).
- `sec_filing` → no extra fields.
- `advocacy_report` → requires `organization` (string). Optional: `published_at` (string).
- `corporate_registration` → requires `registration_type` in {`company_registry`, `trademark`, `beneficial_ownership`}. Optional: `registry`, `jurisdiction`, `identifier`, `filed_at` (all strings).
- `form_adv` → requires `crd` (string). Optional: `sec_number`, `filing_id`, `filing_date`, `table`, `fund_id` (all strings).
- `sanctions_designation` → no extra fields (reserved).
- `foia_release` → no extra fields (reserved).

## Checks per source

1. `label` is a non-empty string; `category` is an integer in 1-5.
2. `url` and `retrieved_at`, if present, are strings.
3. If `type` is absent, only base fields are present.
4. If `type` is present: it is a known value; the variant's required fields are present with valid values (enum fields checked against their allowed sets); optional fields, if present, are the right type; and no unknown field appears beyond the variant's allowed set (this catches a misnamed field like `document_typ`). Starting unknown-field as a warning and promoting to error once the data is clean is fine if you prefer.

## Data in scope

`web/data/records.json` (`SovereignRecord[]`) and `web/data/sovereign_entities.json` (`SovereignEntity[]`): every `primary_sources` array. `web/data/candidates.json` uses a different shape (the ADV candidate `source_filing`) and is out of scope here; note it as a possible parallel check later.

## Verify

- The validator passes on the current post-#47 data.
- Introduce a deliberate break in a scratch copy (for example an `oge_278e` missing `certification_status`, or an invalid `document_type`) and confirm the validator fails; then remove the break.
- It is wired into CI the same way as the regression guard, and a malformed source fails the check.

## Commit

The validator script, the CI change, the one-line `types.ts` comment pointer, and this handoff. Suggested:

```
ci: validate primary_sources against the PrimarySource union (#48)
```

Do not push unless asked.

## Flag back, do not decide

- The exact location and structure of the regression-guard files (disk is authoritative; the README map is stale).
- If the guard runs only on a cron schedule rather than on PRs: a PR-triggered check is more useful here, but match the project's model and flag if a new trigger is warranted.
- If Node/zod in `web/` is preferred over Python.
- Whether to extend coverage to `candidates.json` in a follow-up.

## Out of scope

- `candidates.json` shape.
- The `evidence_category`-versus-source-category consistency rule (separate concern).
- Any data change.

---

read docs/handoffs/2026-06-16-handoff-48-primarysource-validator.md and follow
