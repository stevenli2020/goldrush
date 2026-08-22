# L4-001 — CPI Inflation Rate

Parses FRED `CPIAUCSL` monthly CPI index observations. The shared FRED client
retrieves raw JSON; this package validates and writes the variable output.

Run: `python parser.py --raw ../../data/macro/raw/fred/CPIAUCSL-<timestamp>.json --output data/processed/L4_001_observations.csv`

Values must be positive. Data older than 45 days is marked `STALE`; carry-forward requires operator approval.
