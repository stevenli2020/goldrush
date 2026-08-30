# L2-001 Changelog

## 2026-08-24

- Added OpenBB/yfinance `DX-Y.NYB` collector and separate OHLC parser.
- Added raw snapshot/manifests, schema, fallback behavior, revision handling, tests, and documentation.
- Live 2026-08-24 run: 161 daily rows collected for 2026-01-02 through 2026-08-24; latest `dxy_close=98.83999633789062`, `AVAILABLE`, `PASS`; raw source metadata ``.
- Grace rework: prior-data fallback now returns `STALE` end-to-end and clears stale `BLOCKED` artifacts; non-finite values are rejected, incomplete current-day bars are excluded, and all duplicate OHLC conflicts are detected. Sample provenance is explicitly fixture-only.
- Regenerated processed output after final current-day exclusion: 160 rows remain through the latest completed market day, 2026-08-21; the evolving 2026-08-24 bar is excluded. Typed schema validation passed for all 160 rows.
- Grace approval: L2-001 approved and Complete. No further implementation changes are required; ongoing runs should preserve raw snapshots, manifests, and the finalized-current-day exclusion.
