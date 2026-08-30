# L6-001 Phase 3 closure

Status: complete and approved for Phase 4 integration on 2026-08-30.

The approved Phase 3 value is the deterministic output of the current 60
published `GPRD_ACT` values:

```text
clamp((MA5 - MA20) / max(STD60, 0.1), -1.0, 1.0)
```

The live run preserved source manifest
`gpr-20260824--20260830T084744394742Z.manifest.json`, parsed the official
Caldara-Iacoviello source through 2026-08-24, and emitted the Phase 4 record:

```json
{
  "variable_id": "L6-001",
  "observation_timestamp": "2026-08-24T00:00:00Z",
  "value": -0.21920153489517877,
  "unit_or_scale": "standard_deviation_units_clamped_-1_to_1",
  "availability_status": "AVAILABLE",
  "quality_flag": "PASS"
}
```

`data/state.json` retains the prior score and missing-day count. A stale input
uses the approved 5% decay; the third consecutive stale run emits zero. The
combined collector/parser/scorer/live-handoff tests passed: 13 passed.

Reviewer: owner

Decision: approved for Phase 4 integration.
