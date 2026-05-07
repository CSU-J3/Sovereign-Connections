import Link from "next/link";
import { FooterLegend } from "@/components/FooterLegend";
import { HeaderBar } from "@/components/HeaderBar";
import { getAllEntities } from "@/lib/data";

export default function SwfsPage() {
  const entities = getAllEntities();

  return (
    <div className="flex min-h-screen flex-col">
      <HeaderBar />

      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-4">
        <section
          className="mb-4 border-b pb-3"
          style={{ borderColor: "var(--border-strong)" }}
        >
          <h1
            className="text-[12px] uppercase tracking-[0.5px]"
            style={{ color: "var(--accent-amber)" }}
          >
            Sovereign wealth fund registry
          </h1>
          <p
            className="mt-1 max-w-3xl text-[12px] leading-[1.6]"
            style={{
              color: "var(--text-secondary)",
              fontFamily: "var(--font-sans)",
            }}
          >
            Sovereign wealth funds operate with varying degrees of independence
            from their governments. Treating PIF as identical to the Saudi
            state, or Mubadala as identical to the UAE government, oversimplifies
            the underlying governance. Per-fund governance notes appear below;
            the tracker cites them rather than assuming the relationship.
          </p>
        </section>

        <ul className="space-y-3">
          {entities.map((e) => (
            <li
              key={e.id}
              className="border p-3"
              style={{ borderColor: "var(--border-strong)" }}
            >
              <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                <span
                  className="text-[12px] font-medium uppercase tracking-[0.5px]"
                  style={{ color: "var(--accent-amber)" }}
                >
                  {e.id}
                </span>
                <span
                  className="text-[12px]"
                  style={{ color: "var(--text-primary)" }}
                >
                  {e.name}
                </span>
                <span
                  className="text-[10px] uppercase tracking-[0.5px]"
                  style={{ color: "var(--text-dim)" }}
                >
                  {e.country}
                </span>
              </div>
              <p
                className="mt-2 text-[12px] leading-[1.6]"
                style={{
                  color: "var(--text-secondary)",
                  fontFamily: "var(--font-sans)",
                }}
              >
                {e.governance_note}
              </p>
              {e.primary_sources && e.primary_sources.length > 0 ? (
                <div className="mt-2">
                  <div
                    className="text-[10px] uppercase tracking-[0.5px]"
                    style={{ color: "var(--text-dim)" }}
                  >
                    Primary sources
                  </div>
                  <ul className="mt-1 space-y-1 text-[11px]">
                    {e.primary_sources.map((src, i) => (
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
              ) : null}
            </li>
          ))}
        </ul>

        <div className="mt-4">
          <Link
            href="/"
            className="text-[10px] uppercase tracking-[0.5px] transition hover:text-[var(--text-secondary)]"
            style={{ color: "var(--text-dim)" }}
          >
            ← Back to records
          </Link>
        </div>
      </main>

      <FooterLegend />
    </div>
  );
}
