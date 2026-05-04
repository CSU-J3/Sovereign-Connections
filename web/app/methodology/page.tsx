import Link from "next/link";
import { FooterLegend } from "@/components/FooterLegend";
import { HeaderBar } from "@/components/HeaderBar";

export default function MethodologyPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <HeaderBar />

      <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-4">
        <section
          className="mb-4 border-b pb-3"
          style={{ borderColor: "var(--border-strong)" }}
        >
          <h1
            className="text-[12px] uppercase tracking-[0.5px]"
            style={{ color: "var(--accent-amber)" }}
          >
            Methodology
          </h1>
        </section>

        <p
          className="text-[13px] leading-[1.7]"
          style={{
            color: "var(--text-secondary)",
            fontFamily: "var(--font-sans)",
          }}
        >
          The methodology essay covers the defined terms (named family member,
          financial interest, foreign sovereign and sovereign-adjacent money),
          the evidence hierarchy, scope exclusions, and the per-fund governance
          treatment for sovereign wealth funds. The canonical version is the
          Substack post; this page links to it once published rather than
          duplicating the text.
        </p>

        <p
          className="mt-3 text-[13px] leading-[1.7]"
          style={{
            color: "var(--text-secondary)",
            fontFamily: "var(--font-sans)",
          }}
        >
          For now, the working-reference content lives in{" "}
          <code
            className="text-[12px]"
            style={{ color: "var(--text-primary)" }}
          >
            PROJECT.md
          </code>{" "}
          at the repo root.
        </p>

        <div className="mt-5 flex flex-wrap items-center gap-2">
          <a
            href="https://dasdemarc.substack.com/"
            target="_blank"
            rel="noreferrer"
            className="border px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.5px] transition hover:border-[var(--text-secondary)] hover:text-[var(--text-secondary)]"
            style={{
              color: "var(--text-dim)",
              borderColor: "var(--border-strong)",
            }}
          >
            das_DEMARC Substack ↗
          </a>
          <Link
            href="/"
            className="border px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.5px] transition hover:border-[var(--text-secondary)] hover:text-[var(--text-secondary)]"
            style={{
              color: "var(--text-dim)",
              borderColor: "var(--border-strong)",
            }}
          >
            ← Back to records
          </Link>
        </div>
      </main>

      <FooterLegend />
    </div>
  );
}
