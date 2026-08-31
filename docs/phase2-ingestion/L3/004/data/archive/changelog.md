# L3-004 Changelog

## 2026-08-24

- Final approval recorded. L3-004 is Complete for the validated next-two-meeting
  production scope, with the third meeting retained as recursive validation.
- Replaced the failed independent-meeting calculation with a cumulative
  probability tree. Conditional adjacent outcomes are recursively convolved;
  October uses the November non-meeting-month settlement anchor.
- Implemented the approved next-two-meeting scope; the third meeting is
  validation-only. No shared framework or completed CME variable changed.
- Passed all nine comparisons for observation dates 2026-08-19 through
  2026-08-21 across September, October, and December. All modal buckets agreed,
  no material bucket was missing, and maximum bucket error/TVD was 0.0178568571.
- Added collector, parser, schema, preserved CME/FRED/schedule inputs and
  manifests, canonical output, and production behavior tests. Status is
  implementation ready for Grace review before final approval.
- Verification commands ran from `/mnt/d/Projects/GoldRush` after activating
  `.venv`: `python -m py_compile` for all three L3-004 scripts; `pytest -q`
  across L3-004, L3-002, L3-003, L1-006, and L3-001; the three-manifest
  validation command documented in README; and the collector/parser commands.
  Results: 15 L3-004 tests and 25 completed CME regressions, 40 combined passed.
- Current collection/parser run produced five `PASS`/`AVAILABLE` rows for CME
  settlement date 2026-08-21: two September outcomes and three October
  outcomes. Both group sums are 1.0; all rows have zero schema errors and every
  raw/manifest source metadata matches.
- Operational replay returned five rows with no revisions. A forced collection
  failure returned the same five rows as `STALE`; no-prior wrote `BLOCKED`; a
  successful recovery removed the blocked artifact. Genuine probability-change
  revision behavior passed its focused test.
- Alternative 1 validation executed with `cme-fedwatch==0.1.3`, trade date
  2026-08-21, and explicit preserved EFFR 3.63%. The official comparison files
  were not modified.
- September passed (maximum error and TVD 0.038571). October failed (maximum
  error and TVD 0.771745; modal mismatch; missing material bucket). December
  failed (maximum error 0.284075; TVD 0.3187885; two missing material buckets).
- Full-scope gate failed. Phase B was not started. Retained the Deferred
  recommendation and recorded that a next-meeting-only scope requires Grace
  approval.
- Added `validate_alternative1.py`, eight focused tests, the machine-readable
  comparison report, explicit EFFR input, and preserved raw package output.
- Compilation passed. L3-004 tests: 8 passed. Combined L3-004/L3-002/L3-003 and
  completed CME regression suite: 33 passed.
- Investigated CME FedWatch public tool, methodology, user guide, and official API access path.
- Official probability output could not be reproducibly collected and preserved without API access; embedded QuikStrike access is referrer/session dependent.
- Recommended Deferred rather than mislabeling futures rates or unvalidated interpolation as observed probabilities.
- Grace review concurred with deferral. Final blocker wording: no approved paid FedWatch API subscription or credentials, and no locally calculated methodology validated against preserved official CME examples.
