# L6-001 Active Conflict and Escalation Signal

This package preserves and parses the Caldara–Iacoviello Daily Recent Geopolitical Risk Stata vintage. `GPRD`, `GPRD_THREAT`, and `GPRD_ACT` are published news-based indices; `gpr_act_index` is the canonical acts component. It is a proxy, not a verified conflict-event database. No GDELT, ACLED, NLP, rolling z-scores, ratios, or country aggregation are included.

Run `collector.py` to discover the exact `data_gpr_daily_recent_YYYYMMDD.dta` link, preserve an immutable source metadata-named raw file, and write a manifest. Run `parser.py --raw ... --manifest ... --output ...`. A failed run carries forward the latest valid output as `STALE`; with no prior output it writes `<output>.status.json` with `BLOCKED`. Source vintages and source metadata preserve revisions.

## Phase 4 integration

`score.py` exposes the pure `compute_l6_001` function. The Phase 4 caller passes the latest 60 `GPRD_ACT` values and persists the returned `prev_score` and `missing_days` state between runs. A non-missing observation produces the deterministic float consumed by Phase 4, bounded to `[-1.0, 1.0]`; a missing observation decays the prior score by 5% and resets it to zero after three consecutive missing days. Fewer than 60 values are rejected.
