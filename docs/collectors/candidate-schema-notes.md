# Candidate schema notes — cross-collector

`web/data/candidates.json` is a single shared file written by more than one
collector (OGE 278 → `CAND-001..168`, ADV/IAPD → `CAND-169..171`, more to come).
Every row carries `source_filing.source` (`oge_278`, `adv_iapd`) so the shared
writer (`collectors/common/candidate_writer.py`, Handoff #36) can regenerate one
collector's slice without touching the others, and so a reader can tell which
collector — and which schema reading — a row came from. The full candidate field
set is defined by Handoff #23 (schema) and the per-collector emitter docstrings;
this note records the cross-collector field meanings that differ by `source`.

## `covered_person` per source (Handoff #37)

`covered_person` is a top-level name string on every candidate, naming the
administration-connected person whose tie to the business the candidate documents.
It sits alongside `filer` and `business_name` and closes the gap flagged in #35:
an ADV candidate names the adviser (`filer`) and the fund (`business_name`) but
not the covered person — the reason the candidate matters. The field is uniform
across sources, populated source-appropriately:

- **`oge_278`.** An OGE Form 278e is filed *by* the covered person, so for OGE
  `covered_person` equals `filer`. That duplicates `filer` for OGE rows, but a
  single field that answers "which covered person" regardless of source is worth
  the redundancy.

- **`adv_iapd`.** From the seed, not the filing. The ADV names the adviser and the
  fund but never the covered person, and the seed *is* the list of
  covered-person-connected advisers, so the connection is known at collection, not
  inferred — Affinity (CRD 315482) maps to Jared Kushner. The value is authored in
  the source-faithful Schedule A owner form the ingest already pulls (uppercase
  `LAST, FIRST, MIDDLE`, e.g. `KUSHNER, JARED, COREY`), so it stays as
  source-faithful as the OGE `filer` it sits beside; records-layer normalization is
  deferred (the #35 casing call). Seeded per adviser in
  `collectors/adv_iapd/seed.json` and stamped on every candidate from that adviser.

The field carries a name only. A covered-person *basis* or *relationship*
(officeholder, named family member, covered intermediary, per PROJECT.md) is left
to the seed and the records layer, not asserted on the candidate.

## `rollup_value` per source (closes the Handoff #35 implicit-reuse flag)

`rollup_value` is a nullable object that carries a **value the candidate sits
within but does not itself report** — context for review, never a figure
fabricated onto the row. Its meaning is source-specific, and the slot is reused
across sources by analogy, not by identical shape:

- **`oge_278` (OGE Form 278e).** The OGE 278e holding tree nests arbitrarily deep
  via dotted entry numbers, and a leaf can report value `N/A` because the dollar
  figure rolls up to a parent (e.g. World Liberty Financial at `41.8.1`, whose
  value is carried by its parent). For such a leaf, `rollup_value` is the **nearest
  ancestor that carries a value/income figure** — `entry_number`, `entity_name`,
  `value_range`, `income_type`, `income_range` — so a reviewer can trace where the
  leaf's dollar figure lives without re-opening the parse. It is `null` when the
  row carries its own value (no ancestor to roll up to). See
  `collectors/oge_278/candidates.py` (`_rollup_value`).

- **`adv_iapd` (SEC Form ADV, Schedule D 7.B).** A candidate is a single private
  fund. `rollup_value` carries the **firm-level Item 5 totals the fund sits
  within** — `firm_regulatory_aum` (Item 5.F(2)(c)) and `firm_non_us_aum`
  (Item 5.F(3)) — so the fund's gross asset value can be read against the adviser's
  whole book. This is the **concentration denominator**: a $4.3B fund that is ~70%
  of a $6.16B adviser is a different signal than the same fund inside a $100B
  adviser. It is the ADV *analog* of the OGE parent rollup (a value the row sits
  within), reusing the slot rather than the exact OGE shape; it is firm context
  carried alongside the fund, never summed or fabricated onto the fund. See
  `collectors/adv_iapd/candidates.py` (`_candidate`).

The reuse is deliberate and bounded: both readings answer "what larger value does
this row sit inside," but the keys differ by source (an OGE rollup names an
ancestor holding; an ADV rollup names firm AUM totals). Consumers must branch on
`source_filing.source` before interpreting `rollup_value`.
