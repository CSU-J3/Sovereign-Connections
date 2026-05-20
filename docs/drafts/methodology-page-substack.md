---
TITLE OPTIONS (pick one, delete the others):
1. What this tracker counts, and why
2. The rule before it gets applied
3. What counts as a foreign sovereign payment, and what doesn't

DEK / SUBTITLE OPTIONS:
1. The rule, the cases that test it, and the frameworks it isn't.
2. A methodology, walked through the cases that bound it.
3. (None; let the title carry it.)
---

On January 16, 2025, four days before the second Trump inauguration, a vehicle controlled by Sheikh Tahnoon bin Zayed Al Nahyan, the United Arab Emirates' National Security Advisor and chair of multiple state-backed investment vehicles, acquired a 49% stake in World Liberty Financial for $500 million. $187 million flowed to Trump family entities at signing. $31 million flowed to entities associated with Steve Witkoff, the President's Special Envoy for Peace Missions. The transaction went undisclosed for more than a year. The Wall Street Journal reviewed the underlying deal documents and published the allocations on January 31, 2026.

The Sovereign Connections Tracker logs sovereign-source money flowing to businesses in which named family members of the current administration, and as of v2.0 a defined set of senior administration appointees, hold documented financial interests. The rule is built around what primary records make documentable: the existence of the flow and the structure of the parties at each end of it.

Below: the rule, the cases that test its boundaries, and the legal frameworks it isn't. Burisma as the case the framework excludes despite political salience. The Apollo-channel flows in the Witkoff fact pattern as the case excluded despite documented strategic intent on the sovereign side. The Tahnoon transaction as the case included under v1.x with the convergent-interest flag attached. The Witkoff Group / Pakistan-Roosevelt sequence as the case the v2.0 expansion captures.

What this post does not do: allege quid pro quo, speculate about intent, or claim documented flows caused any policy outcome. The descriptive posture is the project's first commitment to the reader.

## The core rule

The rule has four defined terms doing the work. The canonical text sits in the repo's PROJECT.md under "Defined terms"; this section paraphrases for context and points back for precision.

