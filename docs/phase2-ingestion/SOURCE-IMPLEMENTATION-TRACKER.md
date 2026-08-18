# Phase 2 Source / Implementation Tracker

**Purpose:** Single operational tracker for Phase 2 variable tasks.  
**Owner:** Grace updates the row when each variable task reaches review or closure.  
**Scope:** 44 ADMIT variables from the frozen Phase 1 master registry.  
**Conditional variables:** Excluded from production tracking until separately approved.

## Status values

`Not started` → `Proposed` → `Under review` → `Changes requested` → `Ready for approval` → `Complete` or `Deferred`

## Tracker

| ID | Variable | Owner | Primary source | Fallback source | Collection method | Reuse check | Collector | Status | Review notes | Final decision |
|---|---|---|---|---|---|---|---|---|---|---|
| L0-001 | Above-Ground Gold Stock |  |  |  |  |  |  | Not started |  |  |
| L0-002 | Central-Bank Gold Holdings |  |  |  |  |  |  | Not started |  |  |
| L0-003 | Gold ETF Holdings |  |  |  |  |  |  | Not started |  |  |
| L0-005 | Bar-and-Coin Investment Holdings / Demand |  |  |  |  |  |  | Not started |  |  |
| L0-006 | Gold Recycling Flow |  |  |  |  |  |  | Not started |  |  |
| L0-009 | Gold Lease Rates / Forward Rates |  |  |  |  |  |  | Not started |  |  |
| L1-001 | 10Y TIPS Real Yield |  |  |  |  |  |  | Not started |  |  |
| L1-002 | 5Y TIPS Real Yield |  |  |  |  |  |  | Not started |  |  |
| L1-003 | Forward Real Rates |  |  |  |  |  |  | Not started |  |  |
| L1-005 | Treasury Term Premium |  |  |  |  |  |  | Not started |  |  |
| L1-006 | Expected Policy Rate |  |  |  |  |  |  | Not started |  |  |
| L1-007 | 5Y5Y Forward Real Rate |  |  |  |  |  |  | Not started |  |  |
| L2-001 | DXY US Dollar Index |  |  |  |  |  |  | Not started |  |  |
| L2-002 | Broad Trade-Weighted Nominal US Dollar Index |  |  |  |  |  |  | Not started |  |  |
| L2-003 | USD/CNY |  |  |  |  |  |  | Not started |  |  |
| L3-001 | Fed Funds Futures Expected Policy Rate |  |  |  |  |  |  | Not started |  |  |
| L3-002 | OIS Forward Policy Curve |  |  |  |  |  |  | Not started |  |  |
| L3-003 | Expected Terminal Policy Rate |  |  |  |  |  |  | Not started |  |  |
| L3-004 | Probability Distribution of Future Policy Outcomes |  |  |  |  |  |  | Not started |  |  |
| L3-005 | FOMC Dot Plot Path |  |  |  |  |  |  | Not started |  |  |
| L3-006 | FOMC Statements / Forward-Guidance Signal |  |  |  |  |  |  | Not started |  |  |
| L4-001 | CPI Inflation Rate |  |  |  |  |  |  | Not started |  |  |
| L4-002 | Core PCE Inflation Rate |  |  |  |  |  |  | Not started |  |  |
| L4-003 | 5Y Breakeven Inflation |  |  |  |  |  |  | Not started |  |  |
| L4-004 | 10Y Breakeven Inflation |  |  |  |  |  |  | Not started |  |  |
| L4-006 | Fiscal Deficit / GDP |  |  |  |  |  |  | Not started |  |  |
| L4-007 | Debt / GDP |  |  |  |  |  |  | Not started |  |  |
| L4-008 | Interest Expense / Government Revenue |  |  |  |  |  |  | Not started |  |  |
| L4-009 | Treasury Maturity Structure |  |  |  |  |  |  | Not started |  |  |
| L5-001 | Monthly Official-Sector Gold Purchase Volume |  |  |  |  |  |  | Not started |  |  |
| L5-002 | Gold Share of Official Reserves |  |  |  |  |  |  | Not started |  |  |
| L5-003 | Reserve Composition Change / USD Share Change |  |  |  |  |  |  | Not started |  |  |
| L5-006 | Official-Sector Gold Sales / Lending |  |  |  |  |  |  | Not started |  |  |
| L6-001 | Active Conflict and Escalation Signal |  |  |  |  |  |  | Not started |  |  |
| L6-002 | Sanctions and Sovereign-Asset Freeze Events |  |  |  |  |  |  | Not started |  |  |
| L7-001 | Major Central-Bank Balance-Sheet Liquidity |  |  |  |  |  |  | Not started |  |  |
| L7-003 | Global Private Non-Financial Credit Growth |  |  |  |  |  |  | Not started |  |  |
| L7-004 | Credit-Spread Financial Stress |  |  |  |  |  |  | Not started |  |  |
| L7-005 | Treasury Repo Funding Stress |  |  |  |  |  |  | Not started |  |  |
| L8-001 | Gold ETF Net Flows |  |  |  |  |  |  | Not started |  |  |
| L9-001 | Shanghai Gold Exchange Premium/Discount |  |  |  |  |  |  | Not started |  |  |
| L9-004 | India Physical Gold Imports and Consumer Demand |  |  |  |  |  |  | Not started |  |  |
| L10-001 | COMEX Managed-Money Net Positioning |  |  |  |  |  |  | Not started |  |  |
| L10-002 | COMEX Gold Futures Open Interest |  |  |  |  |  |  | Not started |  |  |

## Closure rule

Grace completes the row after review, recommending `Complete` or `Deferred`. The final approver confirms the decision. Do not mark a variable `Complete` until the collector, validation, fallback behavior, and concise method documentation have been reviewed.
