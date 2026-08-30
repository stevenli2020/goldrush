# L1-006 — Expected Policy Rate

L1-006 is a near-term market-implied expected effective federal-funds rate. It uses the nearest active CME 30-Day Fed Funds futures contract (ZQ), with `100 - settlement_price` as the implied annualized percent rate. This is one Layer-1 opportunity-cost anchor; the broader expected path and repricing remain Layer-3 variables.

The shared CME collector (`collectors/cme/cme_download.py`) uses the protected local cookie session, bounded retries, CME-domain validation, PDF validation, byte-level unchanged-file comparison, raw preservation, and source metadata manifests. It does not calculate or store file hashes. `collectors/cme/cme_extract.py` inspects the preserved sections, selects the section containing the `30D FED FD FUT` table, and then runs `extract_settlements.py` and `parser.py`. If CME expires the session, refresh the local cookies and rerun; preserved source input remains the documented fallback.

The parser accepts only `ZQ` 30-Day Fed Funds contract codes, skips ineligible or expired contracts, and selects the nearest remaining expiry per observation date. Missing required columns, malformed dates/numbers, duplicate observation/contract rows, or no eligible rows fail clearly. Values outside 0–20% are retained with `FLAG`. Carry-forward is allowed for up to three calendar days with `STALE`; realized EFFR/DFF is not substituted.

Run variable tests with `pytest -q tests` and downloader tests with `pytest -q ../../collectors/cme/tests/test_cme_download.py`. A live run requires valid CME cookies. Access failures must remain explicit and must not produce a substitute value.
