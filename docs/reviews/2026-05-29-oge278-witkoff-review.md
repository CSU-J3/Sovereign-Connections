# OGE 278 Candidate Review Worksheet — Witkoff (2026-05-13 filing)

- **Generated:** 2026-05-29 (snapshot; regenerate with `collectors/oge_278/review_worksheet.py`)
- **Source filing:** `data/samples/witkoff-oge278-2025-08-13.pdf` (OGE Form 278e, New Entrant Report)
- **Candidates total:** 168  ·  **unreviewed shown:** 162  ·  **already dispositioned, excluded:** 6 (162 + 6 = 168)

## Already dispositioned (excluded from the table below)

These 6 are not in the worksheet; listed so the count reconciles. World Liberty Financial is **promoted**, not unreviewed, so it is correctly absent below.

| (part, entry) | entity | state | → |
|---|---|---|---|
| (2, 1) | The Witkoff Group LLC (real estate management company) | killed_out_of_scope |  |
| (6, 1) | M&A Management Company Ltd | killed_out_of_scope |  |
| (6, 2) | Sweet Tuna Boat Ltd | killed_out_of_scope |  |
| (6, 7) | Silverpeak Legacy Partners III, L.P. | killed_out_of_scope |  |
| (6, 9.1) | Optima STAR Fund - Long-Only - Class B | hold_pending_research |  |
| (6, 41.8.1) | World Liberty Financial (cryptocurrency) | promoted | SC-007 |

## How to use this worksheet

- Fill the **disposition** column with one of the four lifecycle states: `unreviewed` (leave as-is), `hold_pending_research`, `killed_out_of_scope`, or `promoted`.
- `killed_out_of_scope` **requires a reason** in the reason/note column (the audit trail that the bar was applied — a silent drop looks like nobody looked). `promoted` requires the target `SC-###`.
- Dispositions key on **(part, entry_number)**, the stable row identity — *not* on `CAND-###`, which is a display handle that a candidate re-run reassigns. Edit the disposition/reason cells; a later handoff reads them back keyed on (part, entry).
- Review against the established bar: `docs/references/collector-gap-finding-oge278.md` (kill precedent) and `docs/references/wlf-research-target.md` (promote precedent).

**Sort key (convenience, NOT a judgment):** rows are ordered surface-to-bottom by tier — (1) has a descriptor (parenthetical: crypto, stablecoin, fund/ticker markers), then (2) carries a foreign-signal tag, then (3) high rollup value (≥ $1,000,001 bracket), then (4) everything else in entry order; within tiers 1–3, higher value first. A row low in the list is just where the eye lands last — it is **not** a Code assertion that it's less likely to be killed.

**Signal tags** are surfaced, not judged: `suffix:Ltd` etc. = a non-US corporate form; `suffix:LP` = US limited-partnership form (shown for completeness, not asserted foreign); `place:France` = a non-US place name in the row; `share-class:B` = a fund share-class designation (the same weak signal the 9.1 hold flagged).

## Unreviewed candidates (162)

