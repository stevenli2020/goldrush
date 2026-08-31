# Phase 4 input and status contract — approved MVP

**Status:** Approved (amended)  
**Scope:** Approved input/status contract for Phase 4. This remains a contract, not scoring-engine code.

## Common input

The input is one record per admitted variable from `closure/canonical_dataset.jsonl`, joined to the matching row in `closure/variable_register.json`. The seven canonical fields are:

`variable_id`, `observation_timestamp`, `value`, `unit_or_scale`, `availability_status`, `source_reference`, and `quality_flag`.

The register is authoritative for the approved source, transformation output, cadence and unit. A caller must reject an unknown ID, duplicate ID, missing field, non-finite non-blocked value, unit mismatch, malformed timestamp or missing source reference. The caller must not rewrite the frozen records.

## Historical-input allowlist

The count below is the number of source-backed rows found in the preserved transformation output during preparation. It describes what exists; it does not approve a normalization window or a new calculation.

| ID | Canonical unit or scale | History class | Preserved source-backed availability |
|---|---|---|---:|
| L0-001 | metric_tonnes | A: time series | 16 rows |
| L0-002 | metric_tonnes | P: country panel; context only | 52 rows, one publication date |
| L0-003 | metric_tonnes | A: time series | 281 rows |
| L0-005 | metric_tonnes | A: time series | 82 rows |
| L0-006 | metric_tonnes | A: time series | 66 rows |
| L0-009 | percent_per_annum | N: current scalar | 1 row |
| L1-001 | percent | A: time series | 5,918 rows |
| L1-002 | percent | A: time series | 5,918 rows |
| L1-003 | percent | A: time series | 6,904 rows |
| L1-005 | percent | A: time series | 9,146 rows |
| L1-006 | percent_per_annum | N: current scalar | 1 row |
| L1-007 | percent | A: time series | 5,918 rows |
| L2-001 | index | A: short preserved series | 19 rows |
| L2-002 | index_jan_2006_100_not_seasonally_adjusted | A: time series | 5,174 rows |
| L2-003 | cny_per_usd | A: time series | 11,392 rows |
| L3-001 | percent_per_annum | N: current scalar | 1 row |
| L3-002 | percent_per_annum | E: current curve components | 19 contracts, one date |
| L3-003 | percent_per_annum | N: current scalar | 1 row |
| L3-004 | expected_target_change_bps | E: current event distribution | 8 buckets, one date |
| L3-005 | percent | E: current event panel | 26 bins, one date |
| L3-006 | hawkishness_score_0_to_100 | Q: current encoded result; text context only | No numeric history |
| L4-001 | index | A: time series | 954 rows |
| L4-002 | index | A: time series | 811 rows |
| L4-003 | percent | A: time series | 5,919 rows |
| L4-004 | percent | A: time series | 5,919 rows |
| L4-006 | percent_of_gdp | A: time series | 97 rows |
| L4-007 | percent_of_gdp | A: time series | 241 rows |
| L4-008 | percent_of_federal_receipts | A: time series | 11 rows |
| L4-009 | percent_of_marketable_treasury_debt | A: time series | 24 rows |
| L5-001 | metric_tonnes | A: time series | 294 rows |
| L5-002 | fraction | P: country panel; context only | 97 rows, 18 dates |
| L5-003 | percentage_points_qoq | A: time series | 109 rows |
| L5-006 | metric_tonnes | P: country panel; context only | 2,724 rows, 294 dates |
| L6-001 | standard_deviation_units_clamped_-1_to_1 | H: approved 60-value GPRD source window | 60 source values |
| L6-002 | sovereign_asset_freeze_score_0_to_100 | Q: event evidence only | No numeric history |
| L7-001 | millions_usd | A: time series | 1,237 rows |
| L7-003 | percent_yoy | A: time series | 108 rows |
| L7-004 | percentage_points | A: time series | 787 rows |
| L7-005 | basis_points | A: time series | 2,099 rows |
| L8-001 | metric_tonnes | A: time series | 281 rows |
| L9-001 | usd_per_troy_ounce | A: time series | 6,088 rows |
| L9-004 | metric_tonnes | P: component panel; context only | 308 rows, 66 dates |
| L10-001 | contracts | N: current scalar | 1 row |
| L10-002 | contracts | N: current scalar | 1 row |

History classes are deliberately narrow:

- `A` permits source-backed historical rows for a future, variable-specific rule. It does not grant a z-score, percentile, change window or confidence value.
- `H` is permitted only for the already approved L6-001 60-value source window and its existing variable-local scorer. It must not be generalized to other variables.
- `P` permits panel context and component selection only. Do not pool countries, components or dates into a new aggregate without a separate rule.
- `E` permits the current curve/event components to be labelled and scored as components. It is not a historical series.
- `N` is current-scalar only in the MVP.
- `Q` is evidence context for the existing encoded result; it is not a numerical history.
- `X` is reserved for a variable explicitly held pending source disposition; no current approved scoring variable uses this class.

## Status propagation

These are the approved MVP rules. They preserve the Phase 3 availability state while making downstream eligibility explicit.

**L8-001 resolution:** The owner-approved 2026-08-31 correction uses the per-fund `Demand (tonnes)` sum from `Demand by month`. The corrected July 2026 value is `23.46395211` metric tonnes; the superseded `4,068.01245306` aggregate is not used. L8-001 now follows the ordinary status rules below.

