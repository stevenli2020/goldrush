# L0-003 — Gold ETF Holdings Changelog

## 2026-08-19 — Implementation review

- Confirmed WGC workbook source: `ETF_Flows_2026-08-04_1202.xlsx`.
- Implemented XLSX parsing in `parse_etf_holding.py`.
- Added provenance fields, source metadata, validation statuses, revision metadata, and stale fallback support.
- Corrected configuration and documentation paths to the L0-003 source and output locations.
- Aligned `schema.json` with the generated CSV, including `aum_usd_bn` as an optional nullable field.
- Live run produced 281 records: 237 `PASS`, 44 `FLAG`, 0 `FAIL`.
- Test suite passed: 3 tests.

## Known limitations

- The current workbook provides no populated AUM values; `aum_usd_bn` remains nullable.
- `FLAG` records identify holdings changes above the configured threshold and require review before interpretation.
- The fallback is carry-forward of the latest valid observation with `STALE` availability status.
- The source is manually downloaded; publication and download dates are supplied by the operator.

## Closure

Grace review was completed and final approval was recorded on 2026-08-19.
L0-003 is closed as `Complete`.

## Ingest evidence

| Run timestamp | Source workbook | Records | PASS | FLAG | FAIL | Output |
|---|---|---:|---:|---:|---:|---|
| 2026-08-19T09:38:13Z | `ETF_Flows_2026-08-04_1202.xlsx` | 281 | 237 | 44 | 0 | `processed/L0_003_observations.csv` |
