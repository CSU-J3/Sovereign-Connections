"""ADV/IAPD structured ingest for a single firm CRD (Handoff #35, build slice 1).

Recon (#34, ``docs/collectors/adv-iapd-discovery.md`` §8) returned Verdict A: the
current-period Form ADV data is a scriptable *structured* surface, so this is a
join, not a PDF parse. Given a firm CRD, this module fetches and assembles the
firm's current ADV filing from the live structured surface into one object that
holds the firm's Item 5 totals, its owner rows, and its private funds with their
Schedule D 7.B fields.

Surfaces (all per §8 — read there, not reconstructed here):
  - Firm summary JSON — ``https://api.adviserinfo.sec.gov/search/firm/{CRD}``.
    A ~1.3 KB card; used only to learn the current ``advFilingDate`` (which month's
    bulk file to pull) and cross-check the legal name / SEC number. It does NOT
    carry the schedules.
  - Monthly Part 1 data files (CSV) — indexed by
    ``…/reports/foia/reports_metadata.json`` (section ``advFilingData``), downloaded
    from ``…/reports/foia/advFilingData/{year}/{fileName}``. Same multi-table CSV
    schema as the #33 historical bulk set. The bare ``…/reports/foia/{fileName}``
    path 403s; the ``{section}/{year}`` segments are required.

Tables joined on ``FilingID``:
  - ``IA_ADV_Base`` (split _A/_B) — firm-level Item 5: ``5F2c`` regulatory AUM,
    ``5F3`` non-US AUM (Item 5.F(3)); ``1E1`` CRD, ``1D`` SEC#, ``1A`` legal name.
  - ``IA_Schedule_D_7B1`` — per private fund: ``Fund Name``, ``Fund ID``,
    ``Fund Type``, ``Gross Asset Value``, ``Owners``, ``%Owned Non-US``.
  - ``IA_Schedule_A_B`` — direct/indirect owners: ``Full Legal Name``, ``DE/FE/I``,
    ``Title or Status``, ``Ownership Code``, ``Control Person``.

The proxy limit from #33/#34 stands and is not the ingest's to resolve: the ADV
gives ownership *shape* (how much is non-US, how concentrated), never owner
*identity*. This module copies the structured fields verbatim; it makes no
sovereign claim.

SEC automated-access policy: ``www.sec.gov`` and the reports host expect a
declared User-Agent (name + contact). Override with env ``ADV_IAPD_UA``.

Run: ``.venv/Scripts/python -m collectors.adv_iapd.ingest 315482`` (Windows) /
``.venv/bin/python -m collectors.adv_iapd.ingest 315482`` (macOS/Linux).
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = REPO_ROOT / ".cache" / "adv_iapd"

API_HOST = "https://api.adviserinfo.sec.gov"
REPORTS_HOST = "https://reports.adviserinfo.sec.gov"
METADATA_URL = f"{REPORTS_HOST}/reports/foia/reports_metadata.json"

# SEC policy requires a real contact in the UA. Overridable so a different
# deployer declares their own contact rather than the maintainer's.
DEFAULT_UA = "Sovereign-Connections OSINT research; contact c837394916@rams.colostate.edu"
USER_AGENT = os.environ.get("ADV_IAPD_UA", DEFAULT_UA)

# Known-good reference for the seeded pilot, from the #34 recon (and the #33
# samples). validate() checks the assembled object against these so a silent
# drift in the source surface fails loudly instead of flowing into candidates.
KNOWN_GOOD = {
    "315482": {
        "filing_date": "2026-03-22",
        "regulatory_aum": 6160297411,
        "non_us_aum": 6097061904,
        "fund_count": 6,
        "non_us_fund": ("AFFINITY PARTNERS PARALLEL FUND I LP", 4307145842, 6, 100),
    }
}


def _get(url: str, accept: str | None = None) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if accept:
        req.add_header("Accept", accept)
    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read()


def _iso_date(mmddyyyy: str) -> str:
    """``MM/DD/YYYY`` (with optional trailing time) -> ISO ``YYYY-MM-DD``."""
    d = mmddyyyy.strip().split()[0]
    mm, dd, yyyy = d.split("/")
    return f"{yyyy}-{int(mm):02d}-{int(dd):02d}"


def firm_summary(crd: str) -> dict:
    """The firm card: current filing date + identifiers (to pick the bulk month)."""
    raw = json.loads(_get(f"{API_HOST}/search/firm/{crd}", accept="application/json"))
    hits = raw.get("hits", {}).get("hits", [])
    if not hits:
        raise SystemExit(f"firm CRD {crd} not found on IAPD search")
    ia = json.loads(hits[0]["_source"]["iacontent"])
    bi = ia.get("basicInformation", {})
    sec_type = bi.get("iaSECNumberType")
    sec_num = bi.get("iaSECNumber")
    return {
        "crd": str(bi.get("firmId", crd)),
        "legal_name": bi.get("firmName"),
        "sec_number": f"{sec_type}-{sec_num}" if sec_type and sec_num else None,
        "filing_date": _iso_date(bi["advFilingDate"]),
    }


def _pick_monthly(filing_date_iso: str) -> tuple[str, str]:
    """The ``advFilingData`` (year, fileName) whose date range covers the filing.

    fileNames are ``ADV_Filing_Data_YYYYMMDD_YYYYMMDD.zip``; the firm's filing
    lands in the file for the month it was submitted.
    """
    meta = json.loads(_get(METADATA_URL, accept="application/json"))
    target = filing_date_iso.replace("-", "")  # YYYYMMDD
    section = meta.get("advFilingData", {})
    for year, block in section.items():
        if not year.isdigit():
            continue
        for f in block.get("files", []):
            name = f.get("fileName", "")
            parts = name.replace(".zip", "").split("_")
            if len(parts) >= 5 and parts[-2] <= target <= parts[-1]:
                return year, name
    raise SystemExit(
        f"no advFilingData monthly file covers {filing_date_iso}; the filing may be "
        "more recent than the latest published bulk file (see §8 daily compilation feed)"
    )


def _cached_zip(year: str, file_name: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    dest = CACHE_DIR / file_name
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    url = f"{REPORTS_HOST}/reports/foia/advFilingData/{year}/{file_name}"
    dest.write_bytes(_get(url))
    return dest


def _csv_rows(zf: zipfile.ZipFile, table: str):
    """All rows of the member(s) for ``table``, matched on exact table name.

    The bulk zip holds many tables sharing a prefix (``IA_Schedule_D_7B1`` vs
    ``IA_Schedule_D_7B1A17b`` etc.), so a substring match grabs the wrong columns.
    Match the basename as ``{table}[_<LETTER>]_<YYYYMMDD>_<YYYYMMDD>.csv`` — the
    optional single-letter segment is the ``IA_ADV_Base_A``/``_B`` split.
    """
    pat = re.compile(rf"^{re.escape(table)}(_[A-Z])?_\d{{8}}_\d{{8}}\.csv$")
    names = [n for n in zf.namelist() if pat.match(n.split("/")[-1])]
    rows = []
    for name in names:
        with zf.open(name) as fh:
            rows.extend(csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace")))
    return rows


def _to_int(s: str | None) -> int | None:
    s = (s or "").strip()
    return int(s) if s.lstrip("-").isdigit() else None


def fetch_firm(crd: str) -> dict:
    """Assemble the firm's current ADV filing into one structured object."""
    crd = str(crd)
    summary = firm_summary(crd)
    year, file_name = _pick_monthly(summary["filing_date"])
    zip_path = _cached_zip(year, file_name)

    with zipfile.ZipFile(zip_path) as zf:
        base = [r for r in _csv_rows(zf, "IA_ADV_Base") if r.get("1E1") == crd]
        if not base:
            raise SystemExit(f"CRD {crd} not found in {file_name} IA_ADV_Base")
        # The filing matching the summary's date; else the highest FilingID.
        base.sort(key=lambda r: _to_int(r.get("FilingID")) or 0)
        chosen = next(
            (r for r in base if _iso_date(r["DateSubmitted"]) == summary["filing_date"]),
            base[-1],
        )
        filing_id = chosen["FilingID"]

        funds = [
            {
                "fund_name": r["Fund Name"],
                "fund_id": r.get("Fund ID"),
                "fund_type": r.get("Fund Type"),
                "gross_asset_value": _to_int(r.get("Gross Asset Value")),
                "beneficial_owner_count": _to_int(r.get("Owners")),
                "percent_non_us_owners": _to_int(r.get("%Owned Non-US")),
            }
            for r in _csv_rows(zf, "IA_Schedule_D_7B1")
            if r.get("FilingID") == filing_id
        ]
        owners = [
            {
                "name": r["Full Legal Name"],
                "de_fe_i": r.get("DE/FE/I"),
                "title_or_status": r.get("Title or Status"),
                "ownership_code": r.get("Ownership Code"),
                "control_person": r.get("Control Person"),
            }
            for r in _csv_rows(zf, "IA_Schedule_A_B")
            if r.get("FilingID") == filing_id
        ]

    return {
        "crd": crd,
        "legal_name": chosen.get("1A") or summary["legal_name"],
        "sec_number": chosen.get("1D") or summary["sec_number"],
        "filing_id": filing_id,
        "filing_date": summary["filing_date"],
        "source_dataset": file_name,
        "source_table": "IA_Schedule_D_7B1",
        "item5": {
            "regulatory_aum": _to_int(chosen.get("5F2c")),
            "non_us_aum": _to_int(chosen.get("5F3")),
        },
        "owners": owners,
        "private_funds": funds,
    }


