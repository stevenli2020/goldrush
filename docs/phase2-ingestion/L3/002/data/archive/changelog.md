# L3-002 Changelog

## 2026-08-24

- Final approval recorded. L3-002 is Complete.
- Grace rework: accepted both shared-collector manifest targets (`section09`
  and `section10`) while continuing to reject unrelated CME sections. Added
  target-boundary regression coverage and exact L3-002/L3-003 run commands.
- Added the Forward Policy Rate Curve parser and package using the preserved CME Section 10 ZQ settlement strip.
- Current preserved-bulletin run produced 17 schema-valid curve rows for 2026-08-20, from ZQQ26 at 3.63% through ZQZ27 at 4.00%. PDF, manifest, and output source metadata agree: ``.
- Package tests cover malformed inputs, conflicts, source metadata validation, value-based revisions, unchanged replay, stale fallback, blocked state, and recovery.
- Verification after rework: 9 L3-002 tests, 6 L3-003 tests, and 10 completed CME/L3 regression tests passed; combined suite 25 passed. The preserved replay produced 17 L3-002 rows with zero schema errors.
