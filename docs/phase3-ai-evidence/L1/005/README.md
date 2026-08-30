# L1-005 — Treasury Term Premium

Phase 3 uses the live FRED `THREEFYTP10` series, a Board of Governors model-
derived estimate of the 10-year Treasury term premium. The canonical value is
in percentage points. Missing values are skipped, stale observations remain
explicitly marked, and blocked or invalid observations are never substituted.
