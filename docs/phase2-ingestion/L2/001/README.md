# L2-001 — DXY US Dollar Index

**Status: Complete — Grace approved.**

This package preserves daily OHLC data retrieved through OpenBB's `yfinance`
provider for symbol `DX-Y.NYB`. `dxy_close` is the canonical observation. Yahoo
Finance/OpenBB is an unofficial free market-data source; its availability,
history, and field conventions may change, so raw snapshots and manifests are
retained for replay and review.

Run the collector, then parser:

```bash
python collector.py --start-date 2020-01-01 --raw-dir data/raw --manifest-dir data/manifests
python parser.py --raw data/raw/DX-Y.NYB-<timestamp>.csv --manifest data/manifests/DX-Y.NYB-<timestamp>.json --output data/processed/L2_001_observations.csv
```

Dates are preserved, sorted, and never interpolated. Missing optional OHLC fields
remain null; close is required. Values outside 50–200 are flagged. A failed run
carries forward the latest valid row as `STALE`, or writes a machine-readable
`BLOCKED` artifact when no prior exists. Successful output removes that artifact.
Changed OHLC values for an existing date are marked as revisions; a retrieval
source metadata change alone is not a revision. DXY overlaps with completed L2-002, so the
two dollar variables must not be independently double-weighted in downstream
scoring.
