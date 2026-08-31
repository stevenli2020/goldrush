# L7-001 — Federal Reserve Liquidity Proxy

This baseline uses FRED `WALCL` as a transparent Federal Reserve balance-sheet
proxy. It collects the Federal Reserve's total assets, in millions of U.S.
dollars, not seasonally adjusted, weekly as of Wednesday. H.4.1 is normally
released Thursday at about 4:30 p.m. ET.

This is deliberately narrower than the frozen Phase 1 concept. It is not a
multi-central-bank composite and performs no currency conversion. ECB, BoJ, PBoC,
and broader aggregation are outside the Phase 3 baseline and are not blockers.
Phase 4 must interpret this variable as Federal Reserve liquidity, not global
major-central-bank liquidity.

## Run

```bash
python docs/phase2-ingestion/collectors/macro/fred_client.py WALCL
python docs/phase2-ingestion/L7/001/parser.py \
  --raw docs/phase2-ingestion/data/macro/raw/fred/WALCL-<timestamp>.json \
  --manifest docs/phase2-ingestion/data/macro/manifests/WALCL-<timestamp>.json \
  --output docs/phase2-ingestion/L7/001/data/processed/L7_001_observations.csv
```

The parser retains weekly observation dates and creates no daily observations.
FRED `.` markers are skipped. Malformed dates, non-finite/non-positive values,
wrong-series manifests, source metadata mismatches, and conflicting duplicate dates fail.
Values outside 100,000–50,000,000 million USD are flagged rather than rejected.

Observations older than ten calendar days are `STALE`, allowing normal weekly
publication lag. The shared FRED client and this parser are separate commands;
a collection failure does not automatically start the parser. After a failed
collection, the operator manually exposes the latest valid observation as one
`STALE` row with:

```bash
python docs/phase2-ingestion/L7/001/parser.py \
  --prior docs/phase2-ingestion/L7/001/data/processed/L7_001_observations.csv \
  --output docs/phase2-ingestion/L7/001/data/processed/L7_001_observations.csv
```

If no valid prior output exists, running the parser without usable source or
prior data produces a machine-readable `.status.json` artifact with `BLOCKED`.
A later successful CSV write removes that artifact.
