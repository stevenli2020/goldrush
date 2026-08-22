# L1-005 — Treasury Term Premium

This package parses FRED `THREEFYTP10`, the Board of Governors' daily term-premium
estimate for a 10-year zero-coupon Treasury bond. It is a model-derived estimate,
not a directly observed market price.

The shared `collectors/macro/fred_client.py` retrieves and preserves raw JSON;
this parser owns the L1-005 schema, sanity checks, freshness status, and CSV output.

```bash
python parser.py \
  --raw ../../data/macro/raw/fred/THREEFYTP10-<timestamp>.json \
  --output data/processed/L1_005_observations.csv
```

Values are percentage points. Values outside `-10%` to `10%` are marked `FLAG`.
Observations older than seven days are marked `STALE`; carry-forward requires
explicit operator approval.
