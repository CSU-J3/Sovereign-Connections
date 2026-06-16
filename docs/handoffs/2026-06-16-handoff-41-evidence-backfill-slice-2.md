# Handoff #41 — SC-001 through SC-006 evidence backfill, slice 2: SC-002, SC-003, SC-006

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-41-evidence-backfill-slice-2.md`
**Depends on:** Handoffs #39 and #40 (slice 1, SC-001 retirement and walk repoint). Branch off `main` once the slice-1 PR has merged, so the two branches do not edit `web/data/records.json` in parallel. Slice 2 touches only SC-002, SC-003, and SC-006, which slice 1 did not touch, so there is no content overlap; the only shared file is `records.json`. If slice 1 has not merged, branch off `feat/evidence-backfill-slice-1` and say so in the report.
**Type:** data. Edits `web/data/records.json` only. No `web/lib/types.ts` change (every variant exists), no UI change, no collector change.

## What this does

Second records-layer slice of the SC-001-006 evidence backfill. Adds sourced `primary_sources` to the three records the worksheet left for research: SC-002, SC-003, SC-006. All three currently have no `primary_sources` field. Every variant used is already active: `court_filing`, `press_disclosure` (since #21), `congressional_document`, `advocacy_report`, `corporate_registration` (since #38).

This closes the SC-001-006 backfill. SC-001 was retired in #39; SC-004 and SC-005 were sourced in #39; SC-007 and SC-008 were already on the schema.

## Evidence-tier note, read before Step 3

Each new source carries a `category` (the integer evidence tier). The values below follow the convention visible in SC-009's deployed sources: official filing or registry record and court record at tier 1, congressional document at tier 2, press at tier 3, advocacy or watchdog report at tier 4. PROJECT.md holds the authoritative tier definitions, which were not in hand when this was drafted. If they differ, the per-source `category` values and the `evidence_category` reconciliation in Step 4 need adjusting. Flagged, not assumed.

## What Code needs to do

### Step 1: SC-002 sources

Add these three entries to SC-002's `primary_sources` array (create the array). The worksheet flagged whether the "underlying foreign Emoluments litigation" pointed at SC-004/005 or a separate hospitality-revenue suit. It resolves to CREW v. Trump, the first-filed emoluments case brought by hospitality plaintiffs, distinct from SC-004 though closely analogous.

```json
{
  "type": "court_filing",
  "label": "Citizens for Responsibility and Ethics in Washington v. Trump, 953 F.3d 178 (2d Cir. 2019). The Second Circuit reinstated the first foreign Emoluments Clause suit, holding the hospitality plaintiffs (CREW, ROC United, Eric Goode, Jill Phaneuf) had competitor standing over foreign-government patronage of Trump properties. S.D.N.Y. No. 1:17-cv-00458 (Daniels, J.), decided September 13, 2019. Rehearing en banc denied, 971 F.3d 102 (2d Cir. 2020), five judges dissenting; vacated as moot, Trump v. CREW, No. 20-330, 141 S. Ct. 1262 (2021). Distinct from SC-004 (D.C. and Maryland) though closely analogous.",
  "url": "https://clearinghouse.net/case/15957/",
  "category": 1,
  "retrieved_at": "2026-06-16"
},
{
  "type": "advocacy_report",
  "organization": "Citizens for Responsibility and Ethics in Washington (CREW)",
  "published_at": "2018-01",
  "label": "CREW, 'Profiting from the Presidency' (year-one report, January 2018). Documented at least 11 foreign governments patronizing Trump businesses and 40 special-interest events at Trump properties in the first year, the Trump International Hotel in Washington prominent among them.",
  "url": "https://www.citizensforethics.org/reports-investigations/crew-reports/profiting-from-the-presidency/",
  "category": 4,
  "retrieved_at": "2026-06-16"
},
{
  "type": "congressional_document",
  "document_type": "report",
  "chamber_or_committee": "House Committee on Oversight and Accountability (Democratic minority staff)",
  "document_date": "2024-01-04",
  "label": "House Oversight Democratic minority staff report, 'White House for Sale: How Princes, Prime Ministers, and Premiers Paid Off President Trump,' January 4, 2024, 156 pages. Found at least $7.8M in payments from 20-plus foreign governments and state-owned entities to four Trump properties (Trump International Hotel Washington, Trump International Hotel Las Vegas, Trump World Tower and Trump Tower New York) over 2017-2018, drawn from Mazars USA records obtained through litigation; China the largest source at roughly $5.6M. Ranking Member Raskin foreword.",
  "category": 2,
  "retrieved_at": "2026-06-16"
}
```

The "White House for Sale" report PDF URL on the House Oversight Democrats site was not pinned in this pass; leave `url` off the congressional entry until it is confirmed. Disclosed gap below.

### Step 2: SC-003 sources

Add these three entries to SC-003's `primary_sources` array (create the array).

```json
{
  "type": "corporate_registration",
  "registration_type": "trademark",
  "registry": "China Trademark Office, State Administration for Industry and Commerce (SAIC); trademark functions reorganized into the China National Intellectual Property Administration (CNIPA) in 2018",
  "jurisdiction": "China",
  "label": "China Trademark Office grants to Ivanka Trump Marks LLC, 2017-2018. Grant clusters coincided with administration policy events: provisional approvals around April 6, 2017 (the day Ivanka Trump and Jared Kushner dined with Xi Jinping at Mar-a-Lago); registration and first-trial approvals in May and June 2018 around the ZTE sanctions reversal and a contemporaneous reported $500M Chinese loan to a Trump Organization-linked Indonesia project; and 18 further marks granted to Trump and Ivanka-linked companies over October to November 2018, bringing the year total to roughly 34. Applicant Ivanka Trump Marks LLC. Individual registration numbers are held in the registry database but were not published in the source reporting (disclosed gap).",
  "category": 1,
  "retrieved_at": "2026-06-16"
},
{
  "type": "press_disclosure",
  "label": "Associated Press reporting on the China trademark grants to Ivanka Trump Marks LLC (Erika Kinetz), 2017-2019, establishing the counts and the timing relative to trade negotiations and the ZTE reversal; the May 2018 cluster reported May 28, 2018 and the 18-marks-in-two-months tally reported November 2018.",
  "url": "https://www.cbsnews.com/news/ivanka-trump-receives-5-trademarks-from-china-amid-trade-talks/",
  "category": 3,
  "retrieved_at": "2026-06-16"
},
{
  "type": "advocacy_report",
  "organization": "Citizens for Responsibility and Ethics in Washington (CREW)",
  "published_at": "2018-05",
  "label": "CREW trademark-database reviews flagging the timing of the China grants relative to Trump administration China policy, 2018; the May 2018 registration approvals coinciding with the ZTE announcement noted as the worked example.",
  "url": "https://www.citizensforethics.org/reports-investigations/crew-investigations/ivanka-trumps-business-wins-approval-for-more-china-trademarks/",
  "category": 4,
  "retrieved_at": "2026-06-16"
}
```

### Step 3: SC-006 sources

Add these three entries to SC-006's `primary_sources` array (create the array). SC-006 is the out-of-scope worked example, so its sources document the basis for exclusion rather than a sovereign nexus.

```json
{
  "type": "corporate_registration",
  "registration_type": "company_registry",
  "registry": "Cyprus Department of Registrar of Companies and Official Receiver (DRCOR)",
  "jurisdiction": "Cyprus",
  "identifier": "HE186236",
  "filed_at": "2006-10-26",
  "label": "Burisma Holdings Limited, Cyprus registration HE186236, Department of Registrar of Companies and Official Receiver. Incorporated as a Cyprus private limited company on October 26, 2006; registered office in Limassol; status dissolution following voluntary liquidation, dissolved February 16, 2023. Owned by Brociti Investments Limited (Mykola Zlochevsky). The registry record shows private ownership with no Ukrainian state shareholding, the documentary basis for the out-of-scope classification.",
  "url": "https://opencorporates.com/companies/cy/HE186236",
  "category": 1,
  "retrieved_at": "2026-06-16"
},
{
  "type": "congressional_document",
  "document_type": "report",
  "chamber_or_committee": "Senate Committee on Homeland Security and Governmental Affairs and Senate Committee on Finance (majority staff, joint)",
  "document_date": "2020-09-23",
  "label": "Senate HSGAC and Finance majority staff joint report, 'Hunter Biden, Burisma, and Corruption: The Impact on U.S. Government Policy and Related Concerns,' September 23, 2020. Characterizes the Burisma board compensation and related financial flows. Cited for the documented-record basis of the case, not for a sovereign nexus, which the report does not establish.",
  "category": 2,
  "retrieved_at": "2026-06-16"
},
{
  "type": "press_disclosure",
  "label": "Reuters review of bank records reporting that Burisma sent approximately $3.4 million to Rosemont Seneca Bohai LLC between April 2014 and November 2015, the entity-level inflow behind the documented_amount. Reuters noted it could not independently verify the documents or how much Hunter Biden personally received.",
  "category": 3,
  "retrieved_at": "2026-06-16"
}
```

The Senate HSGAC report URL (hsgac.senate.gov) and the underlying Reuters story URL were not pinned in this pass; leave `url` off those two entries until confirmed. Disclosed gaps below.

### Step 4: Evidence-category reconciliation

The new sources introduce tiers the records' `evidence_category` arrays do not currently list:

- SC-002 is `[1, 2, 3]`. The new `advocacy_report` (CREW) is tier 4 under the SC-009 convention, so the consistent array is `[1, 2, 3, 4]`.
- SC-003 is `[2]`. The sourced evidence is tier 1 (registry), tier 3 (AP), tier 4 (CREW), so the consistent array is `[1, 3, 4]`. The current `[2]` matches none of the sourced tiers.
- SC-006 is `[1, 2, 3]` and the three new sources are tiers 1, 2, 3. No change needed.

Following the #39 posture, do not change any `evidence_category` array in this commit. Surface the SC-002 and SC-003 mismatches in the report. Corey confirms the tier scheme against PROJECT.md and decides whether the reconciliation rides here or in a follow-up.

### Step 5: Verify before reporting back

- `web/data/records.json` is valid JSON.
- SC-002 has three new sources (`court_filing`, `advocacy_report`, `congressional_document`); SC-003 has three (`corporate_registration`/`trademark`, `press_disclosure`, `advocacy_report`); SC-006 has three (`corporate_registration`/`company_registry`, `congressional_document`, `press_disclosure`).
- Every `congressional_document` carries a valid `document_type`; every `corporate_registration` a valid `registration_type`.
- No `label` in any new entry contains an em-dash or en-dash.
- No `evidence_category` array was changed.
- Records other than SC-002, SC-003, SC-006 are untouched.

### Step 6: Commit

Single commit, `web/data/records.json` plus this handoff doc. Suggested message:

```
data(records): backfill SC-002/003/006 primary sources, close SC-001-006 evidence pass (#41)
```

Do not push unless asked.

## Disclosed gaps recorded by this handoff

- SC-003 individual trademark registration numbers: held in the CNIPA / China Trademark Office database, not published by AP or CREW, so the `corporate_registration` entry names the registry and the grant clusters but no `identifier`. Closing this needs a direct CNIPA database pull.
- SC-002 House Oversight "White House for Sale" report PDF URL: not pinned. Title, committee, date, page count, and headline figure verified.
- SC-006 Senate HSGAC joint report URL and the Reuters Burisma bank-records story URL: not pinned. Both are described accurately from the working Burisma reference; pin before publishing.
- SC-006 incorporation date: the registry shows the Cyprus entity HE186236 incorporated October 26, 2006. Secondary sources and the working reference give a 2002 founding for the business. Both are recorded: 2006 is the Cyprus registration, 2002 the business founding.

## Out of scope

- Any `evidence_category` change (Step 4 is a flag, not an edit).
- Any `web/lib/types.ts` or schema change. Every variant used exists.
- ADV candidate promotion (CAND-169 onward) and the `form_adv` records-layer work.
- UI and collector changes.

## Flag back, do not decide

- SC-002 could carry a second congressional document: the October 2021 House Oversight disclosure that the Trump International Hotel Washington took roughly $3.7M from foreign governments, drawn from GSA records, which predates the 2024 Mazars-based report. Not added here because the 2024 report covers the same ground at greater scope. Add it if a second congressional anchor is wanted.
- The SC-006 `press_disclosure` for the Reuters figure: the worksheet also asked whether Rosemont Seneca Bohai LLC's own corporate registration becomes a separate `corporate_registration` entry. Not added, because the out-of-scope rationale turns on Burisma's ownership structure, not Rosemont Seneca Bohai's. Surface if you want it.
- The CREW "Profiting from the Presidency" exact publication day: recorded as January 2018 (year-one report). Tighten to the exact date if wanted.

---

read docs/handoffs/2026-06-16-handoff-41-evidence-backfill-slice-2.md and follow
