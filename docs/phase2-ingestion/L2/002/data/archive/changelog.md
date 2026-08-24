# L2-002 Changelog

## 2026-08-23

- Confirmed FRED `DTWEXBGS` semantics: Nominal Broad U.S. Dollar Index, H.10 release, daily, Jan 2006=100, not seasonally adjusted.
- Added the variable-specific parser, schema, config, tests, and operational documentation.
- Live run completed 2026-08-23: 5,169 numeric observations parsed from 5,380 raw observations; all rows schema-valid and PASS. Latest observation: 2026-08-14 = 118.9028. Raw SHA-256: `8b247b3e50d7430a18ef6739c453db448ebe8ac820e2e9cd5929fc482ef8e650`.
- Rework added an explicit machine-readable `BLOCKED` status artifact when collection fails and no valid prior output exists; CLI behavior covered by an end-to-end test.
- Recovery cleanup added: a successful CSV write removes any prior blocked status artifact; the transition is covered by the CLI test.
- Grace final review passed: 6 variable tests and 7 shared FRED tests passed; live output and provenance were verified. Final approval recorded and status set to `Complete`.
