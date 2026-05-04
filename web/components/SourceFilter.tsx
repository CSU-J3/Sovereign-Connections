import Link from "next/link";
import { SOURCES_FILTER, SOURCE_LABEL } from "@/lib/constants";
import { buildHref } from "@/lib/href";
import type { Framework, Scope, Source } from "@/lib/types";

export function SourceFilter({
  selected,
  scope,
  frameworks,
}: {
  selected: Source[];
  scope: Scope | undefined;
  frameworks: Framework[];
}) {
  return (
    <div className="filter-chips flex items-center gap-1">
      {SOURCES_FILTER.map((s) => {
        const isOn = selected.includes(s);
        const next = isOn
          ? selected.filter((x) => x !== s)
          : [...selected, s];
        const href = buildHref("/", { scope, frameworks, sources: next });
        const style = isOn
          ? {
              backgroundColor: "var(--text-secondary)",
              color: "var(--bg-base)",
              borderColor: "var(--text-secondary)",
            }
          : {
              color: "var(--text-muted)",
              borderColor: "var(--border-strong)",
            };
        return (
          <Link
            key={s}
            href={href}
            scroll={false}
            className="border px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.5px] transition"
            style={style}
          >
            {SOURCE_LABEL[s]}
          </Link>
        );
      })}
    </div>
  );
}
