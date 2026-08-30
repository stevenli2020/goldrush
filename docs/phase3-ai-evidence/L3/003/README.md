# L3-003 — Expected Terminal Policy Rate

Phase 3 uses the validated L3-002 CME curve. The deterministic endpoint proxy
selects the minimum or maximum rate across the first 12 contracts according to
the observed curve direction, retaining the selected contract and full source
provenance. It is not an official forecast and never uses a substitute value.
