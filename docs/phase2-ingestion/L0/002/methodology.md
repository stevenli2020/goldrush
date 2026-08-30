# Methodology Archive & Changelog: L0-002

## Version History

### v1.2.0 (2026-08-29)
* **Canonical source decision:** WGC official-holdings workbook is the approved Phase 3 source and is downloaded through the shared WGC collector.
* **Legacy path:** IMF/OpenBB collector and mock mode are retained only as historical evidence and are not part of the approved production route.

### v1.1.0 (2026-08-19)
* **Architecture Update:** Migrated ingestion pipeline from FRED API to **IMF International Financial Statistics (IFS)** via OpenBB SDK (`openbb-imf`).
* **Entity Correction:** Updated Euro Area identifier from `EMU`/`ECB` to the official IMF IFS institutional code `EZB`.
* **Unit Scale Fix:** Corrected multiplier from `31.1034768` (millions of oz) to `3.11034768e-5` (exact oz to metric tonnes conversion) following initial magnitude verification tests against official U.S. and Swiss benchmarks.

### v1.0.0 (2025-12-15)
* **Initial Draft:** Proposed FRED series-based ingestion (deprecated due to upstream series unavailability).

## Operational Conventions

* WGC official-holdings workbook is the canonical source; the workbook is
  WGC-compiled and based primarily on IMF IFS statistics.
* Entity observations are monthly end-of-period quantities in metric tonnes.
* Observations older than 150 days are marked `STALE`; existing values may be
  carried forward for up to three periods.
* The aggregate is a derived six-entity sum and uses the execution month
  (`YYYY-MM`) rather than an independently published observation date.
* Live payloads are preserved under `data/raw/`, run evidence under
  `data/archive/`, and processed outputs under `data/processed/`.

## Closure Record

Grace reviewed the implementation and verified the three offline tests, live
evidence bundle, metric-tonne conversion, stale EA handling, raw payload
preservation, and documented fallback behavior. Final approval was granted on
2026-08-19 and L0-002 was marked `Complete` in the Phase 2 tracker.
