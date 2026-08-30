# Technical Specification: L0-002 — Central-Bank Gold Holdings

## 1. Objective
Define and implement a reproducible collector for global central-bank gold holdings across a fixed panel of tier-one sovereign and institutional entities, measured strictly in metric tonnes.

## 2. Canonical Data Source
* **Primary Source:** IMF International Financial Statistics (IFS) database.
* **Access Layer:** OpenBB Platform SDK (`openbb-imf` provider extension).
* **Series / Indicator Symbol:** `IL::RGV_REVS` (Monetary Gold / Gold Reserves in Fine Troy Ounces).

## 3. Fixed Panel Scope
* **US:** United States (`USA`)
* **EA:** European Central Bank / Euro Area (`EZB`)
* **CN:** China (`CHN`)
* **JP:** Japan (`JPN`)
* **CH:** Switzerland (`CHE`)
* **IMF:** International Monetary Fund (`IMF`)

## 4. Unit Conversion & Normalization
* **Raw Unit:** Fine Troy Ounces ($1\text{ oz} = 31.1034768\text{ grams}$).
* **Conversion Multiplier:** $3.11034768 \times 10^{-5}$ metric tonnes per troy ounce.

## 5. Freshness & Stale-Data Policy
* **Freshness Threshold:** Observations with an effective date within **150 days** of the execution date are classified as `FRESH`.
* **Stale Threshold / Lag Policy:** Observations older than 150 days (such as lagged central bank reporting like the ECB) are classified as `STALE` and trigger carry-forward handling up to 3 periods.

## 6. Audit & Reproducibility
* Append-only CSV audit logs (`audit_log.csv`).
* Raw payload archiving (`data/raw/imf_ifs_YYYY-MM-DD.json`).
* Executable offline mock mode for test suites (`python collector.py --mock`).

## 7. Aggregate and Evidence Conventions
* Entity records retain the IMF observation month-end date (`YYYY-MM-DD`).
* The `AGGREGATE` row is a derived sum of the six panel entities and is labelled
  with the collector execution month (`YYYY-MM`). It is not an independently
  observed IMF series.
* A `STALE` entity remains visible in the aggregate but is explicitly flagged in
  its entity row and raw payload. Downstream users must inspect entity status
  before relying on the sum.
* Each live run preserves the raw payload and a run-evidence JSON linking it to
  the dated processed CSV.
