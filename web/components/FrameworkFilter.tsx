import Link from "next/link";
import { FRAMEWORKS, FRAMEWORK_LABEL } from "@/lib/constants";
import { buildHref } from "@/lib/href";
import type { Framework, Scope, Source } from "@/lib/types";

export function FrameworkFilter({
  selected,
  scope,
  sources,
}: {
  selected: Framework[];
  scope: Scope | undefined;
  sources: Source[];
}) {
  return (
    <div className="filter-chips flex items-center gap-1">
      {FRAMEWORKS.map((f) => {
        const isOn = selected.includes(f);
        const next = isOn
          ? selected.filter((x) => x !== f)
          : [...selected, f];
        const href = buildHref("/", { scope, frameworks: next, sources });
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
            key={f}
            href={href}
            scroll={false}
            className="border px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.5px] transition"
            style={style}
          >
            {FRAMEWORK_LABEL[f]}
          </Link>
        );
      })}
    </div>
  );
}
