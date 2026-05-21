# SC-001 through SC-006 — evidence discovery worksheet

**Generated:** 2026-05-21 · Handoff #22
**Status:** Discovery worksheet. Transcription and classification only — no research, no record edits, no schema changes.
**Purpose:** Input to Corey's research pass that will source the missing facts (dockets, dates, URLs, filing identifiers) needed to backfill SC-001–006 onto the `PrimarySource` discriminated union from Handoff #21. Application of findings is a follow-up handoff.

## How to read this

Each record below transcribes the evidence-bearing phrases already in its `summary` field, maps each to the most likely `PrimarySource` variant, and lists the fields that variant would need but the record does not currently supply. **Nothing here is researched or invented** — dockets, dates, URLs, filing numbers, and full publication names are named only where the record's own text already names them. Proposed variant fields for non-`oge_278e` variants are *research targets*, not schema commitments (only `oge_278e` has a per-category extras shape in code today).

Abbreviation expansions (e.g. "NYT → New York Times") are flagged as inferences, not transcription.

---

## SC-001 — Affinity Partners

**Record header**
- ID: SC-001
- Title / business: Affinity Partners
- Family member: Jared Kushner
- Scope: COMP
- `primary_sources`: **absent** (field not present on the record)

**Evidence prose extracted from `summary`**
- "SEC filings establish the financial interest"
- "NYT and FT reporting establish the PIF source"

**Per-phrase mapping**

1. "SEC filings establish the financial interest"
   - Likely variant: `sec_filing`
   - Fields the variant needs but the record lacks: form number/type, filer/registrant name, filing date, URL/accession number. (Affinity Partners is a registered investment adviser, so a Form ADV is plausible — but the record does not say so; do not assume.)
   - Already present supporting the mapping: business name "Affinity Partners"; family member "Jared Kushner"; `source: PIF`; `documented_amount: "$2 billion"`. No URL, no date, no specific filing named.

2. "NYT and FT reporting establish the PIF source"
   - Likely variant: `press_disclosure` ×2 (the phrase names two outlets — NYT and FT — so it resolves to two separate press entries).
   - Fields each entry needs but the record lacks: publisher (NYT and FT are abbreviations — *inferred* expansions New York Times and Financial Times, not in the text), article title, publication date, byline, URL.
   - Already present supporting the mapping: outlet abbreviations "NYT" and "FT"; the claim they "establish the PIF source". No titles, dates, or URLs.

**Open questions**
- "SEC filings" is plural and unspecified. Which registrant filed — Affinity Partners itself, a portfolio company, or a related entity — and which form(s)? The record does not say.
- "NYT and FT reporting" names no specific articles; the research pass needs to identify which pieces.

**Coverage estimate**
High — the `summary` carries two evidence sentences and both are surfaced (one `sec_filing`, two `press_disclosure`). All evidence claims in the prose are captured, though every phrase is non-specific (no titles, dates, or URLs to transcribe).

---

## SC-002 — Trump Organization foreign-government bookings

**Record header**
- ID: SC-002
- Title / business: Trump Organization foreign-government bookings
- Family member: Donald Trump (and family beneficial interests)
- Scope: COMP
- `primary_sources`: **absent** (field not present on the record)

**Evidence prose extracted from `summary`**
- "CREW reporting … established the records"
- "House Oversight Committee documents … established the records"
- "the underlying foreign Emoluments litigation established the records"

**Per-phrase mapping**

1. "CREW reporting"
   - Likely variant: **ambiguous** — `press_disclosure` (treating CREW as a publisher of reports) *or* the reserved `advocacy_report` (treating CREW as an advocacy organization; CREW → *inferred* Citizens for Responsibility and Ethics in Washington). Not picked — see Open questions.
   - Fields needed but not present: publisher/organization name, report or article title, date, URL.
   - Already present: the abbreviation "CREW"; the claim it helped establish "the records".

2. "House Oversight Committee documents"
   - Likely variant: **ambiguous** — closest typed variant is `congressional_letter`, but the record says "documents", not a letter; this may be committee correspondence, a committee report, released exhibits, or generic congressional material. Could equally be the generic no-`type` variant. Not picked — see Open questions.
   - Fields a `congressional_letter`-style mapping would need: committee name (the record gives "House Oversight Committee"), signers/addressee, date, URL, and — if not a letter — a document description.
   - Already present: committee name "House Oversight Committee".

