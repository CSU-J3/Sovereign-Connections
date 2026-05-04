import Link from "next/link";
import { ExpandedPanel } from "@/components/ExpandedPanel";
import { ScopePill } from "@/components/ScopePill";
import { SOURCE_LABEL } from "@/lib/constants";
import { formatPeriod } from "@/lib/format";
import { buildHref } from "@/lib/href";
import type { Framework, Scope, Source, SovereignRecord } from "@/lib/types";

export interface RecordRowFilters {
  scope: Scope | undefined;
  frameworks: Framework[];
  sources: Source[];
}

export function RecordRow({
  record,
  filters,
  expandedId,
}: {
  record: SovereignRecord;
  filters: RecordRowFilters;
  expandedId: string | undefined;
}) {
  const isExpanded = expandedId === record.id;
  const href = buildHref("/", {
    scope: filters.scope,
    frameworks: filters.frameworks,
    sources: filters.sources,
    expanded: isExpanded ? undefined : record.id,
  });

  return (
    <li>
      <Link
        href={href}
        replace
        scroll={false}
        prefetch={false}
        className={`records-row ${isExpanded ? "is-expanded" : ""}`}
      >
        <span
          aria-hidden
          style={{
            color: isExpanded
              ? "var(--accent-amber)"
              : "var(--text-dim)",
          }}
        >
          {isExpanded ? "▾" : "▸"}
        </span>
        <span
          className="text-[12px] font-medium"
          style={{ color: "var(--accent-amber)" }}
        >
          {record.id}
        </span>
        <span className="min-w-0 truncate text-[12px]">
          <span style={{ color: "var(--text-primary)" }}>
            {record.business}
          </span>
          <span style={{ color: "var(--text-dim)" }}> · </span>
          <span style={{ color: "var(--text-muted)" }}>
            {record.family_member}
          </span>
        </span>
        <span>
          <ScopePill scope={record.scope} />
        </span>
        <span
          className="col-period text-[11px]"
          style={{ color: "var(--text-dim)" }}
        >
          {formatPeriod(record.period)}
        </span>
        <span
          className="text-[10px] font-medium uppercase tracking-[0.5px]"
          style={{ color: "var(--text-muted)" }}
        >
          {SOURCE_LABEL[record.source]}
        </span>
      </Link>
      {isExpanded ? <ExpandedPanel record={record} /> : null}
    </li>
  );
}
