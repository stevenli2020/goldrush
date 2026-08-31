# L1-001 reader and signal pilot — implementation evidence

**Status:** Implementation complete and approved.  
**Scope:** L1-001 reader and signed-change signal only.

## Delivered

- `l1_001_signal.py` validates the seven canonical fields, `L1-001` identity, `percent` unit, timestamps, finite values, statuses and source references, then sorts records ascending by timestamp.
- `OFFSETS` explicitly defines 5, 63, 252 and 756 prior positions for the four approved horizons.
- `signed_change_signal` computes `current - prior`, maps falling/unchanged/rising yield to `+1/0/-1` gold direction, and emits current/prior timestamps and values, percentage-point delta, offset, source references, direction mapping and flags.
- Current `FLAG` remains `FLAGGED`; `STALE`, `BLOCKED`, missing and insufficient inputs return `INCOMPLETE` without a neutral substitute.
- A selected prior record with status `STALE` or `BLOCKED` is rejected as `INCOMPLETE` and is never used as a comparison point.

## WSL test result

Command:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l1_001_signal.py"
```

Result:

```text
..........                                                               [100%]
10 passed in 0.45s
```

The tests cover sorting and invalid canonical inputs (wrong ID, unit, timestamp and non-finite value, plus duplicate timestamps), every configured offset, bullish/neutral/bearish mapping, visible `FLAG` propagation, `STALE` prior rejection, insufficient/stale current inputs, and loading the preserved 5,918-row L1-001 handoff.

## Scope audit

No scoring-engine aggregation, weights, layers, interactions, Net Index, probabilities, reporting, trading, hashing or replay was added or run. Frozen Phase 3 directories and unrelated worktree changes were preserved. **Approval record:** **2026-08-31** — L1-001 was accepted as complete and correct.
