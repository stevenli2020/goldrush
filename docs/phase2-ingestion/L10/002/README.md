# L10-002 — COMEX Gold Futures Open Interest

This collector extracts the daily `COMEX GOLD` open-interest total from the CME
Section 02B Metals Volume and Open Interest report. It measures outstanding
contracts and leverage capacity, not price direction.

The shared CME collector preserves the raw Section 02B PDF and its SHA-256
manifest. A separate extraction step converts the PDF to this normalized CSV:

```text
observation_date,product,open_interest
```

Run the variable parser:

```bash
python parser.py --input data/raw/section02b_normalized.csv \
  --output data/processed/L10_002_observations.csv
```

Section 62 is not required for this summary implementation. Contract-month
open interest and roll decomposition are deferred. If a report is unavailable,
carry forward the latest observation with `STALE` for up to five trading days.
