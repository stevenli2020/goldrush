# Data Ingestion Summary Report: L9 Pipeline Series

---

## Executive Overview

This report presents the consolidated architecture, operational specifications, and ingestion results for the **L9 Data Ingestion Pipeline Series**:

1. **L9-001**: **Shanghai Gold Exchange (SGE) Premium / Discount Data Pipeline** — High-frequency price spread & physical tightness indicator for Mainland China.
2. **L9-004**: **India Physical Gold Ingestion Pipeline** — Quarterly volume, supply channel, and price dynamics ETL for India.

---

## 1. System Architectural Overview

| Component / Attribute | **Pipeline L9-001** | **Pipeline L9-004** |
| --- | --- | --- |
| **Pipeline Target** | SGE Domestic Gold Premium / Discount | India Physical Gold Supply, Demand & Price |
| **Geography / Market** | China (Domestic vs. International) | India (Domestic Market) |
| **Primary Data Source** | SGE Spot (Au99.99), LBMA Fix, FX Rates | `data/gold-demand-trends/GDT_Tables_Q2'26_EN.xlsx` |
| **Primary Metric Units** | USD / troy oz, USD/CNY Rate, Spread (%) | Tonnes ($\text{t}$), INR per $10\text{g}$ |
| **Ingestion Cadence** | Daily / Real-Time High-Frequency | Quarterly (WGC GDT Release Cycle) |
| **Primary Utility** | Regional physical liquidity & tightness gauge | Import dependence, supply-chain & demand tracking |

---

## 2. Pipeline L9-001 Specifications: SGE Premium / Discount

### Core Objective & Analytical Value

Pipeline **L9-001** tracks the price differential between gold traded domestically on the Shanghai Gold Exchange (SGE) and global spot benchmark prices (LBMA PM Fix / Loco London). It serves as a real-time proxy for Chinese domestic physical gold demand tightness, import quota restrictions, and onshore currency liquidity.

### Mathematical & ETL Formulas

* **Currency Conversion**: Converts RMB/gram to USD/troy ounce using real-time USD/CNY exchange rates:

$$P_{\text{SGE (USD/oz)}} = \left( \frac{P_{\text{SGE (RMB/g)}} \times 31.1034768}{\text{USD/CNY Rate}} \right)$$


* **Absolute Spread**:

$$\Delta P = P_{\text{SGE (USD/oz)}} - P_{\text{Global (USD/oz)}}$$


* **Percentage Premium / Discount**:

$$\text{Premium (\%)} = \left( \frac{P_{\text{SGE (USD/oz)}} - P_{\text{Global (USD/oz)}}}{P_{\text{Global (USD/oz)}}} \right) \times 100$$



---

## 3. Pipeline L9-004 Specifications & Ingestion Results: India Physical Market

### Operational Scope

Pipeline **L9-004** extracts and standardizes multi-sheet quarterly time-series data from `data/gold-demand-trends/GDT_Tables_Q2'26_EN.xlsx` across four dedicated sheets:

* **`India Supply`**: Gross imports, doré imports, net imports, scrap recycling, domestic/other.
* **`Jewellery`**: Domestic jewellery consumer demand.
* **`Bar and Coin`**: Domestic physical investment demand.
* **`Gold Prices`**: Domestic gold price per $10\text{g}$ in INR.

### Key Derived Ratios

* **Import Coverage Ratio (%)**:

$$\text{Import Coverage (\%)} = \left( \frac{\text{Gross Imports (t)}}{\text{Total Consumer Demand (t)}} \right) \times 100$$


* **Doré Import Share (%)**:

$$\text{Doré Share (\%)} = \left( \frac{\text{Doré Imports (t)}}{\text{Gross Imports (t)}} \right) \times 100$$



---

### Recent Quarters Ingestion Breakdown (L9-004)

#### Comparative Analysis: Q1 2026 vs. Q2 2026

| Metric | Q1 2026 | Q2 2026 | Change (%) / Trend |
| --- | --- | --- | --- |
| **Gross Imports** | $209.36\text{ t}$ | $98.39\text{ t}$ | $-53.00\%$ |
| **Doré Imports** | $69.63\text{ t}$ | $64.50\text{ t}$ | $-7.37\%$ |
| **Scrap / Recycling** | $31.22\text{ t}$ | $19.23\text{ t}$ | $-38.39\%$ |
| **Total Domestic Supply** | $244.06\text{ t}$ | $120.16\text{ t}$ | $-50.77\%$ |
| **Jewellery Demand** | $66.13\text{ t}$ | $75.10\text{ t}$ | $+13.57\%$ |
| **Bar & Coin Demand** | $62.30\text{ t}$ | $50.25\text{ t}$ | $-19.34\%$ |
| **Total Consumer Demand** | $128.42\text{ t}$ | $125.35\text{ t}$ | $-2.39\%$ |
| **Domestic Price (INR / 10g)** | ₹$151,105.45$ | ₹$150,744.88$ | $-0.24\%$ |
| **Import Coverage Ratio** | $163.02\%$ | $78.50\%$ | $-84.52\text{ pp}$ |
| **Doré Import Share** | $33.26\%$ | $65.55\%$ | $+32.29\text{ pp}$ |

---

### Multi-Quarter Ingested Series (Recent 5 Quarters)

| Quarter | Gross Imports (t) | Net Imports (t) | Jewellery Demand (t) | Total Demand (t) | Gold Price (INR/10g) | Import Coverage (%) | Doré Share (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Q2 2025** | $128.66$ | $127.38$ | $88.75$ | $134.88$ | ₹$94,876.00$ | $95.39\%$ | $29.82\%$ |
| **Q3 2025** | $212.70$ | $211.87$ | $125.00$ | $216.65$ | ₹$102,287.09$ | $98.18\%$ | $33.54\%$ |
| **Q4 2025** | $232.29$ | $231.46$ | $145.35$ | $241.34$ | ₹$125,741.67$ | $96.25\%$ | $35.80\%$ |
| **Q1 2026** | $209.36$ | $209.03$ | $66.13$ | $128.42$ | ₹$151,105.45$ | $163.02\%$ | $33.26\%$ |
| **Q2 2026** | $98.39$ | $98.06$ | $75.10$ | $125.35$ | ₹$150,744.88$ | $78.50\%$ | $65.55\%$ |

---

## 4. Pipeline Execution & System Validation

* **Target Directory Resolution**: Path successfully configured to `data/gold-demand-trends/GDT_Tables_Q2'26_EN.xlsx` with relative path fallback routines.
* **Data Completeness**: $58\text{ quarters}$ ingested ($Q1\text{ 2012} \rightarrow Q2\text{ 2026}$); $0$ missing or null entries.
* **Execution Time**: Ingestion, normalization, and indicator calculation executed in $<0.05\text{ seconds}$.
* **Validation Status**: **PASSED**.