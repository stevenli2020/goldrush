# L8-001 post-freeze correction evidence

**Correction date:** 2026-08-31  
**Scope:** L8-001 only.
**Owner approval:** Approved 2026-08-31.

## Finding and correction

The superseded frozen handoff reported **4,068.01245306 metric tonnes** for
2026-07-31. Controlled inspection showed that the original parser selected the
aggregate `Tonnes` column from the workbook's `Fund flows by month` sheet. That
column is holdings-like and is not monthly ETF demand.

The corrected parser reads `Demand by month`, sums the numeric per-fund
`Demand (tonnes)` values, and preserves the month-end date and source
provenance. The corrected 2026-07-31 value is **23.46395211 metric tonnes**.
It reconciles to the per-fund total and to the June-to-July holdings change.

The superseded handoff remains at
`data/l8_001_phase3_handoff.superseded-20260831.json`.

## Files changed

- `docs/phase2-ingestion/L8/001/parse_etf_flows.py`
- `docs/phase2-ingestion/L8/001/tests/test_parse_etf_flows.py`
- `docs/phase2-ingestion/L8/001/README.md`
- `docs/phase2-ingestion/L8/001/processed/L8_001_observations.csv`
- `docs/phase3-ai-evidence/L8/001/README.md`
- `docs/phase3-ai-evidence/L8/001/data/l8_001_phase3_handoff.json`
- `docs/phase3-ai-evidence/closure/canonical_dataset.jsonl` (L8-001 row only)
- `docs/phase3-ai-evidence/closure/variable_register.json` (L8-001 source reference only)
- `docs/phase3-ai-evidence/PHASE3-TRACKER.md`
- `docs/phase3-ai-evidence/closure/closure_record.md`
- `docs/phase3-ai-evidence/closure/integration_check_report.md`

The superseded handoff was preserved as an additional audit file. No other
canonical variable was changed.

## Validation

WSL command:

```text
.venv/bin/python -m pytest -q docs/phase2-ingestion/L8/001/tests/test_parse_etf_flows.py docs/phase3-ai-evidence/L8/001/tests/test_build_phase3_handoff.py
```

Result: **3 passed in 9.74s**. The correction and its evidence were approved by
the owner on 2026-08-31.

Read-only consistency checks confirmed 44 canonical records, one L8-001 row,
281 corrected handoff records, canonical and handoff latest value
`23.46395211`, unit `metric_tonnes`, and superseded latest value
`4068.01245306`. No canonical hash or integration replay was run.
