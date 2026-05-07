Pick up Sovereign Connections Tracker Handoff #11 (sovereign_entities schema extension + ADQ/MGX/PIA governance updates + new L'imad entry).

## Prerequisite

Run `git status` to confirm working tree clean and local main matches origin/main. Last known commit was 2e5e207 (README status table refresh).

## Predecessor

Handoff #10 closed with SC-008 as the second LIVE record:
- b02da69 — feat(data): land SC-008 Witkoff Group / Roosevelt redevelopment as v2.0 covered-intermediary worked case
- 2e5e207 — docs(README): refresh status table counts after SC-008 and PIA/ADQ/MGX additions

## Project state

`web/lib/types.ts` is v1.x. `SovereignEntity` interface currently has no `primary_sources` field. Schema extension is the first task in this handoff.

`web/data/sovereign_entities.json` holds 10 entries: PIF, MUBADALA, ADIA, QIA, KIA, NBIM, GIC (seven seeds), plus ADQ, MGX added in Handoff #9 and PIA added in Handoff #10. Three of those (ADQ, MGX, PIA) need governance-note refinement and primary_sources citations. One new entry (L'imad) gets added because verification surfaced ADQ's January 2026 absorption into L'imad Holding Company.

The seven seed entries (PIF through GIC) get the same treatment in a future session. Out of scope here.

## Task

1. Extend `SovereignEntity` interface in `web/lib/types.ts` to include optional `primary_sources?: PrimarySource[]` field, mirroring `SovereignRecord`
2. Revise three existing entries (ADQ, MGX, PIA) in `web/data/sovereign_entities.json`: governance_note rewrite + new primary_sources arrays
3. Add new L'imad entry to `web/data/sovereign_entities.json`
4. Update README status row from "10 entries at /swfs" to "11 entries at /swfs"
5. Add changelog entry as ## 2026-05-07 (later +1) above the existing 2026-05-07 (later) entry

Two-commit split is recommended: schema extension as its own commit (small, low-risk, reversible), then data updates + README + changelog as a second commit.

## Files to edit

### 1. `web/lib/types.ts` — extend SovereignEntity

Change:

```typescript
export interface SovereignEntity {
  id: string;
  name: string;
  country: string;
  governance_note: string;
}
```

To:

```typescript
export interface SovereignEntity {
  id: string;
  name: string;
  country: string;
  governance_note: string;
  primary_sources?: PrimarySource[];
}
```

The `PrimarySource` interface already exists earlier in the file. No changes there. The `?` makes the field optional so existing entries without primary_sources still parse cleanly.

The `/swfs` page rendering will need to handle the optional new field. If the existing template doesn't already render primary_sources for entities, add that rendering — match the SC-007/SC-008 detail page pattern (label, optional URL as link, category badge). If the template does render it via a shared component, no UI change needed.

### 2. `web/data/sovereign_entities.json` — revise ADQ entry

