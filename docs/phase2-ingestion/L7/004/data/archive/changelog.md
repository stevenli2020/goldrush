# L7-004 Changelog

## 2026-08-24

- Confirmed FRED `BAMLH0A0HYM2`: ICE BofA US High Yield Index Option-Adjusted Spread, percent, not seasonally adjusted, daily close.
- Added the variable parser, schema, config, tests, samples, and fallback/recovery behavior using shared FRED transport.
- Documented the U.S. high-yield scope, ICE methodology limitation, and FRED three-year public-history limit beginning April 2026.
- Live run: 795 raw observations, 787 numeric rows from 2023-08-22 through 2026-08-20; all rows schema-valid and PASS. Latest value 2.75 percentage points, AVAILABLE. Raw/manifest/output source metadata: ``.
- Verification: parser compilation passed; 7 L7-004 tests, 7 shared FRED tests, and 14 combined tests passed. CLI fallback, BLOCKED, and recovery cleanup paths are covered end to end.
- Grace review and final approval completed 2026-08-24. L7-004 status changed to `Complete`; no implementation blockers remain.
