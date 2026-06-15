"""ADV/IAPD collector package (Phase 5, Handoff #35).

Structured ingest of SEC Form ADV current-period data for the tracker's
covered-person-connected investment advisers, plus candidate emission into
``web/data/candidates.json``. Recon (#34) returned Verdict A, so this is a
structured CSV join, not a PDF parse; see ``docs/collectors/adv-iapd-discovery.md``
(§8 is the current-period access recon). The proxy limit holds: ADV gives
ownership shape, never sovereign identity — emitted candidates stay ``unreviewed``
until a human promotes them with secondary-source identity work.
"""
