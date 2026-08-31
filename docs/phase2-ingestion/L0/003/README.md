# L0-003: Gold ETF Holdings

## Overview
This module parses monthly global physical Gold ETF holdings and Assets Under Management (AUM) published by the World Gold Council (WGC).

## Directory Structure
```text
.
├── README.md
├── config.yaml
├── parse_etf_holding.py
├── run_ingest.py
├── schema.json
├── archive/
│   ├── changelog.md
│   └── ingest.log
├── data/
│   └── gold_etf_holdings/
│       └── ETF_Flows_2026-08-04_1202.xlsx
├── processed/
│   └── L0_003_observations.csv
├── samples/
│   ├── processed_sample.csv
│   └── raw_parsed_sample.json
└── tests/
    └── test_parse_etf_holding.py