Pick up Sovereign Connections Tracker Handoff #12 (seed sovereign-entities pass: governance-note rewrites and primary_sources arrays for PIF, MUBADALA, ADIA, QIA, KIA, NBIM, GIC).

## Prerequisite

Run `git status` to confirm working tree clean and local main matches origin/main. Last known commits from Handoff #11 were:

```
a4c835f feat(data): expand SWF registry with primary_sources for ADQ, MGX, PIA, plus new L'imad entry
8a964d1 feat(types): add optional primary_sources field to SovereignEntity
```

## Predecessor

Handoff #11 closed with the ADQ/MGX/PIA/LIMAD pass: schema extension to `SovereignEntity` adding optional `primary_sources?: PrimarySource[]`, governance-note revisions and primary_sources arrays for the four post-seed entries, render-template extension on `/swfs` to display `primary_sources` below `governance_note`. Build green, deploy green, registry now showing 11 entries.

The seven seed entries (PIF, MUBADALA, ADIA, QIA, KIA, NBIM, GIC) were explicitly queued for a separate session because their governance_notes were prose-only and pre-dated the verification discipline applied in Handoff #11. This is that session.

## Project state

`web/data/sovereign_entities.json` holds 11 entries. The seven seed entries currently render with prose-only governance_notes and no primary_sources arrays. The four post-seed entries (ADQ, MGX, PIA, LIMAD) render with verified governance_notes and primary_sources arrays following the Handoff #11 pattern.

`web/lib/types.ts` is already at the post-#11 schema (optional `primary_sources?: PrimarySource[]` on `SovereignEntity`). No schema work in this handoff.

The render template on `/swfs` already handles `primary_sources` for any entry that carries the field. No template work in this handoff.

## Task

Rewrite `governance_note` and add `primary_sources` arrays for the seven seed entries in `web/data/sovereign_entities.json`. Update README status row. Add changelog entry.

Two findings from verification that the new notes capture and that the methodology piece will need to absorb in a future pass:

1. **ADIA is chaired by Sheikh Tahnoun bin Zayed Al Nahyan** — the same Tahnoon at the centre of SC-007's Aryam transaction, who concurrently chairs MGX and (pre-L'imad) chaired ADQ. The seed note must surface this overlap rather than treat ADIA as a generic neighbouring SWF.

2. **NBIM's established ethical framework was suspended by the Storting in November 2025**, pending a Ministry of Finance committee review with a report due 15 October 2026. The Council on Ethics is operating under temporary guidelines and is not making observation or exclusion recommendations. The seed note must mark this as a live structural change to the calibration framework, not a settled fact.

## Files to edit

### 1. `web/data/sovereign_entities.json` — replace each of the seven seed entries

Each entry below replaces the existing entry with the same `id`. Match the JSON structure used in Handoff #11 for ADQ/MGX/PIA/LIMAD. Keep `id`, `name`, `country` strings exactly as currently set; replace `governance_note` and add `primary_sources`.

#### PIF

