# L10-001 — COMEX Managed-Money Net Positioning

The collector downloads the official CFTC Disaggregated Futures-Only COT file and extracts the COMEX gold contract (`088691`, `FutOnly`). The raw file is preserved unchanged and source metadata.

`collector.py` uses `curl`, validates the 191-column layout, extracts the gold row, and writes a normalized source file plus a manifest. `parser.py` calculates:

```text
managed_money_net_contracts = managed_money_long_contracts - managed_money_short_contracts
```

The CFTC report date is the Tuesday position date. Retrieval time is recorded separately. The latest valid observation is exposed as the current value; no synthetic carry-forward rows are created. A report becomes `STALE` after 10 calendar days. If no valid prior observation exists after a failed collection, availability is `BLOCKED`.

When a download fails, run `collector.py --prior data/processed/L10_001_observations.csv --as-of YYYY-MM-DD`. It returns the latest valid existing observation with its original `report_date` and refreshed `availability_status`; it does not append or rewrite an observation. Without a valid prior file it returns `BLOCKED`.

The source is weekly and generally released on Friday. The data describes reportable managed-money futures positions, not a daily estimate of all investor positioning.

## Run

```bash
python collector.py
python parser.py --as-of 2026-08-22
```

Historical annual CFTC files and crowding statistics are optional and outside the baseline implementation.
