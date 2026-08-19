# Phase 2 Source / Implementation Tracker

**Purpose:** Single operational tracker for Phase 2 variable tasks.  
**Owner:** Grace updates the row when each variable task reaches review or closure.  
**Scope:** 44 ADMIT variables from the frozen Phase 1 master registry.  
**Conditional variables:** Excluded from production tracking until separately approved.

## Status values

`Not done` -> `Complete` or `Deferred`

## Tracker

| ID | Variable | Owner | Primary source | Fallback source | Collection method | Reuse check | Collector | Status | Review notes | Final decision |
|---|---|---|---|---|---|---|---|---|---|---|
| L0-001 | Above-Ground Gold Stock | Aiproxy | WGC GoldHub above-ground stock `.xlsx` (access confirmed) | Carry-forward of last WGC observation (`STALE`); no live alternative | Manual annual workbook download by Aiproxy in mid-February, followed by reproducible parser run with recorded download/publication dates | No existing adapter; local collector is intentionally standalone until a shared WGC adapter is needed | `docs/phase2-ingestion/L0/001/scripts/parse_above_ground.py` | Complete | Grace review 2026-08-18: fields, tonnes units, annual observation timing, provenance, raw preservation, fallback, freshness rules, validation, and documentation reviewed. Test suite passes (3 tests); supplied workbook processed successfully with explicit dates. WGC access confirmed; methodology note archived; owner/operator recorded as Aiproxy. | Approved by final approver 2026-08-18; Complete |
| L0-002 | Central-Bank Gold Holdings | Assigned | IMF IFS via OpenBB (`IL::RGV_REVS`) | Carry-forward of the latest valid observation for up to 3 periods, flagged `STALE` | Monthly collection via `docs/phase2-ingestion/L0/002/collector.py` | No existing adapter; standalone IMF/OpenBB collector for the fixed six-entity panel | `docs/phase2-ingestion/L0/002/collector.py` | Complete | Grace review: IMF/OpenBB source, metric-tonne conversion, fixed panel, stale fallback, raw payload preservation, audit logging, live evidence bundle, and offline test suite reviewed. Tests pass 3/3; live evidence bundle is present; EA lag is correctly marked `STALE`. | Approved by final approver 2026-08-19; Complete |
| L0-003 | Gold ETF Holdings | Aiproxy | World Gold Council Gold ETF holdings dataset (`ETF_Flows_2026-08-04_1202.xlsx`) | Carry-forward of latest valid observation, flagged `STALE`; no equivalent live alternative identified | Manual WGC workbook download followed by reproducible XLSX parser run with recorded publication/download dates and SHA-256 | Reuses L0-005’s manual-download, provenance, hashing, validation, fallback, and test conventions; separate parser because ETF holdings fields and workbook extraction differ from bar-and-coin demand | `docs/phase2-ingestion/L0/003/parse_etf_holding.py` via `run_ingest.py` | Complete | Grace review: XLSX parser, live evidence, source/output paths, schema alignment, fallback, validation, and documentation reviewed. Live run produced 281 records (237 PASS, 44 FLAG, 0 FAIL); tests pass 3/3. | Approved by final approver 2026-08-19; Complete |
| L0-005 | Bar-and-Coin Investment Holdings / Demand | Chris | WGC Gold Demand Trends quarterly workbook `GDT_Tables_Q{Q}'{YY}_EN.xlsx`; Gold Balance sheet rows 20–23 (global total + sub-components, annual only) and Bar and Coin sheet rows 44–46 (country totals + world total, annual + quarterly) | Carry-forward (`STALE`); no live global alternative | Manual quarterly download by Grace (shared-workbook coordinator); standalone parser `parse_bar_and_coin.py`; SHA-256 integrity check; `--publication-date` supplied by operator at run time; append-only processed store | GDT workbook shared with L0-002, L0-003, L0-006, L8-001 — one download per quarter coordinated by Grace; `parse_bar_and_coin.py` is L0-005-specific | `docs/phase2-ingestion/L0/005/data/parse_bar_and_coin.py` | Complete | Grace re-review 2026-08-19: parser, schema, samples, fallback, validation, documentation, 20/20 tests, and live evidence reviewed. Live run produced 82 records (16 annual, 66 quarterly), 82 PASS, 0 FLAG, 0 FAIL. Scope is demand-flow only; no holdings stock constructed. | Approved by final approver 2026-08-19; Complete |
| L0-006 | Gold Recycling Flow |  |  |  |  |  |  | Not done |  |  |
| L0-009 | Gold Lease Rates / Forward Rates | Chris | 3-month CME-derived GILR proxy: SOFR3M (FRED `SOFR3M`, free CSV) minus CME COMEX gold futures implied forward rate (Nasdaq Data Link `CHRIS/CME_GC1` and `CHRIS/CME_GC2`, free tier); % p.a.; daily | Carry-forward (`STALE`) up to 5 trading days; `BLOCKED` beyond 5 days; no live public alternative | Automated daily fetch of SOFR3M CSV from FRED and CME GC1/GC2 CSVs from Nasdaq Data Link; parser computes and validates derived GILR; manual CME settlement download acceptable fallback if automated retrieval unavailable | No existing collector; standalone; shares CME exchange as data source with L10-002 but different series entirely | `docs/phase2-ingestion/L0/009/data/parse_gilr.py` (not yet built) | Not done — DRAFT v2 submitted for Grace review | v1 review 2026-08-19: contradictory source definition, LBMA named as primary despite not being available, unlicensed-terminal gate, too many optional fields, excessive blocker list. v2 2026-08-19: production variable renamed to `3M GILR — CME-derived proxy`; CME path locked as sole primary; LBMA/licensed terminal references moved to optional future upgrade; calculation methodology made exact (contract selection rule, formula, day-count, SOFR vintage alignment); fields narrowed to core set; blocker list reduced to 4 (B1–B4); FRED API key and licensed terminal removed as blockers. | Pending Grace review of v2 |
| L1-001 | 10Y TIPS Real Yield |  |  |  |  |  |  | Not done |  |  |
| L1-002 | 5Y TIPS Real Yield |  |  |  |  |  |  | Not done |  |  |
| L1-003 | Forward Real Rates |  |  |  |  |  |  | Not done |  |  |
| L1-005 | Treasury Term Premium |  |  |  |  |  |  | Not done |  |  |
| L1-006 | Expected Policy Rate |  |  |  |  |  |  | Not done |  |  |
| L1-007 | 5Y5Y Forward Real Rate |  |  |  |  |  |  | Not done |  |  |
| L2-001 | DXY US Dollar Index |  |  |  |  |  |  | Not done |  |  |
| L2-002 | Broad Trade-Weighted Nominal US Dollar Index |  |  |  |  |  |  | Not done |  |  |
| L2-003 | USD/CNY |  |  |  |  |  |  | Not done |  |  |
| L3-001 | Fed Funds Futures Expected Policy Rate |  |  |  |  |  |  | Not done |  |  |
| L3-002 | OIS Forward Policy Curve |  |  |  |  |  |  | Not done |  |  |
| L3-003 | Expected Terminal Policy Rate |  |  |  |  |  |  | Not done |  |  |
| L3-004 | Probability Distribution of Future Policy Outcomes |  |  |  |  |  |  | Not done |  |  |
| L3-005 | FOMC Dot Plot Path |  |  |  |  |  |  | Not done |  |  |
| L3-006 | FOMC Statements / Forward-Guidance Signal |  |  |  |  |  |  | Not done |  |  |
| L4-001 | CPI Inflation Rate |  |  |  |  |  |  | Not done |  |  |
| L4-002 | Core PCE Inflation Rate |  |  |  |  |  |  | Not done |  |  |
| L4-003 | 5Y Breakeven Inflation |  |  |  |  |  |  | Not done |  |  |
| L4-004 | 10Y Breakeven Inflation |  |  |  |  |  |  | Not done |  |  |
| L4-006 | Fiscal Deficit / GDP |  |  |  |  |  |  | Not done |  |  |
| L4-007 | Debt / GDP |  |  |  |  |  |  | Not done |  |  |
| L4-008 | Interest Expense / Government Revenue |  |  |  |  |  |  | Not done |  |  |
| L4-009 | Treasury Maturity Structure |  |  |  |  |  |  | Not done |  |  |
| L5-001 | Monthly Official-Sector Gold Purchase Volume |  |  |  |  |  |  | Not done |  |  |
| L5-002 | Gold Share of Official Reserves |  |  |  |  |  |  | Not done |  |  |
| L5-003 | Reserve Composition Change / USD Share Change |  |  |  |  |  |  | Not done |  |  |
| L5-006 | Official-Sector Gold Sales / Lending |  |  |  |  |  |  | Not done |  |  |
| L6-001 | Active Conflict and Escalation Signal |  |  |  |  |  |  | Not done |  |  |
| L6-002 | Sanctions and Sovereign-Asset Freeze Events |  |  |  |  |  |  | Not done |  |  |
| L7-001 | Major Central-Bank Balance-Sheet Liquidity |  |  |  |  |  |  | Not done |  |  |
| L7-003 | Global Private Non-Financial Credit Growth |  |  |  |  |  |  | Not done |  |  |
| L7-004 | Credit-Spread Financial Stress |  |  |  |  |  |  | Not done |  |  |
| L7-005 | Treasury Repo Funding Stress |  |  |  |  |  |  | Not done |  |  |
| L8-001 | Gold ETF Net Flows |  |  |  |  |  |  | Not done |  |  |
| L9-001 | Shanghai Gold Exchange Premium/Discount |  |  |  |  |  |  | Not done |  |  |
| L9-004 | India Physical Gold Imports and Consumer Demand |  |  |  |  |  |  | Not done |  |  |
| L10-001 | COMEX Managed-Money Net Positioning |  |  |  |  |  |  | Not done |  |  |
| L10-002 | COMEX Gold Futures Open Interest |  |  |  |  |  |  | Not done |  |  |

## Closure rule

Grace completes the row after review, recommending `Complete` or `Deferred`. The final approver confirms the decision. Do not mark a variable `Complete` until the collector, validation, fallback behavior, and concise method documentation have been reviewed.
