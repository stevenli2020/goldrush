# Gold Probability Engine — Phase 1 T3 Task Brief
**Prepared by:** Chris (Pragmatic Project Advisor)
**For:** Grace (Task Agent)
**Tranche:** T3 — Layers 2 and 7
**Status:** Approved for execution

---

## 1. Your Objective

Build the complete variable admission records for **Layers 2 and 7** of the Gold Probability Engine.

Deliver one standardized 20-field admission record per candidate variable, with a final ADMIT / CONDITIONAL / REJECT decision for each.

---

## 2. Where T3 Sits in the Registry Sequence

| Tranche | Layers | Status |
|---|---|---|
| T1 | 0, 1, 3 | CLOSED — signed off 2026-08-17 |
| T2 | 4, 5 | IN PROGRESS |
| T3 | 2, 7 | **OPEN — this tranche** |
| T4 | 6, 9 | Not started |
| T5 | 8, 10, 11 | Not started |

Your Criterion B baseline is the **full T1 approved registry** (`docs/phase1-registry/T1-registry.md`). T2 is in progress and its registry is not yet signed off. Do not treat T2 candidates as part of your baseline. If a T3 candidate overlaps with a known T2 candidate area, flag the overlap and note that the T2 decision is pending — do not block your own admission on it.

---

## 3. Layers in Scope

### Layer 2 — US Dollar and Global FX Regime

**Role:** Transmission and amplification layer.

**Primary mechanism:** The USD affects gold through at least four distinct channels:

1. **Mechanical translation** — gold is quoted in USD; a stronger dollar immediately raises the local-currency cost of gold for non-US buyers.
2. **Relative purchasing power** — USD strength makes dollar-priced gold more expensive for non-US buyers, directly affecting demand.
3. **US monetary policy transmission** — USD strength often reflects the same monetary-policy expectations that affect real yields; this creates a causal dependency with Layer 1 and Layer 3.
4. **Global dollar liquidity** — funding stress can force investors to liquidate gold to obtain USD cash, causing gold and the dollar to move together during acute crises.

**Key observable categories:** DXY; EUR/USD; USD/JPY; USD/CNY; emerging-market FX stress; cross-currency basis; broad dollar funding indicators.

**Typical horizon:** Intraday to multi-year.

**Critical design rule for Layer 2:** DXY is not always an independent cause. In many episodes it is a downstream transmission variable reflecting monetary and global-liquidity conditions. Your admission records must state which mechanism each variable is capturing and flag the dependency relationship with Layer 1 (real yields), Layer 3 (monetary policy expectations), and Layer 7 (global liquidity) explicitly. Do not treat all FX variables as independent bullion-price drivers.

---

### Layer 7 — Global Liquidity and Financial Conditions

**Role:** Macro amplifier and regime-conditioning layer.

**Primary mechanism:** Liquidity affects both the willingness to own gold and the ability to finance positions. The effect of any rate environment cannot be interpreted independently of the prevailing liquidity regime. Key distinguishing insight: during acute funding crises, gold can initially be sold to raise cash, even when its longer-term fundamental outlook is improving. The monetary-policy response to a liquidity crisis is then often bullish for gold. Layer 7 captures this two-phase dynamics.

**Key observable categories:** Central-bank balance sheets (Fed, ECB, PBoC); global M2; bank credit; credit spreads; repo conditions (SOFR, repo rates); Treasury General Account (TGA); reverse-repo balances; global financial-conditions indices; cross-border capital flows.

**Typical horizon:** Days to years.

**Critical design rule for Layer 7:** Global liquidity overlaps substantially with Layer 3 (monetary policy expectations) because central-bank balance-sheet expansion is itself a monetary-policy tool. Variables must be assessed for what they add beyond Layer 3 monetary expectations. The mechanism that belongs in Layer 7 is realized liquidity conditions and financial-system stress — not the forward policy-path expectation, which belongs in Layer 3.

---

## 4. Admission Criteria — All Five Must Pass

Apply Spec C v2 (`docs/specs/v2/spec_c_variable_admission_criteria_v2.md`). Every candidate must satisfy all five:

**Criterion A — Causal Relevance**
Credible mechanism documented. State: (1) what the variable represents, (2) how it affects gold, (3) expected direction, (4) whether the relationship is conditional or regime-dependent.

**Criterion B — Incremental Information**
The T3 baseline is the full T1 signed-off registry. Every T3 candidate must demonstrate what it adds beyond the variables already admitted in T1. T2 is in progress — if a T3 candidate overlaps with a probable T2 variable, flag the overlap and document your reasoning; do not delay your decision on that account.

State explicitly: *What does this variable add that the T1 registry and the 12-layer causal architecture do not already adequately capture?*

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

Layer 2 and Layer 7 variables will often be downstream of monetary-policy or macro shocks. Transmission position is a classification matter (handled in Overlap, below), not a rejection criterion.

---

## 7. Overlap Classification (Qualitative Only)

When a variable shares information with another candidate or approved variable, classify the relationship using one of three qualitative flags:

| Flag | Meaning |
|---|---|
| **Duplicate candidate** | Materially represents the same information as another variable; combined effective weight should not double-count |
| **Transmission candidate** | Downstream of an upstream driver; transmits part of the same shock but may carry incremental information |
| **Interaction candidate** | Joint effect with another variable that cannot be represented by adding independent contributions alone |

