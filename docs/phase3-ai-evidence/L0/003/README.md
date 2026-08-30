# L0-003 — Gold ETF Holdings

Phase 3 uses the live World Gold Council ETF workbook and the approved Phase 2
parser. The canonical value is global physical ETF holdings in metric tonnes,
with one row per observation date.

## Validation and flags

The parser rejects malformed, non-numeric, negative, or otherwise unusable
holdings records. It marks a usable record as `FLAG` when the change from the
previous observation exceeds the configured 5% review threshold. Large changes
can occur legitimately through ETF inflows, redemptions, gold-price movements,
fund activity, market stress, or source revisions; therefore `FLAG` is a review
warning, not a rejection or a claim that the value is incorrect.

`FLAG` observations retain their source-backed numeric value and remain
`AVAILABLE`. Phase 3 passes the warning through as `quality_flag` so downstream
logic can review, use, down-weight, or otherwise handle the observation. A flag
does not halt the variable or the overall pipeline. Only an unavailable or
`BLOCKED` input prevents a usable handoff; no substitute value is fabricated.
