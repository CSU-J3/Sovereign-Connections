# Handoff #32 — Promote W-002 to SC-008 (Kushner / Affinity), stage 3 catalog candidates

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-05-30-handoff-32-sc-008-affinity.md`
**Branch:** new branch off main, e.g. `feat/sc-008-affinity`
**Type:** record + data. New SC record, watchlist state update, catalog candidates staged (not added). No parser/schema changes.

## Why

W-002 (Jared Kushner / Affinity Partners) is evaluated and ready. The primary record is SEC Form ADV for **A Fin Management LLC** (firm CRD 315482), not an OGE 278e — the first `adv`-sourced record in the tracker. Evidence base and drift guards are fully worked in `docs/references/sc-008-affinity-research-target.md`. This handoff writes the record, links the watchlist, and stages (does not add) the sovereign-vehicle catalog candidates the record surfaces.

This is a **separate subject from SC-007** — different principal, different sovereign funds, different vehicle, different source type. New record, do not fold into SC-007.

## Tasks

### 1. Create SC-008 in `records.json`

- Next free `SC-###` (SC-008 if 007 is the last). Scope LIVE. Subject: Jared Kushner / Affinity Partners (A Fin Management LLC).
- Summary documents **a financial relationship at scale**, not a causal claim: a vehicle wholly owned by a former senior official (Kushner) manages $6,160,297,411 (as of 2025-12-31) on a 2% management fee + up to 20% carry, and discloses sovereign-wealth-fund capital among its investors.
- `primary_sources` — keep the two evidentiary tiers explicit (the schema's source typing should carry this; if it doesn't, note in the record):
  - **Primary (Affinity's own ADV):** sole owner Kushner / DE LLC 2021 (Item 4.A); AUM $6,160,297,411 @ 2025-12-31 (Item 4.E); 2%+20% fee structure (Items 5.A, 6); investor categories include "sovereign wealth funds" (Item 7); the six-fund Schedule D AUM/beneficial-owner breakdown (Part 1A, 2026-03). Cite ADV CRD 315482, brochure dated 2026-03-22.
  - **Secondary (named funds, labeled as such):** PIF ~$2B anchor 2021 with the PIF screening-committee objection overruled by MBS (House Oversight 2022, Wyden 2024, NYT); QIA + Lunate ~$1.5B 2024 (Reuters, Kushner podcast). These name the specific sovereign vehicles the ADV discloses only by category.

### 2. Write the drift guards into the record (load-bearing)

From the reference doc, non-negotiable:
- **No payback / causation claim.** The oversight framing (investment as payback for Kushner's official acts) is drift mode 1 and is denied. The record documents the relationship and scale; it does not assert causation.
- **State the reason causation isn't alleged:** Kushner held no office during the reporting period (left Jan 2021; Affinity incorporated the next day), so there is no contemporaneous official act to link. This sentence belongs in the record — it's why the relationship stands documented without a causal hook.
- **Three distinct sovereign vehicles** (PIF, QIA, Lunate) — separate governance, cited individually, never fused as "Gulf money."
- **ADV categories ≠ named investors** — the primary record confirms sovereign-wealth-fund capital is present; it does not itself name PIF/QIA/Lunate. Don't let secondary reporting silently upgrade the named-fund facts to primary.
- **EA consortium (2025-26):** include only as business development if at all; no official act to link.

### 3. Link the watchlist

In `docs/references/fsf-watchlist.md`, update W-002: state `active` → `evaluated`, add `promoted_to: SC-008`. Preserve the existing nexus text and drift guards. Bump the doc's entry-count/version line if it tracks one.

### 4. Stage (do NOT add) the catalog candidates

The record surfaces three sovereign-vehicle candidates: **PIF**, **QIA**, **Lunate**. Per the catalog-inclusion rule (`docs/references/methodology-note-catalog-inclusion.md`), they enter `sovereign_entities.json` only on evaluation against this fact pattern — which is now in hand, so they're eligible — but each needs a governance line before it's a clean entry:
- **PIF** — Saudi Public Investment Fund; textbook SWF; chaired by MBS. Clean.
- **QIA** — Qatar Investment Authority; textbook SWF. Clean.
- **Lunate** — Abu Dhabi; verify governance (state-adjacent vs. state-owned) for the entry. **Do not conflate with MGX** (separate Abu Dhabi vehicle already in catalog via SC-007).

**Decision point for CJ — do not guess:** two options for this handoff —
- (a) add PIF and QIA now (clean), stage Lunate pending governance verification; or
- (b) stage all three as catalog candidates and add none until a single governance-verification pass covers them together.

Recommend (a): PIF and QIA are unambiguous SWFs evaluated against a real fact pattern; holding them adds nothing. Lunate alone waits. But flag and let CJ choose before writing to `sovereign_entities.json`. If unsure, do (b) and surface it.

### 5. Commit the reference doc

Commit `docs/references/sc-008-affinity-research-target.md` (the evidence base) on this branch so it lands with the record, not separately.

## Verify

- SC-008 exists in `records.json`, validates against the schema, scope LIVE.
- The two source tiers are distinguishable in the record (primary ADV facts vs. secondary named-fund facts).
- No causal claim present; the "no office during reporting period" sentence is in the record.
- W-002 in the watchlist reads `evaluated` / `promoted_to: SC-008`; nexus + guards preserved.
- Catalog: per CJ's (a)/(b) choice — either PIF+QIA added with governance lines and Lunate staged, or all three staged; nothing added without a governance line; Lunate not conflated with MGX.
- `tsc --noEmit` + `next build` green from `web/`. Regression guard still green (this touches records/data, not the candidate pipeline, but confirm).

## Commit / PR

Record + watchlist update + reference doc + catalog change as a PR. Report: the SC-### assigned, the catalog decision taken (a or b), and confirmation no causal claim landed in the record.

## Downstream (not this handoff)

- ADV Part 1A direct pull for per-fund investor identities (IAPD report PDF is JS-gated; use SEC ADV data files) — only if investor-identity detail beyond category-level is wanted.
- Lunate governance verification (if staged).
- Still owed from the OGE 278 thread: MGX + USD1 co-ownership primary anchors; methodology one-line note on retained/off-filing holdings.
