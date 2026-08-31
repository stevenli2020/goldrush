# Phase 4 Layer 0 A-class and corrected L8-001 signal method proposals

**Status:** Method approved; implementation and correction evidence approved and closed.  
**Scope:** L0-001, L0-003, L0-005, L0-006 and corrected L8-001  
**Implementation:** See `layer-0-l8-001-implementation-evidence.md` and `layer-0-l8-001-correction-evidence.md`. The proposal remains the method record; no weights or aggregation are defined here.

This proposal uses the frozen Phase 1 registry, the approved Phase 4 input/status contract, the canonical dataset, and the preserved transformation outputs. It keeps source units and meanings intact and does not introduce z-scores, percentiles, arbitrary thresholds, invented neutral levels or cross-variable history.

## Shared MVP rule

For an applicable horizon, select the current observation and the exact earlier position from the same variable and the same cadence/period type. Define `delta = current_value - prior_value`. The direction mapping is explicit per variable: positive delta, negative delta and zero delta map to the proposed gold-direction `+1`, `-1` and `0`. Zero delta is the only neutral result; a missing or unusable record is not neutralized.

The cadence offsets are:

- daily: `5`, `63`, `252`, `756` for 1–5 days, 1–3 months, 1–3 years and 3–10 years;
- monthly: `1`, `12` for 1–3 months and 1–3 years;
- quarterly: `12`, `40` for 1–3 years and 3–10 years;
- annual: `3`, `10` for 1–3 years and 3–10 years.

Where a registry horizon cannot be resolved by the preserved cadence, it is `NOT_APPLICABLE`. Where the cadence and registry disagree, the conflict is reported below and no daily offset is applied to monthly data. A required but absent prior is `INCOMPLETE`; there is no shorter fallback or interpolation.

## Frozen-input and history checks

| Variable | Canonical current record | Preserved history and observed cadence | Check affecting this proposal |
|---|---|---|---|
| L0-001 | `220700 metric_tonnes`, 2025-12-31, `AVAILABLE`, `OK` | 16 annual rows | Count permits annual offsets 3 and 10. |
| L0-003 | `4067.97 metric_tonnes`, 2026-07-31, `AVAILABLE`, `OK` | 281 month-end rows in the preserved handoff | Registry says daily, but the handoff is monthly; this cadence conflict must remain visible. |
| L0-005 | `307.08301057 metric_tonnes`, 2026-06-30, `AVAILABLE`, `OK` | 82 rows: 16 annual and 66 quarterly | The approved correction changed the 16 invalid Q3 timestamps to valid September quarter ends; superseded evidence is retained. |
| L0-006 | `326.09358209 metric_tonnes`, 2026-06-30, `AVAILABLE`, `OK` | 66 quarterly rows in `docs/phase2-ingestion/L0/006/processed/l0_006_gold_recycling_flow.json` | The approved path correction now aligns the register and canonical reference with the existing source. |
| L8-001 | `23.46395211 metric_tonnes`, 2026-07-31, `AVAILABLE`, `OK` | 281 month-end rows in the corrected handoff | Confirmed corrected per-fund `Demand (tonnes)` sum from `Demand by month`; the superseded 4,068.01245306 aggregate is excluded. |

## Variable proposals

### L0-001 — Above-Ground Gold Stock

- **Economic meaning and direction:** This is the accumulated above-ground gold stock. A larger stock can increase the amount potentially available to marginal holders, while a falling stock can indicate greater scarcity. The registry direction is `Conditional`; the proposed MVP baseline is the available-stock channel: rising stock (`delta > 0`) → `-1`, falling stock (`delta < 0`) → `+1`, unchanged → `0`. This does not claim that stock growth mechanically lowers gold prices, and no regime gate is proposed.
- **Transformation and horizons:** Signed metric-tonne change on the annual series. `1–5 days: NOT_APPLICABLE`; `1–3 months: NOT_APPLICABLE`; `1–3 years: offset 3`; `3–10 years: offset 10`. Sixteen rows are count-sufficient for both offsets. No annual value is converted to a higher-frequency observation.
- **History use:** Only the 16 allowlisted L0-001 annual rows and their WGC provenance. No mine-supply, recycling, holdings or other stock series is pooled into this variable.

