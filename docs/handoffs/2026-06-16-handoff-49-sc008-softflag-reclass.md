# Handoff #49 — Reclassify SC-008 as a soft-flagged watch entry; correct methodology PIA description

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-49-sc008-softflag-reclass.md`
**Branch:** off `main`.
**Numbering:** if #49 is already on disk, take the next free integer and flag back (per the #24 tie-break rule).
**Type:** data (`web/data/records.json`) + content (methodology page). Task 1 is schema-gated; Task 2 is independent and can land regardless.

## Why

SC-008 is logged as a headline LIVE record but does not meet the v2.0 inclusion test it is filed under. The record's own text states both disqualifiers: Witkoff Group is not a party to the Roosevelt MOU, and no PIA-source flow to a Witkoff entity is documented. Methodology condition (2) requires the connected business to receive sovereign or sovereign-adjacent money; condition (4) requires that flow to be sourced. Neither is present. The record is currently carried on "convergent interest at the role-and-portfolio level," which is a weaker basis than the stated rule.

Separately, the methodology page describes the Roosevelt's owner as "a Pakistani state-owned enterprise," while SC-008 documents that PIA was privatized in December 2025 with the Pakistani government holding only a minority stake. The two descriptions contradict each other, and the SOE description overstates the counterparty's sovereign character.

The methodology already defines the mechanism for this case: "Records that belong in the dataset but should not count toward headline totals carry a flag with a documented reason." SC-008 is a legitimate watch entry. Apply that flag rather than removing the record or stretching the rule.

## Decisions already made (Corey's call, recorded here)

1. SC-008 stays in the dataset and keeps scope `LIVE`. It is a current, active matter.
2. A soft-flag marks it as excluded from the headline "live" count, with a documented reason.
3. The record stays visible in the LIVE filter view; the flag is what signals its different status. See flag-back if you think soft-flagged records should drop out of the LIVE filter too.
4. The methodology PIA description is corrected to match the record.

## Task 1 — Soft-flag SC-008 (schema-gated)

This touches the record schema. Read the actual deployed types before writing anything. Do not draft the field shape from this handoff. Standing rule: schema against live `types.ts`, not against a summary.

1. Read `web/lib/types.ts` (the authoritative record interface) and the SC-008 object in `web/data/records.json`. Report:
   - Whether a record-level soft-flag / headline-exclusion field already exists. This is distinct from the convergent-interest flag, which elevates rather than excludes and is carried by SC-007.
   - The exact current shape of any existing flag field.
2. If a suitable field exists: set it on SC-008 with the reason text below.
3. If no suitable field exists: STOP and flag back with a minimal proposed field. Semantics: keeps the record visible, marks it excluded from the headline live count, carries a human-readable reason string. Do not add a new schema field without sign-off.

Reason text to store (verbatim):

> Logged as a v2.0 covered-intermediary watch entry. As of February 2026, Witkoff Group is not a party to the Roosevelt Hotel MOU and no PIA-source flow to a Witkoff entity is documented; post-privatization PIA Investments carries only a minority Pakistani-government stake. Promotes to a headline record if a PIA-source flow to a Witkoff entity, or a Witkoff Group contractual position in the redevelopment, is documented.

Do not change SC-008's scope, frameworks, evidence categories, primary_sources, or any other field. Flag only.

## Task 2 — Correct the methodology PIA description (independent, can land regardless)

1. Grep the methodology page source for every instance of "state-owned enterprise" and "Pakistan International Airlines". The known instance, in the v2.0 covered-intermediaries section, reads:

   > an asset owned by Pakistan International Airlines Investment Limited, a Pakistani state-owned enterprise.

2. Replace the "a Pakistani state-owned enterprise" characterization with language consistent with SC-008's privatization facts. Draft:

   > an asset owned by Pakistan International Airlines Investment Limited. PIA was privatized in December 2025 under Pakistan's IMF Extended Fund Facility program; the Pakistani government retains a minority stake, which makes the counterparty sovereign-adjacent rather than a wholly state-owned enterprise.

   Match the surrounding sentence rhythm and house style (no em-dashes, analyst voice). Keep the precise entity name "Pakistan International Airlines Investment Limited."
3. If the grep finds additional SOE references to PIA elsewhere on the page, correct them the same way and list them in the report.

## Verify

- `types.ts` and SC-008's on-disk shape reported before any edit.
- If the flag was set: SC-008 carries the soft-flag with the exact reason text; no other SC-008 field changed; JSON valid.
- If the flag needs a new field: nothing written to `records.json`; proposed field flagged for sign-off.
- Methodology page no longer calls post-2025 PIA a flat state-owned enterprise; the corrected sentence reads cleanly and matches SC-008.
- No em-dashes introduced. No banned words.

## Commit

One branch off `main`. If both tasks land, a single commit is fine; if Task 1 flags back, commit Task 2 alone. Suggested message:

```
data+content: soft-flag SC-008 as watch entry; correct PIA SOE description (#49)
```

Commit this handoff with the work. Do not push unless asked.

## Flag back, do not decide

- Whether soft-flagged records should also be excluded from the LIVE scope filter view, not only the headline count. Recommendation: keep SC-008 in the LIVE view with a visible flag marker. Surface a different preference if you have one.
- The field shape, if a new one is needed. Sign-off required before writing data.
- Optional: SC-008's record text says the Roosevelt is "owned by Pakistan International Airlines" while the methodology says "Pakistan International Airlines Investment Limited" (the subsidiary that holds the asset). Align if wanted; not required here.

## Out of scope

- The headline count computation itself. Handoff #50 unifies it and consumes this flag.
- SC-007's convergent-interest flag.
- SC-008's evidence categories and sources (correct as set by #45/#47).
- Any other record.

---

read docs/handoffs/2026-06-16-handoff-49-sc008-softflag-reclass.md and follow
