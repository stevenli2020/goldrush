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
| L0-001 | Above-Ground Gold Stock | Aiproxy | WGC GoldHub above-ground stock `.xlsx` (access confirmed) | Carry-forward (`STALE`); no live alternative | Manual annual workbook download; reproducible parser run with recorded dates | Standalone; no shared adapter | `docs/phase2-ingestion/L0/001/scripts/parse_above_ground.py` | Complete | Grace review 2026-08-18: all criteria met; test suite passes; live run confirmed. | Approved 2026-08-18; Complete |
| L0-002 | Central-Bank Gold Holdings | Assigned | IMF IFS via OpenBB (`IL::RGV_REVS`) | Carry-forward (`STALE`) up to 3 periods | Monthly collection via standalone IMF/OpenBB collector | Standalone | `docs/phase2-ingestion/L0/002/collector.py` | Complete | Grace review: all criteria met; tests pass 3/3; live evidence present. | Approved 2026-08-19; Complete |
| L0-003 | Gold ETF Holdings |  |  |  |  |  |  | Not done |  |  |
| L0-005 | Bar-and-Coin Investment Holdings / Demand | Chris | WGC GDT quarterly workbook; Gold Balance rows 20–23 + Bar and Coin rows 44–46 | Carry-forward (`STALE`); no live alternative | Manual quarterly download (Grace coordinates); standalone `parse_bar_and_coin.py`; SHA-256 integrity; append-only store | GDT workbook shared with L0-002, L0-003, L0-006, L8-001; parser is L0-005-specific | `docs/phase2-ingestion/L0/005/data/parse_bar_and_coin.py` | Complete | Grace re-review 2026-08-19: all criteria met; 20/20 tests; live run 82 PASS records. Scope: demand-flow only. | Approved 2026-08-19; Complete |
| L0-006 | Gold Recycling Flow |  |  |  |  |  |  | Not done |  |  |
| L0-009 | Gold Lease Rates / Forward Rates | Chris | 3-month CME-derived GILR proxy: SOFR3M (FRED, free CSV) minus CME COMEX gold futures implied forward rate (Nasdaq Data Link `CHRIS/CME_GC1`/`GC2`, free tier); % p.a.; daily | Carry-forward (`STALE`) up to 5 trading days; `BLOCKED` beyond 5; no live public alternative | Automated daily fetch of SOFR3M and CME settlement CSVs; derived computation; manual download fallback (`--manual` flag) | Standalone; shares CME exchange as data source with L10-002 but different series | `docs/phase2-ingestion/L0/009/data/parse_gilr.py` | Not done — DRAFT v2 submitted for Grace review | v1 2026-08-18: 7 rework items (source contradiction, methodology gaps, excessive fields/blockers). v2 2026-08-19: all 7 items resolved. Parser built; 25/25 tests passing; live manual-mode run 2026-08-19T08:24:17Z produced FLAG (roll proximity, expected). 2 blockers remain open: B1 (Nasdaq ToS) and B4 (automated PASS run pending network access). | Pending Grace review of v2 |
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
