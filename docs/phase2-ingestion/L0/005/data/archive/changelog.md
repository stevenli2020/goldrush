# L0-005 — Bar-and-Coin Investment Holdings / Demand
## Changelog

---

## Version History

### v1 — 2026-08-18 — Initial implementation draft
**Author:** Chris  
**Status:** REVIEWED — NOT COMPLETE. Grace review returned 2026-08-18. See Grace Review Outcome below.

- Proposal drafted: `bar-and-coin-demand.md`
- GDT workbook inspected: `GDT_Tables_Q2'26_EN.xlsx`
- Confirmed sheet structure: `Gold Balance` (rows 20–23) and `Bar and Coin` (rows 44–46)
- Annual coverage confirmed: 2010–2025 (16 years)
- Quarterly coverage confirmed: Q1'10–Q2'26 (66 quarters as of current workbook)
- Sub-component quarterly availability confirmed: bars/coins/medals published at **annual frequency only** in Gold Balance sheet; quarterly records will carry null for sub-components
- Sheet reconciliation confirmed: Gold Balance row 20 total reconciles with Bar and Coin sheet row 46 world total to within floating-point precision (difference: 0.00000001t on 2025 annual)
- Implementation files created: `config.yaml`, `schema.json`, `README.md`, `samples/raw_parsed_sample.json`, `samples/processed_sample.csv`, `archive/changelog.md`

---

## Grace Review Outcome — 2026-08-18

**Decision:** NOT COMPLETE. L0-005 remains `Not done`.

### Blockers returned by Grace

| # | Blocker | Required action |
|---|---|---|
| G1 | Parser missing | Implement `parse_bar_and_coin.py` at one canonical path; `scripts/` and `tests/` directories are empty |
| G2 | No executable test suite | Tests required: annual/quarterly extraction; quarterly null sub-components; sheet reconciliation; negative country-level values; malformed workbook/changed sheet layout; revision detection; stale fallback behavior |
| G3 | No live PASS run | Workbook inspection is not a collector run. A real parse of current workbook must produce 82 records with validation results and an ingest log |
| G4 | Owner still `Chris` in tracker | Must be changed to actual owner/operator once assigned |
| G5 | Tracker collector path inconsistent | Tracker points to `data/parse_bar_and_coin.py`; proposal architecture references same path; must be one canonical path, confirmed by owner |
| G6 | Config ownership fields are placeholders | All `[To be assigned]` in `config.yaml` must be filled before completion |
| G7 | Schema example vs processed sample mismatch | Schema example gives Q2'26 total as `476.77916012`; processed sample gives `307.08301057`; one is wrong — correct both to match actual workbook value |
| G8 | Revision example is invalid | Revision row says "no change detected" but marks `is_revised: true`; a revision record must represent an actual changed value or be removed |
| G9 | Sample SHA-256 placeholders | Acceptable only for clearly labelled fixtures; not acceptable as evidence of a live run |
| G10 | ToS/access decision undocumented | Tracker requires the access decision to be recorded (not just noted as "appears public") |
| G11 | Publication-date procedure has no owner | Responsible operator and evidence source for `source_publication_date` must be assigned |
| G12 | Shared-workbook coordinator unassigned | One-download-per-quarter rule is described but coordinator and handoff process for L0-002, L0-003, L0-006, L8-001 are placeholders |
| G13 | Scope must remain explicit | Implementation produces demand-flow series only; must not silently construct accumulated holdings |

### Acceptance criteria for `Complete`

1. Owner/operator assigned (resolves G4, G6, G11, G12)
2. Parser implemented at one canonical path (resolves G1, G5)
3. Test suite added and passing (resolves G2)
4. Live run of current workbook produces 82 records + ingest log (resolves G3, G9)
5. Samples corrected; Q2'26 total consistent; revision example valid (resolves G7, G8)
6. Config and tracker ownership fields filled (resolves G6)
7. ToS/access decision recorded in tracker (resolves G10)
8. Shared-workbook coordinator confirmed (resolves G12)

---

## Key Findings from Workbook Inspection

