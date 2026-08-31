# Layers 5, 7 and 9 A-class signal implementation evidence

**Status:** Implementation complete and approved; increment closed.  
**Date:** 2026-08-31

## Scope and files

Implemented only the seven methods authorized by the active Phase 4 increment:

- `l5_001_signal.py` — monthly official-sector purchase flow, offsets 1/12, rising → `+1`.
- `l5_003_signal.py` — quarterly pre-derived QoQ USD-share change, offsets 12/40, falling → `+1`.
- `l7_001_status.py` — weekly balance-sheet liquidity, status-only `NOT_APPLICABLE` for all four horizons; raw canonical input remains in trace context.
- `l7_003_signal.py` — quarterly pre-derived YoY credit growth, offsets 12/40, falling → `+1`.
- `l7_004_signal.py` — daily credit-spread change, offsets 5/63/252, widening → `+1`.
- `l7_005_signal.py` — daily SOFR-minus-EFFR spread change, offsets 5/63/252, widening → `+1`.
- `l9_001_signal.py` — daily SGE premium/discount change, offsets 5/63/252, rising premium → `+1`.
- `tests/test_l5_l7_l9_signals.py` — focused reader, signal, status and trace tests.

All six numeric methods use the existing shared validation and signed-change helper. They validate canonical fields, exact variable ID and unit, timestamps, finite values, source references, duplicate timestamps and allowed statuses; sort the variable's own history; use exact prior positions; and preserve trace fields. Current `FLAG` remains visible as `FLAGGED`; current or selected prior `STALE`/`BLOCKED`, missing, malformed, non-finite, wrong-unit, duplicate and insufficient inputs return `INCOMPLETE`. No fallback or cross-variable substitution is used.

L5-003 and L7-003 retain their pre-derived QoQ/YoY semantics and do not recompute levels. Their preserved handoffs contain null early values, which are rejected as non-finite rather than coerced. L7-001 has no weekly offset rule and therefore never computes a numeric signal. L9-001 is traced and interpreted as the registry/handoff SGE premium/discount, not a spot-price series.

## WSL verification

Focused suite:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l5_l7_l9_signals.py"
27 passed in 1.22s
```

Existing L1/L2/L4 and Layer 0/L8 regression suites:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l1*.py docs/phase4-scoring/tests/test_l2_group_signals.py docs/phase4-scoring/tests/test_l4_group_signals.py docs/phase4-scoring/tests/test_layer0_l8_signals.py"
154 passed in 3.93s
```

The focused tests cover reader validation, ascending sort, exact offsets, all direction mappings, pre-derived measures, stress mappings, L7-001 status-only behavior, `FLAG`, `STALE`, `BLOCKED`, missing, malformed, non-finite, wrong-unit, duplicate, insufficient history, `NOT_APPLICABLE`, stale-prior handling and trace completeness.

The complete `docs/phase4-scoring/tests` directory also passes: **181 passed in 3.49s**.

**Owner approval:** 2026-08-31 — All implementable A-class time-series signals were approved as complete and correct. This increment's seven Layer 5/7/9 methods are closed.

## Explicit boundary and preservation

No weights, layer scores, horizon-specific layer weights, interactions, dependency adjustments, Net Index, Phase 5 probabilities, reporting, trading, automatic optimization, hashing or replay were implemented or run. No Phase 3 artifact was modified, and unrelated worktree changes were preserved. The remaining Phase 4 work is limited to separately approved non-A-class groups and aggregation decisions.
