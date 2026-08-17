# Gold Probability Engine — Pre-Phase-1 Architecture Proposal

## Purpose

This document consolidates the current agreed design decisions before Phase 1 begins. It is intended for external AI Agent review.

The review should identify material architectural flaws, ambiguities, omissions, or implementation risks without unnecessarily expanding project scope.

## 1. Core Objective

Run the system once each week, on Saturday or Sunday after the New York gold market close, and produce a systematic probability outlook for **USD gold spot price per troy ounce** across four horizons:

1. 1–5 days
2. 1–3 months
3. 1–3 years
4. 3–10 years

The primary outcome is a three-class probability:

- Bullish
- Consolidation / Range-bound
- Bearish

For each horizon:

> P(Bullish) + P(Consolidation) + P(Bearish) = 100%

The exact quantitative definition of the consolidation band will be established during implementation and should be appropriate to each horizon.

## 2. Weekly Operating Cycle

The live run may use the **full currently available information set**, rather than only newly published information.

All evidence and observations must retain relevant timestamps, including publication/availability time where applicable.

Conceptually:

```text
Collect / refresh data
        ↓
Validate freshness and quality
        ↓
Process quantitative variables
        ↓
AI assessment of analytical variables
        ↓
Calculate variable signals
        ↓
Calculate layer scores
        ↓
Apply horizon-specific scoring
        ↓
Assess interactions / current regime
        ↓
Add historical evidence and counterexamples
        ↓
Calculate 3 outcome probabilities
        ↓
Generate weekly report
        ↓
Archive complete run
```

## 3. Locked 12-Layer Causal Framework

### Layer 0 — Gold Stock/Flow Architecture
Existing above-ground gold stock, ownership distribution, and marginal willingness to buy, hold, or sell.

### Layer 1 — Real Rates / Opportunity Cost
Real yields and relative attractiveness of holding a non-yielding asset.

### Layer 2 — USD / FX
US dollar valuation and currency effects on the global gold price.

### Layer 3 — Monetary-Policy Expectations
Expected future policy paths rather than merely current policy rates.

### Layer 4 — Inflation, Purchasing Power & Fiscal Credibility
Inflation, inflation expectations, fiscal sustainability, debt dynamics, and monetary-confidence effects.

### Layer 5 — Official-Sector Reserve Allocation
Central-bank purchases, reserve diversification, sanctions/reserve-security considerations, and official-sector behavior.

### Layer 6 — Geopolitical Transmission
Four principal channels:
1. Safe-haven demand
2. Energy / inflation transmission
3. Reserve-security effects
4. Monetary-system fragmentation

### Layer 7 — Global Liquidity & Financial Conditions
Global liquidity, credit conditions, funding conditions, monetary-system liquidity, and financial stress.

### Layer 8 — Investment Flows
Gold ETFs, bars/coins, institutional flows, and other investment demand.

### Layer 9 — Regional Physical Markets
China, India, local premiums, seasonal demand, and regional physical-market conditions.

### Layer 10 — Market Microstructure & Derivatives
COMEX, futures, options, positioning, systematic flows, dealer activity, and related market mechanics.

### Layer 11 — Expectations, Psychology & Reflexivity
Narrative, fear, FOMO, confidence, momentum, and price-to-expectation feedback loops.

**Principle:** the 12 layers are causal families, not 12 independent predictors. The scoring system must avoid double-counting the same underlying shock through multiple observables.

## 4. Expandable Variables

The 12 layers remain locked, but the variables inside each layer are deliberately expandable.

A new variable may be added when research establishes that it provides meaningful incremental value.

Adding a variable should normally result in:

> research / validation → worker implementation → layer integration → redistribution of weights within that layer

It should **not automatically change other layer weights**.

Cross-layer or layer-level changes require separate research evidence and review.

## 5. Variable Types

### Quantitative variables
Can be retrieved and/or calculated deterministically.

Examples: DXY, real yields, CPI, breakevens, ETF flows, oil, VIX, CFTC positioning, gold momentum, regional premiums.

### Analytical variables
Require evidence interpretation.

Examples: geopolitical escalation, sanctions implications, monetary fragmentation, fiscal credibility, policy-regime interpretation.

### Composite variables
Derived from multiple quantitative and/or analytical inputs.

