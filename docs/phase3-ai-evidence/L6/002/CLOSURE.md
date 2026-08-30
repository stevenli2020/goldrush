# L6-002 Phase 3 and internal Phase 4 closure

**Decision:** Approved and production-ready 2026-08-30.

## Scope

L6-002 converts official OFAC XML list events plus a retrieved official OFAC
or Federal Register document into a deterministic sovereign-asset-freeze
evidence score. It does not infer geopolitical importance, market impact,
gold direction, or reserve ownership.

## Evidence of completion

- Exact phrase scorer implemented with 40/30/20/10 component caps.
- `REMOVE` events produce `REVERSED`, `score: null`, and no active intervention.
- Bank Markazi official OFAC document test produced `30/100` with breakdown
  `legal_action=0`, `sovereign_relevance=30`, `asset_scope=0`, and
  `legal_authority=0`.
- Controlled mock candidate test passed without invoking the collector.
- `[TEST]` email was accepted by Gmail and receipt was confirmed by the owner.
- Dashboard logging was verified with the required score, breakdown,
  evidentiary gaps, and human-review field.
- WSL validation passed: `22 tests`.

## Production controls

Phase 4 is active for internal research notifications. The seven-day human
review gate was removed by owner approval after the mock test. Production
records are logged to `live-monitor/phase4-dashboard.jsonl` and candidate
records are emailed to the configured research recipients. Public alerts,
automated trading, and other external actions remain disabled explicitly.

The local SMTP credential file is excluded from Git. The scheduled task is
`GoldRush-L6-002-SilentMonitor`; it executes the WSL pipeline with
`--activate-phase4`.

## Supporting records

- `STEP5-SCORING-SPEC.md`
- `mock_phase4_test.py`
- `MANUAL-AUDIT-QUEUE.md`
- `test-set-v2/scored-syria-2025-06-30.json`
- `live-monitor/phase4-dashboard.jsonl`
