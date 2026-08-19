# L0-003: Gold ETF Holdings Dataset Specification

## 1. Overview
This module ingests and standardizes physical gold holdings stock across global gold-backed ETFs.

## 2. Separation of Stock vs. Flow
- **Stock (L0-003):** Total metric tonnes held in vaults at point-in-time $T$.
- **Flows (L8-001):** Periodic net changes ($\Delta \text{stock}$) or monetary capital flows ($\$ \text{USD}$).

## 3. Data Integrity & Validation Rules
1. **Non-negativity:** Records with `holdings_tonnes < 0` are rejected.
2. **Date Alignment:** Dates parsed as `YYYY-MM-DD`. Duplicates per region are dropped.
3. **Abnormal Shifts:** Single-day percentage shifts $> 5\%$ flag `WARNING_ABNORMAL_CHANGE`.
4. **Stale Fallback:** Carry-forward mechanism activates when source feed is delayed, flagging `STALE`.