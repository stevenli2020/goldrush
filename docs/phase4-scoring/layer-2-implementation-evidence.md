# Layer 2 signal implementation evidence

**Status:** Implementation complete and approved; increment closed.  
**Scope:** L2-001, L2-002 and L2-003 readers and signed-change signals only.

## Files created or modified

- Modified `_l1_signal_common.py` to accept explicit falling/rising signal values and direction-mapping text. Existing L1 defaults remain unchanged.
- Created `l2_001_signal.py` for DXY (`index`), offset 5 for 1–5 days, offsets 63/252 returning `INCOMPLETE` when the 19-row history is insufficient, and `NOT_APPLICABLE` for 3–10 years.
- Created `l2_002_signal.py` for the broad trade-weighted index (`index_jan_2006_100_not_seasonally_adjusted`), with offsets 5/63/252/756 and index-base trace metadata.
- Created `l2_003_signal.py` for `cny_per_usd`, with offsets 5/63/252, `NOT_APPLICABLE` for 3–10 years, and the approved rising-USD/CNY-to-`+1` mapping.
- Created `tests/test_l2_group_signals.py` with reader, signal, status, applicability, history-limit and trace tests.

Each reader validates canonical fields, variable ID, unit, timestamps, finite values, source reference, duplicate timestamps and allowed statuses. Each signal sorts its own series, uses exact position offsets, preserves current `FLAG` as `FLAGGED`, rejects current or selected prior `STALE`/`BLOCKED` as `INCOMPLETE`, returns explicit `NOT_APPLICABLE` where approved, and preserves variable-specific trace context.

## WSL test results

Focused L2 suite:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l2_group_signals.py"
19 passed in 0.82s
```

Existing L1 regression suite:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l1*.py"
52 passed in 1.53s
```

The L2 tests cover all requested reader validation cases, ascending sort, exact offsets, all three direction mappings, current `FLAG`, current/prior `STALE` and `BLOCKED`, missing, malformed, non-finite, duplicate and insufficient inputs, `NOT_APPLICABLE` horizons, L2-001's 19-row limit, preserved handoff loading and trace metadata.

## Scope audit

No weights, layer aggregation, interactions, Net Index, probabilities, reporting, trading, optimization, hashing or replay were performed. No Phase 3 artifact was modified by this increment; existing unrelated worktree changes were preserved. The shared helper name `_l1_signal_common.py` is accepted for the MVP; renaming it later is optional and outside this increment.

**Approval record:** **2026-08-31** — The owner approved L2-001, L2-002 and L2-003 as complete and correct, with the helper-name note above recorded as non-blocking. This Layer 2 increment is closed.