### L0-003 — Gold ETF Holdings

- **Economic meaning and direction:** This is the stock of gold held through ETFs, distinct from L8-001's monthly flow. A rising ETF-held stock is the proposed baseline sign of increasing investment allocation and gold absorption: `+1`; falling stock → `-1`; unchanged → `0`. The registry direction remains `Conditional` because price movements, creations/redemptions and overlap with flow measures affect interpretation.
- **Transformation and horizons:** The registry records daily frequency, but the preserved 281-row handoff is month-end. Until that conflict is resolved, use the observed monthly cadence rather than applying daily position counts: `1–5 days: NOT_APPLICABLE`; `1–3 months: offset 1`; `1–3 years: offset 12`; `3–10 years: NOT_APPLICABLE` because the registry does not list it. If the owner confirms daily cadence, a separate approved handoff would be required before offsets 5/63/252 could be used; no daily interpolation is proposed.
- **History use:** Only the 281 allowlisted L0-003 rows. Do not substitute L8-001 flows, reconstruct holdings from price, or pool another ETF series.

### L0-005 — Bar-and-Coin Investment Holdings / Demand

- **Economic meaning and direction:** The preserved value is total bar-and-coin physical investment demand in metric tonnes. Rising demand is proposed as gold-supportive (`+1`), falling demand as `-1`, unchanged as `0`; the registry marks the broader ownership mechanism `Positive`.
- **Transformation and horizons:** The handoff mixes annual and quarterly observations, so the prior must have the same `observation_period_type` as the current record. For a quarterly current record, use `1–3 months: NOT_APPLICABLE`, `1–3 years: offset 12`, `3–10 years: offset 40`. For an annual current record, use `1–3 months: NOT_APPLICABLE`, `1–3 years: offset 3`, `3–10 years: offset 10`. `1–5 days: NOT_APPLICABLE` for both. No annual/quarterly cross-frequency comparison is permitted.
- **Correction state:** The approved upstream amendment changed only the 16 invalid Q3 timestamps to valid September quarter ends. The malformed handoff remains retained as superseded evidence; the corrected 82-row handoff is eligible for the approved reader.
- **History use:** Only the 82 allowlisted L0-005 rows, partitioned by their preserved annual or quarterly period type. No country, regional-demand, L0-006 or L8-002 history is pooled or substituted.

### L0-006 — Gold Recycling Flow

- **Economic meaning and direction:** This is active liquidation of existing gold into market supply. A rising recycling flow increases supply pressure and is proposed as `-1`; a falling flow reduces that pressure and is `+1`; unchanged is `0`. The registry direction is `Negative`.
- **Transformation and horizons:** Use the quarterly series only. `1–5 days: NOT_APPLICABLE`; `1–3 months: NOT_APPLICABLE` because the preserved cadence cannot resolve a shorter monthly horizon; `1–3 years: offset 12`; `3–10 years: NOT_APPLICABLE` because the registry does not list it. Sixty-six rows are count-sufficient for offset 12.
- **History and path state:** The 66 rows and quarterly cadence are confirmed in `l0_006_gold_recycling_flow.json`. The approved register and canonical reference now point to this existing source, which remains unchanged.
- **History use:** Only the 66 own-variable quarterly recycling rows. Do not substitute L0-005 physical demand, mine supply or another recycling estimate.

### L8-001 — Corrected Gold ETF Net Flows

