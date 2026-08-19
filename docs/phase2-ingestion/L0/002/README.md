# L0-002: Central-Bank Gold Holdings

## Overview
This module ingests, normalizes, and audits monthly physical gold reserve holdings for a fixed panel of major sovereign and institutional holders:
* **US** (United States)
* **EA** (Euro Area / ECB - `EZB`)
* **CN** (China - `CHN`)
* **JP** (Japan - `JPN`)
* **CH** (Switzerland - `CHE`)
* **IMF** (International Monetary Fund)

## Files in this Directory
* `collector.py`: Main automated ingestion script.
* `tests/test_collector.py`: Pytest test suite covering conversion math, panel schema structure, and mock API execution.
* `data/config.yaml`: Configuration constants and panel mappings.
* `data/schema.json`: Output data schema contract.
* `data/processed/gold_holdings_panel_YYYY-MM-DD.csv`: Dated generated output panel.
* `data/raw/imf_ifs_YYYY-MM-DD.json`: Preserved source payload and metadata.
* `data/archive/live_run_YYYY-MM-DD.json`: Run evidence linking raw and processed files.
* `audit_log.csv`: Append-only audit ledger tracking timestamps, raw values, and freshness status.

## Usage Instructions

### 1. Run the Collector
From the L0-002 directory, ensure your virtual environment is active and run:
```bash
PYTHONPATH=. python collector.py --live
```

For an offline test run:

```bash
PYTHONPATH=. python collector.py --mock
PYTHONPATH=. pytest -q tests/test_collector.py
```

Entity observations use full month-end dates. The `AGGREGATE` row uses the
execution month (`YYYY-MM`) because it is a derived panel summary, not an
independently observed IMF series. Observations older than 150 days are marked
`STALE` and may be carried forward for up to three reporting periods.
