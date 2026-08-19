# L0-009 — Gold Lease Rates / Forward Rates: Implementation Proposal

**Variable ID:** L0-009  
**Layer:** L0 — Gold's Stock/Flow Monetary Architecture  
**Status:** ADMIT (Phase 1 approval; production contingent on stable verified source)  
**Owner:** Chris  
**Proposal version:** v2 (revised per Grace review 2026-08-19)  
**Date:** 2026-08-19

---

## 1. Causal Mechanism

Gold lease rates measure the cost of borrowing physical gold. They are a market signal of bullion-market tightness, physical-stock mobility, and bullion-bank financing conditions — distinct from L1 real-yield opportunity cost, which measures the competing return on financial assets.

Rising lease rates signal that physical gold is harder to borrow. Falling rates indicate easier physical financing. Relevant at 1–5 day, 1–3 month, and 1–3 year horizons.

**Mandatory source-locking note (Phase 1 registry):** Production use is contingent on a stable, verified source being confirmed.

---

## 2. Production Variable

**Name:** 3-month Gold Implied Lease Rate — CME-derived proxy (GILR-CME)

**Definition:**

```
GILR-CME(3M) = SOFR3M − CME_implied_forward_rate(3M)
```

**This is a derived proxy, not a directly observed lease rate.** It approximates the gold lease rate using exchange-traded futures prices. The result incorporates futures basis, convenience yield, storage costs, and credit effects from the futures market structure in addition to the lending rate. It is not equivalent to an OTC bullion-bank lease quote or the discontinued GOFO.

**Why this approach:**
- GOFO (Gold Forward Offered Rate) was discontinued by LBMA in January 2015; no replacement public series exists
- Direct OTC lease rates (central bank gold lending, bullion bank bilateral quotes) are not publicly available
- LBMA gold forward rates are not published as a free standalone series
- CME COMEX gold futures are exchange-traded, daily-settled, transparent, and free via public endpoints
- SOFR3M is published daily by the Federal Reserve via FRED at no cost
- The CME-derived proxy is a standard industry approximation used when direct rates are unavailable

**Future upgrade (non-blocking):** If a Bloomberg terminal (`GOLDLEAS Index`) or Refinitiv feed (`XAUFOR=`) becomes available, the licensed series would replace the CME-derived proxy as primary. This is an optional enhancement; it does not block current implementation. Document the switch in `changelog.md` if it occurs.

---

## 3. Tenor, Currency, Units, Quotation Convention

| Attribute | Value |
|---|---|
| Tenor | 3-month (3M) — targeting ~90 calendar days between contracts |
| Currency | USD |
| Units | Percentage per annum (% p.a.) |
| Day count | Actual/360 (LBMA OTC convention; applied consistently to both inputs) |
| Sign convention | Positive = gold lending costs positive (normal contango); Negative = backwardation (tight physical market; economically valid in stress conditions, not a data error) |

---

## 4. Primary Source and Collection Method

**Two inputs; one collection route each.**

### Input 1 — SOFR3M (Federal Reserve / FRED)

| Attribute | Value |
|---|---|
| Series | `SOFR3M` — 3-month term SOFR |
| Endpoint | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR3M` |
| Access | Free; public; no API key required for CSV download |
| Format | CSV; date and value columns |
| Frequency | Daily (business days) |
| Publication lag | Published T+1 (previous business day's rate available next morning) |
| FRED API key | Optional; not required for CSV endpoint; register free if rate-limiting becomes an issue |

### Input 2 — CME COMEX Gold Futures Settlements

| Attribute | Value |
|---|---|
| Series | Front-month (`GC1`) and second-month (`GC2`) COMEX gold futures daily settlements |
| Primary endpoint | Nasdaq Data Link `CHRIS/CME_GC1` and `CHRIS/CME_GC2` — free tier; no key required for public datasets |
| URL pattern | `https://data.nasdaq.com/api/v3/datasets/CHRIS/CME_GC1.csv` |
| Manual fallback | CME daily settlement report from CME website; operator downloads and places in `raw/YYYY-MM-DD/cme_gc_settlement.csv` |
| Format | CSV; date, settle, expiry columns |
| Frequency | Daily (CME trading days; not all calendar days) |
| Settlement time | ~14:00 ET |

