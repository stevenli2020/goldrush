# L1-006 reader and status-only method — implementation evidence

**Status:** Implementation complete and approved.  
**Scope:** L1-006 reader and approved status-only method only.

## Delivered

- `l1_006_status.py` accepts exactly one canonical L1-006 scalar, either as one JSON object or a one-item JSON array.
- The reader validates the canonical fields, L1-006 identity, `percent_per_annum` unit, timestamp, finite value, valid availability status and source reference.
- `status_only_method` returns `NOT_APPLICABLE` for all four horizons for valid `AVAILABLE` and finite `FLAG` inputs, preserving the raw scalar as trace context and retaining visible flags.
- `STALE`, `BLOCKED`, missing, malformed, non-finite, wrong-unit and wrong-shape inputs return `INCOMPLETE` with a reason and no numeric signal.

## WSL test result

Command:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l1_006_status.py"
```

Result:

```text
...............                                                          [100%]
15 passed in 0.60s
```

The tests cover exact one-record shape, canonical-field validation, all four horizons, raw context preservation, visible `FLAG` propagation, `STALE` and `BLOCKED` handling, malformed and non-finite input, wrong units, required trace fields, and reading the frozen canonical L1-006 record.

## Scope audit

No other variable was modified. No weights, layers, interactions, Net Index, probabilities, hashing or replay were added or run. Existing frozen Phase 3 and unrelated worktree changes were preserved. **Approval record:** **2026-08-31** — the owner accepted the L1-006 status-only implementation as complete and correct.
