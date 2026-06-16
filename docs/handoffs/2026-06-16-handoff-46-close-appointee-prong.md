# Handoff #46 — Close the covered-adviser inventory appointee prong (Bessent, Lutnick verified divested)

**Repo:** Sovereign-Connections
**Path target:** `docs/handoffs/2026-06-16-handoff-46-close-appointee-prong.md`
**Depends on:** the covered-adviser inventory from #42. Branch off `main`.
**Type:** docs. Updates `docs/references/covered-adviser-inventory.md`. No records, candidates, watchlist, or PROJECT.md change.

## What this does

Closes the inventory's appointee prong. The inventory flagged Bessent (Key Square) and Lutnick (Cantor) as presumptively divested, to verify. Both are now verified: each divested the qualifying interest on confirmation, so both are OUT, the same disposition as Feinberg/Cerberus. The prong now has three documented exclusions and no in-scope subjects.

## What Code needs to do

### Step 1: Update the Bessent and Lutnick entries

Locate the inventory's Bessent and Lutnick entries (currently "presumptively divested, to verify" or similar). Update each to a verified OUT disposition with the content below. Match the inventory's existing entry format; the Feinberg exclusion is the template.

**Bessent (verified OUT):**
- Subject: Scott Bessent, Treasury Secretary. Founder, Key Square Group (RIA).
- Disposition: OUT. Divested the Key Square qualifying interest per the January 2025 ethics agreement; roughly $1B of required divestitures completed before the January 20 inauguration. Fails the qualifying-interest test, same basis as Feinberg.
- Sources: OGE ethics agreement (released January 2025, pledging the Key Square divestiture), category 1; OGE compliance correspondence to Senate Finance (August 2025), category 1, reported by Reuters, category 3.
- Caveat, out of scope: the August 2025 OGE non-compliance finding concerns residual illiquid holdings (North Dakota farmland and two private holdings), not Key Square, and OGE confirmed those do not pose conflicts. Farmland divestiture timing is a conflicts-compliance matter, not a sovereign-source flow, so it is outside this project's scope.

**Lutnick (verified OUT):**
- Subject: Howard Lutnick, Commerce Secretary. Former Chairman and CEO, Cantor Fitzgerald LP (controls Cantor, BGC Group, Newmark Group; Cantor's asset-management arm is an RIA).
- Disposition: OUT. Stepped down on confirmation (February 2025); agreed to divest all interests in Cantor, BGC, and Newmark; forwent all economic benefits as of May 16, 2025; transferred Cantor ownership to trusts for his adult children (controlled by son Brandon Lutnick) and sold BGC ($151.5M) and Newmark ($127M) stakes. Fails the qualifying-interest test, same basis and trust structure as Feinberg.
- Covered-person note: the adult-children's trusts (Brandon-controlled) do not create a retained qualifying interest for Lutnick; adult children's holdings are not imputed under 5 CFR 2640.103(a). Brandon and Kyle Lutnick are the Commerce Secretary's children, not the President's family and not Senate-confirmed, so they are not covered persons. Cantor therefore exits scope entirely.
- Sources: OGE / Commerce ethics agreement, category 1; Lutnick OGE Form 278T periodic transaction report (June 17, 2025), category 1 (extapps2.oge.gov); Cantor Fitzgerald statements (February 18 and May 2025), primary corporate disclosure; Reuters (May 2025), category 3.
- Caveat, out of scope: the certification-timing question (Reed and Warren letters, the 90-day deadline) and the separate Tesla-promotion episode are conflicts-compliance matters, not sovereign-source flows, so outside scope.

### Step 2: Update the prong-level summary

Mark the appointee prong closed. Three documented exclusions, all divested on confirmation: Feinberg/Cerberus, Bessent/Key Square, Lutnick/Cantor. No in-scope appointee RIA subjects. The divestiture test gates each out regardless of the firm's sovereign-money ties, the same symmetric standard applied to the named-family prong. 1789 Capital (Don Jr., named-family prong) remains the only in-scope ADV subject.

## Verify

- Only `covered-adviser-inventory.md` changed.
- Bessent and Lutnick entries now read OUT with sources.
- The prong summary reflects closure.
- No records, candidates, watchlist, or PROJECT.md change.

## Commit

Single commit, the inventory plus this handoff. Suggested:

```
docs(inventory): close appointee prong, Bessent and Lutnick verified divested (#46)
```

Do not push unless asked.

## Flag back, do not decide

- If the inventory's entry format differs from what's specified here, match the file.
- If a caveat reads as out-of-scope creep for the inventory, trim to the disposition plus sources and drop the caveat to a footnote.

## Out of scope

- Records, candidates, watchlist, PROJECT.md.
- Any change to the inventory's seed list. This dispositions two existing appointee entries; it adds no subjects.

---

read docs/handoffs/2026-06-16-handoff-46-close-appointee-prong.md and follow
