# Gold Probability Engine — Phase 1 T4 Task Brief
**Prepared by:** Chris (Pragmatic Project Advisor)
**For:** Grace (Task Agent)
**Tranche:** T4 — Layers 6 and 9
**Status:** Approved for execution

---

## 1. Your Objective

Build the complete variable admission records for **Layers 6 and 9** of the Gold Probability Engine.

Deliver one standardized 20-field admission record per candidate variable, with a final ADMIT / CONDITIONAL / REJECT decision for each.

---

## 2. Where T4 Sits in the Registry Sequence

| Tranche | Layers | Status |
|---|---|---|
| T1 | 0, 1, 3 | CLOSED — signed off 2026-08-17 |
| T2 | 4, 5 | IN PROGRESS — not yet signed off |
| T3 | 2, 7 | CLOSED — signed off 2026-08-17 |
| T4 | 6, 9 | **OPEN — this tranche** |
| T5 | 8, 10, 11 | Not started |

Your Criterion B baseline is the **full T1 approved registry** (`docs/phase1-registry/T1-registry.md`) plus the **T3 signed-off registry** (`docs/phase1-registry/T3-registry.md`). T2 is in progress and not yet signed off — do not treat T2 candidates as part of your baseline. If a T4 candidate overlaps with a probable T2 variable, flag the overlap and note that the T2 decision is pending; do not block your own admission on it.

---

## 3. Layers in Scope

### Layer 6 — Geopolitical Transmission Channels

**Role:** Event-driven shock and structural regime layer.

**Primary mechanism:** Geopolitical events affect gold through four distinct transmission channels. Each must be attributed separately — do not treat geopolitical risk as a single undifferentiated variable.

1. **Safe-haven channel** — fear, uncertainty, and conflict increase demand for liquid, non-sovereign stores of value.
2. **Energy/inflation channel** — conflict or disruption raises oil and shipping costs, changing inflation expectations and therefore the expected monetary-policy response, which can be bullish or bearish for gold depending on regime.
3. **Reserve-security channel** — sanctions, reserve freezes, or sovereign-asset seizure risk change official reserve preferences toward assets outside the reach of potential counterparties.
4. **Monetary-system fragmentation channel** — geopolitical fragmentation encourages diversification away from dependence on a single reserve currency or payment system.

**Key observable categories:** Active conflict intensity and escalation signals; sanctions announcements and asset-freeze events; oil and shipping disruption indicators; reserve-security policy changes; geopolitical-risk indices where methodology is transparent; international monetary-system developments.

**Typical horizon:** Intraday (safe-haven spike) to decades (reserve-security and fragmentation structural shifts).

**Critical design rule for Layer 6:** The four channels can reinforce or offset each other. A conflict can be bullish through safe-haven demand and bearish through higher oil prices driving tighter monetary expectations. Every candidate variable must state which channel(s) it captures and how the offsetting channels are handled. Do not automatically label any geopolitical development as bullish for gold.

---

### Layer 9 — Regional Physical-Market Dynamics

**Role:** Regional demand and supply subsystem layer.

**Primary mechanism:** Regional physical markets set local premiums and discounts, alter import flows, change recycling incentives, and identify the marginal physical buyer or seller. China and India are the two primary subsystems and must be treated as distinct mechanisms, not aggregated into a single physical-demand variable.

**China subsystem key observables:** Shanghai Gold Exchange (SGE) premium/discount; Chinese gold ETF flows; PBoC holdings changes; household investment demand; RMB performance; local interest rates; property-market confidence; capital controls.

**India subsystem key observables:** INR/USD; domestic gold price; import duties; rural income and agricultural conditions; wedding calendar seasonality (Dhanteras, Diwali, Akshaya Tritiya); local premiums; recycling; gold-loan activity.

**Other regional observables:** Middle East and Southeast Asia demand signals where data is reliable; LBMA physical market indicators.

**Typical horizon:** Weeks to years, with strong seasonal components in the India subsystem.

**Critical design rule for Layer 9:** L2-003 USD/CNY is already admitted in Layer 2 for its FX purchasing-power and dollar-transmission mechanism. Do not re-admit it as an independent Layer 9 variable. Layer 9 must use its own regional observables — SGE premium, local demand indicators, capital controls — not FX rate variables already covered in Layer 2. Separately, L0 stock/flow variables (L0-002 Central-Bank Gold Holdings, L0-005 Bar-and-Coin Holdings) measure ownership composition of the existing stock. Layer 9 measures regional demand behavior and price formation — these are distinct.

---

## 4. Admission Criteria — All Five Must Pass

Apply Spec C v2 (`docs/specs/v2/spec_c_variable_admission_criteria_v2.md`). Every candidate must satisfy all five:

