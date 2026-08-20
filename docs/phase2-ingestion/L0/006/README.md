# L0-006: Gold Recycling Flow Ingestion Module

## Overview
This module handles ingestion, parsing, quarter label normalization, and revision tracking for quarterly global gold recycling supply data (measured in metric tonnes).

## Specifications
* **Variable ID:** `L0-006`
* **Unit:** `tonnes`
* **Frequency:** `quarterly`
* **Supported Inputs:** Seed CSV files (`data/raw/seeds/l0_006_recycling_seed.csv`) and Excel workbooks (`.xlsx`).
* **Output Path:** `processed/l0_006_gold_recycling_flow.json`

## Execution
```bash
python scripts/gold_recycling_flow.py