# L0-001 — Above-Ground Gold Stock: Implementation Proposal

**Variable ID:** L0-001
**Layer:** L0 — Gold's Stock/Flow Monetary Architecture
**Status:** ADMIT
**Owner:** Chris
**Proposal version:** v2 (approved)
**Approval date:** 2026-08-18

---

## 1. Primary and Fallback Sources

| | Primary |
|---|---|
| **Provider** | World Gold Council (WGC) — GoldHub |
| **Series / Dataset** | Above-Ground Stock dataset |
| **Page endpoint** | `https://www.gold.org/goldhub/data/how-much-gold` |
| **Download endpoint** | `https://www.gold.org/download/file/7588/above-ground-gold-stocks.xlsx` |
| **Format** | `.xlsx` direct download |
| **Coverage** | Annual, 2010–2025 (as currently published) |
| **Frequency** | Annual; one release per year tied to the full-year Gold Demand Trends report |
| **Revision policy** | WGC revises historical estimates when methodology or underlying source data updates; no formal revision calendar — monitor release notes and methodology PDF for changes |
| **Access / licensing** | Public; direct `.xlsx` download; no API key required; automated access must be validated by the collector before production use — the download endpoint may be restricted |
| **Underlying providers** | Metals Focus; Refinitiv GFMS; World Gold Council |
| **Confidence** | High — WGC is the industry-standard aggregate source |

**Fallback:** Carry-forward of last successfully collected WGC observation, flagged `availability_status: STALE`. This is an operational continuity measure only — it is not a fresh data pull and must not be treated as a new observation. No alternative live source is used.

**Methodology PDF:** `https://www.gold.org/download/file/7589/above-ground-stocks-methodology.pdf`
Treated as lineage and reference material only. Not a live fallback source.

**On USGS:** USGS provides annual mine-production figures, not an independent above-ground-stock estimate. Cumulative production alone omits recycling flows, fabrication losses, and the required starting-stock anchor. USGS data may be consulted as a cross-check on annual mine-supply increments during methodology review but must not enter the production pipeline as a stock figure.

**Source-locking actions required before production:**
- Confirm the `.xlsx` download URL is stable and does not rotate
- Confirm automated retrieval is permitted under WGC ToS
- Archive methodology PDF locally
- Record Metals Focus and Refinitiv GFMS in lineage metadata

---

## 2. Programmatic Collection Method

**Primary flow:**
1. HTTP GET to `.xlsx` download endpoint
2. Parse workbook using `wgc_scraper.py`; extract annual stock figures and sub-component breakdown
3. Write raw `.xlsx` bytes to `data/raw/YYYY/` with timestamped filename
4. Write parsed record to staging
5. Run validation checks (Section 5); route to `PASS`, `FLAG`, or `FAIL`

**Fallback flow (trigger: `.xlsx` download fails or returns unparseable content):**
1. Log `availability_status: BLOCKED`; do not attempt reconstruction
2. After 72 hours with no successful retrieval, carry forward last collected observation with `availability_status: STALE`
3. Escalate to operator; `STALE` records must not enter scoring without explicit operator approval
4. USGS data is not used in this flow

**Collector script:** `collectors/wgc_scraper.py`
Status: **New shared adapter — required; does not yet exist.**
The same script will serve L0-002, L0-003, L0-005, L0-006, L5-001, L5-002, and L8-001 against their respective WGC endpoints. The collector developer must build it; this proposal defines its role and interface.

**`FLAG` records:** May be archived and staged, but must not enter production scoring without explicit operator approval.

**Schedule:**
- Annual: trigger on WGC Gold Demand Trends report release detection (typically Q1 of the following year)
- Monthly: checksum check on the `.xlsx` download; if checksum changes, treat as a revision event and re-collect

---

## 3. Collector Location and Architecture

```
docs/phase2-ingestion/
├── collectors/
│   └── wgc_scraper.py              # New shared adapter — required; not yet built
└── L0/
    └── 001/
        ├── above-ground-stock.md   # This document
        └── data/
            ├── config.yaml
            ├── schema.json
            ├── README.md
            ├── raw/                # Production raw-observation archive (collector writes here)
            │   └── YYYY/
            │       └── raw_wgc_above_ground_stock_YYYYMMDD.xlsx
            ├── samples/            # Static fixtures only — not written to by the collector
            │   ├── raw_wgc_sample.json
            │   └── processed_sample.csv
            └── archive/
                └── changelog.md
```

