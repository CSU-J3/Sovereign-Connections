import Link from "next/link";
import { SCOPES, SCOPE_LABEL } from "@/lib/constants";
import { buildHref } from "@/lib/href";
import type { Framework, Scope, Source } from "@/lib/types";

export function ScopeFilter({
  current,
  frameworks,
  sources,
}: {
  current: Scope | undefined;
  frameworks: Framework[];
  sources: Source[];
}) {
  const options: Array<{ key: string; label: string; scope?: Scope }> = [
    { key: "ALL", label: "ALL" },
    ...SCOPES.map((s) => ({ key: s, label: SCOPE_LABEL[s], scope: s })),
  ];

  return (
    <div className="filter-chips flex items-center gap-1">
      {options.map((opt) => {
        const isOn =
          (opt.scope === undefined && current === undefined) ||
          opt.scope === current;
        const href = buildHref("/", {
          scope: opt.scope,
          frameworks,
          sources,
        });
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
            key={opt.key}
            href={href}
            scroll={false}
            className="border px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.5px] transition"
            style={style}
          >
            {opt.label}
          </Link>
        );
      })}
    </div>
  );
}