**Criterion A — Causal Relevance**
Credible mechanism documented. State: (1) what the variable represents, (2) how it affects gold, (3) expected direction, (4) whether the relationship is conditional or regime-dependent.

**Criterion B — Incremental Information**
The T4 baseline is the full T1 and T3 signed-off registries. Every T4 candidate must demonstrate what it adds beyond the variables already admitted. T2 is in progress — flag overlaps, document reasoning, do not delay your decision.

State explicitly: *What does this variable add that the T1/T3 registries and the 12-layer causal architecture do not already adequately capture?*

**Criterion C — Data/Evidence Reliability**
Assess: source authority, methodology, consistency, revision behavior, historical coverage, missing-data risk, publication frequency, access stability.

**Criterion D — Operational Feasibility**
Assess: data accessibility, cost, retrieval reliability, processing complexity, freshness, licensing restrictions, manual intervention required, maintenance burden.

**Criterion E — Forecast-Horizon Relevance**
Variable must be relevant to at least one of the four fixed horizons:
- 1–5 days
- 1–3 months
- 1–3 years
- 3–10 years

State relevant horizon(s), expected importance by horizon, and whether relevance is structural, cyclical, event-driven, or conditional.

---

## 5. Admission Decisions

| Decision | Meaning |
|---|---|
| **ADMIT** | All five criteria sufficiently satisfied. Variable proceeds to implementation with initial research-derived weight. |
| **CONDITIONAL / RESEARCH ONLY** | Causal case is useful but one or more implementation criteria not yet strong enough for production. Retained in research registry only. |
| **REJECT** | Fails one or more fundamental criteria. |

---

## 6. Hard Rule — Do Not Reject on Correlation or Downstream Position Alone

> **Do not reject a variable solely because it is downstream of or correlated with another variable. Reject only when it fails the incremental-information test or another Spec C criterion.**

Many Layer 6 and Layer 9 variables will be downstream of macro or policy shocks. Transmission position is a classification matter, not a rejection criterion.

---

## 7. Overlap Classification (Qualitative Only)

| Flag | Meaning |
|---|---|
| **Duplicate candidate** | Materially represents the same information as another variable; combined effective weight should not double-count |
| **Transmission candidate** | Downstream of an upstream driver; transmits part of the same shock but may carry incremental information |
| **Interaction candidate** | Joint effect with another variable that cannot be represented by adding independent contributions alone |

**Do NOT assign numerical D_i or T_i values.** That belongs to Spec A implementation in a later phase.
**Do NOT reject a variable solely because it receives a flag.**

For variables that appear in multiple layers: record the mechanism/channel that justifies its role in THIS layer specifically.

---

## 8. T4-Specific Cross-Layer Risks to Manage

Address each directly in your admission records.

### Layer 6 risks

**L6 / L4 boundary (energy/inflation channel):** Oil price variables belong in L6 only when the mechanism is geopolitical supply disruption. If the mechanism is inflation-level or purchasing-power effect, it belongs in L4 (T2 scope). State explicitly which channel an oil-related variable is capturing; do not double-admit it at full weight in both layers.

**L6 / L5 boundary (reserve-security channel):** Layer 5 covers strategic reserve-allocation behavior (T2 scope). Layer 6 reserve-security variables should capture the geopolitical trigger — sanctions announcements, asset-freeze events, sovereign-seizure risk — not the resulting reserve-allocation decision, which belongs in L5. Mechanism ownership must be explicit.

**L6 / L7 boundary (fragmentation channel):** Monetary-system fragmentation can affect Layer 7 liquidity and financial conditions. The L6 mechanism is the geopolitical driver of fragmentation; L7 captures the resulting realized liquidity and funding-stress conditions. Do not treat the same fragmentation development as a full-weight independent contribution in both layers.

**L6 analytical variable treatment:** Most Layer 6 variables will be analytical (Type B) rather than quantitative (Type A). Spec D v2 applies in full — every analytical assessment requires the nine-field evidence record, the five-factor confidence rubric, and explicit fact/interpretation separation. Do not treat geopolitical assessments as free-form judgments.

### Layer 9 risks

**L9 / L0 boundary:** L0 measures the stock and ownership composition of existing gold (central-bank holdings, ETF holdings, bar-and-coin holdings). L9 measures regional demand behavior and physical-market price formation. A central-bank purchase appears in L0 as a stock change and in L5 as a reserve-allocation decision. It does not independently belong in L9 unless the mechanism is specifically regional physical-market price formation (e.g., PBoC buying affecting SGE premium).

**L9 / L8 boundary (future T5):** Investment flows (Layer 8) will be covered in T5. Chinese gold ETF flows are a candidate for L9 where the mechanism is regional physical-market demand; the same flows considered as financial investment-allocation belong in L8. Attribute explicitly. Do not pre-empt T5 scope by admitting flow variables in L9 without explicit regional-physical-market mechanism justification.

