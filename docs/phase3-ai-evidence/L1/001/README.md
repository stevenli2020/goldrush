# L1-001 — 10Y TIPS Real Yield

Phase 3 uses the live FRED `DFII10` series and the approved Phase 2 parser. The
canonical value is the daily 10-year Treasury inflation-protected security real
yield in percentage points. FRED missing values are skipped, stale observations
remain explicitly marked, and blocked or invalid observations are never
substituted.
