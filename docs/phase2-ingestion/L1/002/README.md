# L1-002 — 5Y TIPS Real Yield

This package parses the preserved FRED `DFII5` daily series. The shared
`collectors/macro/fred_client.py` handles retrieval and raw-response manifests;
this parser owns the L1-002 output schema and validation.

## Run

```bash
python parser.py \
  --raw ../../data/macro/raw/fred/DFII5-<timestamp>.json \
  --output data/processed/L1_002_observations.csv
```

Values are percentage points. Values outside the broad `-10%` to `20%` sanity
range are marked `FLAG`, not rejected. Observations older than seven days are
marked `STALE`; carry-forward is allowed only with explicit operator approval.
FRED publishes this as a daily business-day series. Normal FRED missing-value
markers (`.`) are skipped; malformed non-missing observations fail the run. The
collector does not create interpolated observations.

The parser does not calculate forward rates or breakeven inflation.
