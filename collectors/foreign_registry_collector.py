"""Foreign jurisdiction registry collector.

Pulls corporate registrations and ownership records from foreign
jurisdictions, starting with UK Companies House (which has a real API)
and extending to Saudi GAFI, UAE free-zone disclosures, and other
registries relevant to the connected-business set. OCCRP databases serve
as a fallback where direct registry access is unavailable. Source:
per-jurisdiction registries. Cadence: varies by jurisdiction.
"""


def main():
    raise NotImplementedError("foreign_registry_collector is a stub")


if __name__ == "__main__":
    main()
