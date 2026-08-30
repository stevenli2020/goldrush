# L3-006 — Consolidated Scoring Specification

Version: 0.5 | Date: 2026-08-27

Status: prototype implemented; automated checks and a four-call live smoke test
completed on 2026-08-27. Repeated stability testing and calibration remain pending.
This is the sole current scoring specification. Superseded rules and the old
combined prompt were removed; historical test results remain unchanged.

## 1. Architecture and boundaries

Pass 1 is persona-neutral AI extraction from the original current and prior FOMC
statements. It returns verbatim evidence, predefined rule IDs, and directly
extracted numeric inputs. It does not calculate scores, midpoint differences,
weighted averages, coverage, confidence, or status. TypeScript validates the
components and performs all arithmetic.

Pass 2 comprises three independent persona assessments. Each receives only its
persona instructions and the original statements, never baseline data, extracted
components, evidence, coverage, or diagnostics. It returns only `jury_score` and
`supporting_statement`. Jury scores do not modify the baseline.

Both scores run from 0 (strongly dovish), through 50 (neutral/mixed), to 100
(strongly hawkish). These are assessments, not official source classifications
or market forecasts. Calculations are deterministic given identical validated
components; AI extraction and jury assessment can vary. Temperature zero does
not guarantee repeatable extraction.

Policy guidance and voting adjustments remain. Separate inflation, labour, and
growth sentiment adjustments are removed. Guidance-diff adjustment is disabled
for the first retest. Numerical mappings, rank steps, and the 20% balance-sheet
fallback penalty remain provisional, not calibrated evidence of accuracy.

## 2. Category weights and missing data

| Category | Base weight |
|---|---:|
| Policy | 0.35 |
| Balance sheet | 0.20 |
| Inflation | 0.20 |
| Labour | 0.15 |
| Growth | 0.10 |

For scoring, exclude missing inputs and renormalize available weights. For
coverage, retain original weights and give missing inputs zero contribution.
All missing JSON inputs use `null`. Missing evidence is never neutral evidence.

Policy requires a valid rate anchor: without it, policy score is `null` and
policy completeness is zero, regardless of guidance or votes. Other categories
require at least one valid current subcomponent. If all categories are missing,
return baseline `null`, coverage `0`, status `BLOCKED`, confidence `Low`.

## 3. Extraction and validation

1. Evidence must be an exact substring of the relevant supplied current or prior
   statement. No paraphrases, word substitutions, or punctuation changes.
2. Unsupported inference is excluded, not merely lower priority. Map direct
   evidence to a defined rule or return `null`. Preserve subject, negation,
   measurement context, and time reference. Do not infer expectations from
   inflation level, liquidity from asset purchases, or current facts from prior facts.
3. Within the same subcomponent, prefer the longest applicable defined phrase
   (for example, “well above” over embedded “above”). Resolve competing explicit
   matches by type: numeric/quantitative, explicit commitment, current level/state,
   trend/direction, expectations, risks/outlook. Unresolved conflicts become
   `null` with diagnostics. No alphabetical, extremeness, or earliest-clause tiebreaker.
4. Level and direction remain independently extractable. Separate phrases in one
   sentence can support different subcomponents. Do not double-count a single
   phrase as current activity and forward risk without separate support.
5. Invalid evidence is excluded from scoring and coverage, with diagnostics
   retained. Invalid prior evidence cannot support a change calculation; valid
   current balance-sheet evidence may use the specified prior-missing fallback.

TypeScript validates JSON shape, required fields, numeric types/units, rule IDs
allowed for each component, and verbatim evidence against the correct source.
It derives availability, fallback usage, validation diagnostics, and calculations.
The AI reports unresolved extraction conflicts. Its diagnostics cannot override
validation. Verbatim validation checks quotation fidelity, not semantic correctness
or completeness of extraction; this is not a replacement language parser.

## 4. Pass 1 response contract

An ordinary component contains `evidence` and `rule_id`, each a string or `null`.
Numeric inputs add `value`; voting may add `count`. The following is a structural
example with absent evidence, not a test result:

