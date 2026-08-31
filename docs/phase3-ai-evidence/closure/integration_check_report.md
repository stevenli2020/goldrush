# Phase 3 integration check

Checked at: `2026-08-30T15:08:55.155126Z`

| Check | Result |
|---|---|
| 44 records and exact variable IDs | PASS |
| Seven-field schema and types | PASS |
| Timestamp, cadence, and stale detection | PASS |
| Status and quality-flag rules | PASS |
| Units, traceable references, and direct transformation comparison | PASS |
| No accidental cross-variable copies | PASS |

Records checked: **44**.

All integration checks passed. Every canonical value was selected directly from a recorded transformation output; no substitute values were created.

## Post-freeze amendment — L8-001 (2026-08-31)

The L8-001 transformation was corrected after controlled workbook inspection.
The parser now uses the per-fund `Demand (tonnes)` values from `Demand by
month`, rather than the aggregate `Tonnes` column from `Fund flows by month`.
The corrected July 2026 canonical value is 23.46395211 metric tonnes. This is
an L8-001-only amendment, approved by the owner on 2026-08-31; the original frozen handoff is retained separately
as superseded evidence and the original integration result remains historical.
