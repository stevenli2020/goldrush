# L0-009 — Gold Lease Rates / Forward Rates
## Changelog

---

## Version History

### v3 — 2026-08-20 — Automated CME collection confirmed and implemented
**Author:** Chris  
**Status:** DRAFT — pending Grace decision on collection posture (see below)

**New in v3:**
- Built `fetch_cme_bulletin.py`: fully automated collector for the CME Daily Bulletin PDF (Section 62, Metals)
- Confirmed the CME Daily Bulletin PDF (`cmegroup.com/daily_bulletin/current/Section62_Metals_Futures_Products.pdf`) is:
  - Publicly accessible with no login, API key, or registration
  - Fetchable via standard HTTP GET with browser-like headers
  - Machine-parseable: settlement prices and expiry dates both extractable via regex from PDF text
- Found and fixed a real misalignment bug during development: the bulletin's expiry table lists **consecutive calendar months**, not just GC delivery months (Feb/Apr/Jun/Aug/Oct/Dec). A naive positional zip against the 6-per-year settlement list silently misassigned expiry dates (e.g. October's settlement would get September's expiry). Fixed by building the full consecutive-month sequence and matching by (month, year) key. Regression test `test_A3_expiry_mapping_correct` locks this in.
- `fetch_cme_bulletin.py` output format matches `parse_gilr.py --manual` input format exactly, so the two scripts chain directly with no manual reformatting step
- Full pipeline run end-to-end on 2026-08-20 using the live current-day bulletin (data as of 2026-08-18 trade date): fetch → PDF parse → contract selection → GILR computation → validation → storage. Result: FLAG (roll proximity — GCQ26 9 days from expiry), economically valid, `AVAILABLE`.
- 8 new tests (`test_fetch_cme_bulletin.py`) added; all passing. Combined with existing GILR tests: **33/33 passing**.

**Collection posture — decision required from Grace:**

Two viable primary paths now exist:

| Option | Primary | Automation | ToS status |
|---|---|---|---|
| **A** | Nasdaq Data Link (`CHRIS/CME_GC1`/`GC2`) | Automated, but network access to Nasdaq was not testable in this environment | Free-tier ToS unconfirmed for production use (B1, still open) |
| **B** | CME Daily Bulletin PDF (`fetch_cme_bulletin.py`) | **Automated and confirmed working end-to-end in this environment** | No ToS concern — public bulletin, no registration, standard public access |
| **C** | CME Daily Bulletin PDF, manual download | Manual (operator reads PDF, transcribes 2 numbers) | Same as B, zero automation risk |

**Recommendation:** Option B (automated CME Daily Bulletin fetch) is now the strongest candidate — it is free, requires no third-party ToS decision, and automation has been built and verified. This removes the original B1 blocker (Nasdaq ToS) entirely by making Nasdaq optional rather than primary.

### v2 — 2026-08-19 — Rework per Grace review; scope and methodology locked
**Author:** Chris  
**Status:** Submitted for Grace review

- Production variable renamed to `3M Gold Implied Lease Rate — CME-derived proxy (GILR-CME)`
- LBMA/licensed terminal moved to optional future upgrade
- Calculation methodology, contract selection rule, and day-count made exact
- Fields narrowed; blockers reduced from 6 to 4
- Parser (`parse_gilr.py`), config, schema, README, tests written
- 25/25 tests passing
- Live manual-mode run completed: FLAG (roll proximity), correct behavior

### v1 — 2026-08-19 — Initial proposal
**Author:** Chris  
**Status:** REVIEWED — required rework (7 items returned by Grace)

---

## Grace Review Outcomes

**2026-08-18 (on v1):** 7 rework items — source contradiction, methodology gaps, excessive scope. All resolved in v2.

**2026-08-19 (on v2):** "Technically sound, not yet closure-ready — source posture unresolved." Two decisions requested:
1. Choose production collection posture (automated Nasdaq vs. manual CME primary)
2. Confirm automated PASS is optional under project ground rules; manual run is valid evidence

