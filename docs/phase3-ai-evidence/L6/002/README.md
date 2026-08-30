# L6-002 Phase 3 evidence retrieval pilot

This directory covers Steps 3 through 5 and the internal Phase 4 handoff for L6-002.

`retrieval.py` accepts explicitly selected Phase 2 events. It does not read or branch on `is_candidate`; that column remains queryable triage metadata. It respects each host's `robots.txt`, identifies the GoldRush research user agent, queries OFAC Recent Actions first, then the Federal Register API where a legal-authority query is available. It records every attempted URL and stores text only from an official document returned by a successful request.

`scorer.py` applies the accepted deterministic Step 5 rules to retrieval JSON. `silent_monitor.py` runs one live collector → parser → candidate retrieval → scorer snapshot. With `--activate-phase4`, it appends an internal dashboard record and emails the research recipients for candidate review. External alerts and trading remain disabled. `mock_phase4_test.py` exercises this path without invoking the collector.
