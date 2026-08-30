# Phase 3 closure record

## Owner freeze and Phase 4 handoff — 2026-08-30

The owner explicitly confirmed Phase 3 **APPROVED, FROZEN AND CLOSED** and authorized preparation for Phase 4.

- All 44 variable tracker rows are Complete.
- The frozen canonical dataset contains 43 AVAILABLE records, one FLAG record (L3-006, LOW_COVERAGE), zero STALE records, and zero BLOCKED records.
- All checks in the final integration report passed. The canonical dataset SHA-256 was independently rechecked at freeze and matches the value below.
- L3-006, L6-001, and L6-002 remain completed and approved. The old manual L3-006 stance prototype is superseded; the retained coverage flag does not reopen its approval.
- Preserve the closure dataset, register, report, and supporting provenance as the approved baseline. Do not overwrite this snapshot when creating future refresh outputs.
- Phase 4 owns downstream scoring, not upstream source or qualitative-method redesign. Any required upstream change must be reported separately and explicitly approved by the owner before implementation.
- This is a documented project freeze, not a Git commit, tag, or filesystem write lock. Existing unrelated worktree changes remain untouched.

## Canonical dataset

- Dataset: [canonical_dataset.jsonl](canonical_dataset.jsonl)
- SHA-256: `e0d9ed88eef2dce66ee1edf81a65425bcc19b994b20b4865eb53ad3c74a3c2ce`
- Register: [variable_register.json](variable_register.json)
- Integration evidence: [integration_check_report.md](integration_check_report.md)
- Builder and validation logic: [build_phase3_closure.py](build_phase3_closure.py)
- Variable-level source, transformation, and handoff records: [Phase 3 tracker](../PHASE3-TRACKER.md)

## Included variables

`L0-001`, `L0-002`, `L0-003`, `L0-005`, `L0-006`, `L0-009`, `L1-001`,
`L1-002`, `L1-003`, `L1-005`, `L1-006`, `L1-007`, `L2-001`, `L2-002`,
`L2-003`, `L3-001`, `L3-002`, `L3-003`, `L3-004`, `L3-005`, `L3-006`,
`L4-001`, `L4-002`, `L4-003`, `L4-004`, `L4-006`, `L4-007`, `L4-008`,
`L4-009`, `L5-001`, `L5-002`, `L5-003`, `L5-006`, `L6-001`, `L6-002`,
`L7-001`, `L7-003`, `L7-004`, `L7-005`, `L8-001`, `L9-001`, `L9-004`,
`L10-001`, and `L10-002`.

All 44 IDs are present exactly once. Each canonical source reference identifies
the selected transformed output and its preserved source reference.

## Live-refresh evidence

A fresh live-refresh pass was performed on **2026-08-30**. Collectors and
transformation parsers were run against the latest available source data; the
canonical records use the resulting refreshed outputs or explicit blocked-status
evidence. Observation timestamps represent the latest source observation, not
the retrieval time.

## Known limitations

- **Final status counts:** 43 `AVAILABLE`, 0 `STALE`, 1 `FLAG` (L3-006), and
  0 `BLOCKED`.

- **Cadence-aware freshness:** Staleness is now determined by each source's
  release frequency, publication lag, observation-date convention, and a small
  cadence tolerance—not by one global age threshold. The register retains the
  previous `max_age_days` values for historical compatibility.
- **Source-limited lag cleared (4):** L1-003, L1-005, L2-002, and L2-003 are
  now `AVAILABLE` with `OK`. Their 30 August source snapshots were verified
  to contain no observation newer than 21 August 2026; the source had not
  published newer data, so their age is not collector lag.
- **Processing lag fixed (1):** L2-001 is now `AVAILABLE` with `OK`. The
  30 August Yahoo/yfinance snapshot contained completed observations through
  27 August 2026, but the prior processed artifact had fallen back to the 21
  August row after treating an incomplete bar as a fatal parse error. The
  parser now skips incomplete bars and retains later completed rows. The
  canonical value is 99.16000366210938 for 27 August 2026.
- **Previously reclassified to available (7):** L4-001, L4-002, L4-006,
  L4-007, L4-008, L5-003, and L7-003 remain `AVAILABLE`. Their observations
  are within the documented monthly, annual, or quarterly publication-lag
  windows.
- **Date-alignment fix:** L0-009 was previously blocked because the latest CME
  and SOFR observations had different dates. The approved transformation now
  selects the most recent common completed date, 28 August 2026, using CME
  forward rate 4.778430794442623% and SOFR 3.64347%. The resulting spread is
  1.1349607944426228 percentage points and is now `AVAILABLE` with `OK`.
  The earlier refresh status artifact is retained as historical evidence of
  the pre-alignment failure; it is not used by the current closure builder.
- **Flagged (1):** L3-006 is `FLAG` with `LOW_COVERAGE`. Its 0–100
  communication score uses the documented baseline/jury rules and retains its
  source evidence; the flag communicates incomplete baseline coverage.
- **Manual freshness review:** L0-002, L3-004, L3-005, L3-006, L5-002,
  L6-001, L6-002, and L9-001 have timing that is as-published, event-driven, or
  otherwise not safely reducible to a fixed release schedule. Their original
  statuses were preserved pending confirmation of publication lag.
- **Qualitative encodings:** L3-006, L6-001, and L6-002 use their documented
  deterministic scoring thresholds. L6-002's current zero reflects a completed
  official OFAC delta run with no active qualifying candidate, not an absent or
  substituted observation.
- **Source revisions:** delayed official releases and source revisions may
  revise historical observations. The dataset preserves source references so a
  future closure run can be compared directly with this snapshot.

- **Source-availability-aware verification:** the register records the source
  verification time, latest source observation, and whether newer source data
  existed for the five formerly stale records. A source snapshot with no
  newer observation is not treated as a collector failure; a newer uncaptured
  observation is explicitly classified as `COLLECTOR_LAG`.

## Phase 4 readiness

The Phase 3 canonical dataset contains 44 records, all traceable to approved
sources and transformations. No invented substitute values are present. All
stale, blocked, and flagged records are explicitly marked. Phase 4 may consume
this dataset as its common input layer without reference to individual
collection or scoring implementations.
