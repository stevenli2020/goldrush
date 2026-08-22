# L5-001 — Monthly Official-Sector Gold Purchase Volume

This collector aggregates country-level monthly changes from the WGC official
reserves workbook into a global tonnes series. Positive values represent net
purchases; negative values represent net sales or reductions.

Run it with:

```bash
python parse_official_purchases.py \
  --input ../../data/wgc/raw/central-bank/Changes_latest_as_of_Aug2026_IFS.xlsx \
  --output processed/L5_001_observations.csv \
  --publication-date 2026-08-20 --download-date 2026-08-21
```

The shared WGC downloader preserves the workbook and hash. This parser owns
aggregation, output schema, and validation. If publication is delayed, carry
forward the last observation as `STALE` and require approval before scoring.
