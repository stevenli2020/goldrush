# L7-004 — Credit-Spread Financial Stress

This package uses FRED `BAMLH0A0HYM2`, the ICE BofA US High Yield Index
Option-Adjusted Spread. The source observation is the daily closing spread in
percentage points, not seasonally adjusted. Observation dates are preserved
without weekend, holiday, or carry-forward rows. A weekend observation can
occasionally appear for month-end accrued-interest adjustment.

The observation date represents the index's daily close. FRED updates after ICE
makes the index observation available; the source does not publish a fixed daily
release time, so freshness is assessed from the latest valid observation date.

The measure is a transparent U.S.-dollar below-investment-grade corporate-credit
benchmark. It is not a complete global financial-stress measure and does not
produce a gold signal or crisis classification. ICE controls the index methodology.
Starting in April 2026, FRED limits this public series to three years of history;
the shared client preserves each retrieved snapshot and SHA-256 for local use.
ICE's FRED terms describe the top-level data as licensed for internal use, which
fits this personal project but limits redistribution.

## Run

```bash
python docs/phase2-ingestion/collectors/macro/fred_client.py BAMLH0A0HYM2
python docs/phase2-ingestion/L7/004/parser.py \
  --raw docs/phase2-ingestion/data/macro/raw/fred/BAMLH0A0HYM2-<timestamp>.json \
  --manifest docs/phase2-ingestion/data/macro/manifests/BAMLH0A0HYM2-<timestamp>.json \
  --output docs/phase2-ingestion/L7/004/data/processed/L7_004_observations.csv
```

FRED `.` missing markers are skipped. Malformed dates, non-finite values,
wrong-series manifests, hash mismatches, and conflicting duplicate dates fail.
Finite values outside 0.5–30 percentage points are retained and flagged. A
seven-day freshness threshold allows normal weekends and market holidays.

On collection failure, run with `--prior` to expose the latest valid observation
as one `STALE` row. With no valid prior observation, the CLI writes a
machine-readable `.status.json` artifact with `BLOCKED`. A later successful CSV
write removes the obsolete blocked artifact.
