# L4-009 — Treasury Maturity Structure

**Status:** Complete — approved 2026-08-24.

L4-009 measures the share of marketable Treasury debt that matures after each
monthly MSPD record date and within one calendar year:

```text
marketable_debt_maturing_within_1y_pct =
    maturing_within_1y_mil_usd / total_marketable_outstanding_mil_usd * 100
```

The denominator is the unique `Total Marketable` summary. The numerator includes
only positive detail-row amounts with valid maturity dates satisfying
`record_date < maturity_date <= record_date + one calendar year`. Matured rows,
class totals, missing values, and the `Total Marketable` row are excluded.

`dated_detail_outstanding_mil_usd` and `classification_coverage_pct` disclose how
much of total marketable debt can be assigned a maturity date. Rows without dates,
including Federal Financing Bank and summary rows, are not assigned invented
maturities. Classification coverage can be slightly above 100% because Treasury
reports bill detail rows at maturity value while `Total Marketable` reflects bill
discount accounting. This source convention is retained and disclosed; only the
one-year numerator is required not to exceed the denominator.

## Collection

```bash
START_DATE=$(date -u -d '24 months ago' +%F)

python docs/phase2-ingestion/collectors/treasury/treasury_api_client.py \
  'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_3_market' \
  --filter "record_date:gte:${START_DATE}" \
  --sort 'record_date,src_line_nbr' \
  --fields 'record_date,security_type_desc,security_class1_desc,maturity_date,outstanding_amt,src_line_nbr'

python docs/phase2-ingestion/L4/009/parser.py \
  --manifest docs/phase2-ingestion/data/treasury/manifests/<manifest>.json \
  --output docs/phase2-ingestion/L4/009/data/processed/L4_009_observations.csv
```

The shared client preserves every raw page unchanged and records per-page and
aggregate source metadata values. The parser validates those source metadata before calculation.
No daily observations, maturity estimates, or synthetic carry-forward months are
created. Values outside broad 5–80% ratio or 95% coverage bounds are retained as
`FLAG`. The latest monthly observation becomes `STALE` after 62 days.

On failure, the latest valid prior observation is exposed as one `STALE` row. If
none exists, the CLI writes a machine-readable `BLOCKED` artifact. A successful
recovery removes an obsolete blocked artifact.

The files under `data/samples/` are a compact deterministic fixture for parser
and schema inspection. Live raw pages remain in the shared Treasury data area;
the full processed history is under `data/processed/`.

## Daily collection range

The daily operational collector must request a rolling window beginning 24
months before the current date, for example `record_date:gte:2024-08-29` on
2026-08-29. It must not request the full history from 1900 on every run. Full
history is optional archival/backfill work and is kept separate from the daily
path. A recent window is sufficient for the current maturity calculation and
captures recent source revisions without repeatedly downloading 100+ years of
detailed records.
