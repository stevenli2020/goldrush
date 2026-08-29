# L6-002 Phase 3 evidence retrieval pilot

This directory is limited to Steps 3 and 4 of the approved L6-002 plan. It contains no `value` or `score` field and produces no Phase 4 input.

`retrieval.py` accepts explicitly selected Phase 2 events. It does not read or branch on `is_candidate`; that column remains queryable triage metadata. It respects each host's `robots.txt`, identifies the GoldRush research user agent, queries OFAC Recent Actions first, then the Federal Register API where a legal-authority query is available. It records every attempted URL and stores text only from an official document returned by a successful request.