**Do NOT assign numerical D_i or T_i values.** That belongs to Spec A implementation in a later phase.
**Do NOT reject a variable solely because it receives a flag.**

For variables that appear in multiple layers: record the mechanism/channel that justifies its role in THIS layer specifically.

---

## 8. T3-Specific Cross-Layer Risks to Manage

These are the primary attribution risks for your two layers. Address each directly in your admission records.

### Layer 2 risks

**L2 / L1 boundary:** Real yield changes and DXY changes often move together because they share a common upstream cause (monetary policy). A DXY variable is not mechanically redundant with a real-yield variable — it adds currency-valuation and non-US-buyer purchasing-power information — but the dependency must be flagged and the transmission chain documented.

**L2 / L3 boundary:** If a Layer 2 variable is being used as a signal of monetary-policy expectations (e.g., DXY strength as a proxy for expected Fed tightening), that mechanism belongs in Layer 3. The Layer 2 mechanism must be the FX channel itself — the currency's effect on gold demand, purchasing power for non-US buyers, or dollar-liquidity conditions.

**L2 / L7 boundary:** Dollar funding stress overlaps with Layer 7 (global liquidity). Cross-currency basis and USD liquidity variables require explicit mechanism attribution: if the mechanism is FX pricing and purchasing-power transmission, the variable belongs in Layer 2; if the mechanism is realized funding-market stress and balance-sheet constraints, it belongs in Layer 7.

### Layer 7 risks

**L7 / L3 boundary:** This is the highest-risk boundary in T3. Central-bank balance sheets and QE expectations can appear in both layers. The Layer 3 mechanism is the expected forward policy path and its repricing. The Layer 7 mechanism is the resulting realized liquidity conditions, funding stress, and financial-system capacity to hold risk assets — these are distinct. A Fed balance-sheet variable used as a signal of expected future easing belongs in L3. The same variable used to measure current excess reserves, system liquidity, or market functioning belongs in L7.

**L7 / L8 boundary (future T5):** Investment flows (Layer 8) will be covered in T5. Avoid pre-empting Layer 8 by admitting flow variables in Layer 7. Layer 7 should capture liquidity conditions and financial-system capacity, not the resulting asset flows themselves.

**L7 / L1 boundary:** Credit spreads can affect gold via financial-conditions channels (Layer 7) or via their effect on real rates and opportunity cost (Layer 1). The mechanism must be attributed explicitly.

---

## 9. The 20-Field Admission Record

Complete one record per candidate variable:

```
Variable name:
Layer:
Variable ID:          [Format: L{layer number}-{sequence number}, e.g. L2-001]
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
- Do not treat Layer 2 as a residual "everything FX" bucket — apply the four-channel mechanism framework
- Do not treat Layer 7 as a residual "everything macro" bucket — the mechanism is realized liquidity conditions and financial-system stress, not policy expectations
- Do not pre-empt T4 (Layers 6, 9) or T5 (Layers 8, 10, 11) scope

---

## 11. Deliverable Format

For each layer (2 and 7), deliver:

1. A candidate variable list with brief rationale for why each was considered
2. One complete 20-field admission record per candidate
3. A short layer summary table:

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|

4. Cross-layer overlap notes relevant to T4 and T5 (for review before those tranches open)

---

## 12. Authoritative References

| Document | Location | Use |
|---|---|---|
| Causal model | `docs/gold_price_causal_model_v2_2.md` | Layer definitions, mechanisms, observables |
| Spec C v2 | `docs/specs/v2/spec_c_variable_admission_criteria_v2.md` | Admission criteria and decision rules |
| Spec A v2 | `docs/specs/v2/spec_a_interaction_dependency_rules_v2.md` | Overlap classification reference |
| Handoff | `handoff/Claude-Handoff.md` | SSOT and lessons |
| T1 Registry | `docs/phase1-registry/T1-registry.md` | Criterion B baseline — the current approved variable set |

Do not reference v1 specs.

---

## 13. Lessons from T1 Relevant to T3

These are patterns from T1 that apply directly to T2 and T3 work.

- **Shared observables do not mean the same layer.** L1 and L3 share observables (e.g., OIS, policy rates). They were not collapsed because their mechanisms differ. Apply the same discipline to Layer 2 and Layer 7.
- **Transmission position is not a rejection criterion.** DXY is partly downstream of monetary policy. That is a flag, not a reason to reject.
- **Mechanism attribution must be explicit in every record.** When a variable could belong in more than one layer, state clearly why it belongs in THIS layer.
- **Conditional admissions are legitimate.** If a variable has a strong causal case but operational or data constraints exist, CONDITIONAL is the correct decision — not REJECT.
- **Qualitative flags only.** No numerical D_i, T_i, or γ_ij values in Phase 1.

---

## 14. Scope Control Reminder (Spec C Section 13)

> **The purpose of variable admission is not to collect every potentially relevant indicator. It is to build the smallest credible set of variables that adequately represents each causal layer and supports the four forecast horizons.**

Bias toward precision over completeness. A shorter, well-evidenced registry is preferable to a long list of weakly supported variables.

---

**End of T3 Brief**
