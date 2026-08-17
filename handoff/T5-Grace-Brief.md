# Gold Probability Engine — Phase 1 T5 Task Brief
**Prepared by:** Chris (Pragmatic Project Advisor)
**For:** Grace (Task Agent)
**Tranche:** T5 — Layers 8, 10, and 11
**Status:** Approved for execution

---

## 1. Your Objective

Build the complete variable admission records for **Layers 8, 10, and 11** of the Gold Probability Engine.

Deliver one standardized 20-field admission record per candidate variable, with a final ADMIT / CONDITIONAL / REJECT decision for each.

---

## 2. Where T5 Sits in the Registry Sequence

| Tranche | Layers | Status |
|---|---|---|
| T1 | 0, 1, 3 | CLOSED — signed off 2026-08-17 |
| T2 | 4, 5 | IN PROGRESS — not yet signed off |
| T3 | 2, 7 | CLOSED — signed off 2026-08-17 |
| T4 | 6, 9 | IN PROGRESS — not yet signed off |
| T5 | 8, 10, 11 | **OPEN — this tranche** |

Your Criterion B baseline is the **full T1 approved registry** (`docs/phase1-registry/T1-registry.md`) and the **T3 signed-off registry** (`docs/phase1-registry/T3-registry.md`). T2 and T4 are in progress and not yet signed off — do not treat their candidates as part of your baseline. If a T5 candidate overlaps with a probable T2 or T4 variable, flag the overlap and note that those decisions are pending; do not block your own admission on them.

---

## 3. Layers in Scope

### Layer 8 — Investment Flows

**Role:** Marginal price-setting layer at short and medium horizons.

**Primary mechanism:** Investment flows — actual capital allocation into and out of gold investment products and financial exposures — can become the marginal price-setting force over short and medium horizons, particularly when flows enter highly liquid ETFs or derivatives-linked strategies. The mechanism is the flow itself as a demand or supply signal, not the underlying macro driver that caused the flow.

**Key observable categories:** Gold ETF inflows/outflows (GLD, IAU, major Asian ETFs); institutional fund allocations; pension and mutual-fund exposure changes; bar-and-coin investment demand; large fund positioning; retail investment flows.

**Typical horizon:** Days to quarters.

**Critical design rule for Layer 8:** Layer 8 captures flows as a demand/supply signal. The upstream causes of those flows — monetary policy, real yields, geopolitical events — belong in their respective layers (L1, L3, L6, etc.). Do not re-attribute the upstream cause to Layer 8. Separately, L0-003 Gold ETF Holdings measures the stock of gold held in ETFs (ownership composition). Layer 8 ETF flow variables measure the weekly change in that stock — these are distinct and both may be admitted without duplication if their mechanisms are clearly separated.

---

### Layer 10 — Market Microstructure and Derivatives

**Role:** Amplifier and transmission mechanism layer.

**Primary mechanism:** Microstructure determines how strongly a fundamental shock is transmitted into price. The same macro shock can produce a small move in one positioning environment and a much larger move in a crowded or illiquid market. Positioning, options gamma, margin, and systematic flow mechanics are amplifiers — they are generally not independent causes of gold price moves, but they can materially change the magnitude and speed of moves driven by other layers.

**Key observable categories:** COMEX futures open interest; CFTC Commitments of Traders (COT) managed-money net length; commercial positioning; options open interest; call/put skew; dealer gamma exposure; futures basis; COMEX warehouse stocks; margin requirements; CTA/systematic trend positioning; algorithmic flow proxies; gold lease/forward indicators where available.

**Typical horizon:** Minutes to weeks.

**Critical design rule for Layer 10:** Positioning variables should be classified as amplifiers or transmission mechanisms, not independent fundamental drivers, unless there is specific evidence that a positioning dynamic has become a self-sustaining cause rather than a consequence. The admission record must state whether each variable is being admitted as an amplifier, a leading signal, or a market-stress indicator. L0-009 Gold Lease Rates / Forward Rates is already admitted in Layer 0 for its stock-mobility and physical-financing mechanism — do not re-admit it in Layer 10 for the same mechanism; if a different microstructure mechanism is identified, document it explicitly.

