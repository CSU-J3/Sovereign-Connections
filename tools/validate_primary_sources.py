#!/usr/bin/env python3
"""Validate every ``primary_sources`` entry against the ``PrimarySource`` union (Handoff #48).

Single source of truth: ``web/lib/types.ts`` defines the ``PrimarySource`` union;
this script encodes the same rules at runtime (a typed ``tsc`` assertion does not
work — TS widens JSON string fields to ``string``, which is not assignable to the
literal ``type`` discriminants). Adding or changing a variant means updating
**both** this validator and ``types.ts``; the ``PrimarySource`` comment there
points back to this file.

Scope: ``web/data/records.json`` (``SovereignRecord[]``) and
``web/data/sovereign_entities.json`` (``SovereignEntity[]``) — every
``primary_sources`` array. ``web/data/candidates.json`` uses a different shape
(the ADV candidate ``source_filing``) and is out of scope here (a possible
parallel check later).

Run:  ``python tools/validate_primary_sources.py``
Exit: ``0`` = all sources valid; ``1`` = at least one malformed source (each
printed as a ``FAIL`` line). Mirrors the regression guards' fail mechanism.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA = REPO_ROOT / "web" / "data"
DATA_FILES = [
    ("records.json", DATA / "records.json"),
    ("sovereign_entities.json", DATA / "sovereign_entities.json"),
]

# Base shape (PrimarySourceBase). label + category required; url + retrieved_at
# optional strings. `type` is the optional discriminant.
BASE_OPTIONAL_STR = ("url", "retrieved_at")


def _is_str(v) -> bool:
    return isinstance(v, str)


def _is_str_list(v) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


# Enum value sets, mirroring the string-literal unions in types.ts.
FILING_TYPE = {"new_entrant", "annual", "amendment", "termination"}
CERT_STATUS = {
    "filer_signed_only",
    "ethics_certified",
    "oge_certified",
    "amended_post_certification",
}
DOCUMENT_TYPE = {"letter", "report", "hearing_transcript", "testimony", "referral"}
REGISTRATION_TYPE = {"company_registry", "trademark", "beneficial_ownership"}

# Per-variant required / optional extras beyond the base shape. An enum field maps
# to its allowed-value set; a free field maps to a type predicate.
VARIANTS: dict[str, dict[str, dict]] = {
    "oge_278e": {
        "required": {"filing_type": FILING_TYPE, "certification_status": CERT_STATUS},
        "optional": {"parsed_paths": _is_str_list, "entry_paths": _is_str_list},
    },
    "ethics_agreement": {"required": {}, "optional": {}},
    "press_disclosure": {"required": {}, "optional": {}},
    "court_filing": {"required": {}, "optional": {}},
    "congressional_document": {
        "required": {"document_type": DOCUMENT_TYPE},
        "optional": {"chamber_or_committee": _is_str, "document_date": _is_str},
    },
    "sec_filing": {"required": {}, "optional": {}},
    "advocacy_report": {
        "required": {"organization": _is_str},
        "optional": {"published_at": _is_str},
    },
    "corporate_registration": {
        "required": {"registration_type": REGISTRATION_TYPE},
        "optional": {
            "registry": _is_str,
            "jurisdiction": _is_str,
            "identifier": _is_str,
            "filed_at": _is_str,
        },
    },
    "form_adv": {
        "required": {"crd": _is_str},
        "optional": {
            "sec_number": _is_str,
            "filing_id": _is_str,
            "filing_date": _is_str,
            "table": _is_str,
            "fund_id": _is_str,
        },
    },
    "sanctions_designation": {"required": {}, "optional": {}},
    "foia_release": {"required": {}, "optional": {}},
}


def _check_field(field: str, spec, value) -> str | None:
    """Validate one field value against an enum set or a type predicate."""
    if isinstance(spec, set):
        if not isinstance(value, str) or value not in spec:
            return f"{field}={value!r} not in {sorted(spec)}"
    elif not spec(value):
        return f"{field}={value!r} has the wrong type"
    return None


def validate_source(src) -> list[str]:
    """Return a list of error strings for one ``primary_sources`` entry (empty = valid)."""
    if not isinstance(src, dict):
        return [f"source is not an object: {src!r}"]

    errors: list[str] = []

    # 1. Base required fields.
    label = src.get("label")
    if not isinstance(label, str) or not label.strip():
        errors.append("label is missing or not a non-empty string")
    category = src.get("category")
    # bool is a subclass of int; reject it explicitly.
    if isinstance(category, bool) or not isinstance(category, int) or not (1 <= category <= 5):
        errors.append(f"category {category!r} is not an integer in 1-5")

    # 2. Base optional fields, if present, are strings.
    for field in BASE_OPTIONAL_STR:
        if field in src and not isinstance(src[field], str):
            errors.append(f"{field} must be a string")

    # 3. Generic (untyped) shape: only base fields allowed.
    if "type" not in src:
        allowed = {"label", "category", *BASE_OPTIONAL_STR}
        unknown = sorted(set(src) - allowed)
        if unknown:
            errors.append(f"untyped source has unexpected field(s) {unknown}")
        return errors

    # 4. Typed shape.
    type_value = src["type"]
    if type_value not in VARIANTS:
        errors.append(f"unknown type {type_value!r}")
        return errors

    spec = VARIANTS[type_value]
    allowed = {
        "type",
        "label",
        "category",
        *BASE_OPTIONAL_STR,
        *spec["required"],
        *spec["optional"],
    }
    # 4a. Required extras present and valid.
    for field, field_spec in spec["required"].items():
        if field not in src:
            errors.append(f"{type_value} is missing required field {field!r}")
        else:
            err = _check_field(field, field_spec, src[field])
            if err:
                errors.append(f"{type_value} {err}")
    # 4b. Optional extras valid when present.
    for field, field_spec in spec["optional"].items():
        if field in src:
            err = _check_field(field, field_spec, src[field])
            if err:
                errors.append(f"{type_value} {err}")
    # 4c. No unknown fields (catches a misnamed field like `document_typ`).
    unknown = sorted(set(src) - allowed)
    if unknown:
        errors.append(f"{type_value} has unexpected field(s) {unknown}")
    return errors


def _short(label) -> str:
    text = label if isinstance(label, str) else ""
    return f"{text[:50]}..." if len(text) > 50 else text


def main(argv: list[str] | None = None) -> int:
    try:  # keep non-ASCII labels printable on a non-UTF-8 console (CI is UTF-8)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    total_sources = 0
    total_errors = 0
    for fname, path in DATA_FILES:
        if not path.exists():
            print(f"FAIL: missing data file {path}")
            return 1
        records = json.loads(path.read_text(encoding="utf-8"))
        for record in records:
            rid = record.get("id", "<no-id>")
            for index, src in enumerate(record.get("primary_sources") or []):
                total_sources += 1
                for err in validate_source(src):
                    total_errors += 1
                    label = src.get("label") if isinstance(src, dict) else None
                    print(
                        f"FAIL: {fname} {rid} primary_sources[{index}] "
                        f"(label {_short(label)!r}): {err}"
                    )

    if total_errors:
        print(
            f"\n{total_errors} malformed-source error(s) across {total_sources} "
            f"sources. Fix against the PrimarySource union in web/lib/types.ts."
        )
        return 1
    print(
        f"PASS: {total_sources} primary_sources entries valid against the "
        f"PrimarySource union."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
