# L10-002 — COMEX Gold Futures Open Interest

This collector extracts the daily `COMEX GOLD` open-interest total from the CME
Section 02B Metals Volume and Open Interest report. It measures outstanding
contracts and leverage capacity, not price direction.

The shared CME collector preserves the raw Section 02B PDF and its source metadata
manifest. This parser reads that PDF directly; no manually normalized CSV is a
production input.

Run the variable parser:

```bash
python parser.py --pdf ../../data/cme/raw/metals/section02b-<timestamp>.pdf \
  --source-manifest ../../data/cme/manifests/section02b-<timestamp>.json \
  --output data/processed/L10_002_observations.csv
```

It requires exactly one `GC COMEX GOLD FUTURES` row and extracts the current
open-interest field, not volume, options open interest, or prior-year open
interest. A missing, duplicated, malformed, or layout-shifted field fails
explicitly rather than emitting a substitute value.

Section 62 is not required for this summary implementation. Contract-month
open interest and roll decomposition are deferred. If the report is unavailable,
invalid, or cannot be parsed, the run is recorded as `BLOCKED`; it never carries
forward a prior open-interest value.
