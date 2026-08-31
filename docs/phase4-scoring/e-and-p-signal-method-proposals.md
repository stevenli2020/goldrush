# E- and P-class signal method proposals

**Status:** Awaiting owner decision
**Scope:** Proposal only for L3-002, L3-004, L3-005, L5-002 and L5-006. L3-006, L6-001 and L6-002 are complete and unchanged. No reader, signal, scoring-engine, weighting, interaction or probability code is authorized by this document.

## Shared boundary and recommendation

The approved input/status contract permits E-class current curve/event components and P-class panel context, but it does not authorize an unlabelled component choice, cross-country pooling, or a new aggregate. A selected scalar must carry an external `selection_label`, component key, event date and any published aggregate context. The frozen canonical record remains unchanged.

Where the preserved data could support a simple rule, this document identifies the rule as a proposal and the metadata it requires. Until that selection rule is approved and traceable, the affected numeric horizon is `INCOMPLETE`; no value is silently treated as zero or neutral. Where the variable is context-only in the MVP, the recommendation is explicit `NOT_APPLICABLE` for every horizon.

| Variable | Frozen canonical value / unit | Register transformation output | Status and context |
|---|---:|---|---|
| L3-002 | `3.63 percent_per_annum` (2026-08-30) | `L3/002/data/l3_002_phase3_handoff.json`; 19 CME curve contracts, one date | All 19 `AVAILABLE`; contract identity is present only in the preserved output |
| L3-004 | `13.928571428570002 expected_target_change_bps` (2026-08-28) | `L3/004/data/l3_004_phase4_handoff.json`; 8 measures for two meeting dates | All 8 `AVAILABLE`; meeting date and component unit are in the preserved output |
| L3-005 | `3.375 percent` (2026-06-17) | `L3/005/data/l3_005_phase3_handoff.json`; 26 dot-plot bins across four projection horizons | All 26 `AVAILABLE`; bin, horizon, count and median are in the preserved output |
| L5-002 | `0.814218619472411 fraction` (2026-06-30) | `L5/002/data/l5_002_phase3_handoff.json`; 97 panel rows across 18 dates | All 97 `AVAILABLE`; country/panel keys are required by the source builder but are not emitted in the handoff rows |
| L5-006 | `0.062206463251531834 metric_tonnes` (2026-06-01) | `L5/006/data/l5_006_phase3_handoff.json`; 2,724 country-month rows across 294 dates | 5 `AVAILABLE`, 2,719 `STALE`; country/entity keys are not emitted in the handoff rows |

## L3-002 — OIS Forward Policy Curve

**Economic meaning and direction.** The registry defines L3-002 as market pricing of future overnight policy conditions across maturities. A higher policy curve generally raises expected real rates and opportunity cost, which is negative for gold; a lower curve is generally supportive. It is a Layer 3 curve signal and overlaps with L3-001 and L1 policy variables, so later weighting must avoid double counting.

**Proposed MVP method and horizons.** The 19 rates are all same-date contract components. A numeric method would need an approved contract-selection label (or an explicitly defined curve summary such as a named front-to-back spread) and a direction rule. A raw selected rate has no approved neutral anchor; a spread would need an owner-approved pair and sign convention. Recommend `NOT_APPLICABLE` for 1–5 days, 1–3 months and 1–3 years, the registry-applicable horizons, and `NOT_APPLICABLE` for 3–10 years, which is not listed. Do not score the canonical `3.63` as the whole curve.

**History/context.** Class `E` provides 19 current components on one date, not historical observations. Preserve the CME contract key, settlement-derived rate, observation date and source. No pooling of contracts or lookback is permitted.

## L3-004 — Probability Distribution of Future Policy Outcomes

**Economic meaning and direction.** L3-004 captures uncertainty and tail repricing around upcoming policy meetings. The registry assigns conditional direction: tightening expectations can weigh on gold, easing expectations can support it, and uncertainty alone is not directional.

**Proposed MVP method and horizons.** The most direct candidate is the preserved `expected_target_change_bps` component for one explicitly selected upcoming meeting. Use the inherent zero-change anchor: positive expected change maps to gold `-1`, negative expected change to `+1`, and exactly zero to `0`. This rule must carry `selection_label` (for example, `L3-004:expected_target_change_bps`), `meeting_date`, component unit and source. The canonical row currently omits the meeting date and selection label, so no numeric result is implementable until that metadata is supplied without altering the frozen record. Until then, recommend `INCOMPLETE` for the registry-applicable 1–5-day and 1–3-month horizons. Recommend `NOT_APPLICABLE` for 1–3 years and 3–10 years, which the registry does not list. Do not independently score easing, hold and tightening probabilities or use a probability threshold without a separate decision.

**History/context.** Class `E` has eight current measures for two future meetings at one observation date; it has no allowlisted history. Use only the selected meeting/component and retain all other distribution measures as context. No pooling across meetings is allowed.

## L3-005 — FOMC Dot Plot Path

**Economic meaning and direction.** The registry defines L3-005 as official policymaker projections that can shift expectations and the perceived reaction function. A higher projected policy rate is generally negative for gold; a lower projection is generally supportive. Individual dots are not a Committee decision or market forecast.