3. "the underlying foreign Emoluments litigation"
   - Likely variant: `court_filing`
   - Fields needed but not present: case name, court, docket number, filing/decision date, URL.
   - Already present: nothing case-specific — the litigation is referenced only generically. (SC-004 and SC-005 are themselves foreign-Emoluments litigation records; whether this phrase points at those or at a different case — e.g. a hospitality-revenue suit — is not stated. Do not assume.)

**Open questions**
- "CREW reporting" — `press_disclosure` vs. reserved `advocacy_report`. CREW is an advocacy organization that also publishes investigative reporting; the classification depends on how the methodology wants advocacy-org material treated. Surfaced, not decided.
- "House Oversight Committee documents" — "documents" is not a "letter", so `congressional_letter` is an imperfect fit. May warrant a future congressional-document variant or the generic no-`type` variant. Surfaced, not decided.
- "the underlying foreign Emoluments litigation" names no specific case; the research pass must identify which suit(s).

**Coverage estimate**
Moderate. Three discrete evidence phrases surfaced, but the prose is impressionistic — "established the records" and `documented_amount: "Various"` point at a body of evidence without enumerating it. The worksheet captures the named sources; the underlying volume of bookings/payment records behind "the records" is not itemized in the text.

---

## SC-003 — Ivanka Trump China trademarks

**Record header**
- ID: SC-003
- Title / business: Ivanka Trump China trademarks
- Family member: Ivanka Trump
- Scope: COMP
- `primary_sources`: **absent** (field not present on the record)

**Evidence prose extracted from `summary`**
- "Trademarks were awarded by a Chinese state IP office on a non-routine timeline"

**Per-phrase mapping**

1. "Trademarks were awarded by a Chinese state IP office"
   - Likely variant: reserved `corporate_registration` is the closest fit (trademark/IP-office grant records are official registration records). No active variant covers IP-office grants. May warrant a dedicated future variant.
   - Fields a research pass would want: granting office name (the record gives only "a Chinese state IP office" — *inferred* likely the China National Intellectual Property Administration, not in the text), trademark/registration numbers, grant dates, applicant of record, URLs to the registry entries.
   - Already present: granting body described as "a Chinese state IP office"; `documented_amount: "18+ trademarks granted"` corroborates the count; `source: CHN`.

**Open questions**
- The `summary` describes the *event* (trademarks awarded) rather than citing a specific evidentiary document. The trademark grants themselves are the evidence, but no registry record, filing number, or reporting is named.
- No typed variant cleanly covers state IP-office grant records; reserved `corporate_registration` is the nearest. Whether to use it, the generic no-`type` variant, or define a new variant is a methodology decision.

**Coverage estimate**
Low. The `summary` is largely analytical framing ("Tests the state-grant-as-payment framing", "Comparative reference for whether…"). It contains one documentary anchor (the trademark grants) and cites no reporting, court case, or filing. The 18+ grants are a known target but enumerating them is research, not transcription.

---

## SC-004 — DC and Maryland v. Trump

**Record header**
- ID: SC-004
- Title / business: DC and Maryland v. Trump
- Family member: (foreign Emoluments Clause litigation)
- Scope: LITIG
- `primary_sources`: **absent** (field not present on the record)

**Evidence prose extracted from `summary`**
- "Reached the Fourth Circuit on standing and zone-of-interests"
- "vacated and remanded as moot in January 2021 after Trump left office"

**Per-phrase mapping**

1. "Reached the Fourth Circuit … vacated and remanded as moot in January 2021"
   - Likely variant: `court_filing` (the record is itself a litigation entry; its evidence is the case record).
   - Fields needed but not fully present: docket number, specific filing/opinion identifiers, URL(s). A `court_filing` mapping would also distinguish which filing — the Fourth Circuit ruling vs. the vacatur — the entry points at.
   - Already present supporting the mapping: case name "DC and Maryland v. Trump" (the record title); court "the Fourth Circuit"; a date "January 2021" (the moot vacatur/remand). This is the best-anchored of the six records.

**Open questions**
- The summary references both the Fourth Circuit stage and the vacatur — potentially two distinct `court_filing` entries (an appellate ruling and the disposition). Whether to record one entry or several is a curation decision.
- No docket number or court-document URL is in the text.

**Coverage estimate**
High. The record is a single case and the `summary` surfaces the court and the disposition date directly. One well-anchored `court_filing` target; only docket/URL detail is missing.

---

