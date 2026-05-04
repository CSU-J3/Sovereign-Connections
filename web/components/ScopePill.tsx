import { SCOPE_COLOR, SCOPE_LABEL_SHORT } from "@/lib/constants";
import type { Scope } from "@/lib/types";

export function ScopePill({ scope }: { scope: Scope }) {
  return (
    <span
      className="inline-flex items-center text-[10px] font-medium uppercase tracking-[0.5px]"
      style={{ color: SCOPE_COLOR[scope] }}
    >
      ▸ {SCOPE_LABEL_SHORT[scope]}
    </span>
  );
}
