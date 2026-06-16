# Covered-adviser inventory (ADV/IAPD collector seed list)

This is the seed list for the ADV/IAPD collector. The collector runs against covered persons (per the PROJECT.md covered-persons definition) who control an SEC-registered or exempt-reporting investment adviser in which they hold a qualifying financial interest. The collector reads each seeded adviser's Form ADV and emits a candidate per private fund reporting non-US ownership. The sovereign-source test, and for the appointee prong the portfolio-overlap test, are applied at promotion, not at seeding.

The seeding gate is a qualifying financial interest under 5 CFR 2640.103(a) in the adviser. The named-family prong (v1.x) carries no divestiture requirement. The appointee prong (v2.0) does: an appointee who divested their fund holds no qualifying interest, so a divested fund has no covered-person nexus and is not seeded. The gate is checked before seeding, because seeding a divested fund would run the collector against an adviser with no covered-person connection.

## Seed list

| CRD | Adviser | Covered person | Prong | Status |
|---|---|---|---|---|
| 315482 | A Fin Management LLC (Affinity Partners) | Jared Kushner | Named family (son-in-law) | Seeded; in catalog as SC-009 |
| 335007 | 1789 Capital Management, LLC | Donald Trump Jr. (partner, "DTJ" in the ADV) | Named family (son) | Seeded this pass (Handoff #42) |

Donald Trump Jr. joined 1789 Capital as a partner in November 2024, declining a government role, so he is a named family member rather than an appointee. He is identified in the firm's Form ADV by the shorthand DTJ. Reported AUM rose to about $861M, roughly eight times the firm's original target, after he joined. A partnership interest plus the ADV identification is a qualifying financial interest under 5 CFR 2640.103(a), documented through an SEC filing. The firm brands as a venture-capital adviser, so the collector should confirm whether it is a registered adviser or a venture-capital exempt reporting adviser, which affects how complete its Form ADV is.

## Evaluated, not seeded

| Covered person | Adviser | Reason |
|---|---|---|
| Stephen Feinberg | Cerberus Capital Management (~$65B) | Divested all qualifying interests (equity, carried interest, incentive fees and allocations, capital commitments) per the February 2025 ethics agreement. Remaining ties are an administrative-services contract with Cerberus and irrevocable trusts for his adult children that he neither benefits from nor controls. Neither fits the five financial-interest categories. Worked exclusion, the appointee-prong analogue of the Charles Kushner (W-003) exclusion. |
| Scott Bessent | Key Square Group | Treasury Secretary. Presumptively divested on confirmation per standard Cabinet practice. Held out of the seed list pending verification against the OGE 278 and ethics agreement. |
| Howard Lutnick | Cantor Fitzgerald | Commerce Secretary. Presumptively divested or trusteed on confirmation. Held out pending verification against the OGE 278 and ethics agreement. |
| David Sacks | Craft Ventures | White House AI and crypto role held as a part-time special government employee, which reads as an outside advisor without formal appointment and falls outside the v2.0 appointment-level requirement. Confirm appointment status. |
| Kelly Loeffler | Bakkt | SBA Administrator. Bakkt is a crypto platform, not a private-fund adviser. No qualifying adviser. |
| Warren Stephens | Stephens Inc | Ambassador to the UK. Thin portfolio overlap, and divestiture expected on appointment. Low priority. |
| Eric Trump, Ivanka Trump, Lara Trump, Tiffany Trump, Michael Boulos | none | Not in the registered-adviser business. Eric's interests are Trump Organization real estate and the World Liberty Financial crypto stack already recorded at SC-007. |

## Symmetry note

Each evaluation turns on the documented fact pattern, not prominence. Cerberus, the largest adviser connected to any figure in the administration, is excluded because Feinberg divested. 1789 is seeded on the same standard applied to Affinity. An opposite-party analogue, holding the structural features constant, would resolve the same way.

## To verify

- Bessent (Key Square) and Lutnick (Cantor) divestiture, against their OGE 278 filings and ethics agreements. Expected to confirm exclusion. Until confirmed, both stay out of the seed list.
- Sacks appointment status (special government employee versus a covered appointment).

## Note

This inventory is a seed list, not a record of sovereign findings. Whether a seeded adviser yields an SC record depends on the collector reading its ADV Schedule D for non-US ownership and, at promotion, on the sovereign-source test (and the portfolio-overlap test for the appointee prong). The named-family prong is currently the only productive source of net-new seeds, because appointees divest their advisers on confirmation and most named family members are not in the registered-adviser business.
