# L6-002 changelog

2026-08-24 — Initial proportional implementation. Official OFAC structured deltas are preserved and normalized as list actions, with no speculative severity or sovereign-freeze classification. Pending Grace review.
2026-08-24 — Grace rework: official archive POST/API and namespaced XML parser implemented. Live 2026-08-20 delta parsed to 49 actions; publication date comes from XML; descendant-only updates and null names are retained. Pending re-review.
2026-08-24 — Grace final approval: Complete. Official API/XML integration, numbered-delta selection, live evidence, source metadata, schema validation, fallback/recovery, and regression tests accepted. Limitations: U.S. OFAC list-action proxy; no legal, severity, sovereign-freeze, or gold-direction inference.
