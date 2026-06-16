# Handoff #39 — SC-001 through SC-006 evidence backfill, slice 1: litigation pair, Affinity dedup

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-39-evidence-backfill-slice-1.md`
**Depends on:** Handoff #38 (PrimarySource variants, PR #15 merged into `main`). Every variant used here is already active: `court_filing` since #21, `press_disclosure` since #21, `congressional_document` since #38. Branch off `main`.
**Type:** data. Edits `web/data/records.json` and `docs/references/sc-001-006-evidence-worksheet.md`. No `web/lib/types.ts` change (no new variant), no collector change, no UI change.

## What this does

First records-layer slice of the SC-001-006 evidence backfill. Three actions, all against records that already exist:

1. SC-004 and SC-005 gain `court_filing` primary sources, verified against the court record.
2. SC-009 gets three of its existing generic press/congressional entries replaced with dated, URL-bearing versions.
3. SC-001 is retired into SC-009. It carried no `primary_sources`, frameworks identical to SC-009, and a `$2B` amount already subsumed by SC-009.

SC-002, SC-003, and SC-006 are not in this slice. They stay queued for slice 2.

## Background on the SC-001 / SC-009 decision

SC-001 (Affinity Partners, COMP) and SC-009 (A Fin Management LLC / Affinity Partners, LIVE) are the same business on the same money. SC-009's summary already runs from 2021 to present and carries the 2021 PIF origination in full, screening-panel override included, with the House Oversight, Senate Finance, and NYT sources cited inline. SC-001's three-sentence summary pointed at "SEC filings" (the ADV, already on SC-009) and "NYT and FT reporting" (the PIF source). The NYT leg is on SC-009. The FT leg did not resolve to a distinct article: the screening-panel account is the New York Times exclusive, attributed by every other outlet to the Times, and no separate FT piece with a citable byline, date, or URL was located. SC-001 had nothing SC-009 lacked, so it is retired rather than split. The SC-001 ID stays retired and unused. SC-002 through SC-009 are not renumbered, because closing one slot would churn every downstream reference (W-002 points at SC-009, plus any cross-refs and external links) for no gain, and a documented retired ID is more transparent than a silent shift.

## What Code needs to do

### Step 1: SC-004 court_filing sources

Add these two entries to SC-004's `primary_sources` array (create the array if absent). Two entries because the summary spans two stages, the Fourth Circuit en banc proceeding and the Supreme Court vacatur.

```json
{
  "type": "court_filing",
  "label": "In re Trump (DC and Maryland v. Trump), 958 F.3d 274 (4th Cir. 2020) (en banc). Full court denied the President's petition for a writ of mandamus and allowed the foreign Emoluments Clause claims to proceed. D. Md. No. 8:17-cv-01596 (Messitte, J.), decided May 14, 2020.",
  "url": "https://clearinghouse.net/case/15881/",
  "category": 1,
  "retrieved_at": "2026-06-16"
},
{
  "type": "court_filing",
  "label": "Trump v. District of Columbia, No. 20-331, 141 S. Ct. 1262 (2021) (mem.). Cert granted, judgment vacated, case remanded to the Fourth Circuit with instructions to dismiss as moot under Munsingwear, January 25, 2021. Fourth Circuit vacatur 838 F. App'x 789 (4th Cir. 2021); D. Md. case closed May 11, 2021.",
  "url": "https://clearinghouse.net/case/15881/",
  "category": 1,
  "retrieved_at": "2026-06-16"
}
```

SC-004's `evidence_category` is already `[1]` and stays `[1]`. Do not change it.

### Step 2: SC-005 court_filing source

Add this one entry to SC-005's `primary_sources` array. The cert denial sits inside the label rather than as a second entry, because the load-bearing fact is that this opinion survived the 2021 moot-vacatur wave.

```json
{
  "type": "court_filing",
  "label": "Blumenthal v. Trump, 949 F.3d 14 (D.C. Cir. 2020) (per curiam). The D.C. Circuit held that individual members of Congress lack standing to sue over the Foreign Emoluments Clause absent institutional authorization. No. 19-5237, decided February 7, 2020; cert denied, 141 S. Ct. 553 (2020). D.D.C. No. 1:17-cv-01154 (Sullivan, J.). Not vacated in the 2021 moot-vacatur wave; remains good law on legislative standing.",
  "url": "https://clearinghouse.net/case/15893/",
  "category": 1,
  "retrieved_at": "2026-06-16"
}
```

SC-005's `evidence_category` is already `[1]` and stays `[1]`. Do not change it.

### Step 3: SC-009 source enrichment

Replace three existing entries in SC-009's `primary_sources` array. Match each on the distinctive opening of its current `label`, not on array index. Replace the whole entry object with the version given. The other three SC-009 entries (the two `sec_filing` ADV entries and any others) are untouched. SC-009's `evidence_category` stays `[1, 2, 3]`.

Match the entry whose label begins `House Committee on Oversight and Reform correspondence on the PIF`. Replace it with:

```json
{
  "type": "congressional_document",
  "document_type": "letter",
  "chamber_or_committee": "House Committee on Oversight and Reform",
  "document_date": "2022-06-02",
  "label": "House Oversight Chairwoman Carolyn Maloney, letter to Jared Kushner opening the committee probe of the Saudi PIF investment in A Fin Management LLC (Affinity), June 2, 2022. States the $2B PIF raise and Affinity's filing-indicated roughly $25M per year in management fees, and notes Affinity was incorporated in Delaware on January 21, 2021, the day after the first administration ended.",
  "url": "https://oversightdemocrats.house.gov/news/press-releases/chairwoman-maloney-launches-probe-of-saudi-government-s-2-billion-investment-in",
  "category": 2,
  "retrieved_at": "2026-06-16"
}
```

Match the entry whose label begins `NYT reporting on the ~$2B PIF anchor commitment`. Replace it with:

```json
{
  "type": "press_disclosure",
  "label": "David D. Kirkpatrick and Kate Kelly, 'Before Giving Billions to Jared Kushner, Saudi Investment Fund Had Big Doubts,' The New York Times, April 10, 2022. Documents-based account of the PIF screening panel recommending rejection (firm inexperience, an asset-management fee it called excessive, public-relations risk from Kushner's prior White House role) and the full PIF board under Mohammed bin Salman overruling it days later.",
  "category": 3,
  "retrieved_at": "2026-06-16"
}
```

The canonical nytimes.com URL is paywalled and was not captured; leave `url` off this entry until it is pinned. Tracked as a disclosed gap below.

Match the entry whose label begins `Reuters reporting that the Qatar Investment Authority`. Replace it with:

```json
{
  "type": "press_disclosure",
  "label": "Iain Withers, 'Kushner's Affinity's assets jump to $4.8 billion after Gulf cash injection,' Reuters, January 2025. Reports the $1.5B 2024 commitment from the Qatar Investment Authority and Abu Dhabi's Lunate, per Kushner's December 2024 podcast remarks and the A Fin Management ADV. Corroborated by Bloomberg, 'Kushner's Affinity Gets Additional $1.5 Billion From Qatar, Abu Dhabi's Lunate,' December 20, 2024.",
  "url": "https://www.bloomberg.com/news/articles/2024-12-20/jared-kushner-s-affinity-gets-1-5-billion-more-from-qatar-abu-dhabi-s-lunate",
  "category": 3,
  "retrieved_at": "2026-06-16"
}
```

### Step 4: Retire SC-001

Remove the SC-001 object from `web/data/records.json` in full. Do not renumber any other record. SC-002 through SC-009 keep their IDs.

Before removing, grep the repo for any reference to `SC-001` outside `web/data/records.json` (methodology page, README, other docs, the worksheet, the watchlist). List every hit in the report. Repoint references that named SC-001 as the Affinity comparator to SC-009; flag any reference whose intent is unclear rather than guessing.

### Step 5: Update the evidence worksheet

In `docs/references/sc-001-006-evidence-worksheet.md`, replace the body of the `## SC-001 — Affinity Partners` section with a retirement note: SC-001 retired into SC-009 per Handoff #39; its SEC-filing and NYT evidence resolved into SC-009; the FT leg of its summary did not resolve to a distinct citable article and is recorded as a disclosed gap. Keep the section header so the worksheet still reads SC-001 through SC-006 in order. Leave the SC-002 through SC-006 sections unchanged.

