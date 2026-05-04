import type { Framework, Scope, Source } from "@/lib/types";

export interface QueryState {
  scope?: Scope;
  frameworks?: Framework[];
  sources?: Source[];
  expanded?: string;
}

export function buildHref(base: string, q: QueryState): string {
  const params = new URLSearchParams();
  if (q.scope) params.set("scope", q.scope);
  if (q.frameworks && q.frameworks.length > 0)
    params.set("framework", q.frameworks.join(","));
  if (q.sources && q.sources.length > 0)
    params.set("source", q.sources.join(","));
  if (q.expanded) params.set("expanded", q.expanded);
  const qs = params.toString();
  return qs ? `${base}?${qs}` : base;
}
