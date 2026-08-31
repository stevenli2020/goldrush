# L4-009 Changelog

## 2026-08-24 — Implementation ready for Grace review

- Added the MSPD Table 3 marketable-debt parser and one-year refinancing concentration measure.
- Reused the shared Treasury API client, extended only with CLI `fields` support.
- Documented dated-detail coverage and exclusion of rows without maturity dates.
- Added schema, configuration, compact samples, provenance validation, deterministic replay,
  and CLI `STALE`/`BLOCKED`/recovery coverage.
- Full-history live collection preserved 153,404 raw rows across 16 pages and produced
  307 monthly observations from 2001-01-31 through 2026-07-31. All 307 rows are
  schema-valid `PASS`; the latest row is `AVAILABLE`.
- Latest 2026-07-31 values: Total Marketable `31,455,078.3191432` million USD;
  maturing within one year `10,481,977.76117396` million USD; share
  `33.32364222661862%`; classification coverage `99.988386855493%`.
- Live source source metadata: ``;
  every page source metadata, aggregate source metadata, and processed-row source metadata matched.
- Verification: compilation passed; combined Treasury-client, completed L4-008,
  and L4-009 suite passed 23 tests plus 9 subtests; replay was byte-identical;
  actual CLI fallback, blocked artifact, successful recovery, and cleanup passed.
- Source convention: bill detail rows use maturity value while `Total Marketable`
  reflects bill discount accounting, so classification coverage can slightly exceed
  100%. The source value is retained; the required numerator-over-denominator guard remains.
- Final decision: pending Grace review; not marked Complete.

## Final approval — 2026-08-24

- User approved L4-009 for closure after the implementation and verification evidence above.
- Tracker status changed from `Implementation ready for Grace review` to `Complete`.
- Synchronized the variable grouping map, Phase 2 ingestion plan, L4-009 README,
  shared Treasury README, and the stale L4-008 shared-client note.
- Final decision: `Approved 2026-08-24; Complete`.
