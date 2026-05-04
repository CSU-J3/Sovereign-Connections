import Link from "next/link";
import { WalkButton } from "@/components/WalkButton";
import {
  FRAMEWORK_LABEL,
  WALK_PROMPTS,
  hasWalkButton,
} from "@/lib/constants";
import { formatEvidenceCategories } from "@/lib/format";
import type { SovereignRecord } from "@/lib/types";

const labelStyle: React.CSSProperties = {
  color: "var(--text-dim)",
  letterSpacing: "0.5px",
};

export function ExpandedPanel({ record }: { record: SovereignRecord }) {
  const showWalk = hasWalkButton(record.id);
  const walkPrompt = WALK_PROMPTS[record.id];

  return (
    <div className="expanded-panel">
      <p
        className="text-xs leading-[1.6]"
        style={{
          color: "var(--text-secondary)",
          fontFamily: "var(--font-sans)",
        }}
      >
        {record.summary}
      </p>

      {record.documented_amount ? (
        <div className="mt-3 grid grid-cols-[110px_1fr] gap-y-1 text-[11px]">
          <span className="text-[10px] uppercase" style={labelStyle}>
            Amount
          </span>
          <span style={{ color: "var(--text-secondary)" }}>
            {record.documented_amount}
          </span>
        </div>
      ) : null}

      <dl className="mt-3 grid grid-cols-[110px_1fr] gap-y-1 text-[11px]">
        <dt className="text-[10px] uppercase" style={labelStyle}>
          Frameworks
        </dt>
        <dd style={{ color: "var(--text-secondary)" }}>
          {record.frameworks.map((f, i) => (
            <span key={f}>
              {i > 0 ? (
                <span style={{ color: "var(--text-dim)" }}> · </span>
              ) : null}
              {FRAMEWORK_LABEL[f]}
            </span>
          ))}
        </dd>
        <dt className="text-[10px] uppercase" style={labelStyle}>
          Evidence
        </dt>
        <dd style={{ color: "var(--text-secondary)" }}>
          {formatEvidenceCategories(record.evidence_category)}
        </dd>
      </dl>

      {record.primary_sources && record.primary_sources.length > 0 ? (
        <div className="mt-3">
          <div className="text-[10px] uppercase" style={labelStyle}>
            Primary sources
          </div>
          <ul className="mt-1 space-y-0.5 text-[11px]">
            {record.primary_sources.map((src, i) => (
              <li key={i} style={{ color: "var(--text-muted)" }}>
                {src.url ? (
                  <a
                    href={src.url}
                    target="_blank"
                    rel="noreferrer"
                    className="underline-offset-2 hover:underline"
                    style={{ color: "var(--text-secondary)" }}
                  >
                    {src.label}
                  </a>
                ) : (
                  <span style={{ color: "var(--text-secondary)" }}>
                    {src.label}
                  </span>
                )}{" "}
                <span style={{ color: "var(--text-dim)" }}>
                  · cat {src.category}
                </span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <Link
          href={`/record/${record.id}`}
          className="border px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.5px] transition hover:border-[var(--text-secondary)] hover:text-[var(--text-secondary)]"
          style={{
            color: "var(--text-dim)",
            borderColor: "var(--border-strong)",
          }}
        >
          View detail ↗
        </Link>
        {showWalk && walkPrompt ? <WalkButton prompt={walkPrompt} /> : null}
      </div>
    </div>
  );
}
