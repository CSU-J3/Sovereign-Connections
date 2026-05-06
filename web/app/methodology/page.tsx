import Link from "next/link";
import { FooterLegend } from "@/components/FooterLegend";
import { HeaderBar } from "@/components/HeaderBar";

const REPO_BLOB = "https://github.com/CSU-J3/Sovereign-Connections/blob/main";
const BURISMA_REF = `${REPO_BLOB}/docs/references/burisma-methodology-reference.md`;
const WITKOFF_REF = `${REPO_BLOB}/docs/references/witkoff-methodology-reference.md`;
const CHANGELOG = `${REPO_BLOB}/docs/changelog.md`;

const proseStyle: React.CSSProperties = {
  color: "var(--text-secondary)",
  fontFamily: "var(--font-sans)",
};

const linkClass =
  "underline decoration-dotted underline-offset-2 transition hover:text-[var(--accent-amber-bright)]";

function P({ children }: { children: React.ReactNode }) {
  return (
    <p className="mt-3 text-[13px] leading-[1.7]" style={proseStyle}>
      {children}
    </p>
  );
}

function H2({ children }: { children: React.ReactNode }) {
  return (
    <h2
      className="mt-7 mb-2 text-[14px] font-medium leading-snug"
      style={{ color: "var(--text-primary)", fontFamily: "var(--font-sans)" }}
    >
      {children}
    </h2>
  );
}

function PathLink({ href, path }: { href: string; path: string }) {
  return (
    <a href={href} target="_blank" rel="noreferrer" className={linkClass} style={{ color: "var(--text-primary)" }}>
      <code className="text-[12px]">{path}</code>
    </a>
  );
}

