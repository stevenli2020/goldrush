# L0-005 — Bar-and-Coin Investment Holdings / Demand: Implementation Proposal

**Variable ID:** L0-005  
**Layer:** L0 — Gold's Stock/Flow Monetary Architecture  
**Status:** COMPLETE
**Owner:** Chris  
**Proposal version:** v2 (implemented and approved)
**Date:** 2026-08-19

---

## 1. Primary and Fallback Sources

| | Primary |
|---|---|
| **Provider** | World Gold Council (WGC) — Gold Demand Trends (GDT) |
| **Dataset** | GDT quarterly workbook — "Bar and Coin" sheet |
| **Workbook name pattern** | `GDT_Tables_Q{Q}'{YY}_EN.xlsx` |
| **Access method** | Manual download from WGC GoldHub per quarter; saved to `docs/phase2-ingestion/L0/005/data/gold-demand-trends/` |
| **Format** | `.xlsx` — multi-sheet workbook |
| **Coverage** | Annual: 2010–2025; Quarterly: Q1 2010–Q2 2026 (as at current workbook) |
| **Frequency** | Quarterly release (Q1 published ~May, Q2 ~August, Q3 ~November, Q4 ~February following year) |
| **Revision policy** | WGC revises prior-period figures when underlying provider data (Metals Focus, Refinitiv GFMS, ICE Benchmark Administration) is updated; no formal revision calendar; detected by SHA-256 checksum comparison against prior workbook |
| **Access / licensing** | Public; manual download; automated download must be validated against WGC ToS before production |
| **Underlying providers** | Metals Focus; Refinitiv GFMS; ICE Benchmark Administration; World Gold Council |
| **Confidence** | High — WGC GDT is the global industry-standard quarterly demand dataset |

**Relevant sheet:** `Bar and Coin`  
**Relevant rows (confirmed from workbook inspection):**
- Row 44 — `Total above` (sum of all named countries; excludes "Other & stock change")
- Row 45 — `Other & stock change`
- Row 46 — `World total` (production-side reconciled global total = Row 44 + Row 45)
- Row 48 — Source attribution: `Metals Focus, Refinitiv GFMS, ICE Benchmark Administration, World Gold Council`

**Cross-reference from Gold Balance sheet (confirmed):**
- `Total Bar and Coin` (Row 20) = annual global demand reconciled total
- Sub-components also available: `Bars` (Row 21), `Official Coins` (Row 22), `Medals / Imitation Coins` (Row 23)

**Fallback:** Carry-forward of last successfully collected observation, flagged `availability_status: STALE`. No live alternative source exists at equivalent global coverage and methodology. Stale data must not enter scoring without explicit operator approval.

---

## 2. Scope Definition

**Production series: quarterly demand flow (not accumulated holdings stock)**

| Decision | Rationale |
|---|---|
| **Demand flow**, not holdings stock | WGC GDT publishes quarterly bar-and-coin demand (tonnes purchased/sold net in a period). It does not publish an accumulated holdings stock series. The variable name includes "Holdings / Demand" — the production series uses what WGC actually publishes: demand flow. |
| **No mixing of flows and stocks** | A holdings stock could in principle be constructed by cumulating demand flows, but this requires assumptions about starting stock, melting, recycling, and losses. No such transformation will be performed without explicit architecture approval. |
| **Separate fields for bars and coins** | The Gold Balance sheet provides a three-way split: `Bars`, `Official Coins`, `Medals/Imitation Coins`. These are ingested as separate fields. The "Bar and Coin" sheet provides the country breakdown of the combined total only. |
| **Both annual and quarterly** | Annual series (2010–present) and quarterly series (Q1 2010–present) are both available and both ingested. Two record types: `observation_period_type: annual` and `observation_period_type: quarterly`. |

---

## 3. Programmatic Collection Method

