# L5-003 — Reserve Composition Change / USD Share Change

This package collects the IMF COFER world aggregate and retains the published U.S. dollar share of allocated foreign-exchange reserves. It calculates quarter-on-quarter percentage-point change without manufacturing missing quarters.

## Source and series

- Official dataset: IMF Currency Composition of Official Foreign Exchange Reserves (COFER).
- SDMX structure: `IMF.STA:COFER`.
- Selection: world aggregate `G001`, indicator `AFXRA`, U.S. dollar `CI_USD`, published share `SHRO_PT`, quarterly `Q`.
- Unit: percent for the source share and percentage points for the calculated change.

Country-level reserve composition is confidential and is not collected. COFER excludes monetary gold from foreign-exchange reserves. IMF's methodology change introduced with 2025 Q3 eliminated the unallocated-reserves component and revised the published currency shares back to 2000 Q1, so preserved raw vintages may legitimately differ.

A falling U.S. dollar share is not, by itself, evidence of gold buying or de-dollarization. It can reflect exchange rates, reserve-manager transactions, reporting changes, and revisions.

## Operation

From the repository WSL environment:

```bash
python docs/phase2-ingestion/L5/003/collector.py
python docs/phase2-ingestion/L5/003/parser.py \
  --raw docs/phase2-ingestion/L5/003/data/raw/<file>.csv \
  --manifest docs/phase2-ingestion/L5/003/data/manifests/<file>.manifest.json
```

If API access fails, download the official CSV manually, place it unchanged in `data/raw/`, and create a matching manifest with the dataset ID, source URL, timezone-aware retrieval time, raw path, byte size, SHA-256, HTTP status, and collector version. The parser validates these fields and verifies the path, size, and raw hash before extraction.

The calculation is `current published USD share - immediately previous calendar quarter's published USD share`. The first valid observation, and any observation whose immediately preceding quarter is missing, has a null change. Shares outside 0–100 are rejected; finite changes above 5 percentage points in absolute value are retained as `FLAG`. Quarterly data older than 200 days is `STALE`, allowing normal IMF publication lag. A failed collection carries forward only the latest prior valid row as `STALE`; without prior data the CLI writes a machine-readable `.status.json` with `BLOCKED`. A later successful parse removes that artifact.

Raw snapshots are timestamped and hash-named, never overwritten. Manifests and each output row retain the source and hash chain. Carry-forward accepts only prior rows whose variable/source identity, units, dates, values, statuses, timestamps, hashes, and provenance fields remain valid.

## Limitations

- This is a quarterly, revised reserve-composition indicator, not a real-time flow measure.
- Published shares are accepted directly; no incompatible numerator/denominator reconstruction is attempted.
- One official source and manual placement fallback are intentionally sufficient for this personal project.

## Status

Approved and closed 2026-08-24 after Grace review and final approval. The tracker and changelog contain the closure evidence.
