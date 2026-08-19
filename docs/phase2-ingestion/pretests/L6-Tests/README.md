# L6 Data Ingestion & Engineering Summary Report

**Module:** Layer 6 – Geopolitical Risk & Financial Warfare Signals

**Target Application:** Gold Pricing & Quantitative Asset Allocation Model

**Status:** Completed & Validated

---

## 1. Executive Summary

During the **L6 Data Ingestion** phase, automated pipelines were designed, executed, and validated for two critical geopolitical and financial warfare datasets:

1. **`L6-001`: Geopolitical Risk (GPR) Index** — Text-based quantitative risk index measuring news-derived war, terrorism, and geopolitical tension events.
2. **`L6-002`: OFAC Specially Designated Nationals (SDN) List** — Real-time monitoring of U.S. sanctions, asset freezes, and financial warfare enforcement.

---

## 2. Variable L6-001: Geopolitical Risk (GPR) Index

### Overview & Data Origin

* **Primary Source:** Matteo Iacoviello (Federal Reserve Board) — [matteoiacoviello.com/gpr.htm](https://www.matteoiacoviello.com/gpr.htm)
* **Data Format:** Stata binary dataset (`.dta`).
* **Ingestion Logic:** Dynamic HTML scraping via `curl` combined with regular expressions to locate and download the daily `.dta` file into `./data/gpr/`. Parsed into Python via `pandas.read_stata()`.

### Engineered Features & Metrics

From the raw daily time series, five standardized quantitative features were generated for model ingestion:

| Feature Name | Type | Description / Formula | Utility in Gold Model |
| --- | --- | --- | --- |
| **`GPRD`** | Raw Metric | Daily Headline Geopolitical Risk Index | Measures baseline geopolitical risk level. |
| **`GPRD_Z30`** | Derived | 30-Day Rolling Z-score: $Z_{30} = \frac{\text{GPRD} - \mu_{30}}{\sigma_{30}}$ | Detects sudden, short-term geopolitical shock spikes. |
| **`GPRD_THREAT`** | Component | Sub-index isolating explicit geopolitical *threats* | Measures build-up, rhetoric, and rising tension. |
| **`GPRD_ACT`** | Component | Sub-index isolating physical geopolitical *acts* | Measures active kinetic warfare and executed attacks. |
| **`THREAT_ACT_RATIO`** | Derived | Threat-to-Act Ratio: $\frac{\text{GPRD\_THREAT}}{\text{GPRD\_ACT}}$ | Early warning indicator of escalating risk prior to action. |

---

## 3. Variable L6-002: OFAC Sanctions & Financial Warfare Signals

### Overview & Data Origin

* **Primary Source:** U.S. Department of the Treasury – Office of Foreign Assets Control (OFAC)
* **Endpoint:** `[https://www.treasury.gov/ofac/downloads/sdn.csv](https://www.treasury.gov/ofac/downloads/sdn.csv)`
* **Update Frequency:** Ad-hoc / Real-time updates (typically 2–4 releases per week).
* **Ingestion Logic:** Flat 12-column CSV download without native headers, fetched via `curl` into `./data/sanctions/sdn.csv`.

### Data Cleaning & Target Type Mapping

* **Legacy Representation:** Raw OFAC CSV files use legacy markers (`"-0-"`, `"0"`, `"-"`, or empty strings) to classify corporate entities and organizations.
* **Remapping Strategy:** Implemented a unified remapping dictionary to convert raw markers into standard labels: `Entity`, `Individual`, `Vessel`, `Aircraft`.

### Geopolitical Program & Country Exposure Metrics

To capture sanctions intensity across regions that directly impact central bank reserve diversification (such as de-dollarization and official gold buying), search criteria were expanded to evaluate both the primary `Program` column and full text string scans across `Remarks`:

| Geopolitical Category / Program | Search Parameters & Rules | Target Count | % Share |
| --- | --- | --- | --- |
| **Russia / Ukraine** | `RUSSIA`, `UKRAINE`, `UKRAINE-EO13660`, `UKRAINE-EO13661`, `UKRAINE-EO13662` | **6,837** | **35.6%** |
| **Iran** | `IRAN`, `IRAN-EO13846`, `IRAN-TRA`, `IRAN-HR` | **3,841** | **20.0%** |
| **Counter-Terrorism / SDGT** | `SDGT`, `TERRORISM` | **3,245** | **16.9%** |
| **China / Hong Kong** | `CMIC-EO`, `HK-EO13936`, `CHINA`, `HONG KONG` | **992** | **5.2%** |
| **Cyber Operations** | `CYBER2`, `CYBER-EO13694` | **365** | **1.9%** |

### Target Breakdown Summary

* **Total Active Sanctioned Targets:** **19,203**
* **Corporate Entities:** 9,850 (51.3%)
* **Individuals:** 7,490 (39.0%)
* **Vessels:** 1,518 (7.9%)
* **Aircraft:** 345 (1.8%)



---

## 4. Ingestion Directory Structure

```text
data/
├── gpr/
│   ├── gpr_daily_latest.dta        # Raw Stata binary downloaded from Fed portal
│   └── gpr_processed.csv           # Final dataset with Z-scores & ratios
└── sanctions/
    ├── sdn.csv                     # Raw OFAC SDN download
    └── sdn_parsed_summary.json     # Sanitized summary with program exposures

```

---