Examples: monetary-policy pressure, geopolitical pressure, liquidity-regime score.

Composite variables must remain traceable to their inputs.

## 6. Variable-Level Output

Each variable produces:

- **Stance:** Bullish `+1.0`, Neutral `0.0`, Bearish `-1.0`
- **Confidence:** `0.0–1.0`
- **Variable weight:** importance of the variable within its layer

Direction and confidence are separate dimensions.

## 7. Layer Score

For variable i in layer k:

$$
L_k =
rac{
\sum_{i=1}^{N_k}(w_i S_i C_i)
}{
\sum_{i=1}^{N_k}w_i
}
$$

with:

$$
-1 \le L_k \le +1
$$

Interpretation:

- `+1.00` = maximum bullish consensus
- `0.00` = balanced / neutral
- `-1.00` = maximum bearish consensus

Initial variable weights are research-derived and may be refined later.

## 8. Interaction and Weight Adjustment

This part must be explicitly designed before implementation.

Three relationships must be distinguished:

### A. Duplicate information
Two variables substantially measure the same information. Their effective combined contribution should be controlled to avoid double-counting.

### B. Causal transmission
One variable is partly downstream of another.

Example:

```text
Fed expectations
      ↓
Real yields
      ↓
USD
      ↓
Gold
```

Downstream variables should not automatically receive full independent causal weight when they mainly transmit the same shock.

### C. Genuine interaction
Two variables jointly create a materially different effect from their individual effects.

Example:

> Rising real yields while geopolitical risk is exceptionally high.

### Proposed structure

```text
Research-derived base weight
        ↓
Dependency / duplicate-information adjustment
        ↓
Causal-transmission adjustment
        ↓
Interaction adjustment
        ↓
Effective contribution
```

Correlation alone must not automatically reduce weights. The objective is to prevent double-counting while preserving genuinely independent and interaction-driven information.

The exact mathematical implementation will be specified before coding.

## 9. Layer-to-System Combination

Each layer receives a macro weight W_k:

$$
\sum_{k=1}^{12} W_k = 1
$$

Intermediate system index:

$$
S_{total}=\sum_{k=1}^{12}(W_kL_k)
$$

with:

$$
-1 \le S_{total} \le +1
$$

This is an intermediate analytical index, not the final probability.

The final output is:

- P(Bullish)
- P(Consolidation)
- P(Bearish)

with the three probabilities summing to 100%.

## 10. Horizon-Specific Weights

Layer importance will differ by forecast horizon.

Thus the system maintains horizon-specific layer weights for:

- 1–5 days
- 1–3 months
- 1–3 years
- 3–10 years

The initial weights are research-derived.

## 11. Historical Evidence

Historical events and regimes are **not** intended to become a universal quantitative ML dataset.

Historical evidence is primarily used to ask:

- Have comparable mechanisms occurred before?
- What happened?
- What are the similarities?
- What are the important differences?
- What are the counterexamples?
- Does the evidence strengthen or weaken current confidence?

Historical analogy must not automatically change model weights.

A lack of reliable historical quantitative data must not be filled with present-day AI judgment and treated as genuine historical data.

## 12. Research-Derived Initial Weights

Initial variable and layer weights are established through extensive research, including:

- economic literature;
- historical evidence;
- institutional research;
- empirical studies where available;
- mechanism strength;
- persistence;
- horizon relevance;
- evidence quality.

They are research-derived priors, not automatically discovered ML weights.

Each important weight should have documented rationale and evidence.

## 13. Adaptive Weight Feedback

The production system records every forecast and its eventual outcome.

After sufficient observations, it can evaluate:

- repeated over/underweighting;
- layer contribution errors;
- regime changes;
- whether the signal or the weight was wrong;
- missed interactions;
- data-quality issues.

The system produces a **Weight Refinement Proposal**, rather than changing weights automatically.

Conceptually:

```text
Forecast
   ↓
Actual outcome
   ↓
Error / outcome diagnosis
   ↓
Repeated pattern detection
   ↓
Research review
   ↓
Weight-refinement proposal
   ↓
Approval / implementation
```

A single failed forecast should not automatically change weights.

## 14. AI Agent Architecture

The system uses a balanced AI role:

