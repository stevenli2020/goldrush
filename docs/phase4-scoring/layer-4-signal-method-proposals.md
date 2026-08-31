# Phase 4 Layer 4 A-class signal method proposals

**Status:** Proposal only — awaiting owner decision  
**Scope:** L4-001, L4-002, L4-003, L4-004, L4-006, L4-007, L4-008 and L4-009  
**Implementation:** None proposed in this document. No Phase 3 artifact is changed.

This document uses the frozen canonical records, their Phase 3 handoffs, the Phase 1 registry and the approved Phase 4 input/status contract. The canonical record is the input value and unit; it is not silently converted into an inflation rate, a fiscal level, a z-score or a probability.

## Common MVP rule

For a horizon with an approved observation offset `k`, select the current observation and the `k`th earlier observation from the same variable's own time-ordered allowlist. Define:

`delta = current_value - prior_value`

The proposed baseline mapping is `delta > 0 -> +1` (supports gold), `delta < 0 -> -1` (does not support gold), and `delta == 0 -> 0` (unchanged). This is a direction-only MVP signal; it is not a normalized magnitude. For L4-006, the source preserves `negative = deficit` and `positive = surplus`, so the proposed gold-direction mapping is deliberately inverted: `delta < 0 -> +1`, `delta > 0 -> -1`, and zero -> `0`.

The standard position offsets `5, 63, 252, 756` apply to daily observations. Lower-frequency series use the smallest position offset that represents the requested calendar horizon: monthly `1` for 1–3 months and `12` for 1–3 years; quarterly `12` for 1–3 years and `40` for 3–10 years; annual `3` for 1–3 years and `10` for 3–10 years. These are observation positions, not interpolated or synthetic dates. A missing required position produces `INCOMPLETE`; there is no shorter fallback.

All eight registry directions are **Conditional**. The signs below are proposed baseline mappings for the stated purchasing-power or fiscal-credibility mechanism. They do not approve a regime gate, a sign inversion, a coefficient, a variable weight or an interaction rule. Those remain separate scoring-engine decisions.

## Variable proposals

### L4-001 — CPI Inflation Rate

- **Frozen input:** `332.813 index`, observed `2026-07-01`, `AVAILABLE`, `OK`; preserved history class `A`, 954 rows. The registry calls this CPI Inflation Rate, but the canonical unit is an index. The source-backed history is monthly.
- **Meaning and direction:** A rising CPI index represents increasing realized consumer prices and purchasing-power erosion. Under the proposed baseline debasement channel, a rise supports gold (`+1`) and a fall opposes it (`-1`). Policy and real-rate responses keep the registry's conditional caveat visible; no regime inversion is proposed.
- **Transformation and horizons:** Use signed index change with the common mapping. `1–5 days: NOT_APPLICABLE` because monthly observations cannot resolve a daily horizon. `1–3 months: offset 1`; `1–3 years: offset 12`; `3–10 years: NOT_APPLICABLE` because the registry does not list that horizon. Zero index change is the only neutral result.
- **History use:** Use only the 954 allowlisted L4-001 rows, sorted by observation timestamp. Do not convert the index to a rate, pool it with L4-002, or derive a missing observation.

### L4-002 — Core PCE Inflation Rate

- **Frozen input:** `130.658 index`, observed `2026-07-01`, `AVAILABLE`, `OK`; history class `A`, 811 rows, monthly. The canonical unit is an index even though the registry name says inflation rate.
- **Meaning and direction:** A rising core PCE index indicates more persistent underlying price pressure and purchasing-power erosion. Proposed baseline: rising index `+1`, falling index `-1`, unchanged `0`; the registry's conditional policy response caveat remains.
- **Transformation and horizons:** Signed index change. `1–5 days: NOT_APPLICABLE`; `1–3 months: offset 1`; `1–3 years: offset 12`; `3–10 years: NOT_APPLICABLE` (not a registry horizon). No rate conversion or neutral level is introduced.
- **History use:** Only the 811 allowlisted L4-002 rows; no pooling with CPI or other inflation variables and no synthetic history.

### L4-003 — 5Y Breakeven Inflation