---

### Layer 11 — Expectations, Psychology, and Reflexivity

**Role:** Feedback amplifier and narrative layer.

**Primary mechanism:** Gold price can influence future demand, meaning price is not only an outcome of fundamentals but becomes an input into the next round of flows. This reflexive loop — price rise → media attention → retail interest → ETF flows → futures positioning → momentum buying → further price rise — can amplify fundamental moves, create overshoots, and temporarily sustain prices beyond what traditional valuation relationships imply. The reverse loop operates during liquidation.

**Key observable categories:** Google Trends and search intensity for gold-related terms; financial-media mention frequency; retail bar/coin demand signals; ETF flow momentum; options activity as a sentiment proxy; sentiment surveys; momentum and trend signals.

**Typical horizon:** Days to years; reflexive loops can be self-sustaining for months.

**Critical design rule for Layer 11:** Layer 11 variables are by nature overlapping with Layer 8 (investment flows), Layer 10 (microstructure), and other layers. The Layer 11 mechanism is the feedback loop itself — the way price and narrative interact to influence the next round of behavior. Admission candidates must be assessed for whether they add reflexivity/sentiment information not already captured by admitted flow or positioning variables. Speculative or social sentiment proxies require careful Criterion C assessment — source quality, consistency, and manipulation risk must be explicitly evaluated.

---

## 4. Admission Criteria — All Five Must Pass

Apply Spec C v2 (`docs/specs/v2/spec_c_variable_admission_criteria_v2.md`). Every candidate must satisfy all five:

**Criterion A — Causal Relevance**
Credible mechanism documented. State: (1) what the variable represents, (2) how it affects gold, (3) expected direction, (4) whether the relationship is conditional or regime-dependent.

**Criterion B — Incremental Information**
The T5 baseline is the full T1 and T3 signed-off registries. Every T5 candidate must demonstrate what it adds beyond variables already admitted. T2 and T4 are in progress — flag overlaps, document reasoning, do not delay your decision.

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

Layer 8, 10, and 11 variables are frequently downstream amplifiers. Amplifier position is a classification matter, not a rejection criterion.

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

## 8. T5-Specific Cross-Layer Risks to Manage

Address each directly in your admission records.

### Layer 8 risks

**L8 / L0 boundary:** L0-003 Gold ETF Holdings is the stock of ETF-held gold. Layer 8 ETF flow variables are the weekly change in that stock. Both can be admitted if their mechanisms are clearly separated — stock ownership vs. marginal flow demand. Do not treat them as duplicates on the basis of sharing the same underlying product.

**L8 / L9 boundary (T4):** Chinese and Indian physical demand flows may appear in both L8 and L9. The L8 mechanism is the investment-allocation flow signal; the L9 mechanism is the regional physical-market pricing and premium behavior. Where the same data point (e.g., Chinese ETF flows) could qualify for both, attribute it to one layer with the stronger mechanism and flag the overlap.

**L8 / L11 boundary:** Retail investment flows and bar/coin demand can carry both a direct flow signal (L8) and a reflexivity/sentiment signal (L11). Avoid double-admitting the same variable in both layers; assign to the layer where the primary mechanism is strongest and flag the secondary mechanism.

### Layer 10 risks

**L10 / L0 boundary:** L0-009 Gold Lease Rates / Forward Rates is already admitted in Layer 0 for its stock-mobility and physical-financing mechanism. If a lease/forward rate variable is being considered in Layer 10 for a microstructure or derivatives-market mechanism (e.g., as a basis signal or market-stress indicator), document the distinct mechanism explicitly. Do not admit it at full independent weight in both layers without a clear mechanism separation.