**L9 / L2 boundary:** L2-003 USD/CNY is already admitted in Layer 2. Do not re-admit it in Layer 9. RMB performance as a regional physical-market condition variable is distinct from USD/CNY as an FX transmission variable — if RMB weakness is used to explain local gold demand behavior (not FX pricing), document the mechanism carefully and avoid duplicating the L2-003 FX signal.

**L9 data quality caution:** Regional physical-market data for India and China is often less standardized than developed-market financial data. Source authority, revision behavior, and coverage must be assessed rigorously. Conditional admission is appropriate where the causal case is strong but data reliability is not yet production-grade.

---

## 9. The 20-Field Admission Record

Complete one record per candidate variable:

```
Variable name:
Layer:
Variable ID:          [Format: L{layer number}-{sequence number}, e.g. L6-001]
Causal mechanism:
Direction:            [Expected gold relationship: Positive / Negative / Conditional]
Incremental information:
Overlap:              [List overlapping variables + qualitative flag: Duplicate / Transmission / Interaction candidate]
Data/evidence source:
Reliability:          [Assessment narrative]
Historical depth:     [Available coverage]
Frequency:            [Update frequency]
Freshness:            [How quickly it becomes stale]
Accessibility:        [Free / Crawlable / Paid / Restricted]
Operational burden:   [Low / Medium / High]
Relevant horizons:    [One or more of the four fixed horizons]
Initial weight rationale:
Evidence references:
Decision:             [ADMIT / CONDITIONAL / REJECT]
Review date:
Reviewer:
```

---

## 10. What You Are NOT Doing

- Do not modify the 12-layer architecture
- Do not assign or change layer-level weights
- Do not assign numerical D_i or T_i values
- Do not assign γ_ij interaction coefficients
- Do not fabricate historical quantitative data
- Do not reference v1 specs for any decision
- Do not use correlation alone as grounds for rejection or interaction flagging
- Do not treat geopolitical risk as a single undifferentiated variable — attribute to one of the four approved channels
- Do not automatically label any geopolitical development as bullish for gold
- Do not re-admit L2-003 USD/CNY in Layer 9
- Do not pre-empt T5 scope (Layers 8, 10, 11)
- Do not apply Spec D free-form judgment to analytical variables — the five-factor rubric is mandatory

---

## 11. Deliverable Format

For each layer (6 and 9), deliver:

1. A candidate variable list with brief rationale for why each was considered
2. One complete 20-field admission record per candidate
3. A short layer summary table:

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|

4. Cross-layer overlap notes relevant to T5 (for review before T5 opens)

---

## 12. Authoritative References

| Document | Location | Use |
|---|---|---|
| Causal model | `docs/gold_price_causal_model_v2_2.md` | Layer definitions, mechanisms, observables |
| Spec C v2 | `docs/specs/v2/spec_c_variable_admission_criteria_v2.md` | Admission criteria and decision rules |
| Spec A v2 | `docs/specs/v2/spec_a_interaction_dependency_rules_v2.md` | Overlap classification reference |
| Spec D v2 | `docs/specs/v2/spec_d_ai_evidence_protocol_v2.md` | Analytical variable evidence and confidence rubric |
| Handoff | `handoff/Claude-Handoff.md` | SSOT and lessons |
| T1 Registry | `docs/phase1-registry/T1-registry.md` | Criterion B baseline |
| T3 Registry | `docs/phase1-registry/T3-registry.md` | Criterion B baseline |

Do not reference v1 specs.

---

## 13. Lessons from T1 and T3 Relevant to T4

- **Channel attribution is mandatory for Layer 6.** Every geopolitical variable must state which of the four channels it captures. Offsetting channels must be acknowledged.
- **Analytical variables require the full Spec D rubric.** Free-form confidence values are not permitted.
- **Conditional admissions are legitimate.** Strong causal case + weak data = CONDITIONAL, not REJECT.
- **Mechanism attribution must be explicit.** When a variable could belong in more than one layer, state clearly why it belongs in THIS layer.
- **Regional data quality is often lower than financial data.** Assess Criterion C rigorously for L9 candidates; do not admit on the basis of conceptual appeal alone.
- **Qualitative flags only.** No numerical D_i, T_i, or γ_ij values in Phase 1.

---

## 14. Scope Control Reminder (Spec C Section 13)

> **The purpose of variable admission is not to collect every potentially relevant indicator. It is to build the smallest credible set of variables that adequately represents each causal layer and supports the four forecast horizons.**

Bias toward precision over completeness.

---

**End of T4 Brief**