- **Correction confirmation:** The corrected handoff contains 281 monthly rows from the WGC workbook's `Demand by month` sheet, summing each fund's `Demand (tonnes)` change. The latest row is `23.46395211 metric_tonnes` for 2026-07-31. Negative values are valid net outflows. The superseded `4,068.01245306` holdings-like aggregate is not used.
- **Economic meaning and direction:** This is a monthly ETF investment flow, distinct from L0-003's ETF-held stock. An increase in net flow means stronger inflow or less outflow and is proposed as gold-supportive (`+1`); a decrease means weaker demand or greater outflow and is `-1`; unchanged is `0`. The registry direction is positive for net inflows.
- **Transformation and horizons:** Use the corrected monthly series. `1–5 days: NOT_APPLICABLE` because the corrected handoff is monthly; `1–3 months: offset 1`; `1–3 years: offset 12`; `3–10 years: NOT_APPLICABLE` because the registry does not list it. These are changes in the flow observations, not a raw-level threshold or a reconstructed daily flow.
- **Contract classification state:** The approved correction resolves the stock/flow disposition and L8-001 is treated as `A` (own-variable time series) under the ordinary status rules. The current contract records 281 corrected rows and excludes the superseded aggregate.
- **History use:** Only the 281 corrected L8-001 rows. Do not use L0-003 holdings, issuer proxies, a synthetic daily series or the superseded aggregate.

## Common status treatment

For every proposed variable and horizon, apply the approved contract directly:

| Input condition | Proposed result |
|---|---|
| Current and exact prior are `AVAILABLE`, contract-valid and finite | Compute `delta` and the variable's approved direction mapping. |
| Current is finite `FLAG` | Compute and retain a visible `FLAGGED` result; no automatic haircut. |
| Current or selected prior is `STALE` | `INCOMPLETE`; never use the stale prior as a comparison point. |
| Current or selected prior is `BLOCKED` | `INCOMPLETE`; no replacement value. |
| Missing, malformed, non-finite, wrong-unit, missing source or invalid timestamp | Reject or return `INCOMPLETE` with a specific reason; never coerce or repair. |
| Duplicate variable/timestamp or ambiguous same-cadence prior | Reject or return `INCOMPLETE`; never select silently. |
| Required own-series offset is unavailable | `INCOMPLETE` for that horizon. |
| Cadence or registry excludes the horizon | Explicit `NOT_APPLICABLE`, not numeric zero or neutral. |

Each result should trace variable ID, horizon, period type where relevant, current/prior timestamps and values, offset, delta, unit, direction mapping, source references, quality/status flags and any cadence or conditional caveat.

## Later reader and signal test plan

1. Validate the seven canonical fields, exact variable ID and unit, finite value, ISO timestamp, source reference, allowed status and duplicate timestamp. Test each of the five readers against its preserved source shape.
2. Sort each own-variable history by timestamp and verify exact position selection. For L0-005, require matching annual/quarterly period type; never compare across types.
3. Test rising, falling and unchanged values for each direction, including L0-001's available-stock baseline and L0-006's recycling-supply inversion.
4. Assert all listed `NOT_APPLICABLE` horizons return that state without a lookup. Test monthly L0-003/L8-001 daily-horizon handling and the registry applicability conflict trace.
5. Test current `FLAG`, current/prior `STALE`, current/prior `BLOCKED`, missing, malformed, non-finite, wrong-unit, duplicate and insufficient-history inputs. Include L0-005 corrected timestamp validation and L0-006 corrected contract-path resolution.
6. Load the real preserved histories and assert counts: L0-001 16, L0-003 281, L0-005 82, L0-006 66, L8-001 281; assert L8-001 latest value `23.46395211` and corrected source markers.
7. Verify trace completeness for variable, horizon, current/prior, offset, delta, mapping, source references, flags and conditional/cadence notes. No test should invoke weights, layers, interactions, Net Index, probabilities, hashing or replay.

## Decision record

- The baseline signs, horizon offsets and conditional caveats for all five variables were approved for implementation on 2026-08-31.
- The L0-005 timestamp and L0-006 path corrections were approved and are documented separately in `layer-0-l8-001-correction-evidence.md`.
- The L0-003 registry-daily versus preserved-monthly conflict remains visible in trace context; no daily interpolation is used.
- L8-001 remains classified as `A` with corrected per-fund flow provenance.

Owner approval/closure is recorded in `layer-0-l8-001-implementation-evidence.md` and `layer-0-l8-001-correction-evidence.md`.