**`raw/` vs `samples/`:**
- `raw/` is the production archive. The collector writes every retrieved `.xlsx` here with a timestamped filename. Authoritative audit trail; must not be manually edited.
- `samples/` holds static development fixtures only. Committed once to illustrate schema and format; the collector does not write to this directory.

**Processing pipeline:**
1. `wgc_scraper.py` fetches `.xlsx` → writes to `raw/YYYY/raw_wgc_above_ground_stock_YYYYMMDD.xlsx`
2. Parse workbook → staging record
3. Validation checks (Section 5)
4. `PASS` or `FLAG`: append to processed store; archive raw file
5. `FAIL`: halt; write error log; do not write to processed store; escalate

---

## 4. Fields, Units, and Timestamps

| Field | Type | Units | Required | Source | Notes |
|---|---|---|---|---|---|
| `variable_id` | string | — | Required | System | Always `L0-001` |
| `observation_year` | integer | YYYY | Required | WGC | Calendar year the stock estimate represents |
| `above_ground_stock_tonnes` | float | Metric tonnes | Required | WGC | Total accumulated above-ground gold stock |
| `jewellery_tonnes` | float | Metric tonnes | Optional | WGC | Sub-component: jewellery; null if not published |
| `bars_coins_etf_tonnes` | float | Metric tonnes | Optional | WGC | Sub-component: bars, coins, and gold-backed ETFs combined as published; not split |
| `central_banks_tonnes` | float | Metric tonnes | Optional | WGC | Sub-component: central bank holdings |
| `other_tonnes` | float | Metric tonnes | Optional | WGC | Sub-component: other uses |
| `source_name` | string | — | Required | System | `WGC_GOLDHUB` |
| `source_endpoint` | string | — | Required | System | Exact URL retrieved |
| `underlying_providers` | string | — | Required | System | `Metals Focus; Refinitiv GFMS; World Gold Council` |
| `publication_date` | date | ISO 8601 | Required | WGC | Date WGC published or last updated this estimate |
| `retrieval_timestamp` | datetime | ISO 8601 UTC | Required | System | When collector fetched the file |
| `raw_file_path` | string | — | Required | System | Path to archived `.xlsx` in `raw/` |
| `is_revised` | boolean | — | Required | System | `true` only when this record revises a previously stored observation for the same `observation_year` |
| `prior_publication_date` | date | ISO 8601 | Conditional | System | Required if `is_revised: true`; date of the superseded observation |
| `prior_value_tonnes` | float | Metric tonnes | Conditional | System | Required if `is_revised: true`; previously stored total for this `observation_year` |
| `revision_reason` | string | — | Conditional | System / operator | Required if `is_revised: true`; e.g. `"WGC methodology update"`, `"Metals Focus data revision"` |
| `transformation_notes` | string | — | Optional | System | Any unit conversion applied; null if raw value used as-is |
| `validation_status` | string | — | Required | System | `PASS`, `FLAG`, or `FAIL` |
| `availability_status` | string | — | Required | System | `AVAILABLE` on clean retrieval; `PARTIAL`, `STALE`, `INCOMPLETE`, `BLOCKED`, or `INSUFFICIENT_EVIDENCE` otherwise |
| `anomaly_notes` | string | — | Optional | System | Required if `validation_status` is `FLAG` or `FAIL` |

**Timestamp rules:**
- `observation_year`: the year the estimate represents, not the retrieval year
- `publication_date`: the date WGC released this estimate — distinct from retrieval
- `retrieval_timestamp`: always UTC; recorded by the collector at time of fetch

**Revision semantics:** `is_revised: true` means a new retrieval provides a different value for an `observation_year` already stored. A new annual observation for a new year is a new record, not a revision. When `is_revised: true`, all three revision fields (`prior_publication_date`, `prior_value_tonnes`, `revision_reason`) are required; any record with `is_revised: true` and any of those fields null must be treated as `validation_status: FAIL`.

