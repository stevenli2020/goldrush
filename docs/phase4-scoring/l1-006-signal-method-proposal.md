# L1-006 signal method proposal — expected policy rate

**Status:** Approved  
**Scope:** Approved L1-006 status-only method; implementation is recorded separately. No broader scoring-engine work is authorized by this document.

## Frozen input and economic meaning

The frozen L1-006 record is one current scalar: `3.63` with unit `percent_per_annum`, timestamp `2026-08-30`, `AVAILABLE` status and `OK` quality flag. Its approved source is the CME Section 10 handoff recorded in the variable register.

In Layer 1, L1-006 represents the expected policy-rate component embedded in current real opportunity cost: the policy-rate component against which inflation expectations and asset yields are priced. A higher expected policy rate generally raises the return available from competing assets and is negative for gold; a lower expected policy rate generally reduces that opportunity cost and is positive for gold. The registry assigns this negative direction, while reserving policy-path repricing as a separate Layer 3 role.

## Proposed MVP transformation and applicability

**Recommendation: no numeric L1-006 signal in the current MVP.** The `N` history class permits only the current scalar, and there is no approved neutral policy-rate level or source-backed history from which to define a signed change. A raw level such as `3.63%` cannot be called bullish, bearish or neutral without an owner-approved anchor; assigning one would be arbitrary.

Therefore all four horizons are explicitly `NOT_APPLICABLE` for L1-006:

- 1–5 days — `NOT_APPLICABLE`
- 1–3 months — `NOT_APPLICABLE`
- 1–3 years — `NOT_APPLICABLE`
- 3–10 years — `NOT_APPLICABLE`

`NOT_APPLICABLE` is a method state, not a zero signal, neutral observation or missing-data substitution. The current scalar remains preserved and available as trace context. This recommendation also avoids giving L1-006 an independent full policy-expectation contribution alongside L3-001/L3-002.

## Historical data requirement

No L1-006 history is allowlisted: the contract records class `N` and one source-backed row. No signed-change lookback, rolling anchor, z-score, percentile or synthetic history may be used.

If a future numeric L1-006 method is desired, it requires a separate owner-approved source decision and source-backed historical series for the same expected-policy-rate concept, with dates, revisions and methodology preserved. L1-001, L1-002, L3-001 or L3-002 history must not be substituted or pooled. That future decision must also confirm the L1 current-decomposition role remains distinct from L3 forward-path repricing.

## Status treatment

- A finite, contract-valid `AVAILABLE` scalar is retained as context and returns `NOT_APPLICABLE` for every horizon; it does not produce a numeric signal.
- A finite `FLAG` scalar also returns `NOT_APPLICABLE`, with the flag retained visibly in the result and trace.
- `STALE` or `BLOCKED` input is retained for audit but returns `INCOMPLETE`; it is never treated as current and never converted to zero or neutral.
- Missing, malformed, non-finite or wrong-unit input returns `INCOMPLETE` with a reason. No fallback source or level anchor is used.
- A later approved numeric method would need to adopt the general contract rules, including visible flags and rejection of stale prior/current inputs.

## Test plan outline

If implementation is later authorized, WSL tests should verify:

1. The reader accepts exactly one canonical L1-006 scalar with `percent_per_annum`, a valid timestamp and source reference, and rejects wrong ID, unit, shape, timestamp, non-finite value and invalid status.
2. An `AVAILABLE` fixture returns `NOT_APPLICABLE` for all four horizons with the raw value preserved only as context.
3. A finite `FLAG` fixture returns `NOT_APPLICABLE` while retaining the visible flag.
4. `STALE`, `BLOCKED`, missing, malformed and non-finite fixtures return `INCOMPLETE` with no numeric signal.
5. The test confirms no lookback, neutral threshold, zero signal or L3 variable substitution is performed.
6. Trace output records the scalar timestamp, value, unit, source reference, status, method state and flags.

## Approval record

**2026-08-31:** The owner approved deferring L1-006 numeric scoring in the MVP and marking all four horizons `NOT_APPLICABLE`. The status-only implementation is recorded separately; no neutral anchor or historical source was added.
