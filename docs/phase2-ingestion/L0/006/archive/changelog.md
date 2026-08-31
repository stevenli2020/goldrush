# L0-006 — Gold Recycling Flow Changelog

## 2026-08-19 — Closed

- Confirmed WGC Gold Demand Trends workbook source and `Gold Balance` / `Recycled Gold` mapping.
- Implemented the canonical collector at `scripts/parse_gold_recycling.py`.
- Added quarterly normalization, source metadata provenance, revision handling, schema validation, and stale seed fallback.
- Full test suite passed: 8/8.
- Live WGC workbook run passed: 66 quarterly observations, `AVAILABLE`.
- Live output validated successfully against `schema.json`.
- Final decision: `Complete`.
