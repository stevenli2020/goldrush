# L5-003 changelog

## 2026-08-24 — final approval and closure

- Grace rework accepted and final approval recorded.
- Status: **Complete**. Batch 7 is closed for L5-003.

## 2026-08-24 — Grace rework implemented

- Added an explicit manifest contract, including required timezone-aware `retrieved_at`, and controlled `ValueError` failures that enter normal fallback.
- Added schema-equivalent identity, value, status, timestamp, source metadata, and provenance validation before any prior row can be carried forward.
- Regression verification: compilation passed; 13 L5-003 tests and 27 combined Batch 7 tests passed. Live parsing remained 109 schema-valid rows with unchanged latest values and output source metadata. Actual CLI fallback produced one schema-valid `STALE` row.
- Historical status at rework submission: implementation ready for Grace re-review; superseded by the final approval recorded above.

## 2026-08-24 — implementation submitted for Grace review

- Locked the official IMF COFER world U.S. dollar published-share series (`G001.AFXRA.CI_USD.SHRO_PT.Q`).
- Added a small official CSV collector, immutable raw snapshots, source metadata manifests, variable parser, schema, tests, and operational documentation.
- Added quarter-on-quarter percentage-point change, bounds checks, unusual-change flags, freshness, carry-forward `STALE`, no-prior `BLOCKED`, and blocked-to-success recovery.
- Documented the 2025 Q3 methodology revision applied back to 2000 Q1 and interpretive limitations.
- Verification: compilation passed; 9 package tests and 18 combined Batch 7 tests passed. Live collection produced 109 schema-valid observations from 1999-03-31 through 2026-03-31; latest 57.130786895752%, QoQ change +0.7135162353516051 percentage points, `PASS`/`AVAILABLE`.
- Provenance: raw 326,382-byte CSV source metadata ``; raw/manifest/processed source metadata chain verified. Actual CLI `STALE`, `BLOCKED`, recovery cleanup, and deterministic replay passed.
- Historical status at initial submission: implementation ready for Grace review; superseded by the final approval recorded above.
