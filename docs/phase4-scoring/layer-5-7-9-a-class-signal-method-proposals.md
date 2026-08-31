# Phase 4 Layers 5, 7 and 9 A-class signal method proposals

**Status:** Approved; implementation evidence is complete and closed.  
**Scope:** L5-001, L5-003, L7-001, L7-003, L7-004, L7-005 and L9-001  
**Implementation:** See `layer-5-7-9-a-class-implementation-evidence.md`. This document remains the approved method record; it does not define weights or aggregation.

This proposal uses the frozen canonical records, the Phase 1 registry, the approved Phase 4 input/status contract and each variable's own preserved handoff. A signed change is `delta = current_value - prior_value`; `delta > 0`, `delta < 0` and `delta == 0` map to the stated `+1`, `-1` and `0`. The signal is direction-only, not a normalized magnitude. A value that is already a change measure is not re-derived; its own series is compared at the approved cadence.

Approved position offsets are daily `5/63/252/756`, monthly `1/12`, quarterly `12/40`, and annual `3/10`. A horizon excluded by the registry is `NOT_APPLICABLE`. A required prior that is missing or ineligible is `INCOMPLETE`; there is no shorter fallback, interpolation, pooling or synthetic history.

## Preserved inputs and cadence

| Variable | Canonical current | Preserved rows / observed cadence | Preserved status finding |
|---|---|---|---|
| L5-001 | `51.14172951414363 metric_tonnes`, 2026-06-01, `AVAILABLE/OK` | 294, monthly month-start | All 294 rows are `AVAILABLE`. |
| L5-003 | `0.7135162353516051 percentage_points_qoq`, 2026-03-31, `AVAILABLE/OK` | 109, quarterly quarter-end | 108 rows are `STALE`; the first value is `null`/`STALE`. |
| L7-001 | `6730912 millions_usd`, 2026-08-26, `AVAILABLE/OK` | 1,237, weekly Wednesdays | 1,236 rows are `STALE`; only the latest row is `AVAILABLE`. |
| L7-003 | `9.819296231854157 percent_yoy`, 2025-12-31, `AVAILABLE/OK` | 108, quarterly quarter-end | 107 rows are `STALE`; four early values are `null`/`STALE`. |
| L7-004 | `2.63 percentage_points`, 2026-08-27, `AVAILABLE/OK` | 787, daily business dates | 783 rows are `STALE`; four latest rows are `AVAILABLE`. |
| L7-005 | `1.000000000000023 basis_points`, 2026-08-27, `AVAILABLE/OK` | 2,099, daily business dates | 2,096 rows are `STALE`; three latest rows are `AVAILABLE`. |
| L9-001 | `-2.003030999999828 usd_per_troy_ounce`, 2026-08-21, `AVAILABLE/OK` | 6,088, daily market dates | 6,086 rows are `STALE`; two latest rows are `AVAILABLE`. |

The register and handoffs agree on the listed frequencies except that L5-001's preserved sample is monthly within its registry's monthly/quarterly allowance. L7-001 is weekly, for which the current approved offset table has no weekly position rule. L9-001 is identified below as a registry/handoff premium series, not a spot-price series.

## Variable proposals

### L5-001 — Monthly Official-Sector Gold Purchase Volume

- **Meaning and registry direction:** Monthly official-sector net gold purchase volume measures realized official reserve demand. Positive values are purchases and negative values are net reductions/sales. The registry direction is `Positive`.
- **MVP transformation:** Compare the monthly flow observations at the approved position offsets. A rise in the flow (greater purchasing or less selling) → `+1`; a fall → `-1`; unchanged → `0`. This is a change in purchase-flow intensity, not a level threshold.
- **Horizon and offsets:** `1–5 days: NOT_APPLICABLE`; `1–3 months: monthly offset 1`; `1–3 years: monthly offset 12`; `3–10 years: NOT_APPLICABLE` because the registry does not provide a monthly 3–10-year position rule and no quarterly series is preserved.
- **History:** Use only the 294 allowlisted L5-001 monthly rows and their WGC provenance. Do not substitute L0-002 holdings or pool another official-sector series.
- **Status implication:** The preserved current and selected monthly priors are `AVAILABLE`, so the listed offsets are count-sufficient in this snapshot. Any future `STALE`, `BLOCKED`, missing, malformed, non-finite, wrong-unit or duplicate input makes the affected horizon `INCOMPLETE` under the common contract.

### L5-003 — Reserve Composition Change / USD Share Change

