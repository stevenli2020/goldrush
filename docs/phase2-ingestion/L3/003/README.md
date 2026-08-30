# L3-003 — Expected Terminal Policy Rate

**Status:** Complete — approved 2026-08-24.

This parser consumes the validated L3-002 curve; it does not download CME data.
It examines the first 12 eligible monthly contracts. If the farthest rate is
below the nearest, it selects the minimum; if above, it selects the maximum; if
equal, it selects the farthest rate.

The result is a transparent futures-curve endpoint proxy, not an official
forecast. Source PDF, manifest, URL, source metadata, publication date, and retrieval time
are inherited from L3-002. Fallback returns the latest valid observation as
`STALE`; no prior observation produces a machine-readable `BLOCKED` artifact.
Successful recovery clears the artifact. No dates are synthesized.
