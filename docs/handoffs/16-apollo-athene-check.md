# Handoff #16 — Apollo / Athene precision check

## What this resolves

The last open item from Handoff #14. The Substack draft at `docs/drafts/methodology-page-substack.md` Section 4 ("The Apollo bound") currently characterizes the Belgrove $100M loan lender as "Apollo Global Management itself, not a Qatar-linked Apollo subsidiary or trust." The Witkoff Group / Parlatore Law Group October 2, 2025 letter to the NYT names the lender more precisely as "Apollo's Athene insurance vehicle." Athene is an Apollo Global Management subsidiary (Apollo acquired Athene Holding Ltd. in 2022), so the current draft characterization is defensible at the parent level. The question is whether the Substack version should be tightened to match the NYT correction's actual wording.

The Witkoff working reference at `docs/references/witkoff-methodology-reference.md` is the source of truth. If Corey wrote that section based on the primary records, the reference's wording is what the Substack draft should match.

## What Code needs to do

### Step 1: Read

Read `docs/references/witkoff-methodology-reference.md`, Apollo-channel section. Find every passage that characterizes the Belgrove lender. Note both the exact wording the reference uses and any citations the reference attaches to that wording (especially any citation to the NYT October 5, 2025 correction itself).

### Step 2: Decide

Three possible outcomes from Step 1.

**Outcome A: Reference unambiguously says "Athene"** (or "Apollo's Athene insurance vehicle," or some near-equivalent that specifies the subsidiary). Apply the swap to the Substack draft. The current passage:

> The Belgrove Palm Beach $100 million loan, made in May 2025, was originally framed in NYT reporting as coming from "the Apollo trust, a fund partly owned by Qatar." The NYT corrected the framing on October 5, 2025: the Belgrove lender was Apollo Global Management itself, not a Qatar-linked Apollo subsidiary or trust. Apollo Global Management is publicly traded (NYSE: APO) with Vanguard, BlackRock, State Street, and Capital Group as principal shareholders. No documented QIA stake in APO at any control-implying level appears in the record.

becomes:

> The Belgrove Palm Beach $100 million loan, made in May 2025, was originally framed in NYT reporting as coming from "the Apollo trust, a fund partly owned by Qatar." The NYT corrected the framing on October 5, 2025: the Belgrove lender was Apollo's Athene insurance vehicle, an Apollo Global Management subsidiary, not a Qatar-linked Apollo trust. Apollo Global Management is publicly traded (NYSE: APO) with Vanguard, BlackRock, State Street, and Capital Group as principal shareholders. No documented QIA stake in APO or in Athene at any control-implying level appears in the record.

Commit message: `docs(drafts): tighten Belgrove lender characterization to Athene (Handoff #16)`.

**Outcome B: Reference unambiguously says "Apollo Global Management"** (without naming Athene). No change to the draft. Report back what the reference says and confirm no edit needed.

**Outcome C: Reference cites both Athene and Apollo Global Management at different points,** or the wording is otherwise ambiguous. Do not edit the draft. Report back with the relevant passages quoted, and flag that the editorial call (which level of precision the Substack version should land on) needs Corey's adjudication.

### Step 3: Commit

If Outcome A: one commit for the prose change, with the handoff doc tracked in the same commit. Commit message above.

If Outcome B or C: commit only the handoff doc itself. Commit message: `docs(handoffs): add Handoff #16 (Apollo/Athene check, no draft change)`.

## What this doesn't do

- Doesn't resolve the NYT Kamin article URL. Still TK, still needs a Times-logged-in session to retrieve.
- Doesn't push to Substack. The draft remains in `docs/drafts/` until the title is chosen and the NYT URL is filled.
- Doesn't touch any other Substack draft section.

## After this lands

Three items separate the Substack draft from being ready to publish:

1. NYT Kamin URL retrieved (one-step grab once Corey is in front of a Times-logged-in browser).
2. Title chosen from the three options at the top of the draft.
3. Apollo / Athene check resolved (this handoff, plus any follow-up if Outcome C).

Once those three are done, the draft is ready for Corey to paste to Substack at das_DEMARC. The natural next handoff after publication is Phase 5 opener: OGE 278 collector. Multi-handoff piece, real engineering, queued since May 8.
