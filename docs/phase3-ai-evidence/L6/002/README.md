# L6-002 Phase 3 evidence retrieval pilot

This directory covers Steps 3 through 5 of the approved L6-002 plan. It produces evidence and score fields but no Phase 4 input.

`retrieval.py` accepts explicitly selected Phase 2 events. It does not read or branch on `is_candidate`; that column remains queryable triage metadata. It respects each host's `robots.txt`, identifies the GoldRush research user agent, queries OFAC Recent Actions first, then the Federal Register API where a legal-authority query is available. It records every attempted URL and stores text only from an official document returned by a successful request.

`scorer.py` applies the accepted deterministic Step 5 rules to retrieval JSON. `silent_monitor.py` runs one live collector → parser → candidate retrieval → scorer snapshot and writes each run as a timestamped JSON record; it sends no notifications and does not activate Phase 4. Repeated silent runs should be externally scheduled and manually audited before activation.
