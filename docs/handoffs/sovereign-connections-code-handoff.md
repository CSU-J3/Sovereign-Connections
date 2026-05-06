# Sovereign Connections — Code Handoff

Paste this as the opening message of the next chat (Claude Code session, or new Claude.ai chat with Code Execution turned on).

## Where things stand

The repo at github.com/CSU-J3/Sovereign-Connections is scaffolded (README, PROJECT.md, empty data JSON arrays, six Python collector stubs raising NotImplementedError). Status remains pre-launch. No records collected.

In the prior Claude.ai chat, two dashboard iterations were built in the visualizer. The first was a soft, oversight-tracker card layout. It was rejected. The second matched the cbt aesthetic (github.com/CSU-J3/cbt) and was approved. This handoff converts that approved visual into a working Next.js app, deployed on Vercel, matching the cbt stack pattern.

The methodology writing thread is sequenced separately. Post one is the methodology essay. Post two is the Burisma worked example. The 7031(c) section was drafted as a warm-up in the prior chat. None of that is in scope for this handoff.

## What was settled in the prior chat

The stack matches cbt exactly. Next.js 15 App Router, TypeScript, Tailwind v4, Turso (libSQL) when collectors come online, Vercel hosting and Cron when there is anything to schedule. Same directory layout: `app/`, `components/`, `lib/`, `scripts/`, `.claude/skills/sovereign-connections/`, `docs/handoffs/`.

The approved visual is terminal-style. Specifics so the next session does not re-decide:

- Mono font (`var(--font-mono)` or Tailwind `font-mono`) throughout the records area for codes, IDs, dates, scope and source labels. Sans for the prose summary inside expanded rows.
- Header. `SC // SOVEREIGN CONNECTIONS` left, `★ SWFs · N records · 0 live · pre-launch` right. Single border-bottom rule below.
- Three filter strips, in this order, each with a small uppercase label on the left:
  - SCOPE (single-select). Buttons: `ALL · LIVE · COMPARATIVE · LITIGATION · OUT-OF-SCOPE`. Default `ALL` active.
  - FRAMEWORK (multi-select). Buttons: `EMOL · FARA · FIRRMA · OGE · LDA · 7031 · §208`.
  - SOURCE (multi-select). Buttons: `PIF · MUBADALA · ADIA · QIA · CHN · MULTI`.
- Active button styling. Inverted colors (filled background, light text) on active. Inactive buttons have 0.5px borders, transparent fill, hover shifts to a secondary background.
- Column header row. Six columns: chevron (14px) · ID (56px) · BUSINESS / FAMILY MEMBER (flex) · SCOPE (64px) · PERIOD (80px) · SOURCE (70px). Small uppercase letterspaced labels.
- Row layout matches the column grid. Click anywhere on the row toggles expand. Expanded row reveals: 2-4 sentence analyst-voice summary; FRAMEWORKS line; EVIDENCE line (category and source type); a `Walk the definition ↗` button on records where it applies (Affinity, Trump Org, Burisma).
- Status pill colors (must work in light and dark mode, use Tailwind semantic tokens or equivalents):
  - COMP: neutral gray
  - LITIG: blue (info)
  - OOS: coral (danger-muted)
  - LIVE: green (success). No records use this yet.
- Bottom legend. Two lines. Line one explains the status codes. Line two expands the framework abbreviations (EMOL = foreign Emoluments Clause; FARA = 22 USC 611; FIRRMA = CFIUS; OGE = 5 CFR 2635; LDA = 2 USC 1601; 7031 = State 7031(c); §208 = 18 USC 208).
- Empty state. Hidden by default. Shown when filters return zero records: "No records match the active filters."

The walk-the-definition buttons issue prompts back to Claude. Examples:
- Affinity Partners: "Walk the sovereign-adjacent definition through the Affinity Partners record using PROJECT.md categories."
- Burisma: "Apply the sovereign-adjacent definition to the Burisma case step by step using the working reference in project knowledge."

In a real Next.js app these become either (a) buttons that copy a prompt to clipboard with a Claude.ai deep link, or (b) buttons that route to a `/record/[id]/walk` page with the prompt prefilled. Either is fine. The button must be present and labeled `Walk the definition ↗`.

## Routes

- `/` — main records dashboard with filters and expandable rows
- `/record/[id]` — individual record detail page (frameworks, evidence chain, primary-source links if any)
- `/swfs` — sovereign wealth fund registry (PIF, Mubadala, ADIA, QIA, KIA, NBIM, GIC entries with one-paragraph governance notes each)
- `/methodology` — placeholder. Single paragraph explaining what the methodology piece will cover, with an external link to the Substack post once published. Do not copy the essay into the app.

Watchlist, /api/sync, and Vercel Cron are skipped for v0. There is nothing to sync. Add them when the first collector ships a real record.

## Data model

