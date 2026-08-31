# L0-001 data operations

L0-001 records annual above-ground gold stocks published by the World Gold Council. Values are metric tonnes and cover the WGC worksheet `Above-ground stocks`.

## Run the collector

From the repository root:

```bash
source .venv/bin/activate
python docs/phase2-ingestion/L0/001/scripts/parse_above_ground.py \
  --input docs/phase2-ingestion/L0/001/data/raw/YYYY/raw_wgc_above_ground_stock_YYYYMMDD.xlsx \
  --output-dir docs/phase2-ingestion/L0/001/data/processed \
  --download-date 2026-02-15 \
  --publication-date 2026-01-31
```

The supplied development workbook is under `data/above-ground-gold-stocks/2026/`. Production downloads belong under `data/raw/YYYY/` and must be preserved unchanged.

## Outputs

- `processed/above_ground_stocks.csv`: normalized wide observations.
- `processed/above_ground_stocks.parquet`: equivalent columnar output when a Parquet engine is installed.
- `processed/validation_warnings.log`: non-fatal year-over-year warnings.
- `processed/revision_log.json`: changes relative to a previous processed file when supplied with `--previous`.

Each observation includes its year-end reference date, source citation, workbook source metadata, UTC ingestion timestamp, manual download/publication dates, validation status, availability status, and parser version.

## Validation

The parser fails on missing, malformed, negative, or non-finite required values. It checks:

- `jewellery + private investment + central banks + other = total`;
- `bars and coins + ETFs = private investment`;
- both sums within `0.0001` tonnes.

Year-over-year decreases or unusually large changes are logged as warnings and require review; they do not silently alter observations.

Missing or malformed source values fail the run. For a manually downloaded file, record the dates from the WGC release and the day the file was downloaded when invoking the parser.

## Provenance and revisions

Archive each source workbook in `data/raw/YYYY/`. Do not edit archived files. The parser records the workbook source metadata and source citation. If a prior CSV or Parquet file is passed with `--previous`, changed historical values are written to `revision_log.json`.

## Development files

- `schema.json` defines the processed observation contract.
- `samples/` contains small static fixtures.
- `archive/changelog.md` records parser and source changes.
- `../tests/test_parse_above_ground.py` verifies parsing, validation, provenance, outputs, and revisions.