| Input state | Variable result | Layer result | Net Index result |
|---|---|---|---|
| `AVAILABLE` and contract-valid | Eligible numeric input | Contributes if its approved horizon rule exists | Eligible if every required layer is numeric |
| `FLAG` with a finite value and visible reason | Eligible but flagged; no automatic haircut | Contributes and retains the flag | Numeric only when otherwise complete; result is visibly `FLAGGED` |
| `STALE` | Retained but ineligible by default | `INCOMPLETE` unless that variable has an explicitly approved carry-forward rule | No numeric result for affected horizons |
| `BLOCKED` | Ineligible; value remains absent | `INCOMPLETE` | No numeric result for affected horizons |
| Missing, malformed or insufficient permitted history | Ineligible; record the reason | `INCOMPLETE` | No numeric result for affected horizons |

No state is silently converted to zero, neutral, synthetic history or a replacement source. No layer or Net Index denominator is automatically renormalized after an input is excluded. A flagged value is not treated as a pass, and the L3-006 `LOW_COVERAGE` flag remains attached to every downstream result that uses it.

For Layer 11, the contract state is `NOT_ADMITTED`, not `ZERO` or `NEUTRAL`. It may be omitted from an approved active-layer set only when the layer-weight specification explicitly omits it and the remaining weights are explicitly supplied to sum to one. No automatic redistribution is permitted.

## Scalar and component labels

Every selected scalar must carry a declared `selection_label` outside the frozen record, such as `L3-005:selected_dot_plot_rate_bin`, together with its component key, event date and any published aggregate context. The scalar is never described as the full curve, distribution or panel. The canonical seven-field record remains unchanged.

## Contract completion criteria

The input/status boundary in this contract is approved. Signal meaning, direction and horizon applicability are recorded in separate per-variable approval records. All 44 admitted variables now have an explicit approved Phase 4 variable-level treatment. L0-002 and L9-004 are P-class status-only `NOT_APPLICABLE` methods with context retained but no selection, pooling or aggregation; L3-006 maps its approved 0/50/100 dovish-neutral-hawkish scale to the approved short-horizon gold signal while retaining `LOW_COVERAGE`; L6-001 maps the approved existing scorer sign for its two short horizons without rerunning the scorer; and L6-002 is Q-class status-only `NOT_APPLICABLE`. L1-005 remains limited to its provisional conditional opportunity-cost proxy, while L1-006, L7-001 and the approved N-class variables are status-only with `NOT_APPLICABLE` for all horizons. L2-001 retains its explicit short-history behavior, L2-002 retains its broad-dollar index base, and L2-003 retains the registry-defined rising-USD/CNY direction. L4-009 retains explicit `INCOMPLETE` behavior for its 3–10-year horizon when the 120-position monthly prior is unavailable. L5-003 and L7-003 compare their pre-derived QoQ/YoY series; L9-001 follows the registry/handoff premium definition. Regime-gating/context logic, numerical variable weights, layer weights, dependency factors, interaction coefficients and Net Index formulas remain separate decisions for the scoring-engine phase.

## Approval record

**2026-08-31:** The amended contract was approved. The L8-001 source correction was separately approved the same day; the superseded handoff remains retained for audit and the corrected handoff is the current input.

**2026-08-31:** L1-005's provisional signed-change implementation was accepted as complete and correct. Its conditional status and the hold on regime-gating/context logic remain in force.

**2026-08-31:** L2-001, L2-002 and L2-003 signed-change implementations were accepted as complete and correct. The `_l1_signal_common.py` helper name was accepted as a non-blocking MVP note; any rename is optional and deferred.

**2026-08-31:** L1-006's status-only implementation was accepted as complete and correct. All four horizons remain explicitly `NOT_APPLICABLE`.

**2026-08-31:** L4-001, L4-002, L4-003, L4-004, L4-006, L4-007, L4-008 and L4-009 implementations were accepted as complete and correct. L4-003 and L4-004 use the Phase 1 registry's applicable-horizon lists; L4-009's 3–10-year horizon remains `INCOMPLETE` with only 24 preserved monthly rows.

**2026-08-31:** The approved post-freeze L0-005 timestamp correction and L0-006 transformation-output path correction were applied with superseded evidence retained. The corrected L0-005 handoff remains 82 rows; L0-006 uses the unchanged 66-row processed source named by the corrected register and canonical reference. The five Layer 0/L8-001 method implementations are documented separately; no status is silently converted to a numeric neutral result.

**2026-08-31:** The owner approved L0-001, L0-003, L0-005, L0-006 and corrected L8-001 readers/signals as complete and correct. Their correction and implementation evidence are closed; all status propagation and explicit `NOT_APPLICABLE`/`INCOMPLETE` behavior remains in force.

**2026-08-31:** The owner approved all implementable A-class time-series signals as complete and correct. L5-001, L5-003, status-only L7-001, L7-003, L7-004, L7-005 and L9-001 are closed with their implementation evidence. Non-A-class groups and scoring aggregation remain outside this approval.

**2026-08-31:** The owner approved the L0-009, L3-001, L3-003, L10-001 and L10-002 N-class status-only implementations as complete and correct. Their four-horizon `NOT_APPLICABLE` behavior and explicit invalid-input `INCOMPLETE` handling are closed; E, P and Q groups and scoring aggregation remain outside this approval.

**2026-08-31:** The owner approved the final five variable methods as complete and correct. L0-002 and L9-004 are status-only P-class methods; L3-006 is a flagged-aware short-horizon scorer adapter; L6-001 is a short-horizon existing-scorer adapter; and L6-002 is status-only Q-class treatment. All 44 admitted variables now have an explicit closed Phase 4 variable-level method. Scoring aggregation remains separate.