```json
{
  "components": {
    "policy": {
      "rate_action": {
        "evidence": null, "rule_id": null, "value": null,
        "current_range": null, "prior_range": null
      },
      "forward_guidance": { "evidence": null, "rule_id": null },
      "voting": { "evidence": null, "rule_id": null, "count": null }
    },
    "balance_sheet": {
      "asset_purchases": {
        "current_evidence": null, "current_rule_id": null,
        "prior_evidence": null, "prior_rule_id": null
      },
      "liquidity_operations": {
        "current_evidence": null, "current_rule_id": null,
        "prior_evidence": null, "prior_rule_id": null
      }
    },
    "inflation": {
      "level": { "evidence": null, "rule_id": null, "value": null },
      "trend": { "evidence": null, "rule_id": null },
      "expectations": {
        "market_based": { "evidence": null, "rule_id": null },
        "survey_based": { "evidence": null, "rule_id": null }
      }
    },
    "labour": {
      "unemployment_level": { "evidence": null, "rule_id": null },
      "unemployment_direction": { "evidence": null, "rule_id": null },
      "job_gains": { "evidence": null, "rule_id": null },
      "slack_wage_pressures": { "evidence": null, "rule_id": null }
    },
    "growth": {
      "current_activity": { "evidence": null, "rule_id": null },
      "forward_risks": { "evidence": null, "rule_id": null },
      "specific_sectors": { "evidence": null, "rule_id": null }
    }
  },
  "diagnostics": { "competing_matches": [] },
  "error": null
}
```

A non-null range contains `evidence`, `lower`, and `upper`; endpoints are in
percentage points. A single target rate uses equal endpoints. Each range quote
is checked against its respective statement. TypeScript appends
`verbatim_check_failed`, `prior_statement_missing`, `balance_sheet_fallback_used`,
per-component fallback flags, and rate-fallback usage to archived diagnostics.
No AI `change_rule_id`, score, coverage, confidence, or status is accepted.

## 5. Policy

### Rate-action anchor

Use an explicit current-statement magnitude when available, even without a prior
range. `rate_change_bps` supplies signed basis points; alternatively,
`rate_change_percentage_points` supplies signed percentage points (a half-point
cut is `-0.5`). TypeScript converts units. AI does not derive changes from ranges.

Otherwise use `rate_target_ranges` with quoted current/prior endpoints:

```text
delta_bps = 100 × ((current_lower + current_upper)/2
                - (prior_lower + prior_upper)/2)
F_rate = clamp(50 + 0.5 × delta_bps, 0, 100)
```

An explicit `rate_hold` gives delta zero and anchor 50. When magnitude cannot be
established but direction is explicit, documented fallback rules are `rate_lower`
→ 0, `rate_hold` → 50, `rate_raise` → 100. Do not fall back simply because the prior
range is absent when the current statement supplies magnitude. Conflicting
explicit magnitude/range evidence follows the conflict rules.

F_rate measures the rate action, not the restrictiveness of the current rate level.

### Guidance

Select the highest available tier first: explicit time/condition commitment about
future rates, then explicit easing/tightening bias, then general support/caution.
Within that tier choose the largest absolute adjustment. An unresolved opposing
tie becomes `null`; do not sum phrases.

| Rule ID | G |
|---|---:|
| `guidance_strong_dovish` | -20 |
| `guidance_moderate_dovish` | -10 |
| `guidance_data_dependent` | 0 |
| `guidance_moderate_hawkish` | 10 |
| `guidance_strong_hawkish` | 20 |

Use the defined directional guidance types, supported by their source context.
A conditional commitment is not automatically dovish merely because it contains
“until.” Explicit data dependence maps to zero; absent guidance remains missing.

### Voting and calculation

| Rule ID | V |
|---|---:|
| `vote_unanimous` | 0 |
| `vote_dovish_dissent`, count 1 / more than 1 | -5 / -8 |
| `vote_hawkish_dissent`, count 1 / more than 1 | 5 / 8 |

Dissent direction is relative to the adopted action and supported by the stated
alternative. Missing or unresolved voting evidence is `null`.

