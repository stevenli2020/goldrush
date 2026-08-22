# L1-001 Changelog

## 2026-08-21

- Added the standalone DFII10 parser and schema.
- Added FRED raw-response sample and parser tests.
- Live closure verification found normal FRED `.` missing-value markers; updated
  the parser to skip them without interpolation and added regression coverage.
- Targeted shared-client and L1 parser suite: 11 tests passed across L1-001 and
  L1-002, including four L1-001 parser tests.
- Parsed same-day FRED API raw response retrieved at
  `2026-08-21T01:52:35.579018+00:00`: 948 source observations, 40 missing markers
  skipped, 908 processed observations, and 908/908 validation `PASS`.
- Latest observation: `2026-08-19`, `2.35%`, status `AVAILABLE`; independently
  matched the FRED public live CSV endpoint on 2026-08-21.
- Raw SHA-256 verified against the manifest and processed provenance:
  `dbaf1dee142b5509e1bf9302fb5280656ce6c577224707f82b80f876b57e2ee8`.
- Grace closure review: acceptance criteria met; approved `Complete`.