**Primary flow:**
1. Operator manually downloads current GDT workbook from WGC GoldHub quarterly
2. Saves to `docs/phase2-ingestion/L0/005/data/gold-demand-trends/GDT_Tables_Q{Q}'{YY}_EN.xlsx`
3. Parser script runs against the new workbook:
   - Reads `Gold Balance` sheet → extracts global total and sub-components (Bars, Official Coins, Medals/Imitation Coins) for annual and quarterly periods
   - Reads `Bar and Coin` sheet → extracts country-level combined bar-and-coin demand for annual and quarterly periods
4. Computes SHA-256 of the downloaded workbook; records in every output record
5. Validates output against schema
6. Appends to processed store; archives workbook

**Fallback flow (trigger: no new workbook for > 120 days past expected release date):**
1. Log `availability_status: BLOCKED`
2. After operator confirms no new WGC release, carry forward last observation with `availability_status: STALE`
3. Stale data must not enter scoring without explicit operator approval

**Parser script:** `docs/phase2-ingestion/L0/005/data/parse_bar_and_coin.py`  
This is a **standalone L0-005 parser** — it does not reuse `wgc_scraper.py` (which targets a different WGC endpoint and format). The same GDT workbook download is shared with any other L0 variable that draws from GDT sheets (e.g., L0-003 ETF Holdings, L0-006 Recycling Flow). The parser is L0-005-specific in its row/column targets and output schema.

**Shared workbook download:** One downloaded GDT workbook serves multiple L0 variables. The download is performed once per quarter; each variable's parser reads from the same archived file. Do not download the workbook multiple times for different variables.

---

## 4. Collector Location and Architecture

```
docs/phase2-ingestion/
└── L0/
    └── 005/
        ├── bar-and-coin-demand.md          # This document
        └── data/
            ├── parse_bar_and_coin.py       # L0-005 parser (standalone)
            ├── config.yaml                 # Parser config; sheet targets; validation bounds
            ├── schema.json                 # Field definitions and validation rules
            ├── README.md                   # Operational manual
            ├── gold-demand-trends/         # Downloaded workbooks (production archive)
            │   └── GDT_Tables_Q2'26_EN.xlsx
            ├── processed/                  # Parser output (append-only)
            │   └── L0_005_observations.csv
            ├── samples/                    # Static fixtures only
            │   ├── raw_parsed_sample.json
            │   └── processed_sample.csv
            └── archive/
                └── changelog.md
```

**`gold-demand-trends/` vs `samples/`:**
- `gold-demand-trends/` holds the actual downloaded workbooks. Authoritative production archive; one file per quarterly release; do not delete prior files.
- `samples/` holds static development fixtures only; the parser does not write here.

**Processing pipeline:**
1. Operator downloads new GDT workbook → saves to `gold-demand-trends/`
2. `parse_bar_and_coin.py` reads the file, computes SHA-256, extracts rows
3. Validates against schema; routes to `PASS`, `FLAG`, or `FAIL`
4. `PASS`/`FLAG`: appends to `processed/L0_005_observations.csv`; logs to `archive/changelog.md`
5. `FAIL`: halts; writes error log; does not append to processed store; escalates to operator

---

## 5. Fields, Units, and Timestamps

**Two record types share the same schema. The `observation_period_type` field distinguishes them.**