```json
{
  "id": "PIF",
  "name": "Public Investment Fund",
  "country": "Saudi Arabia",
  "governance_note": "Established 1971 by Royal Decree M/24 under King Faisal as a development-financing vehicle. In March 2015 oversight was transferred from the Ministry of Finance to the Council of Economic and Development Affairs (CEDA), and the same year then-Deputy Crown Prince Mohammed bin Salman was assigned chairmanship. The fund's transformation from a passive holding entity to an active global investor dates from this transition. Chair: HRH Crown Prince Mohammed bin Salman bin Abdulaziz Al Saud, Prime Minister and CEDA Chairman, the kingdom's de facto ruler since 2015. Governor: Yasir Al-Rumayyan. AUM SAR 3.53 trillion (approximately USD 941 billion) as of 2025; the 2026-2030 strategy approved by the board on 15 April 2026 continues the trajectory toward the USD 2 trillion AuM target under Vision 2030. PIF's Affinity Partners commitment that anchors SC-001 (USD 2 billion, 2021) was approved over the unanimous opposition of PIF's screening panel before being pushed through by MbS, per the Senate Finance Committee record and contemporaneous reporting; the screening-panel override is the documented case in which PIF's stated arm's-length governance failed. Santiago Principles signatory; structural critique of MbS's personal control over investment decisions documented in academic and policy literature.",
  "primary_sources": [
    { "label": "Public Investment Fund — official site", "url": "https://www.pif.gov.sa/en/", "category": 1 },
    { "label": "PIF Board approves 2026-2030 strategy, 15 April 2026", "url": "https://www.pif.gov.sa/en/news-and-insights/press-releases/2026/chaired-by-hrh-crown-prince-pif-board-of-directors-approves-pif-2026-2030-strategy/", "category": 1 },
    { "label": "Royal Decree M/24 of 1971 (PIF establishment)", "category": 1 },
    { "label": "Council of Economic and Development Affairs reorganisation, March 2015", "category": 1 },
    { "label": "Senate Finance Committee correspondence on PIF–Affinity Partners (Wyden investigation, 2022–2024)", "category": 2 },
    { "label": "Noria Research, 'Diversification Meets Personalization: The Strategic Role of the Public Investment Fund in Saudi Arabia' (January 2025)", "url": "https://noria-research.com/mena/diversification-meets-personalization-the-strategic-role-of-the-public-investment-fund-in-saudi-arabia/", "category": 3 },
    { "label": "Wikipedia, 'Public Investment Fund'", "url": "https://en.wikipedia.org/wiki/Public_Investment_Fund", "category": 3 }
  ]
}
```

#### MUBADALA

```json
{
  "id": "MUBADALA",
  "name": "Mubadala Investment Company",
  "country": "United Arab Emirates",
  "governance_note": "Mubadala Investment Company PJSC was created in 2017 through the merger of Mubadala Development Company (founded 2002) and the International Petroleum Investment Company (founded 1984), with MDC subsequently renamed Mamoura Diversified Global Holding. The Abu Dhabi Investment Council was absorbed in 2019. Wholly owned by the Government of Abu Dhabi. Chair: Sheikh Mansour bin Zayed Al Nahyan, UAE Vice-President and Deputy Prime Minister. Managing Director and Group CEO: Khaldoon Khalifa Al Mubarak, continuous since the founding of MDC in 2002 and concurrently Vice Chair of MGX and a board member of L'imad. AUM USD 385 billion as of 2025. The CFIUS-reviewed acquisition of Fortress Investment Group (announced May 2023, approved May 2024) and the resulting Mubadala-Fortress investment partnership announced April 2025 are documented entry points into US asset management at sovereign scale. Member of IFSWF; Global SWF GSR'25 governance score 9/10.",
  "primary_sources": [
    { "label": "Mubadala — official site", "url": "https://www.mubadala.com/", "category": 1 },
    { "label": "Mubadala 'About' (USD 385bn AUM disclosure, 2025)", "url": "https://www.mubadala.com/en/who-we-are/about-mubadala", "category": 1 },
    { "label": "Mubadala 'Our Structure'", "url": "https://www.mubadala.com/en/who-we-are/our-structure", "category": 1 },
    { "label": "Committee on Foreign Investment in the United States (CFIUS) review of Fortress Investment Group acquisition, 2023–2024", "category": 2 },
    { "label": "Global SWF, Mubadala fund profile (GSR'25 governance scoring)", "url": "https://globalswf.com/fund/MUBAD", "category": 3 },
    { "label": "Wikipedia, 'Mubadala Investment Company'", "url": "https://en.wikipedia.org/wiki/Mubadala_Investment_Company", "category": 3 }
  ]
}
```

#### ADIA

