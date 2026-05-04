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

export interface PrimarySource {
  label: string;
  url?: string;
  category: EvidenceCategory;
}

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

export interface SovereignEntity {
  id: string;
  name: string;
  country: string;
  governance_note: string;
}
