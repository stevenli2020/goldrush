# Final variable methods — implementation evidence

**Status:** Approved and closed on 2026-08-31.  
**Scope:** L0-002, L9-004, L3-006, L6-001 and L6-002 only.

## Implemented methods

| Variable | Module | Approved treatment implemented |
|---|---|---|
| L0-002 | `l0_002_status.py` | P-class country-panel status-only method; valid canonical input is `NOT_APPLICABLE` for all horizons, with panel context retained and no selection or aggregation. |
| L9-004 | `l9_004_status.py` | P-class component-panel status-only method; valid canonical input is `NOT_APPLICABLE` for all horizons, with component context retained and no selection or pooling. |
| L3-006 | `l3_006_signal.py` | Existing-scorer adapter: `<50 -> +1`, `50 -> 0`, `>50 -> -1` for 1–5 days and 1–3 months; long horizons are `NOT_APPLICABLE`; `FLAG` and `LOW_COVERAGE` remain visible. |
| L6-001 | `l6_001_signal.py` | Existing-handoff adapter: `>0 -> +1`, `0 -> 0`, `<0 -> -1` for 1–5 days and 1–3 months; long horizons are `NOT_APPLICABLE`; the upstream scorer is not rerun or changed. |
| L6-002 | `l6_002_status.py` | Q-class event status-only method; valid canonical event score is `NOT_APPLICABLE` for all horizons, with event context retained and no gold-direction mapping. |

All five validate canonical identity, unit, timestamp, finite value, status and source reference. `STALE`, `BLOCKED`, missing, malformed, non-finite, wrong-unit and invalid inputs return `INCOMPLETE` without a neutral substitute. L3-006 and L6-001 include source score, mapping direction, source reference, status, flags and reason in their trace results.

## Tests

Focused test file added: `tests/test_final_variable_methods.py`.

It covers status-only non-numeric treatment, invalid and ineligible inputs, preserved L0-002 and L9-004 panel loading without aggregation or component selection, L3-006 midpoint mapping and `LOW_COVERAGE` retention, L6-001 positive/zero/negative mapping and stale handling, L6-002 reversed-event context retention, and real canonical/preserved-input execution.

WSL command:

```bash
.venv/bin/python -m pytest -q docs/phase4-scoring/tests
```

Result: **257 passed in 5.20s**.

## Boundaries preserved

No weights, layer scores, interactions, dependency adjustments, Net Index, probability mapping, hashing, replay, reporting, trading or optimization were implemented. Existing L3-006, L6-001 and L6-002 scorer internals were not modified. Frozen Phase 3 artifacts and unrelated worktree changes were preserved.

## Owner approval

**2026-08-31:** The owner approved the final five variable methods as complete and correct. This closes the last five admitted-variable methods and completes Phase 4 variable-level treatment for all 44 admitted variables. Implementation closure does not authorize weights, layer scores, interactions, Net Index or Phase 5 probability work.
