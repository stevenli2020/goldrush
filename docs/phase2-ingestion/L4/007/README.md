# L4-007 — Debt / GDP

This package parses FRED `GFDEGDQ188S`, Federal Debt: Total Public Debt as a
Percent of Gross Domestic Product. FRED calculates the ratio as
`((GFDEBTN / 1000) / GDP) * 100`. The published series is quarterly, seasonally
adjusted, and measured as percent of GDP.

This is U.S. federal total public debt (a gross public-debt measure), not net
debt, general-government debt, household debt, or a cross-country comparison.
FRED labels each observation with the first day of its quarter. The parser keeps
that date and does not create monthly or daily rows.

## Run

```bash
python ../../collectors/macro/fred_client.py GFDEGDQ188S
python parser.py \
  --raw ../../data/macro/raw/fred/GFDEGDQ188S-<timestamp>.json \
  --manifest ../../data/macro/manifests/GFDEGDQ188S-<timestamp>.json \
  --output data/processed/L4_007_observations.csv
```

The shared FRED client preserves raw JSON, manifests, retrieval time, and
SHA-256. The parser verifies the series ID and hash, skips `.` missing markers,
rejects malformed/non-finite values and conflicting dates, and flags finite
values outside 0–250% rather than discarding them.

Freshness is based only on the latest source quarter. A snapshot becomes
`STALE` 190 days after the latest quarter end, allowing for the normal quarterly
publication lag. Historical dates remain unchanged.

On failure, the latest valid prior observation is emitted as one `STALE` row.
Without prior data, the CLI writes a machine-readable `.status.json` artifact
with `BLOCKED`. A later successful CSV write removes the obsolete artifact.

FRED may revise either total public debt, GDP, or the resulting ratio. The
shared client preserves changed raw snapshots and hashes; no separate revision
ledger is required for this personal-project collector.
