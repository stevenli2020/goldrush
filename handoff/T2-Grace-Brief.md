# Gold Probability Engine — Phase 1 T2 Task Brief
**Prepared by:** Chris (Pragmatic Project Advisor)  
**For:** Grace (Task Agent)  
**Tranche:** T2 — Layers 4 and 5  
**Status:** Approved for execution  
**T1 closed:** 2026-08-17

---

## 1. Your Objective

Build the complete variable admission records for **Layers 4 and 5** of the Gold Probability Engine.

Deliver one standardized 20-field admission record per candidate variable, with a final ADMIT / CONDITIONAL / REJECT decision for each.

Same format, same rules as T1. This brief highlights what is new or different for T2.

---

## 2. Criterion B Baseline for T2

The T2 baseline is the **full T1 signed-off registry**.

Every T2 candidate must demonstrate incremental information beyond the 24 T1 variables already admitted or conditionally admitted across Layers 0, 1, and 3.

Authoritative baseline: `docs/phase1-registry/T1-registry.md`

Read this before starting admission records. The most relevant T1 variables for T2 overlap assessment are:

| T1 Variable | Overlap risk with T2 |
|---|---|
| L1-001 10Y TIPS Real Yield | L4 inflation expectations / breakevens |
| L1-002 5Y TIPS Real Yield | L4 breakevens |
| L1-006 Expected Policy Rate | L4 inflation/fiscal variables that transmit through policy |
| L3-001 Fed Funds Futures | L4 inflation surprise → policy repricing |
| L3-002 OIS Forward Curve | L4 fiscal credibility → policy expectations |
| L3-008 Inflation Surprise | L4 inflation-level variables — mechanism distinction critical |
| L0-002 Central-Bank Gold Holdings | L5 official-sector reserve allocation — must remain distinct |

---

## 3. Layers in Scope

### Layer 4 — Inflation, Purchasing Power & Fiscal Credibility

**Role:** Primary structural driver.  
**Primary mechanism:** Two distinct and potentially opposing channels:

**Channel A — Purchasing-power/debasement channel**  
Persistent or accelerating inflation, or deteriorating fiscal credibility, increases gold demand as a store of value when confidence in fiat purchasing power weakens.

**Channel B — Policy-response channel**  
The same inflation shock can be bearish for gold if it triggers expectations of tighter real monetary policy. This channel transmits through Layer 1 (real yields) and Layer 3 (policy expectations).

**Critical distinction for T2:**  
Do NOT treat "high inflation = bullish gold" as a direct relationship. The net gold response depends on which channel dominates. Layer 4 variables should capture the underlying inflation/fiscal conditions. The policy-response transmission belongs in Layers 1 and 3 — do not duplicate it here.

**Key observable categories:**

*Inflation quantity*
- CPI, core CPI, PCE, core PCE

*Inflation expectations*
- 5Y/10Y breakevens, inflation swaps, survey-based expectations

*Fiscal credibility*
- Fiscal deficit/GDP, debt/GDP, interest expense/revenue
- Treasury issuance, maturity structure
- Term-premium indicators

**Typical horizon:** Months to decades; inflation surprises can create fast short-term moves.

**Important distinctions — do not conflate these concepts:**
- Inflation level vs. inflation change vs. inflation surprise vs. inflation expectations
- Central-bank reaction function vs. fiscal credibility
- Short-run inflation shock vs. long-run debasement risk

---

### Layer 5 — Official-Sector Reserve Allocation

**Role:** Structural demand driver; longer-horizon and generally less tactical than private investment demand.  
**Primary mechanism:** Strategic reserve allocation by central banks and other official-sector institutions can create persistent gold demand that is longer-horizon and generally less price-sensitive than speculative flows.

**Critical distinction from Layer 0:**  
- **L0-002 (Central-Bank Gold Holdings)** = stock-level measure of how much gold the official sector owns; belongs to Layer 0's stock/flow architecture.  
- **Layer 5** = the *behavioral and strategic allocation process* — why official institutions are buying or selling, what drives reserve composition decisions, and how those decisions affect gold demand flow.

These are NOT the same variable. Do not admit a variable in Layer 5 that simply duplicates L0-002's stock measure without adding behavioral/flow information.

**Separate these five concepts — they overlap but are not interchangeable:**
1. Physical gold accumulation (the act of buying/holding)
2. Reserve diversification (reducing concentration in any single asset)
3. De-dollarization (specifically reducing USD exposure)
4. Sanctions-risk hedging (protecting reserves from asset-freeze risk)
5. Monetary-system fragmentation (broader shift away from USD-centric reserve architecture)

A central bank may buy gold for reserve diversification without intending to de-dollarize. A country can reduce USD exposure by buying another currency rather than gold. Do not conflate these.

**Key observable categories:**
- Monthly/quarterly official-sector gold purchase volumes
- Gold share of total reserves
- Reserve composition changes
- Stated reserve objectives and central-bank survey responses
- Domestic vs. foreign gold custody arrangements
- Official-sector sales or lending where disclosed

**Typical horizon:** Years to decades; with occasional monthly/quarterly flow effects.

**Important qualification:**  
Central-bank demand is generally more strategic and longer-horizon than private investment demand, but it is **not price-insensitive**. Do not state or imply that official buyers are completely price-independent.

---

## 4. Admission Criteria — All Five Must Pass

Apply Spec C v2. Same as T1. No changes.

**Criterion A — Causal Relevance**  
Credible mechanism documented. For Layer 4: state which channel (purchasing-power or policy-response) the variable operates through. For Layer 5: state which of the five official-sector concepts the variable captures.

**Criterion B — Incremental Information**  
T2 baseline = full T1 approved registry. State explicitly what this variable adds beyond the 24 T1 variables. Pay particular attention to overlap with L1-001, L1-002, L3-001, L3-002, L3-008, and L0-002.

