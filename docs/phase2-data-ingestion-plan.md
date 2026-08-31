# Phase 2 — Data Ingestion Start Plan

**Status:** Historical planning record — Phase 2 completed and handed off  
**Date:** 2026-08-17  
**Phase 1 SSOT:** `docs/phase1-registry/Phase1-master-registry.md`  
**Production scope:** 44 ADMIT variables only. The 30 CONDITIONAL / RESEARCH ONLY variables remain outside production ingestion.

This document records the original Phase 2 start plan and is retained for
historical traceability. The current authoritative status is maintained in
`docs/phase2-ingestion/SOURCE-IMPLEMENTATION-TRACKER.md`; the final approval
and handoff are recorded in `docs/phase2-ingestion/phase2-handoff.md`.

## 1. Ingestion contract

Every production observation must preserve:

- Variable ID and layer
- Observation timestamp
- Publication/release timestamp
- Retrieval timestamp
- Source and exact endpoint/file/series identifier
- Revision status and vintage where available
- Raw value and units
- Transformation and normalization applied
- Freshness/availability status
- Access and licensing constraints
- Validation result and anomaly notes

Raw observations must be retained separately from derived signals. Missing, revised, delayed, or inaccessible observations must be recorded explicitly; they must not be silently imputed or replaced with AI judgment.

## 2. Admitted-variable source inventory

The inventory below is the initial Phase 2 source-lock queue. “Source” records the candidate source from the Phase 1 admission record; it is not yet a production source approval. Source validation and endpoint locking are required before each variable enters the live pipeline.

