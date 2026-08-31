# Layer 0 and L8-001 approved correction evidence

**Status:** The two approved upstream corrections are complete and approved; increment closed.  
**Date:** 2026-08-31

## L0-005 timestamp correction

- Original handoff: `docs/phase3-ai-evidence/L0/005/data/l0_005_phase3_handoff.superseded-20260831.json`.
- Corrected handoff: `docs/phase3-ai-evidence/L0/005/data/l0_005_phase3_handoff.json`.
- The handoff builder now uses the calendar month end for quarterly timestamps, preventing regeneration of the malformed `09-31` dates.
- Both files contain 82 records. Exactly 16 invalid Q3 timestamps changed from `YYYY-09-31` to `YYYY-09-30`.
- JSON comparison confirmed that values, units, period labels/types, statuses, quality flags and source references were unchanged for every record; no other timestamp changed.
- The corrected timestamps are valid calendar dates. The current canonical L0-005 value remains `307.08301057 metric_tonnes` for 2026-06-30.

## L0-006 path correction

- Corrected source and transformation output: `docs/phase2-ingestion/L0/006/processed/l0_006_gold_recycling_flow.json`.
- The variable register and L0-006 canonical `source_reference` now use that existing path.
- The closure builder now resolves the same corrected path.
- The source file remains unchanged and contains 66 quarterly observations. No copy, rename, alternate source or value substitution was used.

## Verification and scope

The focused Phase 4 correction/reader suite validates the 82-row corrected handoff, 16-row supersession comparison, valid dates, register path and canonical path. No hashing, replay, scoring aggregation, weights, layer scores, interactions, Net Index, probabilities, reporting, trading or optimization was run. Frozen Phase 3 evidence is retained, with only these two approved post-freeze corrections applied.

**Owner approval:** 2026-08-31 — The L0-005 timestamp correction and L0-006 path correction were approved as complete and correct.