```text
policy_score = clamp(F_rate + G + V, 0, 100)
policy_completeness = 0.60 × available(rate_action)
                    + 0.30 × available(forward_guidance)
                    + 0.10 × available(voting)
```

Missing G or V contributes no adjustment, but receives zero coverage. If the
anchor is missing, override policy score to `null` and policy completeness to 0.

## 6. Balance sheet

| Asset rank | Rule ID | Current-stance fallback score |
|---:|---|---:|
| 0 | `balance_sheet_large_qe_expansion` | 0 |
| 1 | `balance_sheet_ongoing_purchases` | 15 |
| 2 | `balance_sheet_tapering` | 30 |
| 3 | `balance_sheet_reinvestment_only` | 50 |
| 4 | `balance_sheet_reduction_runoff` | 80 |

| Liquidity rank | Rule ID | Current-stance fallback score |
|---:|---|---:|
| 0 | `balance_sheet_liquidity_expanded` | 0 |
| 1 | `balance_sheet_liquidity_normal` | 50 |
| 2 | `balance_sheet_liquidity_reduced` | 75 |
| 3 | `balance_sheet_liquidity_tightening` | 90 |

TypeScript computes current rank minus prior rank within the same scale:

| Difference | Change score |
|---:|---:|
| ≤ -2 | 0 |
| -1 | 20 |
| 0 | 50 |
| 1 | 80 |
| ≥ 2 | 100 |

“Unchanged” is not a stance. Current and prior runoff give change score 50.
Missing current evidence excludes the component. Missing prior evidence invokes
the current-stance fallback per component, whether the document is absent or
merely lacks the relevant evidence. No inference of liquidity from asset purchases.

Score available asset/liquidity components using weights 0.60/0.40, renormalized.
Neither available means category score `null` and completeness zero.

```text
balance_sheet_completeness =
    0.60 × asset_available × (asset_fallback ? 0.80 : 1)
  + 0.40 × liquidity_available × (liquidity_fallback ? 0.80 : 1)
```

Both available with asset-only fallback gives 0.88; liquidity-only gives 0.92;
both fallback gives 0.80. Only asset available with fallback gives 0.48.

## 7. Inflation

Four independent weights: level 0.50, trend 0.25, market expectations 0.125,
survey expectations 0.125. Renormalize available weights for scoring only.
No subcomponent can proxy for another.

An explicit actual 12-month inflation rate uses `inflation_level_numeric`, value
`x` in percent: `clamp(50 + 25 × (x - 2), 0, 100)`. A target, forecast, or unrelated
percentage is not an actual inflation observation.

| Level rule ID | Defined wording | Score |
|---|---|---:|
| `inflation_level_well_below_2` | well/significantly below 2 percent | 10 |
| `inflation_level_below_2` | below 2 percent | 25 |
| `inflation_level_somewhat_below_2` | somewhat below 2 percent | 30 |
| `inflation_level_slightly_below_2` | running slightly below 2 percent | 35 |
| `inflation_level_close_to_2` | close to 2 percent | 45 |
| `inflation_level_near_2` | near/at/right at/around 2 percent | 50 |
| `inflation_level_slightly_above_2` | slightly above 2 percent | 55 |
| `inflation_level_somewhat_elevated` | somewhat elevated | 55 |
| `inflation_level_above_2` | above 2 percent | 75 |
| `inflation_level_elevated` | elevated | 75 |
| `inflation_level_well_above_2` | well/significantly above 2 percent | 90 |

| Trend rule ID | Defined inflation wording | Score |
|---|---|---:|
| `inflation_trend_declined_sharply` | has declined sharply | 10 |
| `inflation_trend_declined` | has declined/fallen/been falling | 20 |
| `inflation_trend_moved_lower` | has moved lower | 25 |
| `inflation_trend_eased` | has eased | 30 |
| `inflation_trend_little_changed` | has been little changed/stable/roughly stable/about the same | 50 |
| `inflation_trend_firmed` | has firmed | 70 |
| `inflation_trend_risen` | has risen/increased/moved higher | 80 |

