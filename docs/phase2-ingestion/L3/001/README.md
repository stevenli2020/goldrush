# L3-001 — Fed Funds Futures Expected Policy Rate

L3-001 measures the forward policy path, not the current policy-rate anchor.
The parser consumes a normalized CME Fed Funds futures strip:

```text
observation_date,contract,implied_rate_percent,months_ahead
```

It averages all eligible contracts one to twelve months ahead. This deliberately
differs from L1-006, which uses only the nearest active contract. The shared CME
collector preserves the raw interest-rate bulletin PDFs and manifests. The
`extract_strip.py` adapter prepares the normalized strip and carries that
provenance into the parser output.

Run:

```bash
python parser.py --input data/raw/fed_funds_strip.csv \
  --output data/processed/L3_001_observations.csv
```

Live extraction from a preserved Section 10 normalized settlement file:

```bash
python extract_strip.py --input ../../data/cme/processed/section10_normalized.csv \
  --output data/raw/fed_funds_strip.csv \
  --source metadata <section-10-source metadata> \
  --manifest ../../data/cme/manifests/<section-10-manifest>.json
```

If the strip is unavailable, carry forward the latest path with `STALE` for up to
three trading days. Do not substitute L1-006's nearest-contract value.
