# L7-003 changelog

## 2026-08-24 — final approval and closure

- Grace rework accepted and final approval recorded.
- Status: **Complete**. Batch 7 is closed for L7-003.

## 2026-08-24 — Grace rework implemented

- Added an explicit manifest contract, including required timezone-aware `retrieved_at`, and controlled `ValueError` failures that enter normal fallback.
- Added schema-equivalent identity, value, status, timestamp, hash, and provenance validation before any prior row can be carried forward.
- Required BIS `UNIT_MULT=9` before interpreting observations as USD billions; the live source contains 108 selected rows and all have multiplier 9.
- Regression verification: compilation passed; 14 L7-003 tests and 27 combined Batch 7 tests passed. Live parsing remained 108 schema-valid rows with unchanged latest values and output hash. Actual CLI fallback produced one schema-valid `STALE` row.
- Historical status at rework submission: implementation ready for Grace re-review; superseded by the final approval recorded above.

## 2026-08-24 — implementation submitted for Grace review

- Locked official BIS series `Q.5A.P.A.M.USD.A`, the F2.2.A all-reporting-countries private non-financial credit aggregate in USD billions.
- Added a small official SDMX CSV collector, immutable raw snapshots, SHA-256 manifests, variable parser, schema, tests, and documentation.
- Added exact prior-year-quarter growth, level validation, unusual-growth flags, freshness, carry-forward `STALE`, no-prior `BLOCKED`, and blocked-to-success recovery.
- Documented coverage/classification revisions, publication lag, and USD exchange-rate sensitivity.
- Verification: compilation passed; 9 package tests and 18 combined Batch 7 tests passed. Live collection produced 108 schema-valid observations from 1999-03-31 through 2025-12-31; latest USD 163,434.02 billion, YoY growth +9.819296231854157%, `PASS`/`AVAILABLE`.
- Provenance: raw 23,958-byte CSV SHA-256 `d7be893b8874ad4002eb67bf5c439649ecd1402e6d0290ac1a966310488af65a`; raw/manifest/processed hash chain verified. Actual CLI `STALE`, `BLOCKED`, recovery cleanup, and deterministic replay passed.
- Historical status at initial submission: implementation ready for Grace review; superseded by the final approval recorded above.