## SC-005 — Blumenthal v. Trump

**Record header**
- ID: SC-005
- Title / business: Blumenthal v. Trump
- Family member: (congressional standing case)
- Scope: LITIG
- `primary_sources`: **absent** (field not present on the record)

**Evidence prose extracted from `summary`**
- "DC Circuit held individual members of Congress lacked standing to sue over foreign Emoluments Clause violations absent institutional authorization"

**Per-phrase mapping**

1. "DC Circuit held individual members of Congress lacked standing…"
   - Likely variant: `court_filing` (litigation record; evidence is the case record).
   - Fields needed but not present: docket number, decision date, opinion identifier, URL.
   - Already present supporting the mapping: case name "Blumenthal v. Trump" (the record title); court "DC Circuit"; the holding described. No date — the `summary` does not state when the DC Circuit ruled (note `period` is `2017-2020`, a range, not a decision date).

**Open questions**
- The decision date is not in the text — only the `2017-2020` `period` range. The research pass needs the specific ruling date.
- No docket number or court-document URL is present.

**Coverage estimate**
High. Single case, court named, holding summarized. One `court_filing` target; decision date, docket, and URL are missing.

---

## SC-006 — Burisma board engagement

**Record header**
- ID: SC-006
- Title / business: Burisma board engagement
- Family member: Hunter Biden
- Scope: OOS
- `primary_sources`: **absent** (field not present on the record)

**Evidence prose extracted from `summary`**
- "Burisma is a Cyprus-registered private holding company"

**Per-phrase mapping**

1. "Burisma is a Cyprus-registered private holding company"
   - Likely variant: reserved `corporate_registration` is the closest fit (the claim rests on a corporate-registry record).
   - Fields a research pass would want: registry name and jurisdiction (the record gives "Cyprus"), company registration number, registered name, incorporation date, URL.
   - Already present supporting the mapping: jurisdiction "Cyprus-registered"; entity type "private holding company". No registry record, number, or URL named.

**Open questions**
- The `summary` cites "the documented record" and "no Ukrainian state ownership in the documented record" generically — it asserts what the evidence shows without naming the underlying sources. Only the Cyprus registration is a discrete documentary anchor.
- `documented_amount` carries "~$3.4M to Rosemont Seneca Bohai LLC (entity-level inflows)" — a figure with an unnamed source. The amount and the entity "Rosemont Seneca Bohai LLC" appear in `documented_amount`, **not** in `summary`, so they are noted here but not extracted as `summary` phrases per the handoff's transcription scope. The research pass should decide whether the financial records behind that figure (and Rosemont Seneca Bohai LLC's own registration) become separate `PrimarySource` entries.
- Whether the Cyprus registration uses reserved `corporate_registration` or the generic no-`type` variant is a methodology decision.

**Coverage estimate**
Low. The `summary` is predominantly methodological framing about why the case is excluded (Cyprus registration, absence of Ukrainian state ownership, symmetry of exclusion). It contains one discrete documentary phrase (the Cyprus registration) and otherwise references "the documented record" without naming sources. The `documented_amount` field points at financial evidence whose source the record does not name.

---

## Summary table

| Record | Evidence phrases | Variants implied | Coverage |
|---|---|---|---|
| SC-001 | 2 | `sec_filing`, `press_disclosure` ×2 | High |
| SC-002 | 3 | `press_disclosure`/`advocacy_report` (ambiguous), `congressional_letter`/generic (ambiguous), `court_filing` | Moderate |
| SC-003 | 1 | reserved `corporate_registration` (imperfect) | Low |
| SC-004 | 1 (spanning 2 stages) | `court_filing` | High |
| SC-005 | 1 | `court_filing` | High |
| SC-006 | 1 | reserved `corporate_registration` (imperfect) | Low |

**Cross-record open questions for the research pass**
- CREW (SC-002): `press_disclosure` vs. reserved `advocacy_report` — a methodology call on how advocacy-organization material is classified.
- "House Oversight Committee documents" (SC-002): no active variant cleanly covers congressional *documents* that are not letters.
- State IP-office grants (SC-003) and corporate-registry records (SC-006): no active variant covers either; reserved `corporate_registration` is the nearest, and a dedicated variant may be warranted.
- SC-001, SC-002, SC-005 all lack dates on at least one source; SC-004 is the only record whose `summary` carries a usable date.

*End of worksheet. No record content or schema was changed in producing this document.*
