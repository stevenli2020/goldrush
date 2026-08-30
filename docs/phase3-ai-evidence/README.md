# Phase 3 — Live Data Integration and Deterministic Outputs

This directory contains Phase 3 variable packages. They turn preserved source
evidence into small, deterministic, auditable outputs for Phase 4. Phase 3
does not implement weights, layer scores, a Net Index, backtesting, or
investment decisions.

The six original Phase 3 source/integrity problems are closed and documented
in [PHASE3-ORIGINAL-SIX-CLOSURE.md](PHASE3-ORIGINAL-SIX-CLOSURE.md). This is a
milestone; it does not close the remaining Phase 3 variables.

## Implemented scope

- `L3/006/` contains the packaged live L3-006 scoring workflow, inputs, results,
  and documentation. It consumes source text produced by the Phase 2 parser;
  the former manual annotation is not used.
- L3/004 retains Phase 2's full deterministic policy-outcome distribution and
  produces compact per-meeting probability and expected-change handoff records.
The former Phase 2 `HAWKISH` annotation and the rejected Python evidence-record
prototype are removed from the active Phase 3 package. The live L3-006 scorer
keeps source evidence, baseline extraction, jury assessments, and calculations
separate.

## Operations

Run from the repository root in the project WSL environment:

```bash
source .venv/bin/activate
pytest -q docs/phase3-ai-evidence/L3/006
```

The live L3-006 workflow is documented in [L3/006/README.md](L3/006/README.md).

## Current limitations and next slice

The L3-006 live workflow calls the configured AI scorer and retains raw
responses, evidence, diagnostics, and run status for review.

The next recommended admitted qualitative variable is **L6-001 — Active
Conflict and Escalation Signal**. Its Phase 2 GPR observations are a news-based
intensity proxy, while the registry requires structured assessment of actual
conflict/escalation, safe-haven transmission, offsets, source agreement, and
counter-evidence. L6-002 is complete and its internal Phase 4 notification path
is active. Deterministic admitted variables should continue to bypass Phase 3
qualitative assessment.