**L10 / L8 boundary:** ETF flow mechanics (creation/redemption arbitrage, authorized participant behavior) can belong in either Layer 8 or Layer 10 depending on whether the mechanism is the flow as a demand signal (L8) or the market-plumbing and arbitrage dynamic (L10). Attribute explicitly.

**L10 / L11 boundary:** Options activity and positioning can signal microstructure stress (L10) or investor sentiment and reflexivity (L11). Where the same variable serves both purposes, assign to the stronger mechanism and flag the other.

**Amplifier classification:** For each L10 variable, state explicitly in the admission record whether it is being admitted as (a) an amplifier of fundamental moves, (b) a leading positioning signal, or (c) a market-stress/liquidity indicator. This classification matters for how the variable is eventually used in the scoring engine.

### Layer 11 risks

**L11 / L8 boundary:** Retail ETF flows and bar/coin demand can be both a direct demand signal (L8) and a sentiment indicator (L11). See L8/L11 note above — assign to one layer and flag the other.

**L11 Criterion C scrutiny:** Sentiment and search-trend variables carry higher data-quality risk than institutional financial data. Google Trends is subject to manipulation, seasonal noise, and methodology changes. Social-media sentiment proxies are particularly vulnerable. Every L11 candidate must receive an explicit, candid Criterion C assessment — do not admit sentiment variables solely because they are easy to retrieve.

**L11 scope boundary:** Layer 11 is a feedback and amplification layer, not a catch-all for variables that do not fit elsewhere. If a variable's primary mechanism is a direct flow (L8), positioning (L10), or fundamental driver from another layer, it does not belong in L11 merely because it also reflects market psychology.

---

## 9. The 20-Field Admission Record

Complete one record per candidate variable:

```
Variable name:
Layer:
Variable ID:          [Format: L{layer number}-{sequence number}, e.g. L8-001]
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
- Do not re-admit L0-009 Gold Lease Rates in Layer 10 without a distinct, documented mechanism
- Do not re-admit L0-003 Gold ETF Holdings as an L8 flow variable without separating stock from flow mechanism
- Do not treat Layer 11 as a residual catch-all — the mechanism must be reflexivity and sentiment feedback specifically
- Do not admit L11 sentiment variables without a candid Criterion C assessment of data quality and manipulation risk
- Do not pre-empt or duplicate T2 or T4 scope

---

## 11. Deliverable Format

For each layer (8, 10, and 11), deliver:

1. A candidate variable list with brief rationale for why each was considered
2. One complete 20-field admission record per candidate
3. A short layer summary table:

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|

4. Cross-layer overlap notes for the full registry (T5 closes Phase 1; these notes will inform Spec A implementation)

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

## 13. Lessons from T1 and T3 Relevant to T5

- **Amplifier ≠ independent cause.** L10 positioning variables amplify shocks from other layers. Admit them for their amplification mechanism, not as standalone drivers.
- **Stock vs. flow must be separated.** L0-003 ETF Holdings (stock) and L8 ETF flows (change) can coexist if mechanisms are explicitly separated.
- **Sentiment variables require candid Criterion C assessment.** Do not admit on conceptual appeal alone.
- **Mechanism attribution must be explicit.** Three-layer boundary risks (L8/L10/L11) are the defining challenge of T5. Each variable must be assigned to one primary layer with the other mechanisms flagged.
- **Conditional admissions are legitimate.** Strong causal case + weak data or operational constraints = CONDITIONAL, not REJECT.
- **Qualitative flags only.** No numerical D_i, T_i, or γ_ij values in Phase 1.
- **T5 closes Phase 1.** The cross-layer overlap notes in your deliverable will be the primary input for Spec A dependency review. Make them thorough.

---

## 14. Scope Control Reminder (Spec C Section 13)

> **The purpose of variable admission is not to collect every potentially relevant indicator. It is to build the smallest credible set of variables that adequately represents each causal layer and supports the four forecast horizons.**

Bias toward precision over completeness. T5 closes the registry — resist the temptation to broaden scope at the final tranche.

---

**End of T5 Brief**
