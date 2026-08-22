# L1-007 — 5Y5Y Forward Real Rate

This package derives the specific 5Y5Y forward real-rate point from FRED
`DFII5` and `DFII10`:

```text
100 × [((1 + DFII10/100)^10 / (1 + DFII5/100)^5)^(1/5) − 1]
```

This is a transparent approximation based on constant-maturity TIPS yields. It
is not a full zero-coupon real-yield curve. Inputs are inner-joined by date;
missing input observations are not interpolated and produce no output row.

## Run

```bash
python parser.py \
  --dfii5 ../../data/macro/raw/fred/DFII5-<timestamp>.json \
  --dfii10 ../../data/macro/raw/fred/DFII10-<timestamp>.json \
  --dfii5-retrieved-at <timestamp> \
  --dfii10-retrieved-at <timestamp> \
  --output data/processed/L1_007_observations.csv
```

Each output row preserves both input paths, hashes, series IDs, retrieval
timestamps, formula version, and parser version. Values outside `-10%` to `20%`
are marked `FLAG`; aligned observations older than seven days are `STALE`.