- **Meaning and registry direction:** The value is the already calculated quarter-over-quarter change in the reported USD share of reserves, in percentage points. The registry direction is `Conditional`; a falling USD share alone does not prove gold allocation, because non-gold diversification and other reserve-security motives are possible.
- **MVP transformation:** Do not recompute the composition change. Compare the `percentage_points_qoq` observations across quarters. Proposed conditional diversification baseline: a fall in the QoQ USD-share-change value → `+1`; a rise → `-1`; unchanged → `0`. This is a proxy for a more gold-compatible reserve-composition direction and must retain the registry caveat.
- **Horizon and offsets:** `1–5 days: NOT_APPLICABLE`; `1–3 months: NOT_APPLICABLE`; `1–3 years: quarterly offset 12`; `3–10 years: quarterly offset 40`.
- **History:** Use only the 109 allowlisted quarterly L5-003 rows. The first null is not a usable observation and is never coerced to zero. No gold-share or purchase series may be substituted.
- **Current feasibility:** Position counts are sufficient, but the exact selected priors are `STALE` in the preserved handoff. Both applicable horizons therefore produce `INCOMPLETE` under the approved status contract until eligible priors exist; no stale value is used.

### L7-001 — Major Central-Bank Balance-Sheet Liquidity

- **Meaning and registry direction:** This is the realized balance-sheet/liquidity capacity represented by the preserved series. Expansion is registry-positive, while acute crisis liquidation remains conditional.
- **MVP transformation proposal:** If an approved weekly position rule is added, compare the weekly balance-sheet values: rising liquidity → `+1`; falling → `-1`; unchanged → `0`. Do not score the raw level as expected future easing.
- **Horizon and offsets:** The registry lists `1–3 months`, `1–3 years` and `3–10 years`, but the observed handoff is weekly and the approved frequency table defines no weekly offsets. Under the current contract, all four horizons are `NOT_APPLICABLE` pending an explicit weekly-to-horizon offset decision. Do not apply daily `5/63/252/756` positions to weekly observations or invent `13/52/156` offsets.
- **History:** Use only the 1,237 allowlisted weekly rows if and when a weekly rule is approved. No multi-country aggregation, currency conversion or other central-bank series is introduced here.
- **Current feasibility:** The latest row is available but every possible selected prior in the preserved series is `STALE`; even after a weekly offset decision, the affected horizons would be `INCOMPLETE` with this snapshot.

### L7-003 — Global Private Non-Financial Credit Growth

- **Meaning and registry direction:** The value is already matching-quarter year-over-year growth in private non-financial credit. Expanding credit can increase financial capacity, while contraction can indicate deleveraging and stress; the registry direction is `Conditional` because precautionary demand and forced liquidation can point in opposite directions.
- **MVP transformation:** Do not recompute the YoY rate. Compare the quarterly `percent_yoy` observations at the approved offsets. Proposed stress/precautionary-demand baseline: falling YoY credit growth → `+1`; rising growth → `-1`; unchanged → `0`. This conditional baseline does not claim a universal sign during acute liquidation.
- **Horizon and offsets:** `1–5 days: NOT_APPLICABLE`; `1–3 months: NOT_APPLICABLE`; `1–3 years: quarterly offset 12`; `3–10 years: quarterly offset 40`.
- **History:** Use only the 108 allowlisted quarterly rows. Null early YoY values remain missing and are not filled or converted to zero.
- **Current feasibility:** Both required priors are `STALE` in the preserved handoff, so both applicable horizons are `INCOMPLETE` for the current snapshot despite sufficient row counts.

### L7-004 — Credit-Spread Financial Stress

- **Meaning and registry direction:** This percentage-point series measures compensation for credit risk. Widening spreads indicate tighter financing and stress, but can coincide with acute cash liquidation; the registry direction is `Conditional`.
- **MVP transformation:** Proposed stress baseline: spread widening (`delta > 0`) → `+1`; narrowing (`delta < 0`) → `-1`; unchanged → `0`. The same direction is proposed for all applicable horizons, with the acute 1–5-day liquidation caveat retained. No threshold, percentile or regime switch is introduced.
- **Horizon and offsets:** `1–5 days: daily offset 5`; `1–3 months: daily offset 63`; `1–3 years: daily offset 252`; `3–10 years: NOT_APPLICABLE`.
- **History:** Use only the 787 allowlisted daily rows. No L1 yield, credit index or global spread substitute is allowed.
- **Current feasibility:** All three selected priors (at offsets 5, 63 and 252) are `STALE`; the current handoff therefore yields `INCOMPLETE` for each applicable horizon rather than using stale comparisons.

### L7-005 — Treasury Repo Funding Stress

- **Meaning and registry direction:** The value is the SOFR-minus-EFFR secured-funding spread in basis points. A wider spread is a direct stress change in the already defined spread, while the registry remains `Conditional` because funding stress can produce both forced liquidation and later liquidity support.
- **MVP transformation:** Compare the spread itself, not its absolute level: widening (`delta > 0`) → `+1`; narrowing (`delta < 0`) → `-1`; unchanged → `0`. No percentile, abnormality threshold or volatility estimate is proposed.
- **Horizon and offsets:** `1–5 days: daily offset 5`; `1–3 months: daily offset 63`; `1–3 years: daily offset 252`; `3–10 years: NOT_APPLICABLE`.
- **History:** Use only the 2,099 allowlisted daily SOFR/EFFR spread rows. Do not substitute a raw SOFR level or another funding series.
- **Current feasibility:** The selected priors at all three offsets are `STALE`; each applicable horizon is therefore `INCOMPLETE` for the preserved current snapshot.