def validate(firm: dict) -> None:
    """Fail loudly if a known-good firm doesn't reproduce its recon figures.

    Step 2 of Handoff #35: 'If the assembled object doesn't reproduce these, stop
    and flag the gap rather than adjusting numbers to fit.'
    """
    kg = KNOWN_GOOD.get(firm["crd"])
    if not kg:
        return
    checks = {
        "filing_date": firm["filing_date"] == kg["filing_date"],
        "regulatory_aum": firm["item5"]["regulatory_aum"] == kg["regulatory_aum"],
        "non_us_aum": firm["item5"]["non_us_aum"] == kg["non_us_aum"],
        "fund_count": len(firm["private_funds"]) == kg["fund_count"],
    }
    name, gav, owners, pct = kg["non_us_fund"]
    match = next((f for f in firm["private_funds"] if f["fund_name"] == name), None)
    checks["non_us_fund"] = bool(
        match
        and match["gross_asset_value"] == gav
        and match["beneficial_owner_count"] == owners
        and match["percent_non_us_owners"] == pct
    )
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(
            f"ingest validation FAILED for CRD {firm['crd']} on {failed}; "
            "the source surface drifted — stop, do not emit"
        )


def main(argv: list[str]) -> None:
    crd = argv[1] if len(argv) > 1 else "315482"
    firm = fetch_firm(crd)
    validate(firm)
    print(json.dumps(firm, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv)
