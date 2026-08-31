# L1-002 Changelog

## 2026-08-21

- Added the standalone DFII5 parser and schema.
- Added FRED raw-response sample and parser tests.
- Live closure verification found normal FRED `.` missing-value markers; updated
  the parser to skip them without interpolation and added regression coverage.
- Targeted shared-client and L1 parser suite: 11 tests passed across L1-001 and
  L1-002, including four L1-002 parser tests.
- Parsed same-day FRED API raw response retrieved at
  `2026-08-21T01:52:36.562263+00:00`: 948 source observations, 40 missing markers
  skipped, 908 processed observations, and 908/908 validation `PASS`.
- Latest observation: `2026-08-19`, `2.07%`, status `AVAILABLE`; independently
  matched the FRED public live CSV endpoint on 2026-08-21.
- Raw source metadata verified against the manifest and processed provenance:
  ``.
- Grace closure review: acceptance criteria met; approved `Complete`.
