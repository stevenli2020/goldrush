# L7-001 Changelog

## 2026-08-24

- Added the FRED `WALCL` parser package using the shared FRED transport.
- Locked the baseline as a Federal Reserve total-assets proxy, not a multi-central-bank composite.
- Added stale fallback, blocked-state artifact, recovery cleanup, schema, tests, and documentation.
- Verification: 7 L7-001 tests, 7 shared FRED tests, and 14 combined tests passed; Python compilation passed.
- Live run preserved 1,236 weekly observations from 2002-12-18 through 2026-08-19; values ranged from 712,809 to 8,965,487 million USD. All rows were schema-valid and PASS; latest value was 6,745,699 million USD and AVAILABLE.
- Raw, manifest, and processed SHA-256 agreed: `3a24781823eb72f13b22a2601df0e0789d423fe204cf51e6a2646b738fa7aa14`.
- Real CLI checks confirmed one-row STALE fallback, no-prior BLOCKED artifact, and artifact removal after successful recovery.
- Grace verified the manual fallback documentation and workflow-status correction. Final approval was granted and L7-001 was marked `Complete` on 2026-08-24.
