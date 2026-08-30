# L6-002 Phase 3 evidence retrieval pilot

This directory covers Steps 3 through 5 and the internal Phase 4 handoff for L6-002.

`retrieval.py` accepts explicitly selected Phase 2 events. It does not read or branch on `is_candidate`; that column remains queryable triage metadata. It respects each host's `robots.txt`, identifies the GoldRush research user agent, queries OFAC Recent Actions first, then the Federal Register API where a legal-authority query is available. It records every attempted URL and stores text only from an official document returned by a successful request.

`scorer.py` applies the accepted deterministic Step 5 rules to retrieval JSON. `silent_monitor.py` runs one live collector → parser → candidate retrieval → scorer snapshot. With `--activate-phase4`, it appends an internal dashboard record and emails the research recipients for candidate review. External alerts and trading remain disabled. `mock_phase4_test.py` exercises this path without invoking the collector.

## Approved production state

Owner approval was recorded on 2026-08-30 after the controlled Bank Markazi
mock candidate test. The mock produced `30/100` with breakdown
`0/30/0/0`, sent a `[TEST]` research notification accepted by Gmail, and
wrote a dashboard record with `human_review_required: true`. A subsequent live
run verified production mode with `human_review_required: false`.

The production notification path is internal research use only. It writes
`live-monitor/phase4-dashboard.jsonl` and sends candidate records to the two
configured research recipients. `external_alerts_enabled` and
`trading_enabled` are explicitly `false`. SMTP credentials are read from the
local ignored `docs/phase3-ai-evidence/credentials.json` file and are never
committed.

The Windows task `GoldRush-L6-002-SilentMonitor` runs the WSL pipeline with
`--activate-phase4`. The former app-level silent-only automation is paused.
The source-available fixtures, Syria reversal result, Bank Markazi validation,
mock test, dashboard record, and WSL test output are supporting evidence; the
canonical Phase 4 record remains the lean scored output.