Foreign sovereign and sovereign-adjacent money is the load-bearing definition. The category captures direct payments from foreign government treasuries; investments by sovereign wealth funds (the SWF Institute's recognized list as the canonical reference); investments by entities majority-owned by a foreign government; investments where a controlling-interest chain runs to a sovereign body, regardless of intermediate layers; and payments by foreign government officials acting in their official capacity. Public-market minority shareholdings without governance rights are out. Trade in publicly traded securities on a regular open market is out. The Apollo case below is the worked example for the public-market boundary.

Named family member is exhaustive and bounded. Per PROJECT.md, the list covers the President's children (biological, adopted, step) and their spouses; the President's siblings and their spouses; any relative of the President holding or having held a Senate-confirmed position during this administration; and any relative of a Senate-confirmed appointee in one of those relationships to the President. Friends, business associates without a family tie, in-laws of in-laws, and romantic partners short of marriage are excluded. Borderline cases default to exclusion. The bright line is documented relationship, not personal proximity.

Financial interest is borrowed from the federal conflict-of-interest framework rather than constructed. The five categories (per 5 CFR 2640.103(a) and 18 USC 208(a)) are: ownership stake in any form; employment by the entity, including consulting and contractor relationships; debt instruments held by the named family member where the entity is the obligor; beneficial interest in a trust where the entity is among the trust's holdings; and spousal interests imputed under 18 USC 208(a)(2). Anything outside these five categories does not count, even when the appearance is suggestive.

Connected business sits on top of the financial-interest definition. An entity qualifies where a named family member holds one of the five interest types and the connection is established through OGE Form 278 filings, SEC filings, public corporate registrations, court filings, or the foreign-jurisdiction equivalents (UK Companies House, Saudi General Authority for Investment registrations, UAE free-zone disclosures). Investigative reporting alone does not establish the connection. Reporting can corroborate or surface a primary record; it cannot stand in for one.

The rule tracks the foreign Emoluments Clause's central concern (foreign-state-source value reaching domestic officeholders) and what primary records can support. A literal Emoluments Clause analysis arguably fails on the Tahnoon-WLF facts: the value reaches Trump family entities through a private vehicle rather than the principal personally, and the source is a state-backed firm rather than the UAE proper. The tracker captures the transaction because the controlling-interest chain runs through Tahnoon's official roles to the cap table. A broader rule captures more cases at the cost of drifting into causal claims the documented record does not support. Narrower-than-this misses the mechanism actually doing the work.

## Burisma: the case the rule excludes

Hunter Biden held a board seat at Burisma Holdings from May 2014 to April 2019. Reuters reviewed bank records showing approximately $3.4 million flowing from Burisma to Rosemont Seneca Bohai LLC, an entity associated with Hunter Biden's business partners, between April 2014 and November 2015 (two monthly payments of $83,333 labeled "consulting services"). Compensation figures circulating in the public record vary because they describe different things: entity-level inflow, principal-level take, combined Archer/Biden board compensation. The Senate HSGAC/Finance joint report (September 2020) characterized payments at "as much as $50,000 per month" to Hunter Biden personally, citing news reporting rather than direct bank records. Burisma operated during a period when Vice President Biden coordinated US-Ukraine policy.

The case dominated 2019 and 2020 oversight discourse and remains a touchstone in current discussion. By the rule the tracker uses, it is out of scope.

Burisma Holdings was a Cyprus-registered private holding company. From 2011 forward, control sat with Brociti Investments Limited, also Cyprus-registered and owned by Mykola Zlochevsky. No Ukrainian government equity in Burisma, Brociti, or any operating subsidiary appears in the documented record. No payments from the Ukrainian Treasury, any Ukrainian ministry, or any Ukrainian state-owned enterprise to Burisma during Hunter Biden's board tenure are documented. The flow of money in the Burisma case ran from a private company to its board. It did not run from a foreign sovereign source to a connected business.

Real state ties exist in the case. They run through the owner's history rather than through the company's ownership structure. Zlochevsky served as Ukraine's Minister of Ecology and Natural Resources from July 2010 to April 2012; Burisma secured nine production licenses for hydrocarbon extraction during that period. AntAC's 2012 research and subsequent Ukrainian prosecutorial investigations have walked the licensing question in detail. That fact pattern describes a private actor monetizing prior state office, which is a recognized category in PEP-risk frameworks. It is not the category this tracker is built to capture. The Burisma working reference in the repo walks each criterion in detail.

Stating the Burisma exclusion explicitly does two things. It shows the rule is not tuned to a particular party. It pre-empts the complaint that the project is selective. A Trump-family-connected board seat at a foreign-oligarch-owned private company with revenues dependent on home-country state licensing would also fall outside scope, by the same rule applied the same way. The Hunter Biden / Burisma case raises questions that belong in different oversight beats (post-office monetization by a former minister, board-seat influence-peddling, FARA exposure, the Lobbying Disclosure Act). Real questions. Not this tracker's questions.

## The Apollo bound: structure over intent

The harder boundary case is one the secondary commentariat has often skipped: a fact pattern where the rule excludes flows even though documented strategic intent exists on the sovereign side.

The Witkoff Group's 2022-onward financing for The Brook, a 52-story Brooklyn rental tower, came from Apollo Commercial Real Estate Finance Inc. (NYSE: ARI), a publicly traded mortgage REIT managed by an Apollo Global Management affiliate. ARI took control of the development site through foreclosure on the prior developer in August 2022; Witkoff joined the project as the deal proceeded. The Qatar Investment Authority has been an ARI common shareholder since 2015. Per the Witkoff Group's October 2, 2025 letter to the New York Times, QIA's position runs to roughly $125 million in common and $160 million in preferred equity, under 10% of ARI's $1.5 billion equity capitalization, with no board seat, no approval authority, and no decision-making rights over which loans the REIT writes. Middle East Forum's April 2023 data placed QIA as the third-largest ARI common shareholder behind BlackRock and Vanguard at 7.4%. Apollo's spokeswoman told the NYT that QIA does not direct the trust's lending decisions, and that Witkoff properties were a small percentage of the trust's deals.

The Belgrove Palm Beach $100 million loan, made in May 2025, was originally framed in NYT reporting as coming from "the Apollo trust, a fund partly owned by Qatar." The NYT corrected the framing on October 5, 2025: the Belgrove lender was Apollo Global Management itself, not a Qatar-linked Apollo subsidiary or trust. Apollo Global Management is publicly traded (NYSE: APO) with Vanguard, BlackRock, State Street, and Capital Group as principal shareholders. No documented QIA stake in APO at any control-implying level appears in the record.

Both flows fail the controlling-interest-chain test. A minority public-market shareholder with no governance rights does not constitute sovereign control over a NYSE-listed REIT's lending decisions. A NYSE-listed asset manager's loan from corporate balance sheet is not a sovereign-source vehicle absent a documented controlling stake at the parent. The NYT's own correction confirms that the underlying framing was imprecise.

The case is harder because of what is documented on the strategic-intent side. Joey Allaham, a former Stonington Strategies lobbyist for Qatar, has described two 2017-2018 meetings on the record. Late 2017 at the St. Regis with Sheikh Mohammed bin Hamad al-Thani (the Qatari emir's brother), discussing Park Lane and Trump access. Early 2018 at QIA's Manhattan headquarters, where Allaham has stated investing in Trump-allied projects via Apollo's REIT was discussed. The strategic framing was that QIA's third-largest shareholding in ARI could be steered toward Trump-allied real estate without QIA itself directing the trust's investment decisions. Apollo and QIA both deny the strategy was implemented.

The rule excludes the resulting flows anyway. Documented intent is not the same as documented control. The methodology test turns on structural mechanism: who in fact had governance rights at the moment the loan was written. A 7.4% public-market shareholding does not turn the issuer's loans into sovereign payments, regardless of what any party has articulated as the relationship's strategic purpose. The same finding would attach to a Democratic-side analogue with the same structure under the symmetry test.

## WLF: the case the rule includes

World Liberty Financial Inc. (WLF) is a decentralized finance protocol and stablecoin issuer founded in 2024 by Zachary Folkman, Chase Herro, Alex Witkoff, Zach Witkoff, and Trump family members (Donald Trump Jr., Eric Trump, Barron Trump). Donald Trump and Steve Witkoff are listed in corporate documentation as "co-founders emeritus." Per disclosures summarized in publicly available reporting, Trump family entities receive 75% of net proceeds from WLFI token sales and a cut of stablecoin profits. The Witkoff family holds an unspecified stake and receives a cut of token sales as well.

The WLF capital structure changed materially on January 16, 2025. A vehicle named Aryam, controlled by Sheikh Tahnoon bin Zayed Al Nahyan, acquired a 49% stake for $500 million. Public Citizen's reading of the underlying documents (subsequently reported by the Wall Street Journal in January 2026) places $187 million flowing to Trump family entities at signing and $31 million flowing to Witkoff-associated entities. The transaction was not publicly disclosed for more than a year. On May 1, 2025, MGX (an Abu Dhabi state-backed AI investment vehicle that Tahnoon also chairs) used WLF's USD1 stablecoin to settle a $2 billion investment in Binance.

The transaction qualifies under the v1.x rule on multiple fronts. Trump children are co-founders. Trump family financial interest is documented in dollar terms at the Tahnoon transaction closing. Tahnoon's controlling-interest chain to UAE sovereign vehicles satisfies the sovereign-source test through his official roles (UAE National Security Advisor, deputy ruler of Abu Dhabi) plus his chairmanship of state-backed firms including ADQ, IHC, G42, and MGX. The House Select Committee on the Strategic Competition Between the United States and the Chinese Communist Party, in its February 4, 2026 letter to Zach Witkoff at WLF, frames Tahnoon's status as serving "at the pinnacle of the UAE's intelligence services and security apparatus" while simultaneously running Abu Dhabi's sovereign wealth fund and several technology investment firms. Public Citizen's analysis observes that Tahnoon's investment portfolio cannot cleanly be separated from his policy portfolio.

The Tahnoon transaction also carries the convergent-interest flag. The flag attaches when the same transaction sends documented value to both a covered intermediary (a senior administration appointee under v2.0) and a named family member of the principal. Witkoff is a senior administration appointee in his Special Envoy capacity. The $31 million allocation to Witkoff-associated entities at the Tahnoon closing is documented in the same primary records as the $187 million to Trump family entities. The flag is a record-level field, not a separate inclusion trigger; a record without it still qualifies if it meets the criteria. Records carrying the flag are presented in a higher evidence category on the dashboard.

What this section does not assert. It does not allege the Tahnoon transaction was a quid pro quo. It does not claim the November 19, 2025 AI chip export approvals to UAE-linked companies were caused by the WLF deal. It does not claim Witkoff's negotiating posture in the Iran or Gaza talks was influenced by his retained interests. The page documents flows and fields. The reader draws what inferences the documented record will support.

## v2.0: covered intermediaries

The v1.x rule captures sovereign-source flows to businesses where named family members hold financial interests. The Witkoff fact pattern surfaced a structural gap: senior administration appointees can hold retained financial interests in businesses receiving sovereign-source money from governments whose policy portfolios overlap with the appointee's official duties, without any family member of the principal being on the cap table. A rule keyed only to family members misses these.

The worked example is the Witkoff Group / Pakistan-Roosevelt Hotel sequence. In January 2026, Zach Witkoff negotiated an agreement with Pakistan's finance minister Muhammad Aurangzeb to incorporate WLF cryptocurrency into Pakistan's financial system. Steve Witkoff subsequently negotiated, in his envoy capacity, a US-Pakistan exploration of redeveloping the Roosevelt Hotel in Manhattan, an asset owned by Pakistan International Airlines Investment Limited, a Pakistani state-owned enterprise. Steve Witkoff's August 13, 2025 OGE Form 278e on file with the White House documents continuing equity exposures across multiple Witkoff Group affiliates.

The v2.0 expansion adds covered intermediaries. A record qualifies under v2.0 where (1) a senior administration appointee or designated envoy holds a financial interest (per the same five-category 5 CFR 2640.103(a) / 18 USC 208(a) definition) in a connected business, (2) that connected business receives foreign sovereign or sovereign-adjacent money, (3) the foreign government providing or controlling that money has policy interests overlapping with the appointee's official duties, and (4) the financial-interest connection is established through category 1 sources and the sovereign-source flow through category 1 or through category 3 reporting that cites underlying primary documents.

The portfolio-overlap test is the bound that prevents sprawl. A Treasury appointee with retained interests in a Gulf-funded business does not qualify under v2.0 unless Treasury portfolio touches Gulf sovereign-financial relations. A Middle East envoy with the same retained interest does qualify, because the portfolio-overlap test is satisfied directly. The test is documented per record on this page where the record turns on a contested feature. v1.x records logged before v2.0 are not re-examined; the change is forward-looking.

## What this rule isn't

Adjacent legal frameworks each interest themselves in foreign corruption or in officeholder financial conflicts; none of them is the rule the tracker uses. Five distinctions matter.

Not the foreign Emoluments Clause analysis itself. Constitutional Emoluments analysis turns on whether the officeholder personally receives foreign-state-source value. The tracker captures family-and-business receipts as a related but distinct category. A foreign Emoluments Clause case might or might not be brought on a record the tracker logs (DC and Maryland v. Trump and Blumenthal v. Trump are the recent litigation reference points); the tracker documents the flow and structure, not the constitutional theory.

Not Section 7031(c) of the State Department appropriations act. 7031(c) bars foreign government officials and their immediate family members from US entry where the Secretary of State has credible information of "significant corruption." The statute lists "corruption related to the extraction of natural resources" as illustrative, language that makes the framework look closer to this tracker's beat than it is. 7031(c) targets foreign officials for their conduct. The tracker tracks domestic officeholders receiving foreign-state-source value. The Burisma-adjacent figure publicly designated under 7031(c) was Ihor Kolomoyskyy in March 2021, on his conduct as Dnipropetrovsk Oblast Governor. The designation does not turn on Burisma ownership and does not bear on whether Burisma payments to Hunter Biden were sovereign-source (they were not).

Not FARA. The Foreign Agents Registration Act covers unregistered representation of foreign principals. A connected business receiving Gulf sovereign money is not a FARA question for the family member or appointee unless that person is also acting as a foreign government's agent.

Not FIRRMA, 18 USC 208, or 5 CFR 2635.204. FIRRMA gives CFIUS authority to review foreign acquisitions on national-security grounds. 18 USC 208 and 5 CFR Part 2640 cover the criminal and administrative conflict-of-interest framework for officeholders, and supply the five-category financial-interest definition the tracker borrows. 5 CFR 2635.204 governs gifts from foreign governments to executive-branch employees. Each is adjacent. None asks the question this tracker asks.

Not the Lobbying Disclosure Act. LDA covers domestic lobbying expenditures. Different transaction class entirely.

Records will sometimes overlap with FARA filings, 7031(c) designations, FIRRMA/CFIUS reviews, 18 USC 208 issues, or Emoluments Clause litigation. The repo dashboard links to adjacent records and does not assume the adjacent framework's verdict.

Sovereign wealth funds operate with varying degrees of independence from their governments. Treating the Public Investment Fund as identical to the Saudi state, or Mubadala as identical to the UAE government, oversimplifies. PROJECT.md commits the project to a per-SWF governance appendix documenting each fund's governance structure, its relationship to its government, and the documentary basis for treating it as sovereign-source.

## Disclosed gaps and cadence

Disclosed-gap principle. When a record's sovereign-source chain or financial interest cannot be established from primary records, the gap is disclosed rather than papered over. The Apollo question above is the live worked example: secondary reporting framed it one way; primary-record verification (and the NYT's own October 5, 2025 correction) closed it the other way. Disclosing gaps makes the records that survive verification stronger.

Soft-flag principle. Records that belong in the dataset but should not count toward headline totals carry a flag with a documented reason. A typical case: the sovereign-source finding is well-documented but the financial-interest documentation is weaker, or the reverse. The reason is on the record. The flag is a signal that the record exists at a different evidence level, not a hedge.

Cadence. This tracker has the slowest cadence of the three projects in the portfolio. Foreign sovereign flows surface through SEC filings, OGE Form 278e disclosures, FARA filings, court records, and reporting; each runs on its own clock. New records get logged when the underlying primary record posts. The tracker does not chase real-time news cycles.

Errors and corrections. Errors get corrected publicly through entries in the repo's changelog, not silent edits. The same evidentiary standard the methodology applies to its sources applies to itself.

## What comes next

Burisma and Witkoff working references in the repo document the worked examples in detail and disclose the gaps where primary-record verification is still pending. The Affinity Partners record, the Trump Organization 2017-2020 foreign-government bookings, the foreign Emoluments Clause litigation, and the Ivanka Trump China trademark grants are in the dashboard as comparative-set entries.

This page is versioned and dated for a reason. Push back on the rule, the bounding tests, the symmetry framing, or the worked examples. The changelog documents where the rule has changed and why. Future changes will document the same.

---

## Primary sources

- Sovereign Connections Tracker repo: https://github.com/CSU-J3/Sovereign-Connections
- PROJECT.md (canonical defined terms): https://github.com/CSU-J3/Sovereign-Connections/blob/main/PROJECT.md
- Burisma working reference: https://github.com/CSU-J3/Sovereign-Connections/blob/main/docs/references/burisma-methodology-reference.md
- Witkoff working reference: https://github.com/CSU-J3/Sovereign-Connections/blob/main/docs/references/witkoff-methodology-reference.md
- Changelog: https://github.com/CSU-J3/Sovereign-Connections/blob/main/docs/changelog.md
- SWF Institute (canonical SWF list): https://www.swfinstitute.org/sovereign-wealth-fund-rankings/
- 5 CFR 2640.103(a): https://www.ecfr.gov/current/title-5/chapter-XVI/subchapter-B/part-2640/subpart-A/section-2640.103
- 18 USC 208: https://www.law.cornell.edu/uscode/text/18/208
- Section 7031(c), P.L. 116-94 (statutory text via CRS R46362): https://crsreports.congress.gov/product/pdf/R/R46362
- State Department public designation of Ihor Kolomoyskyy (March 5, 2021): https://2017-2021.state.gov/public-designation-of-oligarch-and-former-ukrainian-public-official-ihor-kolomoyskyy/
- Wall Street Journal, Sam Kessler, Rebecca Ballhaus, Eliot Brown, and Angus Berwick, "'Spy Sheikh' Bought Secret Stake in Trump Company" (January 31, 2026): https://www.wsj.com/politics/policy/spy-sheikh-secret-stake-trump-crypto-tahnoon-ea4d97e8
- New York Times, Debra Kamin et al., "Where Mideast Envoy Pitched Peace, His Son Pitched Investors" (September 26, 2025; correction posted October 5, 2025): [TK: retrieve direct nytimes.com URL — paywalled article, not indexed in open search results]
- Witkoff Group / Parlatore Law Group letter to the NYT Standards Editor (October 2, 2025): https://cdn01.dailycaller.com/wp-content/uploads/2025/10/Read-the-Letter-to-the-New-York-Times-1.pdf
- House Select Committee on the Strategic Competition Between the United States and the Chinese Communist Party, letter from Rep. Ro Khanna to Zach Witkoff (February 4, 2026): https://democrats-selectcommitteeontheccp.house.gov/sites/evo-subsites/democrats-selectcommitteeontheccp.house.gov/files/evo-media-document/2-4-26-scc-letter-to-wlf.pdf
- Public Citizen, "Conflict Coin: How the Trumps' Billion-Dollar Crypto Stake Depends on a Company That Helped Iran Evade Sanctions": https://www.citizen.org/article/trump-crypto-world-liberty-financial-binance-iran-sanctions/
- Reuters (via Euronews syndication), Polina Ivanova, Maria Tsvetkova, Ilya Zhegulev, and Luke Baker, "What Hunter Biden did on the board of Ukrainian energy company Burisma" (October 18, 2019): https://www.euronews.com/2019/10/18/what-hunter-biden-did-on-the-board-of-ukrainian-energy-company-burisma
- Senate Homeland Security and Governmental Affairs Committee / Finance Committee joint report, "Hunter Biden, Burisma, and Corruption: The Impact on U.S. Government Policy and Related Concerns" (Johnson / Grassley, September 23, 2020): https://www.finance.senate.gov/imo/media/doc/HSGAC%20-%20Finance%20Joint%20Report%202020.09.23.pdf (full PDF); press release at https://www.finance.senate.gov/chairmans-news/johnson-grassley-release-report-on-conflicts-of-interest-investigation
- District of Columbia and State of Maryland v. Trump (D. Md. 8:17-cv-01596-PJM; 4th Cir. 18-2486): https://www.citizensforethics.org/legal-action/lawsuits/dc-md-trump-emoluments/ (CREW case page); Fourth Circuit en banc opinion (May 14, 2020) at https://www.ca4.uscourts.gov/opinions/182486.P.pdf
- Blumenthal v. Trump (D.D.C. 1:17-cv-01154; Constitutional Accountability Center as counsel): https://clearinghouse.net/case/15893/ (Civil Rights Litigation Clearinghouse case page)
