# L3-001 — Fed Funds Futures Expected Policy Rate

Phase 3 uses the CME Fed Funds futures strip from the preserved Section 10
settlement source. The canonical value is the arithmetic average of eligible
contracts one to twelve months ahead, in percent per annum. It is distinct from
L1-006's nearest-contract value. Incomplete or unavailable strips are rejected
and never replaced with L1-006 or another synthetic value.
