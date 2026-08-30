# L2-003 Changelog

## 2026-08-24

- Grace's rework review passed: compilation succeeded; L2-003 tests (6) and shared FRED regression tests (7) passed, 13 tests total. The preserved live output contains 6,675 schema-valid `PASS` rows; the latest observation remains 2026-08-14 at 6.7412 CNY/USD, and the recorded source metadata matches the raw file, manifest, and processed rows.
- Final approver accepted Grace's recommendation. L2-003 is `Complete` as of 2026-08-24.
- Simplified the documented manual fallback command to invoke `--prior` directly.

## 2026-08-23

- Verified official FRED `DEXCHUS` metadata: “Chinese Yuan Renminbi to U.S. Dollar Spot Exchange Rate”; CNY per USD; daily; not seasonally adjusted; Board of Governors H.10 Foreign Exchange Rates release. It is the H.10 noon New York buying rate for cable transfers, distinct from offshore CNH and the PBoC central-parity fixing.
- Added parser, config, schema, README, samples, and tests using the shared FRED transport and provenance conventions.
- Live run completed 2026-08-23 using shared FRED client: 6,945 raw observations, 6,675 numeric observations parsed. Latest observation: 2026-08-14 = 6.7412 CNY/USD. Raw source metadata: ``. All 6,675 rows are schema-valid; validation is 6,675 `PASS`, with 2 `AVAILABLE` and 6,673 `STALE` under the ten-day freshness rule.
- Verification: Python compilation passed; L2-003 tests (6) and shared FRED regression tests (7) passed, 13 tests total. Schema validation, blocked fallback, successful recovery cleanup, and CLI prior fallback are covered.
- Rework requested by Grace: documented H.10’s normal Monday publication of the preceding business week and the rationale for the ten-day freshness threshold; added an end-to-end CLI `--prior` fallback test that validates a canonical `STALE` row against the schema.
