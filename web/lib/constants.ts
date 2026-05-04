import type { Framework, Scope, Source } from "@/lib/types";

export const SCOPES: Scope[] = ["LIVE", "COMP", "LITIG", "OOS"];

export const SCOPE_LABEL: Record<Scope, string> = {
  LIVE: "LIVE",
  COMP: "COMPARATIVE",
  LITIG: "LITIGATION",
  OOS: "OUT-OF-SCOPE",
};

export const SCOPE_LABEL_SHORT: Record<Scope, string> = {
  LIVE: "LIVE",
  COMP: "COMP",
  LITIG: "LITIG",
  OOS: "OOS",
};

export const SCOPE_COLOR: Record<Scope, string> = {
  LIVE: "var(--scope-live)",
  COMP: "var(--scope-comp)",
  LITIG: "var(--scope-litig)",
  OOS: "var(--scope-oos)",
};

export const FRAMEWORKS: Framework[] = [
  "EMOL",
  "FARA",
  "FIRRMA",
  "OGE",
  "LDA",
  "7031",
  "208",
];

export const FRAMEWORK_LABEL: Record<Framework, string> = {
  EMOL: "EMOL",
  FARA: "FARA",
  FIRRMA: "FIRRMA",
  OGE: "OGE",
  LDA: "LDA",
  "7031": "7031",
  "208": "§208",
};

export const FRAMEWORK_FULL: Record<Framework, string> = {
  EMOL: "foreign Emoluments Clause",
  FARA: "22 USC 611",
  FIRRMA: "FIRRMA / CFIUS",
  OGE: "5 CFR 2635",
  LDA: "2 USC 1601",
  "7031": "State 7031(c)",
  "208": "18 USC 208",
};

export const SOURCES_FILTER: Source[] = [
  "PIF",
  "MUBADALA",
  "ADIA",
  "QIA",
  "CHN",
  "MULTI",
];

export const SOURCE_LABEL: Record<Source, string> = {
  PIF: "PIF",
  MUBADALA: "MUBADALA",
  ADIA: "ADIA",
  QIA: "QIA",
  KIA: "KIA",
  NBIM: "NBIM",
  GIC: "GIC",
  CHN: "CHN",
  MULTI: "MULTI",
  NONE: "NONE",
  NA: "NA",
};

const RECORDS_WITH_WALK = new Set(["SC-001", "SC-002", "SC-006"]);

export function hasWalkButton(recordId: string): boolean {
  return RECORDS_WITH_WALK.has(recordId);
}

export const WALK_PROMPTS: Record<string, string> = {
  "SC-001":
    "Walk the sovereign-adjacent definition through the Affinity Partners record using PROJECT.md categories.",
  "SC-002":
    "Walk the foreign-Emoluments-Clause framework through the Trump Organization foreign-government bookings record using PROJECT.md categories.",
  "SC-006":
    "Apply the sovereign-adjacent definition to the Burisma case step by step using the working reference in project knowledge.",
};
