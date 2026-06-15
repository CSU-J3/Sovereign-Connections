# Candidate schema notes — cross-collector

`web/data/candidates.json` is a single shared file written by more than one
collector (OGE 278 → `CAND-001..168`, ADV/IAPD → `CAND-169..171`, more to come).
Every row carries `source_filing.source` (`oge_278`, `adv_iapd`) so the shared
writer (`collectors/common/candidate_writer.py`, Handoff #36) can regenerate one
collector's slice without touching the others, and so a reader can tell which
collector — and which schema reading — a row came from. The full candidate field
set is defined by Handoff #23 (schema) and the per-collector emitter docstrings;
this note records the cross-collector field meanings that differ by `source`.

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
