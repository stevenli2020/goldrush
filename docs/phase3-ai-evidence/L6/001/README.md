# L6-001 Phase 3 live integration

`scripts/run_live.py` performs the complete L6-001 Phase 3 path: it collects
the approved Caldara-Iacoviello GPR source, parses the published `GPRD_ACT`
observations, selects the latest 60 values, and writes one canonical Phase 4
handoff record.

The handoff `value` is the deterministic score from
`docs/phase2-ingestion/L6/001/score.py`, bounded to `[-1.0, 1.0]`. Its state is
persisted in `data/state.json`: callers must retain `prev_score` and
`missing_days` between runs. A stale source decays the prior score by 5%; the
third consecutive stale run emits `0.0`. No external evidence, AI classifier,
or substitute source value is used.

Run in WSL:

```bash
source .venv/bin/activate
python docs/phase3-ai-evidence/L6/001/scripts/run_live.py
```

The canonical payload contains only `variable_id`, `observation_timestamp`,
`value`, `unit_or_scale`, `availability_status`, `source_reference`, and
`quality_flag`; `trend_note` is included only when the score calculation emits
one.
