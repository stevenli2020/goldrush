# L10-001 Changelog

## 2026-08-22

- Implemented the approved single-variable CFTC collector and parser.
- Locked extraction to contract `088691` and `FutOnly` with the official 191-column layout.
- Added separate validation and availability statuses, report-date freshness, raw preservation, source metadata, manifests, and revision detection.
- Live verification 2026-08-22: one gold row extracted for report date 2026-08-18; managed-money long 154,595, short 12,947, net 141,648 contracts; validation PASS; availability AVAILABLE as of 2026-08-22. Raw source metadata: ``.
- Grace rework 2026-08-23: canonical processed/source field comparison fixed false revisions; source metadata-only retrieval changes no longer count as data revisions; executable fallback now returns the latest valid observation with refreshed AVAILABLE/STALE status or BLOCKED without prior data. Regression suite: 13 passed.
- Grace follow-up 2026-08-23: curl `CalledProcessError` is now caught by the executable fallback path; regression suite expanded to 16 passed.
- Final approval 2026-08-23: compilation passed; 16 tests passed; real curl failure returned FALLBACK with prior observation AVAILABLE; unchanged replay remained `is_revision=False`; live net position remained 141,648 contracts. L10-001 approved Complete.