**Criterion C — Data/Evidence Reliability**  
Same standard as T1.

**Criterion D — Operational Feasibility**  
Same standard as T1. Note that some Layer 5 variables (e.g. central-bank purchase data) have significant publication lags — assess freshness carefully.

**Criterion E — Forecast-Horizon Relevance**  
Layer 4 variables may span short (event-driven inflation surprises) to very long (fiscal credibility) horizons. Layer 5 variables are predominantly long-horizon. Specify relevant horizon(s) for each variable.

---

## 5. Hard Rule — Do Not Reject on Correlation or Downstream Position Alone

Same rule as T1:

> **Do not reject a variable solely because it is downstream of or correlated with another variable. Reject only when it fails the incremental-information test or another Spec C criterion.**

Specifically for T2:
- Breakevens may transmit from CPI but still add incremental forward-looking information → do not reject on transmission grounds alone
- Layer 5 purchase flows may partially reflect the same demand captured in L0-002 → assess incremental information, do not auto-reject

---

## 6. Overlap Classification (Qualitative Only)

Same flags as T1:

| Flag | Meaning |
|---|---|
| **Duplicate candidate** | Materially represents the same information as another variable |
| **Transmission candidate** | Downstream of an upstream driver; may carry incremental information |
| **Interaction candidate** | Joint effect with another variable not representable by adding independent contributions |

**Do NOT assign numerical D_i or T_i values.**  
**Do NOT reject a variable solely because it receives a flag.**

For Layer 4: variables that appear in both L4 and L3 (e.g. breakevens) must have explicit mechanism/channel ownership documented. The same data series may legitimately appear in two layers if the mechanism differs. State the L4-specific mechanism clearly.

For Layer 5: flag any variable that overlaps with L0-002 and document whether it adds behavioral/flow information (L5) or merely restates stock-level holdings (L0).

---

## 7. Range Propensity Flag (New in T2)

Spec B requires that Range Propensity inputs be drawn from Phase 1 approved variables. Range Propensity candidate inputs include: realized volatility, ATR or comparable range measure, directional persistence/trend strength, breakout/range behavior, market-structure stress.

These variables will primarily appear in T5 (Layers 8, 10, 11). However, if any T2 candidate variable is also relevant as a Range Propensity input, add the following flag to its admission record:

> **Range Propensity candidate: Yes / No**

This does not affect the ADMIT/CONDITIONAL/REJECT decision. It is a forward reference for Phase 5 pre-conditions.

---

## 8. The 20-Field Admission Record

Same template as T1:

```
Variable name:
Layer:
Variable ID:          [Format: L4-001, L4-002 ... / L5-001, L5-002 ...]
Causal mechanism:
Direction:            [Positive / Negative / Conditional]
Incremental information:
Overlap:              [List overlapping T1 or T2 variables + qualitative flag]
Data/evidence source:
Reliability:
Historical depth:
Frequency:
Freshness:
Accessibility:        [Free / Crawlable / Paid / Restricted]
Operational burden:   [Low / Medium / High]
Relevant horizons:    [One or more of the four fixed horizons]
Initial weight rationale:
Evidence references:
Decision:             [ADMIT / CONDITIONAL / REJECT]
Review date:
Reviewer:
Range Propensity candidate: [Yes / No]
```

Note: Range Propensity candidate field is added for T2 onwards.

---

## 9. What You Are NOT Doing

- Do not modify the 12-layer architecture
- Do not assign or change layer-level weights
- Do not assign numerical D_i or T_i values
- Do not assign γ_ij interaction coefficients
- Do not fabricate historical quantitative data
- Do not reference v1 specs
- Do not treat "high inflation = bullish gold" as a direct causal rule
- Do not conflate Layer 5 reserve-allocation behavior with Layer 0 stock-level holdings
- Do not conflate de-dollarization, reserve diversification, sanctions hedging, and monetary fragmentation as a single variable
- Do not state that official-sector buyers are price-insensitive

---

## 10. Deliverable Format

Same as T1. For each layer (4, 5), deliver:
1. Candidate variable list with one-line rationale per candidate — **submit for review before starting admission records**
2. One complete 20-field admission record per approved candidate
3. Per-layer summary table:

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) | Range Propensity |
|---|---|---|---|---|---|

4. Cross-layer notes relevant to T3 (Layers 2 and 7)

---

## 11. Authoritative References

| Document | Location | Use |
|---|---|---|
| T1 Registry | `docs/phase1-registry/T1-registry.md` | Criterion B baseline |
| Causal model | `docs/gold_price_causal_model_v2_2.md` | Layer definitions, observables, mechanisms |
| Spec C v2 | `docs/specs/v2/spec_c_variable_admission_criteria_v2.md` | Admission criteria |
| Spec A v2 | `docs/specs/v2/spec_a_interaction_dependency_rules_v2.md` | Overlap classification |
| Spec B v2 | `docs/specs/v2/spec_b_three_state_probability_model_v2.md` | Range Propensity context |
| Handoff | `handoff/Claude-Handoff.md` | SSOT and lessons |

Do not reference v1 specs.

---

## 12. Scope Control Reminder

> **The purpose of variable admission is not to collect every potentially relevant indicator. It is to build the smallest credible set of variables that adequately represents each causal layer and supports the four forecast horizons.**

Layer 4 has many potential candidates (every inflation and fiscal metric). Apply the incremental-information test strictly. Bias toward the smallest set that adequately represents the purchasing-power and fiscal-credibility mechanisms without duplicating T1 policy-path variables.

---

**First deliverable: candidate variable list for Layers 4 and 5. Do not start admission records until the list is reviewed and approved.**

**End of T2 Brief**
