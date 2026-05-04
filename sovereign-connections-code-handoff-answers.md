# Sovereign Connections — Code Handoff Answers

Follow-up to `sovereign-connections-code-handoff.md`. Answers the two items Code raised before scaffolding.

## Layout: Option B

Next.js in `web/`, Python collectors stay at root, Vercel project root set to `web/`. Confirms Code's default. The data lifecycle (Python writes JSON, TypeScript reads JSON via `import data from '../../data/records.json'`) is the right separation. Collectors and dashboard have different lifecycles and toolchains and shouldn't share a `package.json`.

Resulting tree:

```
sovereign-connections/
├── README.md
├── PROJECT.md
├── collectors/             (Python, existing stubs)
├── data/                   (canonical JSON, written by Python, read by web/)
├── docs/
│   └── handoffs/
├── .github/workflows/
└── web/                    (Next.js 15 app, Vercel root)
    ├── app/
    ├── components/
    ├── lib/
    ├── package.json
    └── ...
```

## TypeScript types

`web/lib/types.ts`:

```ts
export type Scope = 'LIVE' | 'COMP' | 'LITIG' | 'OOS';

export type Framework =
  | 'EMOL'    // foreign Emoluments Clause
  | 'FARA'    // 22 USC 611-621
  | 'FIRRMA'  // FIRRMA / CFIUS
  | 'OGE'     // 5 CFR Part 2635, 2640
  | 'LDA'     // 2 USC 1601-1614
  | '7031'    // State Dept 7031(c)
  | '208';    // 18 USC 208

export type Source =
  | 'PIF' | 'MUBADALA' | 'ADIA' | 'QIA' | 'KIA' | 'NBIM' | 'GIC'
  | 'CHN' | 'MULTI' | 'NONE' | 'NA';

export type EvidenceCategory = 1 | 2 | 3 | 4 | 5;

export interface SovereignRecord {
  id: string;
  business: string;
  family_member: string;
  scope: Scope;
  source: Source;
  period: string;
  frameworks: Framework[];
  evidence_category: EvidenceCategory[];
  summary: string;
  documented_amount?: string;
  primary_sources?: PrimarySource[];
}

export interface PrimarySource {
  label: string;
  url?: string;
  category: EvidenceCategory;
}

export interface SovereignEntity {
  id: string;
  name: string;
  country: string;
  governance_note: string;
}
```

## Seed data

`data/records.json`:

```json
[
  {
    "id": "SC-001",
    "business": "Affinity Partners",
    "family_member": "Jared Kushner",
    "scope": "COMP",
    "source": "PIF",
    "period": "2021-PRES",
    "frameworks": ["EMOL", "FIRRMA", "OGE", "208"],
    "evidence_category": [2],
    "summary": "The closest documented direct analogue to the post-2025 fact pattern. SEC filings establish the financial interest; NYT and FT reporting establish the PIF source. Pre-2025 timing places it in the comparative set rather than the live tracker.",
    "documented_amount": "$2 billion"
  },
  {
    "id": "SC-002",
    "business": "Trump Organization foreign-government bookings",
    "family_member": "Donald Trump (and family beneficial interests)",
    "scope": "COMP",
    "source": "MULTI",
    "period": "2017-2020",
    "frameworks": ["EMOL", "OGE"],
    "evidence_category": [1, 2, 3],
    "summary": "First-term hospitality-revenue fact pattern. CREW reporting, House Oversight Committee documents, and the underlying foreign Emoluments litigation established the records. Comparative for methodology calibration on what counts as a foreign government official acting in official capacity payment.",
    "documented_amount": "Various"
  },
  {
    "id": "SC-003",
    "business": "Ivanka Trump China trademarks",
    "family_member": "Ivanka Trump",
    "scope": "COMP",
    "source": "CHN",
    "period": "2017-2018",
    "frameworks": ["EMOL", "FARA"],
    "evidence_category": [2],
    "summary": "Tests the state-grant-as-payment framing. Trademarks were awarded by a Chinese state IP office on a non-routine timeline coinciding with her White House role. Comparative reference for whether non-cash sovereign benefits register as foreign Emoluments Clause flows.",
    "documented_amount": "18+ trademarks granted"
  },
  {
    "id": "SC-004",
    "business": "DC and Maryland v. Trump",
    "family_member": "(foreign Emoluments Clause litigation)",
    "scope": "LITIG",
    "source": "NA",
    "period": "2017-2021",
    "frameworks": ["EMOL"],
    "evidence_category": [1],
    "summary": "Anchor case for the foreign Emoluments Clause modern doctrinal posture. Reached the Fourth Circuit on standing and zone-of-interests; vacated and remanded as moot in January 2021 after Trump left office. The case law on emolument definition still governs the framework this tracker uses."
  },
  {
    "id": "SC-005",
    "business": "Blumenthal v. Trump",
    "family_member": "(congressional standing case)",
    "scope": "LITIG",
    "source": "NA",
    "period": "2017-2020",
    "frameworks": ["EMOL"],
    "evidence_category": [1],
    "summary": "DC Circuit held individual members of Congress lacked standing to sue over foreign Emoluments Clause violations absent institutional authorization. Load-bearing for any future enforcement challenge."
  },
  {
    "id": "SC-006",
    "business": "Burisma board engagement",
    "family_member": "Hunter Biden",
    "scope": "OOS",
    "source": "NONE",
    "period": "2014-2019",
    "frameworks": ["FARA", "LDA"],
    "evidence_category": [1, 2, 3],
    "summary": "Documented for methodology completeness as the case the framework excludes despite political salience. Burisma is a Cyprus-registered private holding company; no Ukrainian state ownership in the documented record. State ties run through the owner's prior ministerial tenure, not through ownership structure. The exclusion is symmetrical: a Republican-side analogue with the same facts would also fall outside scope.",
    "documented_amount": "~$3.4M to Rosemont Seneca Bohai LLC (entity-level inflows)"
  }
]
```