**Sub-component note:** WGC publishes bars, coins, and gold-backed ETFs as a single combined figure in this dataset. `bars_coins_etf_tonnes` is recorded as published and must not be split. This combined figure partially overlaps with L0-003 and L0-005, which draw from separate granular WGC datasets. Flagged for Spec A dependency treatment.

---

## 5. Freshness, Validation, and Missing-Data Behavior

### Freshness thresholds

| Condition | Threshold | Action |
|---|---|---|
| New WGC annual release detected | Collect within 7 days | Normal ingestion |
| No new release after 18 months | Stale warning | `availability_status: STALE`; carry prior; operator approval required before passing to scoring |
| Last collected observation older than 24 months | Unusable | `availability_status: INSUFFICIENT_EVIDENCE`; do not use in scoring; escalate |

### Validation checks

| Check | Rule | Status on breach |
|---|---|---|
| Total stock present and numeric | Non-null, > 0 | `FAIL` |
| Total stock within plausible range | 150,000t – 300,000t (current ~220,000t; generous headroom) | `FLAG` if outside; operator review required |
| Year-on-year change | Any change large relative to known annual mine supply (~3,300–3,600t) or any year-on-year decline beyond rounding is flagged for operator review; no fixed percentage bounds applied | `FLAG` with anomaly note; operator decides |
| Sub-components sum to total (if present) | Within ±1% of reported total | `FLAG`; `FAIL` if mismatch > 5% |
| Revision fields complete when `is_revised: true` | `prior_publication_date`, `prior_value_tonnes`, `revision_reason` all non-null | `FAIL` |
| File retrievable and parseable | `.xlsx` downloads without error; at least one numeric value extracted | `FAIL` |

**`FLAG` handling:** `FLAG` records are archived and staged but must not enter production scoring without explicit operator approval.

### Missing-data behavior

| Scenario | `availability_status` | Behavior |
|---|---|---|
| Clean retrieval, all checks passed | `AVAILABLE` | Normal processing; no escalation |
| `.xlsx` temporarily unavailable | `BLOCKED` | Retry after 24h; escalate after 72h |
| No new release for full annual cycle | `STALE` | Carry last observation; log; operator approval required before scoring |
| Stock total present; sub-components absent | `INCOMPLETE` | Proceed with total only; null sub-component fields |
| Last observation older than 24 months | `INSUFFICIENT_EVIDENCE` | Do not pass to scoring; escalate |

---

## 6. Reuse Check Against Existing Adapters

**Collector status:** `wgc_scraper.py` and `treasury_api_client.py` are both referenced in project documentation as planned collectors but neither currently exists on disk. Both must be built as new shared adapters.

| Variable | Source overlap | Reuse decision |
|---|---|---|
| **L0-002** Central-Bank Gold Holdings | WGC GoldHub — different dataset | Reuse `wgc_scraper.py`; different endpoint and parse target |
| **L0-003** Gold ETF Holdings | WGC GoldHub — different dataset | Reuse `wgc_scraper.py` |
| **L0-005** Bar-and-Coin Investment Holdings | WGC GoldHub — demand datasets | Reuse `wgc_scraper.py` |
| **L0-006** Gold Recycling Flow | WGC GoldHub — supply/demand data | Reuse `wgc_scraper.py` |
| **L5-001** Monthly Official-Sector Gold Purchases | WGC GoldHub | Reuse `wgc_scraper.py` |
| **L5-002** Gold Share of Official Reserves | WGC GoldHub | Reuse `wgc_scraper.py` |
| **L8-001** Gold ETF Net Flows | WGC GoldHub | Reuse `wgc_scraper.py` |
| **L0-009** Gold Lease / Forward Rates | Different source — bullion market data | No reuse; separate new collector required |
| **L1-xxx / L4-xxx** TIPS, Treasury series | `treasury_api_client.py` (planned, not yet built) | No overlap with L0-001 |

**Structural overlap (L0-001 and L0-002):** Central-bank holdings are a published sub-component of the WGC above-ground stock total. L0-001 and L0-002 have a Transmission relationship per the Phase 1 registry. Flagged for Spec A dependency treatment.
