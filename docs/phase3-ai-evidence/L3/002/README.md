# L3-002 — Forward Policy Rate Curve

Phase 3 uses the CME 30-Day Fed Funds futures strip and preserves each
unexpired ZQ contract. The deterministic value is `100 - settlement_price`, in
percent per annum, with contract identity retained so the curve is not reduced
to an ambiguous single point. Missing or unavailable curve data is never
substituted.
