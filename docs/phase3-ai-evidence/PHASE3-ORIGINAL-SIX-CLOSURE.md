# Phase 3 — Original Six Problem Variables Closure

**Date:** 2026-08-29  
**Status:** Closed and evidence-consistent

The six source/integrity problems identified during the Phase 3 review are
closed. Each now has an approved source, a reproducible collection and parsing
path, a deterministic output, live-run evidence, and documented handling for
unsupported or unavailable input.

| Variable | Closure evidence | Result |
|---|---|---|
| L0-002 | WGC official-holdings workbook; `L0/002/processed/L0_002_observations.csv` | 52 `PASS`/`AVAILABLE` metric-tonne records; replay matched observation fields |
| L0-006 | WGC GDT workbook and manifest `data/wgc/manifests/gdt-20260829T024619Z.json`; `L0/006/processed/L0_006_observations.json` | 66 quarterly `AVAILABLE` observations; replay matched date, value, unit, and frequency |
| L1-006 | CME Section 10 download and `L1/006/data/processed/L1_006_observations.csv` | Live expected policy rate extracted as 3.63% per annum; validation `PASS` |
| L3-004 | `L3/004/data/l3_004_phase4_handoff.json` and 2026-08-29 live source manifests | Five `PASS`/`AVAILABLE` probability handoff rows; replay was byte-identical |
| L3-006 | `L3/006/data/results/live-l3-006-rerun.json` | Completed live scoring workflow; prior manual annotation is superseded and excluded |
| L10-002 | `L10/002/data/processed/L10_002_observations.csv` and CME Section 02B manifest | 423,793 COMEX Gold open-interest contracts; direct PDF extraction and replay passed |

The six-variable closure is a milestone, not completion of Phase 3 as a whole.
The remaining admitted variables continue through the Phase 3 tracker. In
particular, L6-001 and L6-002 remain open because their qualitative evidence,
interpretation rules, and numeric encodings have not yet been jointly agreed.

The canonical Phase 3 tracker remains the authoritative status record:
[PHASE3-TRACKER.md](PHASE3-TRACKER.md).

## Verification note

The variable-specific live and parser tests pass. The obsolete Python
evidence-record prototype, its tests, and its rejected historical `-0.5`
record were removed so the active package no longer points to that path.
