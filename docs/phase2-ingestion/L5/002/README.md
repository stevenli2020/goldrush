# L5-002 — Gold Share of Official Reserves

This parser extracts WGC/IMF IFS country-level gold shares of official
reserves from the `PDF` sheet of the official-holdings workbook. It is a
separate transformation from L0-002, which reports holdings in tonnes.

```bash
python parse_gold_reserve_share.py \
  --input ../../data/wgc/raw/central-bank/World_official_gold_holdings_as_of_Aug2026_IFS.xlsx \
  --output processed/L5_002_observations.csv \
  --publication-date 2026-08-20 --download-date 2026-08-21
```

The share is stored as a fraction (for example, `0.814219` = 81.4219%).
Negative or out-of-range shares fail validation. Stale carry-forward requires
operator approval before scoring.