### Collection procedure (automated)

```
1. Fetch SOFR3M CSV from FRED (T-1 vintage; latest available)
2. Fetch GC1 and GC2 settlement CSVs from Nasdaq Data Link
3. Select contract pair (see Section 5)
4. Compute GILR-CME (see Section 5)
5. Validate
6. Append to processed store
```

### Manual fallback procedure

If automated retrieval fails on a given day:

```
1. Download SOFR3M CSV from FRED website manually
2. Download CME settlement report from CME website:
   https://www.cmegroup.com/market-data/reports/daily-settlement.html
   (Filter: COMEX, Gold Futures)
3. Save to raw/YYYY-MM-DD/sofr3m.csv and raw/YYYY-MM-DD/cme_gc_settlement.csv
4. Run parser with --manual flag
```

---

## 5. Exact Calculation — Contract Selection and Formula

### Contract selection rule

The parser selects the contract pair on each observation date as follows:

1. **Front contract:** The nearest active COMEX gold futures contract with expiry > 5 calendar days from observation date (avoids delivery-period distortion)
2. **Far contract:** The active contract with expiry closest to 90 calendar days after the front contract expiry, within the range 60–120 calendar days from the front contract expiry

COMEX gold contracts expire on the third-to-last business day of their delivery month. Standard delivery months: February, April, June, August, October, December. The parser must resolve contract codes to actual expiry dates and select accordingly.

If no contract pair falls within the 60–120 day window, the run halts with `availability_status: BLOCKED` and logs the gap.

### Implied forward rate calculation

```
days = actual calendar days between front expiry and far expiry

CME_implied_forward_rate (% p.a.) =
    ((far_settlement / front_settlement) − 1) × (360 / days) × 100
```

### GILR-CME calculation

```
GILR_CME (% p.a.) = SOFR3M (% p.a.) − CME_implied_forward_rate (% p.a.)
```

### SOFR vintage alignment

SOFR3M for observation date T uses the value published on T (which reflects T-1 fixing). If T-day SOFR3M is not yet published when the parser runs, use T-1 published value and record `sofr_vintage_date` accordingly.

### Limitations of this proxy

- The CME-implied forward rate reflects futures market pricing, not OTC dealer quotes
- Futures basis, convenience yield, storage costs, and exchange-specific credit effects are embedded in the result
- The proxy may diverge from direct OTC lease rates during periods of futures market stress or around contract roll dates
- Contract roll dates (typically 5–10 days before expiry) may introduce transient discontinuities; these are flagged, not rejected

---

## 6. Fallback Source

No live public alternative exists at equivalent frequency and definition. Fallback is carry-forward only.

| Scenario | `availability_status` | Action |
|---|---|---|
| Automated retrieval fails; manual inputs present | `AVAILABLE` | Run parser with `--manual` flag |
| No inputs for 1–5 trading days | `STALE` | Carry forward last valid observation; do not use in scoring without operator approval |
| No inputs for > 5 trading days | `BLOCKED` | Stop ingestion; escalate to Grace |
| SOFR3M unavailable; SOFR overnight compounded substitute used | `INCOMPLETE` | Log substitution in `anomaly_notes` |

---

## 7. Frequency and Timestamps

| Attribute | Value |
|---|---|
| Frequency | Daily (CME trading days only) |
| `observation_date` | Date of CME settlement used as far-leg input |
| `sofr_vintage_date` | Date of SOFR3M observation used (T or T-1) |
| `ingested_at` | UTC timestamp of parser run |
| Weekend / holiday | No record produced; gap is expected and not flagged |

---

## 8. Collector Location

