# Implementation Proposal: L0-002 — Central-Bank Gold Holdings

**Status:** Approved and closed as `Complete` (2026-08-19)

## 1. Objective
Establish a robust, automated pipeline to ingest monthly physical monetary gold reserves for a fixed panel of core sovereign and institutional entities (US, Euro Area/EZB, China, Japan, Switzerland, and the IMF) measured strictly in **metric tonnes**.

## 2. Primary Source & Architecture Pivot
* **Initial Evaluation:** Federal Reserve Economic Data (FRED) was initially tested via mnemonics (`GOLDREPUSM`, etc.), but rejected due to lack of continuous foreign central bank physical reserve series (FRED primarily hosts foreign *Reserves excluding Gold*).
* **Final Primary Source:** **World Gold Council official-holdings workbook**, downloaded through the shared WGC collector.
* **Source basis:** WGC-compiled official holdings, based primarily on IMF IFS statistics and identified with WGC source metadata.

## 3. Scope & Panel Definition
* **Entities Tracked:** `US` (USA), `EA` (EZB - European Central Bank), `CN` (China), `JP` (Japan), `CH` (Switzerland), and `IMF`.
* **Exclusions:** Rest of World (RoW) aggregates are intentionally excluded to keep the personal trade-advisor model focused on tier-one sovereign holders.

## 4. Fallback & Stale Policy
If the WGC workbook cannot be retrieved or parsed:
1. The pipeline returns `BLOCKED`, or carries forward a valid prior observation as `STALE` according to the shared WGC fallback policy.
2. Mock data is not an approved fallback.

## 5. Unit Conversion
* **Raw Unit:** Fine Troy Ounces ($1\text{ oz} = 31.1034768\text{ grams}$).
* **Conversion Factor:** $3.11034768 \times 10^{-5}$ metric tonnes per troy ounce.