- **Frozen input:** `2.3 percent`, observed `2026-08-28`, `AVAILABLE`, `OK`; history class `A`, 5,919 rows, daily.
- **Meaning and direction:** The value is a market-implied five-year inflation expectation. A rise in the breakeven supports the purchasing-power/debasement case for gold (`+1`); a fall is `-1`. Breakevens include liquidity and risk-premium components, so the registry's conditional status is retained.
- **Transformation and horizons:** Signed percentage-point change using the standard daily offsets. `1–5 days: NOT_APPLICABLE`; `1–3 months: offset 63`; `1–3 years: offset 252`; `3–10 years: NOT_APPLICABLE`. No percent-to-fraction conversion, threshold or normalization is proposed.
- **History use:** Only the 5,919 allowlisted L4-003 daily rows. The prior must be the exact offset position after timestamp sorting; no L4-004 substitution or pooled history.

### L4-004 — 10Y Breakeven Inflation

- **Frozen input:** `2.31 percent`, observed `2026-08-28`, `AVAILABLE`, `OK`; history class `A`, 5,919 rows, daily.
- **Meaning and direction:** The value is a market-implied longer-run inflation expectation. Rising expectations support gold (`+1`) and falling expectations are `-1`, subject to the registry's conditional liquidity, risk-premium and policy caveat.
- **Transformation and horizons:** Signed percentage-point change with daily offsets. `1–5 days: NOT_APPLICABLE`; `1–3 months: NOT_APPLICABLE`; `1–3 years: offset 252`; `3–10 years: offset 756`. No arbitrary long-run anchor is used.
- **History use:** Only the 5,919 allowlisted L4-004 rows; do not substitute the 5Y series or derive a spread.

### L4-006 — Fiscal Deficit / GDP

- **Frozen input:** `-5.76906 percent_of_gdp`, observed `2025-01-01`, `AVAILABLE`, `OK`; history class `A`, 97 rows. The Phase 3 handoff preserves the annual series and the source convention `negative = deficit; positive = surplus`.
- **Meaning and direction:** This is the fiscal balance as a share of GDP. A move toward a more negative balance is a worsening deficit and, under the proposed fiscal-credibility/debasement baseline, supports gold (`+1`). A move toward surplus or a less negative deficit is `-1`; unchanged is `0`. This rule operates on the signed source value and does not invert or rewrite the frozen record.
- **Transformation and horizons:** Signed percentage-point-of-GDP change with annual offsets. `1–5 days: NOT_APPLICABLE`; `1–3 months: NOT_APPLICABLE`; `1–3 years: offset 3`; `3–10 years: offset 10`. No monthly or quarterly interpolation is proposed.
- **History use:** Only the 97 allowlisted L4-006 annual rows, with the source sign convention retained. No fiscal series is pooled or used as a replacement.

### L4-007 — Debt / GDP

- **Frozen input:** `122.59387 percent_of_gdp`, observed `2026-01-01`, `AVAILABLE`, `OK`; history class `A`, 241 rows. The Phase 3 handoff is gross federal public debt/GDP on quarterly, quarter-start dates.
- **Meaning and direction:** This is accumulated sovereign leverage. Rising debt/GDP increases the proposed fiscal-vulnerability signal (`+1`); falling debt/GDP is `-1`; unchanged is `0`. The registry's conditional definition and gross-debt scope remain explicit.
- **Transformation and horizons:** Signed percentage-point-of-GDP change. `1–5 days: NOT_APPLICABLE`; `1–3 months: NOT_APPLICABLE`; `1–3 years: offset 12` (quarterly positions); `3–10 years: offset 40`. No net-debt substitution or level threshold is proposed.
- **History use:** Only the 241 allowlisted L4-007 quarterly rows. Do not pool with L4-006 or fill quarter gaps synthetically.

### L4-008 — Interest Expense / Government Revenue

- **Frozen input:** `23.222596271472774 percent_of_federal_receipts`, observed `2025-09-30`, `AVAILABLE`, `OK`; history class `A`, 11 rows. The Phase 3 handoff is an annual gross-interest-expense/total-federal-receipts ratio at September year-end.
- **Meaning and direction:** A higher share of receipts consumed by gross interest expense indicates greater debt-service burden and less fiscal flexibility. Rising ratio `+1`, falling ratio `-1`, unchanged `0`, under the proposed fiscal-credibility baseline; the registry's conditional caveat remains.
- **Transformation and horizons:** Signed percentage-point-of-receipts change with annual offsets. `1–5 days: NOT_APPLICABLE`; `1–3 months: NOT_APPLICABLE`; `1–3 years: offset 3`; `3–10 years: offset 10`. Eleven rows are count-sufficient for the 10-observation comparison only at the latest row; this is minimally sufficient and fragile. If the required prior is absent or ineligible, that horizon is `INCOMPLETE`.
- **History use:** Only the 11 allowlisted L4-008 annual rows, preserving the gross-interest/receipts definition. No quarterly, monthly or synthetic values are created.

