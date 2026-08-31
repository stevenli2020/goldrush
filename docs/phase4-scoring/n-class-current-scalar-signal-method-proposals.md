# N-class current-scalar signal method proposals

**Status:** Approved and complete
**Scope:** Approved method and approval record for L0-009, L3-001, L3-003, L10-001 and L10-002. Implementation is documented separately. No weighting, interaction, aggregation or probability work is included. L1-006 remains complete and unchanged.

## Shared MVP recommendation

The approved input/status contract classifies each variable as `N`: one current source-backed scalar and no allowlisted history. A level alone cannot be mapped to a gold-direction signal unless an owner-approved neutral or contextual anchor exists. No such anchor is approved for these variables. Accordingly, the MVP recommendation for every variable and every horizon is a status-only method returning explicit `NOT_APPLICABLE` for a valid current record. This is a method state, not zero, neutral evidence, or a missing-data substitution.

The canonical and preserved inputs are:

| Variable | Frozen value / unit | Observation date | Status | Preserved output and history |
|---|---:|---|---|---|
| L0-009 | `1.1349607944426228 percent_per_annum` | 2026-08-28 | `AVAILABLE` | Phase 3 handoff; 1 row |
| L3-001 | `3.8954166666666663 percent_per_annum` | 2026-08-29 | `AVAILABLE` | Phase 3 handoff; 1 row |
| L3-003 | `4.23 percent_per_annum` | 2026-08-30 | `AVAILABLE` | Phase 3 handoff; 1 row |
| L10-001 | `144747 contracts` | 2026-08-25 | `AVAILABLE` | Phase 3 handoff; 1 row |
| L10-002 | `423793 contracts` | 2026-08-28 | `AVAILABLE` | Approved processed CSV named by the register; 1 row; no separate Phase 3 handoff file |

Each value, unit, date, status and source reference above is preserved in `closure/canonical_dataset.jsonl` and the matching register/output. No values are normalized or reinterpreted by this proposal.

## L0-009 — Gold Lease Rates / Forward Rates

**Economic meaning and direction.** The registry describes L0-009 as the cost and conditions of borrowing or financing physical gold, informing stock mobility and bullion-market tightness. Its gold relationship is **conditional**: financing stress or tight physical availability may support gold in some regimes, while the same rate can reflect other market conditions. It is distinct from L1 current financial opportunity cost and must not be substituted for an L1 variable.

**Method and horizons.** No anchor-free numeric rule is approved for the single `percent_per_annum` scalar. Return `NOT_APPLICABLE` for 1–5 days, 1–3 months and 1–3 years, the horizons listed by the registry; return `NOT_APPLICABLE` for 3–10 years because the registry does not list that horizon. A future numeric method would need an owner-approved level/context rule or same-variable history and a conditional interpretation.

**History.** No L0-009 history is allowlisted beyond the one current row. Do not use L1 rates, another lease series or invented history. Any future history, cadence/offset and anchor decision requires separate approval.

## L3-001 — Fed Funds Futures Expected Policy Rate

**Economic meaning and direction.** L3-001 is the market-implied expected path of Federal Reserve policy. A higher expected path generally raises expected real rates and tightens liquidity, which is negative for gold; a lower path is generally supportive. This is the Layer 3 policy-expectations path and remains separate from L1 current-decomposition variables.

**Method and horizons.** A single `percent_per_annum` level has no approved neutral policy-rate anchor, so no numeric direction is assigned. Return `NOT_APPLICABLE` for 1–5 days, 1–3 months and 1–3 years (registry-applicable), and for 3–10 years (registry-not-applicable). A future level or signed-change method requires an approved same-series history, contract/roll convention and anchor or comparison rule; L1-006, L3-002 or another policy series cannot substitute.

**History.** The contract allowlists no L3-001 history beyond its one current row. No lookback, pooling or synthetic history is permitted.

## L3-003 — Expected Terminal Policy Rate

**Economic meaning and direction.** L3-003 measures the expected endpoint of the tightening/easing cycle. A higher expected terminal rate generally implies greater long-run policy restrictiveness and opportunity cost, negative for gold; a lower expectation is generally supportive. It is a Layer 3 endpoint measure, distinct from L1 current decomposition and from the full policy-path variables.