### Step 6: Verify before reporting back

- `web/data/records.json` is valid JSON.
- Record IDs present are exactly SC-002, SC-003, SC-004, SC-005, SC-006, SC-007, SC-008, SC-009. SC-001 is gone. No record was renumbered.
- SC-004 has two new `court_filing` entries; SC-005 has one; all carry `category: 1`.
- SC-009 has exactly three replaced entries (one `congressional_document`, two `press_disclosure`), the rest of its array unchanged, and `evidence_category` still `[1, 2, 3]`.
- No `label` anywhere in the new or replaced entries contains an em-dash or en-dash (PROJECT.md house rule).
- The grep for `SC-001` references is run and its hits are listed in the report.
- The worksheet's SC-001 section is a retirement note and SC-002 through SC-006 are unchanged.

### Step 7: Commit

Single commit covering `web/data/records.json`, the worksheet, and this handoff doc. Suggested message:

```
data(records): backfill SC-004/005 court filings, enrich SC-009, retire SC-001 into SC-009 (#39)
```

Do not push unless asked.

## Disclosed gaps recorded by this handoff

- SC-009 NYT entry: canonical nytimes.com URL for the April 10, 2022 Kirkpatrick and Kelly piece is paywalled and not yet pinned. Byline, title, and date are verified.
- SC-001 FT leg: no distinct Financial Times article establishing the PIF source independent of the NYT was located. Recorded as a gap on the SC-001 retirement note rather than asserted.

## Out of scope

- SC-002, SC-003, SC-006 sourcing (slice 2).
- Any schema or `web/lib/types.ts` change. Every variant used already exists.
- Renumbering SC-002 through SC-009.
- Reformatting SC-009's pre-existing entries or summary. See the flag-back below.
- UI and collector changes.

## Flag back, do not decide

- SC-009's existing `sec_filing` entries and its `summary` contain em-dashes against the PROJECT.md no-em-dash rule. Not touched here. Flag if you want a separate hygiene pass; do not fold it into this commit.
- Any `SC-001` reference whose repoint target is ambiguous (a methodology passage that used SC-001 to make a comparative point that SC-009 does not frame the same way). Surface it; do not rewrite methodology prose in a data commit.
- If SC-004 or SC-005 already carries a `primary_sources` array with content (it should not, both read absent on disk), surface what is there rather than overwriting.

---

read docs/handoffs/2026-06-16-handoff-39-evidence-backfill-slice-1.md and follow
