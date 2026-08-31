# L3-001 and L3-003 signal method proposal

**Status:** Awaiting owner decision  
**Scope:** Proposal only for the two current-scalar Layer 3 variables. L3-006 is complete and approved and is not reopened. No reader, signal, scoring-engine or pilot code is authorized.

## Shared constraint and recommendation

Both variables are history class `N` in the approved input/status contract: current scalar only, one source-backed row, unit `percent_per_annum`. A signed-change lookback is therefore unavailable. No neutral policy-rate level has been approved, so a raw scalar cannot be assigned a bullish, bearish or neutral gold signal without inventing an anchor.

**Recommendation:** use a status-only method and return explicit `NOT_APPLICABLE` for all four horizons. `NOT_APPLICABLE` is a method state, not a zero signal, neutral observation or missing-data substitute. Preserve the current scalar as trace context.

## L3-001 — Fed Funds Futures Expected Policy Rate

**Frozen input:** `3.8954166666666663`, unit `percent_per_annum`, observation date `2026-08-29`, `AVAILABLE`/`OK`. The register identifies a CME Section 10 source and one preserved row.

**Economic meaning and direction:** L3-001 measures the market-implied expected path of Federal Reserve policy. A higher expected path generally implies higher future real rates and tighter liquidity, which is negative for gold; a lower expected path generally supports gold. This is a Layer 3 expectations/repricing role. It must not be substituted for L1-006's current policy-rate component or counted as the same contribution.

**Applicable horizons:** The registry identifies L3-001 as relevant to 1–5 days, 1–3 months and 1–3 years. Under this proposal, no numeric method is approved for those horizons, and all four horizon outputs are explicitly `NOT_APPLICABLE` until a source-backed history or owner-approved level anchor exists.

**Future data requirement:** No L3-001 history is allowlisted. A future signed-change or level method would require separate approval for a consistent Fed-funds-futures series, contract/roll convention, observation dates, revision treatment and either a permitted lookback or a defensible neutral anchor. L1-006, L3-002 or another policy series cannot stand in for L3-001.

## L3-003 — Expected Terminal Policy Rate

**Frozen input:** `4.23`, unit `percent_per_annum`, observation date `2026-08-30`, `AVAILABLE`/`OK`. The register identifies a CME Section 10 source and one preserved row.

**Economic meaning and direction:** L3-003 measures the market's expected endpoint of the tightening or easing cycle and therefore expected long-run policy restrictiveness. A higher terminal-rate expectation generally weighs on gold through higher expected opportunity cost (`-1`); a lower expectation generally supports gold (`+1`). It isolates the cycle endpoint from the full policy curve and remains a Layer 3 variable, separate from L1-006's current decomposition role.

**Applicable horizons:** The registry identifies L3-003 as relevant to 1–3 months and 1–3 years. Under this proposal, those horizons and the two other horizon bands all return explicit `NOT_APPLICABLE` because no numeric transformation is approved for a single scalar.

**Future data requirement:** No L3-003 history is allowlisted. A future method would require separate source approval for a stable terminal-rate construction, dated observations, contract/curve methodology and a permitted change window or neutral anchor. L3-001, L3-002 or L1-006 history cannot be substituted or pooled.

## Status treatment for both variables

- A finite, contract-valid current `AVAILABLE` scalar is retained as context and returns `NOT_APPLICABLE` for every horizon; it does not produce a numeric signal.
- A finite current `FLAG` scalar also returns `NOT_APPLICABLE`, with the flag retained visibly in the result and trace.
- `STALE` or `BLOCKED` input returns `INCOMPLETE` with the reason retained; it is never treated as current and never converted to zero or neutral.
- Missing, malformed, non-finite or wrong-unit input returns `INCOMPLETE` with a reason. No fallback source, lookback or level anchor is used.
- L3-006's approved encoded result and `LOW_COVERAGE` handling are unchanged and are outside this proposal.

## Test plan outline

If implementation is later authorized, WSL tests should verify:

1. Each reader accepts exactly one canonical scalar with the correct ID, `percent_per_annum` unit, valid timestamp, finite value, allowed status and source reference, and rejects wrong shape, ID, unit, timestamp, non-finite value and invalid status.
2. Valid `AVAILABLE` fixtures return `NOT_APPLICABLE` for all four horizons, preserving the raw value and source as context without a numeric signal.
3. Finite `FLAG` fixtures return `NOT_APPLICABLE` while retaining the visible flag.
4. `STALE`, `BLOCKED`, missing, malformed, non-finite and wrong-unit inputs return `INCOMPLETE` with no signal.
5. Tests confirm no lookback, neutral threshold, zero substitution or L1/L3 variable substitution occurs.
6. Trace output records variable, horizon, scalar timestamp/value, unit, source reference, status, method state and flags.

## Owner decision requested

Approve status-only handling with `NOT_APPLICABLE` for all horizons for L3-001 and L3-003, or provide an approved neutral anchor and source-backed historical-data requirement for a future numeric method. No implementation should begin until that decision is recorded.
