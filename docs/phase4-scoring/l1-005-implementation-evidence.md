# L1-005 provisional signed-change implementation evidence

**Status:** Implementation complete and approved.  
**Scope:** L1-005 Treasury Term Premium only. The direction is a provisional conditional opportunity-cost proxy. Regime-gating and context logic remain held.

## Files created

- `l1_005_signal.py` — L1-005 reader and signed-change signal with horizons/offsets `1–3 months: 63` and `1–3 years: 252`.
- `tests/test_l1_005_signal.py` — reader, signal, status, applicability, trace and preserved-handoff tests.

The implementation reuses `_l1_signal_common.py`. It validates canonical fields, sorts the L1-005 series by timestamp, selects exact prior positions, maps falling/unchanged/rising values to `+1/0/-1`, preserves current `FLAG` as `FLAGGED`, rejects current or selected prior `STALE`/`BLOCKED` as `INCOMPLETE`, and returns explicit `NOT_APPLICABLE` for `1–5 days` and `3–10 years`. Every result includes:

```text
direction_status: provisional_conditional_opportunity_cost_proxy
```

Only the allowlisted L1-005 `A`-class series is accepted. No pooling, substitution, z-score, percentile, threshold or normalization was added.

## WSL test results

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest docs/phase4-scoring/tests/test_l1_005_signal.py docs/phase4-scoring/tests/test_l1_group_signals.py"
27 passed in 1.39s
```

The focused L1-005 tests cover reader validation, ascending sorting, exact offsets, all three directions, `FLAG`, current and prior `STALE`/`BLOCKED`, missing, malformed and insufficient inputs, non-applicable horizons, trace fields, and loading the preserved 9,146-row handoff. The real handoff remains `INCOMPLETE` under the existing stale-status rule; no stale prior or current record is overridden.

## Scope audit

No regime-gating, context logic, weights, layers, interactions, Net Index, probabilities, hashing or replay were performed. Frozen Phase 3 artifacts and unrelated worktree changes were preserved. L1-005 remains conditionally approved as a provisional opportunity-cost proxy; regime-gating remains held. **Approval record:** **2026-08-31** — the owner accepted the L1-005 provisional signed-change implementation as complete and correct.