| Expectations rule ID | Defined wording for the stated measure | Score |
|---|---|---:|
| `inflation_expectations_market_declined` | market-based measures of inflation compensation have declined/fallen | 20 |
| `inflation_expectations_market_moved_lower` | market-based measures of inflation compensation have moved lower | 25 |
| `inflation_expectations_market_stable` | market-based measures of inflation compensation are little changed | 50 |
| `inflation_expectations_market_risen` | market-based measures of inflation compensation have risen/increased | 80 |
| `inflation_expectations_survey_declined` | survey-based measures of longer-term inflation expectations have declined/fallen | 20 |
| `inflation_expectations_survey_stable` | survey-based measures of longer-term inflation expectations are little changed/stable | 50 |
| `inflation_expectations_survey_risen` | survey-based measures of longer-term inflation expectations have risen | 80 |

Slashes denote listed alternatives, not literal evidence strings. Return actual
source quotations. These tables retain the agreed phrases; they do not license
unlisted semantic synonyms or cross-subcomponent inference.

```text
inflation_completeness = 0.50 × available(level)
                       + 0.25 × available(trend)
                       + 0.125 × available(market)
                       + 0.125 × available(survey)
```

There is no separate expectations average carrying 0.25 when only one type is
available. For level 55, trend 30, market 20, survey missing: score = 37.5/0.875
= 42.857142…; completeness = 0.875. No extra sentiment adjustment.

## 8. Labour

| Subcomponent | Weight | Rule ID | Score |
|---|---:|---|---:|
| Unemployment level | 0.20 | `labour_unemployment_low` | 70 |
| | | `labour_unemployment_high` | 15 |
| Unemployment direction | 0.20 | `labour_unemployment_rising` | 20 |
| | | `labour_unemployment_stable` | 50 |
| | | `labour_unemployment_falling` | 80 |
| Job gains | 0.35 | `labour_job_gains_solid` | 65 |
| | | `labour_job_gains_weak` | 20 |
| | | `labour_job_gains_moderated` | 50 |
| Slack/wages | 0.25 | `labour_slack_remains` | 25 |
| | | `labour_market_tight` | 85 |
| | | `labour_wage_pressures` | 80 |
| | | `labour_underemployment` | 30 |

Defined descriptions: low/remained low; elevated/high; moved up/increased/rose;
little changed; declined/fell; solid, weak, moderate/moderated/slowed job gains;
slack remains; labour market tight; wage pressures building; underemployment.
Subject and context must support the selected component.

“Has moved up but remains low” supports direction and level separately. Score
is the weighted mean over available components; completeness is the sum of their
original weights. For 70, 20, 50, null: score = 35.5/0.75 = 47.333333…,
completeness = 0.75. No separate labour sentiment adjustment.

## 9. Growth

| Subcomponent | Weight | Rule ID / defined descriptor | Score |
|---|---:|---|---:|
| Current activity | 0.50 | `growth_contraction` / contraction | 10 |
| | | `growth_moderate_pace` / moderate rate or pace | 55 |
| | | `growth_strong_footing` / strong footing | 65 |
| | | `growth_solid_pace` / solid pace | 70 |
| Forward risks | 0.30 | `growth_downside_risks` / downside risks | 20 |
| | | `growth_activity_weighed_down` / will weigh on activity; uncertainty weighing on activity | 20 |
| | | `growth_below_potential` / below potential | 20 |
| | | `growth_upside_risks` / upside risks | 80 |
| | | `growth_above_potential` / above potential | 80 |
| Specific sectors | 0.20 | `growth_business_fixed_investment_exports_weak` / business fixed investment and exports weak | 25 |
| | | `growth_consumer_spending_strong` / consumer spending strong | 70 |

Keep above/below potential in the agreed forward-risk component; do not silently
move or duplicate them into current activity. Generic uncertainty, balanced
risks, or “pose risks to the economic outlook” without explicit direction does
not supply a forward-risk score. The former separate -5 sentiment adjustment
is removed. Score is the weighted mean over available components; completeness
is the sum of their original weights. No separate growth sentiment adjustment.

## 10. Final calculations, thresholds, and output

```text
baseline_score = sum(base_weight × score for scoreable categories)
               / sum(base_weight for scoreable categories)
coverage = 100 × (0.35 × policy_completeness
                + 0.20 × balance_sheet_completeness
                + 0.20 × inflation_completeness
                + 0.15 × labour_completeness
                + 0.10 × growth_completeness)
```

