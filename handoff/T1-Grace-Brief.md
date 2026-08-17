# Gold Probability Engine — Phase 1 T1 Task Brief
**Prepared by:** Chris (Pragmatic Project Advisor)  
**For:** Grace (Task Agent)  
**Tranche:** T1 — Layers 0, 1, 3  
**Status:** Approved for execution

---

## 1. Your Objective

Build the complete variable admission records for **Layers 0, 1, and 3** of the Gold Probability Engine.

Deliver one standardized 20-field admission record per candidate variable, with a final ADMIT / CONDITIONAL / REJECT decision for each.

---

## 2. Layers in Scope

### Layer 0 — Gold's Stock/Flow Monetary Architecture
**Role:** Foundational. Defines the stock/flow reality that all other layers must interpret.  
**Primary mechanism:** Gold price formation depends heavily on the willingness of existing holders (central banks, ETFs, households, bullion banks) to buy, hold, or sell the existing above-ground stock. Annual mine supply matters but is secondary to stock ownership behavior.  
**Key observable categories:** above-ground stock estimates, central-bank holdings, ETF holdings, household/jewelry holdings, bar-and-coin ownership, recycling flows, producer hedging, vaulted vs. mobile holdings.  
**Typical horizon:** Years to decades for structure; days to months when stock becomes active.

### Layer 1 — Real Interest Rates and Opportunity Cost
**Role:** Primary macro driver.  
**Primary mechanism:** Gold has no coupon or dividend. When expected real returns on competing assets rise, the opportunity cost of holding gold rises. The relationship is regime-dependent — geopolitical stress, banking crises, or fiscal-confidence shocks can cause gold and real yields to move together.  
**Stronger formulation:** Gold tends to weaken when the expected real return on competing high-quality assets rises relative to the expected return from holding gold, all else equal.  
**Key observable categories:** 10Y TIPS yield, 5Y TIPS yield, forward real rates, real yield curve, term premium, expected policy rate.  
**Typical horizon:** Intraday to multi-year.

### Layer 3 — Monetary Policy Expectations
**Role:** Primary macro driver, distinct from Layer 1.  
**Primary mechanism:** Gold reacts to revisions in the expected *future* path of real policy rates and liquidity conditions — not just the current rate. A central bank can hold rates unchanged while gold rallies because the expected forward path becomes more dovish.  
**Core principle:** Gold responds to changes in expectations, not merely changes in current policy.  
**Key observable categories:** Fed Funds futures, OIS curves, dot plots, FOMC statements, speeches, terminal-rate expectations, probability distributions around future meetings.  
**Typical horizon:** Minutes to years; strongest effect around policy and macro-data events.  
**Important:** Layer 1 and Layer 3 share some observables (TIPS, OIS). They are NOT the same layer. Layer 3 is about the expected forward path; Layer 1 is about the current real opportunity cost. Do not collapse them. Preserve both when they represent different mechanisms.

---

## 3. Admission Criteria — All Five Must Pass

Apply Spec C v2. Every candidate must satisfy all five:

**Criterion A — Causal Relevance**  
Credible mechanism documented. State: (1) what the variable represents, (2) how it affects gold, (3) expected direction, (4) whether the relationship is conditional or regime-dependent.

**Criterion B — Incremental Information**  
During T1, the baseline is: the locked 12-layer causal architecture + all other T1 candidates under consideration.  
State explicitly: *What does this variable add that the current set does not adequately capture?*  
A variable may qualify if it measures the same phenomenon more directly, at different frequency, with earlier signal, or captures a different transmission channel.

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

## 4. Admission Decisions

| Decision | Meaning |
|---|---|
| **ADMIT** | All five criteria sufficiently satisfied. Variable proceeds to implementation with initial research-derived weight. |
| **CONDITIONAL / RESEARCH ONLY** | Causal case is useful but one or more implementation criteria not yet strong enough for production. Retained in research registry only. |
| **REJECT** | Fails one or more fundamental criteria. |

---

## 5. Hard Rule — Do Not Reject on Correlation or Downstream Position Alone

> **Do not reject a variable solely because it is downstream of or correlated with another variable. Reject only when it fails the incremental-information test or another Spec C criterion.**

Downstream ≠ redundant. A transmission variable that adds incremental information should be admitted or conditionally admitted, not rejected because it partially reflects an upstream driver.

---

## 6. Overlap Classification (Qualitative Only)

When a variable shares information with another candidate or approved variable, classify the relationship using one of three qualitative flags:

| Flag | Meaning |
|---|---|
| **Duplicate candidate** | Materially represents the same information as another variable; combined effective weight should not double-count |
| **Transmission candidate** | Downstream of an upstream driver; transmits part of the same shock but may carry incremental information |
| **Interaction candidate** | Joint effect with another variable that cannot be represented by adding independent contributions alone |

**Do NOT assign numerical D_i or T_i values.** Numerical dependency/interaction treatment belongs to Spec A implementation in a later phase.  
**Do NOT reject a variable solely because it receives a flag.** The flag is for classification; the admission decision is still determined by the five Spec C criteria.

For variables where the same observable appears in multiple layers (e.g., oil, VIX, OIS rates): record the mechanism/channel that justifies its role in THIS layer specifically. A variable may legitimately appear in more than one layer if it serves a distinct mechanism in each.

---

## 7. The 20-Field Admission Record

Complete one record per candidate variable:

```
Variable name:
Layer:
Variable ID:          [Format: L{layer number}-{sequence number}, e.g. L1-001]
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

## 8. What You Are NOT Doing

- Do not modify the 12-layer architecture
- Do not assign or change layer-level weights
- Do not assign numerical D_i or T_i values
- Do not assign γ_ij interaction coefficients
- Do not fabricate historical quantitative data
- Do not reference v1 specs for any decision
- Do not use correlation alone as grounds for rejection or interaction flagging
- Do not collapse Layer 1 and Layer 3 because they share observables

---

## 9. Deliverable Format

For each layer (0, 1, 3), deliver:
1. A candidate variable list with brief rationale for why each was considered
2. One complete 20-field admission record per candidate
3. A short layer summary table:

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|

4. Any cross-layer overlap notes relevant to T2 (for Chris/Grace to review before T2 opens)

---

## 10. Authoritative References

| Document | Location | Use |
|---|---|---|
| Causal model | `docs/gold_price_causal_model_v2_2.md` | Layer definitions, observables, mechanisms |
| Spec C v2 | `docs/specs/v2/spec_c_variable_admission_criteria_v2.md` | Admission criteria and decision rules |
| Spec A v2 | `docs/specs/v2/spec_a_interaction_dependency_rules_v2.md` | Overlap classification reference |
| Handoff | `handoff/Claude-Handoff.md` | SSOT and lessons |

Do not reference v1 specs.

---

## 11. Scope Control Reminder (Spec C Section 13)

> **The purpose of variable admission is not to collect every potentially relevant indicator. It is to build the smallest credible set of variables that adequately represents each causal layer and supports the four forecast horizons.**

Bias toward precision over completeness. A shorter, well-evidenced registry is preferable to a long list of weakly supported variables.

---

**End of T1 Brief**
