# L4-007 Changelog

## 2026-08-24

- Confirmed FRED `GFDEGDQ188S`: U.S. federal total public debt as percent of GDP, quarterly, seasonally adjusted.
- Added the variable parser, schema, configuration, tests, samples, and operational documentation.
- Defined the observation date as FRED's first day of quarter and freshness as 190 days after the latest quarter end.
- Compilation passed. Tests: 15 L4-007 tests, 7 shared macro FRED tests, and 22 combined tests passed.
- Live run: 241 quarterly observations covering 1966-01-01 through 2026-01-01; all rows schema-valid, PASS, and AVAILABLE. Latest value: 122.59387% of GDP.
- Live raw SHA-256 `fac9b16416d1cd360f762b78c8c0406cbe3c60093203599dae33dec0408556fb` matched the manifest and every processed row.
- Actual CLI fallback produced one schema-valid 2026-Q1 STALE row; no-prior failure produced BLOCKED; successful recovery wrote 241 rows and removed the obsolete blocked artifact.
- Limitation: the series measures U.S. federal total public debt, not net debt, general-government debt, or a cross-country comparable measure. FRED may revise debt, GDP, and the ratio.
- Grace review and final approval received 2026-08-24. L4-007 marked Complete.
