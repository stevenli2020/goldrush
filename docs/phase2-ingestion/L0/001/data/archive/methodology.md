# L0-001 Methodology Archive

## Source

- Provider: World Gold Council (WGC) GoldHub
- Dataset: Above-ground gold stocks
- Source page: https://www.gold.org/goldhub/data/how-much-gold
- Workbook format: XLSX, worksheet `Above-ground stocks`
- Citation stated by WGC workbook: Metals Focus, Refinitiv GFMS, World Gold Council

## Definition and units

The dataset reports estimated above-ground gold stocks by annual observation year,
measured in tonnes. The parser preserves the reported categories and total and
checks that the category totals reconcile within the configured tolerance.

## Collection timing

Aiproxy manually downloads the annual WGC workbook in mid-February. The parser
records the download date, source publication date when available, workbook SHA-256
hash, and ingestion timestamp. The original workbook is retained under the raw
source directory for reproducibility.

## Archive note

This file records the methodology reference used for the L0-001 implementation. If
WGC changes the workbook definition or category structure, update this note and the
parser/schema review before accepting the next annual release.