### L4-009 — Treasury Maturity Structure

- **Frozen input:** `33.32364222661862 percent_of_marketable_treasury_debt`, observed `2026-07-31`, `AVAILABLE`, `OK`; history class `A`, 24 rows. The handoff defines the share of total marketable Treasury debt maturing within one calendar year; the preserved series is monthly over the 24-month collection window.
- **Meaning and direction:** A higher near-term-maturity share indicates greater refinancing concentration and vulnerability. Rising ratio `+1`, falling ratio `-1`, unchanged `0`, under the proposed fiscal-credibility baseline. This is not a current-interest-rate signal, and the registry's conditional maturity interpretation remains.
- **Transformation and horizons:** Signed percentage-point-of-marketable-debt change with monthly positions. `1–5 days: NOT_APPLICABLE`; `1–3 months: offset 1`; `1–3 years: offset 12`; `3–10 years: INCOMPLETE` for insufficient history because 120 monthly positions are required and only 24 are preserved. The long horizon is applicable in the registry but cannot produce an MVP signal from this snapshot. No bucket reconstruction or daily interpolation is proposed.
- **History use:** Only the 24 allowlisted L4-009 monthly rows and their source-derived maturity measure. No Treasury issuance, term-premium or other variable substitutes for the missing long history.

## Status, validation and missing-history treatment

The approved input/status contract applies separately to every variable and horizon:

| Input condition | Proposed variable/horizon result |
|---|---|
| `AVAILABLE`, contract-valid current and eligible prior | Compute the signed change and direction mapping. |
| Finite current `FLAG` with its visible reason | Compute and retain a visible `FLAGGED` result; no automatic haircut. |
| Current or selected prior `STALE` | `INCOMPLETE`; do not use the stale record as a comparison point. |
| Current or selected prior `BLOCKED` | `INCOMPLETE`; value remains absent. |
| Missing, malformed, non-finite, wrong-unit or missing source reference | Reject the record or return `INCOMPLETE` with a specific reason; never coerce. |
| Duplicate variable/timestamp or ambiguous prior | Reject or return `INCOMPLETE`; never choose silently. |
| Required offset not present in the variable's own history | `INCOMPLETE` for that horizon. |
| Registry cadence cannot resolve a horizon | `NOT_APPLICABLE`, not a numeric neutral. |

No condition is converted to zero, a replacement source, synthetic history, or automatic weight redistribution. A result trace should retain variable ID, horizon, offset, current/prior timestamps and values, delta, unit, direction mapping, source references, status/quality flags and any `INCOMPLETE` or conditional note.

## Test plan outline for later implementation

1. **Reader contract:** accept the exact variable ID and unit; require finite value, valid timestamp and source reference; reject malformed, wrong-unit, duplicate timestamp, duplicate ID and unknown records.
2. **Ordering and offsets:** sort one variable's rows by timestamp and verify exact offsets for monthly, quarterly, annual and daily cases. Confirm no calendar interpolation or cross-variable lookup.
3. **Direction cases:** for every variable test rising, falling and unchanged values. Add an L4-006 case where a move from `-3` to `-5` maps to `+1`, and ratio cases where a higher burden maps to `+1`.
4. **Horizon labels:** assert the listed `NOT_APPLICABLE` horizons never attempt a lookup. Assert L4-009 3–10 years is `INCOMPLETE` with 24 rows, and L4-008's 10-observation comparison works only when all required rows are eligible.
5. **Status and data errors:** test current `FLAG`, current/prior `STALE`, current/prior `BLOCKED`, missing, malformed, non-finite, wrong-unit, duplicate and insufficient-history inputs, including the prior-`STALE` case.
6. **Traceability:** verify each numeric or incomplete result records the selected prior, offset, delta, mapping, unit and source references, and that flags remain visible to the layer and later Net Index outputs.

## Decisions requested

Please decide whether to approve, amend or reject:

- the baseline gold-direction mappings and their explicit conditional caveats;
- the frequency-aware offsets (daily `5/63/252/756`, monthly `1/12`, quarterly `12/40`, annual `3/10`);
- L4-008's minimally sufficient but fragile 10-year comparison;
- L4-009's `INCOMPLETE` 3–10-year horizon until a larger own-series history is approved.

No scoring-engine code, probability mapping, layer weighting, interaction coefficients or Net Index implementation should begin from this document alone.
