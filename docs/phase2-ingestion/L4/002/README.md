# L4-002 — Core PCE Inflation Rate

Parses FRED `PCEPILFE` monthly core PCE price-index observations. The shared FRED client retrieves raw JSON; this package validates and writes the variable output.

Run: `python parser.py --raw ../../data/macro/raw/fred/PCEPILFE-<timestamp>.json --output data/processed/L4_002_observations.csv`
