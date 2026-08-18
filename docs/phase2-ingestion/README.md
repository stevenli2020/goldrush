# Phase 2 — Data Ingestion Implementation

## Overview

This folder contains the complete Phase 2 data-ingestion implementation: shared collection libraries, per-variable configurations, operational manuals, and execution tracking.

**Scope:** 44 admitted variables from Phase 1 registry, organized by layer and variable ID.

---

## Folder Structure

```
docs/phase2-ingestion/
├── collectors/                          # Shared collection libraries
│   ├── wgc_scraper.py                  # WGC GoldHub HTML/JSON parser
│   ├── treasury_api_client.py           # Treasury/FRED API client
│   ├── usgs_fetch.py                    # USGS report retrieval
│   └── README.md                        # Collector library documentation
│
├── L0/ L1/ L2/ ... L10/                 # Layer folders
│   └── NNN/                             # Variable folder (e.g., 001, 002, 003)
│       ├── variable-name.md             # Implementation proposal
│       └── data/
│           ├── config.yaml              # Variable-specific configuration
│           ├── README.md                # Operational manual
│           ├── schema.json              # Data validation schema
│           ├── samples/                 # Example raw and processed data
│           └── archive/                 # Change history and notes
│
├── SOURCE-IMPLEMENTATION-TRACKER.md     # Admission gate status + source-lock order
├── phase2-handoff.md                    # Phase 2 completion checkpoint
└── README.md                            # This file
```

---

## Key Files

| File | Purpose |
|---|---|
| `collectors/README.md` | How each shared collector works; dependencies; usage patterns |
| `L*/NNN/variable-name.md` | **Implementation proposal**: sources, frequency, fields, units, validation, reuse checks |
| `L*/NNN/data/config.yaml` | **Configuration**: which collector to use, endpoints, parsing rules, validation bounds |
| `L*/NNN/data/README.md` | **Operational manual**: how to run, dependencies, logs, troubleshooting, maintenance |
| `L*/NNN/data/schema.json` | **Validation spec**: field definitions, types, units, required/optional, allowable bounds |
| `SOURCE-IMPLEMENTATION-TRACKER.md` | Status of each variable (PENDING / DRAFT / REVIEWED / LOCKED); execution order |
| `phase2-handoff.md` | Final freeze point: all 44 implementations approved and ready for ingestion |

---

## Workflow

### 1. Implementation
- Create `L*/*NN*/variable-name.md` with sources, collection method, fields, validation, reuse check (see L0-001 as template)
- Create `data/config.yaml` pointing to shared collector
- Create `data/schema.json` with field specs
- Create `data/README.md` with operational steps

### 2. Review
- Grace reviews `variable-name.md`
- Feedback → iterate
- Update SOURCE-IMPLEMENTATION-TRACKER.md status

### 3. Lock
- Approved implementation → status = "LOCKED"
- Config finalized; ready for Phase 2 execution

### 4. Execution (Phase 2 operations team)
- Read variable `README.md` and `config.yaml`
- Run collector with config
- Validate against `schema.json`
- Store observations in `/data/L*/L*_***/processed/`
- Update `archive/changelog.md` on changes

---

## Shared Collectors

If multiple variables use the same source (e.g., WGC for L0-001, L0-002, L0-003), they share one collector script but maintain separate per-variable `config.yaml`.

**Example:**
- L0-001, L0-002, L0-003 all use `collectors/wgc_scraper.py`
- Each has its own `data/config.yaml` specifying which fields to extract
- One code fix in `wgc_scraper.py` benefits all three

---

## Navigation

**By layer:** `L0/`, `L1/`, `L2/`, etc.

**By variable:** `L*/001/`, `L*/002/`, etc.

**By status:** See `SOURCE-IMPLEMENTATION-TRACKER.md` for overview of all 44 variables

**By collector dependency:** See `collectors/README.md` for which variables use each collector

---

## Key Handoff Points

1. **Phase 1 → Phase 2:** Variable registry frozen (44 admitted). Phase 2 implements ingestion for each.
2. **Implementation → Execution:** SOURCE-IMPLEMENTATION-TRACKER status = "LOCKED" means ready to ingest.
3. **Phase 2 → Phase 3:** `phase2-handoff.md` signed off; all 44 variables in production ingestion; raw observations archived.

---

## Acceptance Gates (per SOURCE-IMPLEMENTATION-TRACKER)

Before a variable moves to "LOCKED":
- ✓ Named, stable source and endpoint
- ✓ Programmatic collection method documented
- ✓ Fields, units, timestamps defined
- ✓ Validation rules and missing-data behavior explicit
- ✓ Reuse check against existing adapters completed
- ✓ Fallback source named (if applicable)
- ✓ Operational manual written

---

## Contact / Escalation

See individual `L*/NNN/data/README.md` for collector-specific issues.

See `SOURCE-IMPLEMENTATION-TRACKER.md` for ownership and review assignment.
