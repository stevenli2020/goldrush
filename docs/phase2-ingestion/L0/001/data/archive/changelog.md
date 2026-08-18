# L0-001 — Above-Ground Gold Stock
## Changelog and Phase 2 Readiness Checklist

---

## Version History

### v2 — 2026-08-18 — Proposal approved; implementation files created
**Author:** Chris
**Status:** Implementation complete; awaiting collector build and source-locking validation

Changes from v1 (proposal):
- WGC historical coverage corrected to 2010–2025 (was incorrectly stated as ~1900–present)
- USGS removed as a production fallback; explicitly excluded from pipeline; noted as mine-production data only
- Fallback redefined as carry-forward only with `availability_status: STALE`
- Methodology PDF reclassified as lineage/reference material, not a live source
- Revision semantics corrected: `is_revised` scoped to same `observation_year`; three revision fields (`prior_publication_date`, `prior_value_tonnes`, `revision_reason`) added as conditional-required
- Arbitrary `–2% to +3%` year-on-year validation bound removed; replaced with operator-review flag
- Collector reuse claim corrected: `wgc_scraper.py` does not exist; flagged as new shared adapter required
- `raw/` production archive separated from `samples/` fixtures
- Update cadence corrected to annual release detection plus monthly checksum check
- `availability_status: AVAILABLE` added as explicit value for passing records
- `FLAG` records: may be archived and staged; must not enter scoring without operator approval
- Implementation files created: `config.yaml`, `schema.json`, `README.md`, `samples/raw_wgc_sample.json`, `samples/processed_sample.csv`, `archive/changelog.md`

### v1 — 2026-08-18 — Initial proposal submitted
**Author:** Chris
**Status:** Reviewed; 8 feedback items returned; revised to v2

---

## Known Limitations

- WGC dataset covers 2010–2025 only. No directly retrievable annual series exists before 2010 from this source. Historical reconstruction before 2010 is out of scope for production ingestion.
- Automated access to the WGC `.xlsx` download has not been validated. The download URL may be restricted; this must be confirmed before production use.
- `wgc_scraper.py` does not yet exist. All implementation files assume it will be built to the interface defined in this proposal.
- WGC publishes bars, coins, and gold-backed ETFs as a single combined sub-component in this dataset. The split between bar/coin and ETF is not available here; use L0-003 and L0-005 for granular breakdowns.
- WGC does not publish a formal revision calendar. Revision detection relies on monthly checksum monitoring, which may miss out-of-cycle corrections published outside the main file.

---

## Phase 2 Readiness Checklist

### Proposal
- [x] Variable is ADMIT in Phase 1 registry
- [x] All 6 proposal sections complete
- [x] Primary source named with endpoint URL
- [x] Fallback defined and correctly scoped (carry-forward only)
- [x] Collector identified (`wgc_scraper.py`, new adapter required)
- [x] All required fields in observation record
- [x] Validation bounds specified; arbitrary percentage rule removed
- [x] All 5 missing-data statuses covered; `AVAILABLE` defined for passing records
- [x] `FLAG` handling documented: archive, stage, no scoring without operator approval
- [x] Reuse check completed; collector existence status corrected
- [x] No historical data fabricated
- [x] No Phase 1 admission decisions modified

### Implementation files
- [x] `above-ground-stock.md` — approved proposal
- [x] `data/config.yaml` — collector config, endpoints, validation bounds, storage paths
- [x] `data/schema.json` — JSON Schema draft-07 with two full example records
- [x] `data/README.md` — quick start, full workflow, fallback, error handling, troubleshooting, maintenance checklist
- [x] `data/samples/raw_wgc_sample.json` — realistic parsed payload fixture
- [x] `data/samples/processed_sample.csv` — 4 rows: 2 clean, 1 revision (PASS), 1 revision (FLAG)
- [x] `data/archive/changelog.md` — this file

### Pre-production blockers — OPEN (required before going live)

All five blockers below must be resolved and signed off before L0-001 moves to production ingestion.

| # | Blocker | Status | Owner | Notes |
|---|---|---|---|---|
| B1 | `collectors/wgc_scraper.py` not implemented or tested | OPEN | Collector developer (unassigned) | Script does not exist. Must be built, unit-tested against `samples/raw_wgc_sample.json`, and validated end-to-end before any production run. |
| B2 | WGC download stability, automated retrieval permission, and ToS compliance unverified | OPEN | Collector developer + legal/ops review | WGC GoldHub download URL has not been confirmed stable. Automated scraping permission and ToS compliance have not been checked. Must be verified before any automated retrieval is scheduled. |
| B3 | WGC methodology PDF not archived locally | OPEN | Operational owner (unassigned) | Methodology lineage documentation has not been downloaded and stored. Required for audit trail and historical reconstruction reference. Archive to `data/archive/wgc_methodology.pdf`. |
| B4 | Collector developer and operator contact unspecified | OPEN | APROXI / project management | `config.yaml` `ownership` section contains placeholder `[To be assigned]` for all roles. Must be filled before production scheduling. |
| B5 | No live collection with a validated `PASS` result completed | OPEN | Collector developer + operational owner | No end-to-end test against the live WGC endpoint has been run. A full dry-run producing a `validation_status: PASS` record is required before production scheduling. |

**Unblocking sequence:**
1. Assign collector developer and operator (B4) — enables all other work
2. Verify WGC ToS and download stability (B2)
3. Build and unit-test `wgc_scraper.py` (B1)
4. Archive WGC methodology PDF (B3)
5. Execute live dry-run; confirm `PASS` (B5)
6. Report resolution to APROXI → Grace final sign-off → status = LOCKED
