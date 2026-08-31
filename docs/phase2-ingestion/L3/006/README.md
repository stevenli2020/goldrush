# L3-006 — FOMC Statements / Forward-Guidance Signal

> **PHASE 2 SOURCE EXTRACTOR ONLY — DO NOT USE THIS FOLDER FOR SCORING.**
> The canonical Phase 3 scoring workflow is
> [`docs/phase3-ai-evidence/L3/006/`](../../../phase3-ai-evidence/L3/006/).
> This folder remains an upstream dependency for official-document extraction.

**Status:** Source extraction operational; forward-guidance scoring is not performed here.

This source extractor produces only source-backed facts: normalized statement text,
any stated federal-funds target range, timestamps, availability, and provenance.
It does not produce a forward-guidance score. Every output is explicitly
`UNCLASSIFIED`.

Output is `AVAILABLE` for 60 days after release, then `STALE`. The latest valid
statement can be carried forward after a collection failure. With no prior record,
the CLI writes a machine-readable `BLOCKED` artifact. A successful recovery clears
that artifact. A `BLOCKED` artifact preserves the original parse error separately
from any failed prior-data fallback. No NLP, sentiment model, embeddings, or LLM
classification is used. A directional signal must not be supplied manually.

Run from the repository root with the matching statement manifests. Do not build
scoring logic on this output directly; use the Phase 3 workflow above:

```bash
python docs/phase2-ingestion/L3/006/parser.py \
  --html-manifest <statement-html-manifest> \
  --pdf-manifest <statement-pdf-manifest> \
  --output docs/phase2-ingestion/L3/006/data/processed/L3_006_statements.csv
```