### L9-001 — Shanghai Gold Exchange Premium/Discount

- **Registry/handoff conflict:** The prompt calls L9-001 “spot gold price,” but the frozen Phase 1 registry, canonical unit (`usd_per_troy_ounce`) and preserved WGC handoff identify it as the Shanghai Gold Exchange premium/discount. This proposal follows the frozen registry/handoff. A spot-price method would require a separate owner-approved registry and source correction.
- **Meaning and registry direction:** The series measures Chinese deliverable-gold pricing relative to an international reference after the preserved conversion. The registry direction is `Conditional`; a rising premium generally indicates local physical tightness/demand but can also reflect VAT, controls, currency conversion or timing.
- **MVP transformation:** Proposed conditional physical-tightness baseline: premium rising (`delta > 0`) → `+1`; premium falling (`delta < 0`) → `-1`; unchanged → `0`. No spot-price interpretation or threshold is added.
- **Horizon and offsets:** `1–5 days: daily offset 5`; `1–3 months: daily offset 63`; `1–3 years: daily offset 252`; `3–10 years: NOT_APPLICABLE`.
- **History:** Use only the 6,088 allowlisted L9-001 daily premium/discount rows. Do not derive a spot price, pool USD/CNY, or substitute another gold benchmark.
- **Current feasibility:** The selected priors at all three offsets are `STALE`; each applicable horizon is `INCOMPLETE` for the preserved current snapshot under the approved contract.

## Common status treatment

| Input condition | Proposed result |
|---|---|
| Current and exact prior are finite, contract-valid `AVAILABLE` records | Compute the variable's signed-change mapping. |
| Finite current `FLAG` with a visible quality reason | Compute and retain `FLAGGED`; no haircut. |
| Current or selected prior `STALE` | `INCOMPLETE`; never use the stale comparison point. |
| Current or selected prior `BLOCKED` | `INCOMPLETE`; no replacement value. |
| Missing, malformed, non-finite, wrong-unit or missing source reference | Reject or return `INCOMPLETE` with a specific reason; never coerce. |
| Duplicate variable/timestamp or ambiguous prior | Reject or return `INCOMPLETE`; never select silently. |
| Required offset absent | `INCOMPLETE` for that horizon. |
| Registry-excluded or currently unsupported cadence/horizon | Explicit `NOT_APPLICABLE`, not numeric zero. |

Every result should trace variable ID, horizon, observed cadence, offset, current/prior timestamps and values, delta, unit, direction mapping, source references, statuses/quality flags and any conditional or cadence caveat. No status is silently converted to a neutral observation.

## Later reader and signal test plan

1. Validate the seven canonical fields, exact variable ID, unit, finite numeric value, ISO timestamp, source reference, allowed status and duplicate timestamps for each preserved handoff.
2. Assert preserved counts and cadence: L5-001 294 monthly, L5-003 109 quarterly, L7-001 1,237 weekly, L7-003 108 quarterly, L7-004 787 daily, L7-005 2,099 daily and L9-001 6,088 daily.
3. Test sorting and exact offsets for monthly, quarterly and daily methods. For L7-001, assert that unsupported weekly horizons return `NOT_APPLICABLE` until a weekly offset rule is approved.
4. Test rising, falling and unchanged mappings, including L5-003/L7-003 pre-derived change measures and the inverted conditional stress mappings for L7-004/L7-005.
5. Test current `FLAG`, current/prior `STALE`, current/prior `BLOCKED`, missing, malformed, non-finite, wrong-unit, duplicate and insufficient-history inputs. Include the preserved null rows in L5-003 and L7-003 and assert no zero coercion.
6. Assert the current preserved priors described above return `INCOMPLETE` when `STALE`; assert all excluded horizons return explicit `NOT_APPLICABLE`.
7. Verify trace completeness and retain the L9-001 registry/handoff premium-versus-prompt conflict in the method record. No test should invoke weights, layers, interactions, Net Index, probabilities, hashing or replay.

## Decision record

- The owner approved all seven proposed methods and their conditional caveats on 2026-08-31.
- L5-003 and L7-003 compare their already derived QoQ/YoY series; no recomputation is used.
- L7-001 remains status-only with `NOT_APPLICABLE` for all horizons because no weekly offset rule is approved.
- L9-001 follows the frozen registry/handoff SGE premium/discount definition, not the conflicting “spot gold price” wording.
- Stale selected priors remain explicitly `INCOMPLETE` under the approved contract.

No weight, layer score, interaction, Net Index or probability implementation is included in this method record.
