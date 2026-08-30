# L1-007 — 5Y5Y Forward Real Rate

Phase 3 uses aligned FRED `DFII5` and `DFII10` observations. The deterministic
value is the compounded 5Y5Y real-forward approximation documented in the Phase
2 package. Missing input dates are not interpolated; stale or blocked status is
preserved explicitly and no substitute value is used.
