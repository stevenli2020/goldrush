# L0-001 — Above-Ground Gold Stock
## Operational Manual

**Variable ID:** L0-001 | **Layer:** L0 | **Status:** ADMIT
**Collector:** `collectors/wgc_scraper.py` (new shared adapter — not yet built)
**Owner:** Chris | **Collector developer:** TBD

---

## Quick Start

```
# Confirm collector exists before running
ls docs/phase2-ingestion/collectors/wgc_scraper.py

# Run collection for L0-001
python docs/phase2-ingestion/collectors/wgc_scraper.py --variable L0-001

# Output locations
#   Raw archive:  docs/phase2-ingestion/L0/001/data/raw/YYYY/raw_wgc_above_ground_stock_YYYYMMDD.xlsx
#   Processed:    pipeline staging store (see config.yaml for path)
#   Logs:         check collector log output for validation_status and availability_status
```

The collector is not yet built. This manual documents the intended operation for the collector developer.

---

## Full Workflow

### 1. Annual release cycle

WGC publishes the above-ground stock dataset once per year, in conjunction with the full-year Gold Demand Trends report (typically Q1 of the following year).

**Trigger:** Detect new Gold Demand Trends report publication. Collect within 7 days.

Steps:
1. HTTP GET to `https://www.gold.org/download/file/7588/above-ground-gold-stocks.xlsx`
2. Write raw bytes to `data/raw/{YYYY}/raw_wgc_above_ground_stock_{YYYYMMDD}.xlsx`
3. Parse workbook; extract `observation_year`, `above_ground_stock_tonnes`, and sub-components
4. Compute checksum; store for monthly revision monitoring
5. Run validation checks (see `config.yaml`)
6. On `PASS` or `FLAG`: write processed record to staging; log result
7. On `FAIL`: write error log; halt; escalate to operator; do not write to processed store
8. `FLAG` records are staged but must not enter scoring without explicit operator approval

### 2. Monthly revision check

On the first business day of each month:
1. HTTP GET to download URL; compute checksum
2. Compare against stored checksum from last successful retrieval
3. If unchanged: log "no revision detected"; exit
4. If changed: treat as revision event; re-run full collection flow
5. On revision: set `is_revised: true`; populate `prior_publication_date`, `prior_value_tonnes`, `revision_reason`

---

## Fallback Procedure

**Trigger:** `.xlsx` download fails or returns unparseable content.

1. Log `availability_status: BLOCKED`
2. Retry after 24 hours
3. After 72 hours with no successful retrieval: escalate to operator
4. Carry forward last successfully collected observation with `availability_status: STALE`
5. `STALE` records must not enter scoring without explicit operator approval
6. Do not use USGS data or any other source as a replacement stock figure
7. Methodology PDF (`https://www.gold.org/download/file/7589/above-ground-stocks-methodology.pdf`) is reference material only; it is not a data source

---

## Error Handling

| Error | Likely cause | Action |
|---|---|---|
| HTTP 403 / 404 on download URL | URL rotated or access restricted | Check WGC page for new URL; confirm ToS permits automated access; escalate |
| `.xlsx` parse fails | File format changed | Inspect raw file; update parser; do not proceed until parseable |
| `above_ground_stock_tonnes` null or zero | Extraction logic broken | `FAIL`; escalate; do not carry forward zero |
| Sub-components sum mismatch > 5% | Source data error or parse error | `FAIL`; inspect raw file; escalate |
| Year-on-year change flagged | Large revision or anomalous figure | `FLAG`; stage; await operator decision before scoring |
| `is_revised: true` but revision fields null | Bug in revision detection logic | `FAIL`; fix collector; do not archive |
| Retrieval succeeds but checksum unchanged | No revision; normal | Log "no revision"; exit cleanly |

---

## Troubleshooting

**Q: Collector runs but produces no output.**
Check that the download URL is reachable. Run `curl -I https://www.gold.org/download/file/7588/above-ground-gold-stocks.xlsx` and inspect the HTTP response code.

**Q: WGC page loads but download returns 403.**
Automated access may be restricted. Manual download and local placement in `raw/` is a temporary workaround. Escalate to confirm ToS and resolve for production.

**Q: Validation flags a large year-on-year change.**
This is expected when WGC publishes a methodology update or when Metals Focus revises its underlying estimates. Review the WGC release notes and methodology PDF. Set `revision_reason` accordingly and obtain operator approval before passing to scoring.

**Q: Sub-components are missing from the parsed record.**
WGC may not publish sub-components for all years. Set sub-component fields to null; proceed with total only; set `availability_status: INCOMPLETE`.

**Q: How do I know if a new annual release has been published?**
Monitor the WGC Gold Demand Trends report publication page. The download URL checksum will change when the file is updated. Check monthly.

---

## Maintenance Checklist

**After each annual collection:**
- [ ] Raw `.xlsx` archived in `data/raw/{YYYY}/`
- [ ] Processed record written to staging
- [ ] `validation_status` and `availability_status` logged
- [ ] `coverage_end` in `config.yaml` updated to reflect new year
- [ ] Checksum stored for next monthly revision check

**After each revision event:**
- [ ] `is_revised: true` in processed record
- [ ] `prior_publication_date`, `prior_value_tonnes`, `revision_reason` all populated
- [ ] New raw file archived alongside original; both retained

**Annually:**
- [ ] Confirm WGC download URL has not changed
- [ ] Confirm ToS still permits automated retrieval
- [ ] Confirm underlying providers (Metals Focus, Refinitiv GFMS) still credited on WGC page
- [ ] Review `config.yaml` plausible range bounds — adjust upper bound if total stock has grown substantially

---

## Ownership and Escalation

| Role | Responsibility |
|---|---|
| Collector developer | Build and maintain `wgc_scraper.py` |
| Operator | Approve `FLAG` and `STALE` records before scoring; handle blocked escalations |
| Chris (proposal author) | Proposal and schema owner; does not build or run collector |

Escalate `FAIL`, `BLOCKED`, and `INSUFFICIENT_EVIDENCE` events immediately. `FLAG` and `STALE` events require operator review before the record may enter scoring.
