# L2-002 — Broad Trade-Weighted Nominal US Dollar Index

The collector parses the official FRED `DTWEXBGS` series: the Federal Reserve
Board's Nominal Broad U.S. Dollar Index from the H.10 Foreign Exchange Rates
release. It is a daily, not-seasonally-adjusted index with January 2006 = 100.

The shared FRED client fetches and preserves the raw JSON, source metadata, and manifest.
This package owns only L2-002 parsing, validation, and output.

## Run

```bash
python ../../collectors/macro/fred_client.py DTWEXBGS
python parser.py --raw ../../data/macro/raw/fred/DTWEXBGS-<timestamp>.json \
  --manifest ../../data/macro/manifests/DTWEXBGS-<timestamp>.json \
  --output data/processed/L2_002_observations.csv
```

FRED missing markers (`.`) are skipped; malformed non-missing observations fail.
Dates are retained exactly, sorted chronologically, and conflicting duplicate
dates fail. Values outside 50–200 are flagged for review, not rejected. A raw
failure can carry forward the latest valid prior row as `STALE`; without prior
data the result is `BLOCKED`. No synthetic daily observations are created.

The source is public and reproducible, but FRED release timing can create a
short gap at the end of the daily series. The 10-day freshness threshold is a
practical trading-project rule, not a source publication guarantee.
