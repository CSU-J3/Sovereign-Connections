# Handoff #45 — Tier congressional committee documents by type (PROJECT.md + catalog reconciliation)

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-45-congressional-doc-tier.md`
**Depends on:** #44 merged (it edited SC-007 label text; this edits SC-007 `category` values, different fields, rebase clean). Branch off `main` after #44 lands.
**Type:** docs (`PROJECT.md`) + data (`web/data/records.json`).

## What this does

Closes the PROJECT.md gap where congressional committee documents aren't explicitly tiered, and reconciles the catalog. SC-007's congressional entries sit at tier 1 while the equivalents in SC-002, SC-006, and SC-009 sit at tier 2. Testimony belongs at tier 1, a sworn primary record, but committee reports and record-resting letters are government synthesis, which is tier 2.

## Part 1: PROJECT.md amendment

In the evidence hierarchy, add explicit handling for congressional committee documents, tiered by type. The `congressional_document` `document_type` enum already exists: letter | report | hearing_transcript | testimony | referral.

- `testimony`, `hearing_transcript`: tier 1 (sworn or verbatim primary record). This makes the existing tier-1 "congressional testimony" line explicit and extends it to hearing transcripts.
- `report`, and `letter` or `referral` that rests on a traceable primary record: tier 2 (government work product synthesizing or resting on primary records, traceable to the underlying filings it cites).
- A committee statement that is position or opinion with no traceable underlying record: tier 4.

Match PROJECT.md's format and voice. If the hierarchy section carries rationale, note: a committee report characterizes evidence rather than being the underlying record, so it sits below the primary filings it cites; testimony earns tier 1 because it is sworn primary evidence.

## Part 2: Catalog reconciliation (`web/data/records.json`)

Scan every record for `congressional_document` primary_sources. For each, set `category` by `document_type` per the Part 1 rule:

- `testimony` / `hearing_transcript` → 1
- `report` → 2
- `letter` / `referral` → 2 if it rests on a traceable primary record (the fact it concerns is established elsewhere in the record or by a cited filing), else 4

Expected diff: SC-007's congressional entries move from 1 to 2. SC-002 (House Oversight "White House for Sale" report), SC-006 (Senate HSGAC/Finance report), and SC-009 (Maloney probe-launch letter, which rests on the documented PIF $2B flow) should already be at tier 2 and stay. Report the actual diff.

The SC-009 Maloney letter is a probe launch, an inquiry, but it rests on the documented $2B PIF to Affinity flow, so it is tier 2 under the "rests on a traceable primary record" test, not tier 4. The tier-4 case is reserved for pure-position statements with no underlying record, which the current catalog does not contain.

## Verify

- PROJECT.md hierarchy updated with the by-type rule.
- Every `congressional_document` `category` in records.json conforms to the rule.
- SC-007's congressional entries are now tier 2.
- No non-congressional source category changed anywhere.
- `candidates.json` and the watchlist are untouched.
- JSON valid.

## Commit

Single commit, PROJECT.md + records.json + this handoff. Suggested:

```
docs: tier congressional committee documents by type, reconcile SC-007 (#45)
```

Do not push unless asked.

## Flag back, do not decide

- Any `congressional_document` entry whose `document_type` is unclear, or any `letter`/`referral` where the tier-2-versus-4 test is genuinely ambiguous.
- Any record that changes tier beyond SC-007. I expect only SC-007 to move; surface anything else.

## Out of scope

- Candidate fields and the watchlist.
- The methodology Section 7 tightening.

---

read docs/handoffs/2026-06-16-handoff-45-congressional-doc-tier.md and follow
