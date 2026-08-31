# L1-002, L1-003 and L1-007 implementation evidence

**Status:** Implementation complete and approved.  
**Scope:** Approved signed-change readers and signals for L1-002, L1-003 and L1-007. L1-005's separate provisional implementation is documented in its own evidence note.

## Files created

- `_l1_signal_common.py` — shared canonical validation, sorting, status handling, trace construction and signed-change mapping.
- `l1_002_signal.py` — L1-002 reader and horizons/offsets `1–5 days: 5`, `1–3 months: 63`, `1–3 years: 252`.
- `l1_003_signal.py` — L1-003 reader and horizons/offsets `1–3 months: 63`, `1–3 years: 252`, `3–10 years: 756`.
- `l1_007_signal.py` — L1-007 reader and horizons/offsets `1–3 years: 252`, `3–10 years: 756`.
- `tests/test_l1_group_signals.py` — reader, signal, status, applicability and trace tests for the three variables.

Each reader validates the canonical fields, variable ID, `percent` unit, timestamps, finite values, source references, duplicate timestamps and allowed statuses. Each signal sorts its own series, uses the exact configured position offset, maps falling/unchanged/rising values to `+1/0/-1`, preserves current `FLAG` as `FLAGGED`, rejects current or selected prior `STALE`/`BLOCKED` as `INCOMPLETE`, and returns `NOT_APPLICABLE` for unapproved horizons.

## WSL test results

Focused group suite:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l1_group_signals.py"
18 passed in 0.83s
```

Full repository suite:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q"
429 passed, 8 warnings, 5 subtests passed in 210.00s (0:03:29)
```

The group tests cover per-variable reader validation, ascending sort, exact offsets, all three directions, trace fields, current `FLAG`, current and prior `STALE`/`BLOCKED`, missing, malformed and insufficient inputs, and explicit `NOT_APPLICABLE` horizons.

## Scope audit

No L1-005 code or tests were changed by this three-variable increment. The full repository run necessarily included pre-existing Phase 3 tests, which were not modified. No weights, layers, interactions, Net Index, probabilities, hashing or replay were performed. Existing user worktree changes, including changes under frozen Phase 3 paths, were preserved and not modified by this increment. **Approval record:** **2026-08-31** — L1-002, L1-003 and L1-007 were accepted as complete and correct.
