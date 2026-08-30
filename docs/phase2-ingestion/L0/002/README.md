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
* `collector.py`: Legacy IMF/OpenBB collector retained for historical reference; not the approved production route.
* `tests/test_collector.py`: Pytest test suite covering conversion math, panel schema structure, and mock API execution.
* `data/config.yaml`: Configuration constants and panel mappings.
* `data/schema.json`: Output data schema contract.
* `data/processed/gold_holdings_panel_YYYY-MM-DD.csv`: Dated generated output panel.
* `data/raw/imf_ifs_YYYY-MM-DD.json`: Legacy IMF payloads retained for historical reference.
* `data/archive/live_run_YYYY-MM-DD.json`: Legacy IMF run evidence.
* `audit_log.csv`: Append-only audit ledger tracking timestamps, raw values, and freshness status.

## Usage Instructions

### 1. Approved WGC route
From the repository root, ensure your WSL virtual environment is active and run:
```bash
python docs/phase2-ingestion/collectors/wgc/wgc_download.py --config docs/phase2-ingestion/collectors/wgc/config.yaml --target official_holdings
```

The downloaded workbook is passed to `docs/phase2-ingestion/L0/002/parse_official_holdings.py` by the configured WGC extractor. The legacy IMF/OpenBB and mock commands are not production instructions.

Entity observations use full month-end dates. The `AGGREGATE` row uses the
execution month (`YYYY-MM`) because it is a derived panel summary, not an
independently observed IMF series. Observations older than 150 days are marked
`STALE` and may be carried forward for up to three reporting periods.
