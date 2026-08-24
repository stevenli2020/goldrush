# L4-006 Changelog

## 2026-08-24

- Added the FYFSGDA188S parser, schema, configuration, tests, and documentation.
- Preserved the FRED sign convention: negative means deficit; positive means surplus.
- Defined annual freshness as 550 days after the latest fiscal-year end.
- Tests: 11 L4-006 tests and 7 shared macro tests passed under importlib mode.
- Live run: 97 raw and numeric observations covering 1929–2025; all schema-valid, PASS, and AVAILABLE. Latest 2025 balance was -5.76906% of GDP (deficit). Raw SHA-256: `fd3f43dc1cdf3694da26d9e879f2573f9e65e71598b8dcf6035b224e0a5771c8`.
- Unchanged replay returned `changed: false`; prior-output fallback returned one schema-valid 2025 STALE row.
- Added an end-to-end CLI regression for failed live input with a valid prior output; it emits exactly one STALE row and no BLOCKED artifact.
- Final verification: 12 L4-006 tests plus 7 shared macro tests passed; compilation passed.
- Grace review requirements satisfied and final approver approval received 2026-08-24. L4-006 marked Complete.