| Finding | Detail |
|---|---|
| Annual series | 2010–2025; 16 periods; columns 2–17 in Gold Balance sheet |
| Quarterly series | Q1'10–Q2'26; 66 periods; columns 22–87 in Gold Balance sheet |
| Header row | Row 5 in both Gold Balance and Bar and Coin sheets |
| Sub-components (bars/coins/medals) | Annual only in Gold Balance; not published quarterly |
| Country breakdown | Combined bar-and-coin only (no bar/coin split by country) in Bar and Coin sheet |
| Sheet reconciliation delta (2025) | 0.00000001t — floating-point rounding only; not a data quality issue |
| Q2'26 quarterly total (Gold Balance row 20, col 87) | 307.08301057t — authoritative value; schema example contained wrong value (476.77916012 = Q1'26); to be corrected in G7 |
| Q1'26 quarterly total (Gold Balance row 20, col 86) | 476.77916012t |
| Negative country-level values | Expected in WGC data for net-selling markets; valid; do not flag |
| Data as of | 30 June 2026 |
| Source attribution (row 48) | "Metals Focus, Refinitiv GFMS, ICE Benchmark Administration, World Gold Council" |

---

## Known Limitations

- Sub-components (Bars, Official Coins, Medals/Imitation Coins) published at **annual frequency only**. Quarterly records carry null for these three fields.
- Country-level breakdown in Bar and Coin sheet provides combined total only — no bar/coin split by country.
- WGC does not publish a formal revision calendar. Revision detection relies on SHA-256 comparison between workbook downloads.
- `source_publication_date` must be recorded manually by the operator at download time.
- Automated download has not been validated against WGC Terms of Service. Current method is manual download only.
- This implementation produces a **demand-flow series only**. It does not construct or maintain accumulated holdings stock. Any such transformation requires explicit architecture approval.

---

## Pre-Production Blockers (consolidated — Grace review + original)

| # | Blocker | Status | Owner | Resolution criteria |
|---|---|---|---|---|
| B1 | `parse_bar_and_coin.py` not implemented | OPEN | Collector developer (unassigned) | Script built at canonical path; tested against `GDT_Tables_Q2'26_EN.xlsx` |
| B2 | WGC ToS compliance not formally recorded | OPEN | Operator (unassigned) | Written decision recorded in tracker: confirmed permitted or escalated |
| B3 | `source_publication_date` recording process has no owner | OPEN | Operator (unassigned) | Responsible operator named; evidence source documented |
| B4 | Owner/operator unassigned | OPEN | APROXI | All `[To be assigned]` in config.yaml and tracker filled |
| B5 | No live parse with validated `PASS` result | OPEN | Collector developer + operator | Full parse of current workbook produces 82 PASS records; ingest log present |
| B6 | Shared-workbook coordinator unassigned | OPEN | APROXI | Named coordinator; handoff process documented for L0-002, L0-003, L0-006, L8-001 |
| B7 | No test suite | OPEN | Collector developer | Tests written and passing for all 7 cases listed in Grace review |
| B8 | Schema/sample Q2'26 value mismatch | OPEN | Chris | Schema example corrected to 307.08301057t; processed sample consistent |
| B9 | Revision example invalid | OPEN | Chris | Revision row replaced with actual changed-value example or removed |

**Unblocking sequence:**
1. APROXI assigns owner/operator (B4) — gates B2, B3, B6
2. Owner confirms canonical parser path (B1, gates B5, B7)
3. Owner confirms ToS decision (B2)
4. Owner assigns shared-workbook coordinator (B6)
5. Owner assigns publication-date responsibility (B3)
6. Chris corrects schema/sample errors (B8, B9) — can proceed immediately
7. Collector developer builds parser + tests (B1, B7)
8. Live run executed; 82 PASS records + ingest log (B5)
9. Report to APROXI → Grace re-review → `Complete`

---

## Ingest Log (production — append on each run)

| Run date | Workbook | Annual records | Quarterly records | PASS | FLAG | FAIL | Revisions | Operator |
|---|---|---|---|---|---|---|---|---|
| [First live run pending B1–B7] | — | — | — | — | — | — | — | — |
