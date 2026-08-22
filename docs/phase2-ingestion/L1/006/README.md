# L1-006 — Expected Policy Rate

L1-006 is a near-term market-implied expected effective federal-funds rate. It uses the nearest active CME 30-Day Fed Funds futures contract (ZQ), with `100 - settlement_price` as the implied annualized percent rate. This is one Layer-1 opportunity-cost anchor; the broader expected path and repricing remain Layer-3 variables.

The shared CME collector (`collectors/cme/cme_download.py`) preserves both public interest-rate PDFs and writes SHA-256 manifests. `collectors/cme/cme_extract.py` inspects both sections, selects whichever contains the `30D FED FD FUT` table, and then runs `extract_settlements.py` and `parser.py`. If PDF text changes or access is blocked, the same CSV can be prepared manually as a fallback.

The parser accepts only `ZQ` 30-Day Fed Funds contract codes, skips ineligible or expired contracts, and selects the nearest remaining expiry per observation date. Missing required columns, malformed dates/numbers, duplicate observation/contract rows, or no eligible rows fail clearly. Values outside 0–20% are retained with `FLAG`. Carry-forward is allowed for up to three calendar days with `STALE`; realized EFFR/DFF is not substituted.

Run tests with `pytest -q tests`. A live run requires CME access; if the public bulletin returns 403, retain the failure in the changelog and use the manual PDF download fallback.
