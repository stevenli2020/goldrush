# L4-008 — Interest Expense / Government Revenue

L4-008 measures the share of annual federal receipts absorbed by gross interest
on Treasury debt securities. It uses the public U.S. Treasury Fiscal Data Monthly
Treasury Statement Table 3 endpoint; no authentication is required.

## Accounting convention

The parser selects September fiscal-year-end rows and calculates:

```text
Interest on Treasury Debt Securities (Gross), line 360, FYTD
---------------------------------------------------------------- * 100
Total Receipts, line 130, FYTD
```

The unit is percent of federal receipts. This is gross Treasury debt interest,
not net interest outlays and not interest as a share of GDP. Available API history
currently yields fiscal years 2015–2025.

## Run

From the repository root:

```bash
python docs/phase2-ingestion/collectors/treasury/treasury_api_client.py \
  https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_3 \
  --filter 'line_code_nbr:in:(130,360)' --sort record_date

python docs/phase2-ingestion/L4/008/parser.py \
  --manifest docs/phase2-ingestion/data/treasury/manifests/<manifest>.json \
  --output docs/phase2-ingestion/L4/008/data/processed/L4_008_observations.csv
```

The shared client preserves exact raw pages, per-page source metadata, an aggregate source metadata,
query metadata, and retrieval time. The parser verifies that provenance, validates
the exact line descriptions, pairs rows by date and fiscal year, and writes only
annual September observations.

Ratios from 0% through 50% are `PASS`; finite non-negative values above 50% are
retained as `FLAG`. Freshness is assessed from the latest completed September
observation using a 450-day threshold to allow normal MTS publication lag.

On failure, `--prior` exposes the latest valid prior observation as one `STALE`
row. Without valid prior data, the CLI writes a machine-readable `.status.json`
artifact with `BLOCKED`. A successful recovery removes that obsolete artifact.
No monthly, quarterly, or synthetic observations are generated.
