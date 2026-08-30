# L4-009 Phase 3 handoff

The handoff preserves the deterministic share of total marketable Treasury
debt maturing after each MSPD record date and within one calendar year. The
numerator and denominator remain source-derived in Phase 2 evidence; the
canonical value is percent of marketable Treasury debt. No maturity estimate
or synthetic observation is introduced.

Daily operation uses a rolling 24-month Treasury collection window. The
126-year full-history query is optional archival/backfill work and is not part
of the daily production path.
