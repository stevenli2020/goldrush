# L4-006 — Fiscal Deficit / GDP

This package parses FRED `FYFSGDA188S`, Federal Surplus or Deficit [-] as a
Percent of Gross Domestic Product. It preserves the source sign convention:
negative means deficit and positive means surplus. No sign inversion occurs.

FRED constructs the series as `((FYFSD / 1000) / GDPA) * 100`. The numerator
is the federal fiscal-year balance and the denominator is annual calendar-year
GDP. The parser preserves FRED's annual observation date and does not create
monthly or quarterly values.

## Run

```bash
python ../../collectors/macro/fred_client.py FYFSGDA188S
python parser.py \
  --raw ../../data/macro/raw/fred/FYFSGDA188S-<timestamp>.json \
  --manifest ../../data/macro/manifests/FYFSGDA188S-<timestamp>.json \
  --output data/processed/L4_006_observations.csv
```

The shared client preserves raw JSON and manifests. The parser verifies the
series ID and SHA-256, skips FRED `.` markers, rejects malformed or conflicting
annual observations, and flags finite values outside -30% to +10%.

Freshness is determined only from the latest observation. The series becomes
`STALE` 550 calendar days after September 30 of the latest observation year.
Historical rows are retained without synthesizing new periods.

On failure, the latest valid prior observation may be emitted as one `STALE`
row. Without valid prior data, the CLI writes a machine-readable `.status.json`
artifact with `BLOCKED`. A later successful CSV write removes that artifact.

FRED may revise the fiscal balance, annual GDP, and therefore the ratio. Changed
raw responses and their hashes are preserved by the shared client; the output is
the current complete FRED snapshot rather than a separate revision ledger.
