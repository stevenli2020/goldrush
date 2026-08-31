# Shared WGC collector changelog

## 2026-08-21

- Completed and tested `wgc_download.py`.
- Added config-driven raw routing, XLSX validation, source metadata manifests,
  unchanged-file detection, structured run logs, and protected cookie storage.
- Added and tested `wgc_extract.py`.
- Added explicit mappings for the verified L0-001 and L0-005 parser CLIs.
- Confirmed unchanged files are skipped and unmapped targets are reported as
  `SKIPPED`.
- Confirmed the downloader/extractor test suite passes (`4 passed`).

## Scope boundary

The shared layer handles WGC access, raw-file preservation, source metadata, manifests,
and parser dispatch. Variable-specific parsers remain responsible for data
extraction, validation, revisions, and output schemas.
-
## Full regression evidence — 2026-08-21

All mapped WGC targets passed the shared extractor regression: L0-001, L0-002,
L0-003, L0-005, L0-006, L5-001, L5-002, and L8-001.

Run log: `data/wgc/logs/wgc-extract-20260821T010308Z.json`.

## 2026-08-24

- Added the narrow `gold_premiums` target for `gold-premiums.xlsx` under
  `data/wgc/raw/premiums/`.
- Added manifest-path substitution to extractor dispatch and verified the L9-001
  parser runs through the shared target.
- Shared downloader/extractor tests plus L9-001 tests: 11 passed.
- Deliberate forced extractor regression completed successfully for all eight
  existing completed mappings plus `gold_premiums`; run log:
  `data/wgc/logs/wgc-extract-20260824T080421Z.json`.