| # | CAND (ref) | (part, entry) | entity | ancestry_path | value | descriptor | signals | disposition | reason / note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CAND-002 | (2, 1.1) | WG Development LLC (development management) | 1 > 1.1 | Over $50,000,000 ↥1 | development management | — |  |  |
| 2 | CAND-045 | (6, 12.9) | US bank #4 (cash) | 12 > 12.9 | Over $50,000,000 | cash | — |  |  |
| 3 | CAND-118 | (6, 41.1.1.1.1.1.3) | USREC Banyan Cay Development LLC (property development) | 41 > 41.1 > 41.1.1 > 41.1.1.1 > 41.1.1.1.1 > 41.1.1.1.1.1 > 41.1.1.1.1.1.3 | Over $50,000,000 ↥41 | property development | — |  |  |
| 4 | CAND-127 | (6, 41.5) | WG FB LLC (food & beverage operating business) | 41 > 41.5 | Over $50,000,000 ↥41 | food & beverage operating business | — |  |  |
| 5 | CAND-128 | (6, 41.6) | WG GM LLC (golf management operating business) | 41 > 41.6 | Over $50,000,000 ↥41 | golf management operating business | — |  |  |
| 6 | CAND-129 | (6, 41.7) | WG HM LLC (hotel management operating business) | 41 > 41.7 | Over $50,000,000 ↥41 | hotel management operating business | — |  |  |
| 7 | CAND-131 | (6, 41.9.1) | SC Financial Technologies LLC (stablecoin) | 41 > 41.9 > 41.9.1 | Over $50,000,000 ↥41 | stablecoin | — |  |  |
| 8 | CAND-065 | (6, 19.1) | UDR, Inc. (UDR) | 19 > 19.1 | $5,000,001 - $25,000,000 ↥19 | UDR | — |  |  |
| 9 | CAND-067 | (6, 20.1) | UDR, Inc. (UDR) | 20 > 20.1 | $5,000,001 - $25,000,000 ↥20 | UDR | — |  |  |
| 10 | CAND-069 | (6, 21.1) | UDR, Inc. (UDR) | 21 > 21.1 | $5,000,001 - $25,000,000 ↥21 | UDR | — |  |  |
| 11 | CAND-156 | (6, 55) | US bank #1 (cash) | 55 | $5,000,001 - $25,000,000 | cash | — |  |  |
| 12 | CAND-020 | (6, 5.1) | Moonpay LLC (financial technology) | 5 > 5.1 | $1,000,001 - $5,000,000 ↥5 | financial technology | — |  |  |
| 13 | CAND-022 | (6, 6.1) | SpaceX (space technology) | 6 > 6.1 | $1,000,001 - $5,000,000 ↥6 | space technology | — |  |  |
| 14 | CAND-028 | (6, 8.1) | Built (construction and real estate finance technology) | 8 > 8.1 | $1,000,001 - $5,000,000 ↥8 | construction and real estate finance technology | — |  |  |
| 15 | CAND-041 | (6, 12.7.1) | Coatue Fintech Fund I LP - Class A - Cash Reserve (US/LATAM) | 12 > 12.7 > 12.7.1 | $1,000,001 - $5,000,000 ↥12.7 | US/LATAM | suffix:LP, share-class:A |  |  |
| 16 | CAND-042 | (6, 12.7.2) | Coatue Fintech Fund I LP - Class A - Private Portfolio (US/LATAM) | 12 > 12.7 > 12.7.2 | $1,000,001 - $5,000,000 ↥12.7 | US/LATAM | suffix:LP, share-class:A |  |  |
| 17 | CAND-043 | (6, 12.7.3) | Coatue Fintech Fund I LP - Class A - MGMT (US/LATAM - MVP Only) | 12 > 12.7 > 12.7.3 | $1,000,001 - $5,000,000 ↥12.7 | US/LATAM - MVP Only | suffix:LP, share-class:A |  |  |
| 18 | CAND-142 | (6, 46.1.1) | SL Green Realty Corp. (SLG) | 46 > 46.1 > 46.1.1 | $1,000,001 - $5,000,000 ↥46 | SLG | — |  |  |
| 19 | CAND-148 | (6, 50.1) | SL Green Realty Corp. (SLG) | 50 > 50.1 | $1,000,001 - $5,000,000 ↥50 | SLG | — |  |  |
| 20 | CAND-032 | (6, 11.2) | Micron Technology Inc. (MU) | 11 > 11.2 | $500,001 - $1,000,000 | MU | — |  |  |
| 21 | CAND-083 | (6, 27.3) | WG Uniondale Internal LLC (holding company with no reportable assets) | 27 > 27.3 | $500,001 - $1,000,000 ↥27 | holding company with no reportable assets | — |  |  |
| 22 | CAND-151 | (6, 52.1) | Material Bank (material sourcing company) | 52 > 52.1 | $500,001 - $1,000,000 ↥52 | material sourcing company | — |  |  |
| 23 | CAND-157 | (6, 56) | US bank #2 (cash) | 56 | $500,001 - $1,000,000 | cash | — |  |  |
| 24 | CAND-030 | (6, 10.1) | Financial Square Treasury Instruments Fund - FST Shares Moody's AAA (FTIXX) | 10 > 10.1 | $100,001 - $250,000 | FTIXX | — |  |  |
| 25 | CAND-094 | (6, 32.1.3.1) | Columbus 95th Street LLC (holding company with no reportable assets) | 32 > 32.1 > 32.1.3 > 32.1.3.1 | $100,001 - $250,000 ↥32 | holding company with no reportable assets | — |  |  |
| 26 | CAND-158 | (6, 57) | US bank #3 (cash) | 57 | $100,001 - $250,000 | cash | — |  |  |
| 27 | CAND-051 | (6, 13.6) | Simon PPTY Group Inc. SBI (SPG) | 13 > 13.6 | $50,001 - $100,000 | SPG | — |  |  |
| 28 | CAND-054 | (6, 13.9) | UBS Select Treasury Institutional Fund (SETXX) | 13 > 13.9 | $50,001 - $100,000 | SETXX | — |  |  |
| 29 | CAND-009 | (5, 1.5) | Ventas, Inc. (VTR) | 1 > 1.5 | $15,001 - $50,000 | VTR | — |  |  |
| 30 | CAND-010 | (5, 1.6) | W P Carey Inc. REIT (WPC) | 1 > 1.6 | $15,001 - $50,000 | WPC | — |  |  |
| 31 | CAND-012 | (5, 1.8) | UBS Select Treasury Institutional Fund (SETXX) | 1 > 1.8 | $15,001 - $50,000 | SETXX | — |  |  |
| 32 | CAND-047 | (6, 13.2) | Healthpeak PPTYS Inc. (DOC) | 13 > 13.2 | $15,001 - $50,000 | DOC | — |  |  |
| 33 | CAND-049 | (6, 13.4) | Merck & Co. Inc. (MRK) | 13 > 13.4 | $15,001 - $50,000 | MRK | — |  |  |
| 34 | CAND-050 | (6, 13.5) | Shell PLC Spon ADR (SHEL) | 13 > 13.5 | $15,001 - $50,000 | SHEL | suffix:PLC |  |  |
| 35 | CAND-146 | (6, 49) | Stomber & Witkoff LLC (law firm) | 49 | $15,001 - $50,000 | law firm | — |  |  |
| 36 | CAND-005 | (5, 1.1) | Macerich Company (MAC) | 1 > 1.1 | $1,001 - $15,000 | MAC | — |  |  |
| 37 | CAND-007 | (5, 1.3) | Regency Centers Corp. (REG) | 1 > 1.3 | $1,001 - $15,000 | REG | — |  |  |
| 38 | CAND-008 | (5, 1.4) | Sabra Health Care REIT, Inc. (SBRA) | 1 > 1.4 | $1,001 - $15,000 | SBRA | — |  |  |
| 39 | CAND-011 | (5, 1.7) | U.S. bank #4 (cash) | 1 > 1.7 | $1,001 - $15,000 | cash | — |  |  |
| 40 | CAND-033 | (6, 11.3) | US bank #4 (cash) | 11 > 11.3 | $1,001 - $15,000 | cash | — |  |  |
| 41 | CAND-046 | (6, 13.1) | Curbline PPTYS Corp (CURB) | 13 > 13.1 | $1,001 - $15,000 | CURB | — |  |  |
| 42 | CAND-048 | (6, 13.3) | Kimco Realty Corp. (KIM) | 13 > 13.3 | $1,001 - $15,000 | KIM | — |  |  |
| 43 | CAND-052 | (6, 13.7) | W P Carey Inc. REIT (WPC) | 13 > 13.7 | $1,001 - $15,000 | WPC | — |  |  |
| 44 | CAND-053 | (6, 13.8) | U.S. bank #4 (cash) | 13 > 13.8 | $1,001 - $15,000 | cash | — |  |  |
| 45 | CAND-006 | (5, 1.2) | Net Lease Office PPTYS (NLOP) | 1 > 1.2 | None (or less than $1,001) | NLOP | — |  |  |
| 46 | CAND-149 | (6, 51) | WG 36 CPS Internal LLC (holding company with no current reportable assets) | 51 | None (or less than $1,001) | holding company with no current reportable assets | — |  |  |
| 47 | CAND-018 | (6, 4) | Atreides Foundation Fund, LP | 4 | $5,000,001 - $25,000,000 | — | suffix:LP |  |  |
| 48 | CAND-017 | (6, 3) | Addition Three, LP | 3 | $1,000,001 - $5,000,000 | — | suffix:LP |  |  |
| 49 | CAND-039 | (6, 12.6) | Flex Ltd [FLEX] | 12 > 12.6 | $1,000,001 - $5,000,000 | — | suffix:Ltd |  |  |
| 50 | CAND-040 | (6, 12.7) | Coatue Fintech Fund I LP | 12 > 12.7 | $1,000,001 - $5,000,000 | — | suffix:LP |  |  |
| 51 | CAND-044 | (6, 12.8) | Highbridge Convertible Dislocation Fund LP - Class A | 12 > 12.8 | $500,001 - $1,000,000 | — | suffix:LP, share-class:A |  |  |
| 52 | CAND-025 | (6, 7.2) | Mixed use real estate, Marseille, France | 7 > 7.2 | $15,001 - $50,000 ↥7 | — | place:France |  |  |
| 53 | CAND-026 | (6, 7.3) | Land development, Mumbai, India | 7 > 7.3 | $15,001 - $50,000 ↥7 | — | place:India |  |  |
| 54 | CAND-003 | (2, 1.2.1) | Aircraft | 1 > 1.2 > 1.2.1 | Over $50,000,000 ↥1 | — | — |  |  |
| 55 | CAND-004 | (2, 1.3.1) | Aircraft | 1 > 1.3 > 1.3.1 | Over $50,000,000 ↥1 | — | — |  |  |
| 56 | CAND-060 | (6, 16) | SW Southampton LLC | 16 | Over $50,000,000 | — | — |  |  |
| 57 | CAND-061 | (6, 16.1) | Residential real estate, Southampton, NY | 16 > 16.1 | Over $50,000,000 ↥16 | — | — |  |  |
| 58 | CAND-108 | (6, 38) | WG 76 11th LLC | 38 | Over $50,000,000 | — | — |  |  |
| 59 | CAND-109 | (6, 38.1.1.1.1) | 76 11th Lender LLC | 38 > 38.1 > 38.1.1 > 38.1.1.1 > 38.1.1.1.1 | Over $50,000,000 ↥38 | — | — |  |  |
| 60 | CAND-110 | (6, 38.1.1.1.2.1.1) | Residential and commercial real estate, New York, NY | 38 > 38.1 > 38.1.1 > 38.1.1.1 > 38.1.1.1.2 > 38.1.1.1.2.1 > 38.1.1.1.2.1.1 | Over $50,000,000 ↥38 | — | — |  |  |
| 61 | CAND-115 | (6, 41) | Witkoff Holdings LLC | 41 | Over $50,000,000 | — | — |  |  |
| 62 | CAND-116 | (6, 41.1.1.1.1.1.1.1) | Recreational and hotel property, West Palm Beach, FL | 41 > 41.1 > 41.1.1 > 41.1.1.1 > 41.1.1.1.1 > 41.1.1.1.1.1 > 41.1.1.1.1.1.1 > 41.1.1.1.1.1.1.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 63 | CAND-117 | (6, 41.1.1.1.1.1.2.1) | Residential real estate, West Palm Beach, FL | 41 > 41.1 > 41.1.1 > 41.1.1.1 > 41.1.1.1.1 > 41.1.1.1.1.1 > 41.1.1.1.1.1.2 > 41.1.1.1.1.1.2.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 64 | CAND-119 | (6, 41.2.1.1.1.1.1) | Mixed use development, Miami Beach, FL | 41 > 41.2 > 41.2.1 > 41.2.1.1 > 41.2.1.1.1 > 41.2.1.1.1.1 > 41.2.1.1.1.1.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 65 | CAND-120 | (6, 41.2.1.1.1.2.1) | Mixed use development, Miami Beach, FL | 41 > 41.2 > 41.2.1 > 41.2.1.1 > 41.2.1.1.1 > 41.2.1.1.1.2 > 41.2.1.1.1.2.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 66 | CAND-121 | (6, 41.2.1.1.1.3.1) | Mixed use development, Miami Beach, FL | 41 > 41.2 > 41.2.1 > 41.2.1.1 > 41.2.1.1.1 > 41.2.1.1.1.3 > 41.2.1.1.1.3.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 67 | CAND-122 | (6, 41.2.1.1.1.4.1) | Mixed use development, Miami Beach, FL | 41 > 41.2 > 41.2.1 > 41.2.1.1 > 41.2.1.1.1 > 41.2.1.1.1.4 > 41.2.1.1.1.4.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 68 | CAND-123 | (6, 41.2.1.1.1.5.1) | Mixed use development, Miami Beach, FL | 41 > 41.2 > 41.2.1 > 41.2.1.1 > 41.2.1.1.1 > 41.2.1.1.1.5 > 41.2.1.1.1.5.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 69 | CAND-124 | (6, 41.2.1.1.1.6.1) | Mixed use development, Miami Beach, FL | 41 > 41.2 > 41.2.1 > 41.2.1.1 > 41.2.1.1.1 > 41.2.1.1.1.6 > 41.2.1.1.1.6.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 70 | CAND-125 | (6, 41.3.1.1) | Members club, marina, hotel and hotel condo development, Hallandale, FL | 41 > 41.3 > 41.3.1 > 41.3.1.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 71 | CAND-126 | (6, 41.4.1) | Mixed use real estate development, Miami Beach, FL | 41 > 41.4 > 41.4.1 | Over $50,000,000 ↥41 | — | — |  |  |
| 72 | CAND-132 | (6, 42) | WG 700 NM LLC | 42 | Over $50,000,000 | — | — |  |  |
| 73 | CAND-133 | (6, 42.1.1.1.1) | Undeveloped land entitled for residential development, Miami, FL | 42 > 42.1 > 42.1.1 > 42.1.1.1 > 42.1.1.1.1 | Over $50,000,000 ↥42 | — | — |  |  |
| 74 | CAND-055 | (6, 14) | Rex Real Estate LLC | 14 | $25,000,001 - $50,000,000 | — | — |  |  |
| 75 | CAND-056 | (6, 14.1) | Residential real estate, Miami, FL | 14 > 14.1 | $25,000,001 - $50,000,000 ↥14 | — | — |  |  |
| 76 | CAND-057 | (6, 15) | Rushing Dream Farm LLC | 15 | $5,000,001 - $25,000,000 | — | — |  |  |
| 77 | CAND-058 | (6, 15.1) | Farmland, Lexington, KY | 15 > 15.1 | $5,000,001 - $25,000,000 ↥15 | — | — |  |  |
| 78 | CAND-059 | (6, 15.2) | Residential real estate, Lexington, KY | 15 > 15.2 | $5,000,001 - $25,000,000 ↥15 | — | — |  |  |
| 79 | CAND-064 | (6, 19) | SCW 10 Martin LLC | 19 | $5,000,001 - $25,000,000 | — | — |  |  |
| 80 | CAND-066 | (6, 20) | SCW 10 Debt LLC | 20 | $5,000,001 - $25,000,000 | — | — |  |  |
| 81 | CAND-068 | (6, 21) | SCW 10 LLC | 21 | $5,000,001 - $25,000,000 | — | — |  |  |
| 82 | CAND-086 | (6, 29) | WG Chrystie Internal LLC | 29 | $5,000,001 - $25,000,000 | — | — |  |  |
| 83 | CAND-087 | (6, 29.1.1.1.1.1.1.1) | Hotel real estate, New York, NY | 29 > 29.1 > 29.1.1 > 29.1.1.1 > 29.1.1.1.1 > 29.1.1.1.1.1 > 29.1.1.1.1.1.1 > 29.1.1.1.1.1.1.1 | $5,000,001 - $25,000,000 ↥29 | — | — |  |  |
| 84 | CAND-095 | (6, 33) | 22 East 60th Street LLC | 33 | $5,000,001 - $25,000,000 | — | — |  |  |
| 85 | CAND-096 | (6, 33.1.1) | Restaurant, New York, NY | 33 > 33.1 > 33.1.1 | $5,000,001 - $25,000,000 ↥33 | — | — |  |  |
| 86 | CAND-097 | (6, 33.1.2) | Restaurant, Sag Harbor, NY | 33 > 33.1 > 33.1.2 | $5,000,001 - $25,000,000 ↥33 | — | — |  |  |
| 87 | CAND-098 | (6, 33.1.3) | Restaurant, Palm Beach, FL | 33 > 33.1 > 33.1.3 | $5,000,001 - $25,000,000 ↥33 | — | — |  |  |
| 88 | CAND-134 | (6, 43) | WG Sadie LLC | 43 | $5,000,001 - $25,000,000 | — | — |  |  |
| 89 | CAND-135 | (6, 43.1.1) | Undeveloped land, Miami, FL | 43 > 43.1 > 43.1.1 | $5,000,001 - $25,000,000 ↥43 | — | — |  |  |
| 90 | CAND-143 | (6, 47) | 150 PH-B LLC | 47 | $5,000,001 - $25,000,000 | — | — |  |  |
| 91 | CAND-144 | (6, 47.1) | Residential real estate, Los Angeles, CA | 47 > 47.1 | $5,000,001 - $25,000,000 ↥47 | — | — |  |  |
| 92 | CAND-154 | (6, 54) | WG TS Hotel LLC | 54 | $5,000,001 - $25,000,000 | — | — |  |  |
| 93 | CAND-155 | (6, 54.1) | Hospitality real estate, New York, NY | 54 > 54.1 | $5,000,001 - $25,000,000 ↥54 | — | — |  |  |
| 94 | CAND-016 | (6, 2.1) | Motorized water vehicle | 2 > 2.1 | $1,000,001 - $5,000,000 ↥2 | — | — |  |  |
| 95 | CAND-019 | (6, 5) | BMW SPV 1 LLC | 5 | $1,000,001 - $5,000,000 | — | — |  |  |
| 96 | CAND-021 | (6, 6) | 3G Investors LLC | 6 | $1,000,001 - $5,000,000 | — | — |  |  |
| 97 | CAND-027 | (6, 8) | Witkoff Innovation Acquisition LLC | 8 | $1,000,001 - $5,000,000 | — | — |  |  |
| 98 | CAND-035 | (6, 12.2) | Cisco Systems Inc. [CSCO] | 12 > 12.2 | $1,000,001 - $5,000,000 | — | — |  |  |
| 99 | CAND-037 | (6, 12.4) | Reddit Inc.-CL A [RDDT] | 12 > 12.4 | $1,000,001 - $5,000,000 | — | — |  |  |
| 100 | CAND-074 | (6, 24) | SW 1107 Broadway LLC | 24 | $1,000,001 - $5,000,000 | — | — |  |  |
| 101 | CAND-075 | (6, 24.1.1.1.1.1) | Residential and commercial real estate, New York, NY | 24 > 24.1 > 24.1.1 > 24.1.1.1 > 24.1.1.1.1 > 24.1.1.1.1.1 | $1,000,001 - $5,000,000 ↥24 | — | — |  |  |
| 102 | CAND-076 | (6, 25) | WG 101 Murray Internal LLC | 25 | $1,000,001 - $5,000,000 | — | — |  |  |
| 103 | CAND-077 | (6, 25.1.1.1.1.1.1.1) | Residential real estate, New York NY | 25 > 25.1 > 25.1.1 > 25.1.1.1 > 25.1.1.1.1 > 25.1.1.1.1.1 > 25.1.1.1.1.1.1 > 25.1.1.1.1.1.1.1 | $1,000,001 - $5,000,000 ↥25 | — | — |  |  |
| 104 | CAND-141 | (6, 46) | 125 Broad Unit A Corp. | 46 | $1,000,001 - $5,000,000 | — | — |  |  |
| 105 | CAND-147 | (6, 50) | WG 1745 Internal LLC | 50 | $1,000,001 - $5,000,000 | — | — |  |  |
| 106 | CAND-159 | (6, 58) | WG Bowtie LLC | 58 | $1,000,001 - $5,000,000 | — | — |  |  |
| 107 | CAND-160 | (6, 58.1.1) | Residential and retail real estate, New York, NY | 58 > 58.1 > 58.1.1 | $1,000,001 - $5,000,000 ↥58 | — | — |  |  |
| 108 | CAND-163 | (6, 60) | WG WALG Holdings LLC | 60 | $1,000,001 - $5,000,000 | — | — |  |  |
| 109 | CAND-164 | (6, 60.1) | Portfolio of net leased Walgreen Drugstores throughout the United States | 60 > 60.1 | $1,000,001 - $5,000,000 ↥60 | — | — |  |  |
| 110 | CAND-014 | (6, 1.1) | Motorized water vehicles | 1 > 1.1 | $15,001 - $50,000 ↥1 | — | — |  |  |
| 111 | CAND-024 | (6, 7.1) | Residential real estate, New York, NY | 7 > 7.1 | $15,001 - $50,000 ↥7 | — | — |  |  |
| 112 | CAND-031 | (6, 11.1) | Escrow New York REIT Inc. | 11 > 11.1 | $50,001 - $100,000 | — | — |  |  |
| 113 | CAND-034 | (6, 12.1) | Escrow New York REIT Inc. | 12 > 12.1 | $15,001 - $50,000 | — | — |  |  |
| 114 | CAND-036 | (6, 12.3) | Nextracker Inc-CL A [NXT] | 12 > 12.3 | $100,001 - $250,000 | — | — |  |  |
| 115 | CAND-038 | (6, 12.5) | Uber Technologies Inc. [UBER] | 12 > 12.5 | $100,001 - $250,000 | — | — |  |  |
| 116 | CAND-062 | (6, 17) | SCW 10 Corp. | 17 | — | — | — |  |  |
| 117 | CAND-063 | (6, 18) | SCW 10 Upper LLC | 18 | — | — | — |  |  |
| 118 | CAND-070 | (6, 22) | Witkoff Lender LLC | 22 | None (or less than $1,001) | — | — |  |  |
| 119 | CAND-071 | (6, 22.1) | WBF LLC | 22 > 22.1 | None (or less than $1,001) ↥22 | — | — |  |  |
| 120 | CAND-072 | (6, 22.2.1.1.1) | Residential & commercial real estate, New York, NY | 22 > 22.2 > 22.2.1 > 22.2.1.1 > 22.2.1.1.1 | None (or less than $1,001) ↥22 | — | — |  |  |
| 121 | CAND-073 | (6, 23) | Witkoff Commercial Acquisition LLC | 23 | None (or less than $1,001) | — | — |  |  |
| 122 | CAND-078 | (6, 26) | SW 150 Charles LLC | 26 | $1,001 - $15,000 | — | — |  |  |
| 123 | CAND-079 | (6, 26.1.1.1.1.1) | Residential real estate, New York, NY | 26 > 26.1 > 26.1.1 > 26.1.1.1 > 26.1.1.1.1 > 26.1.1.1.1.1 | $1,001 - $15,000 ↥26 | — | — |  |  |
| 124 | CAND-080 | (6, 27) | Piano SW HTC LLC | 27 | $500,001 - $1,000,000 | — | — |  |  |
| 125 | CAND-081 | (6, 27.1.1) | Residential condominium real estate, New York, NY | 27 > 27.1 > 27.1.1 | $500,001 - $1,000,000 ↥27 | — | — |  |  |
| 126 | CAND-082 | (6, 27.2.1) | Office building, Miami, FL | 27 > 27.2 > 27.2.1 | $500,001 - $1,000,000 ↥27 | — | — |  |  |
| 127 | CAND-084 | (6, 28) | WG Leroy LLC | 28 | $250,001 - $500,000 | — | — |  |  |
| 128 | CAND-085 | (6, 28.1.1.1.1.1) | Residential condominium real estate, New York, NY | 28 > 28.1 > 28.1.1 > 28.1.1.1 > 28.1.1.1.1 > 28.1.1.1.1.1 | $250,001 - $500,000 ↥28 | — | — |  |  |
| 129 | CAND-088 | (6, 30) | Witkoff Member LLC | 30 | None (or less than $1,001) | — | — |  |  |
| 130 | CAND-089 | (6, 31) | 233 Next LLC | 31 | None (or less than $1,001) | — | — |  |  |
| 131 | CAND-090 | (6, 31.1.1.1.1.1) | Commercial real estate, New York, NY | 31 > 31.1 > 31.1.1 > 31.1.1.1 > 31.1.1.1.1 > 31.1.1.1.1.1 | None (or less than $1,001) ↥31 | — | — |  |  |
| 132 | CAND-091 | (6, 32) | WG Internal Holdings LLC | 32 | $100,001 - $250,000 | — | — |  |  |
| 133 | CAND-092 | (6, 32.1.1.1.1) | Residential real estate, New York, NY | 32 > 32.1 > 32.1.1 > 32.1.1.1 > 32.1.1.1.1 | $100,001 - $250,000 ↥32 | — | — |  |  |
| 134 | CAND-093 | (6, 32.1.2.1.1) | Hotel real estate, New York, NY | 32 > 32.1 > 32.1.2 > 32.1.2.1 > 32.1.2.1.1 | $100,001 - $250,000 ↥32 | — | — |  |  |
| 135 | CAND-099 | (6, 34) | Witkoff 485 Lex LLC | 34 | None (or less than $1,001) | — | — |  |  |
| 136 | CAND-100 | (6, 34.1.1.1.1.1.1) | Commercial real estate, New York, NY | 34 > 34.1 > 34.1.1 > 34.1.1.1 > 34.1.1.1.1 > 34.1.1.1.1.1 > 34.1.1.1.1.1.1 | None (or less than $1,001) ↥34 | — | — |  |  |
| 137 | CAND-101 | (6, 34.2.1.1) | Commercial real estate, Hampstead, NH | 34 > 34.2 > 34.2.1 > 34.2.1.1 | None (or less than $1,001) ↥34 | — | — |  |  |
| 138 | CAND-102 | (6, 34.3.1.1) | Commercial real estate, Windham, Mass | 34 > 34.3 > 34.3.1 > 34.3.1.1 | None (or less than $1,001) ↥34 | — | — |  |  |
| 139 | CAND-103 | (6, 35) | Witkoff TIC LLC | 35 | $500,001 - $1,000,000 | — | — |  |  |
| 140 | CAND-104 | (6, 36) | WG 420 LLC | 36 | None (or less than $1,001) | — | — |  |  |
| 141 | CAND-105 | (6, 36.1.1.1.1.1.1) | Office condominium, New York, NY | 36 > 36.1 > 36.1.1 > 36.1.1.1 > 36.1.1.1.1 > 36.1.1.1.1.1 > 36.1.1.1.1.1.1 | None (or less than $1,001) ↥36 | — | — |  |  |
| 142 | CAND-106 | (6, 37) | WG 55 LLC | 37 | $15,001 - $50,000 | — | — |  |  |
| 143 | CAND-107 | (6, 37.1.1) | Residential real estate, New York, NY | 37 > 37.1 > 37.1.1 | $15,001 - $50,000 ↥37 | — | — |  |  |
| 144 | CAND-111 | (6, 39) | 866 Acquisition LLC | 39 | None (or less than $1,001) | — | — |  |  |
| 145 | CAND-112 | (6, 39.1.1.1.1) | Commercial real estate, New York, NY | 39 > 39.1 > 39.1.1 > 39.1.1.1 > 39.1.1.1.1 | None (or less than $1,001) ↥39 | — | — |  |  |
| 146 | CAND-113 | (6, 40) | 866 Development Partners LLC | 40 | None (or less than $1,001) | — | — |  |  |
| 147 | CAND-114 | (6, 40.1.1.1.1) | Commercial real estate, New York, NY | 40 > 40.1 > 40.1.1 > 40.1.1.1 > 40.1.1.1.1 | None (or less than $1,001) ↥40 | — | — |  |  |
| 148 | CAND-136 | (6, 44) | Witkoff 44 LLC | 44 | None (or less than $1,001) | — | — |  |  |
| 149 | CAND-137 | (6, 44.1.1.1.1.1.1.1.1) | Hospitality real estate, Los Angeles, CA | 44 > 44.1 > 44.1.1 > 44.1.1.1 > 44.1.1.1.1 > 44.1.1.1.1.1 > 44.1.1.1.1.1.1 > 44.1.1.1.1.1.1.1 > 44.1.1.1.1.1.1.1.1 | None (or less than $1,001) ↥44 | — | — |  |  |
| 150 | CAND-138 | (6, 44.1.1.1.2.1.1.1.1) | Hospitality real estate, Los Angeles, CA | 44 > 44.1 > 44.1.1 > 44.1.1.1 > 44.1.1.1.2 > 44.1.1.1.2.1 > 44.1.1.1.2.1.1 > 44.1.1.1.2.1.1.1 > 44.1.1.1.2.1.1.1.1 | None (or less than $1,001) ↥44 | — | — |  |  |
| 151 | CAND-139 | (6, 44.1.1.1.3.1.1.1.1) | Commercial real estate, Los Angeles, CA | 44 > 44.1 > 44.1.1 > 44.1.1.1 > 44.1.1.1.3 > 44.1.1.1.3.1 > 44.1.1.1.3.1.1 > 44.1.1.1.3.1.1.1 > 44.1.1.1.3.1.1.1.1 | None (or less than $1,001) ↥44 | — | — |  |  |
| 152 | CAND-140 | (6, 45) | Witkoff 44 Partners LLC | 45 | $1,001 - $15,000 | — | — |  |  |
| 153 | CAND-145 | (6, 48) | SCW 150 Corp. | 48 | $100,001 - $250,000 | — | — |  |  |
| 154 | CAND-150 | (6, 52) | WG Materials LLC | 52 | $500,001 - $1,000,000 | — | — |  |  |
| 155 | CAND-152 | (6, 53) | WG Investments LLC | 53 | None (or less than $1,001) | — | — |  |  |
| 156 | CAND-153 | (6, 53.1) | Residential real estate, Santa Monica, CA | 53 > 53.1 | None (or less than $1,001) ↥53 | — | — |  |  |
| 157 | CAND-161 | (6, 59) | East 78th Garage LLC | 59 | $15,001 - $50,000 | — | — |  |  |
| 158 | CAND-162 | (6, 59.1) | Residential real estate, New York, NY | 59 > 59.1 | $15,001 - $50,000 ↥59 | — | — |  |  |
| 159 | CAND-165 | (6, 61) | Witkoff Telegraph Partners LLC | 61 | $15,001 - $50,000 | — | — |  |  |
| 160 | CAND-166 | (6, 61.1) | Real property, Bingham Hills, MI | 61 > 61.1 | $15,001 - $50,000 ↥61 | — | — |  |  |
| 161 | CAND-167 | (6, 62) | WG Las Vegas ICA LLC | 62 | None (or less than $1,001) | — | — |  |  |
| 162 | CAND-168 | (6, 62.1.1) | Formerly a Casino Development, Las Vegas, NV | 62 > 62.1 > 62.1.1 | None (or less than $1,001) ↥62 | — | — |  |  |