```
docs/phase2-ingestion/L0/009/
├── gold-lease-forward-rates.md        # This document
└── data/
    ├── parse_gilr.py                  # Standalone collector + parser
    ├── config.yaml
    ├── schema.json
    ├── README.md
    ├── raw/                           # Daily raw inputs (append; do not delete)
    │   └── YYYY-MM-DD/
    │       ├── sofr3m.csv
    │       └── cme_gc_settlement.csv
    ├── processed/
    │   └── L0_009_observations.csv
    ├── samples/
    │   ├── raw_sofr_sample.csv
    │   ├── raw_cme_sample.csv
    │   └── processed_sample.csv
    └── archive/
        └── changelog.md
```

No shared collector with other variables. `parse_gilr.py` is standalone.

---

## 9. Fields

| Field | Type | Units | Required | Source | Notes |
|---|---|---|---|---|---|
| `variable_id` | string | — | Required | System | Always `L0-009` |
| `observation_date` | date | ISO 8601 | Required | System | Date of CME settlement |
| `tenor` | string | — | Required | System | Always `3M` |
| `gilr_cme_pct_pa` | float | % p.a. | Required | Derived | SOFR3M − CME implied forward rate; production series |
| `sofr_3m_pct_pa` | float | % p.a. | Required | FRED SOFR3M | Input to computation |
| `sofr_vintage_date` | date | ISO 8601 | Required | FRED | Date of SOFR3M observation used |
| `sofr_source` | string | — | Required | System | `FRED_SOFR3M` or `FRED_SOFR_COMPOUNDED` if substituted |
| `cme_implied_forward_rate_pct_pa` | float | % p.a. | Required | CME | Derived from contract spread |
| `cme_front_contract` | string | — | Required | CME | Contract code (e.g. `GCQ26`) |
| `cme_front_settlement` | float | USD/troy oz | Required | CME | Settlement price of front contract |
| `cme_front_expiry` | date | ISO 8601 | Required | CME | Actual expiry date of front contract |
| `cme_far_contract` | string | — | Required | CME | Contract code (e.g. `GCZ26`) |
| `cme_far_settlement` | float | USD/troy oz | Required | CME | Settlement price of far contract |
| `cme_far_expiry` | date | ISO 8601 | Required | CME | Actual expiry date of far contract |
| `days_between_contracts` | integer | calendar days | Required | Derived | `cme_far_expiry − cme_front_expiry` |
| `cme_source` | string | — | Required | System | `NASDAQ_CHRIS_CME` or `CME_MANUAL` |
| `ingested_at` | datetime | ISO 8601 UTC | Required | System | Parser run timestamp |
| `parser_version` | string | — | Required | System | Version of `parse_gilr.py` |
| `is_revised` | boolean | — | Required | System | True if prior stored value for same date changed |
| `prior_gilr_cme_pct_pa` | float or null | % p.a. | Conditional | System | Required if `is_revised=true` |
| `revision_reason` | string or null | — | Conditional | System | Required if `is_revised=true` |
| `validation_status` | string | — | Required | System | `PASS`, `FLAG`, `FAIL` |
| `availability_status` | string | — | Required | System | `AVAILABLE`, `STALE`, `INCOMPLETE`, `BLOCKED`, `INSUFFICIENT_EVIDENCE` |
| `anomaly_notes` | string or null | — | Conditional | System | Required if `validation_status` ≠ `PASS` |

**Deferred fields (not in v1):** LBMA PM fix cross-check; multiple alternative source fields. Add in a later revision if needed.

---

## 10. Validation Rules

