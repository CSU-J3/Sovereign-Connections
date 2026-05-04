import Link from "next/link";
import { getRecordCounts } from "@/lib/data";

export function HeaderBar() {
  const { total, live } = getRecordCounts();
  return (
    <header
      className="border-b"
      style={{
        backgroundColor: "var(--bg-panel)",
        borderColor: "var(--border-strong)",
      }}
    >
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-x-4 gap-y-1 px-4 py-2.5">
        <Link
          href="/"
          className="text-[11px] font-medium uppercase tracking-[0.5px]"
          style={{ color: "var(--accent-amber)" }}
        >
          SC <span style={{ color: "var(--text-dim)" }}>//</span>{" "}
          SOVEREIGN CONNECTIONS
        </Link>
        <nav
          className="flex items-center gap-4 text-[10px] uppercase tracking-[0.5px]"
          style={{ color: "var(--text-dim)" }}
        >
          <Link
            href="/swfs"
            className="transition hover:text-[var(--text-secondary)]"
          >
            ★ SWFs
          </Link>
          <Link
            href="/methodology"
            className="transition hover:text-[var(--text-secondary)]"
          >
            Methodology
          </Link>
          <span>
            {total} records
            <span style={{ color: "var(--text-dim)" }}> · </span>
            {live} live
            <span style={{ color: "var(--text-dim)" }}> · </span>
            pre-launch
          </span>
        </nav>
      </div>
    </header>
  );
}
