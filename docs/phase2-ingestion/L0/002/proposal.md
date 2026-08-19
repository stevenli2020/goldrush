# Implementation Proposal: L0-002 — Central-Bank Gold Holdings

**Status:** Approved and closed as `Complete` (2026-08-19)

## 1. Objective
Establish a robust, automated pipeline to ingest monthly physical monetary gold reserves for a fixed panel of core sovereign and institutional entities (US, Euro Area/EZB, China, Japan, Switzerland, and the IMF) measured strictly in **metric tonnes**.

## 2. Primary Source & Architecture Pivot
* **Initial Evaluation:** Federal Reserve Economic Data (FRED) was initially tested via mnemonics (`GOLDREPUSM`, etc.), but rejected due to lack of continuous foreign central bank physical reserve series (FRED primarily hosts foreign *Reserves excluding Gold*).
* **Final Primary Source:** **IMF International Financial Statistics (IFS)** accessed via the OpenBB Platform SDK (`openbb-imf`). 
* **Series Identifier:** `IL::RGV_REVS` (Monetary Gold holdings in troy ounces).

## 3. Scope & Panel Definition
* **Entities Tracked:** `US` (USA), `EA` (EZB - European Central Bank), `CN` (China), `JP` (Japan), `CH` (Switzerland), and `IMF`.
* **Exclusions:** Rest of World (RoW) aggregates are intentionally excluded to keep the personal trade-advisor model focused on tier-one sovereign holders.

## 4. Fallback & Stale Policy
If the primary IMF API query fails or is delayed:
1. The collector flags the observation record as `STALE`.
2. The pipeline carries forward the last successfully ingested valid monthly observation for up to 3 periods before throwing a hard operational alert.

## 5. Unit Conversion
* **Raw Unit:** Fine Troy Ounces ($1\text{ oz} = 31.1034768\text{ grams}$).
* **Conversion Factor:** $3.11034768 \times 10^{-5}$ metric tonnes per troy ounce.
