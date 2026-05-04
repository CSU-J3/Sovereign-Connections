import { FRAMEWORKS, FRAMEWORK_FULL } from "@/lib/constants";

export function FooterLegend() {
  return (
    <footer
      className="mt-auto border-t"
      style={{
        backgroundColor: "var(--bg-panel)",
        borderColor: "var(--border-strong)",
      }}
    >
      <div
        className="mx-auto max-w-6xl px-4 py-2 text-[10px] uppercase tracking-[0.5px]"
        style={{ color: "var(--text-dim)" }}
      >
        <div className="flex flex-wrap items-center gap-3">
          <span style={{ color: "var(--scope-live)" }}>▸ LIVE</span>
          <span>active record post-2025</span>
          <span style={{ color: "var(--text-dim)" }}>·</span>
          <span style={{ color: "var(--scope-comp)" }}>▸ COMP</span>
          <span>comparative pre-2025</span>
          <span style={{ color: "var(--text-dim)" }}>·</span>
          <span style={{ color: "var(--scope-litig)" }}>▸ LITIG</span>
          <span>litigation reference</span>
          <span style={{ color: "var(--text-dim)" }}>·</span>
          <span style={{ color: "var(--scope-oos)" }}>▸ OOS</span>
          <span>out of scope</span>
        </div>
        <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-0.5">
          {FRAMEWORKS.map((f, i) => (
            <span key={f} className="flex items-center gap-1.5">
              {i > 0 ? (
                <span style={{ color: "var(--text-dim)" }}>·</span>
              ) : null}
              <span style={{ color: "var(--text-secondary)" }}>{f}</span>
              <span>= {FRAMEWORK_FULL[f]}</span>
            </span>
          ))}
        </div>
      </div>
    </footer>
  );
}
