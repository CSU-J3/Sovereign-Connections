# Handoff #14 — Substack methodology draft to repo

## What landed

A Substack-ready tightening of the methodology page sits at `/mnt/user-data/outputs/sovereign-connections-methodology-substack.md` (also pastable from the chat that produced this handoff). It's derived from `docs/drafts/methodology-page-first-draft.md` (May 5), not from the post-Handoff #13 live `/methodology` page. Length is ~3,594 words counting the title-options block and primary-sources list; body is ~3,400 against the 3,500 target.

## What Code needs to do

1. Place the file at `docs/drafts/methodology-page-substack.md`.
2. Commit as one change with message: `docs(drafts): add Substack-ready methodology draft (Handoff #14)`.
3. No edits to the live `/methodology` page. The Substack version is a derivative, not the source of truth.

## What changed from the May 5 first draft

- Section 2 ("The core rule"): "why this rule and not broader/narrower" collapsed into a single tighter paragraph. ~80 words out.
- Section 6 ("v2.0: covered intermediaries"): standalone versioning paragraph rolled into the portfolio-overlap paragraph; appointee-bound trimmed. ~120 words out.
- Section 7 ("What this rule isn't"): FIRRMA + 18 USC 208 + 5 CFR 2635.204 collapsed into a single combined paragraph. Five distinctions instead of six. ~150 words out.
- Intro: the heavy signposting paragraph (original line 7) replaced with a tighter case preview.
- Sections 3, 4, 5, 8, 9 untouched at the prose level.
- A `## Primary sources` block was added at the end with the canonical URLs for cited primary records.
- Title and dek options sit at the top of the file as a block to be picked or overridden before the post ships anywhere.

The Section 7 additions from Handoff #13 (Tahnoon-cluster note, NBIM calibration caveat) are deliberately NOT in the Substack version. They're repo-side calibration that reads as inside-baseball on a public surface. The per-SWF appendix paragraph from the May 5 draft is preserved.

## Known gaps

Two items the post should not ship publicly with unresolved:

1. **NYT URL is TK.** The September 26, 2025 Debra Kamin piece "Where Mideast Envoy Pitched Peace, His Son Pitched Investors" carries the October 5 correction note. The canonical nytimes.com URL didn't surface in open search (paywalled). One-step grab from a Times-logged-in session or the Times archive. Marked as TK in the primary-sources block.

2. **Apollo / Athene precision check.** The draft (Section 4 / "The Apollo bound") says: "the NYT corrected the framing on October 5, 2025: the Belgrove lender was Apollo Global Management itself, not a Qatar-linked Apollo subsidiary or trust." The Witkoff Group / Parlatore Law Group letter to the NYT (October 2, 2025) names the lender more precisely as "Apollo's Athene insurance vehicle." Athene is an Apollo Global Management subsidiary acquired in 2022, so "Apollo Global Management" is defensible as the parent characterization, but if the NYT correction itself printed "Athene," the Substack version should be tightened to match. Check against `docs/references/witkoff-methodology-reference.md` (Apollo-channel section) before pushing to Substack. No change to the committed draft yet; flag in the changelog entry only.

## What this handoff doesn't do

- Doesn't push to Substack. The draft sits in `docs/drafts/` until the title is chosen, the NYT URL is resolved, and the Apollo / Athene question is checked.
- Doesn't update the live `/methodology` page. That page already absorbed Handoff #13.
- Doesn't add a changelog entry. The Substack draft is a derivative work that doesn't change tracker definitions or scope, so no versioning event.

## After this lands

Two natural follow-ups from the May 8 sign-off, in order:

1. Resolve the two known gaps (NYT URL retrieval, Apollo / Athene precision check), choose the title, push to Substack at das_DEMARC.
2. Phase 5 opener: OGE 278 collector. Multi-handoff piece. Recommended as the next real engineering branch once the Substack post is live.