| Field | Type | Units | Required | Source | Notes |
|---|---|---|---|---|---|
| `variable_id` | string | — | Required | System | Always `L0-005` |
| `observation_period` | string | — | Required | WGC | Annual: `"2025"`; Quarterly: `"Q2'26"` — exactly as labelled in workbook header row |
| `observation_period_type` | string | — | Required | System | `"annual"` or `"quarterly"` |
| `observation_year` | integer | YYYY | Required | Derived | Calendar year; for quarterly records derived from period label |
| `observation_quarter` | integer or null | 1–4 | Conditional | Derived | Quarter number; null for annual records |
| `bar_demand_tonnes` | float | Metric tonnes | Required | WGC Gold Balance sheet | Row 21: `Bars`; null if unpublished |
| `official_coin_demand_tonnes` | float | Metric tonnes | Required | WGC Gold Balance sheet | Row 22: `Official Coins`; null if unpublished |
| `medals_imitation_coin_tonnes` | float | Metric tonnes | Required | WGC Gold Balance sheet | Row 23: `Medals / Imitation Coins`; null if unpublished |
| `total_bar_and_coin_tonnes` | float | Metric tonnes | Required | WGC Gold Balance sheet | Row 20: `Total Bar and Coin`; global demand reconciled total |
| `named_country_total_tonnes` | float | Metric tonnes | Optional | WGC Bar and Coin sheet | Row 44: `Total above` (sum of named countries only) |
| `other_and_stock_change_tonnes` | float | Metric tonnes | Optional | WGC Bar and Coin sheet | Row 45: `Other & stock change` |
| `world_total_bar_and_coin_sheet_tonnes` | float | Metric tonnes | Optional | WGC Bar and Coin sheet | Row 46: `World total` from Bar and Coin sheet; should reconcile with Gold Balance total |
| `unit` | string | — | Required | System | Always `"metric_tonnes"` |
| `source_name` | string | — | Required | System | `"WGC_GDT"` |
| `source_workbook` | string | — | Required | System | Filename of the downloaded workbook; e.g. `"GDT_Tables_Q2'26_EN.xlsx"` |
| `source_publication_date` | date | ISO 8601 | Required | Operator | Date WGC published this workbook; recorded manually at download |
| `download_date` | date | ISO 8601 | Required | Operator | Date operator downloaded the workbook |
| `workbook_sha256` | string | hex | Required | System | SHA-256 hash of the `.xlsx` file as downloaded; for integrity and revision detection |
| `ingested_at` | datetime | ISO 8601 UTC | Required | System | Timestamp when parser processed this record |
| `parser_version` | string | — | Required | System | Version of `parse_bar_and_coin.py` used; e.g. `"1.0.0"` |
| `underlying_providers` | string | — | Required | System | `"Metals Focus; Refinitiv GFMS; ICE Benchmark Administration; World Gold Council"` |
| `is_revised` | boolean | — | Required | System | `true` if this record replaces a previously stored observation for the same `observation_period` |
| `prior_workbook_sha256` | string or null | hex | Conditional | System | SHA-256 of the prior workbook if `is_revised: true` |
| `prior_total_bar_and_coin_tonnes` | float or null | Metric tonnes | Conditional | System | Prior stored value if `is_revised: true` |
| `revision_reason` | string or null | — | Conditional | Operator | Required if `is_revised: true`; e.g. `"WGC Q3 workbook revised Q1 2026 figures"` |
| `validation_status` | string | — | Required | System | `"PASS"`, `"FLAG"`, or `"FAIL"` |
| `availability_status` | string | — | Required | System | `"AVAILABLE"`, `"STALE"`, `"INCOMPLETE"`, `"BLOCKED"`, `"INSUFFICIENT_EVIDENCE"` |
| `anomaly_notes` | string or null | — | Conditional | System | Required if `validation_status` is `"FLAG"` or `"FAIL"` |

**Timestamp rules:**
- `observation_period`: use the exact label from the workbook header row (e.g. `"Q2'26"`, `"2025"`)
- `source_publication_date`: recorded manually by operator at download; WGC typically publishes release notes on its website
- `download_date`: date the workbook file was saved locally — distinct from publication date
- `ingested_at`: always UTC; set by parser at time of processing

**Revision semantics:**  
`is_revised: true` when a new workbook provides a different value for an `observation_period` already in the processed store. A new quarterly period appearing for the first time is a new record, not a revision. All three revision fields (`prior_workbook_sha256`, `prior_total_bar_and_coin_tonnes`, `revision_reason`) are required when `is_revised: true`; missing revision fields = `validation_status: FAIL`.

---

## 6. Freshness, Validation, and Missing-Data Behavior

### Freshness thresholds

