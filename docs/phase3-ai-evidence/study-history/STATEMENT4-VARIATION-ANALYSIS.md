# Statement 4: variation audit

Date: 2026-08-27. Scope: 30 recorded responses to the 2024-09-18 FOMC statement, compared with 2024-07-31. This is an analysis of saved responses, not a new model run, a replacement score, or approval of the method.

## Main finding

Statement 4's variation is primarily a problem of mapping language into scoring inputs, with insufficient numerical validation and audit detail. It is not demonstrated to be a failure to read the 50 bp cut, and it is not mainly a stable difference between the three personas.

The supplied statement combines changes and levels: easing policy while continuing runoff; rising unemployment that is still low; improving inflation that remains above target; and changes to a prior restriction on cuts. Several rules permit different mappings of these facts.

There is direct evidence of inconsistent mappings in the response diagnostics. The exact contribution of each mapping to each final score is not recoverable: the response contract saves category quotations, not component values, category scores, completeness masks, or the numerical guidance-diff adjustment.

## 1. Evidence and method

Inspected:

- All 30 statement 4 JSON files under [results/150-TEST](results/150-TEST).
- [Current statement](../study/statements/statement4.md) and [prior statement](../study/statements/previous4.md).
- Historical operative prompt, scoring rules, and runner inspected at the time of this analysis. The superseded prompt/rules were subsequently removed and the runner replaced; the current implementation is not the historical snapshot.
- The official [September release](https://www.federalreserve.gov/newsevents/pressreleases/monetary20240918a.htm) and [July release](https://www.federalreserve.gov/newsevents/pressreleases/monetary20240731a.htm).

All 30 policy quotations identify the half-percentage-point reduction. All 149 non-MISSING quotations across the five main categories match the current input after normalizing whitespace, case, apostrophes, and typographical hyphens. This validates the quoted passages, not the unrecorded mappings or arithmetic.

Twenty responses report at least one extraction ambiguity; ten report none. Sixteen mention inflation ambiguity, and five mention liquidity ambiguity. Every response reports that the prior statement was available and that balance-sheet fallback was not used. These are model-reported diagnostics, not independently recorded component calculations.

Current file modification times precede the saved responses. However, the result schema does not preserve the submitted prompt, source snapshot identifiers, model version, or generation settings per call. Modification times alone do not prove identical historical requests.

## 2. How large is the variation?

Scores are on a 0–100 scale. Repeat SD below is sample SD within each persona; pooled SD combines the three within-persona variances, with 27 residual degrees of freedom.

| Persona | Mean baseline | Baseline repeat SD | Mean jury | Jury repeat SD |
|---|---:|---:|---:|---:|
| Policy economist | 46.75 | 5.60 | 39.00 | 3.56 |
| Gold strategist | 45.57 | 3.88 | 37.80 | 3.55 |
| Communications analyst | 45.35 | 4.08 | 36.50 | 4.93 |
| Combined mean / pooled repeat SD | 45.89 | 4.59 | 37.77 | 4.06 |

Baseline range: 38.50–56.10. Jury range: 28–45. The middle half of baseline observations falls between 42.50 and 48.50; the variation is not confined to one exceptional file.

The other four statements have pooled baseline repeat SD 2.25 and jury repeat SD 2.75. Statement 4 therefore has about twice their baseline SD and 1.48 times their jury SD.

A descriptive sum-of-squares decomposition attributes only 1.96% of statement 4 baseline dispersion to differences between persona means; 98.04% is within personas. This is not a causal estimate, but it argues against persona selection being the main source of baseline instability. For jury scores, the corresponding between-persona fraction is 6.55%.

Five baseline outputs exceed 50; all 30 jury outputs are below 50. Crossing 50 is a useful diagnostic here, not proof that the higher baseline is economically wrong.

## 3. Same evidence and coverage, different scores

| Persona and repeats | Coverage in both | Baselines | Difference | Jury scores |
|---|---:|---:|---:|---:|
| Policy economist, 6 and 7 | 81.30 | 38.70 / 52.40 | 13.70 | 38 / 35 |
| Policy economist, 3 and 9 | 73.25 | 46.10 / 56.10 | 10.00 | 42 / 42 |
| Gold strategist, 4 and 7 | 81.25 | 43.60 / 38.60 | 5.00 | 35 / 42 |

For the first two pairs, the five main category quotations are substantively the same; the policy quote has only a small prefix difference. In the gold pair, all five category quotations are exactly identical.

[Policy 6](results/150-TEST/statement4-policy-economist-rep6.json) and [Policy 7](results/150-TEST/statement4-policy-economist-rep7.json) report no extraction ambiguities. Their guidance-diff descriptions differ, but no numerical adjustment is saved. That difference may matter, but it cannot be used to reconstruct the 13.70-point gap.

Coverage and baseline have a Pearson correlation of 0.002 across the 30 responses. This means essentially no linear association in this sample; it does not prove that changing extracted components cannot affect scores.

## 4. Confirmed and plausible mechanisms

### A. Inflation mapping varies — directly documented

The current statement conveys both disinflation progress and continuing elevation, without an actual 12-month inflation number or market/survey expectation measurement.

The response files explicitly take different routes:

| Response | Recorded handling |
|---|---|
| [Gold 7](results/150-TEST/statement4-gold-strategist-rep7.json) | Maps the level description to the slightly-above-target rule. |
| [Communications 3](results/150-TEST/statement4-communications-analyst-rep3.json) | Maps the level description to the above-target rule. |
| [Gold 8](results/150-TEST/statement4-gold-strategist-rep8.json) | Marks the whole inflation category MISSING because the wording does not map cleanly. |
| [Gold 5](results/150-TEST/statement4-gold-strategist-rep5.json) | Reports mapping trend and expectations through the inflation-level description. |
| [Gold 9](results/150-TEST/statement4-gold-strategist-rep9.json) | Reports trend and expectations as MISSING for lack of matching phrases. |

A current inflation level is not itself evidence about market/survey expectations. The Committee's confidence that inflation is converging toward its objective is also not a market/survey expectations measure. Using one as a proxy for another changes both score and reported coverage.

This is the clearest documented inconsistency. The archive does not contain the numerical choices, so no exact variance share can be assigned to it.

### B. The labour rule mixes current level with change — a specific ambiguity

The statement describes unemployment as having increased while remaining low. The prompt assigns 15 to an increase and 70 to a low level, but does not say which takes precedence when both occur.

The phrase describing slower hiring can also be mapped to moderated gains, weak gains, or MISSING. [Communications 10](results/150-TEST/statement4-communications-analyst-rep10.json) and [Communications 5](results/150-TEST/statement4-communications-analyst-rep5.json) explicitly map slower gains to moderated gains.

With job gains fixed at 50 and slack/wages unavailable, unemployment 15 versus 70 changes the labour category from 31.33 to 60.67. With all five categories available, that changes the final baseline by 4.40 points without changing coverage.

This is a sensitivity calculation from the rules. The saved files do not reveal whether any particular high/low baseline actually selected 15 or 70.

### C. Policy guidance and comparison adjustments are insufficiently pinned down

The numeric action itself is clear:

- Prior midpoint: 5.375%.
- Current midpoint: 4.875%.
- Change: -50 bp.
- Rate-action anchor: 25.
- Bowman preferred a smaller cut; relative to the adopted action, that is a hawkish dissent, yielding +5 under the stated rule.

If guidance is classified as explicit data dependence, G is zero and the policy category is 30. The prompt also offers support/commitment classifications with negative adjustments, without defining a unique treatment of the current mixture of policy support and data dependence.

The previous restriction on cutting rates disappears from the new statement. Several related changes could be regarded as one policy idea or multiple additions/removals. The current prompt does not specify the exact phrase list, how to collapse equivalent changes, or precisely where the guidance-diff amount enters the final calculation.

Only three responses save a numerical guidance-diff entry: Policy repeats 1, 3, and 8, all -5. Fourteen save a recognizable current/prior quotation; the remaining thirteen use descriptions. The descriptions cannot establish whether a numeric -5, -10, zero, or another adjustment was applied.

Wording such as “hawkish removal” is ambiguous: it may mean removal of hawkish guidance, not a hawkish change. It is not evidence by itself that an agent used the wrong sign.

### D. Runoff is confused with separate liquidity evidence — directly documented

Both supplied statements continue balance-sheet runoff. Under the specified comparison-of-stance rule, the asset-purchase subcomponent should receive 50 for no stance change. That differs from the fallback score of 80 for a current runoff stance.

No response admits using fallback, so it is not justified to claim that a particular model output used 80. Without category values, accidental state/change substitution cannot be tested.

There is direct evidence of a related problem: [Policy 4](results/150-TEST/statement4-policy-economist-rep4.json) says liquidity operations were mapped from the asset-holdings reduction text. [Gold 9](results/150-TEST/statement4-gold-strategist-rep9.json) says liquidity operations were missing.

The asset-runoff clause does not supply an independent liquidity-operations observation. Reusing it across these subcomponents conflicts with the rules file's prohibition on scoring the same evidence twice within a category and changes coverage by 8 percentage points.

### E. Generic uncertainty is sometimes treated as directional downside risk

[Policy 1](results/150-TEST/statement4-policy-economist-rep1.json) reports mapping general uncertainty to a downside-risk adjustment. The source also describes risks across both mandates as balanced; uncertainty alone does not establish their direction.

The prompt has downside-risk and uncertainty-adjustment rules, but no explicit boundary separating nondirectional uncertainty from identified downside risks. This can change growth scoring and coverage. Its exact numerical effect in that response is unrecorded.

## 5. Numerical sensitivity of the scoring rules

These are analytical examples with other choices held fixed, not reconstructed agent calculations. Final-score effects assume all five categories are available and no score hits a clamp.

| Choice that changes | Potential final-score difference | Conditions |
|---|---:|---|
| Unemployment low (70) versus rising (15) | 4.40 | Job-gains score 50; wages/slack missing |
| Job gains moderated (50) versus weak (20) | 2.10 | Unemployment available; wages/slack missing |
| Inflation level slightly above (55) versus above (75) | 2.67 | Trend 30; expectations missing |
| Guidance zero versus strong dovish -20 | 7.00 | Same rate action and vote |
| Runoff unchanged (50) versus runoff stance fallback (80) | 6.00 | Asset-purchase component only; other categories available |
| One -5 guidance change versus two changes totalling -10 | 5.00 | Adjustment applied to final composite |
| Add a downside-risk score 20 to growth score 70 | 1.88 | Only activity and forward-risk subcomponents available |

Several of these choices can interact, making a 10–18 point overall swing plausible. These effects must not be summed and described as an explanation of the observed variance: we lack the component records required for that attribution.

When a whole inflation category is omitted, the remaining category weights are renormalized. Policy's effective weight rises from 35% to 43.75%, balance sheet from 20% to 25%, labour from 15% to 18.75%, and growth from 10% to 12.5%. Missingness therefore changes the influence of other evidence as well.

## 6. Coverage and confidence are not fully reliable in these outputs

Under the separate-component definitions, these observations are not supplied by the current statement:

| Missing component | Overall coverage weight |
|---|---:|
| Independent liquidity operations | 8.00 |
| Market/survey inflation expectations | 5.00 |
| Slack/wage pressures | 3.75 |
| Specific sector conditions | 2.00 |
| Total | 18.75 |

Even allowing every other component, including forward risks, to be extractable, coverage is capped at 81.25%. This is a conservative ceiling, not a reconstructed coverage value. If nondirectional uncertainty does not qualify as forward-risk evidence, the ceiling becomes 78.25%.

Six reported values exceed the conservative ceiling, allowing for rounding 81.25 to 81.3:

| Response | Reported coverage |
|---|---:|
| [Policy 2](results/150-TEST/statement4-policy-economist-rep2.json) | 86.25 |
| [Gold 1](results/150-TEST/statement4-gold-strategist-rep1.json) | 84.25 |
| [Gold 10](results/150-TEST/statement4-gold-strategist-rep10.json) | 84.30 |
| [Communications 1](results/150-TEST/statement4-communications-analyst-rep1.json) | 86.25 |
| [Communications 4](results/150-TEST/statement4-communications-analyst-rep4.json) | 85.00 |
| [Communications 8](results/150-TEST/statement4-communications-analyst-rep8.json) | 91.30 |

They require unsupported availability, double counting, another normalization rule, or incorrect arithmetic. Component masks are missing, so these alternatives cannot be separated retrospectively.

There is also a formula-level check independent of semantic judgment. The 14 binary component contributions, in coverage percentage points, are:

`21, 10.5, 3.5, 12, 8, 10, 5, 5, 6, 5.25, 3.75, 5, 3, 2`.

Any valid sum is a multiple of 0.25. [Policy 8](results/150-TEST/statement4-policy-economist-rep8.json) reports 76.6, which is neither a valid sum nor a standard rounding of one to the displayed precision. Values such as 76.3 can be legitimate one-decimal rounding of 76.25 and are not treated as errors by this check.

Two confidence labels conflict with the current prompt thresholds:

- [Policy 4](results/150-TEST/statement4-policy-economist-rep4.json): Medium at coverage 67, below the required 70.
- [Policy 6](results/150-TEST/statement4-policy-economist-rep6.json): High at coverage 81.3, below the required 90.

All 30 statuses are PASS because their reported coverage exceeds 60. That status checks the model-reported completeness threshold; it does not independently validate evidence, arithmetic, or repeatability.

## 7. Why the current implementation permits these problems

### The operative prompt and rules file disagree

The rules file requires exact or explicitly approved mappings and forbids inferring a score from similar language. The operative prompt explicitly allows equivalent wording for inflation. The runner sends the prompt file only; it does not send SCORING-RULES.md.

AI extraction is the accepted design. The issue is not use of AI; it is that the permitted equivalences and precedence rules are not defined consistently. The rules file also retains obsolete statements that AI output cannot enter the baseline, despite the accepted AI-extraction approach.

### The AI supplies both facts and arithmetic without independent checking

The runner parses the returned text as JSON and writes it to disk. It does not recalculate the baseline, coverage, confidence, or status, validate the schema numerically, or verify evidence/missingness.

JSON validity therefore says nothing about conformity to the scoring formula.

### The lean response omitted information needed to audit the score

The saved fields contain final numbers and short category evidence. They omit:

- The selected component scores and available/MISSING markers.
- F_rate, G, V, category totals, and applied adjustment values.
- The weights actually retained in each normalized calculation.
- A source reference for each extracted subcomponent.

A short category quotation can support multiple, contradictory mappings. We cannot tell whether an unexplained score gap is caused by a mapping change, different missingness, misplaced adjustment, or arithmetic error.

### Current runtime facts are not preserved per test

The current runner specifies gemini-3.5-flash-lite, temperature 0.2, and medium thinking. It creates a fresh request and does not pass earlier responses into later runs. It does not record a seed or model/version metadata in individual result files.

These observations do not establish the historical settings of every test. There is no basis here to attribute the variance specifically to model size, temperature, or a mid-test model change. The current code should not be described as a verified Gemini 3.6 run.

### The semantic jury remains uncalibrated

The jury prompt defines the endpoints and midpoint, but has no fixed anchors for choosing, for example, 35 versus 42 for the same interpretation. Its 28–45 range is consistent with varying strength assigned to an easing interpretation; all 30 remain below 50.

Same-call generation after baseline scoring may also couple the assessments. It is a design risk, not a demonstrated cause of this dataset's variance.

## 8. Focused recommendations

No fixes or API retests were performed during this audit.

1. Keep AI responsible for reading the language. Add only the component scores, available/MISSING markers, and applied adjustments to archived evidence. The Phase 4 payload can remain lean.
2. Compute aggregation, normalization, coverage, confidence, and status in TypeScript from those structured AI inputs. This does not require a natural-language parser.
3. Resolve the specific ambiguous mappings: unemployment level versus change; inflation elevation versus trend versus expectations; asset runoff versus separate liquidity; general uncertainty versus directional risk; and a unique guidance-diff placement/deduplication rule.
4. Add explicit constraints: a target is not a measured inflation rate; the Fed's own confidence is not survey/market expectations; ongoing runoff does not prove a new independent liquidity operation; missing components remain missing.
5. Preserve the exact submitted prompt and plain model/settings metadata with a test batch. The recorded result should identify that batch without adding unnecessary infrastructure.
6. Retest the same statement, same model/settings, and same persona count after each focused change. Compare both component choices and final-score SD. Keep the original results unchanged and use separate output paths.

The existing 60% PASS threshold is not the cause of the score swings. Changing that threshold would not repair inconsistent mappings or calculations. Do not infer a new threshold or claim calibrated accuracy from this audit.

## Appendix: all 30 responses and their reported ambiguities

The descriptions below are copied from the responses. They document what the model said; they do not establish that its hidden calculation followed that description.

| Response | Baseline | Jury | Coverage % | Reported ambiguity |
|---|---:|---:|---:|---|
| [Communications 1](results/150-TEST/statement4-communications-analyst-rep1.json) | 42.50 | 35.00 | 86.25 | None reported |
| [Communications 2](results/150-TEST/statement4-communications-analyst-rep2.json) | 48.50 | 40.00 | 77.50 | None reported |
| [Communications 3](results/150-TEST/statement4-communications-analyst-rep3.json) | 42.50 | 32.00 | 76.25 | Inflation level 'somewhat elevated' mapped to above target rule with minor ambiguity. |
| [Communications 4](results/150-TEST/statement4-communications-analyst-rep4.json) | 46.50 | 42.00 | 85.00 | None reported |
| [Communications 5](results/150-TEST/statement4-communications-analyst-rep5.json) | 48.90 | 35.00 | 81.25 | Somewhat elevated mapped to slightly above 2% level score. / Job gains slowed mapped to moderated. |
| [Communications 6](results/150-TEST/statement4-communications-analyst-rep6.json) | 52.60 | 45.00 | 73.25 | Inflation trend phrased as progress rather than explicit directional easing verb |
| [Communications 7](results/150-TEST/statement4-communications-analyst-rep7.json) | 42.50 | 38.00 | 72.00 | None reported |
| [Communications 8](results/150-TEST/statement4-communications-analyst-rep8.json) | 44.40 | 35.00 | 91.30 | None reported |
| [Communications 9](results/150-TEST/statement4-communications-analyst-rep9.json) | 46.60 | 35.00 | 81.25 | Inflation trend and expectations mapped as missing due to qualitative progress phrasing not strictly matching explicit directional rules. |
| [Communications 10](results/150-TEST/statement4-communications-analyst-rep10.json) | 38.50 | 28.00 | 73.25 | Inflation level 'somewhat elevated' mapped to rule-based equivalent. / Job gains 'slowed' mapped to 'moderated'. |
| [Gold 1](results/150-TEST/statement4-gold-strategist-rep1.json) | 48.50 | 35.00 | 84.25 | Inflation trend and expectations subcomponents partially implicit |
| [Gold 2](results/150-TEST/statement4-gold-strategist-rep2.json) | 48.50 | 38.00 | 72.50 | Liquidity operations subcomponent missing explicit detail beyond runoff mention. |
| [Gold 3](results/150-TEST/statement4-gold-strategist-rep3.json) | 45.00 | 35.00 | 73.25 | Inflation trend and expectations subcomponents omitted due to lack of explicit keyword matches in current statement. |
| [Gold 4](results/150-TEST/statement4-gold-strategist-rep4.json) | 43.60 | 35.00 | 81.25 | Inflation trend and expectations subcomponents missing explicit rule matches in current statement text. |
| [Gold 5](results/150-TEST/statement4-gold-strategist-rep5.json) | 50.90 | 35.00 | 81.25 | Inflation trend and expectations subcomponents mapped via level description due to absence of explicit rate figures. |
| [Gold 6](results/150-TEST/statement4-gold-strategist-rep6.json) | 46.60 | 35.00 | 81.25 | Inflation trend and expectations subcomponents not explicitly quantified in the text. |
| [Gold 7](results/150-TEST/statement4-gold-strategist-rep7.json) | 38.60 | 42.00 | 81.25 | Inflation level 'somewhat elevated' mapped to slightly above 2% rule equivalent. |
| [Gold 8](results/150-TEST/statement4-gold-strategist-rep8.json) | 42.50 | 45.00 | 66.25 | Inflation level and trend phrasing 'somewhat elevated' and 'made further progress' do not map cleanly to exact rule definitions. |
| [Gold 9](results/150-TEST/statement4-gold-strategist-rep9.json) | 42.10 | 38.00 | 73.25 | Inflation trend and expectations mapped to MISSING due to lack of exact rule-matching phrases. / Liquidity operations component missing from balance sheet text. |
| [Gold 10](results/150-TEST/statement4-gold-strategist-rep10.json) | 49.40 | 40.00 | 84.30 | Inflation trend and expectations subcomponents mapped via level proxy due to structural statement wording changes. |
| [Policy 1](results/150-TEST/statement4-policy-economist-rep1.json) | 45.10 | 38.00 | 76.25 | Forward risks phrasing 'uncertain' mapped to downside risk adjustment. |
| [Policy 2](results/150-TEST/statement4-policy-economist-rep2.json) | 45.00 | 35.00 | 86.25 | Inflation expectations and specific forward risk mappings lacked direct lexical matches in the primary assessment paragraphs. |
| [Policy 3](results/150-TEST/statement4-policy-economist-rep3.json) | 46.10 | 42.00 | 73.25 | Liquidity operations not explicitly detailed outside of standard runoff reference. / Inflation trend and expectations subcomponents map partially via general progress wording. |
| [Policy 4](results/150-TEST/statement4-policy-economist-rep4.json) | 45.20 | 38.00 | 67.00 | Liquidity operations subcomponent mapped from asset holdings reduction text. |
| [Policy 5](results/150-TEST/statement4-policy-economist-rep5.json) | 38.80 | 35.00 | 76.30 | Inflation trend phrased as progress rather than explicit directional verb from standard list / Liquidity operations not explicitly mentioned |
| [Policy 6](results/150-TEST/statement4-policy-economist-rep6.json) | 38.70 | 38.00 | 81.30 | None reported |
| [Policy 7](results/150-TEST/statement4-policy-economist-rep7.json) | 52.40 | 35.00 | 81.30 | None reported |
| [Policy 8](results/150-TEST/statement4-policy-economist-rep8.json) | 48.50 | 42.00 | 76.60 | None reported |
| [Policy 9](results/150-TEST/statement4-policy-economist-rep9.json) | 56.10 | 42.00 | 73.25 | None reported |
| [Policy 10](results/150-TEST/statement4-policy-economist-rep10.json) | 51.60 | 45.00 | 73.30 | None reported |

## Limit of this diagnosis

Confirmed: quoted evidence is largely stable; numerical outputs vary; several mappings differ explicitly; some coverage/confidence results violate the stated rules; the runner does not verify the arithmetic.

Not recoverable from these files: the exact component-by-component calculation of each final baseline, or a causal percentage attribution of variance to inflation, labour, guidance, or arithmetic. Producing such an attribution now would require inventing missing intermediates.