```json
{
  "id": "ADIA",
  "name": "Abu Dhabi Investment Authority",
  "country": "United Arab Emirates",
  "governance_note": "Established 1976 by Sheikh Zayed bin Sultan Al Nahyan as an independent investment institution; predecessor entity was Abu Dhabi's Financial Investments Board (1967). Estimated AUM USD 1.057 trillion (SWFI; ADIA itself does not publicly disclose). Chair: H.H. Sheikh Tahnoun bin Zayed Al Nahyan, Deputy Ruler of Abu Dhabi and UAE National Security Advisor — the same individual at the centre of the Tahnoon-Aryam transaction that anchors SC-007 and concurrently chair of MGX, G42, and (pre-L'imad) ADQ. Managing Director: H.H. Sheikh Hamed bin Zayed Al Nahyan, continuous since 2010 (succeeded his late brother Sheikh Ahmed bin Zayed). Board appointed by decree of the Ruler of Abu Dhabi, terms three years renewable, currently includes Sheikh Mansour bin Zayed and Sheikh Khaled bin Mohamed bin Zayed (Crown Prince). ADIA co-chaired the IFSWF working group that produced the 2008 Santiago Principles. ADIA's official governance language asserts it 'conducts its investment activities independently and without reference to the Government of the Emirate of Abu Dhabi'; the institutional reality of Tahnoon's chairmanship, set against his concurrent leadership across the Abu Dhabi sovereign-adjacent cluster, sits in tension with the arm's-length framing for tracker purposes.",
  "primary_sources": [
    { "label": "Abu Dhabi Investment Authority — official site", "url": "https://www.adia.ae/", "category": 1 },
    { "label": "ADIA Annual Review 2024, Board of Directors", "url": "https://www.adia.ae/en/pr/2024/pdf/ADIA Annual Review 2024- Board of Directors.pdf", "category": 1 },
    { "label": "ADIA Governance page", "url": "https://www.adia.ae/en/investments/governance", "category": 1 },
    { "label": "Abu Dhabi Media Office, 'Tahnoon bin Zayed chairs 3rd 2025 meeting of Board of Directors of Abu Dhabi Investment Authority' (9 December 2025)", "url": "https://www.mediaoffice.abudhabi/en/economy/in-the-presence-of-mansour-bin-zayed-and-khaled-bin-mohamed-bin-zayed-tahnoon-bin-zayed-chairs-3rd-2025-meeting-of-board-of-directors-of-abu-dhabi-investment-authority/", "category": 1 },
    { "label": "IFSWF member profile, Abu Dhabi Investment Authority", "url": "https://www.ifswf.org/members/abu-dhabi-investment-authority", "category": 2 },
    { "label": "Wikipedia, 'Abu Dhabi Investment Authority'", "url": "https://en.wikipedia.org/wiki/Abu_Dhabi_Investment_Authority", "category": 3 }
  ]
}
```

#### QIA

```json
{
  "id": "QIA",
  "name": "Qatar Investment Authority",
  "country": "Qatar",
  "governance_note": "Established 2005 by Amiri Decision under then-Emir Hamad bin Khalifa Al Thani. Constitutional framework updated by Amiri Decision No. 34 of 2023; board restructured by Amiri Decision No. 14 of 25 March 2026. Wholly owned by the Government of the State of Qatar. Accountable to the Supreme Council for Economic Affairs and Investment, chaired by the Amir. Chair (post-March 2026): Sheikh Bandar bin Mohammed bin Saud Al Thani; Vice Chair: Sheikh Mohammed bin Hamad bin Khalifa Al Thani. Estimated AUM USD 526–557 billion as of 2025 (QIA does not publicly disclose). Founding member of IFSWF; helped draft the 2008 Santiago Principles. Notable entry points into US assets include the January 2026 Goldman Sachs MoU committing up to USD 25 billion across funds and co-investments; the Monumental Sports & Entertainment minority stake (initial June 2023, expanded December 2025); and the xAI Series C (December 2024) and Databricks (January 2025) funding rounds. Decision-making procedures publicly characterised as non-transparent; spending decisions historically linked to the Emir and Prime Minister regardless of board composition.",
  "primary_sources": [
    { "label": "Qatar Investment Authority — official site", "url": "https://www.qia.qa/", "category": 1 },
    { "label": "QIA Governance page", "url": "https://www.qia.qa/en/About/Pages/Governance.aspx", "category": 1 },
    { "label": "Amiri Decision No. 34 of 2023 (constitutional update)", "category": 1 },
    { "label": "Amiri Decision No. 14 of 2026 (board restructuring, 25 March 2026)", "url": "https://qna.org.qa/en/News-Area/News/2026-3/25/hh-the-amir-issues-amiri-decision-restructuring-board-of-directors-of-qatar-investment-authority", "category": 1 },
    { "label": "QIA-Goldman Sachs Asset Management MoU, 20 January 2026", "url": "https://www.goldmansachs.com/pressroom/press-releases/2026/qatar-investment-authority-and-goldman-sachs-sign-mou", "category": 1 },
    { "label": "IFSWF member profile, Qatar Investment Authority", "url": "https://www.ifswf.org/member-profiles/qatar-investment-authority", "category": 2 },
    { "label": "Wikipedia, 'Qatar Investment Authority'", "url": "https://en.wikipedia.org/wiki/Qatar_Investment_Authority", "category": 3 }
  ]
}
```

