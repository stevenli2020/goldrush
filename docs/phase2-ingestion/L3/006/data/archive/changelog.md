# L3-006 Changelog

## 2026-08-24 Final approval

- Grace accepted the normalized-statement-hash rework and final approval was
  granted.
- Final verification: compilation passed; 10 L3-006 tests and 23 combined
  FOMC/L3 tests passed. The fresh live row remained schema-valid,
  `PASS`/`AVAILABLE`, with matching statement-text, raw, manifest, and output
  hashes.
- Final decision: `Complete`.

## 2026-08-24 Grace rework

- Replaced volatile raw-HTML annotation binding with SHA-256 of normalized
  official statement text. Raw HTML SHA-256 remains separately preserved in the
  manifest and processed record.
- Added regressions proving that different HTML wrappers with identical statement
  text accept the same annotation and changed statement text rejects it.
- BLOCKED diagnostics now retain the original parse error and record the failed
  fallback separately.
- Updated the HAWKISH supporting excerpt to quote the three rate-increase dissents
  directly.
- Fresh retrieval HTML SHA-256:
  `d5f151657aef4f32ddf82f53b1377d1c92d59630e04f75e1acbe832264133ddb`.
  Normalized statement SHA-256 remained
  `060903fbb982f5bf20b9904482679f2a59bf9eeafd3f86b42e40f07987097591`.
- Regenerated live output: one schema-valid `PASS`/`AVAILABLE` row; raw,
  manifest, statement-text, and output hashes matched. L3-006 tests: 10 passed;
  combined FOMC/L3 suite: 23 passed.
- Status: rework complete and ready for Grace re-review; final decision pending.

## 2026-08-24

- Added official-statement text and target-range parser with HTML/PDF provenance.
- Added strict hash/date/evidence matching for operator-reviewed annotations.
- Added UNCLASSIFIED, freshness, carry-forward, and BLOCKED behavior.
- Live July 29, 2026 statement produced one `PASS`/`AVAILABLE` row with a
  3.50%-3.75% target range. Aiproxy's hash-bound reviewed annotation classified
  it `HAWKISH`, citing elevated inflation while recording the unchanged range as
  counter-evidence; the parser did not infer this signal.
- Live HTML SHA-256: `c5dcf9b53c28af4905f861347f8d846f6e59b19da8cdab8bf6c481d84efbea1c`.
  Supporting PDF SHA-256: `825cfed5e0956055d46ea3bf4d09f3939d79890fa0b3ade78bbf3957d7264522`.
- The live row passed schema and raw/manifest hash validation. Eight L3-006
  tests passed; the combined FOMC/L3 suite passed 21 tests. UNCLASSIFIED,
  annotation rejection, STALE carry-forward, no-prior BLOCKED, recovery cleanup,
  and shared manual-file fallback were exercised.
- Status: implementation ready for Grace review; final decision pending.
