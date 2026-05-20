# Handoff #15 — Substack draft URL substitutions

## What this does

Replaces four of the five TK placeholders in `docs/drafts/methodology-page-substack.md` with retrieved primary-source URLs. Leaves the NYT URL as the one remaining TK in the file. No other edits.

## The four substitutions

In the `## Primary sources` block of `docs/drafts/methodology-page-substack.md`, replace these lines exactly.

### 1. Reuters Burisma piece

**Replace:**
```
- Reuters bank-record reporting on Rosemont Seneca Bohai: [TK: insert Reuters URL]
```

**With:**
```
- Reuters (via Euronews syndication), Polina Ivanova, Maria Tsvetkova, Ilya Zhegulev, and Luke Baker, "What Hunter Biden did on the board of Ukrainian energy company Burisma" (October 18, 2019): https://www.euronews.com/2019/10/18/what-hunter-biden-did-on-the-board-of-ukrainian-energy-company-burisma
```

Note for the record: the canonical reuters.com URL for this piece didn't surface in open search. Reuters has rotated several archival URL patterns since 2019, and the AOL / Yahoo / Euronews syndications are now the more stable surfaces for citation. The Euronews mirror preserves the full text and byline. If a reuters.com URL is later found, this line should be updated.

### 2. Senate HSGAC/Finance joint report

**Replace:**
```
- Senate HSGAC/Finance joint report (September 2020): [TK: insert Senate report URL]
```

**With:**
```
- Senate Homeland Security and Governmental Affairs Committee / Finance Committee joint report, "Hunter Biden, Burisma, and Corruption: The Impact on U.S. Government Policy and Related Concerns" (Johnson / Grassley, September 23, 2020): https://www.finance.senate.gov/imo/media/doc/HSGAC%20-%20Finance%20Joint%20Report%202020.09.23.pdf (full PDF); press release at https://www.finance.senate.gov/chairmans-news/johnson-grassley-release-report-on-conflicts-of-interest-investigation
```

### 3. DC and Maryland v. Trump

**Replace:**
```
- DC and Maryland v. Trump (litigation docket): [TK: insert litigation URL]
```

**With:**
```
- District of Columbia and State of Maryland v. Trump (D. Md. 8:17-cv-01596-PJM; 4th Cir. 18-2486): https://www.citizensforethics.org/legal-action/lawsuits/dc-md-trump-emoluments/ (CREW case page); Fourth Circuit en banc opinion (May 14, 2020) at https://www.ca4.uscourts.gov/opinions/182486.P.pdf
```

### 4. Blumenthal v. Trump

**Replace:**
```
- Blumenthal v. Trump (litigation docket): [TK: insert litigation URL]
```

**With:**
```
- Blumenthal v. Trump (D.D.C. 1:17-cv-01154; Constitutional Accountability Center as counsel): https://clearinghouse.net/case/15893/ (Civil Rights Litigation Clearinghouse case page)
```

## Commit

One commit: `docs(drafts): resolve four TK URLs in Substack draft (Handoff #15)`. No other edits to the draft. The title-options block, body prose, and remaining NYT TK all stay as written.

## What this doesn't do

- **Does not resolve the NYT URL.** The September 26, 2025 Debra Kamin piece "Where Mideast Envoy Pitched Peace, His Son Pitched Investors" (with the October 5 correction note) is still TK. Multiple search angles failed to surface the canonical nytimes.com URL. Best resolved from a Times-logged-in session or the Times archive directly. Leave the line as-is in the file.
- **Does not touch the Apollo / Athene precision check.** That was Handoff #14's other unresolved item and remains the natural Handoff #16.

## After this lands

Handoff #16 candidate: Apollo / Athene precision check against `docs/references/witkoff-methodology-reference.md`. The Substack draft's Section 4 currently says "the Belgrove lender was Apollo Global Management itself, not a Qatar-linked Apollo subsidiary or trust." The Witkoff Group / Parlatore Law Group October 2, 2025 letter names the lender more precisely as "Apollo's Athene insurance vehicle." Athene is an Apollo Global Management subsidiary acquired in 2022, so the current draft characterization is defensible. The question is whether the NYT correction itself printed "Apollo Global Management" or "Athene"; the Witkoff working reference in the repo should resolve which level of precision the Substack version should land on.
