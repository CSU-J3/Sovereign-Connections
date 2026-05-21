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
 * variants carry the same base shape; only `oge_278e` adds required extra
 * fields in this pass. The other active variants and the four reserved
 * variants gain per-category extras in future handoffs as real records force
 * them.
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
  | (PrimarySourceBase & { type: "congressional_letter" })
  | (PrimarySourceBase & { type: "sec_filing" })
  // Reserved variants — accepted `type` values, extra shape deferred per case.
  | (PrimarySourceBase & { type: "sanctions_designation" })
  | (PrimarySourceBase & { type: "corporate_registration" })
  | (PrimarySourceBase & { type: "foia_release" })
  | (PrimarySourceBase & { type: "advocacy_report" });

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
