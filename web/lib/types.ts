export type Scope = "LIVE" | "COMP" | "LITIG" | "OOS";

export type Framework =
  | "EMOL"
  | "FARA"
  | "FIRRMA"
  | "OGE"
  | "LDA"
  | "7031"
  | "208";

export type Source =
  | "PIF"
  | "MUBADALA"
  | "ADIA"
  | "QIA"
  | "KIA"
  | "NBIM"
  | "GIC"
  | "CHN"
  | "MULTI"
  | "NONE"
  | "NA";

export type EvidenceCategory = 1 | 2 | 3 | 4 | 5;

/** OGE Form 278e filing types. Per Handoff #17 discovery / schema proposal v2. */
export type OgeFilingType =
  | "new_entrant"
  | "annual"
  | "amendment"
  | "termination";

/** OGE Form 278e certification states. Per Handoff #17 discovery / schema proposal v2. */
export type OgeCertStatus =
  | "filer_signed_only"
  | "ethics_certified"
  | "oge_certified"
  | "amended_post_certification";

/**
 * Kinds of congressional document carried by the `congressional_document`
 * variant (Handoff #38). Replaces the letter-only `congressional_letter` so the
 * variant covers committee output beyond letters. Starter set; extend as records
 * force new kinds.
 */
export type CongressionalDocumentType =
  | "letter"
  | "report"
  | "hearing_transcript"
  | "testimony"
  | "referral";

/**
 * Kinds of corporate-registry filing carried by the `corporate_registration`
 * variant (Handoff #38), so company-registry and trademark filings are one
 * variant distinguished by type. Starter set; extend as records force new kinds.
 */
export type CorporateRegistrationType =
  | "company_registry"
  | "trademark"
  | "beneficial_ownership";

/**
 * Fields shared by every primary-source variant.
 *
 * `category` is the integer evidence tier (1-5), not the union discriminant.
 * The discriminant is the optional `type` field on each variant of
 * `PrimarySource` below.
 */
interface PrimarySourceBase {
  label: string;
  url?: string;
  category: EvidenceCategory;
  retrieved_at?: string; // ISO 8601, optional
}

/**
 * A primary source cited by a record or sovereign entity.
 *
 * Discriminated union keyed on `type`. An entry with no `type` is the generic
 * shape (label / url / category) that SC-007, SC-008, and every
 * sovereign-entity source currently use — those stay valid unchanged. Typed
 * variants carry the same base shape; `oge_278e`, the three #38-activated
 * variants (`advocacy_report`, `congressional_document`, `corporate_registration`),
 * and `form_adv` add extra fields. The remaining active variants and the two
 * still-reserved variants gain per-category extras in future handoffs as real
 * records force them. Across the typed variants the report/document title reuses
 * the base `label` and the source link reuses the base `url` rather than adding
 * per-variant title/url fields; date fields follow the base `retrieved_at` ISO
 * 8601 convention (`form_adv` keeps `filing_date` to match the ADV candidate).
 *
 * Note: schema proposal v2 keyed this union on `category`, which collided with
 * the pre-existing integer evidence-tier field of the same name. Per Handoff
 * #21 sign-off the discriminant is `type`; `category` stays the evidence tier.
 */
export type PrimarySource =
  // Generic (untyped) source — the pre-existing flat shape.
  | (PrimarySourceBase & { type?: undefined })
  // Active variants.
  | (PrimarySourceBase & {
      type: "oge_278e";
      filing_type: OgeFilingType;
      certification_status: OgeCertStatus;
      parsed_paths?: string[]; // pointers into parser output
      entry_paths?: string[]; // pointers into specific parsed entries
    })
  | (PrimarySourceBase & { type: "ethics_agreement" })
  | (PrimarySourceBase & { type: "press_disclosure" })
  | (PrimarySourceBase & { type: "court_filing" })
  // Congressional output (Handoff #38) — replaces the letter-only
  // `congressional_letter`. `document_type` widens coverage beyond letters; the
  // document title is the base `label`, the link the base `url`.
  | (PrimarySourceBase & {
      type: "congressional_document";
      document_type: CongressionalDocumentType;
      chamber_or_committee?: string; // issuing chamber or committee
      document_date?: string; // ISO 8601
    })
  | (PrimarySourceBase & { type: "sec_filing" })
  // Advocacy / watchdog report (Handoff #38) — activated from reserved. Distinct
  // from `press_disclosure` (press coverage). CREW reports are the driving case;
  // title is the base `label`, link the base `url`.
  | (PrimarySourceBase & {
      type: "advocacy_report";
      organization: string; // publishing advocacy / watchdog org (e.g. CREW)
      published_at?: string; // ISO 8601 publication date
    })
  // Company-registry / trademark filing (Handoff #38) — activated from reserved.
  | (PrimarySourceBase & {
      type: "corporate_registration";
      registration_type: CorporateRegistrationType;
      registry?: string; // registry or authority (e.g. UK Companies House)
      jurisdiction?: string; // jurisdiction of the filing
      identifier?: string; // registration or filing number
      filed_at?: string; // ISO 8601
    })
  // ADV provenance (Handoff #38) for records promoted from ADV candidates,
  // aligned to the ADV candidate `source_filing` shape so a promoted record's
  // provenance matches the candidate it came from. Typed-extras modeled on
  // `oge_278e`.
  | (PrimarySourceBase & {
      type: "form_adv";
      crd: string; // firm CRD
      sec_number?: string; // SEC file number (e.g. 801-122021)
      filing_id?: string;
      filing_date?: string; // ISO 8601
      table?: string; // schedule / table, e.g. "IA_Schedule_D_7B1"
      fund_id?: string; // Schedule D 7.B fund / entry pointer
    })
  // Reserved variants — accepted `type` values, extra shape deferred per case.
  | (PrimarySourceBase & { type: "sanctions_designation" })
  | (PrimarySourceBase & { type: "foia_release" });

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
  convergent_interest_flag?: boolean;
}

export interface SovereignEntity {
  id: string;
  name: string;
  country: string;
  governance_note: string;
  primary_sources?: PrimarySource[];
}
