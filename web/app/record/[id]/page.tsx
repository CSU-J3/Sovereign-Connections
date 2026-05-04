import Link from "next/link";
import { notFound } from "next/navigation";
import { FooterLegend } from "@/components/FooterLegend";
import { HeaderBar } from "@/components/HeaderBar";
import { ScopePill } from "@/components/ScopePill";
import { WalkButton } from "@/components/WalkButton";
import {
  FRAMEWORK_FULL,
  FRAMEWORK_LABEL,
  SOURCE_LABEL,
  WALK_PROMPTS,
  hasWalkButton,
} from "@/lib/constants";
import { getAllRecords, getRecordById } from "@/lib/data";
import { formatEvidenceCategories, formatPeriod } from "@/lib/format";

export function generateStaticParams() {
  return getAllRecords().map((r) => ({ id: r.id }));
}

export default async function RecordDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const record = getRecordById(id);
  if (!record) notFound();

  const labelStyle: React.CSSProperties = {
    color: "var(--text-dim)",
    letterSpacing: "0.5px",
  };

  const showWalk = hasWalkButton(record.id);
  const walkPrompt = WALK_PROMPTS[record.id];

  return (
    <div className="flex min-h-screen flex-col">
      <HeaderBar />

      <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-4">
        <div
          className="mb-3 text-[10px] uppercase tracking-[0.5px]"
          style={{ color: "var(--text-dim)" }}
        >
          <Link
            href="/"
            className="transition hover:text-[var(--text-secondary)]"
          >
            ← Back to records
          </Link>
        </div>

        <header
          className="mb-4 border-b pb-3"
          style={{ borderColor: "var(--border-strong)" }}
        >
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
            <span
              className="text-[12px] font-medium uppercase tracking-[0.5px]"
              style={{ color: "var(--accent-amber)" }}
            >
              {record.id}
            </span>
            <ScopePill scope={record.scope} />
            <span
              className="text-[11px] uppercase tracking-[0.5px]"
              style={{ color: "var(--text-dim)" }}
            >
              {formatPeriod(record.period)}
            </span>
            <span
              className="text-[11px] uppercase tracking-[0.5px]"
              style={{ color: "var(--text-muted)" }}
            >
              {SOURCE_LABEL[record.source]}
            </span>
          </div>
          <h1
            className="mt-2 text-[14px]"
            style={{ color: "var(--text-primary)" }}
          >
            {record.business}
          </h1>
          <div
            className="mt-1 text-[12px]"
            style={{ color: "var(--text-muted)" }}
          >
            {record.family_member}
          </div>
        </header>

        <p
          className="text-[13px] leading-[1.7]"
          style={{
            color: "var(--text-secondary)",
            fontFamily: "var(--font-sans)",
          }}
        >
          {record.summary}
        </p>

        <dl className="mt-4 grid grid-cols-[120px_1fr] gap-y-2 text-[12px]">
          {record.documented_amount ? (
            <>
              <dt className="text-[10px] uppercase" style={labelStyle}>
                Amount
              </dt>
              <dd style={{ color: "var(--text-secondary)" }}>
                {record.documented_amount}
              </dd>
            </>
          ) : null}
          <dt className="text-[10px] uppercase" style={labelStyle}>
            Frameworks
          </dt>
          <dd style={{ color: "var(--text-secondary)" }}>
            <ul className="space-y-0.5">
              {record.frameworks.map((f) => (
                <li key={f}>
                  <span style={{ color: "var(--text-primary)" }}>
                    {FRAMEWORK_LABEL[f]}
                  </span>
                  <span style={{ color: "var(--text-dim)" }}> · </span>
                  <span style={{ color: "var(--text-muted)" }}>
                    {FRAMEWORK_FULL[f]}
                  </span>
                </li>
              ))}
            </ul>
          </dd>
          <dt className="text-[10px] uppercase" style={labelStyle}>
            Evidence
          </dt>
          <dd style={{ color: "var(--text-secondary)" }}>
            {formatEvidenceCategories(record.evidence_category)}
          </dd>
        </dl>

        {record.primary_sources && record.primary_sources.length > 0 ? (
          <div className="mt-4">
            <div
              className="text-[10px] uppercase tracking-[0.5px]"
              style={labelStyle}
            >
              Primary sources
            </div>
            <ul className="mt-1 space-y-1 text-[12px]">
              {record.primary_sources.map((src, i) => (
                <li key={i}>
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
        ) : (
          <div className="mt-4">
            <div
              className="text-[10px] uppercase tracking-[0.5px]"
              style={labelStyle}
            >
              Primary sources
            </div>
            <p
              className="mt-1 text-[11px]"
              style={{ color: "var(--text-dim)" }}
            >
              Not yet linked. Underlying records exist; link list pending.
            </p>
          </div>
        )}

        {showWalk && walkPrompt ? (
          <div className="mt-5">
            <WalkButton prompt={walkPrompt} />
          </div>
        ) : null}
      </main>

      <FooterLegend />
    </div>
  );
}