Apply the policy-anchor exception before selecting scoreable categories.

| Unrounded coverage | Status |
|---|---|
| ≥ 60 | PASS |
| ≥ 40 and < 60 | FLAG |
| < 40 | BLOCKED |

| Unrounded coverage | Confidence |
|---|---|
| ≥ 90 | High |
| ≥ 70 and < 90 | Medium |
| < 70 | Low |

Confidence is coverage-only, including the specified fallback discount. It is
not a probability of correctness. No ambiguity adjustment. Retain full floating-
point precision internally; apply thresholds before rounding. Round final baseline
to one decimal and coverage to two. Keep category scores/completeness unrounded
internally; optional display rounding is two decimals.

Coverage weights and discounts are accumulated as exact integer units before
conversion to percent, preventing binary floating-point drift at exact thresholds.
This is not intermediate rounding or a change to the weights.

Archive components, rule version, category scores/completeness, baseline, coverage,
status, confidence, diagnostics, and the separate jury responses. The lean baseline
payload contains `baseline_score`, `coverage`, `status`, and `confidence`; evidence
and diagnostics stay in the archive.

Subsequent user-approved output addition: retain the separate underlying scores
and add root-level `avg_jury_score` (the three-person mean rounded to one decimal)
and `final_score = (baseline_score + avg_jury_score) / 2`, rounded to one decimal
using the reported scores. Final score is null if baseline is unavailable or any
jury response fails. The 50/50 blend is provisional and does not change baseline
arithmetic or coverage/status/confidence, which still describe baseline evidence.

Illustrative arithmetic only: scores 30, 50, 46.666666…, 47.333333…, 70 and
completeness 1, 0.6, 0.75, 0.75, 0.5 yield baseline 43.933333… → **43.9**,
coverage **78.25**, **PASS**, **Medium**. This assumes verified unchanged assets
and no balance-sheet fallback; it is not a live result.

## 11. Independent jury and implementation plan

Retain these three personas:

- `CENTRAL_BANK_POLICY_ECONOMIST`: dual mandate, reaction function, inflation,
  employment, and policy risks.
- `GOLD_CROSS_ASSET_STRATEGIST`: rates, real yields, dollar, liquidity, risk appetite,
  and gold transmission, without assuming a fixed gold-price response.
- `FINANCIAL_COMMUNICATIONS_ANALYST`: wording, conditionality, confidence, omissions,
  and changes from the prior statement.

Each returns only `{ "jury_score": number, "supporting_statement": string }`
on the same 0–100 hawkishness scale, with no baseline context.

Implemented settings: Pass 1 temperature 0; Pass 2 temperature 0.2. Use the current
runner's configured `gemini-3.5-flash-lite` with medium thinking unless explicitly
changed and documented. Current runner configuration is not proof of per-run
model metadata for the archived 150 responses.

Implementation and verification:

1. `scoring.ts` implements rule mappings, calculation, response schemas, and validation;
   `scoring.test.ts` checks missing data, invalid evidence, normalization, fallback,
   boundaries, and independent call orchestration.
2. `PASS1-BASELINE-PROMPT.md` and `PASS2-JURY-PROMPT.md` replace the combined prompt.
   `fomc_parser.ts` makes one baseline call and three separate jury calls.
3. Live smoke verification is archived in `../../../study-history/results/v05-smoke-statement4-verified.json`.
   The earlier smoke artifact is retained because it exposed a schema issue;
   it is not the final verification result. See README.md for manual commands.
4. Pending: repeat persona-neutral extraction on Statement 4 independently; measure rule
   selections, availability, coverage, and baseline variability.
5. Pending: separately repeat each of the three jury personas; measure jury variability and
   agreement. Baseline repetitions do not belong to personas.
6. Pending: compare with archived results, then extend to historical testing and calibration.
   Stability alone does not establish predictive accuracy.

Record actual model/settings and rule/prompt versions for new runs. Preserve
prior test evidence; do not present old results as tests of this specification.
