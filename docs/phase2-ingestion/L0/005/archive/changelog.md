# L0-005 — Bar-and-Coin Investment Holdings / Demand
## Changelog

---

## Version History

### v2 — 2026-08-19 — Blockers resolved; live run completed
**Author:** Chris  
**Status:** COMPLETE — approved and closed

**Resolved since v1:**
- B1: `parse_bar_and_coin.py` implemented at `docs/phase2-ingestion/L0/005/data/parse_bar_and_coin.py`
- B2: WGC ToS compliance confirmed by APROXI 2026-08-18
- B3: `source_publication_date` recorded via `--publication-date` CLI argument; operator supplies at run time
- B4: Owner/operator assigned to Chris
- B5: Live parse completed 2026-08-19; 82 records, 82 PASS, 0 FLAG, 0 FAIL
- B6: Shared-workbook coordinator assigned to Grace
- B7: 20-test suite written and passing (20/20)
- B8: Schema Q2'26 example corrected to 307.08301057t
- B9: Revision example replaced with genuine value-change scenario

### v3 — 2026-08-19 — Grace re-review and final approval
**Status:** COMPLETE — officially closed

- Grace re-review accepted the proportional, personal-project implementation.
- Final approver approved L0-005 for closure on 2026-08-19.
- Tracker status updated to `Complete`.
- No unresolved implementation blockers remain.

### v1 — 2026-08-18 — Initial implementation draft
**Author:** Chris  
**Status:** REVIEWED — NOT COMPLETE (Grace review returned 9 blockers)

---

## Grace Review Outcome — 2026-08-18

**Decision:** NOT COMPLETE. 9 blockers returned. See v1 for full blocker list.  
**Re-review:** Required. Submitted for Grace re-review 2026-08-19.

---

## Key Findings from Workbook Inspection

| Finding | Detail |
|---|---|
| Annual series | 2010–2025; 16 periods |
| Quarterly series | Q1'10–Q2'26; 66 periods |
| Header row | Row 5 in both sheets |
| Sub-components (bars/coins/medals) | Annual only; null for all quarterly records |
| Country breakdown | Combined total only; no bar/coin split by country |
| Sheet reconciliation delta (2025) | 0.00000001t — floating-point only |
| Q1'26 quarterly total | 476.77916012t |
| Q2'26 quarterly total | 307.08301057t |
| Data as of | 30 June 2026 |
| Source attribution | Metals Focus, Refinitiv GFMS, ICE Benchmark Administration, World Gold Council |

---

## Known Limitations

- Sub-components (Bars, Official Coins, Medals/Imitation Coins) published at annual frequency only
- Country breakdown in Bar and Coin sheet: combined total only; no bar/coin split by country
- No formal WGC revision calendar; revision detection relies on source metadata comparison
- `source_publication_date` supplied manually via CLI at run time; operator must verify against WGC press release
- This implementation produces a **demand-flow series only**; no accumulated holdings stock is constructed

---

## Pre-Production Blockers

| # | Blocker | Status | Resolution |
|---|---|---|---|
| B1 | `parse_bar_and_coin.py` not implemented | CLOSED | Implemented 2026-08-19 |
| B2 | WGC ToS compliance unconfirmed | CLOSED | Confirmed by APROXI 2026-08-18 |
| B3 | Publication-date process has no owner | CLOSED | CLI `--publication-date` argument; operator supplies at run time |
| B4 | Owner unassigned | CLOSED | Chris assigned 2026-08-18 |
| B5 | No live PASS run | CLOSED | 82 records, 82 PASS — 2026-08-19T03:15:44Z |
| B6 | Shared-workbook coordinator unassigned | CLOSED | Grace assigned 2026-08-18 |
| B7 | No test suite | CLOSED | 20 tests written and passing 2026-08-19 |
| B8 | Schema Q2'26 value mismatch | CLOSED | Corrected to 307.08301057t |
| B9 | Revision example invalid | CLOSED | Replaced with genuine value-change scenario |

---

## Ingest Log

| Run date | Workbook | Annual | Quarterly | PASS | FLAG | FAIL | Revisions | source metadata | Operator |
|---|---|---|---|---|---|---|---|---|---|
| 2026-08-19T03:15:44Z | GDT_Tables_Q2'26_EN.xlsx | 16 | 66 | 82 | 0 | 0 | 0 |  | Chris |
