# L3-006 — FOMC Statements / Forward-Guidance Signal

**Status:** Complete — approved 2026-08-24.

The parser extracts normalized text and any stated federal-funds target range from
official FOMC statement HTML while preserving the matching PDF. It never infers a
qualitative signal. Without a matching reviewed annotation, output is explicitly
`UNCLASSIFIED`.

Annotations under `data/annotations/` must match both release date and the
SHA-256 of the normalized official statement text. This stable content hash
allows the same reviewed annotation to accompany byte-different HTML wrappers
that contain identical statement text. The raw HTML SHA-256 remains separate in
the output and manifest for provenance. Supporting evidence and any
counter-evidence must be verbatim excerpts traceable to the preserved statement.
Allowed signals are `DOVISH`, `NEUTRAL`, `HAWKISH`, `MIXED`, and `UNCLASSIFIED`.

Output is `AVAILABLE` for 60 days after release, then `STALE`. The latest valid
statement can be carried forward after a collection failure. With no prior record,
the CLI writes a machine-readable `BLOCKED` artifact. A successful recovery clears
that artifact. A `BLOCKED` artifact preserves the original parse error separately
from any failed prior-data fallback. No NLP, sentiment model, embeddings, or LLM
classification is used.

Run from the repository root with the matching statement manifests and a reviewed
annotation:

```bash
python docs/phase2-ingestion/L3/006/parser.py \
  --html-manifest <statement-html-manifest> \
  --pdf-manifest <statement-pdf-manifest> \
  --annotation docs/phase2-ingestion/L3/006/data/annotations/<release-date>.json \
  --output docs/phase2-ingestion/L3/006/data/processed/L3_006_statements.csv
```
