"""Filing discovery for the OGE 278 collector.

``discover_filings()`` is the seam between *finding* filings to collect and
*collecting* them. Everything downstream — the regression guard today, a real
scheduled backfill tomorrow — calls this function and iterates over what it
returns, without caring whether the list came from a hard-coded stub or a live
source.

Right now the body is a **stub**: it returns the one known Witkoff filing that
the committed ``web/data/candidates.json`` was generated from. Handoff #32
("filing discovery") replaces the *body* of ``discover_filings()`` with a real
source (OGE disclosure polling or a filer watchlist). The *signature and the
contract below do not change* — only where the list comes from.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Repo root is two levels up from collectors/oge_278/discover.py.
_REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class FilingRef:
    """A filing to collect.

    Attributes:
        source: Filesystem path of the filing's source PDF today. Handoff #32
            may widen this to a URL when discovery goes live; downstream code
            should treat it as an opaque locator the collector knows how to
            consume.
        filing_id: Stable identifier for the filing (the PDF stem today). Must
            be stable across runs — the committed snapshot is keyed to it.
    """

    source: Path
    filing_id: str


# The one filing the committed web/data/candidates.json was generated from. Kept
# as a module constant so the regression guard can tie its comparison back to
# exactly what discovery hands it.
_WITKOFF_PDF = _REPO_ROOT / "data" / "samples" / "witkoff-oge278-2025-08-13.pdf"


def discover_filings() -> list[FilingRef]:
    """Return the filings the collector should process.

    Contract for callers:
        - Returns a list of :class:`FilingRef`. Iterate it; do not assume the
          length. Callers must not care whether the list is a stub or live.
        - Today the list is exactly the filing that composes the committed
          ``web/data/candidates.json``. The regression guard relies on this to
          detect drift.

    Contract for the discovery handoff (#32):
        - Replace the body below with a real source. Keep the return type.
        - Once this returns filings beyond the committed snapshot, the
          scheduled job stops being a pure regression guard and becomes a
          backfilling collector — see the #32 downstream note in Handoff #31.

    # STUB: returns only the one known Witkoff filing. Replace in Handoff #32.
    """
    return [FilingRef(source=_WITKOFF_PDF, filing_id=_WITKOFF_PDF.stem)]
