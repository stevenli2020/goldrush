# L7-005 changelog

## 2026-08-24 — initial implementation

- Confirmed FRED `SOFR` and `EFFR` semantics from New York Fed/FRED metadata.
- Implemented `(SOFR - EFFR) * 100` in basis points with date intersection only.
- Added independent raw/manifest source metadata and provenance checks, broad FLAG bounds,
  five-day freshness, carry-forward `STALE`, and machine-readable `BLOCKED`.
- Pending Grace review after tests and live evidence.

## Live evidence — 2026-08-24

- Shared FRED client fetched 2,188 SOFR and 6,819 EFFR observations.
- Joined output: 2,094 overlapping rows, 2018-04-03 through 2026-08-20.
- Latest: SOFR 3.63%, EFFR 3.63%, spread 0.0 bps; all rows finite and PASS,
  latest availability AVAILABLE.
- SOFR source metadata: ``.
- EFFR source metadata: ``.
- CLI blocked, recovery, and prior-row STALE paths are covered by tests.
- Unchanged replay returned `changed: false` for both inputs and reused the same
  raw paths/source metadata; no new raw snapshot was created.

## Rework verification — 2026-08-24

- Fallback now preserves both prior source retrieval timestamps, source metadata values,
  raw paths, and manifest paths; only `availability_status` changes to `STALE`.
- Tests expanded to 6 L7-005 tests plus 7 shared FRED tests: **13 passed**.
- Added finite outlier retention (`FLAG`) and explicit EFFR series/source metadata failure
  coverage. CLI `BLOCKED`, recovery, and provenance-preserving `STALE` fallback
  paths pass schema validation.
- Compilation passed. Live recheck remains 2,094 schema-valid rows; latest
  2026-08-20 spread 0.0 bps. Status remains pending Grace review.

## Final approval — 2026-08-24

- Grace rework accepted and final approver approved L7-005.
- Tracker status changed to **Complete**.
- No outstanding blockers; the documented limitation remains that this is a
  simple SOFR-minus-EFFR relative-rate proxy, not a complete repo stress index.
