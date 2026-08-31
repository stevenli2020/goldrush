# L9-001 — Shanghai Gold Exchange Premium/Discount

**Status: Complete — Grace approved.**

This parser consumes the World Gold Council's published `gold-premiums.xlsx`
workbook from the [Gold Premium & Discount](https://www.gold.org/goldhub/data/gold-premium)
page. It extracts only the China series. WGC describes the series as a theoretical
local-versus-international gold-price difference in USD/oz, updated weekly.
The page may display a five-day average; this parser preserves the workbook's
daily file values and records the workbook's verified five-day moving-average
definition. Both premiums and discounts are valid.

The shared WGC downloader target is `gold_premiums`; it preserves the raw file
at `docs/phase2-ingestion/data/wgc/raw/premiums/gold-premiums.xlsx` and passes
the generated manifest to this parser. The parser selects only the exact
`Chinese premiums-discounts` sheet, verifies the title/unit/moving-average text,
and does not calculate a replacement premium from SGE, FX, COMEX, or LBMA data.

Primary collection uses the shared authenticated WGC cookie downloader target
`gold_premiums`. If that session is unavailable, download the workbook manually,
save it unchanged, and create a reproducible manifest with:
`python create_manifest.py gold-premiums.xlsx data/manifests/gold-premiums.json`
Manual manifests record HTTP status and content type as unknown unless observed;
they do not claim a response status. Then pass the manifest to `parser.py --manifest`.
The direct SGE benchmark endpoint is only a diagnostic
and is not substituted for the WGC calculated series. COMEX futures are not used
as an LBMA replacement. Historical changes are retained as revisions. The
January 2025 methodology revision documented by WGC applies to the Indian
series; no China-specific revision date is assumed.

On source failure, the latest valid published row is carried forward as `STALE`;
without prior data the parser writes a machine-readable `BLOCKED` artifact. A
successful output removes that artifact. No observations are synthesized.
