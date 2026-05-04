import Link from "next/link";
import { FooterLegend } from "@/components/FooterLegend";
import { FrameworkFilter } from "@/components/FrameworkFilter";
import { HeaderBar } from "@/components/HeaderBar";
import { RecordRow } from "@/components/RecordRow";
import { ScopeFilter } from "@/components/ScopeFilter";
import { SourceFilter } from "@/components/SourceFilter";
import { filterRecords, getAllRecords } from "@/lib/data";
import {
  sanitizeFrameworks,
  sanitizeScope,
  sanitizeSources,
} from "@/lib/format";

type SearchParams = {
  scope?: string;
  framework?: string;
  source?: string;
  expanded?: string;
};

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: Promise<SearchParams>;
}) {
  const params = await searchParams;
  const scope = sanitizeScope(params.scope);
  const frameworks = sanitizeFrameworks(params.framework);
  const sources = sanitizeSources(params.source);
  const expandedParam =
    typeof params.expanded === "string" ? params.expanded : undefined;
  const hasFilters = !!scope || frameworks.length > 0 || sources.length > 0;

  const records = filterRecords(getAllRecords(), {
    scope,
    frameworks,
    sources,
  });
  const expandedId =
    expandedParam && records.some((r) => r.id === expandedParam)
      ? expandedParam
      : undefined;

  const labelStyle: React.CSSProperties = {
    color: "var(--text-dim)",
    minWidth: 64,
  };

  return (
    <div className="flex min-h-screen flex-col">
      <HeaderBar />

      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-4">
        <section
          className="mb-3 space-y-2 border-b pb-3"
          style={{ borderColor: "var(--border-strong)" }}
        >
          <div className="flex flex-wrap items-center gap-3">
            <span
              className="text-[10px] uppercase tracking-[0.5px]"
              style={labelStyle}
            >
              Scope
            </span>
            <ScopeFilter
              current={scope}
              frameworks={frameworks}
              sources={sources}
            />
            {hasFilters ? (
              <Link
                href="/"
                className="ml-auto text-[10px] uppercase tracking-[0.5px] transition hover:text-[var(--text-secondary)]"
                style={{ color: "var(--text-dim)" }}
              >
                Clear filters ✕
              </Link>
            ) : null}
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span
              className="text-[10px] uppercase tracking-[0.5px]"
              style={labelStyle}
            >
              Framework
            </span>
            <FrameworkFilter
              selected={frameworks}
              scope={scope}
              sources={sources}
            />
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span
              className="text-[10px] uppercase tracking-[0.5px]"
              style={labelStyle}
            >
              Source
            </span>
            <SourceFilter
              selected={sources}
              scope={scope}
              frameworks={frameworks}
            />
          </div>
        </section>

        <div
          className="border"
          style={{ borderColor: "var(--border-strong)" }}
        >
          <div className="records-header-row">
            <span aria-hidden></span>
            <span>ID</span>
            <span>Business / Family member</span>
            <span>Scope</span>
            <span className="col-period">Period</span>
            <span>Source</span>
          </div>

          {records.length === 0 ? (
            <div
              className="px-6 py-8 text-center text-[11px] uppercase tracking-[0.5px]"
              style={{ color: "var(--text-dim)" }}
            >
              No records match the active filters.
            </div>
          ) : (
            <ul>
              {records.map((r) => (
                <RecordRow
                  key={r.id}
                  record={r}
                  filters={{ scope, frameworks, sources }}
                  expandedId={expandedId}
                />
              ))}
            </ul>
          )}
        </div>
      </main>

      <FooterLegend />
    </div>
  );
}
