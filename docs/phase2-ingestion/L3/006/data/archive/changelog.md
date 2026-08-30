# L3-006 Changelog

## 2026-08-24 Final approval

- Grace accepted the normalized-statement-source metadata rework and final approval was
  granted.
- Final verification: compilation passed; 10 L3-006 tests and 23 combined
  FOMC/L3 tests passed. The fresh live row remained schema-valid,
  `PASS`/`AVAILABLE`, with matching statement-text, raw, manifest, and output
  source metadata.
- Final decision: `Complete`.

## 2026-08-24 Grace rework

- Replaced volatile raw-HTML annotation binding with source metadata of normalized
  official statement text. Raw HTML source metadata remains separately preserved in the
  manifest and processed record.
- Added regressions proving that different HTML wrappers with identical statement
  text accept the same annotation and changed statement text rejects it.
- BLOCKED diagnostics now retain the original parse error and record the failed
  fallback separately.
- Updated the HAWKISH supporting excerpt to quote the three rate-increase dissents
  directly.
- Fresh retrieval HTML source metadata:
  ``.
  Normalized statement source metadata remained
  ``.
- Regenerated live output: one schema-valid `PASS`/`AVAILABLE` row; raw,
  manifest, statement-text, and output source metadata matched. L3-006 tests: 10 passed;
  combined FOMC/L3 suite: 23 passed.
- Status: rework complete and ready for Grace re-review; final decision pending.

## 2026-08-24

- Added official-statement text and target-range parser with HTML/PDF provenance.
- Added strict source metadata/date/evidence matching for operator-reviewed annotations.
- Added UNCLASSIFIED, freshness, carry-forward, and BLOCKED behavior.
- Live July 29, 2026 statement produced one `PASS`/`AVAILABLE` row with a
  3.50%-3.75% target range. Aiproxy's source metadata-bound reviewed annotation classified
  it `HAWKISH`, citing elevated inflation while recording the unchanged range as
  counter-evidence; the parser did not infer this signal.
- Live HTML source metadata: ``.
  Supporting PDF source metadata: ``.
- The live row passed schema and raw/manifest source metadata validation. Eight L3-006
  tests passed; the combined FOMC/L3 suite passed 21 tests. UNCLASSIFIED,
  annotation rejection, STALE carry-forward, no-prior BLOCKED, recovery cleanup,
  and shared manual-file fallback were exercised.
- Status: implementation ready for Grace review; final decision pending.
