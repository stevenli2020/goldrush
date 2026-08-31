# Phase 4 input decisions — approved MVP

**Status:** Approved (amended)  
**Scope:** Tasks 1 and 2 are approved and complete. Subsequent variable-level approvals are recorded below; no unrecorded scoring-engine work is authorized.

## Baseline and boundaries

The frozen Phase 3 snapshot remains the sole production input baseline. It contains the 44 admitted variables and preserves the one `FLAG` record (`L3-006`, `LOW_COVERAGE`). No Phase 3 artifact is changed, rebuilt, or reclassified by this document. Phase 4 owns downstream interpretation and aggregation; Phase 5 owns the three-state probabilities.

The Phase 4 input contract is the seven-field canonical record plus the approved variable register and, only where this sheet allows it, a source-backed historical/context series. A history is evidence for a declared transformation, not an invented observation and not an automatic z-score window.

## Decisions requested

| Issue | MVP recommendation | Decision state |
|---|---|---|
| L8-001 stock/flow conflict | Resolved by the owner-approved 2026-08-31 correction: use the per-fund `Demand (tonnes)` sum and do not use the superseded `4,068.01245306` tonnes aggregate. | Approved and complete |
| Selected-component scalars | Label the component in the signal contract, for example `L3-005: selected dot-plot rate-bin value`, and retain the component key, panel/event date and published aggregate fields as context. A scalar may not be described as the full curve, panel or distribution. | Approved contract rule |
| Layer 11 has no admitted variables | Omit Layer 11 from the MVP contribution set and mark it `NOT_ADMITTED`; do not assign zero stance, zero weight or neutral evidence. A horizon requiring Layer 11 remains explicitly incomplete until a later admission decision. | Approved `NOT_ADMITTED` treatment |
| Historical inputs | Permit only the allowlist in `input-status-contract.md`. Use preserved source-backed rows with their own dates and provenance. No history may be reconstructed from current AI judgment, copied across variables, or pooled across countries/contracts without a declared rule. | Approved allowlist |
| Status propagation | Use the exact rules in `input-status-contract.md`. In particular, `FLAG` remains visible, `STALE` is not silently made current, and `BLOCKED`/missing inputs do not become zero or trigger automatic weight redistribution. | Approved contract rule |
| Existing Phase 4-labelled files | Reuse `docs/phase2-ingestion/L6/001/score.py` only as the approved L6-001 variable-local calculation. Reuse `docs/phase3-ai-evidence/L6/002/scorer.py` only as the approved L6-002 variable-local calculation. Preserve and ignore `L3-004` Phase 4 handoff files as Phase 3 outputs. Ignore `L6-002/mock_phase4_test.py` and `L6-002/live-monitor/phase4-dashboard.jsonl` for the central engine. No existing file is a substitute for the shared engine. | Recorded disposition |

## Evidence requiring care

The post-freeze L8-001 correction resolved the source-semantic exception. The approved parser now reads `Demand by month`, sums per-fund demand changes, and produces `23.46395211` tonnes for July 2026. The former `4,068.01245306` aggregate is retained only as superseded evidence and is not used for scoring.

The frozen L3-005 handoff selects a dot-plot bin (`3.375%`, one participant) while retaining a published median (`3.8%`). The Phase 4 contract must identify which component is being scored and must not call that value the complete dot-plot path.

## Approval boundary

The original approval boundary authorized drafting and reviewing the input contract only. Subsequent approval records below authorize only the named variable increments. Weights, layer aggregation, interaction coefficients, probability mapping, production reporting, trading, and changes to frozen Phase 3 evidence remain outside scope.

## Subsequent approval records

- **2026-08-31:** L1-001 method and corrected reader/signal increment accepted as complete and correct.
- **2026-08-31:** L1-002, L1-003 and L1-007 method and reader/signal increment accepted as complete and correct.
- **Resolved:** L8-001 source disposition is complete and its corrected handoff is eligible under the ordinary input/status rules.
- **2026-08-31:** L1-005 provisional negative opportunity-cost signed-change implementation accepted as complete and correct. Its direction remains explicitly conditional; regime-gating and context logic remain held for a separate decision.
- **2026-08-31:** L1-006 status-only implementation accepted as complete and correct. All four horizons remain explicitly `NOT_APPLICABLE`; no numeric signal, neutral anchor or historical series was approved.
- **2026-08-31:** L2-001, L2-002 and L2-003 signed-change implementations accepted as complete and correct. The shared helper name `_l1_signal_common.py` is accepted for the MVP; any rename is optional and deferred.
- **2026-08-31:** L4-001, L4-002, L4-003, L4-004, L4-006, L4-007, L4-008 and L4-009 reader/signed-change implementations accepted as complete and correct. L4-003 and L4-004 applicability follows the Phase 1 registry; L4-009 3–10-year output remains `INCOMPLETE` with the preserved 24-row history.
- **2026-08-31:** The approved L0-005 timestamp correction and L0-006 transformation-path correction were applied as post-freeze amendments with superseded evidence retained. The L0-001, L0-003, L0-005, L0-006 and corrected L8-001 signal methods were then implemented; implementation evidence and owner approval remain separate.
- **2026-08-31:** The owner approved the Layer 0 and corrected L8-001 increment as complete and correct. The correction and implementation evidence are closed; no weights, aggregation, interactions, Net Index or Phase 5 probability work is included.
- **2026-08-31:** The owner approved all implementable A-class time-series signals as complete and correct. This includes L5-001, L5-003, status-only L7-001, L7-003, L7-004, L7-005 and L9-001. Non-A-class `N`, `E`, `P` and `Q` groups and scoring aggregation remain separate decisions.
- **2026-08-31:** The owner approved the N-class status-only implementations for L0-009, L3-001, L3-003, L10-001 and L10-002 as complete and correct. All four horizons remain explicit `NOT_APPLICABLE`; no numeric signal, history, anchor or cross-variable substitution was approved. E, P and Q groups and scoring aggregation remain separate decisions.
- **2026-08-31:** The owner approved the final five variable methods as complete and correct: P-class status-only L0-002 and L9-004, Q-class L3-006 short-horizon scorer adapter, H-class L6-001 short-horizon scorer adapter, and Q-class status-only L6-002. This completes explicit Phase 4 variable-level treatment for all 44 admitted variables. Weights, layer aggregation, interactions, Net Index and Phase 5 probability work remain outside this approval.