| Condition | Threshold | Action |
|---|---|---|
| New quarterly workbook downloaded | Within 14 days of WGC release | Normal ingestion |
| No new workbook after 120 days past expected release | Overdue warning | Operator checks WGC GoldHub; escalates if no new release |
| Last ingested observation older than 6 months | Stale | `availability_status: STALE`; operator approval required before scoring |
| Last ingested observation older than 12 months | Unusable | `availability_status: INSUFFICIENT_EVIDENCE`; remove from scoring; escalate |

### Validation checks

| Check | Rule | On breach |
|---|---|---|
| All demand fields non-negative | `bar_demand_tonnes`, `official_coin_demand_tonnes`, `medals_imitation_coin_tonnes`, `total_bar_and_coin_tonnes` ≥ 0 | `FAIL` if negative; note: negative values in WGC data (e.g., Japan, Thailand) represent net selling/dishoarding — valid for country-level but `total_bar_and_coin_tonnes` at global level should be ≥ 0 |
| Global total positive | `total_bar_and_coin_tonnes` > 0 | `FAIL` |
| Sub-components sum to total | `bar + official_coin + medals` ≈ `total_bar_and_coin_tonnes` within ±1% | `FLAG`; `FAIL` if mismatch > 5% |
| Bar-and-coin sheet reconciliation | `world_total_bar_and_coin_sheet_tonnes` ≈ `total_bar_and_coin_tonnes` within ±1% | `FLAG` with `anomaly_notes` |
| Global total within plausible range | Annual: 600t–2,000t; Quarterly: 100t–700t (based on 2010–2026 observed range) | `FLAG` if outside; operator review |
| Quarter-on-quarter change | Any QoQ change > 200t flagged for review; no hard rejection | `FLAG` with `anomaly_notes` |
| Period label format valid | Annual: 4-digit year; Quarterly: matches `Q[1-4]'[0-9]{2}` | `FAIL` if malformed |
| SHA-256 present and 64-character hex | Non-null, valid format | `FAIL` if absent or malformed |
| Revision fields complete when `is_revised: true` | All three revision fields non-null | `FAIL` |

**On country-level negatives:**  
Individual countries can show negative bar-and-coin demand (net dishoarding / selling back into market). This is valid in WGC data — e.g., Japan, Thailand have historically shown negative annual figures. Do not flag country-level negatives as errors; they are structurally expected. Only flag if the global `total_bar_and_coin_tonnes` is negative.

**`FLAG` handling:** `FLAG` records are archived and staged; must not enter scoring without explicit operator approval.

### Missing-data behavior

| Scenario | `availability_status` | Behavior |
|---|---|---|
| Clean parse, all checks passed | `AVAILABLE` | Normal; no escalation |
| Workbook not yet downloaded for current quarter | `BLOCKED` | Operator download pending; no parser run |
| WGC delays publication beyond 120 days | `STALE` | Carry last observation; operator approval required before scoring |
| Global total present; sub-components absent | `INCOMPLETE` | Proceed with total only; sub-component fields null |
| Last observation older than 12 months | `INSUFFICIENT_EVIDENCE` | Do not pass to scoring; escalate |

---

## 7. Reuse Check Against Existing Adapters

**Collector status:** `wgc_scraper.py` (L0-001) targets a different WGC endpoint (above-ground stock `.xlsx`). It does not handle GDT workbooks. L0-005 requires a standalone parser: `parse_bar_and_coin.py`.

**Shared workbook:** The GDT workbook downloaded for L0-005 contains multiple sheets. Other L0 variables that draw from GDT should reuse the same downloaded file rather than downloading independently.