| Check | Rule | Action |
|---|---|---|
| All required fields present and parseable | No null/non-numeric required fields | `FAIL` |
| SOFR3M is numeric and non-negative | `sofr_3m_pct_pa >= 0` | `FLAG` if negative (unusual policy environment); `FAIL` if < −1.0% |
| Contract ordering | `cme_far_expiry > cme_front_expiry` | `FAIL` if inverted |
| Day span within target range | `60 <= days_between_contracts <= 120` | `FAIL` if outside; parser must not produce a record outside this window |
| SOFR vintage not forward-dated | `sofr_vintage_date <= observation_date` | `FAIL` |
| Derived calculation reconciliation | Recompute `GILR-CME` from stored inputs; must match `gilr_cme_pct_pa` within 0.0001% | `FAIL` if mismatch (indicates computation or storage error) |
| Settlement prices plausible | Both settlements > 0; far/front ratio between 0.85 and 1.15 | `FAIL` if settlement ≤ 0; `FLAG` if ratio outside range |
| GILR-CME within broad historical range | −2.0% to +4.0% p.a. | `FLAG` if outside; never `FAIL` on range alone |
| Negative GILR-CME | Any value < 0 | `FLAG` with note: "Negative GILR-CME indicates backwardation or tight physical financing conditions; economically valid" |
| Contract roll proximity | `cme_front_expiry − observation_date <= 10 calendar days` | `FLAG` with note: "Near contract roll; proxy may show transient basis effects" |
| Missing-day gap | > 3 consecutive missing trading days | `FLAG`; > 5 = `BLOCKED` |
| Revision fields complete | All non-null when `is_revised=true` | `FAIL` |

---

## 11. Missing-Data Behavior

| Scenario | `availability_status` | Action |
|---|---|---|
| All inputs present; all checks passed | `AVAILABLE` | Normal |
| SOFR3M substituted with compounded overnight SOFR | `INCOMPLETE` | Log substitution; flag |
| Automated retrieval fails; manual inputs provided | `AVAILABLE` | Run with `--manual`; log source as `CME_MANUAL` |
| No contract pair within 60–120 day window | `BLOCKED` | Log; do not produce record; escalate |
| Missing 1–5 trading days | `STALE` | Carry forward; operator approval required before scoring |
| Missing > 5 trading days | `BLOCKED` | Halt; escalate to Grace |
| Validation `FLAG` | `AVAILABLE` | Store; operator approval required before scoring |
| Validation `FAIL` | do not store | Log error; do not append to processed store |

---

## 12. Reuse Check

| Variable | Overlap | Decision |
|---|---|---|
| L1-001 10Y TIPS Real Yield | SOFR/rates data — entirely different series | No overlap; SOFR is an input here, not a stored output |
| L1-003 Forward Real Rates | Conceptually adjacent; GILR-CME measures gold-specific financing spread | Distinct; Phase 1 registry explicitly classifies this as a duplicate candidate only if misinterpreted |
| L10-002 COMEX Gold Futures OI | Shares CME as data source | No field overlap; open interest vs settlement prices are different series |
| All other L0 variables | Different sources and concepts | No overlap |

---

## 13. Pre-Production Blockers

| # | Blocker | Status | Notes |
|---|---|---|---|
| B1 | Nasdaq Data Link free tier ToS for production analytical use not confirmed | OPEN | Confirm whether free tier permits non-commercial analytical use; CME manual download is acceptable fallback if restricted |
| B2 | `parse_gilr.py` not implemented | OPEN | Awaiting Grace approval of this proposal |
| B3 | Contract selection logic not tested against historical data | OPEN | Parser must correctly select contract pair for a range of dates including roll periods |
| B4 | No live PASS run | OPEN | Follows B1–B3 |

**Removed from blockers (per Grace review):**
- B6 (licensed terminal decision) — optional future upgrade; not a gate
- B2 prior (FRED API key) — not required for CSV endpoint

**Recommended sequence:** Grace approves v2 → B1 confirmed → B2 built → B3 tested → B4 live run → Grace re-review.

---

## 14. Implementation Status

| Item | Status |
|---|---|
| Proposal | v2 DRAFT — submitted for Grace review |
| Production variable | LOCKED — 3M GILR-CME derived proxy |
| Source | LOCKED — FRED SOFR3M + Nasdaq/CME GC1/GC2 |
| Calculation methodology | LOCKED — documented in Section 5 |
| Fields | LOCKED — Section 9 |
| Parser | NOT STARTED — awaiting Grace approval |
| Tests | NOT STARTED |
| Live run | NOT STARTED |
| Licensed terminal upgrade | DEFERRED — optional; document in changelog if acquired |