export default function MethodologyPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <HeaderBar />

      <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-4">
        <section
          className="mb-4 border-b pb-3"
          style={{ borderColor: "var(--border-strong)" }}
        >
          <h1
            className="text-[12px] uppercase tracking-[0.5px]"
            style={{ color: "var(--accent-amber)" }}
          >
            Methodology
          </h1>
          <p
            className="mt-2 text-[16px] font-medium leading-tight"
            style={{
              color: "var(--text-primary)",
              fontFamily: "var(--font-sans)",
            }}
          >
            What this tracker counts, and why
          </p>
          <p
            className="mt-1.5 text-[10px] uppercase tracking-[0.5px]"
            style={{ color: "var(--text-dim)" }}
          >
            Adopted v2.0 · 2026-05-05 ·{" "}
            <a
              href={CHANGELOG}
              target="_blank"
              rel="noreferrer"
              className="underline decoration-dotted underline-offset-2 transition hover:text-[var(--text-secondary)]"
            >
              changelog ↗
            </a>
          </p>
        </section>

        <P>
          On January 16, 2025, four days before the second Trump inauguration, a
          vehicle controlled by Sheikh Tahnoon bin Zayed Al Nahyan, the United
          Arab Emirates' National Security Advisor and chair of multiple
          state-backed investment vehicles, acquired a 49% stake in World
          Liberty Financial for $500 million. $187 million flowed to Trump
          family entities at signing. $31 million flowed to entities associated
          with Steve Witkoff, the President's Special Envoy for Peace Missions.
          The transaction went undisclosed for more than a year. The Wall Street
          Journal reviewed the underlying deal documents and published the
          allocations on January 31, 2026.
        </P>

        <P>
          The Sovereign Connections Tracker logs sovereign-source money flowing
          to businesses in which named family members of the current
          administration, and as of v2.0 a defined set of senior administration
          appointees, hold documented financial interests. The rule is built
          around what primary records make documentable: the existence of the
          flow and the structure of the parties at each end of it.
        </P>

        <P>
          This page sets out the inclusion and exclusion rule the tracker uses.
          It walks the cases that test the rule's boundaries: Burisma as the
          case the framework excludes despite political salience, the
          Apollo-channel flows in the Witkoff fact pattern as the case excluded
          despite documented strategic intent on the sovereign side, the Tahnoon
          transaction as the case included under v1.x with the
          convergent-interest flag attached, and the Witkoff Group /
          Pakistan-Roosevelt sequence as the case the v2.0 expansion captures.
          It distinguishes the rule from adjacent legal frameworks (the foreign
          Emoluments Clause analysis itself, FARA, 7031(c), FIRRMA, 18 USC 208,
          the Lobbying Disclosure Act). It sets out what the rule deliberately
          does not capture.
        </P>

        <P>
          What this page does not do: allege quid pro quo, speculate about
          intent, or claim the documented flows caused any policy outcome. The
          descriptive posture is the project's first commitment to the reader.
        </P>

        <H2>The core rule</H2>

        <P>
          The rule has four defined terms doing the work. The full canonical
          text sits in PROJECT.md under "Defined terms"; this page paraphrases
          for context and points back for precision.
        </P>

        <P>
          Foreign sovereign and sovereign-adjacent money is the load-bearing
          definition. The category captures direct payments from foreign
          government treasuries; investments by sovereign wealth funds (the SWF
          Institute's recognized list as the canonical reference); investments
          by entities majority-owned by a foreign government (state-owned
          enterprises); investments where a controlling-interest chain runs to a
          sovereign body, regardless of the number of intermediate layers; and
          payments by foreign government officials acting in their official
          capacity, per the foreign Emoluments Clause case law. Public-market
          minority shareholdings in NYSE-listed entities, where the sovereign
          holder has no governance rights, are out. Trade in publicly traded
          securities on a regular open market is out. The Apollo case below is
          the worked example for the public-market boundary.
        </P>

        <P>
          Named family member is exhaustive and bounded. Per PROJECT.md the list
          covers the President's children (biological, adopted, step) and their
          spouses; the President's siblings and their spouses; any relative of
          the President holding or having held a Senate-confirmed position
          during this administration; and any relative of a Senate-confirmed
          appointee who is in one of those relationships to the President.
          Friends, business associates without a family tie, in-laws of in-laws,
          and romantic partners short of marriage are excluded. Borderline cases
          default to exclusion. The bright line is documented relationship, not
          personal proximity.
        </P>

        <P>
          Financial interest is borrowed from the federal conflict-of-interest
          framework rather than constructed for the tracker. The five categories
          (per 5 CFR 2640.103(a) and 18 USC 208(a)) are: ownership stake in any
          form; employment by the entity, including consulting and contractor
          relationships; debt instruments held by the named family member where
          the entity is the obligor; beneficial interest in a trust where the
          entity is among the trust's holdings; and spousal interests imputed
          under 18 USC 208(a)(2). Anything outside these five categories does
          not count, even when the appearance is suggestive.
        </P>

        <P>
          Connected business sits on top of the financial-interest definition. A
          connected business is an entity in which a named family member holds a
          financial interest in one of the five categories above, where the
          connection is established through OGE Form 278 filings, SEC filings,
          public corporate registrations, court filings, or the
          foreign-jurisdiction equivalents (UK Companies House, Saudi General
          Authority for Investment registrations, UAE free-zone disclosures, and
          so on). Investigative reporting alone does not establish the
          connection. Reporting can corroborate or surface a primary record; it
          cannot stand in for one.
        </P>

        <P>
          Why this rule and not a broader one. The rule tracks the foreign
          Emoluments Clause's central concern (foreign-state-source value
          reaching domestic officeholders) and what primary records can support.
          Broader rules capture more cases at the cost of drifting into causal
          claims the documented record does not support. Why not a narrower one.
          A literal Emoluments Clause analysis arguably fails on the
          Tahnoon-WLF facts, because the value reaches Trump family entities
          through a private vehicle rather than the principal personally and
          the source is a state-backed firm rather than the UAE proper. The
          tracker captures the transaction because the controlling-interest
          chain runs through Tahnoon's official roles to the cap table.
          Narrower-than-this misses the mechanism actually doing the work in
          the case the tracker is built around.
        </P>

        <H2>Burisma: the case the rule excludes</H2>

        <P>
          Hunter Biden held a board seat at Burisma Holdings from May 2014 to
          April 2019. Reuters reviewed bank records showing approximately $3.4
          million flowing from Burisma to Rosemont Seneca Bohai LLC, an entity
          associated with Hunter Biden's business partners, between April 2014
          and November 2015 (two monthly payments of $83,333 labeled "consulting
          services"). Compensation figures circulating in the public record vary
          because they describe different things: entity-level inflow,
          principal-level take, combined Archer/Biden board compensation. The
          Senate HSGAC/Finance joint report (September 2020) characterized
          payments at "as much as $50,000 per month" to Hunter Biden personally,
          citing news reporting rather than direct bank records. Burisma
          operated during a period when Vice President Biden coordinated
          US-Ukraine policy.
        </P>

        <P>
          The case dominated 2019 and 2020 oversight discourse and remains a
          touchstone in current discussion. By the rule the tracker uses, it is
          out of scope.
        </P>

        <P>
          Burisma Holdings was a Cyprus-registered private holding company. From
          2011 forward, control sat with Brociti Investments Limited, also
          Cyprus-registered and owned by Mykola Zlochevsky. No Ukrainian
          government equity in Burisma, Brociti, or any operating subsidiary
          appears in the documented record. No payments from the Ukrainian
          Treasury, any Ukrainian ministry, or any Ukrainian state-owned
          enterprise to Burisma during Hunter Biden's board tenure are
          documented. The flow of money in the Burisma case ran from a private
          company to its board. It did not run from a foreign sovereign source
          to a connected business.
        </P>

        <P>
          Real state ties exist in the case. They run through the owner's
          history rather than through the company's ownership structure.
          Zlochevsky served as Ukraine's Minister of Ecology and Natural
          Resources from July 2010 to April 2012; Burisma secured nine
          production licenses for hydrocarbon extraction during that period.
          AntAC's 2012 research and subsequent Ukrainian prosecutorial
          investigations have walked the licensing question in detail. That fact
          pattern describes a private actor monetizing prior state office, which
          is a recognized category in PEP-risk frameworks. It is not the
          category this tracker is built to capture. The Burisma working
          reference at{" "}
          <PathLink
            href={BURISMA_REF}
            path="docs/references/burisma-methodology-reference.md"
          />{" "}
          walks each criterion in detail.
        </P>

        <P>
          Stating the Burisma exclusion explicitly does two things. It shows the
          rule is not tuned to a particular party. And it pre-empts the
          complaint that the project is selective. A Trump-family-connected
          board seat at a foreign-oligarch-owned private company with revenues
          dependent on home-country state licensing would also fall outside
          scope, by the same rule applied the same way. The Hunter Biden /
          Burisma case raises questions that belong in different oversight beats
          (post-office monetization by a former minister, board-seat
          influence-peddling, FARA exposure, the Lobbying Disclosure Act). They
          are real questions. They are not this tracker's questions.
        </P>

        <H2>The Apollo bound: structure over intent</H2>

        <P>
          The harder boundary case is one the secondary commentariat has often
          skipped: a fact pattern where the rule excludes flows even though
          documented strategic intent exists on the sovereign side.
        </P>

        <P>
          The Witkoff Group's 2022-onward financing for The Brook (a 52-story
          Brooklyn rental tower) came from Apollo Commercial Real Estate Finance
          Inc. (NYSE: ARI), a publicly traded mortgage REIT managed by an Apollo
          Global Management affiliate. ARI took control of the development site
          through foreclosure on the prior developer in August 2022; Witkoff
          joined the project as the deal proceeded. The Qatar Investment
          Authority has been an ARI common shareholder since 2015. Per the
          Witkoff Group's October 2, 2025 letter to the New York Times, QIA's
          position runs to roughly $125 million in common and $160 million in
          preferred equity, under 10% of ARI's $1.5 billion equity
          capitalization, with no board seat, no approval authority, and no
          decision-making rights over which loans the REIT writes. Middle East
          Forum's April 2023 data placed QIA as the third-largest ARI common
          shareholder behind BlackRock and Vanguard at 7.4%. Apollo's
          spokeswoman told the NYT that QIA does not direct the trust's lending
          decisions, and that Witkoff properties were a small percentage of the
          trust's deals.
        </P>

        <P>
          The Belgrove Palm Beach $100 million loan, made in May 2025, was
          originally framed in NYT reporting as coming from "the Apollo trust, a
          fund partly owned by Qatar." The NYT corrected the framing on October
          5, 2025: the Belgrove lender was Apollo Global Management itself, not
          a Qatar-linked Apollo subsidiary or trust. Apollo Global Management is
          publicly traded (NYSE: APO) with Vanguard, BlackRock, State Street,
          and Capital Group as principal shareholders. No documented QIA stake
          in APO at any control-implying level appears in the record.
        </P>

        <P>
          Both flows fail the controlling-interest-chain test. A minority
          public-market shareholder with no governance rights does not
          constitute sovereign control over a NYSE-listed REIT's lending
          decisions. A NYSE-listed asset manager's loan from corporate balance
          sheet is not a sovereign-source vehicle absent a documented
          controlling stake at the parent. The NYT's own correction confirms
          that the underlying framing was imprecise.
        </P>

        <P>
          The case is harder because of what is documented on the
          strategic-intent side. Joey Allaham, a former Stonington Strategies
          lobbyist for Qatar, has described two 2017-2018 meetings on the
          record. Late 2017 at the St. Regis with Sheikh Mohammed bin Hamad
          al-Thani (the Qatari emir's brother), discussing Park Lane and Trump
          access. Early 2018 at QIA's Manhattan headquarters, where Allaham has
          stated investing in Trump-allied projects via Apollo's REIT was
          discussed. The strategic framing was that QIA's third-largest
          shareholding in ARI could be steered toward Trump-allied real estate
          without QIA itself directing the trust's investment decisions. Apollo
          and QIA both deny the strategy was implemented.
        </P>

        <P>
          The rule excludes the resulting flows anyway. Documented intent is not
          the same as documented control. The methodology test turns on
          structural mechanism: who in fact had governance rights at the moment
          the loan was written. A 7.4% public-market shareholding does not turn
          the issuer's loans into sovereign payments, regardless of what any
          party has articulated as the relationship's strategic purpose. The
          same finding would attach to a Democratic-side analogue with the same
          structure under the symmetry test. The Witkoff working reference at{" "}
          <PathLink
            href={WITKOFF_REF}
            path="docs/references/witkoff-methodology-reference.md"
          />
          , Apollo-channel section, walks the underlying corporate
          documentation.
        </P>

        <H2>WLF: the case the rule includes</H2>

        <P>
          World Liberty Financial Inc. (WLF) is a decentralized finance protocol
          and stablecoin issuer founded in 2024 by Zachary Folkman, Chase Herro,
          Alex Witkoff, Zach Witkoff, and Trump family members (Donald Trump
          Jr., Eric Trump, Barron Trump). Donald Trump and Steve Witkoff are
          listed in corporate documentation as "co-founders emeritus." Per
          disclosures summarized in publicly available reporting, Trump family
          entities receive 75% of net proceeds from WLFI token sales and a cut
          of stablecoin profits. The Witkoff family holds an unspecified stake
          and receives a cut of token sales as well.
        </P>

        <P>
          The WLF capital structure changed materially on January 16, 2025, four
          days before the second inauguration. A vehicle named Aryam, controlled
          by Sheikh Tahnoon bin Zayed Al Nahyan, acquired a 49% stake in WLF for
          $500 million. Public Citizen's reading of the underlying documents
          (subsequently reported by the Wall Street Journal in January 2026)
          places $187 million flowing to Trump family entities at signing and
          $31 million flowing to Witkoff-associated entities. The transaction
          was not publicly disclosed for more than a year. On May 1, 2025, MGX
          (an Abu Dhabi state-backed AI investment vehicle that Tahnoon also
          chairs) used WLF's USD1 stablecoin to settle a $2 billion investment
          in Binance.
        </P>

        <P>
          The transaction qualifies under the v1.x rule on multiple fronts.
          Trump children are co-founders. Trump family financial interest is
          documented in dollar terms at the Tahnoon transaction closing.
          Tahnoon's controlling-interest chain to UAE sovereign vehicles
          satisfies the sovereign-source test through his official roles (UAE
          National Security Advisor, deputy ruler of Abu Dhabi) plus his
          chairmanship of state-backed firms including ADQ, IHC, G42, and MGX.
          The House Select Committee on the Strategic Competition Between the
          United States and the Chinese Communist Party, in its February 4, 2026
          letter to Zach Witkoff at WLF, frames Tahnoon's status as serving "at
          the pinnacle of the UAE's intelligence services and security
          apparatus" while simultaneously running Abu Dhabi's sovereign wealth
          fund and several technology investment firms. Public Citizen's
          analysis observes that Tahnoon's investment portfolio cannot cleanly
          be separated from his policy portfolio.
        </P>

        <P>
          The Tahnoon transaction also carries the convergent-interest flag. The
          flag attaches when the same transaction or transaction sequence sends
          documented value to both a covered intermediary (a senior
          administration appointee under v2.0) and a named family member of the
          principal (under v1.x). Witkoff is a senior administration appointee
          in his Special Envoy capacity. The $31 million allocation to
          Witkoff-associated entities at the Tahnoon closing is documented in
          the same primary records as the $187 million to Trump family entities.
          The flag is a record-level field, not a separate inclusion trigger; a
          record without it still qualifies if it meets the v2.0 criteria.
          Records carrying the flag are presented in a higher evidence category
          on the dashboard.
        </P>

        <P>
          What this section does not assert. It does not allege the Tahnoon
          transaction was a quid pro quo. It does not claim the November 19,
          2025 AI chip export approvals to UAE-linked companies were caused by
          the WLF deal. It does not claim Witkoff's negotiating posture in the
          Iran or Gaza talks was influenced by his retained interests. The page
          documents flows and fields. The reader draws what inferences the
          documented record will support.
        </P>

        <H2>v2.0: covered intermediaries</H2>

        <P>
          The v1.x rule captures sovereign-source flows to businesses where
          named family members hold financial interests. The Witkoff fact
          pattern surfaced a structural gap: senior administration appointees
          and designated envoys can hold retained financial interests in
          businesses receiving sovereign-source money from governments whose
          policy portfolios overlap with the appointee's official duties,
          without any family member of the principal being on the cap table. A
          rule keyed only to family members misses these.
        </P>

        <P>
          The worked example is the Witkoff Group / Pakistan-Roosevelt Hotel
          sequence. In January 2026, Zach Witkoff negotiated an agreement with
          Pakistan's finance minister Muhammad Aurangzeb to incorporate WLF
          cryptocurrency into Pakistan's financial system. Steve Witkoff
          subsequently negotiated, in his envoy capacity, a US-Pakistan
          exploration of redeveloping the Roosevelt Hotel in Manhattan, an asset
          owned by Pakistan International Airlines Investment Limited, a
          Pakistani state-owned enterprise. Steve Witkoff's August 13, 2025 OGE
          Form 278e (the New Entrant Report on file with the White House)
          documents continuing equity exposures across multiple Witkoff Group
          affiliates.
        </P>

        <P>
          The v2.0 expansion adds covered intermediaries. A record qualifies
          under v2.0 where (1) a senior administration appointee or designated
          envoy holds a financial interest (per the same five-category 5 CFR
          2640.103(a) / 18 USC 208(a) definition) in a connected business, (2)
          that connected business receives foreign sovereign or
          sovereign-adjacent money, (3) the foreign government providing or
          controlling that money has policy interests overlapping with the
          appointee's official duties, and (4) the financial-interest connection
          is established through category 1 sources and the sovereign-source
          flow through category 1 sources or through category 3 reporting that
          cites underlying primary documents. The four conditions are documented
          per record.
        </P>

        <P>
          "Senior administration appointee or designated envoy" is bounded. It
          covers Cabinet officers, sub-Cabinet appointees at deputy/under-secretary
          level or above, White House staff at Assistant-to-the-President level
          or above, and any individual designated as a presidential envoy,
          special envoy, ambassador-at-large, or equivalent. Career officials
          are out of scope unless they hold a political appointment meeting the
          above. Outside advisors without formal appointment are out of scope.
          The line is contestable and has been drawn explicitly so disagreements
          about it can happen on the record rather than through silent inclusion
          or exclusion.
        </P>

        <P>
          Portfolio overlap is the bound that prevents sprawl. A Treasury
          appointee with retained interests in a Gulf-funded business does not
          qualify under v2.0 unless Treasury portfolio touches Gulf
          sovereign-financial relations. A Middle East envoy with the same
          retained interest does qualify, because the portfolio-overlap test is
          satisfied directly. The test is documented per record on this
          methodology page where the record turns on a contested feature.
        </P>

        <P>
          Versioning posture. v1.x records logged before v2.0 adoption are not
          re-examined; the change is forward-looking. The 2026-05-05 entry in{" "}
          <PathLink href={CHANGELOG} path="docs/changelog.md" /> documents the
          diff, the rationale, and the worked-example references that motivated
          the change. Every methodology change is versioned and dated.
        </P>

        <H2>What this rule isn't</H2>

        <P>
          Adjacent legal frameworks each interest themselves in foreign
          corruption or in officeholder financial conflicts; none of them is the
          rule the tracker uses. Six distinctions matter for readers familiar
          with the oversight space.
        </P>

        <P>
          Not the foreign Emoluments Clause analysis itself. Constitutional
          Emoluments analysis turns on whether the officeholder personally
          receives foreign-state-source value. The tracker captures
          family-and-business receipts as a related but distinct category. A
          foreign Emoluments Clause case might or might not be brought on a
          record the tracker logs (DC and Maryland v. Trump and Blumenthal v.
          Trump are the recent litigation reference points); the tracker
          documents the flow and structure, not the constitutional theory.
        </P>

        <P>
          Not Section 7031(c) of the State Department appropriations act.
          7031(c) bars foreign government officials and their immediate family
          members from US entry where the Secretary of State has credible
          information of "significant corruption" or "gross violation of human
          rights." The statute lists "corruption related to the extraction of
          natural resources" as illustrative, language that makes the framework
          look closer to this tracker's beat than it is. 7031(c) targets foreign
          officials for their conduct; the tracker tracks domestic officeholders
          receiving foreign-state-source value. The Burisma-adjacent figure
          publicly designated under 7031(c) was Ihor Kolomoyskyy in March 2021,
          on his conduct as Dnipropetrovsk Oblast Governor. The designation does
          not turn on Burisma ownership and does not bear on whether Burisma
          payments to Hunter Biden were sovereign-source (they were not).
        </P>

        <P>
          Not FARA. The Foreign Agents Registration Act (22 USC 611-621) covers
          unregistered representation of foreign principals. A connected
          business receiving Gulf sovereign money is not a FARA question for the
          family member or appointee unless that person is also acting as a
          foreign government's agent.
        </P>

        <P>
          Not FIRRMA or CFIUS jurisdiction. The Foreign Investment Risk Review
          Modernization Act of 2018 gives CFIUS authority to review foreign
          acquisitions on national-security grounds; this tracker documents
          flows. Records can overlap, but the analyses are separate and the
          tracker does not adopt CFIUS verdicts.
        </P>

        <P>
          Not 18 USC 208 or 5 CFR Part 2640. These cover the criminal and
          administrative conflict-of-interest framework for officeholders, and
          supply the five-category financial-interest definition the tracker
          borrows. They then ask a different question: whether the officeholder
          is barred from participating in particular matters. Records can
          surface 208 exposure; this page does not make 208 findings.
        </P>

        <P>
          Not 5 CFR 2635.204 (gifts from foreign governments to executive-branch
          employees) and not the Lobbying Disclosure Act. Each governs a
          different transaction class adjacent to but outside this tracker's
          frame.
        </P>

        <P>
          Cross-framework note. Records will sometimes overlap with FARA
          filings, 7031(c) designations, FIRRMA/CFIUS reviews, 18 USC 208
          issues, or Emoluments Clause litigation. This page links to adjacent
          records and does not assume the adjacent framework's verdict.
        </P>

        <P>
          Per-SWF appendix. Sovereign wealth funds operate with varying degrees
          of independence from their governments; treating the Public Investment
          Fund as identical to the Saudi state, or Mubadala as identical to the
          UAE government, oversimplifies. PROJECT.md commits this page to a
          per-SWF governance appendix that documents each fund's governance
          structure, its relationship to its government, and the documentary
          basis for treating it as sovereign-source. The appendix grows as the
          registry grows.
        </P>

        <H2>Disclosed gaps and cadence</H2>

        <P>
          Disclosed-gap principle. When a record's sovereign-source chain or
          financial interest cannot be established from primary records, the gap
          is disclosed rather than papered over. The Apollo question discussed
          above is the live worked example: secondary reporting framed it one
          way; primary-record verification (and the NYT's own October 5, 2025
          correction) closed it the other way. Disclosing gaps makes the records
          that survive verification stronger.
        </P>

        <P>
          Soft-flag principle. Records that belong in the dataset but should not
          count toward headline totals carry a flag with a documented reason. A
          typical case: the sovereign-source finding is well-documented but the
          financial-interest documentation is weaker, or the reverse. The reason
          is on the record. The flag is not a hedge; it is a signal that the
          record exists at a different evidence level than the headline records.
        </P>

        <P>
          Cadence. This tracker has the slowest cadence of the three projects in
          the portfolio. Foreign sovereign flows surface through SEC filings,
          OGE Form 278e disclosures, FARA filings, court records (CFIUS, civil
          litigation), and reporting; each runs on its own clock. New records
          get logged when the underlying primary record posts. The tracker does
          not chase real-time news cycles. Many of the underlying records
          publish irregularly or only when triggered by litigation or media
          attention.
        </P>

        <P>
          Errors and corrections. Errors get corrected publicly through entries
          in <PathLink href={CHANGELOG} path="docs/changelog.md" />, not silent
          edits. The same evidentiary standard the methodology applies to its
          sources applies to itself.
        </P>

        <H2>What comes next</H2>

        <P>
          The Burisma working reference at{" "}
          <PathLink
            href={BURISMA_REF}
            path="docs/references/burisma-methodology-reference.md"
          />{" "}
          and the Witkoff working reference at{" "}
          <PathLink
            href={WITKOFF_REF}
            path="docs/references/witkoff-methodology-reference.md"
          />{" "}
          document the worked examples in detail and disclose the gaps where
          primary-record verification is still pending. The Affinity Partners
          record, the Trump Organization 2017-2020 foreign-government bookings,
          the foreign Emoluments Clause litigation (DC and Maryland v. Trump,
          Blumenthal v. Trump), and the Ivanka Trump China trademark grants are
          in the dashboard as comparative-set entries.
        </P>

        <P>
          This page is versioned and dated for a reason. Push back on the rule,
          the bounding tests, the symmetry framing, or the worked examples. The
          entries in <PathLink href={CHANGELOG} path="docs/changelog.md" />{" "}
          document where the rule has changed and why. Future changes will
          document the same.
        </P>

        <div
          className="mt-8 flex flex-wrap items-center gap-2 border-t pt-4"
          style={{ borderColor: "var(--border-strong)" }}
        >
          <a
            href="https://dasdemarc.substack.com/"
            target="_blank"
            rel="noreferrer"
            className="border px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.5px] transition hover:border-[var(--text-secondary)] hover:text-[var(--text-secondary)]"
            style={{
              color: "var(--text-dim)",
              borderColor: "var(--border-strong)",
            }}
          >
            das_DEMARC Substack ↗
          </a>
          <Link
            href="/"
            className="border px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.5px] transition hover:border-[var(--text-secondary)] hover:text-[var(--text-secondary)]"
            style={{
              color: "var(--text-dim)",
              borderColor: "var(--border-strong)",
            }}
          >
            ← Back to records
          </Link>
        </div>
      </main>

      <FooterLegend />
    </div>
  );
}
