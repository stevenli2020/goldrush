# L8-001 — Gold ETF Demand (change in holdings)

L8-001 is monthly gold ETF demand, defined by the WGC workbook as the change in
gold holdings during the period. It is distinct from L0-003, which measures ETF
holdings as a stock.

## Run directly

```bash
python parse_etf_flows.py \
  --input ../../data/wgc/raw/etf/ETF_Flows_2026-08-04_1202.xlsx \
  --output processed/L8_001_observations.csv \
  --publication-date 2026-08-04 \
  --download-date 2026-08-21
```

## Shared WGC flow

The normal workflow downloads the ETF workbook once and dispatches it to both
the L0-003 holdings parser and this L8-001 flow parser through `wgc_extract.py`.

## Fields and limitations

The parser reads the `Demand by month` sheet and sums numeric per-fund demand
columns after the metadata columns. It does not use the aggregate `Tonnes`
column from `Fund flows by month`, which is holdings-like in the preserved
workbook. Negative values are valid net outflows. The parser preserves source
filename, dates, source metadata, ingestion timestamp, and status fields. It does
not use the GLD/IAU Yahoo Finance activity proxy from the pretest folder.

If WGC publication is delayed, carry forward the last observation as `STALE`
and require operator approval before scoring.
