# L7-005 — Treasury Repo Funding Stress

This package joins the official New York Fed reference-rate series preserved by
the shared FRED client: `SOFR` (secured overnight Treasury repo financing rate)
and `EFFR` (effective federal funds rate). Both are daily, not seasonally
adjusted percentages. The output is the deliberately narrow proxy:

`repo_funding_stress_bps = (SOFR - EFFR) * 100`

Positive values mean secured repo funding is above unsecured federal funds;
negative values are valid. This is not a complete repo stress index.

The parser verifies both series IDs, raw-file source metadata, retrieval metadata,
dates, finite numeric values, and conflicting duplicate dates. It skips FRED `.`
markers and intersects dates only; it never carries one rate across a missing
date. Rates and spreads outside broad configured bounds are retained with
`FLAG`. A five-calendar-day freshness threshold permits weekends and holidays.

On failure, `--prior` emits the latest valid row once with `STALE`. If no valid
prior exists, the CLI writes a machine-readable `.status.json` with `BLOCKED`.
A successful CSV write removes that obsolete status artifact.

## Run

From the repository root, using the project virtual environment:

```bash
source .venv/bin/activate
python docs/phase2-ingestion/collectors/macro/fred_client.py SOFR
python docs/phase2-ingestion/collectors/macro/fred_client.py EFFR
python docs/phase2-ingestion/L7/005/parser.py \
  --sofr-raw docs/phase2-ingestion/data/macro/raw/fred/SOFR-<timestamp>.json \
  --sofr-manifest docs/phase2-ingestion/data/macro/manifests/SOFR-<timestamp>.json \
  --effr-raw docs/phase2-ingestion/data/macro/raw/fred/EFFR-<timestamp>.json \
  --effr-manifest docs/phase2-ingestion/data/macro/manifests/EFFR-<timestamp>.json \
  --output docs/phase2-ingestion/L7/005/data/processed/L7_005_observations.csv
```

After a collection failure, expose the latest valid prior row as `STALE`:

```bash
python docs/phase2-ingestion/L7/005/parser.py \
  --prior docs/phase2-ingestion/L7/005/data/processed/L7_005_observations.csv \
  --output docs/phase2-ingestion/L7/005/data/processed/L7_005_observations.csv
```

The verified New York Fed schedule is approximately 8:00 a.m. ET for SOFR and
approximately 9:00 a.m. ET for EFFR, generally reporting the prior business
day's activity. SOFR publication follows the SIFMA U.S. government-securities
holiday calendar, while EFFR follows the New York Fed holiday schedule. The
five-calendar-day threshold therefore allows ordinary weekends and holidays
without manufacturing observations or falsely marking a current run stale.