#### KIA

```json
{
  "id": "KIA",
  "name": "Kuwait Investment Authority",
  "country": "Kuwait",
  "governance_note": "World's oldest sovereign wealth fund, traceable to the Kuwait Investment Board (1953), restructured as the Kuwait Investment Authority by Law No. 47 of 1982. Manages two funds: the General Reserve Fund (state treasury and stabilisation vehicle) and the Future Generations Fund (intergenerational endowment, established 1976; minimum 10% of state revenues mandatorily transferred annually; withdrawal requires legislation). AUM approximately USD 1.029 trillion as of March 2025 (SWFI). Board chaired by the Minister of Finance / State Minister for Economic Affairs and Investment, with Energy Minister, Central Bank Governor, and MoF Undersecretary as ex officio members alongside five private-sector experts (three of whom must hold no other public office), all appointed by Amiri Decree for four-year renewable terms. Statutory secrecy: Law No. 47 Clause 8 prohibits public disclosure of KIA-related information; Clause 9 sets criminal penalties for unauthorised disclosure. Reports annually to the Council of Ministers and to the National Assembly's Standing Committee on Finance and Economic Affairs. Member of IFSWF. Historical governance failures documented in the Grupo Torras / KIO London scandal of the early 1990s.",
  "primary_sources": [
    { "label": "Kuwait Investment Authority — official site", "url": "https://www.kia.gov.kw/", "category": 1 },
    { "label": "KIA About page (governance structure)", "url": "https://www.kia.gov.kw/about-kia/", "category": 1 },
    { "label": "Law No. 47 of 1982 (KIA establishment)", "category": 1 },
    { "label": "IFSWF member profile, Kuwait Investment Authority", "url": "https://www.ifswf.org/member-profiles/kuwait-investment-authority", "category": 2 },
    { "label": "US State Department, '2025 Investment Climate Statements: Kuwait'", "url": "https://www.state.gov/reports/2025-investment-climate-statements/kuwait", "category": 2 },
    { "label": "Wikipedia, 'Kuwait Investment Authority'", "url": "https://en.wikipedia.org/wiki/Kuwait_Investment_Authority", "category": 3 }
  ]
}
```

#### NBIM

