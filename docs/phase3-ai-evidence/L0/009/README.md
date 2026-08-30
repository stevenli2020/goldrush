# L0-009 — Gold Lease Rates / Forward Rates

Phase 3 uses the CME Section 62 gold futures settlement pair and FRED
`SOFR90DAYAVG`. The deterministic value is the annualized gold futures forward
rate minus the 90-day average SOFR, expressed as percent per annum. The
transformation selects the most recent common completed date present in both
inputs; if no common date exists, the result is blocked rather than
substituted.