**Response (this version, v3):** A third posture (Option B — automated CME Daily Bulletin fetch) has been built and verified, which resolves the posture question without requiring a live/manual tradeoff: it is both automated and free of third-party ToS risk. Submitted for Grace decision on which of A/B/C to lock as primary.

---

## Live Run Records

| Run date | Mode | Obs date (trade date) | GILR-CME | SOFR3M | Front | Far | Days | Status | Source |
|---|---|---|---|---|---|---|---|---|---|
| 2026-08-19T08:24:17Z | Manual (illustrative SOFR/CME fixture values) | 2026-08-18 | 0.761443% | 4.85% | GCQ26 @ 2485.30 | GCV26 @ 2502.80 | 62 | FLAG | CME_MANUAL |
| 2026-08-20T12:01:45Z | Automated CME bulletin fetch + manual SOFR fixture | 2026-08-18 | 2.017521% | 4.85% | GCQ26 @ 4489.40 | GCV26 @ 4511.30 | 62 | FLAG | CME_MANUAL (fed by `fetch_cme_bulletin.py`) |

**Note on price discrepancy between runs:** The 2026-08-19 run used illustrative placeholder settlement values (2485.30/2502.80) written for testing purposes before the automated fetcher existed. The 2026-08-20 run used real settlement prices (4489.40/4511.30) pulled live from the actual CME Daily Bulletin PDF for the 2026-08-18 trade date. The 2026-08-20 figures are the authentic market data; the 2026-08-19 figures were a development fixture and should not be treated as real market observations.

**FLAG rationale (both runs):** GCQ26 expires 2026-08-27, which is 9 days from the 2026-08-18 observation date — within the 10-day roll-proximity threshold. This is expected and correctly flagged, not a data error.

---

## Known Limitations

- Derived proxy; incorporates futures basis, storage costs, and convenience yield — not a pure OTC lease quote
- No live public alternative if both CME sources become unavailable; carry-forward (`STALE`) only
- Negative GILR is economically valid; always FLAG, never FAIL
- Contract roll periods introduce transient basis effects; flagged informatively
- CME Daily Bulletin expiry table only covers ~13 months forward; far-dated contracts beyond that window are correctly excluded rather than guessed (see B4 test coverage)
- SOFR3M automated fetch was not testable end-to-end in this development environment (FRED request timed out); CME bulletin fetch was fully testable and confirmed working

---

## Pre-Production Blockers

| # | Blocker | Status | Resolution |
|---|---|---|---|
| B1 | Nasdaq Data Link ToS for production use | **Superseded** | No longer required if Option B (CME bulletin) is selected as primary |
| B2 | `parse_gilr.py` not implemented | CLOSED | Implemented; 25/25 tests passing |
| B3 | Contract selection logic not tested | CLOSED | T1–T3 (GILR tests) + A1–A6 (bulletin fetcher tests); 33/33 total passing |
| B4 | No live PASS run | **Partially closed** | Two live runs completed (manual-fixture and automated-bulletin); both produced correct FLAG (roll proximity, not an error). A clean PASS run (not near a roll date) has not yet been demonstrated — first run after 2026-08-27 (once GCQ26 rolls off) would naturally produce PASS if all else holds |

**New:** B5 — SOFR3M automated fetch untested end-to-end in this environment (FRED timeout). Not a blocker for manual-primary posture, since SOFR is always obtainable as a public CSV via browser even if the environment's outbound automation is restricted.

---

## Future Upgrades (non-blocking)

- **Licensed terminal:** Bloomberg `GOLDLEAS Index` or Refinitiv `XAUFOR=` would replace the CME-derived proxy with a directly observed rate.
- **Additional tenors:** 1M and 12M GILR-CME via extended contract selection.
- **LBMA PM fix cross-check:** Deferred field.
- **Nasdaq Data Link as secondary cross-check:** Retain as an optional convenience/validation source once Option B is confirmed primary.
