# L3-005 — FOMC Dot Plot Path

**Status:** Complete — approved 2026-08-24.

This parser reads the official accessible SEP HTML federal-funds-rate distribution
and preserves the matching official PDF as supporting evidence. It emits one row
for each current-release projection horizon and non-zero rate bin. Embedded prior
projection columns elsewhere on the SEP page are not ingested.

These dots are individual FOMC participants' assessments of appropriate monetary
policy. They are not a Committee decision, promise, or market forecast.

The parser validates non-negative integer counts, unique bins, plausible rates,
participant totals, published medians, manifests, and raw source metadata. A horizon may
contain one fewer participant where the SEP explicitly permits an omitted
projection. Output remains `AVAILABLE` for 120 days and then becomes `STALE`.
No observations are synthesized between SEP releases. If live parsing fails, the
latest valid release can be carried forward as `STALE`; without prior data a
machine-readable `BLOCKED` artifact is written.

Run from the repository root with the shared SEP HTML and PDF manifest paths:

```bash
python docs/phase2-ingestion/L3/005/parser.py \
  --html-manifest <sep-html-manifest> \
  --pdf-manifest <sep-pdf-manifest> \
  --output docs/phase2-ingestion/L3/005/data/processed/L3_005_dot_distribution.csv
```
