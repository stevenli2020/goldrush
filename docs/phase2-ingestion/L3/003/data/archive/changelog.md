# L3-003 Changelog

## 2026-08-24

- Final approval recorded after the L3-002 regression condition passed. L3-003
  is Complete.
- Added the fixed 12-contract terminal-rate proxy consuming L3-002 output.
- Current preserved-curve run selected ZQN27 at 4.015% from an upward curve (nearest 3.63%, farthest of first 12 contracts 4.015%). Source provenance is inherited unchanged from L3-002.
- Package tests cover all three curve directions, first-12 selection, provenance consistency, revisions, fallback, blocked state, and recovery.
- Post-L3-002-rework verification: 6 L3-003 tests passed; combined L3-002/L3-003/completed-CME suite 25 passed. Replay produced one row with zero schema errors and retained the 4.015% ZQN27 result.
