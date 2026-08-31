# L2-003 — USD/CNY

This package parses FRED `DEXCHUS`, the Federal Reserve Board H.10 series
“Chinese Yuan Renminbi to One U.S. Dollar.” It is a daily, not seasonally
adjusted CNY-per-USD noon buying rate in New York for cable transfers. It is
distinct from offshore CNH pricing and is not the PBoC central-parity fixing.

The shared FRED client preserves the raw response and source metadata manifest. This
package owns parsing, validation, provenance fields, and fallback output.

## Run

```bash
python ../../collectors/macro/fred_client.py DEXCHUS
python parser.py --raw ../../data/macro/raw/fred/DEXCHUS-<timestamp>.json \
  --manifest ../../data/macro/manifests/DEXCHUS-<timestamp>.json \
  --output data/processed/L2_003_observations.csv
```

If collection fails, carry forward a canonical prior output explicitly:

```bash
python parser.py --prior data/processed/L2_003_observations.csv \
  --output data/processed/L2_003_observations.csv
```

FRED `.` markers are skipped. Dates are retained and sorted; conflicting
duplicate dates fail. Values from 4.0 through 9.0 CNY/USD are `PASS`; values
outside that practical range are retained as `FLAG` for review. Rows older than
ten days are `STALE`. H.10 normally publishes the preceding business week’s
daily observations on Monday ([release schedule](https://www.federalreserve.gov/releases/h10/)),
so this threshold allows for the weekly release cadence plus a short retrieval
gap. A failed collection carries forward the latest valid
prior row; with no valid prior, a machine-readable `.status.json` is written as
`BLOCKED`. A successful CSV write removes that obsolete status artifact. No
synthetic daily observations are created.

The source is public and reproducible. Publication timing, revisions, managed-
exchange-rate policy, and CNY/CNH market differences remain limitations.
