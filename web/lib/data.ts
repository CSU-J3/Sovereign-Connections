import recordsJson from "@/data/records.json";
import entitiesJson from "@/data/sovereign_entities.json";
import type {
  Framework,
  Scope,
  Source,
  SovereignEntity,
  SovereignRecord,
} from "@/lib/types";

const RECORDS = recordsJson as SovereignRecord[];
const ENTITIES = entitiesJson as SovereignEntity[];

export function getAllRecords(): SovereignRecord[] {
  return RECORDS;
}

export function getRecordById(id: string): SovereignRecord | undefined {
  return RECORDS.find((r) => r.id === id);
}

export function getAllEntities(): SovereignEntity[] {
  return ENTITIES;
}

export function getEntityById(id: string): SovereignEntity | undefined {
  return ENTITIES.find((e) => e.id === id);
}

export function getRecordCounts(): {
  total: number;
  live: number;
} {
  return {
    total: RECORDS.length,
    live: RECORDS.filter((r) => r.scope === "LIVE").length,
  };
}

export interface FilterState {
  scope: Scope | undefined;
  frameworks: Framework[];
  sources: Source[];
}

export function filterRecords(
  records: SovereignRecord[],
  filters: FilterState,
): SovereignRecord[] {
  return records.filter((r) => {
    if (filters.scope && r.scope !== filters.scope) return false;
    if (filters.frameworks.length > 0) {
      const overlap = filters.frameworks.some((f) => r.frameworks.includes(f));
      if (!overlap) return false;
    }
    if (filters.sources.length > 0) {
      if (!filters.sources.includes(r.source)) return false;
    }
    return true;
  });
}
