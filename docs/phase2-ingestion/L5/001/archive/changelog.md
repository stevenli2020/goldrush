# L5-001 changelog

## 2026-08-21

- Added WGC monthly official-sector purchase-change parser.
- Added config, schema, README, samples, and tests.
- Uses the shared `official_changes` WGC workbook and downloader manifest.

## 2026-08-23 — Grace rework

- Defined the aggregation population: exclude rows marked `*` (including gross `Turkey*`) and retain adjusted `Turkey`.
- Added regression coverage for the Turkey alternative-series rule and repository-root test imports.
- Corrected live run 2026-08-23: 294 monthly rows using the canonical population rule; gross `Turkey*` excluded and adjusted `Turkey` retained. Combined L5/WGC tests pass.
- Final approval 2026-08-23: L5-001 marked Complete.
