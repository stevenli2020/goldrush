# L0-009 Operational Manual
## 3-Month CME-Derived Gold Implied Lease Rate Proxy (GILR-CME)

**Variable:** Gold Lease Rates / Forward Rates  
**Layer:** 0  
**Parser:** `parse_gilr.py` (standalone collector + parser)  
**Configuration:** `config.yaml`  
**Schema:** `schema.json`  
**Inputs:** FRED SOFR3M + CME COMEX gold futures settlements

---

## Overview

L0-009 computes a daily 3-month Gold Implied Lease Rate proxy (GILR-CME) from two free public inputs:

1. **SOFR3M** — 3-month term SOFR from the Federal Reserve via FRED
2. **CME COMEX gold futures settlements** — front and far month contracts via Nasdaq Data Link

**Formula:**
```
CME_forward_rate = ((far_settle / front_settle) − 1) × (360 / days) × 100
GILR-CME = SOFR3M − CME_forward_rate
```

This is a derived proxy, not a directly observed OTC lease rate. It incorporates futures basis, storage, and convenience-yield effects in addition to the lending rate signal.

---

## Quick Start

### Prerequisites
- Python 3.8+
- Libraries: `pyyaml` (only external dependency)
- Network access to FRED and Nasdaq Data Link (for automated mode)
- Or: manually placed raw files (for manual mode)

```bash
pip install pyyaml
```

### Automated run (requires network)
```bash
python parse_gilr.py --config config.yaml --date 2026-08-19
```

### Manual run (place raw files first — see Manual Fallback section)
```bash
python parse_gilr.py --config config.yaml --date 2026-08-19 --manual
```

### Dry run (validate without writing output)
```bash
python parse_gilr.py --config config.yaml --date 2026-08-19 --manual --dry-run
```

### Expected output
- `processed/L0_009_observations.csv` — one record appended per run
- `archive/ingest.log` — execution log

---

## Contract Selection

For each observation date the parser selects two active COMEX gold contracts:

- **Front contract:** nearest delivery contract with ≥ 5 calendar days to expiry (avoids delivery distortion)
- **Far contract:** next delivery contract with expiry 60–120 calendar days after the front contract expiry (targeting ~90 days)

COMEX gold delivery months: February, April, June, August, October, December.  
Expiry: third-to-last business day of the delivery month.

**Near-roll FLAG:** If the front contract expires within 10 calendar days of the observation date, the record is flagged with `anomaly_notes` noting roll proximity. This is informational; the record is still stored as `AVAILABLE`.

**No valid pair:** If no contract pair falls within the 60–120 day window, the parser aborts with `BLOCKED` — do not interpolate or force a pair.

---

## Manual Fallback Procedure

If automated retrieval (FRED or Nasdaq) is unavailable:

**Step 1 — Download SOFR3M**
1. Go to: https://fred.stlouisfed.org/series/SOFR3M
2. Click "Download" → CSV
3. Save as: `raw/YYYY-MM-DD/sofr3m.csv`

**Step 2 — Download CME settlements**
1. Go to: https://www.cmegroup.com/market-data/reports/daily-settlement.html
2. Filter: COMEX → Gold → Gold Futures
3. Note settlement prices for the two active contracts (front and far per contract selection rules above)
4. Create `raw/YYYY-MM-DD/cme_gc_settlement.csv` with columns:
   ```
   date,front_contract,front_settle,far_contract,far_settle
   2026-08-19,GCQ26,2485.30,GCV26,2502.80
   ```
   Use contract codes in format `GC{month_code}{YY}`:
   February=G, April=J, June=M, August=Q, October=V, December=Z

**Step 3 — Run parser**
```bash
python parse_gilr.py --config config.yaml --date 2026-08-19 --manual
```

---

## Full Workflow (daily operations)

```
1. (Automated) Run parser for current trading day
   OR
   (Manual) Place raw files → run with --manual

2. Check ingest.log:
   tail -10 archive/ingest.log

3. Verify output record:
   tail -2 processed/L0_009_observations.csv

4. If FLAG: review anomaly_notes; approve before scoring
5. If FAIL: do not use; investigate; re-run after correcting inputs
6. If gap > 5 trading days: escalate to Grace
```

---

## Validation Reference

| Check | Rule | Action |
|---|---|---|
| Required fields present and numeric | All required fields non-null | FAIL |
| SOFR3M ≥ 0% | `sofr_3m_pct_pa >= 0` | FLAG if negative; FAIL if < −1% |
| Settlements > 0 | Both front and far > 0 | FAIL |
| Settlement ratio | `0.85 ≤ far/front ≤ 1.15` | FLAG |
| Contract ordering | `far_expiry > front_expiry` | FAIL |
| Day span | `60 ≤ days ≤ 120` | FAIL |
| SOFR vintage | `sofr_vintage_date ≤ observation_date` | FAIL |
| Calculation reconciliation | Recomputed GILR matches stored within 0.0001% | FAIL |
| GILR range | −2.0% to +4.0% p.a. | FLAG |
| Negative GILR | Any value < 0 | FLAG (economically valid; never FAIL) |
| Roll proximity | Front expiry ≤ 10 days away | FLAG |

**FLAG records:** Stored as `AVAILABLE`; operator approval required before scoring.

---

## Error Handling

| Symptom | Likely cause | Resolution |
|---|---|---|
| `HTTP Error 404` on FRED endpoint | Network restricted; URL changed | Use `--manual` mode |
| `No SOFR3M data on or before {date}` | Weekend/holiday with no prior data in file | Ensure raw file covers the preceding business days |
| `Manual contract span Xd outside [60, 120]` | Wrong contract pair in manual file | Check delivery months and select correct pair (see Contract Selection section) |
| `FAIL: calculation mismatch` | Stored GILR doesn't match recomputed | Re-run from raw inputs; do not edit CSV directly |
| `No valid pair found` | Unusual market calendar gap | Check CME holiday schedule; escalate to Grace |
| `FAIL: far_expiry <= front_expiry` | Manual file has contracts in wrong order | Swap front and far in `cme_gc_settlement.csv` |

---

## Maintenance

### Daily
- Run parser for each trading day
- Check log for FLAG/FAIL

### Weekly
- Verify no gaps > 3 consecutive trading days in processed store
- Check CME holiday schedule for upcoming week

### Quarterly
- Confirm Nasdaq Data Link free tier still active
- Confirm FRED SOFR3M series still published
- Review validation bounds (−2% to +4%) against recent GILR-CME range
- Update `archive/changelog.md`

### If source structure changes
- FRED changes SOFR3M series ID → update `config.yaml sofr.series` and `sofr.endpoint`
- Nasdaq changes CSV column names → update `parse_nasdaq_gc_csv()` column detection
- CME changes delivery months or expiry rule → update `config.yaml delivery_months` and `nth_to_last_business_day()`
- All changes require test re-run before production use

---

## Ownership and Escalation

| Role | Contact | Responsibility |
|---|---|---|
| Parser owner | Chris | Maintains `parse_gilr.py` |
| Config owner | Chris | Updates `config.yaml` on source structure changes |
| Operational owner | Chris | Daily runs; monitoring; escalation |
| Architecture review | Grace | Approves scope changes, validation bound changes |

**Escalation path:**
1. Parser/config errors → Chris
2. Validation FAIL → Chris + Grace
3. Gap > 5 trading days → Chris + Grace
4. Source discontinuation → Grace decision on replacement or deferral