| ID | Variable | Candidate source | Frequency | Accessibility | Horizons |
|---|---|---|---|---|---|
| L0-001 | Above-Ground Gold Stock | Gold-market stock estimates and institutional industry research; exact production source to be finalized during implementation. | Annual / irregular structural updates | Mixed / source-dependent | 1–3 years; 3–10 years — structural |
| L0-002 | Central-Bank Gold Holdings | Official central-bank disclosures / institutional gold-market datasets. | Monthly / quarterly / irregular depending on issuer | Mixed / largely public for disclosed holdings | 1–3 months; 1–3 years; 3–10 years — structural |
| L0-003 | Gold ETF Holdings | Fund-reported holdings / established market datasets. | Daily | Generally public / crawlable | 1–5 days; 1–3 months; 1–3 years — cyclical |
| L0-005 | Bar-and-Coin Investment Holdings / Demand | Institutional physical-demand datasets and national-market sources. | Quarterly / annual | Mixed | 1–3 months; 1–3 years; 3–10 years — cyclical / structural |
| L0-006 | Gold Recycling Flow | Institutional recycling estimates / physical-market data. | Quarterly / annual; some market indicators may be more frequent | Mixed | 1–3 months; 1–3 years — cyclical |
| L0-009 | Gold Lease Rates / Forward Rates | Gold lease, forward, swap and bullion-market data where reliably available. | Daily / market-dependent | Restricted / mixed | 1–5 days; 1–3 months; 1–3 years — cyclical / conditional |
| L1-001 | 10Y TIPS Real Yield | US Treasury / Federal Reserve market data. | Daily | Free / public | All four — cyclical / structural |
| L1-002 | 5Y TIPS Real Yield | US Treasury / institutional market data. | Daily | Free / public | 1–5 days; 1–3 months; 1–3 years — cyclical |
| L1-003 | Forward Real Rates | Derived from Treasury/institutional yield and inflation-linked market data. | Daily / derived | Free / derivable using public inputs | 1–3 months; 1–3 years; 3–10 years — structural / cyclical |
| L1-005 | Treasury Term Premium | Institutional/model-derived Treasury term-premium estimates. | Daily | Generally public for established model series | 1–3 months; 1–3 years — cyclical |
| L1-006 | Expected Policy Rate | Market-implied policy-rate data / official policy information. | Daily / event-driven | Generally public | 1–5 days; 1–3 months; 1–3 years — cyclical |
| L1-007 | 5Y5Y Forward Real Rate | Derived market-based real-rate data. | Daily | Free / derivable where inputs are public | 1–3 years; 3–10 years — structural / cyclical |
| L3-001 | Fed Funds Futures Expected Policy Rate | Fed funds futures market. | Intraday / daily | Mixed / market-data dependent | 1–5 days; 1–3 months; 1–3 years — event-driven / cyclical |
| L3-002 | OIS Forward Policy Curve | OIS market data. | Daily / intraday where available | Mixed / possibly paid | 1–5 days; 1–3 months; 1–3 years — cyclical |
| L3-003 | Expected Terminal Policy Rate | Market-implied curve / policy-market pricing. | Daily / event-driven | Mixed | 1–3 months; 1–3 years — cyclical |
| L3-004 | Probability Distribution of Future Policy Outcomes | Market-implied probabilities / futures and options where appropriate. | Daily / intraday | Mixed | 1–5 days; 1–3 months — event-driven |
| L3-005 | FOMC Dot Plot Path | Federal Reserve / FOMC primary publication. | Quarterly / FOMC schedule | Free / public | 1–3 months; 1–3 years — event-driven / cyclical |
| L3-006 | FOMC Statements / Forward-Guidance Signal | FOMC statements and official Federal Reserve communications. | Event-driven | Free / public | 1–5 days; 1–3 months — event-driven |
| L4-001 | CPI Inflation Rate | Official national inflation statistics. | Monthly | Free / public | 1–5 days; 1–3 months; 1–3 years — event-driven / cyclical |
| L4-002 | Core PCE Inflation Rate | Official PCE inflation statistics. | Monthly | Free / public | 1–3 months; 1–3 years — cyclical / structural |
| L4-003 | 5Y Breakeven Inflation | Treasury inflation-linked securities market data. | Daily | Free / public | 1–3 months; 1–3 years — cyclical |
| L4-004 | 10Y Breakeven Inflation | Treasury inflation-linked securities market data. | Daily | Free / public | 1–3 years; 3–10 years — structural / cyclical |
| L4-006 | Fiscal Deficit / GDP | Official fiscal statistics. | Monthly / quarterly / annual | Free / public | 1–3 years; 3–10 years — structural |
| L4-007 | Debt / GDP | Official sovereign fiscal data. | Quarterly / annual | Free / public | 1–3 years; 3–10 years — structural |
| L4-008 | Interest Expense / Government Revenue | Official government budget/fiscal reports. | Quarterly / annual | Free / public | 1–3 years; 3–10 years — structural |
| L4-009 | Treasury Maturity Structure | U.S. Treasury Fiscal Data Monthly Statement of the Public Debt, Table 3 Marketable Securities (`mspd_table_3_market`); completed measure is marketable debt maturing within one calendar year as a percentage of Total Marketable debt. | Monthly | Free / public | 1–3 months; 1–3 years — structural / cyclical |
| L5-001 | Monthly Official-Sector Gold Purchase Volume | Official central-bank disclosures and established institutional gold-market datasets. | Monthly / quarterly | Generally public / mixed for some institutions | 1–3 months; 1–3 years; 3–10 years — structural / cyclical |
| L5-002 | Gold Share of Official Reserves | Official reserve data / institutional reserve-composition datasets. | Monthly / quarterly / annual | Mixed / public for many major institutions | 1–3 years; 3–10 years — structural |
| L5-003 | Reserve Composition Change / USD Share Change | Official reserve-composition statistics and institutional reserve datasets. | Quarterly / annual | Mixed / some restricted components | 1–3 years; 3–10 years — structural |
| L5-006 | Official-Sector Gold Sales / Lending | Official disclosures and institutional gold-market reporting where transactions are observable. | Event-driven / monthly / quarterly | Mixed | 1–3 months; 1–3 years — cyclical / structural |
| L2-001 | DXY US Dollar Index | OpenBB `yfinance` provider, symbol `DX-Y.NYB`, daily OHLC with `dxy_close` as the canonical field; raw snapshots and source metadata manifests are preserved. | Daily finalized market observations; evolving current-day bars excluded. | Free public quotation source; unofficial and subject to provider availability. Carry-forward is marked `STALE` when needed. | 1–5 days; 1–3 months; 1–3 years — cyclical and transmission-driven; conditional over 3–10 years. |
| L2-002 | Broad Trade-Weighted Nominal US Dollar Index | Federal Reserve H.10 / FRED series DTWEXBGS: https://fred.stlouisfed.org/series/DTWEXBGS | Daily. | Free / public. | 1–5 days; 1–3 months; 1–3 years; 3–10 years — cyclical, structural, and regime-dependent. |
| L2-003 | USD/CNY | Federal Reserve H.10 exchange rates / FRED DEXCHUS; official Chinese foreign-exchange reference information where needed. | Daily. | Free / public for the Federal Reserve series. | 1–5 days; 1–3 months; 1–3 years — cyclical and regional; conditional over 3–10 years. |
| L7-001 | Major Central-Bank Balance-Sheet Liquidity | Federal Reserve H.4.1; ECB financial-statement data; PBoC and other major-central-bank official balance-sheet releases, subject to a documented aggregation method. | Weekly to monthly, depending on institution. | Free / public for major official series; some national series require additional processing. | 1–3 months; 1–3 years; 3–10 years — cyclical and structural regime conditions. |
| L7-003 | Global Private Non-Financial Credit Growth | BIS total credit statistics for the private non-financial sector: https://www.bis.org/statistics/tables_f.htm | Quarterly. | Free / public. | 1–3 years; 3–10 years — structural and cyclical; limited direct 1–5-day use. |
| L7-004 | Credit-Spread Financial Stress | Publicly documented corporate option-adjusted spread series such as Federal Reserve/FRED ICE BofA measures, supplemented only where methodology is transparent. | Daily. | Public series may be free; underlying index methodology/data can be vendor-controlled. | 1–5 days; 1–3 months; 1–3 years — event-driven and cyclical. |
| L7-005 | Treasury Repo Funding Stress | New York Federal Reserve SOFR, TGCR, and BGCR reference rates: https://www.newyorkfed.org/markets/reference-rates | Daily. | Free / public. | 1–5 days; 1–3 months — event-driven and conditional; 1–3 years for regime monitoring. |
| L6-001 | Active Conflict and Escalation Signal | ACLED or another documented conflict-event database; official statements and primary reporting from governments and international organizations; Caldara-Iacoviello GPR threat/acts data as a benchmark: https://www.matteoiacoviello.com/gpr.htm | Daily / event-driven. | Mixed / public for major sources; some structured event data may be paid or restricted. | 1–5 days; 1–3 months — event-driven; 1–3 years — conditional regime risk. |
| L6-002 | Sanctions and Sovereign-Asset Freeze Events | US Treasury OFAC sanctions programs and designations; UN Security Council sanctions; EU sanctions database and official national measures. | Event-driven / daily. | Free / public for major official sources. | 1–5 days; 1–3 months; 1–3 years — event-driven and structural; 3–10 years for persistent reserve-security regimes. |
| L9-001 | Shanghai Gold Exchange Premium/Discount | World Gold Council `gold_premiums` shared authenticated workbook target; exact `Chinese premiums-discounts` sheet and published five-day moving-average series. | Daily / market-day. | Shared cookie collection with manual authenticated download and canonical manifest fallback. | 1–5 days; 1–3 months; 1–3 years — cyclical and regional. |
| L9-004 | India Physical Gold Imports and Consumer Demand | Government of India Department of Commerce / DGCI&S trade statistics; World Gold Council and other transparent institutional demand datasets. Example official source: https://www.commerce.gov.in/ | Monthly / quarterly. | Free / public for official trade data; institutional demand estimates may be paid. | 1–3 months; 1–3 years — cyclical, seasonal, and structural. |
| L8-001 | Gold ETF Net Flows | World Gold Council gold ETF holdings and flows dataset; issuer filings and fund-reported holdings; SEC filings for US products. WGC methodology/data: https://www.gold.org/goldhub/data/gold-etfs-holdings-and-flows | Weekly / monthly, with some daily issuer information. | Mixed; public issuer data, with comprehensive institutional datasets potentially paid. | 1–5 days; 1–3 months; 1–3 years — cyclical and flow-driven. |
| L10-001 | COMEX Managed-Money Net Positioning | CFTC Disaggregated Commitments of Traders reports: https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm | Weekly. | Free / public. | 1–5 days; 1–3 months — cyclical and amplifier-driven. |
| L10-002 | COMEX Gold Futures Open Interest | CME Group daily volume/open-interest reports: https://www.cmegroup.com/market-data/volume-open-interest.html | Daily. | Free / public summary data; granular data may be paid. | 1–5 days; 1–3 months — amplifier and market-activity regime. |

