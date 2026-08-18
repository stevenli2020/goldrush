| ID | Variable | Open Source Proj? (Y/N) | Open Source Options | Free API Available? (Y/N) | Can Scrape? (Y/N) | Absolutely No Free Info? (Y/N) |
| --- | --- | --- | --- | --- | --- | --- |
| **L0-001** | Above-Ground Gold Stock | N | — | N | Y | N |
| **L0-002** | Central-Bank Gold Holdings | Y | `openbb`, `imf-data` | Y | N | N |
| **L0-003** | Gold ETF Holdings | Y | `olddatasets/gold-spot-downloader` | Y | N | N |
| **L0-005** | Bar-and-Coin Investment Holdings / Demand | N | — | N | Y | N |
| **L0-006** | Gold Recycling Flow | N | — | N | Y | N |
| **L0-009** | Gold Lease Rates / Forward Rates | N | — | N | Y | N |
| **L1-001** | 10Y TIPS Real Yield | Y | `fedfred`, `fredapi`, `openbb` | Y | N | N |
| **L1-002** | 5Y TIPS Real Yield | Y | `fedfred`, `fredapi`, `openbb` | Y | N | N |
| **L1-003** | Forward Real Rates | Y | `fedfred`, `fredapi` | Y | N | N |
| **L1-005** | Treasury Term Premium | Y | `fedfred`, `fredapi` | Y | N | N |
| **L1-006** | Expected Policy Rate | Y | `yfinance`, `fredapi` | Y | N | N |
| **L1-007** | 5Y5Y Forward Real Rate | Y | `fedfred`, `fredapi` | Y | N | N |
| **L2-001** | DXY US Dollar Index | Y | `yfinance`, `fredapi`, `openbb` | Y | N | N |
| **L2-002** | Broad Trade-Weighted Nominal US Dollar Index | Y | `fredapi`, `openbb` | Y | N | N |
| **L2-003** | USD/CNY | Y | `yfinance`, `fredapi` | Y | N | N |
| **L3-001** | Fed Funds Futures Expected Policy Rate | Y | `yfinance` | Y | N | N |
| **L3-002** | OIS Forward Policy Curve | N | — | Y (Derived/Public) | Y | N |
| **L3-003** | Expected Terminal Policy Rate | N | — | Y (Derived/Public) | Y | N |
| **L3-004** | Probability Distribution of Future Policy Outcomes | N | — | Y (CME FedWatch end) | Y | N |
| **L3-005** | FOMC Dot Plot Path | N | — | Y (Fed RSS/PDF) | Y | N |
| **L3-006** | FOMC Statements / Forward-Guidance Signal | Y | `feedparser`, LangChain loaders | Y | Y | N |
| **L4-001** | CPI Inflation Rate | Y | `fedfred`, `fredapi`, `openbb` | Y | N | N |
| **L4-002** | Core PCE Inflation Rate | Y | `fedfred`, `fredapi`, `openbb` | Y | N | N |
| **L4-003** | 5Y Breakeven Inflation | Y | `fedfred`, `fredapi` | Y | N | N |
| **L4-004** | 10Y Breakeven Inflation | Y | `fedfred`, `fredapi` | Y | N | N |
| **L4-006** | Fiscal Deficit / GDP | Y | `fredapi`, `openbb` | Y | N | N |
| **L4-007** | Debt / GDP | Y | `fredapi`, `openbb` | Y | N | N |
| **L4-008** | Interest Expense / Government Revenue | Y | `fredapi` | Y | N | N |
| **L4-009** | Treasury Maturity Structure | N | — | Y (TreasuryDirect API) | Y | N |
| **L5-001** | Monthly Official-Sector Gold Purchase Volume | Y | `openbb`, `imf-data` | Y | N | N |
| **L5-002** | Gold Share of Official Reserves | Y | `openbb`, `imf-data` | Y | N | N |
| **L5-003** | Reserve Composition Change / USD Share Change | Y | `openbb`, `imf-data` | Y | N | N |
| **L5-006** | Official-Sector Gold Sales / Lending | Y | `openbb`, `imf-data` | Y | N | N |
| **L6-001** | Active Conflict and Escalation Signal | Y | `gdelt` / GDELT wrappers | Y | N | N |
| **L6-002** | Sanctions and Sovereign-Asset Freeze Events | N | — | Y (OFAC API) | Y | N |
| **L7-001** | Major Central-Bank Balance-Sheet Liquidity | Y | `fredapi`, `openbb` | Y | N | N |
| **L7-003** | Global Private Non-Financial Credit Growth | Y | OpenBB / BIS API | Y | N | N |
| **L7-004** | Credit-Spread Financial Stress | Y | `fredapi`, `openbb` | Y | N | N |
| **L7-005** | Treasury Repo Funding Stress | Y | `fredapi` | Y | N | N |
| **L8-001** | Gold ETF Net Flows | Y | `olddatasets/gold-spot-downloader` | Y | Y | N |
| **L9-001** | Shanghai Gold Exchange Premium/Discount | N | — | N | Y | N |
| **L9-004** | India Physical Gold Imports and Consumer Demand | N | — | N | Y | N |
| **L10-001** | COMEX Managed-Money Net Positioning | Y | `cot_reports`, `cftc-cot` | Y | N | N |
| **L10-002** | COMEX Gold Futures Open Interest | Y | `cot_reports`, `yfinance` | Y | Y | N |