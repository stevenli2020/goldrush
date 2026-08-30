# WGC Collector Closure Status

**Review date:** 2026-08-24
**Reviewer:** Grace  
**Status:** Complete for the current approved WGC scope

## Accepted scope

The shared WGC downloader/extractor supports these verified mappings:

- L0-001 — Above-ground gold stock
- L0-002 — Central-bank gold holdings
- L0-003 — Gold ETF holdings
- L0-005 — Bar-and-coin demand
- L0-006 — Gold recycling flow
- L5-001 — Monthly official-sector purchase changes
- L5-002 — Gold share of official reserves
- L8-001 — Monthly gold ETF net flows
- L9-001 — Shanghai Gold Exchange premium/discount

## Acceptance review

- Primary WGC workbooks are accessible through the shared downloader.
- Raw workbooks are preserved by category and identified with source metadata.
- Manifests and extractor run logs are written.
- Unchanged workbooks are skipped during routine runs.
- Variable-specific parsers remain separate.
- Parser-specific tests and shared extractor regression passed.
- Manual file placement remains a documented fallback.
- Cookie storage is protected and excluded from version control.

## Evidence

Regression log:

`docs/phase2-ingestion/data/wgc/logs/wgc-extract-20260821T010308Z.json`

All eight previously completed mappings returned `PASS` during the reviewed
forced regression; L9-001 subsequently passed live download, extraction,
schema, provenance, and fallback verification.

## Limitations

- `--force` should be used only for deliberate regression runs because some
  existing parsers append or rewrite processed outputs.
- WGC page structure or workbook layouts may change and require configuration or
  parser maintenance.
- Conditional variables such as L8-002, L8-004, and L9-002 are outside this
  closure and require separate scope approval.

## Copy-ready main-chat update prompt

> WGC collector review is complete. The shared downloader/extractor supports
> nine approved mappings: L0-001, L0-002, L0-003, L0-005, L0-006, L5-001,
> L5-002, L8-001, and L9-001. Raw workbooks, source metadata manifests, logs, parser-specific
> outputs, tests, schemas, and documentation are in place. Existing variable
> parsers remain separate, unchanged except for thin integration adapters.
> Routine runs skip unchanged files, with L9-001 availability refreshed on
> unchanged manifests; `--force` is reserved for deliberate
> regression testing. The WGC collector is Complete for the approved scope.
> Conditional variables remain outside scope.
