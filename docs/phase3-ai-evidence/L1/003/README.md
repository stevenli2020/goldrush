# L1-003 — Forward Real Rates

Phase 3 uses the live Federal Reserve GS&W zero-coupon TIPS curve. The parser
calculates five documented forward-rate components from the six required
maturities and emits their arithmetic mean in percent per annum. Missing inputs
are not interpolated. Source freshness is preserved explicitly; stale values
remain `STALE` and are never presented as current.
