# L3-004 — Probability Distribution of Future Policy Outcomes

L3-004 is deterministic. Phase 2 calculates the complete distribution from
preserved CME 30-Day Fed Funds futures settlements, FRED EFFR/target-range
observations, and the FOMC meeting schedule. It is a calculated CME-method
probability, not an official CME FedWatch output.

Phase 3 retains that complete distribution as evidence and creates four compact
handoff measures for each of the next two meetings:

- `probability_easing_0_to_1`
- `probability_hold_0_to_1`
- `probability_tightening_0_to_1`
- `expected_target_change_bps`

`meeting_date` is retained because this variable is a forward distribution:
without it, two otherwise identical numeric values would have ambiguous
horizons. All other handoff fields follow the Phase 3 common interface.

Run from the repository root in WSL:

```bash
source .venv/bin/activate
python docs/phase3-ai-evidence/L3/004/scripts/build_phase4_handoff.py \
  --input docs/phase2-ingestion/L3/004/data/processed/L3_004_probabilities.csv \
  --output docs/phase3-ai-evidence/L3/004/data/l3_004_phase4_handoff.json
pytest -q docs/phase3-ai-evidence/L3/004/tests
```

The bridge rejects a distribution that is incomplete, unavailable, invalid, or
does not sum to one. It never substitutes probabilities.
