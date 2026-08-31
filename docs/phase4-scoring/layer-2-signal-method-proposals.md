# Layer 2 signal method proposals

**Status:** Approved and closed  
**Scope:** Proposal only for L2-001, L2-002 and L2-003. No reader, signal, scoring-engine or pilot code is authorized.

## Shared MVP rule

For each variable and applicable horizon, sort that variable's own allowlisted series ascending by observation timestamp and calculate:

```text
delta_h = latest_value - value_N_positions_before_latest
```

The four observation-count conventions are 5, 63, 252 and 756 for 1–5 days, 1–3 months, 1–3 years and 3–10 years. They are explicit MVP offsets, not claims about economic completion dates. The endpoint values and percentage-point/index-point delta remain in the trace.

No z-score, percentile, fitted normalization, arbitrary level threshold, pooled series, substitution or synthetic observation is proposed. Exact zero change is neutral where a numeric method is applicable.

## L2-001 — DXY US Dollar Index

**Frozen input:** `99.16000366210938`, unit `index`, observation date `2026-08-27`, `AVAILABLE`/`OK`. The register identifies this as the ICE DXY series and classifies its preserved history as `A`, with 19 rows.

**Economic meaning and direction:** DXY measures the US dollar against a fixed basket. Under the registry's mechanical purchasing-power channel, a stronger dollar raises the USD cost of gold for non-US buyers and is generally bearish (`-1`); a weaker dollar is generally bullish (`+1`). The registry also marks the relationship conditional during acute dollar-funding stress. The proposed MVP keeps the mechanical direction and records the stress caveat as context; it does not invent a regime switch.

**Transformation and horizons:** Use signed change with offset 5 for 1–5 days. The 19-row history cannot supply offsets 63, 252 or 756, so 1–3 months and 1–3 years must return `INCOMPLETE` for insufficient permitted history. The 3–10-year relationship is conditional in the registry and has no approved MVP rule, so it is explicitly `NOT_APPLICABLE` pending a separate regime method.

**History:** Class `A`, 19 source-backed rows. Use only the same DXY series and exact position selection after sorting. Do not substitute L2-002 or a different dollar index. If the selected five-position prior is `STALE`, the status contract makes the 1–5-day result `INCOMPLETE` rather than permitting the stale value.

**Neutral/context:** None required for the signed change; exact zero is neutral. DXY basket identity and the dollar-funding-stress caveat remain trace context.

## L2-002 — Broad trade-weighted nominal US dollar index

**Frozen input:** `118.0628`, unit `index_jan_2006_100_not_seasonally_adjusted`, observation date `2026-08-21`, `AVAILABLE`/`OK`. The approved source is Federal Reserve H.10/FRED DTWEXBGS; history class `A` contains 5,174 rows.

**Economic meaning and direction:** This broader trade-weighted dollar measure captures USD appreciation across more currencies than DXY. Under the normal purchasing-power channel, a rising index is generally bearish for gold (`-1`) and a falling index is bullish (`+1`). The registry marks the relationship conditional during global dollar-liquidity stress; the MVP proposal retains the normal direction and records that caveat without an unapproved regime override.

**Transformation and horizons:** Use signed change with offset 5 for 1–5 days, 63 for 1–3 months, 252 for 1–3 years and 756 for 3–10 years. The 5,174-row series is long enough for each position offset, subject to the status and endpoint checks below.

**History:** Class `A`, 5,174 source-backed rows. Use only the same Federal Reserve broad-dollar series, sorted by timestamp. Do not pool it with DXY or derive a composite. The existing registry warning about L2-001/L2-002 overlap is a later dependency/weight decision, not a reason to alter this variable's standalone method.

**Neutral/context:** None required; exact zero change is neutral. Index base (`January 2006 = 100`) and the global-liquidity caveat remain trace context.

## L2-003 — USD/CNY

**Frozen input:** `6.721`, unit `cny_per_usd`, observation date `2026-08-21`, `AVAILABLE`/`OK`. The approved source is Federal Reserve H.10/FRED DEXCHUS; history class `A` contains 11,392 rows.

**Economic meaning and direction:** A higher CNY-per-USD value means renminbi depreciation against the dollar. The registry assigns L2-003 a **positive direction for USD/CNY** through the local-currency gold-cost channel, while noting that safe-haven and domestic-stress episodes can be conditional. Following that approved direction, a rising USD/CNY maps to bullish gold (`+1`) and a falling USD/CNY maps to bearish gold (`-1`) for the MVP signed-change proposal. This mapping must remain labelled as the registry's USD/CNY convention; it must not be silently reversed based on the separate possibility that higher local gold prices reduce physical demand.

**Transformation and horizons:** Use signed change with offset 5 for 1–5 days, 63 for 1–3 months and 252 for 1–3 years. The 3–10-year relationship is conditional in the registry and has no approved MVP rule, so it is explicitly `NOT_APPLICABLE` pending a separate long-run/regime method.

**History:** Class `A`, 11,392 source-backed rows. Use only the same CNY-per-USD series, sorted by timestamp, with no onshore/offshore substitution, country pooling or derivation from DXY/broad USD. Keep the selected rate convention and timezone in trace context.

**Neutral/context:** None required; exact zero change is neutral. The rate quotation (`cny_per_usd`), managed-rate caveat and conditional stress note remain visible context.

## Status treatment for all three variables

- A finite, contract-valid current `AVAILABLE` record and an eligible prior produce the proposed signed-change result.
- A finite current `FLAG` produces the result as visibly `FLAGGED`; no haircut or clean-pass relabelling is applied. Any prior flag remains in the trace.
- A current or selected prior `STALE` record returns `INCOMPLETE` with the reason retained and is never used as the comparison point.
- A current or selected prior `BLOCKED`, missing, malformed or non-finite record returns `INCOMPLETE`; no zero, neutral substitute, shortened offset or weight redistribution is allowed.
- Insufficient permitted history returns `INCOMPLETE`. Horizons marked `NOT_APPLICABLE` have no signal method and must not be represented as a neutral numeric score.

## Test plan outline

For each later reader and signal function, WSL tests should verify:

1. Canonical ID, unit, timestamp, finite value, source reference, allowed status and duplicate-timestamp validation.
2. Ascending sort and exact position selection for every proposed offset, including L2-001's offset-5 success path and explicit insufficient-history paths for 63/252/756.
3. Direction mapping: falling/rising DXY and broad-dollar index values map to `+1/-1`, while USD/CNY follows the registry's rising=`+1` convention; unchanged values map to `0`.
4. Current `FLAG` remains `FLAGGED`; current and prior `STALE`/`BLOCKED`, missing, malformed and insufficient inputs return `INCOMPLETE` with no signal.
5. Conditional or non-applicable horizons return explicit `NOT_APPLICABLE`, not a neutral score.
6. Trace output includes variable, horizon, current/prior timestamps and values, offset, delta, direction mapping, source references, quotation/base metadata and flags.

## Approval record

**2026-08-31:** The owner approved the L2-001, L2-002 and L2-003 methods and their implementation. The shared signed-change rule, exact offsets, L2-001 short-history behavior, mechanical negative directions for L2-001/L2-002, registry-following positive USD/CNY direction for L2-003, and `NOT_APPLICABLE` conditional 3–10-year treatment are accepted. Dollar-liquidity caveats remain context-only in this MVP.

The shared helper remains named `_l1_signal_common.py`; this is accepted for the MVP. A later rename to `_signal_common.py` is optional and is not part of this closed increment.
