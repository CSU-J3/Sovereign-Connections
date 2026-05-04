"use client";

import { useState } from "react";

export function WalkButton({ prompt }: { prompt: string }) {
  const [copied, setCopied] = useState(false);

  async function onClick() {
    try {
      await navigator.clipboard.writeText(prompt);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      setCopied(false);
    }
    window.open("https://claude.ai/new", "_blank", "noopener,noreferrer");
  }

  return (
    <button
      type="button"
      onClick={onClick}
      className="border px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.5px] transition hover:border-[var(--text-secondary)] hover:text-[var(--text-secondary)]"
      style={{
        color: "var(--text-dim)",
        borderColor: "var(--border-strong)",
        backgroundColor: "transparent",
      }}
      aria-label="Copy walk-the-definition prompt and open Claude"
    >
      {copied ? "Prompt copied ✓" : "Walk the definition ↗"}
    </button>
  );
}