`data/sovereign_entities.json`:

```json
[
  {
    "id": "PIF",
    "name": "Public Investment Fund",
    "country": "Saudi Arabia",
    "governance_note": "Effectively the crown prince's investment vehicle. Chaired by MBS since 2015. Board composition and major investment decisions track royal-court priorities; the institutional separation between fund and state is thin compared to other listed SWFs."
  },
  {
    "id": "MUBADALA",
    "name": "Mubadala Investment Company",
    "country": "United Arab Emirates",
    "governance_note": "Sovereign with more institutional separation than PIF. Chaired by MBZ. Operates as an investment institution with named CEOs and published annual reports. The sovereign character is real; the governance gap between fund and state is narrower than NBIM but wider than PIF."
  },
  {
    "id": "ADIA",
    "name": "Abu Dhabi Investment Authority",
    "country": "United Arab Emirates",
    "governance_note": "Conservative governance norms. Rarely takes activist or operational positions in portfolio companies. Discloses limited operational detail compared to NBIM. Treated as sovereign for tracker purposes despite the lower public profile."
  },
  {
    "id": "QIA",
    "name": "Qatar Investment Authority",
    "country": "Qatar",
    "governance_note": "Royal-family controlled. Board chaired by the Emir. Investment activity tracks royal-court priorities including high-profile real estate and sports holdings."
  },
  {
    "id": "KIA",
    "name": "Kuwait Investment Authority",
    "country": "Kuwait",
    "governance_note": "Parliamentary oversight in theory. Managing director system in practice. The Kuwaiti National Assembly holds nominal oversight authority; the operational fund is run by professional managers with limited direct political interference relative to GCC peers."
  },
  {
    "id": "NBIM",
    "name": "Norges Bank Investment Management / Government Pension Fund Global",
    "country": "Norway",
    "governance_note": "Statutorily independent. Published ethics guidelines. Public exclusion lists naming companies the fund will not invest in. The strongest governance separation in the SWF universe; useful as a calibration point for what sovereign-source money looks like when the fund operates at arm's length from the state."
  },
  {
    "id": "GIC",
    "name": "GIC Private Limited",
    "country": "Singapore",
    "governance_note": "Technocratic governance. Chairman traditionally the sitting prime minister. Operates with formal investment-committee structures and named CEOs. Sovereign character documented; institutional separation between fund and state intermediate."
  }
]
```

`data/candidates.json` and `data/connected_businesses.json` stay as `[]` for v0. Candidate-review and standalone business-registry workflows aren't needed pre-launch.

## Notes

Period strings normalized to ASCII hyphens (`2021-PRES`, not `2021–PRES`) for cross-system safety. If the rendered UI wants en-dashes for typographic reasons, format at render time, not in the data.

The full visual spec (filter strips, column grid, status pill colors, expanded-row layout, bottom legend) is in the original `sovereign-connections-code-handoff.md` under "What was settled in the prior chat." Reference that section if anything below the data layer is ambiguous.
