# Phase 2 — Data Ingestion

## Purpose and scope

This directory contains the approved Phase 2 collectors, variable-specific
parsers, schemas, raw-data evidence, tests, and operational documentation for
the 44 variables admitted by the frozen Phase 1 registry.

The 30 Phase 1 variables marked `CONDITIONAL / RESEARCH ONLY` are outside
production ingestion and are not promoted by Phase 2.

Phase 2 is complete and formally handed off. See
[phase2-handoff.md](phase2-handoff.md) for the closure record.

## Current layout

```text
docs/phase2-ingestion/
├── collectors/                         # Reusable source transports/extractors
│   ├── cme/                             # CME bulletin download/extraction
│   ├── fomc/                            # Federal Reserve publication download
│   ├── macro/                           # FRED and SOFR/FRED transport
│   ├── treasury/                        # U.S. Treasury Fiscal Data API client
│   └── wgc/                             # WGC download, manifests, extraction
├── data/wgc/                            # Shared WGC raw files, manifests, logs
├── L0/ ... L10/                         # Variable packages by Phase 1 layer
│   └── NNN/
│       ├── parser/collector scripts     # Package-specific implementation
│       ├── config.yaml                  # Where used; package configuration
│       ├── schema.json                  # Where used; output validation schema
│       ├── README.md                    # Operational instructions
│       ├── tests/                       # Focused regression tests
│       ├── raw/                         # Where used; preserved source files
│       ├── processed/                   # Normalized variable output
│       └── archive/                     # Changelog and ingest evidence
├── pretests/                            # Historical exploratory checks
├── PHASE2-WORKFLOW.md                   # Review and closure rules
├── SOURCE-IMPLEMENTATION-TRACKER.md     # Authoritative variable status record
├── phase2-handoff.md                    # Final approval and handoff
└── README.md                            # This guide
```

Variable packages are not required to have an identical internal layout. Their
README, configuration, schema, parser, raw evidence, and processed-output
locations are authoritative for that variable. Do not infer a `data/` folder
where the package does not contain one.

## Shared collectors

Shared collectors handle transport, source preservation, manifests, source metadata, and
common retrieval concerns. Variable parsers remain separate and own extraction,
validation, revisions, units, freshness, fallback, and output schemas.

- `collectors/wgc/` — World Gold Council downloads and dispatch
- `collectors/cme/` — CME PDF download and settlement extraction
- `collectors/macro/` — FRED JSON/raw retrieval and SOFR support
- `collectors/treasury/` — paginated Treasury Fiscal Data API retrieval
- `collectors/fomc/` — official FOMC HTML/PDF preservation

Completed variable implementations reuse these collectors where appropriate;
they do not use one universal parser.

## Operational workflow

For a routine run:

1. Open the variable package README and configuration.
2. Retrieve or place the documented primary source; preserve the raw file or
   response unchanged when the package requires it.
3. Run the package collector/parser or the documented shared-collector command.
4. Validate output against the package schema and review validation and
   availability statuses.
5. Retain the raw source, manifest/source metadata, processed output, and ingest evidence.
6. Record meaningful source or parser changes in the package changelog.

Fallback behavior is variable-specific. Carry-forward observations are marked
`STALE`; an unavailable series with no valid prior observation is represented by
the documented `BLOCKED` status. Synthetic observations are not silently added.

## Review and status rules

The workflow is defined in [PHASE2-WORKFLOW.md](PHASE2-WORKFLOW.md). The
authoritative status source is
[SOURCE-IMPLEMENTATION-TRACKER.md](SOURCE-IMPLEMENTATION-TRACKER.md).

The permitted lifecycle is:

```text
Not done → Complete
Not done → Deferred
```

`Complete` requires a named accessible source, reproducible collection,
defined fields/units/timestamps, documented freshness and fallback behavior,
preserved raw observations, validation, and operational instructions.

`Deferred` is reserved for an unresolved source, methodology, access,
historical-coverage, or reproducibility blocker, and must state its reopening
condition.

## Verification

Run the full Phase 2 test suite from the repository root:

```bash
source .venv/bin/activate
pytest -q docs/phase2-ingestion
```

The final closure run passed **310 tests** and **9 subtests**, with no failures.
Third-party OpenBB/Pydantic deprecation warnings are non-blocking environment
warnings.

## Navigation

- By layer: `L0/`, `L1/`, … `L10/`
- By variable: `L*/NNN/`
- By source transport: `collectors/<source>/`
- By status and ownership: `SOURCE-IMPLEMENTATION-TRACKER.md`
- By final decision: `phase2-handoff.md`
