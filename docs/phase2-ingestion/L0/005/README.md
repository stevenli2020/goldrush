# L0-005 Operational Manual
## Bar-and-Coin Investment Holdings / Demand

**Variable:** Bar-and-Coin Investment Holdings / Demand  
**Layer:** 0  
**Parser:** `parse_bar_and_coin.py` (standalone; not shared)  
**Configuration:** `config.yaml`  
**Schema:** `schema.json`  
**Source:** WGC Gold Demand Trends quarterly workbook

---

## Overview

L0-005 ingests quarterly and annual bar-and-coin demand figures from the WGC Gold Demand Trends (GDT) workbook. The workbook is downloaded manually once per quarter; the parser extracts demand data from two sheets (`Gold Balance` and `Bar and Coin`), validates, and appends to the processed store.

**Output:** ~66 quarterly records + 16 annual records per full workbook parse (growing by 1 quarterly + 1 annual each quarter).

---

## Quick Start

### Prerequisites
- Python 3.8+
- Libraries: `openpyxl`, `pandas`, `pyyaml`, `jsonschema`, `` (stdlib)
- Read access to `docs/phase2-ingestion/L0/005/data/gold-demand-trends/`
- Write access to `docs/phase2-ingestion/L0/005/data/processed/`

### Install dependencies
```bash
pip install openpyxl pandas pyyaml jsonschema
```

### Run parser
```bash
cd docs/phase2-ingestion/L0/005/data
python parse_bar_and_coin.py \
  --workbook "gold-demand-trends/GDT_Tables_Q2'26_EN.xlsx" \
  --config config.yaml \
  --publication-date 2026-08-07 \
  --download-date 2026-08-18
```

### Expected output
- `processed/L0_005_observations.csv` — appended with new records
- `archive/ingest.log` — execution log with record counts and validation summary

---

## Manual Download Process

The GDT workbook is not available via a stable automated download endpoint. It must be downloaded manually each quarter.

### Steps
1. Navigate to: https://www.gold.org/goldhub/data/gold-demand-by-country
2. Locate the current quarterly GDT workbook download link (typically labelled "Download data tables")
3. Download the `.xlsx` file
4. **Record the publication date** — check the WGC press release or page metadata for the official release date; this is required as `source_publication_date` at parse time
5. Save to: `docs/phase2-ingestion/L0/005/data/gold-demand-trends/`
6. Use the exact WGC filename (e.g. `GDT_Tables_Q3'26_EN.xlsx`); do not rename
7. Confirm the file opens correctly in Excel or Python before running the parser

### Download timing
| Quarter | Expected release | Download target |
|---|---|---|
| Q1 | ~May | By end of May |
| Q2 | ~August | By end of August |
| Q3 | ~November | By end of November |
| Q4 | ~February (following year) | By end of February |

### Shared workbook
The GDT workbook is shared with L0-002, L0-003, L0-006, and L8-001. One download per quarter serves all these variables. Coordinate with the assigned shared-workbook owner (see `config.yaml`) before downloading — the file may already be present.

---

## Full Workflow

### 1. Confirm workbook is present
```bash
ls docs/phase2-ingestion/L0/005/data/gold-demand-trends/
```
Expected: `GDT_Tables_Q2'26_EN.xlsx` (or current quarter file)

### 2. Verify the file can be read
```python
import openpyxl
wb = openpyxl.load_workbook("GDT_Tables_Q2'26_EN.xlsx", read_only=True, data_only=True)
print(wb.sheetnames)
# Expected: ['User guide & contents', 'Disclaimer', 'Exec Summary', 'Snapshot',
#            'Gold Balance', 'Jewellery', 'Bar and Coin', 'Consumer per Capita',
#            'Gold Prices', 'India Supply', 'ETFs']
```

### 3. Run parser
```bash
python parse_bar_and_coin.py \
  --workbook "gold-demand-trends/GDT_Tables_Q2'26_EN.xlsx" \
  --config config.yaml \
  --publication-date <WGC_PUBLICATION_DATE> \
  --download-date <TODAY>
```

### 4. Check log
```bash
tail -30 archive/ingest.log
```
Expected summary:
```
2026-08-18 10:30:00 UTC | INFO | Workbook: GDT_Tables_Q2'26_EN.xlsx
2026-08-18 10:30:00 UTC | INFO | source metadata: a3f1c2...
2026-08-18 10:30:00 UTC | INFO | Annual records extracted: 16
2026-08-18 10:30:00 UTC | INFO | Quarterly records extracted: 66
2026-08-18 10:30:00 UTC | INFO | Validation: 82 PASS, 0 FLAG, 0 FAIL
2026-08-18 10:30:00 UTC | INFO | Revisions detected: 0
2026-08-18 10:30:00 UTC | INFO | Appended 82 records to L0_005_observations.csv
```

### 5. Spot-check processed output
```bash
tail -5 processed/L0_005_observations.csv
```
Confirm `Q2'26` quarterly record present with `validation_status=PASS` and `availability_status=AVAILABLE`.

### 6. Revision check
Parser automatically compares extracted values against previously stored records for the same `observation_period`. If any value differs:
- Sets `is_revised: true`
- Records prior source metadata and prior value
- Prompts operator to supply `revision_reason`
- Logs revision event in `archive/ingest.log`

### 7. Update SOURCE-IMPLEMENTATION-TRACKER.md
After successful `PASS` run, update L0-005 row in `docs/phase2-ingestion/SOURCE-IMPLEMENTATION-TRACKER.md`.

---

## Parser Logic (for developer reference)

