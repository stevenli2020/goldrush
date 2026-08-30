# L3-005 Changelog

## 2026-08-24 Final approval

- Grace review and final approval accepted.
- Final verification: compilation passed; 7 L3-005 tests and 23 combined
  FOMC/L3 tests passed. Live SEP output remained 26 schema-valid
  `PASS`/`AVAILABLE` rows with matching raw, manifest, and output source metadata.
- Final decision: `Complete`.

## 2026-08-24

- Added authoritative accessible-HTML dot-distribution parser with matching PDF provenance.
- Added participant-count, median, uniqueness, freshness, fallback, and schema controls.
- Live June 17, 2026 SEP produced 26 non-zero bins: 18 participants for 2026,
  18 for 2027, 17 for 2028, and 18 for the longer run. Published medians were
  3.8%, 3.6%, 3.4%, and 3.1%, respectively.
- Live HTML source metadata: ``.
  Supporting PDF source metadata: ``.
- All 26 live rows passed schema and raw/manifest source metadata validation and were
  `AVAILABLE`. Seven L3-005 tests passed; the combined FOMC/L3 suite passed
  21 tests. STALE carry-forward, no-prior BLOCKED, recovery cleanup, and shared
  manual-file fallback were exercised.
- Status: implementation ready for Grace review; final decision pending.
