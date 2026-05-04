import { FRAMEWORKS, SCOPES, SOURCES_FILTER } from "@/lib/constants";
import type { Framework, Scope, Source } from "@/lib/types";

const SCOPE_SET = new Set<string>(SCOPES);
const FRAMEWORK_SET = new Set<string>(FRAMEWORKS);
const SOURCE_SET = new Set<string>(SOURCES_FILTER);

export function sanitizeScope(value: unknown): Scope | undefined {
  if (typeof value !== "string") return undefined;
  const upper = value.toUpperCase();
  return SCOPE_SET.has(upper) ? (upper as Scope) : undefined;
}

export function sanitizeFrameworks(value: unknown): Framework[] {
  if (typeof value !== "string" || value.length === 0) return [];
  const parts = value
    .split(",")
    .map((p) => p.trim().toUpperCase())
    .filter((p) => FRAMEWORK_SET.has(p));
  return Array.from(new Set(parts)) as Framework[];
}

export function sanitizeSources(value: unknown): Source[] {
  if (typeof value !== "string" || value.length === 0) return [];
  const parts = value
    .split(",")
    .map((p) => p.trim().toUpperCase())
    .filter((p) => SOURCE_SET.has(p));
  return Array.from(new Set(parts)) as Source[];
}

export function formatPeriod(period: string): string {
  return period.replace(/-(?=\d|PRES)/g, "–");
}

export function formatEvidenceCategories(
  categories: ReadonlyArray<number>,
): string {
  if (categories.length === 0) return "";
  if (categories.length === 1) return `cat ${categories[0]}`;
  const min = Math.min(...categories);
  const max = Math.max(...categories);
  const isContiguous =
    max - min + 1 === categories.length &&
    categories.every((c, i) => c === min + i);
  if (isContiguous && categories.length > 1) return `cat ${min}–${max}`;
  return `cat ${categories.join(", ")}`;
}
