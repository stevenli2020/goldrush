# L2-002 — Broad Trade-Weighted Nominal US Dollar Index

Phase 3 uses the official FRED `DTWEXBGS` series from the H.10 Foreign Exchange
Rates release. The canonical value is the not-seasonally-adjusted index with
January 2006 equal to 100. Missing observations are skipped, stale status is
preserved explicitly, and no synthetic value is created.
