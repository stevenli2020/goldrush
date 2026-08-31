# Next L1 signal methods proposal

**Status:** Approved for L1-002, L1-003 and L1-007; L1-005 provisional implementation approved; regime-gating held  
**Scope:** Approved methods for L1-002, L1-003 and L1-007, plus the provisional L1-005 signed-change proxy. L1-005 remains explicitly conditional; no regime-gating or context logic is authorized by this document.

## Shared MVP rule

For each applicable horizon, sort that variable's own allowlisted series by timestamp and calculate:

```text
delta_h = latest_value - value_N_positions_before_latest
```

The proposed direction signal is a signed change: `+1` when the relevant real-rate or term-premium measure falls in a gold-supportive direction, `0` when unchanged, and `-1` when it rises in a gold-adverse direction. The proposed position offsets are the approved MVP conventions used by L1-001: 5, 63, 252 and 756 for 1–5 days, 1–3 months, 1–3 years and 3–10 years respectively. These are observation-count conventions, not economic completion claims.

No z-scores, percentiles, fitted normalization, pooled series or invented neutral level is proposed. Exact zero change is neutral. The percentage-point delta and both endpoint records remain in the trace.

## Variable proposals

### L1-002 — 5Y TIPS real yield

**Economic meaning and direction:** Measures shorter/intermediate real opportunity cost. A fall generally supports gold (`+1`); a rise generally weighs on gold (`-1`). This is the registry's negative direction and complements, rather than replaces, L1-001's 10Y measure.

**Applicability and transformation:** Use signed change with offset 5 for 1–5 days, 63 for 1–3 months and 252 for 1–3 years. Do not produce an L1-002 signal for 3–10 years because that horizon is not listed as applicable in the registry.

**History:** Class `A`, 5,918 source-backed rows. Use only the same-variable US series, ordered by timestamp, to select the stated prior position. No cross-maturity substitution from L1-001.

**Neutral/context:** None required; exact zero change is neutral. The current level is trace context only.

### L1-003 — Forward real rates

**Economic meaning and direction:** Measures implied real-rate conditions over future intervals. A fall in the forward real-rate measure generally reduces expected future opportunity cost and supports gold (`+1`); a rise generally weighs on gold (`-1`).

**Applicability and transformation:** Use signed change with offset 63 for 1–3 months, 252 for 1–3 years and 756 for 3–10 years. No 1–5-day signal is proposed because the registry does not list that horizon for L1-003.

**History:** Class `A`, 6,904 source-backed rows. Use only the preserved L1-003 series and its dated observations. Do not reconstruct or pool forward-rate components from another variable.

**Neutral/context:** None required; exact zero change is neutral. The forward-rate construction and source reference remain visible in the trace.

### L1-005 — Treasury term premium

**Economic meaning and direction:** Measures compensation for holding long-duration nominal Treasuries beyond expected short rates. Under the opportunity-cost channel, a rising term premium can raise competing duration returns and weigh on gold (`-1`), while a falling term premium can support gold (`+1`). The registry marks this relationship **conditional** because the model-derived premium can move with inflation, fiscal and risk regimes; the approved implementation is therefore a provisional opportunity-cost proxy and does not include regime-gating.

**Applicability and transformation:** Use the approved provisional signed change with offset 63 for 1–3 months and 252 for 1–3 years. Do not produce L1-005 signals for 1–5 days or 3–10 years because those horizons are not listed as applicable.

**History:** Class `A`, 9,146 source-backed rows. Use only the preserved term-premium series and same-variable prior positions. Do not treat it as an observed yield or substitute L1-001 history.

**Neutral/context:** None required; exact zero change is neutral. Model identity, source reference and the conditional-direction note must remain trace context.

### L1-007 — 5Y5Y forward real rate

**Economic meaning and direction:** Measures the market-implied real rate for the five-year period beginning five years forward. A fall generally reduces long-forward opportunity cost and supports gold (`+1`); a rise generally weighs on gold (`-1`).

**Applicability and transformation:** Use signed change with offset 252 for 1–3 years and 756 for 3–10 years. No shorter-horizon signal is proposed because the registry lists only these two horizons.

**History:** Class `A`, 5,918 source-backed rows. Use only the preserved L1-007 series, ordered by timestamp. Do not derive it from L1-003 or L1-001 rows.

**Neutral/context:** None required; exact zero change is neutral. The forward-period identity remains visible trace context.

## Status treatment for all four variables

- Current `AVAILABLE` with a finite value and a valid prior produces the signed-change result.
- Current `FLAG` with a finite value produces the result as visibly `FLAGGED`; no automatic haircut or clean-pass relabelling is applied. Any prior flag remains in the trace.
- Current or selected prior `STALE` returns `INCOMPLETE` with the reason retained; the stale value is not used.
- Current or selected prior `BLOCKED`, missing or malformed input returns `INCOMPLETE`; no zero, neutral substitute, shortened offset or denominator redistribution is allowed.
- Insufficient permitted history returns `INCOMPLETE`. Non-applicable horizons have no signal method and must remain explicitly `NOT_APPLICABLE`, not neutral.

## Test plan outline

For each variable's later reader and signal function, WSL tests should verify:

1. Reader validation of variable ID, canonical unit, timestamps, finite values, source reference, duplicate timestamps and allowed statuses.
2. Ascending sort and exact prior-position selection at every proposed offset for that variable.
3. Falling, unchanged and rising endpoint pairs map to `+1`, `0` and `-1` under the proposed direction.
4. Current `FLAG` remains visibly `FLAGGED`, while current and prior `STALE`, `BLOCKED`, missing and insufficient inputs return `INCOMPLETE` with no signal.
5. Non-applicable horizons return an explicit non-applicable result rather than a neutral score.
6. Trace output contains variable, horizon, current/prior timestamps and values, offset, delta, direction mapping, source references and flags.

## Approval record and remaining boundary

**2026-08-31:** The shared signed-change rule, listed horizon offsets and applicability, and negative direction for L1-002, L1-003 and L1-007 were approved. The owner accepted L1-005's provisional negative opportunity-cost signed-change implementation as complete and correct while retaining its conditional status; regime-gating and context logic remain unapproved and inactive.
