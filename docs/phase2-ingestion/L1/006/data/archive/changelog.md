# L1-006 Changelog

## 2026-08-21

- Definition approved: nearest active CME 30-Day Fed Funds futures implied rate.
- Formula: `100 - settlement_price`; realized EFFR/DFF is not an equivalent fallback.
- Package created with separate PDF preservation downloader and normalized-settlement parser.
- Live verification completed; closure recorded below.

## Verification attempt — 2026-08-21

- Parser tests: **3 passed**.
- Live CME Section 10 download attempted with browser-like headers; endpoint returned HTTP 403 in the current environment.
- No live raw PDF, source metadata, or processed production output is claimed. Manual browser download remains the documented fallback.

## Deferred revisit — 2026-08-21

- Optional enhancement deferred: test a WGC-style `curl_cffi` browser-impersonated
  session with a protected local CME cookie jar.
- Cookies must remain local-only; credentials/session cookies must never be printed,
  committed, or shared.
- Current operation remains scripted download first, then manual browser PDF
  placement when CME returns 403. This fallback was exercised successfully.

## Rework — 2026-08-21

- Downloader now rejects non-200 responses and content without a `%PDF` signature before saving.
- Schema now includes emitted source fields and declares `retrieved_at` as date-time.
- Parser now validates `ZQ` contract codes, ISO dates, expiry eligibility, duplicates, and empty selections.
- Regression suite: **7 passed**, including duplicate observation/contract rejection.

## Extraction adapter — 2026-08-21

- Added `extract_settlements.py` to convert preserved Section 10 PDFs into normalized ZQ settlement CSVs.
- Confirmed from supplied files that Section 09 contains Treasury futures while Section 10 contains `30D FED FD FUT`; only Section 10 is required for L1-006.

## Live evidence — 2026-08-21

- Preserved manual CME Section 10 PDF: `data/raw/section10-manual-20260820.pdf`.
- source metadata: ``.
- Normalized 17 ZQ rows; parser selected `ZQQ26` for observation date `2026-08-20`.
- Parsed output: `3.63%` per annum; validation `PASS`; availability `AVAILABLE`.
- Processed output: `data/processed/L1_006_observations.csv`.
- Evidence was ready for final closure review.
- Two supplied CME interest-rate PDFs were compared. Section 09 contained no `30D FED FD FUT` rows and was removed from the temporary folder; Section 10 is the retained source for L1-006.

## Orchestration rework — 2026-08-21

- `cme_extract.py` now inspects every preserved section for the required marker before selecting a source.
- A marker-free section is logged as `INSPECTED_UNUSED`; both raw PDFs remain preserved.
- Added a normalized shared-manifest record for the manual Section 10 artifact so `cme_extract.py` can discover it when no newer automated manifest exists.
- The routine path is now download → preserve/source metadata → extract → parse; manual normalization remains fallback only.

## Closure — 2026-08-21

- Final approver approved L1-006 as **Complete**.
- Variable-level live evidence and shared CME orchestration integration are accepted for the approved personal trade-advisor scope.
- Future improvement: make `cme_extract.py --force` control reruns consistently with the downloader; non-blocking.

## 2026-08-29 — Phase 3 live verification and downloader approval

- Refreshed CME cookies restored live access.
- Live downloader returned `PASS` for Sections 09, 10, 62, and 02B.
- L1-006 selected Section 10, extracted 19 contracts, and selected nearest active contract `ZQQ26`.
- Settlement `96.37` produced `3.63%` per annum using `100 - settlement_price`; validation `PASS`, availability `AVAILABLE`.
- Downloader now uses bounded retries, a 30-second timeout, CME HTTPS-domain validation, PDF validation, atomic raw writes, and non-zero failure for missing targets.
- Unchanged PDFs are detected through direct byte comparison; no hash is calculated or stored.
- Focused downloader tests: **3 passed**. Final approver approved the downloader revision.
