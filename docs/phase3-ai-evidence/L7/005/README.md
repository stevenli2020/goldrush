# L7-005 Phase 3 handoff

The handoff preserves the deterministic repo-funding proxy `(SOFR - EFFR) *
100` in basis points. Only dates present in both official New York Fed series
are emitted; neither rate is carried across a missing date. Positive values
mean secured Treasury repo funding is above unsecured federal funds. This is a
narrow proxy, not a complete repo-stress index.
