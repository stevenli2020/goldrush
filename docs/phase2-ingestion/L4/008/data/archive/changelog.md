# L4-008 Changelog

## 2026-08-24 — Implementation ready for Grace review

- Added minimal shared Treasury Fiscal Data transport with pagination, retries, exact raw-page preservation, source metadata, and manifests.
- Added annual September parser for Table 3 lines 130 and 360 and the gross-interest-to-receipts calculation.
- Added schema, configuration, operational documentation, fixtures, validation, and fallback/recovery tests.
- Live run: 274 filtered raw records produced 11 annual observations for fiscal years 2015–2025; all schema-valid, PASS, and AVAILABLE.
- Latest FY2025: gross interest `$1,215,613,829,754.39`; receipts `$5,234,616,386,315.43`; ratio `23.222596271472774%`.
- Live source source metadata: ``.
- Limitation: public API history for these exact rows starts in FY2015; the measure uses gross Treasury debt interest rather than net interest outlays.
- Rework: shared Treasury transport now retries real timeout and connection exceptions within the existing bounded retry policy; regression coverage added.

## Final approval — 2026-08-24

- Grace review accepted the source semantics, accounting convention, provenance, validation, fallback, blocked/recovery behavior, and retry rework.
- Final approver approved L4-008 for closure.
- Final verification: Treasury client 4 tests passed; L4-008 parser 8 tests plus 4 invalid-input subtests passed; combined suite 12 tests plus 4 subtests passed.
- Status: `Complete` for the approved Phase 2 scope.