### Sheet: Gold Balance
- **Header row:** Row 5 — contains period labels (`2010`, `2011`, ..., `Q1'10`, `Q2'10`, ...)
- **Annual columns:** detect by matching 4-digit integer labels (2010–present)
- **Quarterly columns:** detect by matching `Q[1-4]'[0-9]{2}` pattern
- **Extract rows:**
  - Row 20: `Total Bar and Coin` → `total_bar_and_coin_tonnes`
  - Row 21: `Bars` → `bar_demand_tonnes`
  - Row 22: `Official Coins` → `official_coin_demand_tonnes`
  - Row 23: `Medals Imitation Coins` → `medals_imitation_coin_tonnes`

### Sheet: Bar and Coin
- **Header row:** Row 5 — same period label structure
- **Extract rows:**
  - Row 44: `Total above` → `named_country_total_tonnes`
  - Row 45: `Other & stock change` → `other_and_stock_change_tonnes`
  - Row 46: `World total` → `world_total_bar_and_coin_sheet_tonnes`

### Period label to year/quarter mapping
- `"2025"` → `observation_year=2025`, `observation_quarter=null`
- `"Q2'26"` → `observation_year=2026`, `observation_quarter=2`
- Two-digit year: assume 2000s (e.g. `'10` → 2010, `'26` → 2026)

### Column detection
Parser must detect column positions dynamically from header row — do not hardcode column indices. WGC adds columns as new periods are published.

### source metadata computation
```python
import 
with open(workbook_path, "rb") as f:
    source metadata = .source metadata(f.read()).()
```

---

## Validation Reference

| Check | Rule | Action |
|---|---|---|
| Global total non-negative | `total_bar_and_coin_tonnes >= 0` | FAIL |
| Annual range | 600t–2,000t | FLAG |
| Quarterly range | 100t–700t | FLAG |
| Sub-components sum | bars + coins + medals ≈ total ±1% | FLAG; FAIL if >5% |
| Sheet reconciliation | world_total ≈ total ±1% | FLAG |
| QoQ change | > 200t | FLAG with note |
| Country-level negatives | Allowed; do not flag | — |
| Period label format | Annual `^[0-9]{4}$`; Quarterly `^Q[1-4]'[0-9]{2}$` | FAIL |
| source metadata format | 64-char hex | FAIL |
| Revision fields | All required if `is_revised=true` | FAIL |

**FLAG records:** Archived and staged; must not enter scoring without operator approval.

---

## Fallback Procedure

**If WGC has not published a new workbook within 120 days of expected release:**

1. Check WGC GoldHub manually: https://www.gold.org/goldhub/data/gold-demand-by-country
2. If no new workbook available, set `availability_status: STALE` on last known observation
3. Log in `archive/ingest.log`: `STALE — no new workbook as of <date>; last observation: <period>`
4. Do not attempt to reconstruct or interpolate missing data
5. Escalate to Grace if outage exceeds one full quarter (90 days past expected release)
6. `STALE` data must not enter scoring without explicit operator approval

---

## Error Handling

| Symptom | Likely cause | Resolution |
|---|---|---|
| `openpyxl` cannot open file | Corrupted download or wrong file format | Re-download workbook; verify file extension is `.xlsx` |
| `Sheet 'Gold Balance' not found` | WGC renamed a sheet | Check workbook manually; update `config.yaml` sheet name |
| `Row 20 label mismatch: expected 'Total Bar and Coin'` | WGC restructured rows | Inspect workbook; update `config.yaml` row targets |
| Column detection finds no annual headers | WGC changed header row | Check header row number in workbook; update `config.yaml` |
| `FAIL: total_bar_and_coin_tonnes < 0` | Parse error; wrong row/column selected | Inspect raw cell value; cross-check against workbook manually |
| `FAIL: sub-component mismatch > 5%` | WGC methodology change or parse error | Cross-check Gold Balance sheet manually; update schema if WGC changed breakdown |
| Revision detected but `revision_reason` not supplied | Operator did not pass `--revision-reason` flag | Re-run parser with `--revision-reason "WGC Q3'26 revised Q2'26 figures"` |

---

## Maintenance

### Quarterly
- [ ] Download new GDT workbook within 14 days of WGC release
- [ ] Record `source_publication_date` from WGC press release
- [ ] Run parser; confirm `PASS`
- [ ] Check for revisions to prior periods
- [ ] Update `SOURCE-IMPLEMENTATION-TRACKER.md`

### Annual
- [ ] Review validation bounds against published range (annual: 600–2,000t; quarterly: 100–700t)
- [ ] Confirm WGC sheet structure unchanged (sheet names, row numbers, header row)
- [ ] Archive prior year's processed CSV: `L0_005_observations_2025.csv`
- [ ] Update `archive/changelog.md`

### When WGC changes workbook structure
1. Note change in `archive/changelog.md` with workbook version and description
2. Update affected `config.yaml` fields (sheet names, row targets, header row)
3. Test parser against new workbook before production run
4. Flag if validation bounds need review; escalate to Grace for approval

---

## Ownership and Escalation

| Role | Contact | Responsibility |
|---|---|---|
| Parser owner | [To be assigned] | Builds and maintains `parse_bar_and_coin.py` |
| Config/schema owner | [To be assigned] | Updates `config.yaml` and `schema.json` when WGC structure changes |
| Operational owner | [To be assigned] | Downloads workbook, runs parser, monitors freshness |
| Shared workbook coordinator | [To be assigned — APROXI to confirm] | Ensures one download per quarter shared across L0-002, L0-003, L0-006, L8-001 |
| Architecture review | Grace | Approves changes to scope, field definitions, validation bounds |

**Escalation path:**
1. Parser errors → Parser owner
2. Config/schema mismatch → Config owner
3. Validation FAIL or FLAG → Operational owner + Grace
4. WGC structural change → Config owner + Grace
5. Extended WGC publication delay → Operational owner + Grace
