# L1-001 signal method proposal — 10Y TIPS real yield

**Status:** Approved  
**Scope:** Approved L1-001 method; implementation and correction are complete. No broader scoring-engine work is authorized by this document.

## Variable meaning and direction

L1-001 measures the real yield available from a high-quality competing asset. A higher real yield generally raises the opportunity cost of holding non-yielding gold; a lower real yield generally reduces that cost. The registry therefore assigns L1-001 a negative gold direction.

| Horizon | Economic meaning | Proposed observation comparison |
|---|---|---|
| 1–5 days | Immediate repricing of long-duration real opportunity cost | Latest eligible yield minus the value five prior business-day observations earlier |
| 1–3 months | Short cyclical change in the real-rate environment | Latest eligible yield minus the value 63 prior business-day observations earlier |
| 1–3 years | Medium-cycle change in expected real return from competing assets | Latest eligible yield minus the value 252 prior business-day observations earlier |
| 3–10 years | Secular direction of long-duration real opportunity cost | Latest eligible yield minus the value 756 prior business-day observations earlier |

The lookbacks are observation-count conventions for the four horizon bands, not claims that the economic effect completes on those exact dates. They must remain explicit configuration in any later implementation.

## MVP-simple transformation

For each horizon, let `delta_h = latest_yield_percent - prior_yield_percent` using the specified prior observation. The proposed gold-direction signal is:

```text
delta_h < 0  -> +1  (bullish gold: real yield fell)
delta_h = 0  ->  0  (neutral: no change)
delta_h > 0  -> -1  (bearish gold: real yield rose)
```

This is a signed change signal. It uses no z-score, percentile, fitted scale, arbitrary threshold, or invented neutral yield level. The magnitude of the percentage-point change is retained in the trace for review, while the proposed signal is the three-value direction above. A later continuous transformation would require a separate decision.

## Historical data and eligibility

Only the allowlisted 5,918 L1-001 rows may be used. They must be joined by `variable_id`, ordered by observation timestamp, and kept as one US 10Y TIPS series. No country pooling, synthetic observations, copied history or invented dates are permitted.

The current input must be the canonical L1-001 record and contract-valid. The comparison value must be a finite, dated row from the same allowlisted series at the stated observation offset. If either endpoint is missing, malformed, non-finite or otherwise fails the approved input contract, the horizon result is `INCOMPLETE`; it is not replaced with zero or a neutral value. Historical `STALE` labels remain visible provenance and must not be treated as a current eligible observation.

## Neutral anchor or context

None required. Exact zero change is the neutral case. The current yield level may be displayed as trace context but does not receive a separately invented bullish or bearish threshold.

## Reader and signal test plan

After approval, WSL tests should cover:

1. Reader accepts the canonical L1-001 unit (`percent`), source reference and timestamps, and rejects an unknown ID, duplicate row, bad unit, malformed timestamp or non-finite value.
2. A small fixture with at least 756 ordered observations returns `+1`, `0` and `-1` for falling, unchanged and rising endpoint pairs at all four offsets.
3. Unsorted, missing or insufficient history returns `INCOMPLETE` with a reason; it never returns zero or silently shortens the lookback.
4. The trace records horizon, current timestamp/value, prior timestamp/value, percentage-point delta, direction mapping and source references.
5. The test confirms the frozen canonical and Phase 3 directories are not modified by the reader or signal implementation.

**Approval record:** **2026-08-31** — The signed-change method and four explicit observation offsets were approved. The corresponding reader/signal implementation is recorded separately in the implementation evidence.