## 3. Initial execution order

1. Lock free/public, high-frequency institutional series first: TIPS, FX, FOMC/OIS inputs, CPI/PCE, Treasury data, CFTC COT, CME open interest, SOFR, and ETF holdings/flows.
2. Build raw-observation storage with publication and retrieval timestamps before adding derived transformations.
3. Validate the source-locking open items in the Phase 1 master registry, especially L0-001, L0-009, L1-005, L7-001, and all variables with composite or vendor-dependent construction.
4. Add lower-frequency fiscal, official-sector, credit, and regional series with explicit release-lag and revision handling.
5. Keep all conditional variables in a separate research queue; do not promote them into production ingestion without a new admission decision.

## 4. Phase 2 acceptance gates

- Every admitted variable has a named, stable source and endpoint.
- Raw values can be retrieved reproducibly on the weekly schedule.
- Publication and retrieval timestamps are preserved.
- Revisions and missing observations are visible in the archive.
- Derived variables have documented formulas and units.
- Source failures produce a controlled status rather than fabricated data.
- No scoring or probability-engine implementation begins until the ingestion contract is operational for the required baseline variables.

## 5. Phase 1-to-Phase 2 handoff

The Phase 1 variable universe is frozen at 74 records: 44 admitted, 30 conditional, and 0 rejected. Phase 2 may validate and ingest the admitted universe, but it may not add variables, change layer ownership, alter layer weights, or promote conditional variables without the defined review process.
