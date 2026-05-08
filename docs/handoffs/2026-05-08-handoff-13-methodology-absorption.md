Pick up Sovereign Connections Tracker Handoff #13 (methodology page absorption of Handoff #12 findings).

## Prerequisite

Run `git status` to confirm working tree clean and local main matches origin/main. Last known commits from Handoff #12 were:

```
3fc2bbd feat(data): verify and cite the seven seed sovereign-entities entries
33b3559 docs(README, data): tighten PIA name and SWF status row
a4c835f feat(data): expand SWF registry with primary_sources for ADQ, MGX, PIA, plus new L'imad entry
```

## Predecessor

Handoff #12 closed the seed sovereign-entities verification pass: governance-note rewrites and primary_sources arrays for PIF, MUBADALA, ADIA, QIA, KIA, NBIM, GIC. Two structural findings landed in the registry data:

1. **ADIA chairmanship sits with Sheikh Tahnoun bin Zayed Al Nahyan** — the same Tahnoon at the centre of SC-007's Aryam transaction and concurrent chair of MGX, G42, and pre-L'imad ADQ. The Abu Dhabi sovereign cluster organises around an individual rather than around fund-level governance.

2. **NBIM's established ethical framework was suspended by the Storting in November 2025** pending review by a public committee appointed by the King in Council; report due 15 October 2026. Council on Ethics operating under temporary guidelines, not making observation or exclusion recommendations.

Both findings currently live only in the registry data at /swfs. The methodology page at /methodology was drafted before these findings surfaced and treats NBIM as the calibration point and the Abu Dhabi cluster as fund-organised. Both framings are now partially out of date.

## Project state

`web/app/methodology/page.tsx` holds the rendered methodology page (~3,950 words across nine sections, integrated in Handoff #8, with Section 7's per-SWF appendix forward-reference linked to /swfs in Handoff #9). No structural changes since.

The two additions in this handoff are prose insertions, not structural rewrites. No schema work, no template work, no new pages.

## Task

Two prose additions to `web/app/methodology/page.tsx`:

### Addition 1: Tahnoon-cluster note

Insert as a short standalone paragraph in Section 7 (the "what the rule isn't" / per-SWF appendix forward-reference section), after the existing paragraph that mentions the per-SWF governance appendix linking to /swfs. The note tells readers how to read the appendix in light of the verification-pass finding.

Prose to insert (use as-is, voice already aligned to PROJECT.md house style):

> One pattern surfaced during the per-SWF appendix verification pass that's worth naming. The Abu Dhabi sovereign cluster organises around an individual rather than around fund-level governance. Sheikh Tahnoun bin Zayed Al Nahyan chairs ADIA (the emirate's largest fund at roughly USD 1 trillion), MGX, G42, and (until its January 2026 absorption into L'imad) ADQ. Reading the appendix fund by fund understates this. A Mubadala transaction and an MGX transaction sit inside a network that traces back through individual chairmanships, not just through corporate registry. The appendix cites the overlap on each affected entry; methodology readers should weight it when interpreting transaction patterns, particularly where SC-007's Aryam vehicle and MGX both appear in the underlying record.

### Addition 2: NBIM-suspension caveat

Find the existing NBIM reference in the methodology page (most likely in Section 2 where sovereign-source money is defined, or wherever the page describes what arm's-length governance looks like). After that reference, insert the following caveat. If the page already has footnote scaffolding, format as a footnote; if not, insert as a short parenthetical paragraph immediately following the existing NBIM mention.

Prose to insert (use as-is):

> NBIM is treated here as the reference framework for what arm's-length sovereign governance looks like. The November 2025 caveat: the Storting suspended the established ethical framework pending review by a public committee appointed by the King in Council, with the report due 15 October 2026. The Council on Ethics is operating under temporary guidelines and is not making observation or exclusion recommendations. The reference framework remains useful as a calibration point; the suspension is an active structural change, not a settled rewrite, and the methodology page will be revisited once the committee reports.

If the existing NBIM reference is already detailed enough that this insertion would create redundancy, just append the November 2025 caveat sentences (from "The November 2025 caveat:" onward) rather than the full insertion.

## Voice and style

PROJECT.md house style holds. No em-dashes (the existing methodology page is clean of them; preserve that). No red-flag words (paradigm shift, unprecedented, shocking, staggering, alarming, etc.). Analyst-not-advocate voice. The prose above is already aligned; no editorial changes to it without flagging.

The two additions should read as continuous with the existing voice, not as bolted-on amendments. Light editorial smoothing of transition sentences is fine if necessary to make the insertion read naturally with the surrounding prose.

## Files to edit

`web/app/methodology/page.tsx` — only file touched in this handoff.

No README change required (the methodology page row already reads "Live at /methodology (v2.0 adopted 2026-05-05)" and the v2.0 timestamp captures the substantive rule; today's additions are post-rule findings absorbed into the live page, not a new rule version).

## Changelog entry

`docs/changelog.md` — new entry above existing 2026-05-08:

```markdown
## 2026-05-08 (later)

Methodology page absorbs the two structural findings from the Handoff #12 seed sovereign-entities verification pass.

Section 7 gains a short paragraph on the Abu Dhabi sovereign cluster's individual-organised character: Sheikh Tahnoun bin Zayed Al Nahyan chairs ADIA, MGX, G42, and pre-L'imad ADQ, which means reading the per-SWF appendix fund by fund understates the network. The note tells methodology readers how to weight the chairmanship overlap, particularly where SC-007's Aryam vehicle and MGX both appear.

The NBIM reference gains a November 2025 caveat. The Storting suspended the established ethical framework pending committee review (report due 15 October 2026); Council on Ethics operating under temporary guidelines without observation or exclusion recommendations. NBIM remains the calibration point for arm's-length sovereign governance, but the calibration point is itself in active structural change. The methodology page will be revisited once the committee reports.

No rule change. v2.0 covered-persons definition unchanged. Defined terms unchanged.
```

## Verification

```bash
cd web
npm run build
```

Confirm: TypeScript compiles unchanged (no schema work); page prerenders.

After build, run `npm run dev` and visit `/methodology`:
- Section 7 reads with the Tahnoon-cluster paragraph following the per-SWF appendix forward reference
- NBIM reference reads with the November 2025 caveat following the calibration-point framing
- Page voice and pacing unchanged elsewhere
- Internal `/swfs` link in Section 7 still resolves correctly

## Commit suggestion

Single commit:

```
feat(methodology): absorb Handoff #12 findings into the live page

Section 7 gains a paragraph on the Abu Dhabi cluster's
individual-organised character (Tahnoun chairmanship across ADIA,
MGX, G42, pre-L'imad ADQ). NBIM reference gains a November 2025
caveat: Storting suspension of the established ethical framework
pending committee review (report due 15 October 2026), Council on
Ethics operating under temporary guidelines. No rule change; v2.0
covered-persons definition and defined terms unchanged.
```

Push and paste `git log --oneline -3`.