**Proposed MVP method and horizons.** A potentially anchor-free rule is to compare an explicitly selected dot-plot statistic with the published median for the same `projection_horizon`: above median maps to `-1`, below median to `+1`, and equal to `0`. The simplest candidate statistic is the participant-count-weighted mean of the preserved rate bins for that horizon, but selecting a single bin or using the weighted mean requires an owner-approved `selection_label` and exact projection-horizon mapping to the 1–3-month and 1–3-year outputs. The current canonical row (`3.375%`) omits its horizon, participant count and median, so it cannot be scored as a complete dot-plot signal. Recommend `INCOMPLETE` for 1–3 months and 1–3 years until that component/statistic and horizon mapping are approved. Recommend `NOT_APPLICABLE` for 1–5 days and 3–10 years, which are not registry-applicable. No cross-horizon averaging or arbitrary rate anchor is permitted.

**History/context.** Class `E` provides 26 bins on one SEP release date across 2026, 2027, 2028 and Longer run; no historical series is allowlisted. Preserve projection horizon, rate bin, participant count, published median, release date and source.

## L5-002 — Gold Share of Official Reserves

**Economic meaning and direction.** L5-002 measures strategic allocation weight toward gold rather than absolute holdings. The registry assigns positive direction: a rising gold share indicates stronger official reserve preference for gold over the measured denominator. The registry also requires distinguishing active allocation changes from mechanical market-value changes.

**Proposed MVP method and horizons.** This is a P-class country panel and context-only input. The current handoff emits 97 scalar rows but omits country/panel identity, so no traceable country selection is possible. Do not pool countries or dates and do not treat the canonical `0.8142` fraction as a global aggregate. Recommend `NOT_APPLICABLE` for all four horizons, including the registry-applicable 1–3-year and 3–10-year horizons. A future numeric method would require a preserved country key, an owner-approved country/component selection and a same-country change or level rule.

**History/context.** The allowlist contains 97 panel rows across 18 publication dates, all `AVAILABLE`; it is context, not a pooled time series. Use only an explicitly selected country's own rows. No cross-country mean, date pooling or substitution from L5-001/L0-002 is permitted.

## L5-006 — Official-Sector Gold Sales / Lending

**Economic meaning and direction.** L5-006 is documented as an official-sector net-reduction proxy, not a separately measured sales or lending series. The registry assigns negative direction for official-sector reductions: increased net reduction generally adds gold supply or removes official demand, while the precise mechanism is conditional. Sales, lending, swaps and reporting adjustments cannot be separated.

**Proposed MVP method and horizons.** This is a P-class country-month panel and context-only input. The current handoff emits 2,724 scalar rows but omits country/entity identity; the canonical `0.0622` tonnes cannot be treated as a global reduction. Recommend `NOT_APPLICABLE` for all four horizons, including the registry-applicable 1–3-month and 1–3-year horizons. A future numeric method would require a preserved country/entity key, an approved selection rule and an explicit treatment of the net-reduction proxy. Any selected `STALE` row would be ineligible and could not be used as a current observation or comparison point.

**History/context.** The allowlist contains 2,724 country-month context rows across 294 dates, but only 5 are `AVAILABLE` and 2,719 are `STALE`. No pooling, stale carry-forward, country substitution or derivation from L5-001 is permitted.

## Status treatment for all five variables

- A contract-valid `AVAILABLE` component or selected panel row is eligible only for the explicitly approved method; a variable with no approved MVP numeric rule returns `NOT_APPLICABLE` and retains provenance/context.
- A finite `FLAG` remains visible and flagged. It is not silently promoted to `PASS`, and any later component/panel result retains the flag.
- `STALE` and `BLOCKED` inputs are retained for audit but are ineligible and return `INCOMPLETE` when selected or required. They are never converted to zero, neutral or current data.
- Missing, malformed, non-finite, wrong-unit, invalid-status or duplicate component/panel rows return `INCOMPLETE` with an explicit reason. A missing selection label, component key, event date, projection horizon or panel identity also makes a proposed numeric result `INCOMPLETE`.
- No partial panel drop, cross-meeting substitution, shortened history, fallback source or automatic denominator/weight renormalization is permitted.

## Later implementation test plan

If approved, WSL tests should verify:

1. Readers preserve exact component/panel keys, dates, units, statuses, source references and quality flags, and reject malformed, duplicate, wrong-unit and missing-selection metadata.
2. L3-002 never scores a raw curve point without its contract selection label; all unapproved horizons return explicit `NOT_APPLICABLE`.
3. L3-004 tests the selected expected-target-change rule for positive, negative and zero bps, requires meeting/component labels, and rejects stale or missing meeting context.
4. L3-005 tests the selected statistic-versus-median rule, requires projection horizon and participant metadata, and rejects cross-horizon averaging.
5. L5-002 and L5-006 reject countryless panel selection and verify no pooling; selected stale rows return `INCOMPLETE`.
6. Every result includes variable, horizon, current/component context, selection label, source references, flags, method state and reason. Tests confirm no z-score, percentile, arbitrary threshold, synthetic history or cross-variable substitution is used.

## Owner decision requested

Approve the explicit status-only recommendations and the conditional L3-004/L3-005 component rules, or provide the missing component/panel selection labels, horizon mapping and any additional numeric rule. No implementation should begin until the method and metadata decisions are recorded.
