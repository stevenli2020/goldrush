# Layer 4 A-class signal implementation evidence

**Status:** Implementation complete and approved  
**Scope:** L4-001, L4-002, L4-003, L4-004, L4-006, L4-007, L4-008 and L4-009 readers and signed-change signals only.

## Files created

- `l4_001_signal.py` — monthly CPI index; offsets `1` and `12` for 1–3 months and 1–3 years.
- `l4_002_signal.py` — monthly core PCE index; offsets `1` and `12` for 1–3 months and 1–3 years.
- `l4_003_signal.py` — daily 5Y breakeven; offsets `63` and `252` for 1–3 months and 1–3 years.
- `l4_004_signal.py` — daily 10Y breakeven; offsets `252` and `756` for 1–3 years and 3–10 years.
- `l4_006_signal.py` — annual fiscal balance/GDP; offsets `3` and `10`, with the approved negative-deficit direction inversion.
- `l4_007_signal.py` — quarterly gross debt/GDP; offsets `12` and `40`.
- `l4_008_signal.py` — annual interest expense/receipts; offsets `3` and `10`; the 10-row prior requires all 11 preserved rows.
- `l4_009_signal.py` — monthly debt maturing within one year/marketable debt; offsets `1`, `12` and `120`; the 120-position horizon returns `INCOMPLETE` with the preserved 24 rows.
- `tests/test_l4_group_signals.py` — focused reader, signal, status, horizon, history-limit and trace tests.

The existing `_l1_signal_common.py` helper was reused without changing its behavior. It validates the seven canonical fields, variable identity, exact unit, timestamps, finite values, source reference, allowed statuses and duplicate timestamps; sorts each own-variable series; selects the exact prior position; preserves a finite current `FLAG` as `FLAGGED`; rejects current or selected prior `STALE`/`BLOCKED` as `INCOMPLETE`; and emits trace fields for current/prior records, offset, delta, source references and flags.

## Registry verification for daily Layer 4 variables

Before implementation, the Phase 1 registry was checked directly:

- L4-003 lists only `1–3 months` and `1–3 years`. The implementation therefore uses offsets `63` and `252`; `1–5 days` and `3–10 years` return explicit `NOT_APPLICABLE`.
- L4-004 lists only `1–3 years` and `3–10 years`. The implementation therefore uses offsets `252` and `756`; `1–5 days` and `1–3 months` return explicit `NOT_APPLICABLE`.

The daily short-horizon states are based on the registry's explicit horizon lists, not on cadence alone.

## WSL test results

Focused Layer 4 suite:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l4_group_signals.py"
....................................................                     [100%]
60 passed in 1.38s
```

Existing Layer 1 and Layer 2 regression suites:

```text
wsl.exe bash -lc "cd /mnt/d/Projects/GoldRush && .venv/bin/python -m pytest -q docs/phase4-scoring/tests/test_l1*.py docs/phase4-scoring/tests/test_l2_group_signals.py"
.......................................................................  [100%]
71 passed in 1.85s
```

The focused tests cover per-variable reader validation, ascending ordering, exact offsets, all three direction outcomes, L4-006 deficit inversion, current `FLAG`, current/prior `STALE` and `BLOCKED`, missing, malformed, non-finite, wrong-unit, duplicate, insufficient history, all explicit `NOT_APPLICABLE` horizons, L4-008's 11-row boundary, L4-009's 24-row long-horizon failure and trace fields.

## Scope audit

No weights, layer scores, horizon-specific layer weights, interactions, dependencies, Net Index, probabilities, reporting, trading, optimization, hashing or replay were performed. No Phase 3 artifact was modified. Existing unrelated worktree changes were preserved.

**Approval record:** **2026-08-31** — The owner approved the Layer 4 A-class signal implementation as complete and correct. Implementation completion and owner approval are recorded separately in the decision sheet and contract.