> Quantitative data is the backbone; AI provides structured interpretation where deterministic variables cannot adequately represent the phenomenon.

### Research stage
Specialist research agents may handle groups of layers, followed by a synthesis/review agent.

### Variable implementation stage

Each variable is an independent work package.

A **Worker Agent** is responsible for:

- research;
- source validation;
- retrieval/calculation code;
- processing logic;
- tests;
- brief usage manual;
- handoff document;
- assumptions and limitations.

A worker is released once its deliverable is accepted.

A **Layer Manager Agent**:

- assigns variable work;
- reviews deliverables;
- validates consistency;
- integrates variables;
- manages weights within the layer;
- resolves conflicts;
- commissions future rework.

Worker agents do not independently change the 12-layer architecture or cross-layer weights.

## 15. Random Forest

Random Forest is **not the core forecasting engine**.

Its intended role is a later supporting diagnostic, if enough reliable data exists.

The question it should answer is:

> Are there nonlinear relationships or interactions among our existing variables that the research-derived scoring model is missing?

Potential examples:

- real rates × geopolitical conditions;
- DXY × positioning;
- liquidity × monetary-policy expectations.

A Random Forest finding becomes a research item for review. It does not automatically become a new model weight.

If sufficient data does not exist, especially for long horizons, Random Forest is simply not used.

## 16. Weekly Report

Proposed structure:

```markdown
# Gold Market Outlook
Reference Price: $X,XXX/oz

| Horizon | P(Bullish) | P(Consolidation) | P(Bearish) | Signal Strength | Primary Drivers |
|---|---:|---:|---:|---|---|
| 1–5 Days | XX% | XX% | XX% | ... | ... |
| 1–3 Months | XX% | XX% | XX% | ... | ... |
| 1–3 Years | XX% | XX% | XX% | ... | ... |
| 3–10 Years | XX% | XX% | XX% | ... | ... |

## System Summary

## Main Bullish Forces

## Main Bearish Forces

## Layer Summary

Brief assessment of all 12 layers.

## Historical Evidence

Relevant historical comparisons and counterexamples.

## Important Weekly Developments

## Confidence / Limitations
```

## 17. Project Phases

This is one project, implemented progressively.

### Phase 1 — Variable Registry
Define variables, sources, mechanisms, horizon relevance, quality, and initial weights.

### Phase 2 — Data Ingestion
Build automated collection and validation for quantitative variables.

### Phase 3 — AI Evidence Engine
Build standardized assessment of analytical variables.

### Phase 4 — Scoring Engine
Implement:

> Variable → Layer → Horizon → System score

including interaction and weight-adjustment logic.

### Phase 5 — Probability Engine
Produce the three probabilities for all four horizons.

### Phase 6 — Weekly Production Engine
Automate the full Saturday/Sunday workflow and report.

### Phase 7 — Feedback & Weight Refinement
Track realized outcomes and periodically generate evidence-based refinement proposals.

## 18. Scope Discipline

The project is focused on:

> **A weekly gold-price probability assessment system for USD gold spot across four future horizons.**

The following are not objectives unless later shown necessary:

- automated portfolio allocation;
- automated trading;
- intraday trading;
- prediction of unrelated assets;
- excessive ML model expansion;
- uncontrolled social-media sentiment scraping;
- artificial reconstruction of unreliable historical datasets;
- autonomous self-modifying weights.

Future changes should be justified by the project's actual performance and requirements.

## 19. External Review Questions

Please review only for material issues affecting design, implementation, reliability, or usefulness.

1. Is the three-outcome probability framework (Bullish / Consolidation / Bearish) appropriate?
2. Is the Variable → Layer → Horizon → System architecture sound?
3. Is the treatment of duplicate information, causal transmission, and genuine interaction sufficiently defined?
4. Is research-derived weighting plus controlled feedback-based refinement preferable to automatic historical backtest optimization for this project?
5. Is the role of historical evidence appropriate given uneven historical data availability?
6. Is Random Forest correctly positioned as a supporting diagnostic?
7. Is the worker-agent / layer-manager implementation model practical?
8. Are there any critical omissions, contradictions, or implementation risks?

Please prioritize **material issues over optional enhancements**. The project should remain achievable, auditable, and tightly aligned with its objective.
