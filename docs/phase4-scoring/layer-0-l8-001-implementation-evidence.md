# Layer 0 and corrected L8-001 signal implementation evidence

**Status:** Implementation complete and approved; increment closed.  
**Date:** 2026-08-31

## Scope

Implemented only the approved readers and signed-change signals for L0-001, L0-003, L0-005, L0-006 and corrected L8-001. The existing shared validation helper supplies canonical-field validation, sorting, exact position offsets, status propagation and trace fields.

| Variable | Unit and cadence | Approved offsets | Direction |
|---|---|---|---|
| L0-001 | metric tonnes, annual | 1–3 years: 3; 3–10 years: 10 | rise → -1; fall → +1 |
| L0-003 | metric tonnes, observed monthly | 1–3 months: 1; 1–3 years: 12 | rise → +1; fall → -1 |
| L0-005 | metric tonnes, annual/quarterly | annual: 3/10; quarterly: 12/40 for 1–3/3–10 years | rise → +1; fall → -1 |
| L0-006 | metric tonnes, quarterly | 1–3 years: 12 | rise → -1; fall → +1 |
| L8-001 | metric tonnes, monthly | 1–3 months: 1; 1–3 years: 12 | rise → +1; fall → -1 |

Unlisted horizons return explicit `NOT_APPLICABLE`. Missing or insufficient own history, malformed/non-finite/wrong-unit input, duplicates, or current/prior `STALE`/`BLOCKED` return `INCOMPLETE`; a finite current `FLAG` remains `FLAGGED`. L0-005 selects the prior from the same annual or quarterly period type only. L0-003 records the registry-daily versus preserved-monthly cadence conflict in trace context and does not apply daily offsets. L8-001 reads the corrected per-fund `Demand (tonnes)` handoff, including the July 2026 value `23.46395211`.

## Files

- `l0_001_signal.py`, `l0_003_signal.py`, `l0_005_signal.py`, `l0_006_signal.py`, `l8_001_signal.py`
- `tests/test_layer0_l8_signals.py`
- Correction evidence: `layer-0-l8-001-correction-evidence.md`

## WSL verification

Focused suite:

```text
23 passed in 1.07s
```

Existing regression suites for L1, L2 and L4:

```text
131 passed in 2.85s
```

The tests cover preserved row counts, corrected dates and paths, reader validation, sorting, exact offsets, direction mappings, period-type matching, corrected L8-001 value/source, `FLAG`/`STALE`/`BLOCKED`, missing, malformed, non-finite, wrong-unit, duplicate, insufficient history, `NOT_APPLICABLE` and trace completeness.

**Owner approval:** 2026-08-31 — The Layer 0 and corrected L8-001 increment was approved as complete and correct.

## Explicit boundary

No variable weights, layer scores, horizon-specific layer weights, interaction/dependency adjustments, Net Index, Phase 5 probabilities, reporting, trading, automatic optimization, hashing or replay were implemented or run. No other variable or Phase 3 method was changed.
