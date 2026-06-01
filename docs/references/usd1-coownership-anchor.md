# Catalog/record anchor — USD1 co-ownership (primary), and SC-007 precision fix

**Date:** 2026-05-30
**Status:** ready for a small handoff — SC-007 source enrichment + precision fix
**Owner:** CJ
**Retires:** the owed "USD1 co-ownership primary anchor" (catalog hygiene from SC-007)

## The find

The USD1 co-ownership fact is now anchored to a **primary document**: BitGo's own USD1 Reserve Reports (the monthly attestation packages). The co-ownership statement appears verbatim in the reserve report on page 2 of every monthly package examined (Dec 2025, Jan, Feb, Mar 2026), in identical language:

> "USD1 is issued and redeemed by [BitGo], and the USD1 brand and certain associated trademarks are owned and controlled by World Liberty Financial, Inc. and SC Financial Technologies, LLC (together, with their respective affiliates, 'WLF')."

Four consecutive months carry the same sentence, so it is settled standing language, not a one-off.

**Stored source documents** (committed to the repo with this anchor): four monthly USD1 Reserve Attestation packages —
`docs/sources/usd1-attestations/USD1_Reserve_Attestation_Report_December_2025.pdf` (and January, February, March 2026). Each is a Crowe LLP examination report + BitGo's USD1 Reserve Report.

## The precision fix — issuance vs. brand ownership

SC-007 currently treats "WLF / SC Financial Technologies co-own USD1." That is correct as to the *brand*, but the primary document draws a clean line the record should preserve:

- **BitGo issues, mints, redeems, and custodies USD1.** (BitGo Bank & Trust, N.A. — a national trust bank; see entity note below.) "World Liberty Financial does not issue or custody USD1 directly."
- **WLF, Inc. and SC Financial Technologies, LLC own and control the USD1 brand and associated trademarks.**

So the defensible wording for SC-007:

> The USD1 brand and associated trademarks are owned and controlled by World Liberty Financial, Inc. and SC Financial Technologies, LLC (the two Witkoff-held entities at 41.8.1 / 41.9.1). USD1 is issued, minted, redeemed, and custodied by BitGo (BitGo Bank & Trust, N.A.), not by WLF.

This is sharper than "co-own USD1": it gets right what the Witkoff entities actually hold (the brand) versus what a third party operates (issuance/custody). It does not weaken SC-007 — the entities the MGX settlement and Pakistan MOU run through still own the brand the stablecoin trades under — it just states the structure the way the primary document does.

## Evidentiary characterization — read this before citing

The co-ownership sentence sits in the **"USD1 Reserve Report"** portion of the package, which each report **footnotes as "Not subject to the Independent Accountant's Examination Report."** Crowe attested the *reserve figures*, not the brand-ownership sentence.

So characterize it precisely: this is **BitGo's own formal representation in a published attestation document** — a party statement by the issuer about who owns the brand — **not** an auditor-attested fact. That is entirely appropriate for a brand-ownership fact (an auditor would not opine on trademark ownership), and it is still primary (the issuer's own published statement). For a belt-and-suspenders registry-grade anchor, the **USPTO trademark registration** for the USD1 mark and its registered owner remains an optional future pull (`tmsearch.uspto.gov`); not required given the attestation statement.

## Entity note (minor, for precision if the record names the issuer)

The Dec 9 2025 package was issued by **BitGo Technologies, LLC**; from Dec 31 2025 onward it is **BitGo Bank & Trust, N.A.** Per the Dec report's footnote, BitGo Trust Company converted to BitGo Bank & Trust, N.A. following **OCC approval on 2025-12-12**. If SC-007 names the issuer/custodian, it's now an OCC-regulated national trust bank.

## Optional enrichment — USD1 supply scale (primary)

If SC-007 wants to convey the magnitude of the asset the Witkoff entities own the brand of, the attestations give clean primary figures for total USD1 redeemable tokens outstanding:

| Date | USD1 outstanding |
|------|------------------|
| 2025-12-09 | $2.73B |
| 2025-12-31 | $3.31B |
| 2026-01-31 | $5.07B |
| 2026-02-17 | $5.14B (peak in window) |
| 2026-03-31 | $4.39B |

Roughly doubled over the window the MGX settlement and Pakistan MOU sit in. Use only if the record documents scale; otherwise hold as a note. (No causal claim — scale is not causation.)

## Drift-guard note

- This only firms up *who owns the USD1 brand* and *who issues it*. The MGX→USD1 settlement and the Pakistan MOU legs of SC-007 are unchanged.
- No causal claim is added. Brand ownership and supply scale are structural facts, not evidence any official act followed.
- Keep the BitGo issuance role and the WLF/SC brand-ownership role distinct in the record — conflating "owns the brand" with "issues the coin" is the precise error this fix corrects.

## Source grades

| Fact | Source | Grade |
|------|--------|-------|
| WLF Inc. + SC Financial Technologies own/control USD1 brand & trademarks | BitGo USD1 Reserve Report, p.2 (Dec 2025–Mar 2026) | **primary (issuer's published representation; not auditor-attested)** |
| BitGo issues/mints/redeems/custodies USD1; WLF does not | BitGo USD1 Reserve Report + WLF docs | **primary** |
| Reserve figures / USD1 outstanding | BitGo USD1 Reserve Report, Crowe-examined | **primary (auditor-attested)** |
| BitGo Trust → BitGo Bank & Trust N.A., OCC approval 2025-12-12 | Dec 2025 report footnote | primary |
| USD1 trademark registered owner | USPTO (not yet pulled) | registry — optional future anchor |

## Handoff tasks (small)

1. **Store sources:** commit the four attestation PDFs to `docs/sources/usd1-attestations/` (Dec 2025, Jan, Feb, Mar 2026). These are the cited primary documents. (Binary files; confirm the repo isn't configured to reject PDFs — none of the existing data is binary, so check `.gitattributes`/`.gitignore` first.)
2. **SC-007 fix:** replace any "WLF/SC Financial Technologies issue/co-own USD1" wording with the issuance-vs-brand-ownership wording above. Add the attestation as a `primary_source` (issuer representation), characterized precisely (not auditor-attested for the ownership line). Increment SC-007 source count.
3. **Optional:** add the supply-scale figures if the record documents scale; otherwise skip.
4. **Verify:** SC-007 validates; the BitGo-issues / WLF-owns distinction is preserved; no causal claim added; `tsc --noEmit` + `next build` green; regression guard green.
5. **Commit** as a small PR or docs+data commit; report SC-007's new source count.

## Still owed after this

- **Lunate** governance verification (state-owned vs state-adjacent; distinct from MGX) before any catalog entry.
- Methodology one-line note on retained/off-filing holdings.
- (MGX ownership anchor — see `docs/references/mgx-ownership-anchor.md`, if not already applied.)