```json
{
  "id": "NBIM",
  "name": "Norges Bank Investment Management (Government Pension Fund Global)",
  "country": "Norway",
  "governance_note": "Norges Bank Investment Management is the operational arm of Norges Bank, Norway's central bank, responsible for managing the Government Pension Fund Global on behalf of the Ministry of Finance. AUM NOK 21 trillion (approximately USD 1.85 trillion as of late 2025), the world's largest sovereign wealth fund. Mandate originated as the Government Petroleum Fund (1990); renamed Government Pension Fund-Global in 2006. The Council on Ethics, established 2004 by royal decree, has historically functioned as an independent body monitoring the portfolio and recommending companies for observation or exclusion under criteria covering serious human rights violations, weapons sales to states subject to investment restrictions, severe environmental damage, gross corruption, and other ethical violations, with public exclusion lists maintained at NBIM's responsible-investment portal. Live structural change: in November 2025 the Storting suspended the established ethical framework pending review by a public committee appointed by the King in Council; under the temporary ethical guidelines the Council on Ethics continues to monitor but is instructed not to recommend observation or exclusion, and Norges Bank is to hold off making decisions based on the old guidelines until a new framework is decided. Committee report due 15 October 2026. Reference framework for arm's-length sovereign governance per the Sverdrup Committee report (NOU 2022:12); the November 2025 suspension is the structural caveat to that framework.",
  "primary_sources": [
    { "label": "Norges Bank Investment Management — official site", "url": "https://www.nbim.no/en/", "category": 1 },
    { "label": "NBIM Responsible Investment page (current temporary ethical guidelines notice)", "url": "https://www.nbim.no/en/responsible-investment/", "category": 1 },
    { "label": "Norges Bank submission, 'Government Pension Fund Global – renewed review of responsible investment work and investments in Israeli companies' (18 August 2025)", "url": "https://www.norges-bank.no/en/news-events/news/Submissions/2025/2025-08-18-fin/", "category": 1 },
    { "label": "Norway Ministry of Finance, temporary ethical guidelines and committee mandate (November 2025)", "category": 1 },
    { "label": "Sverdrup Committee Report, NOU 2022:12 (Government Pension Fund Global long-term framework)", "category": 1 },
    { "label": "IPE, 'Norway unveils temporary ethical rules for SWF, sets up panel to revamp code' (November 2025)", "url": "https://www.ipe.com/news/norway-unveils-temporary-ethical-rules-for-swf-sets-up-panel-to-revamp-code/10133579.article", "category": 3 },
    { "label": "Chief Investment Officer, 'Norway Pension Giant's Ethical Investment Policy Placed on Hold by Parliament' (March 2026)", "url": "https://www.ai-cio.com/news/norway-pension-giants-ethical-investment-policy-placed-on-hold-by-parliament/", "category": 3 }
  ]
}
```

#### GIC

```json
{
  "id": "GIC",
  "name": "GIC Private Limited",
  "country": "Singapore",
  "governance_note": "Government of Singapore Investment Corporation (now GIC Private Limited) was incorporated 22 May 1981 under the Companies Act as a private investment company wholly owned by the Government of Singapore. Brainchild of then-Deputy Prime Minister Goh Keng Swee; founding board chaired by then-Prime Minister Lee Kuan Yew. Chairmanship traditionally held by the sitting Prime Minister; current chair is Lawrence Wong (concurrent Prime Minister and Minister for Finance, since 2024). CEO: Lim Chow Kiat. Group CIO: Bryan Yeo (appointed 1 April 2025). Estimated AUM USD 744–800 billion (Forbes/SWFI 2025); GIC does not publicly disclose AUM as a deliberate policy against currency speculation. Fifth Schedule company under the Singapore Constitution; accountable in key areas to the President of Singapore, with the Auditor-General submitting annual audit reports to the President and Parliament. Approximately 80% of portfolio managed in-house. Net Investment Returns Contribution to the Singapore budget estimated at SGD 28.5 billion in FY 2026. Member of IFSWF; alongside NBIM and the better-governed Gulf funds, a calibration point for sovereign-source money operating with technocratic separation from day-to-day political direction.",
  "primary_sources": [
    { "label": "GIC — official site", "url": "https://www.gic.com.sg/", "category": 1 },
    { "label": "GIC 'Who We Are'", "url": "https://www.gic.com.sg/who-we-are/", "category": 1 },
    { "label": "GIC Report on the Management of the Government's Portfolio 2024/25", "url": "https://www.gic.com.sg/uploads/2025/07/GIC_AR_2024-25_PRINT.pdf", "category": 1 },
    { "label": "Prime Minister's Office Singapore, 'PM Lawrence Wong at GIC Insights 2025' (18 November 2025)", "url": "https://www.pmo.gov.sg/newsroom/pm-lawrence-wong-at-gic-insights-2025/", "category": 1 },
    { "label": "Singapore Constitution, Fifth Schedule (GIC accountability framework)", "category": 1 },
    { "label": "National Library Board Singapore, 'Government of Singapore Investment Corporation (GIC)' reference entry", "url": "https://www.nlb.gov.sg/main/article-detail?cmsuuid=ed5d02b0-a615-4a91-a59b-482f94739de4", "category": 2 },
    { "label": "Wikipedia, 'GIC (sovereign wealth fund)'", "url": "https://en.wikipedia.org/wiki/GIC_(Singaporean_sovereign_wealth_fund)", "category": 3 }
  ]
}
```