TypeScript types. These should live in `lib/types.ts` and mirror the JSON file shapes in `data/`.

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
  id: string;                       // 'SC-001', 'SC-002'...
  business: string;                 // 'Affinity Partners'
  family_member: string;            // 'Jared Kushner'
  scope: Scope;
  source: Source;
  period: string;                   // '2021–PRES', '2017–2020'
  frameworks: Framework[];
  evidence_category: EvidenceCategory[];   // [1,2,3] for spans
  summary: string;                  // 2-4 sentences, analyst voice
  documented_amount?: string;       // '$2 billion', '~$3.4M to RSB LLC'
  primary_sources?: PrimarySource[];
}

export interface PrimarySource {
  label: string;                    // 'SEC Form ADV'
  url?: string;
  category: EvidenceCategory;
}

export interface SovereignEntity {
  id: string;                       // 'PIF', 'MUBADALA'...
  name: string;                     // 'Public Investment Fund'
  country: string;
  governance_note: string;          // one paragraph, analyst voice
}
```

## Open decisions for the new chat

The Python collector stubs versus a TypeScript rewrite. The existing repo has six Python stubs. cbt is TypeScript end-to-end. Consistent-stack argues for a TS rewrite. Practical-scraping argues that some foreign-jurisdiction registry work is easier in Python, and the collectors output JSON consumed by the Next.js app at build or sync time, so the language gap does not matter at runtime. Recommendation: leave Python stubs in place for now, decide per-source as collectors come online.

Static JSON versus Turso for v0. cbt uses Turso for live bill data. Sovereign Connections has zero live records. Static JSON in `data/records.json` is sufficient for pre-launch and removes infra setup from this session. Recommendation: static JSON now, migrate to Turso when the first collector ships.

The walk-the-definition button mechanic. Two viable approaches: clipboard-copy with a Claude.ai deep link, or a `/record/[id]/walk` page that pre-fills the prompt. Either works. Pick whichever is faster and keep the surface consistent across records.

The methodology page approach. External link to the Substack post is the recommendation. The MDX-inside-the-app alternative duplicates content and creates a maintenance burden. The Substack post is the canonical version.

## House style

PROJECT.md is authoritative. For this code session specifically:

- Match cbt's component patterns (small Tailwind primitives, no UI library beyond Tailwind v4 and lucide-react if needed).
- Match cbt's mono-first aesthetic. Resist the urge to soften it with rounded cards or large spacing; the terminal feel is the point.
- All in-app copy follows PROJECT.md voice rules. Banned words apply. No em-dashes (use commas or parentheses). Analyst voice, point-first. No hype adjectives ("alarming", "unprecedented", "staggering").
- Status pills, framework codes, scope codes use the exact string literals defined in the type unions. Do not introduce new abbreviations without updating the union type.
- Filenames lowercase-kebab-case (matches cbt).

## Suggested first prompt for the new chat

> Continuing Sovereign Connections. The terminal-style dashboard was approved in the previous Claude.ai chat. This session converts it to a working Next.js 15 + TypeScript + Tailwind v4 app matching the cbt stack pattern (github.com/CSU-J3/cbt). Static JSON for v0 (no Turso yet), no /api routes, no Vercel Cron, no Watchlist. Target deliverables for this session: scaffold the app, render the records dashboard at `/` with working filters and expand rows, ship the SWF registry at `/swfs`, deploy to Vercel. Six seed records and the type definitions are in the handoff doc above. PROJECT.md governs voice; cbt governs stack and component patterns. Ask one clarifying question before scaffolding.

## Seed data

`data/records.json`. Full payload, ready to drop in:

```json
[
  {
    "id": "SC-001",
    "business": "Affinity Partners",
    "family_member": "Jared Kushner",
    "scope": "COMP",
    "source": "PIF",
    "period": "2021–PRES",
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
    "period": "2017–2020",
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
    "period": "2017–2018",
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
    "period": "2017–2021",
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
    "period": "2017–2020",
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
    "period": "2014–2019",
    "frameworks": ["FARA", "LDA"],
    "evidence_category": [1, 2, 3],
    "summary": "Documented for methodology completeness as the case the framework excludes despite political salience. Burisma is a Cyprus-registered private holding company; no Ukrainian state ownership in the documented record. State ties run through the owner's prior ministerial tenure, not through ownership structure. The exclusion is symmetrical: a Republican-side analogue with the same facts would also fall outside scope.",
    "documented_amount": "~$3.4M to Rosemont Seneca Bohai LLC (entity-level inflows)"
  }
]
```

`data/sovereign_entities.json`. Seed registry:

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

## Cross-project hygiene

Once this session ships the v0 app and deploys to Vercel:

- Update Sovereign Connections README to point to the live URL (replacing the "Public dashboard | Not deployed" line in the status table).
- Add the deployment URL to the docs/handoffs/ index if cbt's pattern is followed.
- Consider adding the Sovereign Connections deployment URL to the Follow-the-Moneys and Connected-Procurement READMEs under "Related work" once they have public dashboards too.
