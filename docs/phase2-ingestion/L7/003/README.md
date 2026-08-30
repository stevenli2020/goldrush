# L7-003 — Global Private Non-Financial Credit Growth

This package collects the BIS-published all-reporting-countries aggregate for credit to the private non-financial sector and calculates its year-on-year growth. It uses the official aggregate rather than constructing a country sum.

## Source and series

- Official dataset: BIS Credit to the non-financial sector, table family F2.2.A.
- SDMX structure: `BIS:WS_TC(2.0)`.
- Series key: `Q.5A.P.A.M.USD.A` — quarterly, all reporting countries (`5A`), private non-financial borrowers (`P`), all lenders (`A`), market value (`M`), USD (`USD`), adjusted for breaks (`A`). The parser additionally requires `UNIT_MULT=9`, the BIS multiplier that identifies the returned values as USD billions.
- Unit: USD billions.

The calculation is `(current quarter / matching quarter one year earlier - 1) * 100`. Growth remains null where the matching prior-year quarter is absent. Levels must be positive and finite. Finite growth above 30% in absolute value is retained as `FLAG`.

## Operation

From the repository WSL environment:

```bash
python docs/phase2-ingestion/L7/003/collector.py
python docs/phase2-ingestion/L7/003/parser.py \
  --raw docs/phase2-ingestion/L7/003/data/raw/<file>.csv \
  --manifest docs/phase2-ingestion/L7/003/data/manifests/<file>.manifest.json
```

If API access fails, download the official flat CSV manually, place it unchanged in `data/raw/`, and create a matching manifest with the dataset and series IDs, URL, timezone-aware retrieval time, raw path, byte size, source metadata, HTTP status, and collector version. The parser validates those fields and the path, size, and source metadata before extraction.

BIS publishes this dataset quarterly with a material lag: a quarter-end level can be released roughly five to six months later. Data older than 270 days is `STALE`, covering that lag plus the interval to the next quarterly release without treating a newly published observation as stale. A failed collection carries forward only the latest prior valid row as `STALE`; its identity, units, dates, values, statuses, timestamps, source metadata, and provenance must validate first. Without valid prior data the CLI writes a machine-readable `.status.json` with `BLOCKED`. Successful recovery removes that artifact. Raw vintages are timestamped and source metadata-named and are not overwritten.

## Interpretation and limitations

- This is a slow-moving credit-capacity indicator, not a short-term market-stress signal.
- Coverage follows the BIS all-reporting-countries aggregate and can change as reporting coverage or classifications change. BIS classification changes and revisions can alter history; preserved vintages expose that.
- USD-denominated aggregate growth is sensitive to exchange-rate movements as well as underlying local-currency credit.
- Publication lag makes carry-forward normal near release dates; no synthetic quarters are created.

## Status

Approved and closed 2026-08-24 after Grace review and final approval. The tracker and changelog contain the closure evidence.