### 2. `README.md` — no row count change (still 11 entries)

The status row "Sovereign wealth fund registry | 11 entries at /swfs" remains accurate. No edit unless rendering surfaces a copy issue.

### 3. `docs/changelog.md` — new entry above existing 2026-05-07 (later +1)

```markdown
## 2026-05-08

Seven seed sovereign-entities entries (PIF, MUBADALA, ADIA, QIA, KIA, NBIM, GIC) revised with verified governance_notes and primary_sources arrays following the pattern established in Handoff #11. Two findings from the verification pass land in the new notes and warrant methodology-page absorption in a future session:

ADIA's chairmanship is held by Sheikh Tahnoun bin Zayed Al Nahyan, the same individual at the centre of the SC-007 Tahnoon-Aryam transaction and concurrent chair of MGX, G42, and pre-L'imad ADQ. The new ADIA note surfaces this overlap and notes the tension between ADIA's official arm's-length governance language and the institutional reality of Tahnoon's cluster-wide leadership.

NBIM's established ethical framework was suspended by the Storting in November 2025 pending a public committee review; the Council on Ethics is operating under temporary guidelines and is not recommending observation or exclusion. Committee report due 15 October 2026. The new NBIM note retains the fund's reference-framework status while marking the suspension as a live structural caveat. The methodology page's calibration-point treatment of NBIM should be revisited once the committee reports.

Other notable updates absorbed: PIF 2026-2030 strategy approved 15 April 2026; QIA board reshuffled by Amiri Decision No. 14 of 25 March 2026 (chair Sheikh Bandar bin Mohammed bin Saud Al Thani); GIC chairmanship transitioned to Lawrence Wong with the Prime Minister handover; Mubadala AUM now USD 385 billion per its own disclosure; KIA AUM USD 1.029 trillion per March 2025 SWFI ranking.

Defined terms unchanged.
```

## Verification

```bash
cd web
npm run build
```

Confirm: TypeScript compiles unchanged (no schema work); JSON parses; `/swfs` prerenders.

After build, run `npm run dev` and visit:
- `/swfs` — confirm all 11 entries render; the seven seed entries now display primary_sources lists below their governance_notes, matching the format used for ADQ, MGX, PIA, LIMAD
- spot-check ADIA and NBIM specifically for the live structural-finding language landing correctly
- counter at `/` still reads "8 records · 2 live"; no record-side changes in this handoff

## Commit suggestion

Single commit (data only, no schema or template work):

```
feat(data): verify and cite the seven seed sovereign-entities entries

Rewrites governance_note and adds primary_sources for PIF, MUBADALA,
ADIA, QIA, KIA, NBIM, GIC matching the Handoff #11 verification pattern.
Two structural findings land in the new notes: ADIA chairmanship sits
with Sheikh Tahnoun bin Zayed (SC-007 overlap); NBIM ethical framework
suspended by Storting November 2025 pending committee review (report
due October 2026). Other updates absorb 2025-2026 governance and AUM
movements across the cluster.
```

Push and paste `git log --oneline -3`.
