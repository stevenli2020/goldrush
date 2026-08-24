# L5-002 changelog

## 2026-08-21

- Added official-reserve-share parser using the existing WGC official-holdings workbook.
- Reused L0-002 workbook discovery and shared extractor infrastructure.
- Added config, schema, README, and tests.

## 2026-08-23 — Grace rework

- Extract both left and right entity panels from the PDF sheet.
- Preserve `panel` and `holdings_as_of` for every observation.
- Enforce the inclusive 0..1 reserve-share bound and exclude the separate aggregate table.
- Added two-panel and out-of-range regression coverage.
- Corrected live run 2026-08-23: 97 rows extracted (48 left-panel, 49 right-panel); every row retains `holdings_as_of`; reserve-share values are within 0..1. Combined L5/WGC tests pass.
- Final approval 2026-08-23: L5-002 marked Complete.