Replace the existing ADQ entry (the one added in Handoff #9) with:

```json
{
  "id": "ADQ",
  "name": "Abu Dhabi Developmental Holding Company",
  "country": "United Arab Emirates",
  "governance_note": "Established 2018 (originally Abu Dhabi Developmental Holding Company / ADDH), rebranded ADQ in 2020. Diversified sovereign holdings across utilities, healthcare, food, transport, and logistics; assets variously reported at $159B-$263B by late 2025. Chaired by Sheikh Tahnoon bin Zayed Al Nahyan (UAE National Security Advisor, Deputy Ruler of Abu Dhabi) through January 2026. On January 15, 2026 the Abu Dhabi Supreme Council for Financial and Economic Affairs launched L'imad Holding Company as a successor vehicle absorbing ADQ, with Crown Prince Sheikh Khaled bin Mohamed Al Nahyan as L'imad chair; takeover ongoing as of this entry. The Tahnoon-Aryam (January 2025) and MGX-Binance-WLF (May 2025) transactions referenced in SC-007 occurred under ADQ's pre-L'imad governance structure. Future ADQ-source flows route through L'imad governance, which represents continued direct sovereign control rather than greater institutional independence.",
  "primary_sources": [
    {
      "label": "ADQ official 'Who we are' page",
      "url": "https://www.adq.ae/about-adq/who-we-are/",
      "category": 1
    },
    {
      "label": "Abu Dhabi Media Office, 'Abu Dhabi Launches Comprehensive Global Investment Strategy on Artificial Intelligence', September 25, 2024 (establishes AIATC and Tahnoon's chairmanship of ADQ-adjacent vehicles)",
      "url": "https://www.mediaoffice.abudhabi/en/technology/abu-dhabi-launches-comprehensive-global-investment-strategy-on-artificial-intelligence/",
      "category": 1
    },
    {
      "label": "Abu Dhabi Supreme Council for Financial and Economic Affairs statement on L'imad Holding Company, February 2, 2026",
      "category": 1
    },
    {
      "label": "Asia Asset Management, 'Abu Dhabi's newly minted wealth fund L'imad to take over US$263 billion peer ADQ', February 4, 2026",
      "url": "https://www.asiaasset.com/post/30467-limadadq-gte-0203",
      "category": 3
    },
    {
      "label": "AGBI ADQ profile and reporting on L'imad consolidation",
      "url": "https://www.agbi.com/companies/adq/",
      "category": 3
    }
  ]
}
```

### 3. `web/data/sovereign_entities.json` — revise MGX entry

Replace the existing MGX entry (the one added in Handoff #9) with:

```json
{
  "id": "MGX",
  "name": "MGX",
  "country": "United Arab Emirates",
  "governance_note": "Abu Dhabi state-backed AI-focused investment vehicle launched March 2024 by the Artificial Intelligence and Advanced Technology Council (AIATC), itself established January 22, 2024 by UAE President Mohamed bin Zayed Al Nahyan. Foundational partners: Mubadala and G42 (the Abu Dhabi-headquartered AI conglomerate). Chaired by Sheikh Tahnoon bin Zayed Al Nahyan; Vice Chair is Khaldoon Al Mubarak (Mubadala Managing Director and Group CEO); CEO is Ahmed Yahia Al Idrissi (formerly CEO of Mubadala's direct investments platform). Target AUM up to $100 billion. Notable positions and partnerships include the Global AI Infrastructure Investment Partnership with BlackRock, Microsoft, and GIP (September 2024); the Stargate Project with OpenAI, SoftBank, and Oracle (January 2025); and significant positions in OpenAI, xAI, and Anthropic. Tahnoon's chairmanship continues post-ADQ-to-L'imad transition; he chaired MGX's first board meeting of 2026 in February 2026. Sovereign-adjacent character documented in House Select Committee on the CCP correspondence (February 4, 2026 letter to Zach Witkoff) and WSJ reporting on the WLF Tahnoon-Aryam-Binance sequence.",
  "primary_sources": [
    {
      "label": "Abu Dhabi Media Office, 'Abu Dhabi Launches Comprehensive Global Investment Strategy on Artificial Intelligence', September 25, 2024",
      "url": "https://www.mediaoffice.abudhabi/en/technology/abu-dhabi-launches-comprehensive-global-investment-strategy-on-artificial-intelligence/",
      "category": 1
    },
    {
      "label": "MGX official Leadership page",
      "url": "https://www.mgx.ae/en/leadership",
      "category": 1
    },
    {
      "label": "Abu Dhabi Media Office, 'Tahnoon bin Zayed chairs MGX's first board meeting of 2026', February 27, 2026",
      "url": "https://www.mediaoffice.abudhabi/en/technology/tahnoon-bin-zayed-chairs-mgxs-first-board-meeting-of-2026/",
      "category": 1
    },
    {
      "label": "Mubadala press release co-announcing MGX, September 2024",
      "url": "https://www.mubadala.com/en/news/abu-dhabi-launches-comprehensive-global-investment-strategy-on-artificial-intelligence",
      "category": 1
    },
    {
      "label": "House Select Committee on the CCP, letter to Zach Witkoff, February 4, 2026",
      "category": 1
    },
    {
      "label": "WSJ, 'Spy Sheikh Secret Stake Trump Crypto Tahnoon' series, January 31, 2026",
      "category": 3
    }
  ]
}
```

### 4. `web/data/sovereign_entities.json` — revise PIA entry

Replace the existing PIA entry (the one added in Handoff #10) with:

```json
{
  "id": "PIA",
  "name": "Pakistan International Airlines (PIA)",
  "country": "Pakistan",
  "governance_note": "Pakistan's national airline, historically a wholly state-owned enterprise. Privatized December 23, 2025: an Arif Habib-led consortium (with AKD Group Holdings, Fatima Fertilizer, City Schools, Lake City Holdings, and military-owned Fauji Fertilizer) acquired a 75% stake for Rs135 billion (~$482 million); the Pakistani government retains a 25% stake, with the consortium holding an option to acquire the remaining 25% within three months at a 12% premium. The Roosevelt Hotel and other PIA overseas real estate assets were ring-fenced from the airline privatization and are being privatized through a separate process under the Cabinet Committee on Privatisation's joint-venture model approved July 2025. The Roosevelt is held by PIA Investment Limited (PIAIL, the investment arm of PIA), with the asset titled to Roosevelt Hotel Corporation as a PIAIL subsidiary. PIAIL acquired the Roosevelt in 1979. The February 19, 2026 US-Pakistan Roosevelt redevelopment MOU referenced in SC-008 sits within this separate privatization process. Sovereign-adjacent through the residual government minority stake, the carve-out structure for foreign-held assets, and the broader IMF Extended Fund Facility privatization framework that retains state involvement in transactional decisions. Post-privatization structure remains in flux as transition mechanics complete.",
  "primary_sources": [
    {
      "label": "Pakistan Privatisation Commission, transaction structure approval for PIA and Roosevelt Hotel, July 2025",
      "category": 1
    },
    {
      "label": "Pakistan Finance Division statement on Roosevelt Hotel MOU with US GSA, February 19, 2026",
      "category": 1
    },
    {
      "label": "Arab News, 'Pakistan prequalifies four investors for PIA, greenlights Roosevelt Hotel joint venture deal', July 9, 2025",
      "url": "https://www.arabnews.com/node/2607397/pakistan",
      "category": 3
    },
    {
      "label": "Al Jazeera, 'Why is the sale of Pakistan's national airline stirring a political storm?', December 26, 2025",
      "url": "https://www.aljazeera.com/news/2025/12/26/why-is-the-sale-of-pakistans-national-airline-stirring-a-political-storm",
      "category": 3
    },
    {
      "label": "Arab News, 'Pakistan says Roosevelt Hotel deal still being structured after PIA sale', December 24, 2025",
      "url": "https://www.arabnews.com/node/2627307/pakistan",
      "category": 3
    },
    {
      "label": "Express Tribune, 'Arif Habib consortium wins PIA privatisation bid with Rs135b offer', December 24, 2025",
      "url": "https://tribune.com.pk/story/2583719/govt-finally-cuts-loose-white-elephant-pia-1",
      "category": 3
    }
  ]
}
```

### 5. `web/data/sovereign_entities.json` — append new L'imad entry

Append after the PIA entry:

```json
{
  "id": "LIMAD",
  "name": "L'imad Holding Company",
  "country": "United Arab Emirates",
  "governance_note": "Sovereign investment entity launched January 15, 2026 by the Abu Dhabi Supreme Council for Financial and Economic Affairs to absorb ADQ and consolidate it with Modon (real estate) and CYVN (automotive) holdings. Chaired by Sheikh Khaled bin Mohamed Al Nahyan, Crown Prince of Abu Dhabi; CEO is Jassem Al Zaabi. Khaldoon Al Mubarak (Mubadala Managing Director and Group CEO) sits on the L'imad board. ADQ assets at the time of takeover announcement reported at $263 billion. The transition marks a generational shift in Abu Dhabi sovereign investment governance away from Sheikh Tahnoon's portfolio toward the crown prince's direct oversight; regional analysts cited in AGBI read this as the rise of a new generation of leaders preparing to take over political and economic stewardship of the UAE. Sovereign character is direct given the chairman's crown prince status. Treated as sovereign-adjacent for tracker purposes; no transactions documented in tracker records yet attribute to L'imad, but ADQ-source flows in pre-2026 records are expected to migrate to L'imad attribution as takeover mechanics complete.",
  "primary_sources": [
    {
      "label": "Abu Dhabi Supreme Council for Financial and Economic Affairs statement on L'imad Holding Company, February 2, 2026",
      "category": 1
    },
    {
      "label": "Asia Asset Management, 'Abu Dhabi's newly minted wealth fund L'imad to take over US$263 billion peer ADQ', February 4, 2026",
      "url": "https://www.asiaasset.com/post/30467-limadadq-gte-0203",
      "category": 3
    },
    {
      "label": "Global SWF, LIMAD fund profile",
      "url": "https://globalswf.com/fund/ADQ",
      "category": 3
    },
    {
      "label": "AGBI reporting on the L'imad consolidation",
      "url": "https://www.agbi.com/companies/adq/",
      "category": 3
    }
  ]
}
```

### 6. `README.md` — status row update

Change:

```
| Sovereign wealth fund registry | 10 entries at /swfs |
```

To:

```
| Sovereign wealth fund registry | 11 entries at /swfs (3 with primary_sources; seven seeds queued) |
```

Also change:

```
| Data file | 8 records (2 LIVE), 10 entities; collectors not yet wired |
```

To:

```
| Data file | 8 records (2 LIVE), 11 entities; collectors not yet wired |
```

### 7. `docs/changelog.md` — new entry above existing 2026-05-07 (later)

```markdown
## 2026-05-07 (later +1)

`SovereignEntity` schema extended with optional `primary_sources` field, mirroring the `SovereignRecord` pattern. Schema change is structural and reversible; existing entries without primary_sources continue to parse.

Three sovereign-entities entries revised with primary-source verification: ADQ, MGX, PIA. ADQ governance_note now reflects the January 15, 2026 launch of L'imad Holding Company as a successor sovereign vehicle absorbing ADQ; pre-2026 ADQ-attributed transactions in SC-007 remain accurate as documented under ADQ's pre-L'imad governance structure. MGX governance_note refined with verified founding-partner, leadership, and partnership detail; Tahnoon's chairmanship continues post-transition. PIA governance_note corrected on two points: PIA itself was privatized December 23, 2025 with Pakistani government retaining a 25% stake, and the Roosevelt Hotel ownership chain runs through PIA Investment Limited (PIAIL) and Roosevelt Hotel Corporation as PIAIL's subsidiary, not directly through PIA — the Roosevelt and other overseas assets were ring-fenced from the airline privatization for separate joint-venture-model handling.

One new sovereign-entities entry: L'imad Holding Company (LIMAD), with governance_note covering the January 15, 2026 launch and consolidation of ADQ, Modon, and CYVN under the Abu Dhabi crown prince's chairmanship.

Seven seed entries (PIF, MUBADALA, ADIA, QIA, KIA, NBIM, GIC) queued for primary-source verification in a future session; their existing prose-only governance_notes remain in place pending that pass.

Defined terms unchanged.
```

## Verification

```bash
cd web
npm run build
```

Confirm: TypeScript compiles after the SovereignEntity schema change (the optional field is the only structural addition; existing data parses cleanly with or without primary_sources). JSON parses. /swfs prerenders.

After build, run `npm run dev` and visit:
- `/swfs` — confirm 11 entries; ADQ, MGX, PIA, L'imad each show primary_sources entries below their governance_note (assuming the rendering template handles the new field; if it doesn't, ship the data and template update together so primary_sources are visible)
- Confirm the seven seed entries (PIF through GIC) still render unchanged with no broken layout
- `/` — counter still reads "8 records · 2 live"; no record-side changes in this handoff

## Commit suggestion

Two-commit split:

Commit 1 (schema extension only):

```
feat(types): add optional primary_sources field to SovereignEntity

Mirrors the SovereignRecord shape so registry entries can carry the same
PrimarySource[] structure used by records. Field is optional so existing
data parses unchanged. Render template updated to display the new field
when present.
```

Commit 2 (data updates):

```
feat(data): expand SWF registry with primary_sources for ADQ, MGX, PIA, plus new L'imad entry

- Revise ADQ governance_note to reflect January 15 2026 L'imad takeover
- Refine MGX governance_note with verified founding-partner, leadership,
  and partnership detail
- Correct PIA governance_note: airline privatized December 23 2025 (75%
  to Arif Habib consortium, 25% retained by government); Roosevelt Hotel
  ownership chain runs through PIA Investment Limited (PIAIL) and
  Roosevelt Hotel Corporation, ring-fenced from airline privatization
- Add new LIMAD entry for L'imad Holding Company
- Update README status rows (11 entries; 11 entities total)
- Add 2026-05-07 (later +1) changelog entry

Pre-2026 ADQ-attributed transactions in SC-007 remain accurate under ADQ's
pre-L'imad governance structure. Seven seed entries queued for
primary-source verification in a future session.

Defined terms unchanged.
```

## House style

Per PROJECT.md: no em-dashes, no red-flag words, analyst-not-advocate voice, descriptive not prescriptive. Governance_notes are tighter than the seed entries' prose-only form because they now carry citation density via primary_sources; preserve that compression rather than re-padding with prose.

After committing, paste output of `git log --oneline -5`. Confirm Vercel deploy is green and `/swfs` shows the 11 entries with primary_sources rendering for ADQ, MGX, PIA, L'imad.