**Method and horizons.** No numeric rule can be applied to the lone `percent_per_annum` level without an approved neutral endpoint or change comparison. Return `NOT_APPLICABLE` for 1–3 months and 1–3 years, the registry-applicable horizons, and for 1–5 days and 3–10 years, which are registry-not-applicable. A future method needs a stable same-series history and separately approved curve/contract and anchor rules; do not substitute L3-001, L3-002 or L1-006.

**History.** No L3-003 history is allowlisted beyond the one current row. No invented lookback or pooled policy history is allowed.

## L10-001 — COMEX Managed-Money Net Positioning

**Economic meaning and direction.** L10-001 measures CFTC managed-money net futures exposure. The registry assigns **conditional** direction: extreme net length can increase downside liquidation risk, while extreme net short exposure can increase squeeze risk. It is a Layer 10 amplifier, not a standalone fundamental direction.

**Method and horizons.** One `contracts` level cannot identify crowding or an extreme without a same-series baseline, nor can it resolve liquidation versus squeeze risk. Return `NOT_APPLICABLE` for 1–5 days and 1–3 months (registry-applicable), and for 1–3 years and 3–10 years (registry-not-applicable). A future numeric method requires separately approved positioning history, category/contract conventions and context rules; no arbitrary threshold or substitution from L10-002, L8 flows or price is permitted.

**History.** No L10-001 history is allowlisted beyond the one weekly row. Do not manufacture a baseline or pool other positioning categories.

## L10-002 — COMEX Gold Futures Open Interest

**Economic meaning and direction.** L10-002 measures outstanding COMEX gold futures contracts and the capacity for leveraged participation and repositioning. Direction is **conditional**: rising open interest may reinforce a trend or increase later liquidation capacity, but interpretation depends on price, volume and trader composition. It is a market-plumbing amplifier, not an independent directional claim.

**Method and horizons.** A lone `contracts` level cannot establish whether participation is crowded, trend-confirming or liquidation-prone. Return `NOT_APPLICABLE` for 1–5 days and 1–3 months (registry-applicable), and for 1–3 years and 3–10 years (registry-not-applicable). A future method needs approved same-series history plus explicit price/volume/positioning context and a rule for contract rolls and revisions; no arbitrary level or other variable's history may be used.

**History.** No L10-002 history is allowlisted beyond the one daily row in the approved processed CSV. Do not pool it with L10-001, L8 flows or gold price history.

## Status treatment for all five variables

- A finite, contract-valid `AVAILABLE` scalar returns `NOT_APPLICABLE` for all four horizons and remains traceable with its raw value, unit, timestamp and source.
- A finite `FLAG` scalar returns `NOT_APPLICABLE`, with the quality/status reason retained visibly; the flag is not silently promoted to `PASS`.
- `STALE` and `BLOCKED` are retained for audit but return `INCOMPLETE`; neither is treated as a current observation or converted to zero/neutral.
- Missing, malformed, non-finite, wrong-unit or invalid-status input returns `INCOMPLETE` with an explicit reason. A duplicate ID or duplicate current row fails the one-record contract and returns `INCOMPLETE`/rejected input.
- There is no prior record, carry-forward, fallback source or permitted-history path for these N-class proposals. No layer or Net Index denominator may be renormalized by this proposal.

## Implementation test plan (completed)

The completed WSL tests cover each reader and status-only method:

1. Accept exactly one canonical record with the expected ID, unit, finite value, valid timestamp, source reference and allowed status; reject wrong ID, wrong unit, malformed/missing fields, non-finite value, invalid status and duplicate rows.
2. Return explicit `NOT_APPLICABLE` for all four horizons for valid `AVAILABLE` fixtures, preserving value and provenance only as trace context.
3. Return the same method state for finite `FLAG` fixtures while retaining the visible flag and reason.
4. Return `INCOMPLETE` for `STALE`, `BLOCKED`, missing, malformed, non-finite and wrong-unit fixtures, with no numeric signal.
5. Verify registry horizon applicability is documented but does not create a numeric output, and verify no lookback, threshold, anchor, neutral substitution or cross-variable history is used.
6. Verify trace output records variable, horizon, raw scalar, unit, timestamp, source, input status, method state and reason/flags. Include regression coverage confirming L1-006 remains unchanged.

## Approval record

**2026-08-31:** The owner approved the status-only implementations for L0-009, L3-001, L3-003, L10-001 and L10-002 as complete and correct. All four horizons remain explicit `NOT_APPLICABLE` for valid current records; no numeric signal, history, anchor or cross-variable substitution was approved.