| Variable | Source overlap | Reuse decision |
|---|---|---|
| **L0-001** Above-Ground Gold Stock | Different WGC endpoint (`above-ground-stocks.xlsx`) | No workbook reuse; different dataset entirely |
| **L0-002** Central-Bank Gold Holdings | WGC GDT Gold Balance sheet (Row 25: `Central Bank and Other Institutions`) | **Shared workbook**: L0-002 parser reads from same GDT download; different sheet rows |
| **L0-003** Gold ETF Holdings | WGC GDT Gold Balance sheet (Row 24: `ETFs and Similar Products`) + WGC ETFs sheet | **Shared workbook**: same GDT download; different parser |
| **L0-006** Gold Recycling Flow | WGC GDT Gold Balance sheet (Row 10: `Recycled Gold`) | **Shared workbook**: same GDT download; different parser |
| **L8-001** Gold ETF Net Flows | WGC GDT ETFs sheet | **Shared workbook**: same GDT download; different parser |
| **L5-001** Monthly Official-Sector Gold Purchases | WGC GoldHub separate dataset (not GDT) | No workbook reuse |

**Structural overlap with L0-001:**  
The `Gold Balance` sheet Row 20 (`Total Bar and Coin`) is a subset of the investment demand total, which in turn is a subset of total demand. L0-001 accumulates stock over time; L0-005 measures quarterly flow into physical investment. These are complementary, not duplicative. Transmission relationship: bar-and-coin demand flow (L0-005) incrementally adjusts the above-ground stock (L0-001). Flagged for Spec A dependency treatment.

**Structural note on bars vs coins:**  
The `Bar and Coin` sheet provides country-level breakdown of the combined total. The `Gold Balance` sheet provides the global three-way split (Bars, Official Coins, Medals/Imitation Coins). Both are ingested; neither is dropped.

---

## 8. Pre-Production Blockers

| # | Blocker | Status | Owner | Notes |
|---|---|---|---|---|
| B1 | `parse_bar_and_coin.py` not implemented or tested | OPEN | Collector developer (unassigned) | Script does not exist. Must be built and tested against `GDT_Tables_Q2'26_EN.xlsx` before any production run. |
| B2 | WGC ToS compliance for manual download not formally confirmed | OPEN | Operator (unassigned) | Manual download appears to be standard public access; formal confirmation still required before production scheduling. |
| B3 | `source_publication_date` recording process not yet established | OPEN | Operator (unassigned) | Operator must record the WGC publication date at download time; no automated way to retrieve it post-hoc. |
| B4 | Collector developer and operator unassigned | OPEN | APROXI / project management | `config.yaml` ownership fields are placeholders. Must be filled before production. |
| B5 | No live parse with validated `PASS` result completed | OPEN | Collector developer + operator | A full parse of `GDT_Tables_Q2'26_EN.xlsx` producing a `PASS` record is required before production scheduling. |
| B6 | Shared workbook download protocol with L0-002, L0-003, L0-006, L8-001 not yet formalised | OPEN | APROXI | One operator downloads GDT once per quarter; all GDT-dependent parsers run against the same file. Protocol for coordinating this across variables must be documented. |

**Unblocking sequence:**
1. Assign operator and collector developer (B4)
2. Confirm WGC ToS for manual download (B2)
3. Establish publication-date recording process (B3)
4. Build and test `parse_bar_and_coin.py` against current workbook (B1)
5. Formalise shared workbook download protocol (B6)
6. Execute live parse; confirm `PASS` (B5)
7. Report to APROXI → Grace sign-off → status = COMPLETE

---

## Implementation Status

| Item | Status | Note |
|---|---|---|
| Proposal | COMPLETE | Implemented and approved 2026-08-19 |
| Sources | LOCKED | WGC GDT quarterly workbook; no live fallback |
| Scope | LOCKED | Demand flow; quarterly + annual; bars/coins split from Gold Balance sheet |
| Fields/schema | COMPLETE | See schema.json |
| Parser | COMPLETE | `data/parse_bar_and_coin.py`; live run passed 82/82 records |
| Config | COMPLETE | See config.yaml |
| Operational manual | COMPLETE | See data/README.md |
| Pre-production blockers | CLOSED | Resolved and reviewed 2026-08-19 |
